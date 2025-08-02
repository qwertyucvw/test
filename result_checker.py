import os
import json
import sys

def main():
    results_dir = "results"
    if not os.path.exists(results_dir):
        print(f"Error: Results directory '{results_dir}' not found")
        return 1
    
    files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
    if not files:
        print(f"Error: No JSON files found in '{results_dir}'")
        return 1
    
    required_fields = [
        "username", 
        "generation_time", 
        "sorting_time", 
        "total_time", 
        "correctly_sorted"
    ]
    
    errors = []
    valid_count = 0
    
    for filename in files:
        filepath = os.path.join(results_dir, filename)
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            # Проверка обязательных полей
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                errors.append(f"{filename}: Missing fields - {', '.join(missing_fields)}")
                continue
                
            # Проверка типов данных
            if not isinstance(data['username'], str):
                errors.append(f"{filename}: username must be string")
                continue
                
            if not all(isinstance(data[field], (int, float)) for field in ['generation_time', 'sorting_time', 'total_time']):
                errors.append(f"{filename}: Time fields must be numbers")
                continue
                
            if not isinstance(data['correctly_sorted'], bool):
                errors.append(f"{filename}: correctly_sorted must be boolean")
                continue
                
            # Дополнительные проверки
            if data['total_time'] != data['generation_time'] + data['sorting_time']:
                errors.append(f"{filename}: total_time doesn't match sum of generation_time and sorting_time")
                continue
                
            valid_count += 1
                
        except json.JSONDecodeError:
            errors.append(f"{filename}: Invalid JSON format")
        except Exception as e:
            errors.append(f"{filename}: Unexpected error - {str(e)}")
    
    if errors:
        print("\nValidation errors found:")
        for error in errors:
            print(f" - {error}")
        print(f"\n{len(errors)} files have errors, {valid_count} files are valid")
        return 1
    
    print(f"Validation successful! All {valid_count} files are valid")
    return 0

if __name__ == "__main__":
    sys.exit(main())
