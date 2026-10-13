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

DB_FILE = "user_data.json"

# ==========================================
# 1. ასაკობრივი მისიების მოდული (ჩაშენებული)
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
        else: # ქართული (Default)
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
# 2. ენების ლექსიკონი (TRANSLATIONS)
# ==========================================
TRANSLATIONS = {
    "ქართული": {
        "title": "⭐ GameOfUs: Family Edition",
        "subtitle": "თამაში ბავშვისთვის • მხარდაჭერა მშობლისთვის • ზრდა ორივესთვის",
        "profile": "👤 პროფილი",
        "enter_age": "შეიყვანე ასაკი:",
        "group_label": "📌 ჯგუფი:",
        "tab_child": "👦 ბავშვის / გმირის სივრცე",
        "tab_parent": "👨‍👩‍👧 მშობლის / მენტორის პანელი",
        "tab_chess": "♟️ შინაგანი ჭადრაკი (დამკვირვებელი)",
        "hello_hero": "გამარჯობა, გმირო! 👋",
        "stars_label": "⭐ შენი ვარსკვლავები:",
        "level_label": "🏆 დონე:",
        "xp_label": "✨ XP:",
        "energy_label": "⚡ შენი ენერგია:",
        "energy_plus": "🔋 ენერგიის მომატება (+2)",
        "energy_minus": "🪫 დავიღალე (-2)",
        "mood_title": "💭 როგორ გრძნობ თავს დღეს?",
        "mood_happy": "😃 მხიარული",
        "mood_calm": "🧘 მშვიდი",
        "mood_tired": "😴 დაღლილი",
        "mood_sad": "😔 მოწყენილი",
        "mood_angry": "😡 გაბრაზებული",
        "mood_note_placeholder": "დაამატე პატარა ჩანაწერი შენს ემოციაზე (არასავალდებულო):",
        "save_mood": "💾 ემოციის შენახვა",
        "mood_saved": "ემოცია ჩაინიშნა! 🌿",
        "urge_title": "🌊 Urge Surfing — იმპულსის ტალღა",
        "urge_button": "⏱️ ტალღის გადაგორება (10 წამიანი პაუზა)",
        "urge_spinner": "ტალღა გადადის... ისუნთქე ღრმად... 🌬️",
        "urge_success": "✅ ყოჩაღ! ტალღამ ჩაიარა!",
        "missions_title": "📋 დღევანდელი მისიები",
        "completed": "✅ შესრულებულია",
        "do_mission": "შესრულება",
        "rewards_title": "🎁 ჯილდოების მაღაზია",
        "rewards_locked_msg": "🔒 **ჯილდოების განაღდება შესაძლებელია პარასკევიდან კვირის ჩათვლით!** ახლა დააგროვე ვარსკვლავები. ✨",
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
        "mood_history": "📜 ემოციების ისტორია",
        "no_moods": "ჯერ ემოციების ჩანაწერი არ არის.",
        "add_mission": "➕ ახალი მისიის დამატება",
        "mission_title_input": "მისიის სათაური:",
        "mission_desc_input": "აღწერა:",
        "add_mission_btn": "➕ მისიის დამატება",
        "mission_added": "მისია დაემატა!",
        "reset_day": "🔄 დღის გადატვირთვა",
        "reset_success": "დღიური მისიები განახლდა!",
        "select_language": "🌐 აირჩიეთ ენა / Select Language",
        "settings": "⚙️ პარამეტრები"
    },
    "English": {
        "title": "⭐ GameOfUs: Family Edition",
        "subtitle": "A game for kids • Support for parents • Growth for both",
        "profile": "👤 Profile",
        "enter_age": "Enter age:",
        "group_label": "📌 Group:",
        "tab_child": "👦 Child / Hero Space",
        "tab_parent": "👨‍👩‍👧 Parent / Mentor Panel",
        "tab_chess": "♟️ Inner Chess (Observer)",
        "hello_hero": "Hello, Hero! 👋",
        "stars_label": "⭐ Your Stars:",
        "level_label": "🏆 Level:",
        "xp_label": "✨ XP:",
        "energy_label": "⚡ Your Energy:",
        "energy_plus": "🔋 Energy Boost (+2)",
        "energy_minus": "🪫 I'm Tired (-2)",
        "mood_title": "💭 How are you feeling today?",
        "mood_happy": "😃 Happy",
        "mood_calm": "🧘 Calm",
        "mood_tired": "😴 Tired",
        "mood_sad": "😔 Sad",
        "mood_angry": "😡 Angry",
        "mood_note_placeholder": "Add a quick note about your feelings (optional):",
        "save_mood": "💾 Save Mood",
        "mood_saved": "Mood saved! 🌿",
        "urge_title": "🌊 Urge Surfing — Ride the Wave",
        "urge_button": "⏱️ Ride the wave (10s pause)",
        "urge_spinner": "The wave is passing... breathe deeply... 🌬️",
        "urge_success": "✅ Great job! The wave passed!",
        "missions_title": "📋 Today's Missions",
        "completed": "✅ Completed",
        "do_mission": "Complete",
        "rewards_title": "🎁 Reward Store",
        "rewards_locked_msg": "🔒 **Rewards can only be redeemed Friday through Sunday!** Collect stars for now. ✨",
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
        "mood_history": "📜 Mood History",
        "no_moods": "No mood records yet.",
        "add_mission": "➕ Add New Mission",
        "mission_title_input": "Mission title:",
        "mission_desc_input": "Description:",
        "add_mission_btn": "➕ Add Mission",
        "mission_added": "Mission added!",
        "reset_day": "🔄 Reset Day",
        "reset_success": "Daily missions reset!",
        "select_language": "🌐 Select Language",
        "settings": "⚙️ Settings"
    },
    "Русский": {
        "title": "⭐ GameOfUs: Family Edition",
        "subtitle": "Игра для ребенка • Поддержка для родителя • Рост для обоих",
        "profile": "👤 Профиль",
        "enter_age": "Введите возраст:",
        "group_label": "📌 Группа:",
        "tab_child": "👦 Пространство Героя",
        "tab_parent": "👨‍👩‍👧 Панель Родителя",
        "tab_chess": "♟️ Внутренний Шахмат (Наблюдатель)",
        "hello_hero": "Привет, Герой! 👋",
        "stars_label": "⭐ Ваши звезды:",
        "level_label": "🏆 Уровень:",
        "xp_label": "✨ XP:",
        "energy_label": "⚡ Ваша энергия:",
        "energy_plus": "🔋 Пополнить энергию (+2)",
        "energy_minus": "🪫 Я устал (-2)",
        "mood_title": "💭 Как вы себя чувствуете сегодня?",
        "mood_happy": "😃 Веселый",
        "mood_calm": "🧘 Спокойный",
        "mood_tired": "😴 Уставший",
        "mood_sad": "😔 Грустный",
        "mood_angry": "😡 Злой",
        "mood_note_placeholder": "Запишите свои мысли (необязательно):",
        "save_mood": "💾 Сохранить эмоцию",
        "mood_saved": "Запись сохранена! 🌿",
        "urge_title": "🌊 Urge Surfing — Преодолей импульс",
        "urge_button": "⏱ Переждать волну (пауза 10 сек)",
        "urge_spinner": "Волна проходит... Дышите глубже... 🌬️",
        "urge_success": "✅ Отлично! Волна прошла!",
        "missions_title": "📋 Задания на сегодня",
        "completed": "✅ Выполнено",
        "do_mission": "Выполнить",
        "rewards_title": "🎁 Магазин Наград",
        "rewards_locked_msg": "🔒 **Награды доступны только с пятницы по воскресенье!** Собирайте звезды. ✨",
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
        "mood_history": "📜 История настроения",
        "no_moods": "Записей пока нет.",
        "add_mission": "➕ Добавить новое задание",
        "mission_title_input": "Название задания:",
        "mission_desc_input": "Описание:",
        "add_mission_btn": "➕ Добавить",
        "mission_added": "Задание добавлено!",
        "reset_day": "🔄 Сброс дня",
        "reset_success": "Дневные задания обновлены!",
        "select_language": "🌐 Выберите язык",
        "settings": "⚙️ Настройки"
    }
}

