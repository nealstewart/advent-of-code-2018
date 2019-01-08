import pandas as pd
import numpy as np
from functools import reduce
from datetime import datetime
from operator import itemgetter
import re

def to_state(event: str):
    if event == 'falls asleep':
        return 'asleep'
    else:
        return 'awake'

guard_id_regex = re.compile(r"#([0-9]+)")
def get_guard_id(event: str):
    return guard_id_regex.findall(event)[0]

regular_expression = re.compile(r"\[(.*)\] (.*)")
def create_record(line: str):
    event_start, event = regular_expression.findall(line)[0]

    return {
        'guard': get_guard_id(event) if 'begins shift' in event else None,
        'state': to_state(event),
        'time': datetime.strptime(event_start, "1518-%m-%d %H:%M")
    }

def get_records() -> pd.DataFrame:
    with open('input') as f:
        df = pd.DataFrame([create_record(line) for line in f])
        df = df.set_index('time').sort_index().ffill()
        df.index = pd.to_datetime(df.index)
        return df

def create_sleep_summary() -> dict:
    records = get_records()
    records['state'] = pd.Categorical(records['state'], categories = ['late', 'awake', 'asleep'])

    days = pd.date_range(records.index[0].replace(hour=23, minute=0), records.index[-1].replace(hour=23, minute=0), freq="d")

    guard_days = {guard: [] for guard in records['guard'].unique()}

    for day in days:
        start_time = day + pd.Timedelta(minutes=30)
        actual_start_time = day + pd.Timedelta(hours=1)
        end_time = day + pd.Timedelta(hours=2)

        # select all of the records for the evening
        day_records = records[start_time:end_time].copy(deep=True)
        if day_records.shape[0] == 0: # some evenings are empty
            continue

        # Fill up 1am
        last_time = end_time - pd.Timedelta(minutes=1)
        if day_records[last_time:].shape[0] == 0:
            day_records.loc[last_time] = [np.nan, np.nan]

        # Handle them being late
        if day_records[actual_start_time:actual_start_time].shape[0] == 0:
            day_records.loc[actual_start_time] = [np.nan, np.nan]

        # Resample to fill in time between events
        filled = day_records.resample("1min").ffill().fillna(method='ffill')
        filled['guard'].fillna(method="bfill", inplace=True)
        filled['state'].fillna('late', inplace=True)

        # Select only the midnight hour
        only_midnight_hour = filled[actual_start_time:end_time]
        only_midnight_hour.index = only_midnight_hour.index.minute

        # convert to one hot encoding for easier addition
        only_midnight_hour = pd.get_dummies(only_midnight_hour, columns=["state"])

        # Handle no sleeping
        if 'state_asleep' not in only_midnight_hour.columns:
            only_midnight_hour['state_asleep'] = 0 

        guard = only_midnight_hour["guard"].unique()[0]
        guard_days[guard].append(only_midnight_hour['state_asleep'])
    
    return {guard: reduce(lambda x, y: x + y, guard_day) for guard, guard_day in guard_days.items()}

def part_1():
    guard_id, sleep_summary = sorted(create_sleep_summary().items(), key= lambda k: sum(k[1]), reverse=True)[0]
    minute_sleeping_most, times_sleeping = max(enumerate(sleep_summary), key=itemgetter(1))
    print("Solution to part 1:", int(guard_id) * minute_sleeping_most)

def part_2():
    guard_id, sleep_summary = sorted(create_sleep_summary().items(), key= lambda k: max(k[1]), reverse=True)[0]
    minute_sleeping_most, times_sleeping = max(enumerate(sleep_summary), key=itemgetter(1))
    print("Solution to part 2:", int(guard_id) * minute_sleeping_most)

part_1()
part_2()