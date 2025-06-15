import csv
import os
import mysql.connector  # pip install mysql-connector-python로 라이브러리 설치해주세요


# MySQL 연결과 INSERT 쿼리를 쉽게 하기 위한 헬퍼 클래스
class MySQLHelper:
    def __init__(self, host, user, password):
        # MySQL 서버와 연결
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        # 쿼리 실행을 위한 커서 생성
        self.cursor = self.conn.cursor()
        self.init_database()

    def init_database(self):
        # 데이터베이스가 없으면 생성
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS mars')
        self.cursor.execute('USE mars')
        # 테이블이 없으면 생성
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mars_weather (
                weather_id INT AUTO_INCREMENT PRIMARY KEY,
                mars_date DATETIME NOT NULL,
                temp INT,
                storm INT
            )
        ''')

    # 날씨 데이터를 삽입하는 함수
    def insert_weather(self, mars_date, temp, storm):
        sql = (
            'INSERT INTO mars_weather (mars_date, temp, storm) '
            'VALUES (%s, %s, %s)'
        )
        # 실제 삽입할 값 지정
        values = (mars_date, temp, storm)
        # 쿼리 실행
        self.cursor.execute(sql, values)

    # 커밋하여 실제 DB에 반영
    def commit(self):
        self.conn.commit()

    # 커서와 연결 종료
    def close(self):
        self.cursor.close()
        self.conn.close()

# CSV 파일을 읽어 리스트로 반환
def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        # CSV 헤더를 기준으로 딕셔너리 형태로 읽음
        reader = csv.DictReader(f)
        # 리스트로 변환하여 반환
        return list(reader)


def main():
    csv_file = 'mars_weathers_data.csv'

    if not os.path.exists(csv_file):
        print(f'파일을 찾을 수 없습니다: {csv_file}')
        return

    # CSV 파일을 읽어 리스트로 저장
    data_list = read_csv(csv_file)
    print(f'{len(data_list)}개의 데이터를 읽었습니다.')

    # DB 연결 정보 설정
    db = MySQLHelper(
        host='localhost', 
        user='root',
        password='admin'
    )

    # 읽은 CSV 데이터를 하나씩 DB에 삽입
    for row in data_list:
        mars_date = row['mars_date']
        # temp 열에는 소수점이 있는 값이 존재하므로 정수로 처리
        temp = int(float(row['temp'])) if row['temp'] else None
        storm = int(row['storm']) if row['storm'] else None
        # INSERT 실행
        db.insert_weather(mars_date, temp, storm)

    # 전체 트랜잭션 커밋
    db.commit()
    # 연결 종료
    db.close()
    print('데이터 삽입 완료')


if __name__ == '__main__':
    main()