# მონაცემების ჩატვირთვა
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# მონაცემების შენახვა
def save_data():
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
        "chess_history": st.session_state.get("chess_history", [])
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

saved_data = load_data()
today_str = datetime.now().strftime("%Y-%m-%d")

# სესიის ინიციალიზაცია
if 'language' not in st.session_state:
    st.session_state.language = saved_data.get("language", "ქართული")
if 'xp' not in st.session_state:
    st.session_state.xp = saved_data.get("xp", 0)
if 'level' not in st.session_state:
    st.session_state.level = saved_data.get("level", 1)
if 'stars' not in st.session_state:
    st.session_state.stars = saved_data.get("stars", 0)
if 'energy' not in st.session_state:
    st.session_state.energy = saved_data.get("energy", 5)
if 'age' not in st.session_state:
    st.session_state.age = saved_data.get("age", 26)
if 'completed_missions' not in st.session_state:
    st.session_state.completed_missions = set(saved_data.get("completed_missions", []))
if 'requested_rewards' not in st.session_state:
    st.session_state.requested_rewards = saved_data.get("requested_rewards", [])
if 'parent_penalties' not in st.session_state:
    st.session_state.parent_penalties = saved_data.get("parent_penalties", 0)
if 'custom_missions' not in st.session_state:
    st.session_state.custom_missions = saved_data.get("custom_missions", [])
