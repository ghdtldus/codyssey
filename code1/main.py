import os

def get_log_filepath():
    #현재 실행 중인 파일의 디렉토리를 기준으로 로그 파일 경로를 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "mission_computer_main.log")

def get_error_log_filepath():
    #현재 실행 중인 파일의 디렉토리를 기준으로 에러 로그 파일 경로를 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "error_logs.txt")

def read_log_file(filename):
    #로그 파일을 읽어 리스트로 반환
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"오류: 파일 '{filename}'을(를) 찾을 수 없습니다.")
    except IsADirectoryError:
        print(f"오류: '{filename}'은(는) 파일이 아니라 디렉터리입니다.")
    except PermissionError:
        print(f"오류: '{filename}' 파일에 대한 읽기 권한이 없습니다.")
    except UnicodeDecodeError:
        print(f"오류: '{filename}' 파일을 읽는 중 인코딩 오류가 발생했습니다.")
    except IOError:
        print(f"오류: '{filename}' 파일을 읽는 중 입출력(IO) 오류가 발생했습니다.")
    except OSError:
        print(f"오류: '{filename}' 파일을 여는 중 운영 체제(OS) 오류가 발생했습니다.")
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")
    return []

def filter_error_logs(lines):
    #'unstable' 또는 'explosion'이 포함된 로그만 필터링
    return [line for line in lines if "unstable" in line.lower() or "explosion" in line.lower()]

def write_error_logs(filename, error_logs):
    #필터링된 오류 로그를 파일에 저장
    try:
        with open(filename, "w", encoding="utf-8") as error_file:
            error_file.writelines(error_logs)
        print(f"문제 로그가 '{filename}' 파일에 저장되었습니다.")
    except Exception as e:
        print(f"오류 로그 저장 중 오류 발생: {e}")

def print_logs(lines):
    #로그를 최신순으로 출력
    print("\n--- 로그 내용 (최신순) ---")
    for line in reversed(lines):  # 리스트를 역순 출력
        print(line.strip())

def main():
    log_file = get_log_filepath()
    error_log_file = get_error_log_filepath()

    # 로그 파일 읽기
    logs = read_log_file(log_file)
    if not logs:
        return  # 로그 파일이 없으면 종료

    # 최신순으로 로그 출력
    print_logs(logs)

    # 문제 로그 필터링 및 저장
    error_logs = filter_error_logs(logs)
    if error_logs:
        print("\n--- 주요 오류 로그 ---")
        for error in error_logs:
            print(error.strip())

        write_error_logs(error_log_file, error_logs)
    else:
        print("로그에서 중요한 오류를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
