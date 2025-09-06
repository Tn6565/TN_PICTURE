def optimize_tags(tags: list) -> list:
    """
    関連タグを自動最適化
    重複排除＆ソート
    戻り値: 最適化されたタグリスト
    """
    if not isinstance(tags, list):
        raise ValueError("tagsはlist型である必要があります")
    return sorted(set(tags))