if 'mood_logs' not in st.session_state:
    st.session_state.mood_logs = saved_data.get("mood_logs", [])
if 'last_active_date' not in st.session_state:
    st.session_state.last_active_date = saved_data.get("last_active_date", today_str)
if 'rewards' not in st.session_state:
    st.session_state.rewards = saved_data.get("rewards", [
        {"title": "🚲 30 წუთი ველოსიპედით სეირნობა", "cost": 3},
        {"title": "🍦 საყვარელი ნაყინი", "cost": 5},
        {"title": "🎬 საღამოს ანიმაციური ფილმი", "cost": 7},
        {"title": "🎡 კვირას პარკში წასვლა", "cost": 10},
    ])
if 'chess_history' not in st.session_state:
    st.session_state.chess_history = saved_data.get("chess_history", [])

# თარგმნის დამხმარე ფუნქცია
def t(key):
    lang = st.session_state.language
    return TRANSLATIONS.get(lang, TRANSLATIONS["ქართული"]).get(key, key)

# 🗓️ ავტომატური დღის გადატვირთვა
if st.session_state.last_active_date != today_str:
    st.session_state.completed_missions.clear()
    st.session_state.last_active_date = today_str
    save_data()

# 👤 გვერდითა მენიუ (SIDEBAR)
st.sidebar.header(f"⚙️ {t('settings')}")

language_list = ["ქართული", "English", "Русский"]
lang_index = language_list.index(st.session_state.language) if st.session_state.language in language_list else 0

selected_lang = st.sidebar.selectbox(
    t("select_language"),
    options=language_list,
    index=lang_index
)

if selected_lang != st.session_state.language:
    st.session_state.language = selected_lang
    save_data()
    st.rerun()

st.sidebar.divider()
st.sidebar.header(t("profile"))
age = st.sidebar.number_input(t("enter_age"), min_value=6, max_value=99, value=int(st.session_state.age), step=1)

if age != st.session_state.age:
    st.session_state.age = age
    save_data()

if 6 <= age <= 9:
    age_group_name = "6-9 წელი (პატარა მკვლევარი)"
