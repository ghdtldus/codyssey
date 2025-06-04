import os
import wave
import datetime
import threading
import msvcrt  # Windows용 키 입력 감지 모듈
import pyaudio  # 마이크 입력 및 오디오 처리 라이브러리
import csv
import contextlib
import speech_recognition as sr

# 폴더가 없으면 생성 (녹음 파일 저장용)
def prepare_directory(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

# 현재 시각 기반으로 '년월일-시간분초.wav' 형식의 파일명 생성
def get_timestamp_filename(folder):
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d-%H%M%S')
    return os.path.join(folder, f'{timestamp}.wav')

# 녹음된 오디오 데이터를 지정된 path에 .wav 파일로 저장
def save_to_file(path, frames, channels, rate, format):
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(channels)  # 채널 수
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(format))  # 샘플당 바이트 수
        wf.setframerate(rate)  # 초당 샘플 수
        wf.writeframes(b''.join(frames))  # 모든 오디오 데이터를 하나로 합쳐 저장

# 해당 파일의 재생 시간을 계산해서 반환
def get_wav_duration(path):
    # contextlib.closing()을 사용하여여 파일을 닫아줌
    with contextlib.closing(wave.open(path, 'r')) as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
    return duration


def transcribe_audio_to_csv(wav_path):
    # SpeechRecognition 라이브러리의 음성 인식기 객체 생성
    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_path) as source:
        duration = get_wav_duration(wav_path)
        interval = 5 
        results = []

        # 0초부터 전체 길이까지 5초씩 이동하며 반복
        for offset in range(0, int(duration), interval):
            try:
                audio = recognizer.record(source, duration=interval)
                # 추출한 음성을 Google STT API를 이용해 한국어 텍스트로 변환
                text = recognizer.recognize_google(audio, language='ko-KR')
                timestamp = str(datetime.timedelta(seconds=offset))
                results.append((timestamp, text))
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f'STT 요청 실패: {e}')
                break

    # sample.wav → sample.csv
    csv_path = wav_path.replace('.wav', '.csv')

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['시간', '텍스트'])
        for timestamp, text in results:
            writer.writerow([timestamp, text])

    print(f'STT 결과 저장 완료: {csv_path}')


def record_audio():
    folder = 'records'
    prepare_directory(folder)

    # 오디오 녹음 설정값 정의
    channels = 1          # 채널 수
    rate = 44100          # CD 품질 (샘플링 속도)
    chunk = 1024          # 한번에 읽는 데이터 양
    format = pyaudio.paInt16  # 16비트 정수 오디오
    frames = []           # 녹음 데이터 누적 저장용 리스트
    is_recording = True   # True인 동안 녹음 계속

    # 키보드 입력 감지 함수 (누르면 녹음 종료)
    def listen_keyboard():
        # 바깥 함수의 지역 변수를 안쪽 함수에서 수정하고싶을 때 nonlocal
        nonlocal is_recording
        # 사용자가 키를 누를 때까지 기다리고, 누른 키 한 글자를 바이트 형태로 반환
        msvcrt.getch() 
        is_recording = False

    # listen_keyboard()를 백그라운드에서 실행 (녹음과 동시에 진행)
    # -> 백그라운드에서 키보드 입력 감지해서 is_recording = False 만듦
    threading.Thread(target=listen_keyboard, daemon=True).start()

    # 마이크 장치 초기화 및 스트림 열기
    audio = pyaudio.PyAudio()

    # 마이크로부터 데이터를 받을 스트림 객체 열여서 준비
    # 오디오 데이터를 어떻게 녹음할지를 결정하는 옵션 넣기
    stream = audio.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)  

    print('녹음 중... (아무 키나 누르면 종료)')

    # 녹음 루프 시작 : 실시간으로 마이크 데이터 읽어서 frames에 저장
    while is_recording:
        data = stream.read(chunk)  # chunk 단위로 데이터 읽기
        frames.append(data)        # 리스트에 누적 저장

    print('녹음 종료.')

    # 마이크 및 PyAudio 자원 정리
    stream.stop_stream()  # 스트림 중지
    stream.close()        # 스트림 닫기
    audio.terminate()     # PyAudio 세션 종료

    # 저장 경로 생성 및 파일 저장
    path = get_timestamp_filename(folder)
    save_to_file(path, frames, channels, rate, format)

    print(f'파일 저장 완료: {path}')

    # STT 및 CSV 저장
    transcribe_audio_to_csv(path)

# 보너스 과제 !!
def search_keyword_in_csv_files(keyword):
    folder = 'records'
    if not os.path.exists(folder):
        print('CSV 파일 폴더가 없습니다.')
        return

    found = False
    # records 폴더 안의 모든 파일 중에서 
    for filename in os.listdir(folder):
        # .csv로 끝나는 파일만 처리
        if filename.endswith('.csv'):
            path = os.path.join(folder, filename)
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)  
                # 두 번째 열에 키워드가 포함되어 있는지
                for row in reader:
                    if keyword in row[1]:
                        if not found:
                            print(f'\n키워드 "{keyword}" 검색 결과:\n')
                        found = True
                        print(f'{filename} - {row[0]}: {row[1]}')

    if not found:
        print(f'키워드 "{keyword}"를 포함하는 텍스트를 찾을 수 없습니다.')

# 프로그램 실행 진입점
if __name__ == '__main__':
    print('1: 녹음 및 STT 실행')
    print('2: 키워드로 CSV 내용 검색')
    choice = input('실행할 작업 번호를 입력하세요: ').strip()

    if choice == '1':
        record_audio()

    elif choice == '2':
        keyword = input('검색할 키워드를 입력하세요: ').strip()
        search_keyword_in_csv_files(keyword)
    else:
        print('올바른 번호를 입력해주세요.')
