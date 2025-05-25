import os

# password.txt 파일에서 암호문 읽기
def read_password_text():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, "password.txt")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readline().strip()  
    except FileNotFoundError:
        print("password.txt 파일을 찾을 수 없음음")
        return None

# 카이사르 복호화 함수 
def caesar_cipher_decode(target_text):
    results = []

    # 카이사르 암호 : 알파벳을 일정한 수만큼 밀어서 다른 글자로 바꾸는 방식임
    # shift 자릿수는 0 ~ 25 (26개)
    # shift가 0일 때 : 0만큼 밀었다는 뜻
    for shift in range(26):
        decoded = ""
        for char in target_text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                decoded += chr((ord(char) - base - shift) % 26 + base)
            else:
                decoded += char  
        results.append((shift, decoded))

    print(f"\n암호문: {target_text}")
    print("가능한 복호화 결과 (shift 0~25):\n")
    for shift, result in results:
        print(f"[shift {shift}] {result}")

    while True:
        try:
            selected = int(input("\n맞는 shift 번호를 입력(0~25): "))
            if 0 <= selected <= 25:
                break
            else:
                print("0~25 사이의 숫자를 입력")
        except ValueError:
            print("숫자를 입력")

    final = results[selected][1]

    try:
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(f"[shift {selected}] {final}\n")
        print("\n복호화 결과가 result.txt에 저장")
    except Exception as e:
        print(f"result.txt 저장 중 오류 발생: {e}")

if __name__ == "__main__":
    text = read_password_text()
    if text:
        caesar_cipher_decode(text)
