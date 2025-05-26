import os
import wave
import datetime
import threading
import msvcrt  
import pyaudio


class VoiceRecorder:
    def __init__(self, folder='records'):
        self.folder = folder
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.frames = []
        self.is_recording = True
        self._prepare_directory()

    def _prepare_directory(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def _get_timestamp_filename(self):
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y%m%d-%H%M%S')
        return os.path.join(self.folder, f'{timestamp}.wav')

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.format,
                            channels=self.channels,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=self.chunk)

        print('녹음 중... (아무 키나 누르면 종료)')

        def listen_keyboard():
            msvcrt.getch()
            self.is_recording = False

        threading.Thread(target=listen_keyboard, daemon=True).start()

        while self.is_recording:
            data = stream.read(self.chunk)
            self.frames.append(data)

        print('녹음 종료.')
        stream.stop_stream()
        stream.close()
        audio.terminate()

        path = self._get_timestamp_filename()
        self._save_to_file(path, self.frames)
        print(f'파일 저장 완료: {path}')

    def _save_to_file(self, path, frames):
        with wave.open(path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))


if __name__ == '__main__':
    recorder = VoiceRecorder()
    recorder.record()
