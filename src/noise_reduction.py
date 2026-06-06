'''
Noise reduction is achoeved through masking and deduplication which is needed to find the frequency count

Masking:
    Replaces dynamic values such as IP addresses, UUIDs, hexadecimal identifiers,
    and numeric values with generic placeholders to normalize log messages into
    common event templates.

Deduplication:
    Groups normalized log messages and aggregates their occurrence counts to
    reduce repetitive log entries and highlight dominant event patterns.
    
'''

import src.parser as parser
import re 

aggregated_logs = {}

def parameter_masker(message):
   # IP addresses
    message = re.sub(
        r"\d+\.\d+\.\d+\.\d+",
        "<IP>",
        message
    )

    # request IDs
    message = re.sub(
        r"req-[a-fA-F0-9\-]+",
        "<UUID>",
        message
    )

    # Long hexadecimal strings
    message = re.sub(
        r"\b[a-fA-F0-9]{16,}\b",
        "<HEX>",
        message
    )

    # Numbers 
    message = re.sub(
        r"\b\d+(?:\.\d+)?\b",
        "<NUM>",
        message
    )

    return message

def frequency_aggregator():
    for record in parser.parser():
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
    frequency_aggregator()
    print(f"Unique groups: {len(aggregated_logs)}")