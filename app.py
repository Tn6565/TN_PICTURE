import streamlit as st
import requests
from collections import Counter
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import time
import json

# =========================
# ページ設定（ファビコン & タイトル）
# =========================
# Chromeタブ用のアイコン（Web上でアクセス可能なURL推奨）
CHROME_ICON_URL = "https://github.com/Tn6565/TN_PICTURE/blob/5112d49b987619b73a3183da4cfe232091dc68d3/icon.png/TNICON.png"

st.set_page_config(
    page_title="Auto Stock Uploader",
    page_icon=CHROME_ICON_URL,
    layout="wide"
)

# =========================
# iPhoneホーム画面用アイコン設定
# =========================
IPHONE_ICON_180 = "https://github.com/Tn6565/TN_PICTURE/blob/5112d49b987619b73a3183da4cfe232091dc68d3/icon.png/TNICON.png"
IPHONE_ICON_152 = "https://github.com/Tn6565/TN_PICTURE/blob/5112d49b987619b73a3183da4cfe232091dc68d3/icon.png/TNICON.png"

st.markdown(
    f"""
    <link rel="apple-touch-icon" sizes="180x180" href="{IPHONE_ICON_180}">
    <link rel="apple-touch-icon" sizes="152x152" href="{IPHONE_ICON_152}">
    """,
    unsafe_allow_html=True
)

# =========================
# 初期設定
# =========================
load_dotenv()
API_KEY = os.getenv("EXTNPIXABAY")
if not API_KEY:
    st.error("Pixabay APIキーが設定されていません。`.env` に PIXABAY_API_KEY=追加してください。")
    st.stop()

BASE_URL = "https://pixabay.com/api/"
STOP_TAGS = {
    "background", "copy space", "isolated", "nobody", "space", "empty",
    "robot", "artificial intelligence"
}

USAGE_FILE = "api_usage.json"
MAX_REQUESTS_PER_HOUR = 50

def check_api_limit():
    now = int(time.time())
    if not os.path.exists(USAGE_FILE):
        usage = {"last_reset": now, "count": 0}
    else:
        with open(USAGE_FILE, "r") as f:
            usage = json.load(f)
    if now - usage["last_reset"] >= 3600:
        usage["last_reset"] = now
        usage["count"] = 0
    if usage["count"] >= MAX_REQUESTS_PER_HOUR:
        return False
    usage["count"] += 1
    with open(USAGE_FILE, "w") as f:
        json.dump(usage, f)
    return True