elif 10 <= age <= 13:
    age_group_name = "10-13 წელი (ახალგაზრდა გმირი)"
elif 13 <= age <= 17:
    age_group_name = "13-17 წელი (მოზარდი მეომარი)"
elif 18 <= age <= 25:
    age_group_name = "18-25 წელი (ახალგაზრდა ლიდერი)"
else:
    age_group_name = "26+ წელი (ბრძენი მენტორი)"

st.sidebar.success(f"{t('group_label')} {age_group_name}")

# ==========================================
# მთავარი ინტერფეისი
# ==========================================
st.title(t("title"))
st.caption(t("subtitle"))

tab1, tab2, tab3 = st.tabs([t("tab_child"), t("tab_parent"), t("tab_chess")])

with tab1:
    st.header(t("hello_hero"))
    st.info(f"{t('stars_label')} **{st.session_state.stars} ⭐** | {t('level_label')} **{st.session_state.level}** | {t('xp_label')} **{st.session_state.xp}/100**")
    
    st.subheader(f"{t('energy_label')} {st.session_state.energy}/10")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t("energy_plus")):
            st.session_state.energy = min(10, st.session_state.energy + 2)
            save_data()
            st.rerun()
    with col2:
        if st.button(t("energy_minus")):
            st.session_state.energy = max(1, st.session_state.energy - 2)
            save_data()
            st.rerun()

    st.divider()

    # 📝 ემოციების დღიური
    st.subheader(t("mood_title"))
    col_e1, col_e2, col_e3, col_e4, col_e5 = st.columns(5)
    selected_mood = None
    if col_e1.button("😃"): selected_mood = t("mood_happy")
    if col_e2.button("🧘"): selected_mood = t("mood_calm")
    if col_e3.button("😴"): selected_mood = t("mood_tired")
    if col_e4.button("😔"): selected_mood = t("mood_sad")
    if col_e5.button("😡"): selected_mood = t("mood_angry")

    mood_note = st.text_input(t("mood_note_placeholder"), key="mood_input")
    if st.button(t("save_mood")):
        if selected_mood or mood_note:
            entry = f"{today_str} | {selected_mood if selected_mood else '📝'} {mood_note}"
            st.session_state.mood_logs.append(entry)
            save_data()
            st.success(t("mood_saved"))

    st.divider()

    # 🌊 Urge Surfing
    st.subheader(t("urge_title"))
    if st.button(t("urge_button")):
        with st.spinner(t("urge_spinner")):
            time.sleep(10)
        st.success(t("urge_success"))
        st.session_state.xp += 15
        st.session_state.stars += 1
        save_data()
        st.balloons()

    st.divider()

    # 📋 მისიები
    st.subheader(f"{t('missions_title')} ({age_group_name})")
    current_missions = AgeBasedMissions.get_missions_for_age(st.session_state.age, lang=st.session_state.language) + st.session_state.custom_missions
    
    for m in current_missions:
        col_m1, col_m2 = st.columns([3, 1])
        with col_m1:
            st.markdown(f"**{m['title']}**\n\n*{m['desc']}*")
        with col_m2:
            if m['id'] in st.session_state.completed_missions:
                st.success(t("completed"))
            else:
                if st.button(t("do_mission"), key=m['id']):
                    st.session_state.completed_missions.add(m['id'])
                    st.session_state.xp += 20
                    st.session_state.stars += 1
                    save_data()
                    st.rerun()

    st.divider()

    # 🎁 ჯილდოების მაღაზია
    st.subheader(t("rewards_title"))
    weekday = datetime.now().weekday()
    is_weekend_window = weekday in [4, 5, 6]

    if not is_weekend_window:
        st.info(t("rewards_locked_msg"))

    for idx, r in enumerate(st.session_state.rewards):
        col_r1, col_r2 = st.columns([3, 1])
        with col_r1:
            st.markdown(f"**{r['title']}** — `{r['cost']} ⭐`")
        with col_r2:
            if is_weekend_window:
                if st.button(t("claim_reward"), key=f"req_{idx}"):
                    if st.session_state.stars >= r['cost']:
                        st.session_state.stars -= r['cost']
                        st.session_state.requested_rewards.append(r['title'])
                        save_data()
                        st.success(t("reward_requested"))
                        st.rerun()
                    else:
                        st.error(t("no_stars"))
            else:
                st.button(t("locked_button"), key=f"req_dis_{idx}", disabled=True)

    if st.session_state.requested_rewards:
        st.subheader(t("pending_rewards"))
        for req_item in st.session_state.requested_rewards:
            st.warning(f"🎁 **{req_item}** — {t('preparing_reward')}")

