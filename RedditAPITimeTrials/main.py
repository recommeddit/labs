from pmaw_parser import parse_with_pmaw, parse_with_two_step_pmaw
from praw_parser import parse_with_praw
from psaw_parser import parse_with_psaw
from pushshift_parser import parse_with_raw_pushshift_api

from utils import time

print("Using PRAW")
time(parse_with_praw)()

print("Using PSAW")
time(parse_with_psaw)()

print("Using PMAW (direct)")
time(parse_with_pmaw)()

print("Using PMAW (indirect)")
time(parse_with_two_step_pmaw)()

print("Using raw API")
time(parse_with_raw_pushshift_api)()
