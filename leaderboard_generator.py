from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def generate_leaderboard_image():
    with open('LEADERBOARD.md', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip() and not line.startswith('#') and not line.startswith('---')]
    headers = [h.strip() for h in lines[0].split('|')[1:-1]]
    data = [[p.strip() for p in line.split('|')[1:-1]] for line in lines[1:]]

    cell_width, cell_height = 200, 50
    rows, cols = len(data) + 1, len(headers)
    img = Image.new('RGB', (cell_width * cols, cell_height * rows), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    for i, header in enumerate(headers):
        draw.rectangle([i*cell_width, 0, (i+1)*cell_width, cell_height], outline=(0, 0, 0))
        draw.text((i*cell_width + cell_width//2, cell_height//2), header, fill=(0, 0, 0), font=font, anchor="mm")
    
    for row in range(len(data)):
        for col in range(len(data[row])):
            draw.rectangle([col*cell_width, (row+1)*cell_height, (col+1)*cell_width, (row+2)*cell_height], outline=(0, 0, 0))
            draw.text((col*cell_width + cell_width//2, (row+1)*cell_height + cell_height//2), data[row][col], fill=(0, 0, 0), font=font, anchor="mm")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"leaderboard_{timestamp}.png"
    img.save(output_filename)
    print(f"Generated {output_filename}")

if __name__ == "__main__":
    generate_leaderboard_image()
