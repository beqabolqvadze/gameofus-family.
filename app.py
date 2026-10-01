import streamlit as st
import json
import os
from datetime import datetime

# ==========================================
# 1. ენების ლექსიკონი (TRANSLATIONS)
# ==========================================
TRANSLATIONS = {
    "ქართული": {
        "welcome": "კეთილი იყოს თქვენი მობრძანება GameOfUs-ში",
        "journal_title": "ემოციური დღიური და განწყობის აღრიცხვა",
        "select_mood": "როგორ გრძნობთ თავებს დღეს?",
        "mood_happy": "😊 ბედნიერი / მხიარული",
        "mood_calm": "😌 მშვიდი / დასვენებული",
        "mood_tired": "😴 დაღლილი",
        "mood_sad": "😢 მოწყენილი",
        "mood_energetic": "⚡ ენერგიული",
        "write_notes": "დაწერეთ თქვენი ფიქრები ან ჩანაწერები:",
        "save_button": "შენახვა (+10 XP)",
        "rewards_title": "ჯილდოების მაღაზია (პარასკევი–კვირა)",
        "rewards_locked": "🔒 ჯილდოების მაღაზია იხსნება მხოლოდ პარასკევიდან კვირის ჩათვლით!",
        "xp_points": "თქვენი XP ქულები",
        "select_language": "აირჩიეთ ენა",
        "settings": "პარამეტრები",
        "saved_success": "ჩანაწერი წარმატებით შენახულია! (+10 XP)",
        "history_title": "ჩანაწერების ისტორია"
    },
    "English": {
        "welcome": "Welcome to GameOfUs",
        "journal_title": "Emotional Journal & Mood Log",
        "select_mood": "How are you feeling today?",
        "mood_happy": "😊 Happy / Joyful",
        "mood_calm": "😌 Calm / Relaxed",
        "mood_tired": "😴 Tired",
        "mood_sad": "😢 Sad",
        "mood_energetic": "⚡ Energetic",
        "write_notes": "Write your thoughts or notes:",
        "save_button": "Save Entry (+10 XP)",
        "rewards_title": "Reward Store (Fri–Sun)",
        "rewards_locked": "🔒 Rewards are only available Friday through Sunday!",
        "xp_points": "Your Current XP",
        "select_language": "Choose Language",
        "settings": "Settings",
        "saved_success": "Saved successfully! (+10 XP)",
        "history_title": "Entry History"
    },
    "Русский": {
        "welcome": "Добро пожаловать в GameOfUs",
        "journal_title": "Дневник эмоций и настроения",
        "select_mood": "Как вы себя чувствуете сегодня?",
        "mood_happy": "😊 Счастливый / Веселый",
        "mood_calm": "😌 Спокойный / Расслабленный",
        "mood_tired": "😴 Уставший",
        "mood_sad": "😢 Грустный",
        "mood_energetic": "⚡ Энергичный",
        "write_notes": "Запишите свои мысли:",
        "save_button": "Сохранить (+10 XP)",
        "rewards_title": "Магазин наград (Пт–Вс)",
        "rewards_locked": "🔒 Награды доступны только с пятницы по воскресенье!",
        "xp_points": "Ваши очки XP",
        "select_language": "Выберите язык",
        "settings": "Настройки",
        "saved_success": "Успешно сохранено! (+10 XP)",
        "history_title": "История записей"
    },
    "Türkçe": {
        "welcome": "GameOfUs'a Hoş Geldiniz",
        "journal_title": "Duygu ve Mod Günlüğü",
        "select_mood": "Bugün nasıl hissediyorsunuz?",
        "mood_happy": "😊 Mutlu / Neşeli",
        "mood_calm": "😌 Sakin / Rahat",
        "mood_tired": "😴 Yorgun",
        "mood_sad": "😢 Üzgün",
        "mood_energetic": "⚡ Enerjik",
        "write_notes": "Düşüncelerinizi yazın:",
        "save_button": "Kaydet (+10 XP)",
        "rewards_title": "Ödül Mağazası (Cuma–Pazar)",
        "rewards_locked": "🔒 Ödüller yalnızca Cuma ve Pazar günleri arasında kullanılabilir!",
        "xp_points": "Mevcut XP Puanınız",
        "select_language": "Dil Seçin",
        "settings": "Ayarlar",
        "saved_success": "Başarıyla kaydedildi! (+10 XP)",
        "history_title": "Kayıt Geçmişi"
    },
    "中文": {
        "welcome": "欢迎来到 GameOfUs",
        "journal_title": "情绪与心情日志",
        "select_mood": "您今天感觉如何？",
        "mood_happy": "😊 开心 / 快乐",
        "mood_calm": "😌 平静 / 放松",
        "mood_tired": "😴 疲惫",
        "mood_sad": "😢 难过",
        "mood_energetic": "⚡ 精力充沛",
        "write_notes": "写下您的想法：",
        "save_button": "保存记录 (+10 XP)",
        "rewards_title": "奖励商店（周五至周日）",
        "rewards_locked": "🔒 奖励仅在周五至周日期间开放！",
        "xp_points": "当前的 XP 积分",
        "select_language": "选择语言",
        "settings": "设置",
        "saved_success": "保存成功！(+10 XP)",
        "history_title": "历史记录"
    },
    "日本語": {
        "welcome": "GameOfUs へようこそ",
        "journal_title": "感情・ mood ログ",
        "select_mood": "今日の気分はどうですか？",
        "mood_happy": "😊 幸せ / 楽しい",
        "mood_calm": "😌 穏やか / リラックス",
        "mood_tired": "😴 疲れている",
        "mood_sad": "😢 悲しい",
        "mood_energetic": "⚡ エネルギッシュ",
        "write_notes": "考えやメモを記入：",
        "save_button": "保存する (+10 XP)",
        "rewards_title": "ご褒美ストア（金〜日）",
        "rewards_locked": "🔒 ご褒美は金曜日から日曜日までのみ利用可能です！",
        "xp_points": "現在の XP ポイント",
        "select_language": "言語を選択",
        "settings": "設定",
        "saved_success": "正常に保存されました！(+10 XP)",
        "history_title": "履歴"
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
    return {"xp": 0, "language": "ქართული", "journal": []}

def save_user_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ==========================================
# 3. SESSION STATE & ენის ინიციალიზაცია
# ==========================================
user_data = load_user_data()

if "language" not in st.session_state:
    st.session_state["language"] = user_data.get("language", "ქართული")

def t(key):
    lang = st.session_state["language"]
    return TRANSLATIONS.get(lang, TRANSLATIONS["ქართული"]).get(key, key)

# ==========================================
# 4. SIDEBAR - ენის არჩევანი
# ==========================================
st.sidebar.title(f"⚙️ {t('settings')}")

language_options = ["ქართული", "English", "Русский", "Türkçe", "中文", "日本語"]
current_lang_idx = language_options.index(st.session_state["language"]) if st.session_state["language"] in language_options else 0

selected_lang = st.sidebar.selectbox(
    t("select_language"),
    options=language_options,
    index=current_lang_idx
)

if selected_lang != st.session_state["language"]:
    st.session_state["language"] = selected_lang
    user_data["language"] = selected_lang
    save_user_data(user_data)
    st.rerun()

# ==========================================
# 5. მთავარი ინტერფეისი
# ==========================================
st.title(t("welcome"))

# XP ქულების ჩვენება
st.metric(label=t("xp_points"), value=user_data.get("xp", 0))

st.divider()

# დღიურისა და განწყობის სექცია
st.header(t("journal_title"))

mood_options = [
    t("mood_happy"),
    t("mood_calm"),
    t("mood_tired"),
    t("mood_sad"),
    t("mood_energetic")
]
selected_mood = st.selectbox(t("select_mood"), mood_options)

entry_text = st.text_area(t("write_notes"), height=120)

if st.button(t("save_button")):
    if entry_text.strip() or selected_mood:
        new_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mood": selected_mood,
            "text": entry_text
        }
        user_data.setdefault("journal", []).append(new_entry)
        user_data["xp"] = user_data.get("xp", 0) + 10
        save_user_data(user_data)
        st.success(t("saved_success"))
        st.rerun()

st.divider()

# ისტორიის ჩვენება
if user_data.get("journal"):
    st.subheader(t("history_title"))
    for item in reversed(user_data["journal"]):
        with st.expander(f"📅 {item.get('timestamp')} | {item.get('mood')}"):
            st.write(item.get("text"))

st.divider()

# ჯილდოების მაღაზიის შემოწმება (პარასკევი-კვირა)
today_weekday = datetime.now().weekday()  # 4 = პარასკევი, 5 = შაბათი, 6 = კვირა
is_reward_window_open = today_weekday in [4, 5, 6]

if is_reward_window_open:
    st.subheader(t("rewards_title"))
    st.write("🎁 მაღაზია ღიაა!")
else:
    st.info(t("rewards_locked"))
