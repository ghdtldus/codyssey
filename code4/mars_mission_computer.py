import time
import json
import random
from datetime import datetime

class DummySensor:
    def __init__(self):
        self.env_values = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None
        }

    def set_env(self):
        self.env_values["mars_base_internal_temperature"] = round(random.uniform(18.0, 30.0), 1)
        self.env_values["mars_base_external_temperature"] = round(random.uniform(0.0, 21.0), 1)
        self.env_values["mars_base_internal_humidity"] = round(random.uniform(50.0, 60.0), 1)
        self.env_values["mars_base_external_illuminance"] = round(random.uniform(500.0, 715.0), 1)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 3)
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4.0, 7.0), 2)

    def get_env(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_lines = [f"{k}: {v}" for k, v in self.env_values.items()]
        data_str = "\n".join(data_lines)
        log_entry = f"[{now}]\n{data_str}\n\n"
        with open("sensor_log.txt", "a", encoding="utf-8") as f:
            f.write(log_entry)
        return self.env_values


class MissionComputer:
    def __init__(self):
        self.env_values = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None
        }
        self.ds = DummySensor()

    def get_sensor_data(self):
        
        while True:
            self.ds.set_env()
            self.env_values = self.ds.get_env()
            json_data = json.dumps(self.env_values, indent=4)
            print(json_data)
            time.sleep(5)

def main():
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()  

if __name__ == "__main__":
    main()