# =========================
# Pixabay検索
# =========================
def analyze_market(keyword: str):
    if not check_api_limit():
        st.error("API無料枠を超えたため、使用不可です")
        st.stop()
    params = {
        "key": API_KEY,
        "q": keyword,
        "image_type": "photo",
        "per_page": 100,
        "safesearch": "true"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        return {"total_hits": 0, "popular_tags": [], "error": f"API failed: {response.status_code}"}
    data = response.json()
    total_hits = data.get("totalHits", 0)
    tags = []
    tag_to_image = {}
    for hit in data.get("hits", []):
        if "tags" in hit and hit["tags"]:
            for t in hit["tags"].split(","):
                t = t.strip()
                if t.lower() not in STOP_TAGS:
                    tags.append(t)
                    if t not in tag_to_image:
                        tag_to_image[t] = hit.get("previewURL", "")
    tag_counts = Counter(tags)
    popular_tags = tag_counts.most_common(5)
    popular_tag_images = [(t, tag_to_image[t], count) for t, count in popular_tags]
    return {"total_hits": total_hits, "popular_tags": popular_tag_images}

def search_tag_images(tag: str):
    if not check_api_limit():
        st.error("API無料枠を超えたため、使用不可です")
        st.stop()
    params = {
        "key": API_KEY,
        "q": tag,
        "image_type": "photo",
        "per_page": 20,
        "safesearch": "true"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        return []
    data = response.json()
    images = [hit.get("webformatURL") for hit in data.get("hits", []) if hit.get("webformatURL")]
    return images

def display_api_usage():
    if not os.path.exists(USAGE_FILE):
        usage = {"last_reset": int(time.time()), "count": 0}
    else:
        with open(USAGE_FILE, "r") as f:
            usage = json.load(f)
    now = int(time.time())
    if now - usage["last_reset"] >= 3600:
        usage["count"] = 0
    remaining = MAX_REQUESTS_PER_HOUR - usage["count"]
    st.sidebar.subheader("🔹 Pixabay API使用状況")
    st.sidebar.write(f"1時間あたり上限: {MAX_REQUESTS_PER_HOUR}")
    st.sidebar.write(f"現在の使用数: {usage['count']}")
    st.sidebar.write(f"残りリクエスト数: {remaining}")
    st.sidebar.progress(usage['count']/MAX_REQUESTS_PER_HOUR)

# =========================
# UI設定
# =========================
st.markdown(
    """
    <style>
    .stApp {background-color: #f7f7f7;}
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color:white;
        border-radius: 12px;
        height: 3em;
        width: 12em;
        font-size: 16px;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Auto Stock Uploader")
display_api_usage()
st.sidebar.header("設定")
mode = st.sidebar.selectbox("モード選択", ["市場分析", "画像チェック＆加工", "アップロード"], key="mode_selector")

# =========================
# 市場分析
# =========================
if mode == "市場分析":
    st.subheader("市場分析")
    keyword = st.text_input("検索キーワード", key="market_keyword")
    if st.button("分析開始", key="analyze_button"):
        with st.spinner("🔄 分析中..."):
            result = analyze_market(keyword)
            time.sleep(1)
        if result["total_hits"] == 0 or len(result["popular_tags"]) == 0:
            st.warning("検索結果が0件か、関連タグが見つかりません。ワードを変えて試してください。")
        else:
            st.subheader("📊 検索結果概要")
            st.write(f"総件数: {result['total_hits']}")
            st.subheader("🔖 人気タグトップ5")
            num_cols = 5
            show_buttons = []
            for i in range(0, len(result["popular_tags"]), num_cols):
                cols = st.columns(num_cols)
                for j, (tag, img_url, count) in enumerate(result["popular_tags"][i:i+num_cols]):
                    col = cols[j]
                    with col:
                        st.markdown(
                            f"""
                            <div style="
                                width: 150px;
                                height: 280px;
                                background-color: #ffffff;
                                padding: 10px;
                                border-radius: 10px;
                                box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
                                display: flex;
                                flex-direction: column;
                                align-items: center;
                                margin: 5px 10px;
                            ">
                                <h4 style="margin:0; font-size:14px;">NO{i+j+1}</h4>
                                <div style="flex-grow:1; display:flex; align-items:flex-start; justify-content:center; width:100%;">
                                    <img src="{img_url}" style="max-width:140px; max-height:150px; object-fit:contain;"/>
                                </div>
                                <p style="margin:5px 0 0 0; text-align:center;"><b>{tag}</b><br>({count} 件)</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        show_buttons.append(tag)
            st.subheader("🔘 タグを表示")
            for tag in show_buttons:
                if st.button(f"{tag} を表示", key=f"show_{tag}"):
                    images = search_tag_images(tag)
                    if images:
                        st.subheader(f"{tag} の画像一覧")
                        for url in images:
                            st.image(url, width=200)
                    else:
                        st.info(f"{tag} に関する画像が見つかりませんでした。")
            st.subheader("📈 人気タグ件数グラフ")
            tags, _, counts = zip(*result["popular_tags"])
            fig, ax = plt.subplots(figsize=(6,4))
            ax.bar(tags, counts, color="#4FC3F7")
            ax.set_ylabel("件数")
            ax.set_title("人気タグ件数")
            st.pyplot(fig)

# =========================
# 画像チェック＆加工
# =========================
elif mode == "画像チェック＆加工":
    st.subheader("画像チェック＆加工")
    uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"], key="image_upload")
    if uploaded_file:
        st.image(uploaded_file, caption="アップロードされた画像", use_container_width=True)

# =========================
# アップロード
# =========================
elif mode == "アップロード":
    st.subheader("アップロード")
    file = st.file_uploader("アップロード画像", key="upload_image")
    if file:
        st.success("アップロード処理が完了しました")