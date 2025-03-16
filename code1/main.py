log_file = "mission_computer_main.log"
error_log_file = "error_logs.txt"

try:
    with open(log_file, "r", encoding="utf-8") as file:
        lines = file.readlines()  
    lines.reverse()  

    # 문제가 있는 로그만 필터링 (unstable, explosion 키워드 포함 여부)
    error_logs = [line for line in lines if "unstable" in line.lower() or "explosion" in line.lower()]

    with open(error_log_file, "w", encoding="utf-8") as error_file:
        error_file.writelines(error_logs)
    print(f"문제 로그가 '{error_log_file}' 파일에 저장되었습니다.")
    for line in lines:
        print(line.strip())  

except FileNotFoundError:    
    print(f"파일 '{log_file}'을(를) 찾을 수 없습니다. 파일명을 확인하세요!")
except IsADirectoryError:
    print(f"'{log_file}'은(는) 파일이 아니라 디렉터리입니다. 올바른 파일을 선택하세요.")
except PermissionError:
    print(f"'{log_file}' 파일에 대한 읽기 권한이 없습니다. 관리자 권한으로 실행하거나 권한을 변경하세요.")
except UnicodeDecodeError:
    print(f"'{log_file}' 파일을 읽는 중 인코딩 오류가 발생했습니다. 올바른 인코딩을 사용하세요.")
except IOError:
    print(f"'{log_file}' 파일을 읽는 중 입출력(IO) 오류가 발생했습니다. 디스크 상태를 확인하세요.")
except OSError:
    print(f"'{log_file}' 파일을 여는 중 운영 체제(OS) 오류가 발생했습니다.")
except Exception as e:
    print(f"알 수 없는 오류 발생: {e}")
