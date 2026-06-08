#!/usr/bin/env python3
"""
Script con desplazamiento automático para los primeros frames.
"""

from PIL import Image
import os
from collections import Counter

def get_background_color(img, sample_size=10):
    pixels = []
    width, height = img.size
    for x in range(0, sample_size):
        for y in range(0, sample_size):
            pixels.append(img.getpixel((x, y)))
        for y in range(height - sample_size, height):
            pixels.append(img.getpixel((x, y)))
    most_common = Counter(pixels).most_common(1)[0][0]
    return most_common[:3]

def extract_and_crop_sprite_sheet(
    sheet_path,
    output_folder,
    num_frames,
    frame_width,
    target_size=None,
    padding=12,
    first_frames_shift=6   # ← Píxeles que se desplazan los primeros frames a la derecha
):
    os.makedirs(output_folder, exist_ok=True)
    
    sheet = Image.open(sheet_path).convert('RGBA')
    sheet_width, sheet_height = sheet.size
    frame_height = sheet_height
    
    # Detectar color de fondo
    first_frame = sheet.crop((0, 0, frame_width, frame_height))
    background_color = get_background_color(first_frame)
    print(f"Color de fondo detectado: RGB{background_color}")
    
    print(f"Sprite sheet: {sheet_width}x{sheet_height}")
    print(f"Frames: {num_frames} | Frame width: {frame_width}")
    
    frames_data = []
    centers = []
    
    for i in range(num_frames):
        left = i * frame_width
        right = min(left + frame_width, sheet_width)
        frame = sheet.crop((left, 0, right, frame_height))
        
        # Quitar fondo
        datas = frame.getdata()
        new_data = []
        for item in datas:
            r, g, b, a = item
            if (abs(r - background_color[0]) < 30 and
                abs(g - background_color[1]) < 30 and
                abs(b - background_color[2]) < 30):
                new_data.append((r, g, b, 0))
            else:
                new_data.append(item)
        frame.putdata(new_data)
        
        bbox = frame.getbbox()
        if bbox:
            cropped = frame.crop(bbox)
            center_x = bbox[0] + (bbox[2] - bbox[0]) // 2
            centers.append(center_x)
            frames_data.append((i + 1, cropped))
        else:
            print(f"  Frame {i+1} vacío")
    
    if not frames_data:
        print("No se pudo procesar ningún frame.")
        return
    
    avg_center = sum(centers) // len(centers)
    print(f"Centro promedio: {avg_center}")
    
    max_w = max(f.width for _, f in frames_data)
    max_h = max(f.height for _, f in frames_data)
    
    if target_size:
        final_w, final_h = target_size
    else:
        final_w = max_w + padding * 2
        final_h = max_h + padding * 2
    
    print(f"Tamaño final: {final_w}x{final_h}")
    
    for frame_num, cropped in frames_data:
        new_frame = Image.new('RGBA', (final_w, final_h), (0, 0, 0, 0))
        
        paste_x = (final_w - cropped.width) // 2
        paste_y = (final_h - cropped.height) // 2
        
        # === DESPLAZAR LOS PRIMEROS 3 FRAMES A LA DERECHA ===
        if frame_num <= 3:
            paste_x += first_frames_shift
        
        new_frame.paste(cropped, (paste_x, paste_y), cropped)
        
        filename = f"idle{frame_num}.png"
        new_frame.save(os.path.join(output_folder, filename))
        print(f"  Guardado: {filename}")
    
    print(f"\n¡Completado! Frames guardados en: {output_folder}")


if __name__ == "__main__":
    # ==================== CONFIGURA AQUÍ ====================
    
    SHEET_PATH        = "assets/mario_sheet.png"
    OUTPUT_FOLDER     = "assets/mario"
    NUM_FRAMES        = 38
    FRAME_WIDTH       = 47
    TARGET_SIZE       = None
    PADDING           = 12
    FIRST_FRAMES_SHIFT = 6     # ← Píxeles que se mueven los primeros 3 frames
    
    # =======================================================
    
    extract_and_crop_sprite_sheet(
        SHEET_PATH,
        OUTPUT_FOLDER,
        NUM_FRAMES,
        FRAME_WIDTH,
        TARGET_SIZE,
        PADDING,
        FIRST_FRAMES_SHIFT
    )