with tab2:
    st.header(t("parent_panel"))

    col_p1, col_p2, col_p3 = st.columns(3)
    col_p1.metric(label=t("level_label"), value=st.session_state.level)
    col_p2.metric(label=t("xp_label"), value=f"{st.session_state.xp} / 100")
    col_p3.metric(label=t("stars_label"), value=st.session_state.stars)

    if st.session_state.xp >= 100:
        st.session_state.level += 1
        st.session_state.xp -= 100
        save_data()
        st.success(t("level_up").format(st.session_state.level))

    st.divider()

    # ⭐ ბონუს ვარსკვლავები
    st.subheader(t("bonus_stars"))
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        if st.button("➕ 1 ⭐"):
            st.session_state.stars += 1
            save_data()
            st.success(t("bonus_added").format(1))
            st.rerun()
    with col_b2:
        if st.button("➕ 3 ⭐"):
            st.session_state.stars += 3
            save_data()
            st.success(t("bonus_added").format(3))
            st.rerun()
    with col_b3:
        if st.button("➕ 5 ⭐"):
            st.session_state.stars += 5
            save_data()
            st.success(t("bonus_added").format(5))
            st.rerun()

    st.divider()

    # 🎁 მოთხოვნილი ჯილდოები
    st.subheader(t("requested_rewards_parent"))
    if not st.session_state.requested_rewards:
        st.write(t("no_pending_rewards"))
    else:
        for idx, req_title in enumerate(st.session_state.requested_rewards):
            col_req1, col_req2, col_req3 = st.columns([2, 1, 1])
            with col_req1:
                st.markdown(f"👉 **{req_title}**")
            with col_req2:
                if st.button(t("mark_done"), key=f"done_{idx}"):
                    st.session_state.requested_rewards.pop(idx)
                    save_data()
                    st.rerun()
            with col_req3:
                if st.button(t("cant_do"), key=f"fail_{idx}"):
                    st.session_state.requested_rewards.pop(idx)
                    st.session_state.stars += 2
                    st.session_state.parent_penalties += 1
                    save_data()
                    st.rerun()

    st.divider()

    # 📜 ემოციების ისტორია
    st.subheader(t("mood_history"))
    if st.session_state.mood_logs:
        for log in reversed(st.session_state.mood_logs[-5:]):
            st.write(f"• {log}")
    else:
        st.write(t("no_moods"))

    st.divider()

    # ➕ ახალი მისიის დამატება
    st.subheader(t("add_mission"))
    new_m_title = st.text_input(t("mission_title_input"))
    new_m_desc = st.text_input(t("mission_desc_input"))
    if st.button(t("add_mission_btn")):
        if new_m_title and new_m_desc:
            new_id = f"custom_{len(st.session_state.custom_missions) + 1}"
            st.session_state.custom_missions.append({"title": new_m_title, "desc": new_m_desc, "id": new_id})
            save_data()
            st.success(t("mission_added"))
            st.rerun()

    st.divider()

    # 🔄 დღის გადატვირთვა
    if st.button(t("reset_day")):
        st.session_state.completed_missions.clear()
        save_data()
        st.success(t("reset_success"))
        st.rerun()

