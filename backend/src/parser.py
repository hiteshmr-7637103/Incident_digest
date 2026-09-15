from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent.parent

# Centralized regex patterns for each log flavor
PATTERNS = {
    "openstack": re.compile(
        r'^(?P<log_file>\S+)\s+'
        r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d{3})\s+'
        r'(?P<pid>\d+)\s+'
        r'(?P<level>\w+)\s+'
        r'(?P<component>\S+)\s+'
        r'\[(?P<request_id>[^\]]*)\]\s+'
        r'(?P<message>.*)$'
    ),
    "hdfs": re.compile(
        r'^(?P<timestamp>\d{6}\s+\d{6})\s+'
        r'(?P<pid>\d+)\s+'
        r'(?P<level>\w+)\s+'
        r'(?P<component>[\w\.\$\s]+):\s+'
        r'(?P<message>.*)$'
    ),
    "linux": re.compile(
        r'^(?P<timestamp>[A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+'
        r'(?P<hostname>\S+)\s+'
        r'(?P<component>[\w\-\.\/]+)(?:\[(?P<pid>\d+)\])?:\s+'
        r'(?P<message>.*)$'
    )
}

def parser(log_type="openstack"):
    """
    Dynamically parses a log file based on its type and streams uniform dictionaries.
    Supported types: 'openstack', 'hdfs', 'linux'
    """
    log_type = log_type.lower()
    if log_type not in PATTERNS:
        raise ValueError(f"Unsupported log type: {log_type}. Choose from {list(PATTERNS.keys())}")
        
    # Map types to their respective files
    file_mapping = {
        "openstack": "OpenStack_2k.log",
        "hdfs": "HDFS_2k.log",
        "linux": "Linux_2k.log"
    }
    
    log_path = BASE_DIR / "data" / file_mapping[log_type]
    pattern = PATTERNS[log_type]

    if not log_path.exists():
        print(f"Error: File not found at {log_path}")
        return

    with open(log_path, "r", errors="ignore") as log_file:
        for line in log_file:
            line = line.strip()
            match = pattern.match(line)  
            
            if match:
                record = match.groupdict()
                
                # Standardized output payload
                yield {
                    "timestamp": record.get("timestamp"),
                    "level": record.get("level", "INFO"),  # Linux defaults to INFO if unspecified
                    "service": record.get("component"),
                    "request_id": record.get("request_id", "N/A"), # Default if missing
                    "message": record.get("message")
                }