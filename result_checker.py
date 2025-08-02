import os
import json
import glob

def validate_results():
    results_dir = "results"
    valid_count = 0
    total_count = 0
    
    # Проверяем существование папки с результатами
    if not os.path.exists(results_dir):
        print(f"❌ Error: Results directory '{results_dir}' not found!")
        return 1
    
    print(f"🔍 Checking results in '{results_dir}' directory...")
    
    # Проверяем все JSON-файлы в папке результатов
    for filepath in glob.glob(os.path.join(results_dir, "*.json")):
        try:
            total_count += 1
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            # Проверяем обязательные поля
            required_fields = [
                "username", "generation_time", 
                "sorting_time", "total_time", "correctly_sorted"
            ]
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                print(f"❌ {filepath}: Missing fields - {', '.join(missing_fields)}")
                continue
                
            # Проверяем типы данных
            if not isinstance(data["username"], str):
                print(f"❌ {filepath}: Invalid username type")
                continue
                
            if not all(isinstance(data[field], (int, float)) for field in ["generation_time", "sorting_time", "total_time"]):
                print(f"❌ {filepath}: Time fields must be numbers")
                continue
                
            if not isinstance(data["correctly_sorted"], bool):
                print(f"❌ {filepath}: correctly_sorted must be boolean")
                continue
                
            # Проверяем логическую согласованность
            if abs(data["total_time"] - (data["generation_time"] + data["sorting_time"])) > 0.1:
                print(f"❌ {filepath}: Total time doesn't match sum of generation and sorting times")
                continue
                
            # Если все проверки пройдены
            valid_count += 1
            print(f"✅ {filepath}: Valid result for {data['username']}")
            
        except json.JSONDecodeError:
            print(f"❌ {filepath}: Invalid JSON format")
        except Exception as e:
            print(f"❌ {filepath}: Unexpected error - {str(e)}")
    
    # Выводим итоговый отчет
    print("\n" + "="*50)
    print(f"Validation complete!")
    print(f"Valid results: {valid_count}/{total_count}")
    print(f"Invalid results: {total_count - valid_count}")
    print("="*50)
    
    return 0 if valid_count == total_count and total_count > 0 else 1

if __name__ == "__main__":
    exit(validate_results())
