from PIL import Image, ImageDraw, ImageFont
import os

def generate_leaderboard():
    try:
        with open('LEADERBOARD.md', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        headers = []
        data = []
        for line in lines:
            if line.startswith('|'):
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if 'Rank' in parts and 'Username' in parts and 'Total Time' in parts:
                    headers = parts
                elif parts and len(parts) == len(headers):
                    data.append(parts)
        
        if not headers or not data:
            raise ValueError("Invalid table format in LEADERBOARD.md")

        rank_idx = headers.index('Rank')
        user_idx = headers.index('Username')
        time_idx = [i for i, h in enumerate(headers) if 'Total Time' in h][0]

        img_width = 600
        row_height = 50
        img_height = row_height * (len(data) + 1)
        
        img = Image.new('RGB', (img_width, img_height), (242, 242, 242))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", 20)
            bold_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
        except:
            font = ImageFont.load_default()
            bold_font = font


        headers = ['Rank', 'Username', 'Time (s)']
        col_widths = [80, 350, 170]
        for i, (header, width) in enumerate(zip(headers, col_widths)):
            draw.rectangle([sum(col_widths[:i]), 0, sum(col_widths[:i+1]), row_height], 
                          fill=(70, 130, 180))
            draw.text((sum(col_widths[:i]) + width/2, row_height/2), 
                     header, font=bold_font, fill='white', anchor='mm')


        for row, entry in enumerate(data, 1):
            y = row * row_height
            rank = entry[rank_idx]
            username = entry[user_idx]
            time = entry[time_idx]

            fill = (255, 255, 255) if row % 2 else (230, 240, 250)
            draw.rectangle([0, y, img_width, y + row_height], fill=fill)
            draw.text((col_widths[0]/2, y + row_height/2), rank, font=font, anchor='mm')
            draw.text((col_widths[0] + col_widths[1]/2, y + row_height/2), username, font=font, anchor='mm')
            draw.text((sum(col_widths[:2]) + col_widths[2]/2, y + row_height/2), time, font=font, anchor='mm')
        img.save('leaderboard.png')
        print("Successfully generated leaderboard.png")
        
    except Exception as e:
        print(f"Error generating leaderboard: {str(e)}")
        img = Image.new('RGB', (600, 100), (255, 200, 200))
        draw = ImageDraw.Draw(img)
        draw.text((300, 50), f"Error: {str(e)}", fill='red', anchor='mm')
        img.save('leaderboard.png')

if __name__ == "__main__":
    generate_leaderboard()
