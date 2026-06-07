import src.parser as parser
import re 

aggregated_logs = {}

def parameter_masker(message):
    if not message:
        return ""
    
    # IP addresses
    message = re.sub(r"\d+\.\d+\.\d+\.\d+", "<IP>", message)

    # Request IDs / OpenStack spec
    message = re.sub(r"req-[a-fA-F0-9\-]+", "<UUID>", message)

    # Long hexadecimal strings 
    message = re.sub(r"\b[a-fA-F0-9]{16,}\b", "<HEX>", message)

    # Numbers 
    message = re.sub(r"\b\d+(?:\.\d+)?\b", "<NUM>", message)

    return message

def frequency_aggregator(log_type="openstack"):
    # Clear map between distinct pipeline runs if processing sequentially
    aggregated_logs.clear()
    
    for record in parser.parser(log_type=log_type):
        masked_msg = parameter_masker(record['message'])
        group_key = (record["service"], record["level"], masked_msg)
        
        if group_key not in aggregated_logs:
            aggregated_logs[group_key] = {
                "first_seen": record["timestamp"],
                "last_seen": record["timestamp"],
                "service": record["service"],
                "level": record["level"],
                "masked_message": masked_msg,
                "count": 1
            }
        else:
            aggregated_logs[group_key]["count"] += 1
            aggregated_logs[group_key]["last_seen"] = record["timestamp"]

if __name__ == "__main__":
    for flavor in ["openstack", "hdfs", "linux"]:
        frequency_aggregator(log_type=flavor)
        print(f"[{flavor.upper()}] Unique aggregated groups: {len(aggregated_logs)}")