with tab3:
    st.header("♟️ შინაგანი ჭადრაკი — დამკვირვებლის პოზიცია")
    st.caption("რეალური გამოწვევები • გააზრებული სვლები • სიმშვიდის შენარჩუნება")

    st.markdown("""
    > *„თამაში არ მთავრდება გამარჯვებით ან დამარცხებით. თამაში მთავრდება მაშინ, როცა შენ ირჩევ პაუზას, სიმართლეს და შინაგან სიფხიზლეს.“*
    """)
    st.divider()

    st.subheader("1. 🌑 აირჩიე წინაღობა / გამოწვევა:")
    obstacle = st.selectbox(
        "რა გამოწვევას აწყდები დღეს?",
        [
            "🔥 ძველი ჩვევის ძახილი / ცდუნება",
            "🏃 იმპულსური რეაქცია / მოუთმენლობა",
            "👥 სხვების სიამოვნება (People-pleasing)",
            "😮‍💨 დაღლილობა და ყურადღების გაფანტვა",
            "💭 მომავლის შფოთვა / უაზრო ფიქრები"
        ]
    )

    st.divider()

    st.subheader("2. 🛡️ აირჩიე შენი პასუხი (დამკვირვებლის სვლა):")
    
    col_ch1, col_ch2, col_ch3 = st.columns(3)
    
    selected_move = None
    move_desc = ""

    with col_ch1:
        if st.button("🌊 Urge Surfing"):
            selected_move = "Urge Surfing (ტალღაზე სერფინგი)"
            move_desc = "არ ვებრძვი ტალღას, უბრალოდ ვაკვირდები, როგორ ჩაივლის 10 წამში."
        if st.button("⏱️ 2-წუთიანი წესი"):
            selected_move = "2-წუთიანი წესი"
            move_desc = "ვიწყებ პატარა ნაბიჯით 2 წუთით და ვაჩერებ შინაგან წინააღმდეგობას."

    with col_ch2:
        if st.button("🤫 დუმილი & პაუზა"):
            selected_move = "დუმილი & პაუზა"
            move_desc = "არ ვპასუხობ რეაქტიულად. ვაკეთებ ღრმა ჩასუნთქვას."
        if st.button("👑 საკუთარი თავის პრიორიტეტი"):
            selected_move = "საკუთარი თავის პრიორიტეტი"
            move_desc = "უარს ვამბობ სხვების სიამოვნებაზე, ჩემი შინაგანი მშვიდობის სასარგებლოდ."

    with col_ch3:
        if st.button("👁️ დამკვირვებლის თვალი"):
            selected_move = "დამკვირვებლის პოზიცია"
            move_desc = "მე არ ვარ ჩემი ფიქრი, მე ვარ ის, ვინც ამ ფიქრს აკვირდება."
        if st.button("🌟 ჭეშმარიტება"):
            selected_move = "ჭეშმარიტება & ყოფნა"
            move_desc = "ვიღებ მომენტს ისეთს, როგორიც არის, ბრძოლის გარეშე."

    if selected_move:
        log_text = f"{today_str} | 🌑 {obstacle} ➔ 🛡️ **{selected_move}**: *{move_desc}*"
        st.session_state.chess_history.append(log_text)
        st.session_state.xp += 10
        st.session_state.stars += 1
        save_data()
        st.success(f"🎯 სვლა გაკეთებულია! +10 XP | +1 ⭐\n\n**{selected_move}**: {move_desc}")
        st.balloons()

    st.divider()

    st.subheader("📜 შინაგანი ბრძოლების & გაძლების დღიური")
    if st.session_state.chess_history:
        for history_item in reversed(st.session_state.chess_history[-6:]):
            st.info(f"• {history_item}")
    else:
        st.write("ჯერ სვლები არ გაგიკეთებია. აირჩიე წინაღობა და გააკეთე პირველი სვლა!")
