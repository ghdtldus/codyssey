import time
import json
import random
from datetime import datetime
import threading

# 센서 설계도
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

    #센서 데이터를 로그 파일에 기록하고 반환
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
        self.env_values = {}
        self.ds = DummySensor()
        self.running = True
        self.data_history = []

    def stop_listener(self):
        while True:
            # 사용자가 입력한 값을 소문자로 바꾸고 공백 제거한 후 확인
            if input().strip().lower() == 'q':
                # 종료 플래그 설정
                self.running = False
                # 종료 메시지 출력
                print("System stopped…")
                break

    def calculate_and_print_average(self):
        # 누적된 데이터가 없으면 함수 종료
        if not self.data_history:
            return
        
        # 평균값을 저장할 딕셔너리 초기화
        average = {}
        # 첫 데이터의 키값들을 기준으로 평균 계산 (모든 데이터에 동일한 키가 있다고 가정)
        keys = self.data_history[0].keys()

        for key in keys:
            # 각 키에 대한 값만 리스트로 추출
            values = [d[key] for d in self.data_history]
            # co2는 정밀하게 3자리, 그 외는 소수점 2자리 반올림
            average[key] = round(sum(values) / len(values), 3 if 'co2' in key else 2)

        print("\n--- 5분 평균 환경 정보 ---")
        print(json.dumps(average, indent=4))
        print("-------------------------\n")
        self.data_history = []

    def get_sensor_data(self):
        input_thread = threading.Thread(target=self.stop_listener)
        input_thread.daemon = True
        input_thread.start()

        counter = 0
        while self.running:

            self.ds.set_env()
            self.env_values = self.ds.get_env()
            self.data_history.append(self.env_values.copy())
            print(json.dumps(self.env_values, indent=4))

            time.sleep(5)
            counter += 1

            # 루프가 60회 반복했으면(300초) 평균 계산
            if counter == 60:  
                self.calculate_and_print_average()
                counter = 0

def main():
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()

if __name__ == "__main__":
    main()
