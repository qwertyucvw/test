from PIL import Image, ImageDraw, ImageFont
import os

def generate_leaderboard():
    try:
        with open('LEADERBOARD.md', 'r', encoding='utf-8') as f:
            content = f.read()

        table_lines = []
        in_table = False
        for line in content.split('\n'):
            if line.startswith('|') and ('Rank' in line or '-----' in line or in_table):
                in_table = True
                table_lines.append(line.strip())
        
        if len(table_lines) < 3:
            raise ValueError("Not enough table rows found")


        headers = [h.strip() for h in table_lines[0].split('|')[1:-1]]
        data = []
        for line in table_lines[2:]:
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) == len(headers):
                data.append(parts)
        rank_idx = headers.index('Rank')
        user_idx = headers.index('Username')
        time_idx = headers.index('Total Time (s)')
        col_widths = [80, 200, 150]  # Rank, Username, Time
        row_height = 50
        header_height = 60
        img_width = sum(col_widths)
        img_height = header_height + len(data) * row_height
        
        img = Image.new('RGB', (img_width, img_height), (240, 240, 240))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 20)
            bold_font = ImageFont.truetype("arialbd.ttf", 22)
        except:
            font = ImageFont.load_default()
            bold_font = font
        x_pos = 0
        headers_display = ['Rank', 'Username', 'Time (s)']
        for i, (header, width) in enumerate(zip(headers_display, col_widths)):
            draw.rectangle([x_pos, 0, x_pos + width, header_height], 
                          fill=(50, 100, 150))
            draw.text((x_pos + width/2, header_height/2), 
                     header, font=bold_font, fill='white', anchor='mm')
            x_pos += width
        for row_idx, row in enumerate(data):
            y_pos = header_height + row_idx * row_height
            x_pos = 0
            fill_color = (255, 255, 200) if row_idx == 0 else (255, 255, 255)
            
            for col_idx, width in enumerate(col_widths):
                cell_value = ''
                if col_idx == 0:
                    cell_value = row[rank_idx]
                elif col_idx == 1:
                    cell_value = row[user_idx]
                else:
                    cell_value = row[time_idx]
                
                draw.rectangle([x_pos, y_pos, x_pos + width, y_pos + row_height], 
                              fill=fill_color, outline=(220, 220, 220))
                draw.text((x_pos + width/2, y_pos + row_height/2), 
                         cell_value, font=font, fill='black', anchor='mm')
                x_pos += width
        img.save('leaderboard.png')
        print("Leaderboard image generated successfully")
        
    except Exception as e:
        print(f"Error: {str(e)}")

        img = Image.new('RGB', (600, 150), (255, 230, 230))
        draw = ImageDraw.Draw(img)
        draw.text((300, 50), "Error generating leaderboard", fill='red', 
                 font=ImageFont.load_default(), anchor='mm')
        draw.text((300, 100), str(e), fill='red', 
                 font=ImageFont.load_default(size=14), anchor='mm')
        img.save('leaderboard.png')

if __name__ == "__main__":
    generate_leaderboard()
