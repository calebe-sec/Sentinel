import re
import yaml

from base_parser import BaseParser

def load_patterns(path, category):
    with open(path) as f:
        raw = yaml.safe_load(f)

    compiled = {}

    for event_type, data in raw[category].items():
        compiled[data["keyword"]] = (event_type, re.compile(data["regex"]))
        return compiled

class NginxParseLog(BaseParser):
    HEADER = re.compile(r"(?P<ip>\d+).+\[(?P<day>\d{2})/(?P<month>\w{3})/(?P<year>\d{4}):(?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})\s+(?P<tz>[+-]\d{4})\]\s+\"(?P<method>\w+)\s+/(?P<URL>.+)/(?P<version>\d\.\d)\"\s+(?P<stcd>)\s+(?P<bytes>\d+)\"(?P<subd>.+)\"")

    #def __init__(self, patterns_path="config/log_patterns.yaml"):

    def parse(self, filepath):
        
        events = {}
        
        with open(filepath) as f:
            for line in f:

                match = self.HEADER.search(line)

                if not match:
                    continue
                