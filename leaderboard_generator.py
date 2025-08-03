from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def generate_leaderboard_image():
    with open('LEADERBOARD.md', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    lines = [line.strip() for line in lines if line.strip() and not line.startswith('#') and not line.startswith('---')]

    headers = [h.strip() for h in lines[0].split('|')[1:-1]]
    try:
        rank_idx = headers.index("Rank")
        user_idx = headers.index("Username")
        time_idx = headers.index("Total Time (s)")
    except ValueError as e:
        print(f"Ошибка: Не найдена необходимая колонка ({e})")
        return
    data = []
    for line in lines[1:]:
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if len(parts) > max(rank_idx, user_idx, time_idx):
            data.append([parts[rank_idx], parts[user_idx], parts[time_idx] + "s"])
    
    col_widths = [80, 250, 150]  # Ширина колонок: Rank, Username, Time
    cell_height = 60
    header_height = 70
    img_width = sum(col_widths)
    img_height = header_height + (len(data) * cell_height)
    
    img = Image.new('RGB', (img_width, img_height), color=(25, 25, 25))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 24)
        bold_font = ImageFont.truetype("arialbd.ttf", 26)
    except:
        font = ImageFont.load_default()
        bold_font = font
   
    x_pos = 0
    for i, (header, width) in enumerate(zip(["Rank", "Username", "Time"], col_widths)):
        draw.rectangle([x_pos, 0, x_pos + width, header_height], fill=(40, 40, 40))
        draw.text((x_pos + width//2, header_height//2), header, 
                 fill=(255, 215, 0), font=bold_font, anchor="mm")
        x_pos += width
    

    for row_idx, row_data in enumerate(data):
        y_pos = header_height + (row_idx * cell_height)
        x_pos = 0
        
        for col_idx, (cell, width) in enumerate(zip(row_data, col_widths)):
            if row_idx == 0:  
                fill_color = (250, 250, 210)
            elif row_idx == 1:
                fill_color = (220, 220, 220)
            elif row_idx == 2:
                fill_color = (205, 170, 125)
            else:
                fill_color = (180, 180, 180)
            
            draw.rectangle([x_pos, y_pos, x_pos + width, y_pos + cell_height], 
                         fill=(35, 35, 35), outline=(60, 60, 60))
            draw.text((x_pos + width//2, y_pos + cell_height//2), cell, 
                     fill=fill_color, font=font, anchor="mm")
            x_pos += width

    if len(data) > 0:
     
        draw.rectangle([0, header_height + cell_height - 15, col_widths[0], header_height + cell_height], 
                      fill=(255, 215, 0))
        if len(data) > 1:
     
            draw.rectangle([0, header_height + cell_height*2 - 10, col_widths[0], header_height + cell_height*2], 
                          fill=(192, 192, 192))
        if len(data) > 2:
   
            draw.rectangle([0, header_height + cell_height*3 - 5, col_widths[0], header_height + cell_height*3], 
                          fill=(205, 127, 50))

    output_filename = "leaderboard.png"
    img.save(output_filename)
    print(f"Сгенерировано изображение: {output_filename}")

if __name__ == "__main__":
    generate_leaderboard_image()
