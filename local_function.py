import json
import time

def process_message(data):
    
    temp = data.get("temperature")
    moist = data.get("moisture")

    if temp > 35:
        print("🔥 High Temperature Alert:", temp)
    if moist < 30:
        print("💧 Low Moisture Alert:", moist)
    # Save processed data to another file
    with open("processed_data.json", "a") as f:
        f.write(json.dumps(data) + "\n")

if __name__ == "__main__":
    print("Function started, monitoring data...")
    
    while True:
        try:
            # Read all lines from iot_messages.json and then truncate (clear) the file
            with open("iot_messages.json", "r+") as f:
                lines = f.readlines()
                f.truncate(0)
            for line in lines:
                data = json.loads(line.strip())
                process_message(data)
        except FileNotFoundError:
            # Continue running if the file doesn't exist yet
            pass
        time.sleep(3)