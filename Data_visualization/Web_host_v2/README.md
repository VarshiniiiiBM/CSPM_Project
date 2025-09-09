# FastAPI WebSocket Serial Data Broadcaster

This script opens a FastAPI server that:
- Reads JSON-formatted data from a serial port
- Broadcasts the data in real time to all connected WebSocket clients.
- Serves HTML file named "frontend.html" to view raw incoming data in the browser.

## Features
- Reads serial data from a configurable COM port and baud rate.
- Parses newline-separated JSON objects.
- Broadcasts parsed data to all WebSocket clients simultaneously.
- Uses Python’s "logging' module for structured logs instead of "print".
- Adjustable "debuglevel" variable for fine-grained debugging.

##Logger and Debug Option
-This script uses Python’s logging module instead of print to handle all output.
Logs are timestamped and categorized by severity (DEBUG, INFO, WARNING, ERROR).
This makes it easier to filter messages.

## Debug levels
Controlled by the debuglevel variable at the top of the script:

0 → Only ERROR messages (minimal logging)

1 → WARNING + ERROR

2 → INFO + above

3 → DEBUG + above (most verbose, includes raw details)

This allows to adjust verbosity without editing multiple lines of code.
