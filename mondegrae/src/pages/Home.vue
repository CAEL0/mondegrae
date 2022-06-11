<template>
  <div>
    <!-- 최상단 -->
    <div class="my-10">

      <!-- Mondegrae -->
      <a class="text-4xl font-semibold">
        Mondegrae
      </a>
      
      <!-- Light / Dark 모드 -->
      <button
        name="toggle-theme"
        class="hover:text-yellow-400 focus:outline-none float-right pt-5"
        @click="toggleTheme()"
        aria-label="Toggle color mode"
      >
        <template v-if="!dark">
          <svg
            class="w-8 h-8"
            aria-hidden="true"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"
            ></path>
          </svg>
        </template>
        <template v-else>
          <svg
            class="w-8 h-8"
            aria-hidden="true"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
              clip-rule="evenodd"
            ></path>
          </svg>
        </template>
      </button>
    </div>

    <!-- 입력 창 -->
    <div class="mb-6">
      <label class="flex block w-full text-sm">
        <input
          v-model="inputKeyword"
          class="block w-full dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-input focus:border-blue-400 focus:outline-none focus:shadow-outline-blue dark:focus:shadow-outline-gray"
          placeholder="검색어를 입력해주세요."
          @keyup.enter="updateKeyword"
        >
        <button
          class="block dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-input focus:border-blue-400 focus:outline-none focus:shadow-outline-blue dark:focus:shadow-outline-gray"
          @click="updateKeyword"
        >
          <font-awesome-icon icon="search"/>
        </button>
      </label>
    </div>

    <!-- Top 10 -->
    <div class="justify-between items-center mb-6 p-4 bg-white rounded-lg shadow-md dark:bg-gray-800">
      <p class="mb-2 text-xl font-semibold text-gray-700 dark:text-gray-200">
        실시간 Top 10
      </p>
      <div class="grid gap-6 mb-2 md:grid-cols-2 xl:grid-cols-2">
        <div>
          <p
            class="text-l font-semibold text-gray-700 dark:text-gray-200 py-2"
            v-for="(word, index) in top1_5"
            :key="word"
          >
            {{ index + 1 }}. {{ word.tag }} ({{ word.count }}회)
          </p>
        </div>
        <div>
          <p
            class="text-l font-semibold text-gray-700 dark:text-gray-200 py-2"
            v-for="(word, index) in top6_10"
            :key="word"
          >
            {{ index + 6 }}. {{ word.tag }} ({{ word.count }}회)
          </p>
        </div>
      </div>
    </div>

    <!-- Graph -->
    <div class="flex -mx-3 mb-6">
      <div class="w-full px-3">
        <div class="w-full bg-white rounded-lg shadow-md dark:bg-gray-800 p-4 pb-10 mb-8 xl:mb-0">
          <div>
            <a class="text-xl font-semibold text-gray-700 dark:text-gray-200 mb-4">
              실시간 트윗 수
            </a>
            <label class="flex block ml-3 mb-3 text-sm float-right">
              <span class="text-gray-700 dark:text-gray-400 mt-3 mr-3">
                Interval
              </span>
              <select
                class="block m-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-blue-400 focus:outline-none focus:shadow-outline-blue dark:focus:shadow-outline-gray"
                v-model="term"
              >
                <option value="1" selected="true">Hour</option>
                <option value="7">Day</option>
              </select>
            </label>
          </div>
          <div style="height: 350px">
            <line-chart
              style="height: 100%"
              chart-id="green-line-chart"
              :chart-data="greenLineChart.chartData"
              :extra-options="greenLineChart.extraOptions"
            >
            </line-chart>
          </div>
        </div>
      </div>
    </div>

    <!-- 관련 트윗 -->
    <div class="grid xl:grid-cols-1 mb-6">
      <div
        class="p-4 bg-white rounded-lg shadow-md dark:bg-gray-800"
      >
        <div>
          <p class="mb-8 text-xl font-semibold text-gray-700 dark:text-gray-200">
            관련 트윗
          </p>
          <div id="container">
            <li v-for="tweet in tweets" :key="tweet">
              {{ tweet }}<br><br>
            </li>
          </div>
        </div>
      </div>
    </div>

    <!-- 최하단 -->
    <div class="grid gap-6 mb-2 md:grid-cols-2 xl:grid-cols-2 mb-20">
      <div class="flex-row items-center p-4 bg-white rounded-lg shadow-md dark:bg-gray-800">
        <div>
          <p class="text-xl font-semibold text-gray-700 dark:text-gray-200 pb-3">
            연관 키워드 순위
          </p>
          <p
            class="text-l font-semibold text-gray-700 dark:text-gray-200 py-2"
            v-for="(related, index) in relatedChart"
            :key="related"
          >
            {{ index + 1 }}. {{ related[0] }} ({{ related[1] }}회)
          </p>
        </div>
      </div>

      <div class="p-4 bg-white rounded-lg shadow-md dark:bg-gray-800">
        <div>
          <a class="text-xl font-semibold text-gray-700 dark:text-gray-200 pb-3">
            호감도 분석
          </a>
          <div v-if="this.score > 0" class="text-6xl text-center m-8 p-8">
            {{ this.emoji[parseInt((this.score - 1) / 20)] }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import LineChart from "@/components/LineChart";
import tweetCountData from "@/utils/tweetCountData";
import tweetTextData from "@/utils/tweetTextData";
import tweetTop10 from "@/utils/tweetTop10"

export default {
  name: "DashboardHome",
  components: {
    LineChart
  },
  data() {
    return {
      inputKeyword: "",
      keyword: "크리스마스",
      top1_5: [],
      top6_10: [],
      term: 1,
      capData: [],
      capLabels: [],
      index: 0,
      tweets: [],
      relatedChart: [],
      score: 0,
      emoji: ["😭", "😢", "😐", "😄", "🥰"]
    };
  },
  computed: {
    ...mapState([
      "dark"
    ]),
    greenLineChart() {
      return {
        extraOptions: {
          maintainAspectRatio: false,
          legend: {
            display: false
          },
          responsive: true,
          tooltips: {
            backgroundColor: '#f5f5f5',
            titleFontColor: '#333',
            bodyFontColor: '#666',
            bodySpacing: 4,
            xPadding: 12,
            intersect: 0,
            mode: "x",
            position: "nearest",
            callbacks: {
              beforeLabel: (tooltipItem) => { this.setIndex(tooltipItem.index); }
            }
          },
          scales: {
            yAxes: [{
              barPercentage: 1.6,
              gridLines: {
                drawBorder: false,
                color: 'rgba(0,242,195,0.1)',
                zeroLineColor: "transparent",
              },
              ticks: {
                padding: 20,
                fontColor: "#9e9e9e"
              }
            }],
            xAxes: [{
              barPercentage: 1.6,
              gridLines: {
                drawBorder: false,
                color: 'rgba(0,242,195,0.0)',
                zeroLineColor: "transparent",
              },
              ticks: {
                callback: function(value) { return value.split(" ")[0]; },
                padding: 10,
                fontColor: "#9e9e9e",
                maxRotation: 0,
                minRotation: 0,
                autoSkip: true,
                autoSkipPadding: 85,
              }
            }]
          },
          events: ['click', 'mousemove'],
          onClick: () => { this.getTweet(); }
        },
        chartData: {
          labels: this.capLabels,
          datasets: [
            {
              backgroundColor: "rgba(0,242,195,0.1)",
              borderColor: "#42b883",
              borderWidth: 2,
              pointBackgroundColor: "#42b883",
              pointBorderColor: "rgba(255,255,255,0)",
              pointHoverBackgroundColor: "#42b883",
              pointBorderWidth: 20,
              pointHoverRadius: 4,
              pointHoverBorderWidth: 15,
              pointRadius: this.term == 1 ? 0 : 3,
              lineTension: 0,
              data: this.capData
            },
          ],
        },
      };
    }
  },
  methods: {
    getTweetCount() {
      this.$toast.info(`Search ${this.keyword}`);
      this.tweets = [];
      this.relatedChart = [];
      tweetCountData(this.keyword, this.term, this.setChartData);
    },
    setChartData(res) {
      const tweetCount = res.data.map((x) => x.tweet_count);
      this.capLabels = Array(tweetCount.length);
      for (let i = 0; i < tweetCount.length; i++) {
        this.capLabels[i] = res.data[i].time;
      }
      this.capData = tweetCount;
    },
    setIndex(idx) {
      this.index = idx;
    },
    getTweet() {
      this.$toast.info(`Load tweets about ${this.keyword}`);
      tweetTextData(this.keyword, this.capLabels[this.index], this.setRelatedTweet);
    },
    setRelatedTweet(res) {
      this.score = res.score;
      this.tweets = [];
      for (let i = 0; i < res.data.length; i++) {
        this.tweets.push(res.data[i].text);
      }
      this.relatedChart = [];
      for (let i = 0; i < 5; i++) {
        this.relatedChart.push(res.top_keywords[i]);
      }
    },
    updateKeyword() {
      if (this.inputKeyword == "") {
        this.$toast.info("Please enter any keyword");
      }
      else if (this.inputKeyword.length <= 1) {
        this.$toast.info("Keyword is too short");
      }
      else {
        this.keyword = this.inputKeyword;
        this.getTweetCount();
      }
    },
    toggleTheme() {
      this.$store.dispatch("toggleTheme");
    },
    getTop10() {
      tweetTop10(this.refresh);
      setTimeout(() => tweetTop10(this.refresh), 3 * 60 * 1000);
      setTimeout(() => tweetTop10(this.refresh), 3 * 60 * 1000);
      setTimeout(() => tweetTop10(this.refresh), 3 * 60 * 1000);
      setTimeout(() => tweetTop10(this.refresh), 3 * 60 * 1000);
    },
    refresh(res) {
      this.top1_5 = [];
      this.top6_10 = [];
      for (let i = 0; i < 5; i++) {
        this.top1_5.push(res[i]);
      }
      for (let i = 5; i < 10; i++) {
        this.top6_10.push(res[i]);
      }
      this.$toast.info("Update Top 10");
    }
  },
  mounted() {
    this.getTweetCount();
    this.getTop10();
  },
  watch: {
    term() {
      this.getTweetCount();
    }
  },
};
</script>

<style scoped>
#container {
  table-layout: fixed;
  border-collapse: collapse;
  overflow: auto;
  width: 90%;
  height: 250px;
  margin: auto;
  margin-bottom: 8px;
}
#container::-webkit-scrollbar {
  width: 10px;
}
#container::-webkit-scrollbar-thumb {
  background-color: #2f3542;
  border-radius: 10px;
  background-clip: padding-box;
  border: 2px solid transparent;
}
#container::-webkit-scrollbar-track {
  background-color: grey;
  border-radius: 10px;
  box-shadow: inset 0px 0px 5px white;
}
</style>