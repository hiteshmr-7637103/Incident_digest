from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "data" / "OpenStack_2k.log"

pattern = re.compile(
    r'^(?P<log_file>\S+)\s+'  # Matches log file name
    r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d{3})\s+'  # Matches timestamp
    r'(?P<pid>\d+)\s+'    # Matches Process ID
    r'(?P<level>\w+)\s+'  # Matches Log Level (INFO, ERROR, etc.)
    r'(?P<component>\S+)\s+' # Matches the service/logger component
    r'\[(?P<request_id>[^\]]*)\]\s+' # Matches everything inside the brackets []
    r'(?P<message>.*)$'# Matches everything else as the message
)
def parser():

    with open(LOG_FILE) as openstack_file:
        for line in openstack_file:
            line = line.strip()
            match = pattern.match(line)  
            
            if match:
                record = match.groupdict()
                standardized_record = {
                    "timestamp": record.get("timestamp"),
                    "level": record.get("level"),
                    "service": record.get("component"),
                    "request_id": record.get("request_id"),
                    "message": record.get("message")
                }
                
                # yield logs 
                yield standardized_record