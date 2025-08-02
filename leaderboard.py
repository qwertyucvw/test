import os
import json
import glob
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from tabulate import tabulate

def generate_leaderboard():
    print("="*60)
    print("🏆 Starting Code Execution Leaderboard Generation")
    print("="*60)
    
    # Создаем папку для результатов
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    print(f"📂 Results directory: {os.path.abspath(results_dir)}")
    
    # Собираем все результаты
    all_results = []
    for filepath in glob.glob(os.path.join(results_dir, "*.json")):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
                # Извлекаем никнейм из данных или имени файла
                if 'username' in data:
                    username = data['username']
                else:
                    # Для обратной совместимости
                    username = os.path.splitext(os.path.basename(filepath))[0]
                    data['username'] = username
                
                all_results.append(data)
                print(f"📥 Loaded result: {username} - Total time: {data['total_time']:.2f}ms")
        except Exception as e:
            print(f"⚠️ Error processing {filepath}: {str(e)}")
    
    if not all_results:
        print("❌ No valid results found. Creating sample data...")
        sample_data = [
            {"username": "sample_user", "generation_time": 15.23, "sorting_time": 25.41, 
             "total_time": 40.64, "correctly_sorted": True}
        ]
        all_results = sample_data
    
    # Сортируем по общему времени выполнения (чем меньше - тем лучше)
    sorted_results = sorted(all_results, key=lambda x: x['total_time'])
    
    # Генерация Markdown таблицы
    leaderboard_md = "# 🏆 Code Execution Leaderboard\n\n"
    leaderboard_md += "Rank | Username | Total Time (ms) | Generation (ms) | Sorting (ms) | Correctly Sorted\n"
    leaderboard_md += "-----|----------|-----------------|-----------------|--------------|-----------------\n"
    
    for i, result in enumerate(sorted_results, 1):
        status_icon = "✅" if result['correctly_sorted'] else "❌"
        leaderboard_md += (
            f"{i} | {result['username']} | {result['total_time']:.2f} | "
            f"{result['generation_time']:.2f} | {result['sorting_time']:.2f} | "
            f"{status_icon}\n"
        )
    
    # Генерация графика
    if sorted_results:
        usernames = [result['username'] for result in sorted_results]
        total_times = [result['total_time'] for result in sorted_results]
        
        plt.figure(figsize=(14, 8))
        bars = plt.barh(usernames, total_times, color='skyblue')
        plt.xlabel('Total Time (ms)')
        plt.title('Code Execution Leaderboard (Lower is Better)')
        plt.gca().invert_yaxis()  # Лучший результат сверху
        
        # Добавляем значения на график
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                     f'{width:.2f}ms', 
                     ha='left', va='center')
        
        plt.tight_layout()
        plt.savefig('leaderboard.png')
        print("\n📊 Generated leaderboard.png visualization")
    
    # Сохраняем результаты в JSON
    with open('leaderboard.json', 'w') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "results": sorted_results
        }, f, indent=2)
    
    # Сохраняем Markdown файл
    with open("LEADERBOARD.md", "w") as f:
        f.write(leaderboard_md)
    
    print("\n" + "="*60)
    print(f"🏁 Leaderboard generation complete! Top performer: {sorted_results[0]['username']}")
    print(f"  - Total time: {sorted_results[0]['total_time']:.2f}ms")
    print("="*60)

if __name__ == "__main__":
    generate_leaderboard()
