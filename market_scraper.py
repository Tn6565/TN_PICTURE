import streamlit as st

# =========================
# ダミー版 analyze_market
# =========================
def analyze_market(keyword):
    """
    検索ワードに応じて総件数と人気タグを返すテスト用関数
    """
    # 総件数：検索ワードの文字数×123（簡易変化）
    total_hits = len(keyword) * 123

    # 人気タグ：検索ワードを含めて生成
    popular_tags = [
        f"{keyword} AI",
        f"{keyword} tech",
        f"{keyword} trends"
    ]

    return {
        "total_hits": total_hits,
        "popular_tags": popular_tags
    }

# =========================
# Streamlit UI
# =========================
st.title("Auto Stock Uploader")

st.sidebar.header("設定")
# 🔹 key を追加してID重複を防止
mode = st.sidebar.selectbox(
    "モード選択",
    ["市場分析", "画像チェック＆加工", "アップロード"],
    key="mode_select"
)

if mode == "市場分析":
    st.subheader("市場分析")
    keyword = st.text_input("検索キーワード", key="keyword_input")
    if st.button("分析開始", key="analyze_btn"):
        results = analyze_market(keyword)

        # 総件数と人気タグのみ表示するカードUI
        if isinstance(results, dict):
            total_hits = results.get("total_hits", "N/A")
            popular_tags = results.get("popular_tags", [])

            st.markdown(
                f"""
                <div style="
                    box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
                    padding:20px;
                    border-radius:15px;
                    background-color:#ffffff;
                    max-width:600px;
                    margin-bottom:20px;
                ">
                    <h3 style="margin-bottom:10px;">📊 検索結果概要</h3>
                    <p style="font-size:28px; color:#2E86C1; font-weight:bold; margin:5px 0;">
                        総件数: {total_hits}
                    </p>
                    <p style="margin:10px 0 5px 0; font-weight:bold;">🔖 人気タグ:</p>
                    <div>
                        {" ".join([f"<span style='background-color:#F5B041;color:white;padding:5px 12px;border-radius:12px;margin-right:5px;margin-top:5px;display:inline-block'>{tag}</span>" for tag in popular_tags])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("結果が見つかりませんでした")

elif mode == "画像チェック＆加工":
    st.subheader("画像チェック＆加工")
    uploaded_file = st.file_uploader("画像をアップロード", type=["png","jpg","jpeg"], key="upload_file")
    if uploaded_file:
        from originality_guard import check_originality
        from fix_module import enhance_image

        similarity = check_originality(uploaded_file)
        if similarity < 0.9:
            enhanced_image = enhance_image(uploaded_file)
            st.image(enhanced_image, caption="加工済み画像")
        else:
            st.error(f"類似度が高すぎます（{similarity*100:.1f}%）")

elif mode == "アップロード":
    st.subheader("アップロード")
    file = st.file_uploader("アップロード画像", key="adobe_upload")
    if file:
        from uploader import upload_to_adobe
        response = upload_to_adobe(file)
        st.write(response)
