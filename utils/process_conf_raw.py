#!/usr/bin/env python3
# coding: utf-8

import yaml
import datetime
from collections import OrderedDict
import pytz
from yaml.resolver import BaseResolver

# Constants
dateformat = '%Y-%m-%d %H:%M:%S'
tba_words = ["tba", "tbd"]
right_now = datetime.datetime.now(pytz.utc).replace(microsecond=0)
_mapping_tag = BaseResolver.DEFAULT_MAPPING_TAG

# Timezone alias mapping
timezone_alias_map = {
    # UTC offsets (reversed sign for IANA)
    "UTC-12": "Etc/GMT+12", "UTC-11": "Etc/GMT+11", "UTC-10": "Etc/GMT+10", "UTC-9": "Etc/GMT+9",
    "UTC-8": "Etc/GMT+8", "UTC-7": "Etc/GMT+7", "UTC-6": "Etc/GMT+6", "UTC-5": "Etc/GMT+5",
    "UTC-4": "Etc/GMT+4", "UTC-3": "Etc/GMT+3", "UTC-2": "Etc/GMT+2", "UTC-1": "Etc/GMT+1",
    "UTC+0": "Etc/GMT", "UTC+1": "Etc/GMT-1", "UTC+2": "Etc/GMT-2", "UTC+3": "Etc/GMT-3",
    "UTC+4": "Etc/GMT-4", "UTC+5": "Etc/GMT-5", "UTC+6": "Etc/GMT-6", "UTC+7": "Etc/GMT-7",
    
    # Correct mappings for Asia timezones
    "UTC+8": "Asia/Shanghai",  # Correct IANA name for UTC+8
    "UTC+9": "Asia/Seoul",     # Correct IANA name for UTC+9
    
    "UTC+10": "Etc/GMT-10", "UTC+11": "Etc/GMT-11", "UTC+12": "Etc/GMT-12",

    # Time zone abbreviations (using IANA names for daylight saving)
    "EST": "America/New_York", "EDT": "America/New_York", "CST": "America/Chicago",
    "CDT": "America/Chicago", "MST": "America/Denver", "MDT": "America/Denver",
    "PST": "America/Los_Angeles", "PDT": "America/Los_Angeles",
    "AKST": "America/Anchorage", "AKDT": "America/Anchorage", "HST": "Pacific/Honolulu",
    "HAST": "Pacific/Honolulu", "HADT": "Pacific/Honolulu", "KST": "Asia/Seoul",
    "JST": "Asia/Tokyo", "IST": "Asia/Kolkata", "CET": "Europe/Paris", "CEST": "Europe/Paris",
    "BST": "Europe/London", "MSK": "Europe/Moscow", "AEST": "Australia/Sydney",
    "AEDT": "Australia/Sydney", "NZST": "Pacific/Auckland", "NZDT": "Pacific/Auckland",

    # AoE (Anywhere on Earth), uses the latest time zone possible (UTC-12)
    "AoE": "Etc/GMT+12",
    "AOE": "Etc/GMT+12",

    # GMT shorthand (reversed sign for IANA)
    "GMT": "Etc/GMT", "GMT+0": "Etc/GMT", "GMT+1": "Etc/GMT-1", "GMT+2": "Etc/GMT-2", "GMT+3": "Etc/GMT-3",
    "GMT+4": "Etc/GMT-4", "GMT+5": "Etc/GMT-5", "GMT+6": "Etc/GMT-6", "GMT+7": "Etc/GMT-7",
    "GMT+8": "Etc/GMT-8", "GMT+9": "Etc/GMT-9", "GMT+10": "Etc/GMT-10", "GMT-1": "Etc/GMT+1",
    "GMT-2": "Etc/GMT+2", "GMT-3": "Etc/GMT+3", "GMT-4": "Etc/GMT+4", "GMT-5": "Etc/GMT+5",
    "GMT-6": "Etc/GMT+6", "GMT-7": "Etc/GMT+7", "GMT-8": "Etc/GMT+8", "GMT-9": "Etc/GMT+9",
    "GMT-10": "Etc/GMT+10",
}

def normalize_timezone(tz):
    return timezone_alias_map.get(tz.strip(), tz)

def find_invalid_timezones(data):
    invalid_tz_set = set()
    for entry in data:
        tz = entry.get("timezone", "").strip()
        if not tz:
            continue
        try:
            pytz.timezone(normalize_timezone(tz))
        except Exception:
            invalid_tz_set.add(tz)
    return sorted(invalid_tz_set)

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader): pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(_mapping_tag, construct_mapping)
    return yaml.load(stream, OrderedLoader)

def ordered_dump(data):
    class OrderedDumper(yaml.Dumper): pass
    def _dict_representer(dumper, data):
        return dumper.represent_mapping(_mapping_tag, data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, Dumper=OrderedDumper, default_flow_style=False)

def deadline_key(x):
    dt_naive = datetime.datetime.strptime(x['deadline'], dateformat)
    tz = pytz.timezone(normalize_timezone(x['timezone']))
    dt_local = tz.localize(dt_naive)
    return dt_local.astimezone(pytz.utc)

# Load and process
with open("../_data/conferences_raw.yml", 'r') as stream:
    data = ordered_load(stream, Loader=yaml.SafeLoader)

    invalid_tzs = find_invalid_timezones(data)
    if invalid_tzs:
        print("⚠️ Invalid or unrecognized timezones found:")
        for tz in invalid_tzs:
            print(f" - {tz}")
        print("Please correct them or extend the timezone_alias_map.\n")
    else:
        print("✅ All timezones are valid.\n")

    valid_conf = [x for x in data if x['deadline'].lower() not in tba_words]
    tba_conf = [x for x in data if x['deadline'].lower() in tba_words]

    upcoming = [x for x in valid_conf if deadline_key(x) >= right_now]
    past = [x for x in valid_conf if deadline_key(x) < right_now]

    upcoming.sort(key=deadline_key)
    past.sort(key=deadline_key)
    sorted_all = upcoming + past + tba_conf

    # Normalize timezone field before writing
    for item in sorted_all:
        item['timezone'] = normalize_timezone(item.get('timezone', ''))

    with open('../_data/conferences.yml', 'w') as outfile:
        for item in sorted_all:
            yaml_text = ordered_dump([item])
            yaml_text = yaml_text.strip().replace("- id:", "\n- id:")
            outfile.write(yaml_text + "\n\n")
