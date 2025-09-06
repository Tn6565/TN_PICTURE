from PIL import Image

def check_originality(image: Image.Image) -> float:
    """
    市場に既存する画像との類似度をチェック
    戻り値: 類似率（0～1、0に近いほどオリジナル）
    """
    # 実際にはここで画像特徴量抽出＋DB比較
    # 仮ロジックとして常に0.3返す
    return 0.3