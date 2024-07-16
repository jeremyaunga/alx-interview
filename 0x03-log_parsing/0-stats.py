#!/usr/bin/python3
import sys
import signal

# Initialize metrics
total_size = 0
status_counts = {
    "200": 0,
    "301": 0,
    "400": 0,
    "401": 0,
    "403": 0,
    "404": 0,
    "405": 0,
    "500": 0
}

line_count = 0

def print_stats():
    """Print the current statistics."""
    print(f"File size: {total_size}")
    for status_code in sorted(status_counts.keys()):
        if status_counts[status_code] > 0:
            print(f"{status_code}: {status_counts[status_code]}")

def signal_handler(sig, frame):
    """Handle the CTRL+C signal to print stats."""
    print_stats()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

try:
    for line in sys.stdin:
        # Check if the line matches the expected format
        parts = line.split()
        if len(parts) != 9:
            continue
        ip, _, _, date, _, request, _, status_code, file_size = parts
        if request != '"GET /projects/260 HTTP/1.1"':
            continue
        if not status_code.isdigit() or not file_size.isdigit():
            continue

        # Update metrics
        total_size += int(file_size)
        if status_code in status_counts:
            status_counts[status_code] += 1

        line_count += 1

        # Print stats after every 10 lines
        if line_count % 10 == 0:
            print_stats()

except KeyboardInterrupt:
    print_stats()
    sys.exit(0)
