def generate_related_tags(base_tag: str) -> list:
    """
    キーワードに関連するタグを生成
    戻り値: 関連タグのリスト
    """
    if not isinstance(base_tag, str):
        raise ValueError("base_tagはstr型である必要があります")
    return [base_tag, f"{base_tag} art", f"{base_tag} concept"]