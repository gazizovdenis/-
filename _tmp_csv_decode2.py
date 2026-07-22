import sys, io, json, base64
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Read the raw API response - it's stored somewhere from the download
# Let me check if there's a file with the CSV content
import os

# Look for the most recently created tool-results file
tool_results_dir = r"C:\Users\Denis\.claude\projects\c--Users-Denis-Desktop--------\1fe30397-edde-49bd-b3f9-87fa47acc811\tool-results"
files = []
for f in os.listdir(tool_results_dir):
    full = os.path.join(tool_results_dir, f)
    files.append((os.path.getmtime(full), f, full))

files.sort(reverse=True)
print("Recent tool result files:")
for mtime, name, path in files[:10]:
    size = os.path.getsize(path)
    print(f"  {name} ({size} bytes)")
