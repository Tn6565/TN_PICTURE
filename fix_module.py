from PIL import Image, ImageEnhance

def enhance_image(image: Image.Image) -> Image.Image:
    """
    画像の明るさ補正・リサイズ・メタデータ削除など
    """
    # 明るさ補正（例：1.2倍）
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.2)

    # リサイズ（例：長辺を1024pxに揃える）
    max_size = 1024
    image.thumbnail((max_size, max_size), Image.LANCZOS)

    # メタデータ削除（新しいImageにコピー）
    image_no_meta = Image.new(image.mode, image.size)
    image_no_meta.putdata(list(image.getdata()))

    return image_no_meta