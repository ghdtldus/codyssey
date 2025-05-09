import csv
import os

class InventoryItem:
    def __init__(self, substance, weight, specific_gravity, strength, flammability):
        self.substance = substance
        self.weight = weight
        self.specific_gravity = specific_gravity
        self.strength = strength
        self.flammability = float(flammability)

class Inventory:
    def __init__(self):
        self.items = []
        self.filename = "Mars_Base_Inventory_List.csv"
        self.filepath = self.get_csv_filepath() 

    def get_csv_filepath(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, self.filename)

    def file_exists(self):
        return os.path.exists(self.filepath)
    

    def read_from_csv(self, filename):
        #2 .CSV 파일을 읽어 InventoryItem 객체로 변환하여 리스트에 저장
        if not self.file_exists():
            print(f"오류: {self.filepath} 파일을 찾을 수 없습니다!")
            return []

        with open(filename, mode='r', newline='', encoding='utf-8') as file:  # filename 사용
            csv_reader = csv.reader(file)
            next(csv_reader)  
            for row in csv_reader:
                substance, weight, specific_gravity, strength, flammability = row
                item = InventoryItem(substance, weight, specific_gravity, strength, flammability)
                self.items.append(item)

    #원본 데이터를 그대로 출력
    def print_inventory(self):
        for item in self.items:
            print(f"{item.substance}, {item.weight}, {item.specific_gravity}, {item.strength}, {item.flammability}")

    #인화성 기준으로 내림차순 정렬
    def sort_by_flammability(self):
        self.items.sort(key=lambda item: item.flammability, reverse=True)

    #인화성 지수가 threshold 이상인 항목을 필터링
    def filter_by_flammability(self, threshold=0.7):
        filtered_items = [item for item in self.items if item.flammability >= threshold]
        self.print_filtered_items(filtered_items, threshold)
        return filtered_items

    #필터링된 항목을 출력
    def print_filtered_items(self, filtered_items, threshold):
        print(f"----- (Items with Flammability >= {threshold}) -----")
        for item in filtered_items:
            print(f"{item.substance}, {item.weight}, {item.specific_gravity}, {item.strength}, {item.flammability}")

    #필터링된 항목들을 CSV 파일로 저장
    def save_to_csv(self, filename, items):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            header = ['Substance', 'Weight', 'Specific Gravity', 'Strength', 'Flammability']
            csv_writer.writerow(header)
            for item in items:
                csv_writer.writerow([item.substance, item.weight, item.specific_gravity, item.strength, item.flammability])

def main():
    inventory = Inventory()
    
    # 1. CSV 파일 읽기
    inventory.read_from_csv('Mars_Base_Inventory_List.csv')

    # 1-2. CSV 파일 원본 그대로 출력
    print("----- (Original Inventory) -----")
    inventory.print_inventory()
    
    # 3. 인화성 기준으로 정렬만 함
    inventory.sort_by_flammability()
    
    # 4. 인화성 지수가 0.7 이상인 항목 필터링
    flammable_items = inventory.filter_by_flammability(0.7)
    
    # 5. 인화성 지수가 0.7 이상인 항목을 새로운 CSV 파일로 저장
    inventory.save_to_csv('Mars_Base_Inventory_danger.csv', flammable_items)
    print("Flammable items have been saved to Mars_Base_Inventory_danger.csv")

if __name__ == "__main__":
    main()
