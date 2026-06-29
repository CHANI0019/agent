import os
try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Pillow 라이브러리가 필요합니다. 설치 중...")
    import subprocess
    subprocess.check_call(["pip", "install", "Pillow"])
    from PIL import Image, ImageDraw

def create_icon(size, path, source_path=None):
    if source_path and os.path.exists(source_path):
        try:
            print(f"원본 이미지 '{source_path}' 로드 중...")
            img = Image.open(source_path)
            # Resize image with high-quality resampling
            resample_filter = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.ANTIALIAS
            img_resized = img.resize((size, size), resample=resample_filter)
            img_resized.save(path, 'PNG')
            print(f"아이콘 생성 완료 (원본 리사이즈): {path} ({size}x{size})")
            return
        except Exception as e:
            print(f"원본 이미지 처리 중 오류 발생 (기본 도형으로 대체): {e}")

    # Fallback: Procedural generation
    # 1. Create canvas with background color (#0b0f19)
    img = Image.new('RGBA', (size, size), color=(11, 15, 25, 255))
    draw = ImageDraw.Draw(img)
    
    # 2. Draw gold circle stroke (#fbbf24)
    margin = size // 10
    stroke_w = max(4, size // 36)
    draw.ellipse(
        [margin, margin, size - margin, size - margin], 
        outline=(251, 191, 36, 255), 
        width=stroke_w
    )
    
    # 3. Draw cyan center circle (#06b6d4)
    center_r = size // 8
    draw.ellipse(
        [size // 2 - center_r, size // 2 - center_r, size // 2 + center_r, size // 2 + center_r], 
        fill=(6, 182, 212, 255)
    )
    
    # 4. Draw network nodes (4 sub-nodes around center)
    node_r = size // 20
    offset = size // 4
    # Top Node
    draw.ellipse([size // 2 - node_r, size // 2 - offset - node_r, size // 2 + node_r, size // 2 - offset + node_r], fill=(251, 191, 36, 255))
    # Bottom Node
    draw.ellipse([size // 2 - node_r, size // 2 + offset - node_r, size // 2 + node_r, size // 2 + offset + node_r], fill=(251, 191, 36, 255))
    # Left Node
    draw.ellipse([size // 2 - offset - node_r, size // 2 - node_r, size // 2 - offset + node_r, size // 2 + node_r], fill=(251, 191, 36, 255))
    # Right Node
    draw.ellipse([size // 2 + offset - node_r, size // 2 - node_r, size // 2 + offset + node_r, size // 2 + node_r], fill=(251, 191, 36, 255))
    
    # Save file
    img.save(path, 'PNG')
    print(f"아이콘 생성 완료 (기본 도형): {path} ({size}x{size})")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_img = os.path.join(script_dir, 'logo_backup.png')
    create_icon(192, os.path.join(script_dir, 'icon-192.png'), source_img)
    create_icon(512, os.path.join(script_dir, 'icon-512.png'), source_img)
