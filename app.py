import streamlit as st
import time
import json
import os
from datetime import datetime

# გვერდის კონფიგურაცია
st.set_page_config(
    page_title="GameOfUs: Family Edition",
    page_icon="⭐",
    layout="centered"
)

# ==========================================
# 🎨 თანამედროვე, სუფთა და თბილი CSS დიზაინი
# ==========================================
def inject_custom_css():
    st.markdown("""
    <style>
        .stApp {
            background-color: #FAF9F6;
            color: #2C3E50;
        }
        h1, h2, h3 {
            color: #1E293B !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }
        .game-card {
            background-color: #FFFFFF;
            padding: 1.25rem 1.5rem;
            border-radius: 16px;
            border: 1px solid #ECEAE4;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            margin-bottom: 1rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .game-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
        }
        .hero-stats {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
            border: 1px solid #FDE68A;
            border-radius: 18px;
            padding: 1rem;
            margin-bottom: 1.2rem;
            text-align: center;
        }
        .stat-item {
            display: flex;
            flex-direction: column;
        }
        .stat-val {
            font-size: 1.4rem;
            font-weight: 800;
            color: #B45309;
        }
        .stat-lbl {
            font-size: 0.85rem;
            color: #78350F;
            font-weight: 500;
        }
        .medallion-box {
            text-align: center;
            padding: 1.8rem 1.5rem;
            border-radius: 20px;
            margin: 1rem 0;
        }
        .medallion-front {
            background: linear-gradient(135deg, #FFFDF7 0%, #FEF3C7 100%);
            border: 2px solid #F59E0B;
            box-shadow: 0 8px 20px rgba(245, 158, 11, 0.12);
        }
        .medallion-back {
            background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
            border: 2px solid #10B981;
            box-shadow: 0 8px 20px rgba(16, 185, 129, 0.12);
        }
        .medallion-title {
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .medallion-text {
            font-size: 1rem;
            color: #374151;
            font-style: italic;
        }
        .stButton > button {
            border-radius: 12px !important;
            font-weight: 600 !important;
            border: 1px solid #E2E8F0 !important;
            padding: 0.45rem 1rem !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover {
            border-color: #CBD5E1 !important;
            background-color: #F8FAFC !important;
            transform: scale(1.01);
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #F1EFEA;
            padding: 6px;
            border-radius: 14px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 8px 16px;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: #FFFFFF !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        .chess-green {
            background-color: #F0FDF4;
            border-left: 5px solid #22C55E;
            padding: 1.2rem;
            border-radius: 12px;
            color: #14532D;
        }
        .chess-dark {
            background-color: #FFFBEB;
            border-left: 5px solid #F59E0B;
            padding: 1.2rem;
            border-radius: 12px;
            color: #78350F;
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ==========================================
# 1. ასაკობრივი მისიების მოდული
# ==========================================
class AgeBasedMissions:
    @staticmethod
    def get_missions_for_age(age, lang="ქართული"):
        if lang == "English":
            if 6 <= age <= 9:
                return [
                    {"id": "m1", "title": "🏃 Morning Exercise", "desc": "Do 5 minutes of morning stretching."},
                    {"id": "m2", "title": "💧 Drink Water", "desc": "Drink a full glass of water."},
                    {"id": "m3", "title": "📚 Read a Page", "desc": "Read at least one page of a book."}
                ]
            elif 10 <= age <= 13:
                return [
                    {"id": "m1", "title": "🏋️ Active Workout", "desc": "Complete a 15-minute workout session."},
                    {"id": "m2", "title": "🥗 Healthy Snack", "desc": "Eat a healthy meal or salad."},
                    {"id": "m3", "title": "🧘 Mindfulness", "desc": "Take 2 minutes of silent breathing."}
                ]
            else:
                return [
                    {"id": "m1", "title": "🎯 Daily Focus", "desc": "Define your main goal for the day."},
                    {"id": "m2", "title": "🚴 Physical Activity", "desc": "Cardio or gym session for 30+ minutes."},
                    {"id": "m3", "title": "🧠 Self-Reflection", "desc": "Observe your thoughts and write a short note."}
                ]
        elif lang == "Русский":
            if 6 <= age <= 9:
                return [
                    {"id": "m1", "title": "🏃 Утренняя зарядка", "desc": "Сделайте 5 минут разминки."},
                    {"id": "m2", "title": "💧 Выпить воды", "desc": "Выпейте стакан чистой воды."},
                    {"id": "m3", "title": "📚 Почитать книгу", "desc": "Прочитайте хотя бы одну страницу."}
                ]
            elif 10 <= age <= 13:
                return [
                    {"id": "m1", "title": "🏋️ Активная тренировка", "desc": "15 минут физических упражнений."},
                    {"id": "m2", "title": "🥗 Полезный перекус", "desc": "Съешьте что-то полезное."},
                    {"id": "m3", "title": "🧘 Осознанность", "desc": "2 минуты дыхательной паузы."}
                ]
            else:
                return [
                    {"id": "m1", "title": "🎯 Фокус дня", "desc": "Определите главную цель на день."},
                    {"id": "m2", "title": "🚴 Физическая активность", "desc": "Кардио или зал от 30 минут."},
                    {"id": "m3", "title": "🧠 Самоанализ", "desc": "Проследите за своими мыслями."}
                ]
        else:  # ქართული
            if 6 <= age <= 9:
                return [
                    {"id": "m1", "title": "🏃 დილის ვარჯიში", "desc": "გააკეთე 5 წუთიანი გაჭიმვა."},
                    {"id": "m2", "title": "💧 წყლის დალევა", "desc": "დალიე ერთი ჭიქა სუფთა წყალი."},
                    {"id": "m3", "title": "📚 წიგნის წაკითხვა", "desc": "წაიკითხე წიგნის ერთი გვერდი მაინც."}
                ]
            elif 10 <= age <= 13:
                return [
                    {"id": "m1", "title": "🏋️ აქტიური ვარჯიში", "desc": "შეასრულე 15 წუთიანი ფიზიკური აქტივობა."},
                    {"id": "m2", "title": "🥗 ჯანსაღი კვება", "desc": "მიირთვი ჯანსაღი საჭმელი ან სალათი."},
                    {"id": "m3", "title": "🧘 დამკვირვებლის პაუზა", "desc": "დაუთმე 2 წუთი სუნთქვას და სიმშვიდეს."}
                ]
            else:
                return [
                    {"id": "m1", "title": "🎯 დღის მთავარი მიზანი", "desc": "განსაზღვრე დღევანდელი პრიორიტეტი."},
                    {"id": "m2", "title": "🚴 ფიზიკური აქტივობა / სპორტი", "desc": "კარდიო ან ზალი (30+ წუთი)."},
                    {"id": "m3", "title": "🧠 შინაგანი დაკვირვება", "desc": "დააკვირდი შენს ფიქრებს და გააზრე მომენტი."}
                ]

# ==========================================
# 2. ენების ლექსიკონი
# ==========================================
TRANSLATIONS = {
    "ქართული": {
        "title": "⭐ GameOfUs: Family Edition",
        "subtitle": "თამაში ბავშვისთვის • მხარდაჭერა მშობლისთვის • ზრდა ორივესთვის",
        "profile": "👤 პროფილი",
        "enter_age": "შეიყვანე ასაკი:",
        "group_label": "📌 ჯგუფი:",
        "tab_child": "👦 გმირის სივრცე",
        "tab_parent": "👨‍👩‍👧 მენტორის პანელი",
        "tab_chess": "♟️ შინაგანი ჭადრაკი",
        "hello_hero": "გამარჯობა, გმირო! 👋",
        "stars_label": "ვარსკვლავები",
        "level_label": "დონე",
        "xp_label": "XP პროგრესი",
        "energy_label": "⚡ შენი ენერგია:",
        "energy_plus": "🔋 მომატება (+2)",
        "energy_minus": "🪫 დავიღალე (-2)",
        "mood_title": "💭 როგორ გრძნობ თავს დღეს?",
        "mood_happy": "😃 მხიარული",
        "mood_calm": "🧘 მშვიდი",
        "mood_tired": "😴 დაღლილი",
        "mood_sad": "😔 მოწყენილი",
        "mood_angry": "😡 გაბრაზებული",
        "mood_note_placeholder": "დაამატე პატარა ჩანაწერი შენს ემოციაზე (არასავალდებულო):",
        "save_mood": "💾 ემოციის შენახვა",
        "mood_saved": "ემოცია ჩაინიშნა და შეინახა თვის არქივში! 🌿",
        "urge_title": "🌊 Urge Surfing — იმპულსის ტალღა",
        "urge_button": "⏱️ ტალღის გადაგორება (10 წამიანი პაუზა)",
        "urge_spinner": "ტალღა გადადის... ისუნთქე ღრმად... 🌬️",
        "urge_success": "✅ ყოჩაღ! ტალღამ ჩაიარა!",
        "missions_title": "📋 დღევანდელი მისიები",
        "completed": "✅ შესრულებულია",
        "do_mission": "შესრულება",
        "rewards_title": "🎁 ჯილდოების მაღაზია",
        "rewards_locked_msg": "🔒 ჯილდოების განაღდება შესაძლებელია პარასკევიდან კვირის ჩათვლით! ახლა დააგროვე ვარსკვლავები. ✨",
        "claim_reward": "მიღება",
        "locked_button": "🔒 ჩაკეტილია",
        "reward_requested": "🎉 მოთხოვნა გაიგზავნა!",
        "no_stars": "არ გყოფნის ვარსკვლავები!",
        "pending_rewards": "⏳ შენი მომლოდინე ჯილდოები",
        "preparing_reward": "მენტორი/მშობელი ამზადებს ამ ჯილდოს!",
        "parent_panel": "👨‍👩‍👧 მშობლის / მენტორის პანელი",
        "level_up": "🎉 გადავიდა მე-{} დონეზე!",
        "bonus_stars": "⭐ ბონუს ვარსკვლავის გაჩუქება",
        "bonus_added": "+{} ⭐ დაემატა!",
        "requested_rewards_parent": "🎁 მოთხოვნილი ჯილდოები (შესასრულებელი)",
        "no_pending_rewards": "🎉 მომლოდინე ჯილდოები არ არის.",
        "mark_done": "✅ შესრულდა",
        "cant_do": "⚠️ ვერ ვასრულებ",
        "mood_history": "📜 ემოციების და პროგრესის სრული არქივი (თვის შეჯამება)",
        "no_moods": "ჯერ ჩანაწერები არ არის.",
        "add_mission": "➕ ახალი მისიის დამატება",
        "mission_title_input": "მისიის სათაური:",
        "mission_desc_input": "აღწერა:",
        "add_mission_btn": "➕ მისიის დამატება",
        "mission_added": "მისია დაემატა!",
        "reset_day": "🔄 დღის გადატვირთვა",
        "reset_success": "დღიური მისიები განახლდა!",
        "select_language": "🌐 აირჩიეთ ენა / Select Language",
        "settings": "⚙️ პარამეტრები",
        "username_label": "👤 მომხმარებლის სახელი:"
    },
    "English": {
        "title": "⭐ GameOfUs: Family Edition",
        "subtitle": "A game for kids • Support for parents • Growth for both",
        "profile": "👤 Profile",
        "enter_age": "Enter age:",
        "group_label": "📌 Group:",
        "tab_child": "👦 Hero Space",
        "tab_parent": "👨‍👩‍👧 Mentor Panel",
        "tab_chess": "♟️ Inner Chess",
        "hello_hero": "Hello, Hero! 👋",
        "stars_label": "Stars",
        "level_label": "Level",
        "xp_label": "XP Progress",
        "energy_label": "⚡ Your Energy:",
        "energy_plus": "🔋 Boost (+2)",
        "energy_minus": "🪫 Tired (-2)",
        "mood_title": "💭 How are you feeling today?",
        "mood_happy": "😃 Happy",
        "mood_calm": "🧘 Calm",
        "mood_tired": "😴 Tired",
        "mood_sad": "😔 Sad",
        "mood_angry": "😡 Angry",
        "mood_note_placeholder": "Add a quick note about your feelings (optional):",
        "save_mood": "💾 Save Mood",
        "mood_saved": "Mood saved to monthly archive! 🌿",
        "urge_title": "🌊 Urge Surfing — Ride the Wave",
        "urge_button": "⏱️ Ride the wave (10s pause)",
        "urge_spinner": "The wave is passing... breathe deeply... 🌬️",
        "urge_success": "✅ Great job! The wave passed!",
        "missions_title": "📋 Today's Missions",
        "completed": "✅ Completed",
        "do_mission": "Complete",
        "rewards_title": "🎁 Reward Store",
        "rewards_locked_msg": "🔒 Rewards can only be redeemed Friday through Sunday! Collect stars for now. ✨",
        "claim_reward": "Claim",
        "locked_button": "🔒 Locked",
        "reward_requested": "🎉 Request sent!",
        "no_stars": "Not enough stars!",
        "pending_rewards": "⏳ Your Pending Rewards",
        "preparing_reward": "Mentor/Parent is preparing this reward!",
        "parent_panel": "👨‍👩‍👧 Parent / Mentor Panel",
        "level_up": "🎉 Reached Level {}!",
        "bonus_stars": "⭐ Gift Bonus Stars",
        "bonus_added": "+{} ⭐ added!",
        "requested_rewards_parent": "🎁 Requested Rewards (To fulfill)",
        "no_pending_rewards": "🎉 No pending rewards.",
        "mark_done": "✅ Done",
        "cant_do": "⚠️ Can't fulfill",
        "mood_history": "📜 Complete Mood & Progress Archive",
        "no_moods": "No records yet.",
        "add_mission": "➕ Add New Mission",
        "mission_title_input": "Mission title:",
        "mission_desc_input": "Description:",
        "add_mission_btn": "➕ Add Mission",
        "mission_added": "Mission added!",
        "reset_day": "🔄 Reset Day",
        "reset_success": "Daily missions reset!",
        "select_language": "🌐 Select Language",
        "settings": "⚙️ Settings",
        "username_label": "👤 Username:"
    },
    "Русский": {
        "title": "⭐ GameOfUs: Family Edition",
        "subtitle": "Игра для ребенка • Поддержка для родителя • Рост для обоих",
        "profile": "👤 Профиль",
        "enter_age": "Введите возраст:",
        "group_label": "📌 Группа:",
        "tab_child": "👦 Пространство Героя",
        "tab_parent": "👨‍👩‍👧 Панель Ментора",
        "tab_chess": "♟️ Внутренний Шахмат",
        "hello_hero": "Привет, Герой! 👋",
        "stars_label": "Звезды",
        "level_label": "Уровень",
        "xp_label": "XP Прогресс",
        "energy_label": "⚡ Ваша энергия:",
        "energy_plus": "🔋 Пополнить (+2)",
        "energy_minus": "🪫 Я устал (-2)",
        "mood_title": "💭 Как вы себя чувствуете сегодня?",
        "mood_happy": "😃 Веселый",
        "mood_calm": "🧘 Спокойный",
        "mood_tired": "😴 Уставший",
        "mood_sad": "😔 Грустный",
        "mood_angry": "😡 Злой",
        "mood_note_placeholder": "Запишите свои мысли (необязательно):",
        "save_mood": "💾 Сохранить эмоцию",
        "mood_saved": "Запись сохранена в архив! 🌿",
        "urge_title": "🌊 Urge Surfing — Преодолей импульс",
        "urge_button": "⏱ Переждать волну (пауза 10 сек)",
        "urge_spinner": "Волна проходит... Дышите глубже... 🌬️",
        "urge_success": "✅ Отлично! Волна прошла!",
        "missions_title": "📋 Задания на сегодня",
        "completed": "✅ Выполнено",
        "do_mission": "Выполнить",
        "rewards_title": "🎁 Магазин Наград",
        "rewards_locked_msg": "🔒 Награды доступны только с пятницы по воскресенье! Собирайте звезды. ✨",
        "claim_reward": "Получить",
        "locked_button": "🔒 Заблокировано",
        "reward_requested": "🎉 Запрос отправлен!",
        "no_stars": "Не хватает звезд!",
        "pending_rewards": "⏳ Ожидающие награды",
        "preparing_reward": "Родитель готовит эту награду!",
        "parent_panel": "👨‍👩‍👧 Панель Родителя / Ментора",
        "level_up": "🎉 Переход на уровень {}!",
        "bonus_stars": "⭐ Подарить бонусные звезды",
        "bonus_added": "+{} ⭐ добавлено!",
        "requested_rewards_parent": "🎁 Запрошенные награды",
        "no_pending_rewards": "🎉 Нет ожидающих наград.",
        "mark_done": "✅ Выполнено",
        "cant_do": "⚠️ Не могу выполнить",
        "mood_history": "📜 Полный архив эмоций и прогресса",
        "no_moods": "Записей пока нет.",
        "add_mission": "➕ Добавить новое задание",
        "mission_title_input": "Название задания:",
        "mission_desc_input": "Описание:",
        "add_mission_btn": "➕ Добавить",
        "mission_added": "Задание добавлено!",
        "reset_day": "🔄 Сброс дня",
        "reset_success": "Дневные задания обновлены!",
        "select_language": "🌐 Выберите язык",
        "settings": "⚙️ Настройки",
        "username_label": "👤 Имя пользователя:"
    }
}

def t(key):
    lang = st.session_state.get("language", "ქართული")
    return TRANSLATIONS.get(lang, TRANSLATIONS["ქართული"]).get(key, key)

# ==========================================
# 3. 🪪 მომხმარებლის პროფილი (Sidebar)
# ==========================================
st.sidebar.header(f"⚙️ {t('settings')}")

language_list = ["ქართული", "English", "Русский"]
current_lang = st.session_state.get("language", "ქართული")
lang_index = language_list.index(current_lang) if current_lang in language_list else 0

selected_lang = st.sidebar.selectbox(
    t("select_language"),
    options=language_list,
    index=lang_index
)

if selected_lang != current_lang:
    st.session_state.language = selected_lang
    st.rerun()

st.sidebar.divider()
st.sidebar.header(t("profile"))

username = st.sidebar.text_input(t("username_label"), value="ბექა")
safe_username = "".join(c for c in username if c.isalnum() or c in (' ', '_')).rstrip() or "unknown_user"
DB_FILE = f"user_data_{safe_username}.json"

# ==========================================
# 4. 🔒 Session State ინიციალიზაცია
# ==========================================
defaults = {
    'language': "ქართული",
    'xp': 0,
    'level': 1,
    'stars': 0,
    'energy': 5,
    'age': 26,
    'completed_missions': set(),
    'requested_rewards': [],
    'parent_penalties': 0,
    'custom_missions': [],
    'mood_logs': [],
    'last_active_date': datetime.now().strftime("%Y-%m-%d"),
    'rewards': [
        {"title": "🚲 30 წუთი ველოსიპედით სეირნობა", "cost": 3},
        {"title": "🍦 საყვარელი ნაყინი", "cost": 5},
        {"title": "🎬 საღამოს ანიმაციური ფილმი", "cost": 7},
        {"title": "🎡 კვირას პარკში წასვლა", "cost": 10},
    ],
    'chess_history': [],
    'daily_history': [],
    'medallion_flips': 0,
    'selected_mood_temp': None
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==========================================
# 5. მონაცემების შენახვა/ჩატვირთვა
# ==========================================
def load_user_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for k in defaults:
                if k in data:
                    if k == 'completed_missions':
                        st.session_state[k] = set(data[k])
                    else:
                        st.session_state[k] = data[k]

def save_user_data():
    data = {
        "xp": st.session_state.xp,
        "level": st.session_state.level,
        "stars": st.session_state.stars,
        "energy": st.session_state.energy,
        "age": st.session_state.age,
        "language": st.session_state.language,
        "completed_missions": list(st.session_state.completed_missions),
        "requested_rewards": st.session_state.requested_rewards,
        "parent_penalties": st.session_state.parent_penalties,
        "custom_missions": st.session_state.custom_missions,
        "last_active_date": st.session_state.last_active_date,
        "mood_logs": st.session_state.mood_logs,
        "rewards": st.session_state.rewards,
        "chess_history": st.session_state.chess_history,
        "daily_history": st.session_state.daily_history,
        "medallion_flips": st.session_state.medallion_flips
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'current_user' not in st.session_state or st.session_state.current_user != safe_username:
    st.session_state.current_user = safe_username
    load_user_data()

today_str = datetime.now().strftime("%Y-%m-%d")

if st.session_state.last_active_date != today_str:
    summary_entry = f"📅 {st.session_state.last_active_date} | მისიები: {len(st.session_state.completed_missions)} | ⭐ {st.session_state.stars} | ✨ XP: {st.session_state.xp}"
    st.session_state.daily_history.append(summary_entry)
    st.session_state.completed_missions.clear()
    st.session_state.last_active_date = today_str
    save_user_data()

age = st.sidebar.number_input(t("enter_age"), min_value=6, max_value=99, value=int(st.session_state.age), step=1)
if age != st.session_state.age:
    st.session_state.age = age
    save_user_data()

if 6 <= age <= 9:
    age_group_name = "6-9 წელი (პატარა მკვლევარი)"
elif 10 <= age <= 13:
    age_group_name = "10-13 წელი (ახალგაზრდა გმირი)"
elif 14 <= age <= 17:
    age_group_name = "14-17 წელი (მოზარდი მეომარი)"
elif 18 <= age <= 25:
    age_group_name = "18-25 წელი (ახალგაზრდა ლიდერი)"
else:
    age_group_name = "26+ წელი (ბრძენი მენტორი)"

st.sidebar.info(f"{t('group_label')} **{age_group_name}**")

# ==========================================
# 6. 🪙 ცოცხალი მედალიონის კომპონენტი
# ==========================================
def render_medallion(unique_key):
    st.subheader("🪙 მადლიერების მედალიონი")
    is_front = st.session_state.medallion_flips % 2 == 0
    
    if is_front:
        st.markdown("""
        <div class="medallion-box medallion-front">
            <div class="medallion-title">🪙 მადლიერი ვარ</div>
            <div class="medallion-text">„მადლიერი ვარ ყველაფრისთვის, რაც მაქვს.“</div>
        </div>
        """, unsafe_allow_html=True)
        button_text = "🔄 მედალიონის გადატრიალება (+1 ⭐)"
    else:
        st.markdown("""
        <div class="medallion-box medallion-back">
            <div class="medallion-title">✨ მადლიერებისთვის</div>
            <div class="medallion-text">„მადლიერი ვარ იმისთვის, რომ შემიძლია ვიყო მადლიერი.“</div>
        </div>
        """, unsafe_allow_html=True)
        button_text = "🔄 უკან დაბრუნება (+1 ⭐)"

    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        if st.button(button_text, key=unique_key, use_container_width=True):
            st.session_state.medallion_flips += 1
            st.session_state.xp += 5
            st.session_state.stars += 1
            if st.session_state.xp >= 100:
                st.session_state.level += 1
                st.session_state.xp -= 100
            save_user_data()
            st.balloons()
            st.rerun()

# ==========================================
# 7. მთავარი ინტერფეისი
# ==========================================
st.title(t("title"))
st.caption(t("subtitle"))

tab1, tab2, tab3 = st.tabs([t("tab_child"), t("tab_parent"), t("tab_chess")])

# ---------------- TAB 1: გმირის სივრცე ----------------
with tab1:
    st.subheader(t("hello_hero"))
    
    st.markdown(f"""
    <div class="hero-stats">
        <div class="stat-item">
            <span class="stat-val">{st.session_state.stars} ⭐</span>
            <span class="stat-lbl">{t('stars_label')}</span>
        </div>
        <div class="stat-item">
            <span class="stat-val">Lvl {st.session_state.level}</span>
            <span class="stat-lbl">{t('level_label')}</span>
        </div>
        <div class="stat-item">
            <span class="stat-val">{st.session_state.xp} / 100</span>
            <span class="stat-lbl">{t('xp_label')}</span>
        </div>
        <div class="stat-item">
            <span class="stat-val">{st.session_state.energy}/10 ⚡</span>
            <span class="stat-lbl">ენერგია</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(st.session_state.xp / 100)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(t("energy_plus"), key=f"en_plus_{safe_username}", use_container_width=True):
            st.session_state.energy = min(10, st.session_state.energy + 2)
            save_user_data()
            st.rerun()
    with col2:
        if st.button(t("energy_minus"), key=f"en_minus_{safe_username}", use_container_width=True):
            st.session_state.energy = max(1, st.session_state.energy - 2)
            save_user_data()
            st.rerun()

    st.write("")
    render_medallion(f"med_child_{safe_username}")
    st.divider()

    st.subheader(t("mood_title"))
    col_e1, col_e2, col_e3, col_e4, col_e5 = st.columns(5)
    if col_e1.button("😃", key=f"m1_{safe_username}", use_container_width=True): st.session_state.selected_mood_temp = t("mood_happy")
    if col_e2.button("🧘", key=f"m2_{safe_username}", use_container_width=True): st.session_state.selected_mood_temp = t("mood_calm")
    if col_e3.button("😴", key=f"m3_{safe_username}", use_container_width=True): st.session_state.selected_mood_temp = t("mood_tired")
    if col_e4.button("😔", key=f"m4_{safe_username}", use_container_width=True): st.session_state.selected_mood_temp = t("mood_sad")
    if col_e5.button("😡", key=f"m5_{safe_username}", use_container_width=True): st.session_state.selected_mood_temp = t("mood_angry")

    if st.session_state.selected_mood_temp:
        st.caption(f"არჩეული განწყობა: **{st.session_state.selected_mood_temp}**")

    mood_note = st.text_input(t("mood_note_placeholder"), key=f"mood_note_{safe_username}")
    if st.button(t("save_mood"), key=f"save_mood_{safe_username}"):
        chosen = st.session_state.selected_mood_temp
        if chosen or mood_note:
            entry = f"{today_str} | {chosen if chosen else '📝'} {mood_note}"
            st.session_state.mood_logs.append(entry)
            st.session_state.selected_mood_temp = None
            save_user_data()
            st.success(t("mood_saved"))

    st.divider()

    st.subheader(t("urge_title"))
    if st.button(t("urge_button"), key=f"urge_btn_{safe_username}", use_container_width=True):
        with st.spinner(t("urge_spinner")):
            time.sleep(10)
        st.success(t("urge_success"))
        st.session_state.xp += 15
        st.session_state.stars += 1
        save_user_data()
        st.balloons()

    st.divider()

    st.subheader(f"{t('missions_title')} ({today_str})")
    current_missions = AgeBasedMissions.get_missions_for_age(st.session_state.age, lang=st.session_state.language) + st.session_state.custom_missions
    
    for m in current_missions:
        is_done = m['id'] in st.session_state.completed_missions
        st.markdown(f"""
        <div class="game-card" style="opacity: {'0.65' if is_done else '1'};">
            <div style="font-size: 1.05rem; font-weight: 700;">{m['title']}</div>
            <div style="font-size: 0.9rem; color: #64748B; margin-top: 4px;">{m['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if is_done:
            st.success(t("completed"))
        else:
            if st.button(f"{t('do_mission')} (+20 XP | +1 ⭐)", key=f"do_{m['id']}_{safe_username}"):
                st.session_state.completed_missions.add(m['id'])
                st.session_state.xp += 20
                st.session_state.stars += 1
                if st.session_state.xp >= 100:
                    st.session_state.level += 1
                    st.session_state.xp -= 100
                save_user_data()
                st.rerun()

    st.divider()

    st.subheader(t("rewards_title"))
    weekday = datetime.now().weekday()
    is_weekend_window = weekday in [4, 5, 6]
    if not is_weekend_window:
        st.info(t("rewards_locked_msg"))

    for idx, r in enumerate(st.session_state.rewards):
        st.markdown(f"""
        <div class="game-card" style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 600;">{r['title']}</span>
            <span style="background: #FEF3C7; color: #B45309; padding: 4px 10px; border-radius: 20px; font-weight: 700;">{r['cost']} ⭐</span>
        </div>
        """, unsafe_allow_html=True)
        if is_weekend_window:
            if st.button(t("claim_reward"), key=f"req_{idx}_{safe_username}"):
                if st.session_state.stars >= r['cost']:
                    st.session_state.stars -= r['cost']
                    st.session_state.requested_rewards.append(r['title'])
                    save_user_data()
                    st.success(t("reward_requested"))
                    st.rerun()
                else:
                    st.error(t("no_stars"))
        else:
            st.button(t("locked_button"), key=f"req_dis_{idx}_{safe_username}", disabled=True)

    if st.session_state.requested_rewards:
        st.subheader(t("pending_rewards"))
        for req_item in st.session_state.requested_rewards:
            st.warning(f"🎁 **{req_item}** — {t('preparing_reward')}")

# ---------------- TAB 2: მენტორის პანელი ----------------
with tab2:
    st.header(t("parent_panel"))
    col_p1, col_p2, col_p3 = st.columns(3)
    col_p1.metric(label=t("level_label"), value=st.session_state.level)
    col_p2.metric(label=t("xp_label"), value=f"{st.session_state.xp} / 100")
    col_p3.metric(label=t("stars_label"), value=st.session_state.stars)

    st.divider()
    render_medallion(f"med_parent_{safe_username}")
    st.divider()

    st.subheader(t("bonus_stars"))
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        if st.button("➕ 1 ⭐", key=f"b1_{safe_username}", use_container_width=True):
            st.session_state.stars += 1
            save_user_data()
            st.rerun()
    with col_b2:
        if st.button("➕ 3 ⭐", key=f"b3_{safe_username}", use_container_width=True):
            st.session_state.stars += 3
            save_user_data()
            st.rerun()
    with col_b3:
        if st.button("➕ 5 ⭐", key=f"b5_{safe_username}", use_container_width=True):
            st.session_state.stars += 5
            save_user_data()
            st.rerun()

    st.divider()

    st.subheader(t("requested_rewards_parent"))
    if not st.session_state.requested_rewards:
        st.write(t("no_pending_rewards"))
    else:
        for idx, req_title in enumerate(st.session_state.requested_rewards):
            col_req1, col_req2, col_req3 = st.columns([2, 1, 1])
            with col_req1:
                st.markdown(f"👉 **{req_title}**")
            with col_req2:
                if st.button(t("mark_done"), key=f"done_{idx}_{safe_username}"):
                    st.session_state.requested_rewards.pop(idx)
                    save_user_data()
                    st.rerun()
            with col_req3:
                if st.button(t("cant_do"), key=f"fail_{idx}_{safe_username}"):
                    st.session_state.requested_rewards.pop(idx)
                    st.session_state.stars += 2
                    st.session_state.parent_penalties += 1
                    save_user_data()
                    st.rerun()

    st.divider()

    # 📜 ემოციებისა და პროგრესის სრული არქივი (გვერდებად დაყოფით / შეჯამებით)
    st.subheader(t("mood_history"))
    
    all_moods = st.session_state.mood_logs
    if all_moods:
        st.markdown(f"📊 სულ შენახულია **{len(all_moods)}** ემოციის ჩანაწერი.")
        
        # გვერდებად დაყოფა (Pagination)
        items_per_page = 5
        total_pages = max(1, (len(all_moods) + items_per_page - 1) // items_per_page)
        
        page_num = st.slider("📄 აირჩიეთ არქივის გვერდი:", min_value=1, max_value=total_pages, value=1, key=f"mood_page_{safe_username}")
        
        start_idx = (page_num - 1) * items_per_page
        end_idx = start_idx + items_per_page
        current_page_items = list(reversed(all_moods))[start_idx:end_idx]
        
        st.markdown(f"*(გვერდი {page_num} / {total_pages})*")
        for log in current_page_items:
            st.markdown(f'<div class="game-card" style="padding: 0.7rem 1rem; margin-bottom: 0.5rem;">• {log}</div>', unsafe_allow_html=True)
    else:
        st.write(t("no_moods"))

    if st.session_state.daily_history:
        st.markdown("#### 🗓️ წარსული დღიური შეჯამებები:")
        for day_item in reversed(st.session_state.daily_history[-7:]):
            st.info(day_item)

    st.divider()

    # მისიების მართვა და წაშლა
    st.subheader("📋 მისიების მართვა (დამატება / წაშლა)")
    all_current_missions = AgeBasedMissions.get_missions_for_age(st.session_state.age, lang=st.session_state.language) + st.session_state.custom_missions
    
    for m in all_current_missions:
        col_m1, col_m2 = st.columns([3, 1])
        with col_m1:
            st.markdown(f"**{m['title']}** — *{m['desc']}*")
        with col_m2:
            if m['id'].startswith("custom_"):
                if st.button("🗑️ წაშლა", key=f"del_m_{m['id']}_{safe_username}"):
                    st.session_state.custom_missions = [cm for cm in st.session_state.custom_missions if cm['id'] != m['id']]
                    if m['id'] in st.session_state.completed_missions:
                        st.session_state.completed_missions.remove(m['id'])
                    save_user_data()
                    st.success("მისია წაიშალა!")
                    st.rerun()
            else:
                st.caption("საბაზისო მისია")

    st.write("")
    new_m_title = st.text_input(t("mission_title_input"), key=f"new_title_{safe_username}")
    new_m_desc = st.text_input(t("mission_desc_input"), key=f"new_desc_{safe_username}")
    if st.button(t("add_mission_btn"), key=f"add_btn_{safe_username}"):
        if new_m_title and new_m_desc:
            new_id = f"custom_{int(datetime.now().timestamp())}"
            st.session_state.custom_missions.append({"title": new_m_title, "desc": new_m_desc, "id": new_id})
            save_user_data()
            st.success(t("mission_added"))
            st.rerun()

    st.divider()

    if st.button(t("reset_day"), key=f"reset_btn_{safe_username}"):
        st.session_state.completed_missions.clear()
        save_user_data()
        st.success(t("reset_success"))
        st.rerun()

# ---------------- TAB 3: შინაგანი ჭადრაკი ----------------
with tab3:
    st.header("♟️ შინაგანი ჭადრაკი — დამკვირვებლის პოზიცია")
    st.caption("ნათელი დღეები • კრიზისული გამოწვევები • გააზრებული სვლები • სიმშვიდე")
    st.markdown("> *„თამაში არ მთავრდება გამარჯვებით ან დამარცხებით. თამაში მთავრდება მაშინ, როცა შენ ირჩევ პაუზას, სიმართლეს და შინაგან სიფხიზლეს.“*")
    st.divider()

    st.subheader("1. 🧭 აირჩიე შენი მიმდინარე სამყარო:")
    
    col_state1, col_state2 = st.columns(2)
    
    with col_state1:
        green_state = st.selectbox(
            "🌿 ნათელი დღეები",
            [
                "---",
                "✨ შინაგანი სიმშვიდე და სიცხადე",
                "⚡ მაღალი ენერგია და ენთუზიაზმი",
                "🌱 მადლიერების და კმაყოფილების განცდა",
                "🎯 ღრმა ფოკუსი და ნაკადის (Flow) მდგომარეობა",
                "🤝 კავშირი სხვებთან (სითბო, სიახლოვე)",
                "🌤️ მიღების განცდა (რაც არის, ისეა)",
                "💪 საკუთარი ძალის შეგრძნება",
                "🕊️ პატიების და გაშვების განცდა",
                "🧠 სიცხადე და გადაწყვეტილების მიღება",
                "💤 ღრმა დასვენება და აღდგენა"
            ],
            key=f"green_state_{safe_username}"
        )

    with col_state2:
        dark_state = st.selectbox(
            "🌑 რთული დღეები",
            [
                "---",
                "🔥 ძველი ჩვევის ძახილი / ცდუნება",
                "🏃 იმპულსური რეაქცია / მოუთმენლობა",
                "👥 სხვების სიამოვნება (People-pleasing)",
                "😮‍💨 დაღლილობა და ყურადღების გაფანტვა",
                "💭 მომავლის შფოთვა / უაზრო ფიქრები",
                "😡 ბრაზი და გაღიზიანება (არსაიდან)",
                "😔 სევდა და მარტოობის განცდა",
                "😨 შიში და გაურკვევლობა",
                "🪞 საკუთარი თავის კრიტიკა (შიგა ხმა)",
                "😶 სიცარიელე და აპათია (არაფერი მინდა)"
            ],
            key=f"dark_state_{safe_username}"
        )

    state_choice = None
    if green_state != "---":
        state_choice = f"🟢 {green_state}"
    elif dark_state != "---":
        state_choice = f"🌑 {dark_state}"

    st.divider()
    
    if state_choice:
        st.subheader("🛡️ შენი განმარტება:")
        
        if green_state != "---":
            messages_green = {
                "სიმშვიდე": "🧘 **სიმშვიდე:** ეს არის შენი დამსახურება. დაუთმე ამ წუთს 5 წამი. უბრალოდ ისუნთქე და იგრძენი, რომ ახლა ყველაფერი რიგზეა. ტვინმა იცის, რომ უსაფრთხოდ ხარ.",
                "ენერგია": "⚡ **ენერგია:** ეს არის ოქროს დრო. ენერგია უნდა დახარჯო საქმეზე, რომელიც გინდა. ტვინმა მიიღოს სიგნალი: 'ვმოქმედებ, ვარ ძლიერი'.",
                "მადლიერების": "🌱 **მადლიერება:** შეხედე ირგვლივ. მადლობა იმისთვის, რაც ახლა გაქვს. ეს არის ყველაზე ძლიერი ანტიდოტი შფოთვის წინააღმდეგ.",
                "ფოკუსი": "🎯 **ფოკუსი:** შენ ხარ ნაკადში. არაფერი არ გადაგიშალოს. ტვინმა იცის, რომ ეს მდგომარეობა ძვირფასია.",
                "კავშირი": "🤝 **კავშირი:** ეს არის ძალიან ღირებული. შენ ხარ სხვებთან და ეს გათბობს. დაუთმე დრო ამ ადამიანებს. ტვინმა იცის, რომ ის მარტო არ არის.",
                "მიღების": "🌤️ **მიღება:** შენ ახლა თანხმდები იმაზე, რაც არის. ეს არის სიმწიფე. ტვინმა იცის: 'მე ვიღებ რეალობას, როგორც არის'.",
                "ძალის": "💪 **ძალა:** შენ გრძნობ შენს ძალას. გამოიყენე ის სიკეთისთვის. ტვინმა იცის: 'მე ვარ ძლიერი და ღირსეული'.",
                "პატიების": "🕊️ **პატიება:** შენ ახლა ათავისუფლებ ტვირთს. ეს არის სიმსუბუქე. ტვინმა მიიღოს სიგნალი: 'მე ვათავისუფლებ, მე ვსუნთქავ'.",
                "სიცხადე": "🧠 **სიცხადე:** შენი გონება ნათელია. ახლა კარგი დროა გადაწყვეტილების მისაღებად. ტვინმა იცის: 'მე ვხედავ გზას'.",
                "დასვენება": "💤 **დასვენება:** ეს არის წამალი. ტვინმა მიიღოს სიგნალი: 'მე მაქვს უფლება დავისვენო და აღვიდგე'."
            }
            for key_word, text_val in messages_green.items():
                if key_word in green_state:
                    st.markdown(f'<div class="chess-green">{text_val}</div>', unsafe_allow_html=True)
                    break

        elif dark_state != "---":
            messages_dark = {
                "ცდუნება": "🔥 **ცდუნება:** ეს არის მხოლოდ ტალღა. ის მოვიდა და წავა. ნუ ებრძვი, უბრალოდ უყურე. ტვინმა იცის: 'მე არ ვარ ეს იმპულსი, მე ვარ დამკვირვებელი'.",
                "იმპულსური": "🏃 **იმპულსი:** გაჩერდი. სანამ რამეს იტყვი ან გააკეთებ, დაითვალე 10-მდე. ტვინმა მიიღოს სიგნალი: 'მე ვირჩევ პაუზას'.",
                "People-pleasing": "👥 **სხვების სიამოვნება:** ახლა შენი საზღვრები მნიშვნელოვანია. შენ არ ხარ ვალდებული ყველას ასიამოვნო. ტვინმა იცის: 'ჩემი მშვიდობა პირველ ადგილზეა'.",
                "დაღლილობა": "😮‍💨 **დაღლილობა:** ეს ნიშნავს, რომ დასვენება გჭირდება. ტვინმა მიიღოს სიგნალი: 'მე მაქვს უფლება დავისვენო'. დალიე წყალი, გაისეირნე ან უბრალოდ თვალები დახუჭე.",
                "შფოთვა": "💭 **შფოთვა:** ტვინი ცდილობს დაგიცვას იმისგან, რაც ჯერ არ მომხდარა. უთხარი მას: 'მე ვარ აქ, ახლა. ყველაფერი რიგზეა'. ისუნთქე ღრმად 3-ჯერ.",
                "ბრაზი": "😡 **ბრაზი:** ეს ენერგიაა. ნუ მიმართავ სხვისკენ. უთხარი: 'მე ვგრძნობ ბრაზს, მაგრამ მე არ ვარ ბრაზი'. გაისეირნე, ან დაარტყი ბალიშს.",
                "სევდა": "😔 **სევდა:** ნება მიეცი, რომ იყოს. ეს ნიშნავს, რომ რაღაც გენატრება ან გტკივა. არ გაურბიოდე. ტვინმა იცის: 'მე მაქვს უფლება ვიყო სევდიანი'.",
                "შიში": "😨 **შიში:** ტვინი გეუბნება, რომ რაღაც საშიშია. ჰკითხე: 'ეს არის რეალური საფრთხე თუ ილუზია?'. ტვინმა იცის: 'მე ვარ უსაფრთხოდ'.",
                "კრიტიკა": "🪞 **კრიტიკა:** ეს არის შენი შიგა ხმა, რომელიც გეუბნება, რომ არ ხარ საკმარისი. ეს ტყუილია. ტვინმა იცის: 'მე ვარ საკმარისი, როგორც ვარ'.",
                "სიცარიელე": "😶 **სიცარიელე:** ეს არ არის ცუდი. ეს არის სივრცე. ნება მიეცი, რომ იყოს. ტვინმა იცის: 'სიცარიელე ნიშნავს, რომ მე არ ვარ დაკავებული ცუდი აზრებით'."
            }
            for key_word, text_val in messages_dark.items():
                if key_word in dark_state:
                    st.markdown(f'<div class="chess-dark">{text_val}</div>', unsafe_allow_html=True)
                    break

        st.write("")
        if st.button("✅ ამის გაცნობიერება (+10 XP)", key=f"ack_{safe_username}", use_container_width=True):
            log_text = f"{today_str} | ♟️ {state_choice} ➔ 🛡️ *გაცნობიერებულია*"
            st.session_state.chess_history.append(log_text)
            st.session_state.xp += 10
            st.session_state.stars += 1
            if st.session_state.xp >= 100:
                st.session_state.level += 1
                st.session_state.xp -= 100
            save_user_data()
            st.balloons()
            st.rerun()
    else:
        st.info("აირჩიე მდგომარეობა ზემოთ, რომ ნახო განმარტება.")

    st.divider()
    st.subheader("📜 შინაგანი ბრძოლების & ნათელი დღეების ისტორია")
    if st.session_state.chess_history:
        for history_item in reversed(st.session_state.chess_history[-6:]):
            st.markdown(f'<div class="game-card" style="padding: 0.8rem 1.2rem;">{history_item}</div>', unsafe_allow_html=True)
    else:
        st.write("ჯერ სვლები არ გაგიკეთებია.")
