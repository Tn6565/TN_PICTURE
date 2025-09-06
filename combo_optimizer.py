def optimize_combo(tags: list, genre: str) -> dict:
    """
    ジャンル×タグの最適な組み合わせを提案
    戻り値: {"genre": ジャンル, "optimized_tags": 最適化されたタグリスト}
    """
    if not isinstance(tags, list):
        raise ValueError("tagsはlist型である必要があります")
    if not isinstance(genre, str):
        raise ValueError("genreはstr型である必要があります")
    return {"genre": genre, "optimized_tags": tags[:5]}