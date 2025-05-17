import zipfile
import string
import time
import multiprocessing
from io import BytesIO

# 사용할 문자셋 (소문자 + 숫자)
CHARSET = string.ascii_lowercase + string.digits
PASSWORD_LENGTH = 6
BASE = len(CHARSET)

# 암호 문자열 생성기
def generate_passwords(prefix):
    # 남은 자리 수 계산
    length_to_generate = PASSWORD_LENGTH - len(prefix)
    for i in range(BASE ** length_to_generate):
        rest_password = ''
        tmp = i
        for _ in range(length_to_generate):
            rest_password = CHARSET[tmp % BASE] + rest_password
            tmp //= BASE
        # 완성된 암호 반환
        yield prefix + rest_password

# 워커 프로세스: 구간 내 암호 검증
def worker(prefix, zip_bytes, target_file, result_queue, progress_queue):
    zf = zipfile.ZipFile(BytesIO(zip_bytes))  # 메모리 IO 활용
    attempts = 0
    # 해당 구간의 전체 경우의 수
    total = BASE ** (PASSWORD_LENGTH - len(prefix))

    for password in generate_passwords(prefix):
        # 첫 글자가 알파벳이 아닐 경우 skip (핵심 조건)
        if password[0] not in string.ascii_lowercase:
            continue
        # 마지막 글자가 숫자가 아닐 경우 skip (핵심 조건)
        if password[-1] not in string.digits:
            continue

        try:
            # 암호 대입하여 파일 열기 시도
            with zf.open(target_file, pwd=password.encode('utf-8')) as file:
                # 실제 읽기를 해야 암호 검증됨
                file.read(1)  
                result_queue.put(password)
                return
        except Exception:
            pass

        attempts += 1
        if attempts % 50000 == 0:
            progress_queue.put((prefix, attempts, total, password))

# 멀티프로세스 관리 및 전체 흐름
def unlock_zip(zip_path, target_file='password.txt', output_file='password.txt'):
    try:
        with open(zip_path, 'rb') as f:
            zip_bytes = f.read()  # 디스크 IO는 여기서 딱 한 번만 발생
    except Exception as e:
        print(f"[오류] ZIP 파일 열기 실패: {e}")
        return

    manager = multiprocessing.Manager()
    result_queue = manager.Queue()
    progress_queue = manager.Queue()

    start_time = time.time()

    # 전체 순차 시도, 조건은 if문에서 필터링
    prefixes = ['']  
    total_prefixes = len(prefixes)
    total_cases = total_prefixes * (BASE ** (PASSWORD_LENGTH - len(prefixes[0])))

    print(f"암호 찾기 시작 - 총 경우의 수(필터 전): {total_cases}, 워커 수: {multiprocessing.cpu_count()}")

    running_processes = {}
    found_password = None
    # prefix 반복자 생성
    prefix_iter = iter(prefixes)

    # 다음 prefix 구간 시작 함수
    def start_next():
        try:
            prefix = next(prefix_iter)
            p = multiprocessing.Process(target=worker, args=(prefix, zip_bytes, target_file, result_queue, progress_queue))
            p.start()
            running_processes[p.pid] = (p, prefix)
        except StopIteration:
            pass

    # CPU 코어 수 만큼 워커 시작
    for _ in range(min(multiprocessing.cpu_count(), total_prefixes)):
        start_next()

    # 메인 루프 (결과 수집 및 프로세스 관리)
    while running_processes:
        if not result_queue.empty():
            # 암호 발견 시 수집
            found_password = result_queue.get()
            break

        # 진행 상황 출력
        while not progress_queue.empty():
            prefix, attempts, total, password = progress_queue.get()
            progress = (attempts / total) * 100
            elapsed = time.time() - start_time
            print(f"\r[{prefix}] {attempts}/{total} ({progress:.2f}%) | 경과: {elapsed:.2f}초 | 현재 암호: {password}", end='', flush=True)

        # 종료된 프로세스 처리 및 다음 구간 시작
        for pid, (p, prefix) in list(running_processes.items()):
            if not p.is_alive():
                p.terminate()
                p.join()
                del running_processes[pid]
                start_next()

        # 과도한 CPU 사용 방지
        time.sleep(0.1)

    # 안전 종료
    for p, _ in running_processes.values():
        p.terminate()

    if found_password:
        try:
            with open(output_file, 'w') as f:
                f.write(found_password)
            print(f"\n암호 저장 완료: {found_password}")
        except Exception as e:
            print(f"[오류] 암호 저장 실패: {e}")
    else:
        print("\n암호 찾기 실패")

    print(f"총 경과 시간: {time.time() - start_time:.2f}초")

if __name__ == "__main__":
    unlock_zip('emergency_storage_key.zip')
