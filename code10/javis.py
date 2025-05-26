import os
import wave
import datetime
import threading
import msvcrt
import pyaudio

def prepare_directory(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def get_timestamp_filename(folder):
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d-%H%M%S')
    return os.path.join(folder, f'{timestamp}.wav')


def save_to_file(path, frames, channels, rate, format):
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))


def record_audio():
    folder = 'records'
    prepare_directory(folder)

    channels = 1
    rate = 44100
    chunk = 1024
    format = pyaudio.paInt16
    frames = []
    is_recording = True

    def listen_keyboard():
        nonlocal is_recording
        msvcrt.getch()
        is_recording = False

    threading.Thread(target=listen_keyboard, daemon=True).start()

    audio = pyaudio.PyAudio()
    stream = audio.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

    print('녹음 중... (아무 키나 누르면 종료)')

    while is_recording:
        data = stream.read(chunk)
        frames.append(data)

    print('녹음 종료.')

    stream.stop_stream()
    stream.close()
    audio.terminate()

    path = get_timestamp_filename(folder)
    save_to_file(path, frames, channels, rate, format)
    print(f'파일 저장 완료: {path}')


if __name__ == '__main__':
    record_audio()
