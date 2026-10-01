import streamlit as st
import json
import os
from datetime import datetime

# ==========================================
# 1. ენების ლექსიკონი (TRANSLATIONS)
# ==========================================
TRANSLATIONS = {
    "English": {
        "welcome": "Welcome to GameOfUs",
        "journal_title": "Emotional Journal & Mood Log",
        "rewards_title": "Reward Store (Fri–Sun)",
        "rewards_locked": "Rewards are only available Friday through Sunday!",
        "xp_points": "Your Current XP",
        "save_button": "Save Entry",
        "select_language": "Choose Language",
        "settings": "Settings",
        "saved_success": "Saved successfully!"
    },
    "Русский": {
        "welcome": "Добро пожаловать в GameOfUs",
        "journal_title": "Дневник эмоций и настроения",
        "rewards_title": "Магазин наград (Пт–Вс)",
        "rewards_locked": "Награды доступны только с пятницы по воскресенье!",
        "xp_points": "Ваши очки XP",
        "save_button": "Сохранить",
        "select_language": "Выберите язык",
        "settings": "Настройки",
        "saved_success": "Успешно сохранено!"
    },
    "Türkçe": {
        "welcome": "GameOfUs'a Hoş Geldiniz",
        "journal_title": "Duygu ve Mod Günlüğü",
        "rewards_title": "Ödül Mağazası (Cuma–Pazar)",
        "rewards_locked": "Ödüller yalnızca Cuma ve Pazar günleri arasında kullanılabilir!",
        "xp_points": "Mevcut XP Puanınız",
        "save_button": "Kaydet",
        "select_language": "Dil Seçin",
        "settings": "Ayarlar",
        "saved_success": "Başarıyla kaydedildi!"
    },
    "中文": {
        "welcome": "欢迎来到 GameOfUs",
        "journal_title": "情绪与心情日志",
        "rewards_title": "奖励商店（周五至周日）",
        "rewards_locked": "奖励仅在周五至周日期间开放！",
        "xp_points": "当前的 XP 积分",
        "save_button": "保存记录",
        "select_language": "选择语言",
        "settings": "设置",
        "saved_success": "保存成功！"
    },
    "日本語": {
        "welcome": "GameOfUs へようこそ",
        "journal_title": "感情・ mood ログ",
        "rewards_title": "ご褒美ストア（金〜日）",
        "rewards_locked": "ご褒美は金曜日から日曜日までのみ利用可能です！",
        "xp_points": "現在の XP ポイント",
        "save_button": "保存する",
        "select_language": "言語を選択",
        "settings": "設定",
        "saved_success": "正常に保存されました！"
    }
}

DATA_FILE = "user_data.json"

# ==========================================
# 2. მონაცემების ჩატვირთვა / შენახვა
# ==========================================
def load_user_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"xp": 0, "language": "English", "journal": []}

def save_user_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ==========================================
# 3. SESSION STATE & ენის ინიციალიზაცია
# ==========================================
user_data = load_user_data()

if "language" not in st.session_state:
    st.session_state["language"] = user_data.get("language", "English")

# თარგმნის დამხმარე ფუნქცია
def t(key):
    lang = st.session_state["language"]
    return TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, key)

# ==========================================
# 4. SIDEBAR - ენის არჩევანი
# ==========================================
st.sidebar.title(f"⚙️ {t('settings')}")

language_options = ["English", "Русский", "Türkçe", "中文", "日本語"]
current_lang_idx = language_options.index(st.session_state["language"]) if st.session_state["language"] in language_options else 0

selected_lang = st.sidebar.selectbox(
    t("select_language"),
    options=language_options,
    index=current_lang_idx
)

# ენის ცვლილების ასახვა და შენახვა
if selected_lang != st.session_state["language"]:
    st.session_state["language"] = selected_lang
    user_data["language"] = selected_lang
    save_user_data(user_data)
    st.rerun()

# ==========================================
# 5. მთავარი ინტერფეისი
# ==========================================
st.title(t("welcome"))

# XP ქულები
st.metric(label=t("xp_points"), value=user_data.get("xp", 0))

st.divider()

# დღიურის სექცია
st.header(t("journal_title"))
entry_text = st.text_area("...", height=100)

if st.button(t("save_button")):
    if entry_text.strip():
        new_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text": entry_text
        }
        user_data.setdefault("journal", []).append(new_entry)
        user_data["xp"] = user_data.get("xp", 0) + 10  # 10 XP ყოველ ჩანაწერზე
        save_user_data(user_data)
        st.success(t("saved_success"))
        st.rerun()

st.divider()

# ჯილდოების მაღაზიის შემოწმება (პარასკევი-კვირა)
today_weekday = datetime.now().weekday()  # 4 = პარასკევი, 5 = შაბათი, 6 = კვირა
is_reward_window_open = today_weekday in [4, 5, 6]

if is_reward_window_open:
    st.subheader(t("rewards_title"))
    # აქ დაემატება ჯილდოები
else:
    st.info(t("rewards_locked"))
