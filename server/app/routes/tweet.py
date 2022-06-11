from typing import List, Optional
import os
import pandas as pd
import requests
from concurrent import futures
from time import time as time_
from konlpy.tag import Okt
from collections import Counter
from itertools import chain
from fastapi import APIRouter
from datetime import timedelta, datetime
from starlette.responses import JSONResponse
from app.utils.examples import get_count_responses
from collections import defaultdict
import re
import random
import boto3

router = APIRouter(prefix='/tweet')
bearer_token = os.environ.get('BEARER_TOKEN')
BUCKET_NAME_STRING = 'kinesis-bucket2'
FOLDER_NAME = 'kinesis-bucket2'
stop_words = open('routes/stopwords.txt', 'r').read().split('\n')
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')


#result_top_ten default set
result_top_ten = [{'tag': '크리스마스', 'count': 104}, {'tag': '진짜', 'count': 96}, {'tag': '사람', 'count': 85}, {'tag': '방탄소년단', 'count': 63}, {'tag': '하나', 'count': 62}, {'tag': '포스트', 'count': 59}, {'tag': '오늘', 'count': 52}, {'tag': '생각', 'count': 48}, {'tag': '사랑', 'count': 45}, {'tag': '우리', 'count': 42}]

s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

s3 = boto3.resource(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)
my_bucket = s3.Bucket(BUCKET_NAME_STRING)


def get_stream_from_s3():
    result = ""

    for my_bucket_object in my_bucket.objects.all():
        FILE_NAME_STRING = my_bucket_object.key
        s3_response_object = s3_client.get_object(Bucket=BUCKET_NAME_STRING, Key=FILE_NAME_STRING)
        object_content = s3_response_object['Body'].read()
        decoded_object_content = object_content.decode()
        result = result + decoded_object_content
    return result


def select_text(resultstr):
    pattern = re.compile("\'text\':\s\'(.*?)\\'},")
    result_list = pattern.findall(resultstr)
    return result_list


def cleaning(result_list):
    df = pd.DataFrame(result_list)
    df = df.replace("[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]", "", regex=True)
    df = df.dropna(axis=0)
    cleaned_resultstr = ''
    for content in df[0]:
        cleaned_resultstr = cleaned_resultstr + content
    return cleaned_resultstr


def preprocess(cleaned_resultstr):
    nlpy = Okt()
    nouns = nlpy.nouns(cleaned_resultstr)
    nouns = [token for token in nouns if not token in stop_words]
    return nouns


def count_nouns(nouns):
    count = Counter(nouns)
    return count


def most_common_top_ten(count):
    tag_count = []
    tags= []
    for n, c in count.most_common():
        dics = {'tag': n, 'count': c}
        if len(dics['tag']) >= 2 and len(tags) <= 49:
            if (len(tag_count) == 10):
                break
            tag_count.append(dics)
            tags.append(dics['tag'])
    return tag_count


async def get_request(url, auth, params):
    return requests.get(url, auth=auth, params=params)


def parse_time(time_str):
    return datetime.strptime(time_str[:-5], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=9)


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    return r


def text_refinement(text):
    text = ' '.join(re.sub("(@[A-Za-z0-9_]+)|(#[A-Za-z0-9]+)|(RT)|(\w+:\/\/\S+)|"
                           "[\.\,\!\?\:\;\-\=]", " ", text).split())
    return text


@router.get('/')
async def get_tweet(query: str, time: Optional[str] = None):
    url = "https://api.twitter.com/2/tweets/search/recent"
    params = {'query': query, 'expansions': 'author_id', 'user.fields': 'username,profile_image_url', 'tweet.fields': 'public_metrics,created_at', 'max_results': 100}
    if time:
        if ' ' in time:
            start_time = datetime.strptime(time, "%Y-%m-%d %H:%M") - timedelta(hours=9)
            end_time = start_time + timedelta(hours=1)
        else:
            start_time = datetime.strptime(time, "%Y-%m-%d") - timedelta(hours=9)
            end_time = start_time + timedelta(days=1)
        params['start_time'], params['end_time'] = start_time.strftime('%Y-%m-%dT%H:%M:%SZ'), end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    response = await get_request(url, auth=bearer_oauth, params=params)
    response = response.json()
    user_dic = {user['id']: {"name": user['name'], "profile_img_url": user['profile_image_url'], "username": user['username']} for user in response['includes']['users']}

    def process_tweet(tweet):
        tweet['user'] = user_dic[tweet['author_id']]
        tweet['created_at'] = parse_time(tweet['created_at']).strftime('%Y-%m-%d %H:%M:%S')
        del tweet['author_id']
        return tweet

    txt_for_analysis = [text_refinement(tweet['text']) for tweet in response['data']]

    response['data'] = list(map(process_tweet, response['data']))
    response['top_keywords'] = []
    del response['includes']
    start = time_()
    keywords = Counter(chain(*[Okt().nouns(t) for t in txt_for_analysis])).most_common()
    end = time_()
    print(f"{end - start:.5f} sec")
    i = 0
    while len(response['top_keywords']) < 10:
        if keywords[i][0] not in stop_words and len(keywords[i][0]) >= 2 and keywords[i][0] != query:
            response['top_keywords'].append(keywords[i])
        i += 1
    # sa = Pororo(task="sentiment", model="brainbert.base.ko.nsmc", lang="ko")
    # start = time_()
    # response['score'] = sum(sa(t) == 'Positive' for t in txt_for_analysis)
    # end = time_()
    # print(f"{end - start:.5f} sec")
    response['score'] = random.randint(0, 99)
    return response


@router.get('/count', responses=get_count_responses)
async def get_count(query: str, granularity: str):
    if granularity != 'day' and granularity != 'hour':
        return JSONResponse(status_code=400, content=dict(msg="WRONG_GRANULARITY"))
    url = "https://api.twitter.com/2/tweets/counts/recent"
    response = await get_request(url, auth=bearer_oauth, params={'query': query, 'granularity': 'hour'})
    print(response.status_code)
    if response.status_code != 200:
        return JSONResponse(status_code=500, content=dict(msg="SERVER_ERROR"))
    response = response.json()
    if granularity == 'hour':
        for i in range(len(response['data'])):
            response['data'][i]['time'] = parse_time(response['data'][i]['start']).strftime('%Y-%m-%d %H:00')
            del response['data'][i]['end']
            del response['data'][i]['start']
    elif granularity == 'day':
        count_dic = defaultdict(int)
        for i in range(len(response['data'])):
            count_dic[parse_time(response['data'][i]['start']).strftime('%Y-%m-%d')] += response['data'][i]['tweet_count']
        response['data'] = []
        for key in count_dic:
            response['data'].append({'time': key, 'tweet_count': count_dic[key]})

    return response


@router.get('/hot-now')
async def get_hot():
    resultstr = get_stream_from_s3()
    result_list = select_text(resultstr)
    cleaned_resultstr = cleaning(result_list)
    nouns = preprocess(cleaned_resultstr)
    count = count_nouns(nouns)
    result_top_ten = most_common_top_ten(count)
    return result_top_ten

