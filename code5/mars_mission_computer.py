import time
import threading
import platform
import os
import json
import random
from datetime import datetime

#문제7
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
        self.env_values = {}
        self.ds = DummySensor()
        self.running = True
        self.data_history = []

    #문제7
    def stop_listener(self):
        while True:
            if input().strip().lower() == 'q':
                self.running = False
                print("System stopped…")
                break
    #문제7
    def calculate_and_print_average(self):
        if not self.data_history:
            return
        average = {}
        keys = self.data_history[0].keys()
        for key in keys:
            values = [d[key] for d in self.data_history]
            average[key] = round(sum(values) / len(values), 3 if 'co2' in key else 2)
        print("\n--- 5분 평균 환경 정보 ---")
        print(json.dumps(average, indent=4))
        print("-------------------------\n")
        self.data_history = []
    #문제7
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
            if counter == 60:
                self.calculate_and_print_average()
                counter = 0

    # 파일을 읽어서 출력할 항목을 리스트로 반환
    def read_settings(self):
        try:
            with open("setting.txt", "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []
    
    #미션 컴퓨터의 시스템 정보를 수집
    def get_mission_computer_info(self):
        settings = self.read_settings()
        info = {}
        if "os" in settings:
            info["os"] = platform.system() #OS의 이름을 문자열로 반환
        if "os_version" in settings:
            info["os_version"] = platform.version() #OS버전 문자열로 반환
        if "cpu_architecture" in settings:
            info["cpu_architecture"] = platform.processor() # CPU 아키텍처 또는 모델명을 반환
        if "cpu_cores" in settings:
            info["cpu_cores"] = os.cpu_count() # 논리적 CPU 코어 수를 정수로 반환
        if "memory_info" in settings:
            info["memory_info"] = self._get_memory_info() #메모리 크기

        print("\n--- Mission Computer System Info ---")
        print(json.dumps(info, indent=4))
        print("------------------------------\n")
        
    # 미션 컴퓨터의 부하를 가져옴
    def get_mission_computer_load(self):
        settings = self.read_settings()
        load = {}

        if "cpu_usage_percent" in settings:
            load["cpu_usage_percent"] = self._get_cpu_load() #실시간 CPU 사용률
        if "memory_usage_percent" in settings:
            load["memory_usage_percent"] = self._get_memory_usage() #실시간 메모리 사용률

        print("\n--- Mission Computer Load ---")
        print(json.dumps(load, indent=4))
        print("--------------------------------\n")

    
   
    def _get_memory_info(self):
        # POSIX 계열 운영체제인 경우
        if os.name == 'posix':
		    # 메모리 정보를 제공하는 시스템 가상 파일 (Key: Value 형태)
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal'):
                        return line.split(":")[1].strip()
        #Windows 운영체제인 경우 (nt는 Windows의 내부 이름)           
        elif os.name == 'nt':
            # C 스타일 (구조체와 시스템 API 호출을 가능하게 하는) 내장 모듈
            import ctypes
            # Windows 시스템 API와 연동하기 위한 구조체 정의
            # Structure는 C와 같은 구조체 메모리 구조를 구현하는 방식
            class MEMORYSTATUS(ctypes.Structure):
                #Windows가 요구하는 필드들을 구조체 형태로 정의
                _fields_ = [("dwLength", ctypes.c_ulong),
                            ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong),
                            ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong),
                            ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong),
                            ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("sullAvailExtendedVirtual", ctypes.c_ulonglong)]
            memoryStatus = MEMORYSTATUS()
            #구조체의 크기 정보를 시스템에 알려주는 필수 설정 
            memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUS)
            #memoryStatus 구조체를 참조 형태로 받아서 시스템 메모리 관련 정보를 채워줌 
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))
            # RAM 바이트 단위 -> 메가바이트
            total_memory = memoryStatus.ullTotalPhys // (1024 * 1024)
            return f"{total_memory} MB"
        return "Unknown"

    
    def _get_memory_usage(self):
        if os.name == 'posix':
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.readlines()
                mem_total = int([x for x in meminfo if "MemTotal" in x][0].split()[1])
                mem_available = int([x for x in meminfo if "MemAvailable" in x][0].split()[1])
                # 실제 사용 중인 메모리 계산: 전체 - 사용 가능 = 사용된 메모리
                mem_used = mem_total - mem_available
                
                return round((mem_used / mem_total) * 100, 2)
        elif os.name == 'nt':
            import ctypes
            class MEMORYSTATUS(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong),
                            ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong),
                            ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong),
                            ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong),
                            ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("sullAvailExtendedVirtual", ctypes.c_ulonglong)]
            memoryStatus = MEMORYSTATUS()
            memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUS)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))
            # 메모리 사용률(%)을 나타내는 dwMemoryLoad 값을 반환
            # 이미 Windows 시스템이 사용률 퍼센트 값을 자동 계산해서 제공해 줌
            return memoryStatus.dwMemoryLoad
        return 0.0

    
    def _get_cpu_load(self):
        if os.name == 'posix':
            # os.getloadavg()는 (1분, 5분, 15분 평균 CPU load)를 튜플로 반환
            load1, _, _ = os.getloadavg()
            # 전체 CPU 코어 수 대비 load 비율을 %로 계산
            return round((load1 / os.cpu_count()) * 100, 2)
        elif os.name == 'nt':
            import ctypes
            # Windows API에서 사용하는 시간 구조체 FILETIME 정의
            # dwHighDateTime은 상위 32비트, dwLowDateTime은 하위 32비트
            class FILETIME(ctypes.Structure):
                _fields_ = [
                    ("dwLowDateTime", ctypes.c_ulong),
                    ("dwHighDateTime", ctypes.c_ulong)
                ]
                
            idleTime = FILETIME()
            kernelTime = FILETIME()
            userTime = FILETIME()

            # 이 함수를 통해 전체 시간 값을 하나의 정수로 합침
            def filetime_to_int(ft):
                return (ft.dwHighDateTime << 32) | ft.dwLowDateTime
            
            #첫 번째 시간 측정
            ctypes.windll.kernel32.GetSystemTimes(
                ctypes.byref(idleTime), 
                ctypes.byref(kernelTime), 
                ctypes.byref(userTime)
            )

            idle1 = filetime_to_int(idleTime)
            kernel1 = filetime_to_int(kernelTime)
            user1 = filetime_to_int(userTime)

            time.sleep(1)

            #두 번째 시간 측정
            ctypes.windll.kernel32.GetSystemTimes(
                ctypes.byref(idleTime),
                ctypes.byref(kernelTime), 
                ctypes.byref(userTime)
            )

            idle2 = filetime_to_int(idleTime)
            kernel2 = filetime_to_int(kernelTime)
            user2 = filetime_to_int(userTime)

            # 1초 동안의 idle 시간과 전체 실행 시간 계산
            idle = idle2 - idle1
            # total: 커널 + 사용자 모드 실행 시간 변화량
            total = (kernel2 - kernel1) + (user2 - user1)

            # 0으로 나누는 에러 방지 (혹시라도 시간 변화가 없다면 0.0%)
            if total == 0:
                return 0.0
            
            # CPU가 바쁘게 일한 시간 = 전체 - idle
            # ex) idle이 25%, 총이 100% → 사용률 = 75%
            return round((1.0 - (idle / total)) * 100.0, 2)
        return 0.0

def main():
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()

if __name__ == "__main__":
    main()
