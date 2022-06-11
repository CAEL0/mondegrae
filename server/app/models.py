from datetime import datetime
from enum import Enum
from typing import List, Dict

from pydantic import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr, IPvAnyAddress


class TweetCount(BaseModel):
    data: List
    meta: Dict

