import time
import json
import random
from datetime import datetime

#센서 설계도
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
        #이산화탄소 농도는 범위가 작아서 소수점3자리까지 표현해서 미세한 차이를 나타냄
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 3)
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4.0, 7.0), 2)


	#센서 데이터를 로그 파일에 기록
    def get_env(self):
        # 현재 컴퓨터의 날짜와 시간 얻기
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # env_values (센서 데이터)를 문자열로 포맷
        data_lines = [f"{k}: {v}" for k, v in self.env_values.items()]
        data_str = "\n".join(data_lines)
        
        # 로그 내용
        log_entry = f"[{now}]\n{data_str}\n\n"
        
        # 기록
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
        #속성에 self.ds 라는 DummySensor() 인스턴스를 추가
        #미션컴퓨터가 연결한 센서!
        self.ds = DummySensor()  

    # 센서 데이터를 계속 수집하고 출력
    def get_sensor_data(self):
        while True:
            self.ds.set_env() 
            self.env_values = self.ds.get_env()  
            # self.env_values를 JSON 문자열로 변환하고, 보기 좋게 4칸 들여쓰기
            json_data = json.dumps(self.env_values, indent=4)
            print(json_data)
            # 5초 대기 후 루프 다시 시작
            time.sleep(5) 


def main():
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()


if __name__ == "__main__":
    main()