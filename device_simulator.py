import time, json, random

def send_data():
  
    while True:
        data = {
            "device_id": "simDevice01",
            "temperature": round(random.uniform(25, 40), 2),
            "moisture": round(random.uniform(20, 60), 2)
        }
        
        with open("iot_messages.json", "a") as f:
            f.write(json.dumps(data) + "\n")
        print("Sent:", data)
        time.sleep(3)

if __name__ == "__main__":
    send_data()