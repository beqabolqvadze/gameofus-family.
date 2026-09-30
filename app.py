import streamlit as st
import time
import json
import os
from datetime import datetime
from age_missions import AgeBasedMissions

# გვერდის კონფიგურაცია
st.set_page_config(
    page_title="GameOfUs: Family Edition",
    page_icon="⭐",
    layout="centered"
)

DB_FILE = "user_data.json"

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
        "completed_missions": list(st.session_state.completed_missions),
        "requested_rewards": st.session_state.requested_rewards,
        "parent_penalties": st.session_state.parent_penalties,
        "custom_missions": st.session_state.custom_missions,
        "last_active_date": st.session_state.last_active_date,
        "mood_logs": st.session_state.mood_logs,
        "rewards": st.session_state.rewards
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

saved_data = load_data()
today_str = datetime.now().strftime("%Y-%m-%d")

# სესიის ინიციალიზაცია
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

# 🗓️ ავტომატური დღის გადატვირთვა
if st.session_state.last_active_date != today_str:
    st.session_state.completed_missions.clear()
    st.session_state.last_active_date = today_str
    save_data()

# 👤 გვერდითა მენიუ
st.sidebar.header("👤 პროფილი")
age = st.sidebar.number_input("შეიყვანე ასაკი:", min_value=6, max_value=99, value=int(st.session_state.age), step=1)

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

st.sidebar.success(f"📌 ჯგუფი: {age_group_name}")

st.title("⭐ GameOfUs: Family Edition")
st.caption("თამაში ბავშვისთვის • მხარდაჭერა მშობლისთვის • ზრდა ორივესთვის")

tab1, tab2 = st.tabs(["👦 ბავშვის / გმირის სივრცე", "👨‍👩‍👧 მშობლის / მენტორის პანელი"])

with tab1:
    st.header("გამარჯობა, გმირო! 👋")
    st.info(f"⭐ შენი ვარსკვლავები: **{st.session_state.stars} ⭐** | 🏆 დონე: **{st.session_state.level}** | ✨ XP: **{st.session_state.xp}/100**")
    
    st.subheader(f"⚡ შენი ენერგია: {st.session_state.energy}/10")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔋 ენერგიის მომატება (+2)"):
            st.session_state.energy = min(10, st.session_state.energy + 2)
            save_data()
            st.rerun()
    with col2:
        if st.button("🪫 დავიღალე (-2)"):
            st.session_state.energy = max(1, st.session_state.energy - 2)
            save_data()
            st.rerun()

    st.divider()

    # 📝 ემოციების დღიური
    st.subheader("💭 როგორ გრძნობ თავს დღეს?")
    col_e1, col_e2, col_e3, col_e4, col_e5 = st.columns(5)
    selected_mood = None
    if col_e1.button("😃"): selected_mood = "😃 მხიარული"
    if col_e2.button("🧘"): selected_mood = "🧘 მშვიდი"
    if col_e3.button("😴"): selected_mood = "😴 დაღლილი"
    if col_e4.button("😔"): selected_mood = "😔 მოწყენილი"
    if col_e5.button("😡"): selected_mood = "😡 გაბრაზებული"

    mood_note = st.text_input("დაამატე პატარა ჩანაწერი შენს ემოციაზე (არასავალდებულო):", key="mood_input")
    if st.button("💾 ემოციის შენახვა"):
        if selected_mood or mood_note:
            entry = f"{today_str} | {selected_mood if selected_mood else '📝'} {mood_note}"
            st.session_state.mood_logs.append(entry)
            save_data()
            st.success("ემოცია ჩაინიშნა! 🌿")

    st.divider()

    st.subheader("🌊 Urge Surfing — იმპულსის ტალღა")
    if st.button("⏱️ ტალღის გადაგორება (10 წამიანი პაუზა)"):
        with st.spinner("ტალღა გადადის... ისუნთქე ღრმად... 🌬️"):
            time.sleep(10)
        st.success("✅ ყოჩაღ! ტალღამ ჩაიარა!")
        st.session_state.xp += 15
        st.session_state.stars += 1
        save_data()
        st.balloons()

    st.divider()

    # მისიები
    st.subheader(f"📋 დღევანდელი მისიები ({age_group_name})")
    current_missions = AgeBasedMissions.get_missions_for_age(st.session_state.age) + st.session_state.custom_missions
    
    for m in current_missions:
        col_m1, col_m2 = st.columns([3, 1])
        with col_m1:
            st.markdown(f"**{m['title']}**\n\n*{m['desc']}*")
        with col_m2:
            if m['id'] in st.session_state.completed_missions:
                st.success("✅ შესრულებულია")
            else:
                if st.button("შესრულება", key=m['id']):
                    st.session_state.completed_missions.add(m['id'])
                    st.session_state.xp += 20
                    st.session_state.stars += 1
                    save_data()
                    st.rerun()

    st.divider()

    # 🎁 ჯილდოების მაღაზია + 📅 დღეების გრაფიკი
    st.subheader("🎁 ჯილდოების მაღაზია")
    weekday = datetime.now().weekday()  # 0=ორშ, 4=პარ, 5=შაბ, 6=კვ
    is_weekend_window = weekday in [4, 5, 6]  # პარასკევი, შაბათი, კვირა

    if not is_weekend_window:
        st.info("🔒 **ჯილდოების განაღდება შესაძლებელია პარასკევიდან კვირის ჩათვლით!** ახლა დააგროვე ვარსკვლავები. ✨")

    for idx, r in enumerate(st.session_state.rewards):
        col_r1, col_r2 = st.columns([3, 1])
        with col_r1:
            st.markdown(f"**{r['title']}** — `{r['cost']} ⭐`")
        with col_r2:
            if is_weekend_window:
                if st.button("მიღება", key=f"req_{idx}"):
                    if st.session_state.stars >= r['cost']:
                        st.session_state.stars -= r['cost']
                        st.session_state.requested_rewards.append(r['title'])
                        save_data()
                        st.success("🎉 მოთხოვნა გაიგზავნა!")
                        st.rerun()
                    else:
                        st.error("არ გყოფნის ვარსკვლავები!")
            else:
                st.button("🔒 ჩაკეტილია", key=f"req_dis_{idx}", disabled=True)

    if st.session_state.requested_rewards:
        st.subheader("⏳ შენი მომლოდინე ჯილდოები")
        for req_item in st.session_state.requested_rewards:
            st.warning(f"🎁 **{req_item}** — მენტორი/მშობელი ამზადებს ამ ჯილდოს!")

with tab2:
    st.header("👨‍👩‍👧 მშობლის / მენტორის პანელი")

    col_p1, col_p2, col_p3 = st.columns(3)
    col_p1.metric(label="🏆 დონე", value=st.session_state.level)
    col_p2.metric(label="✨ XP", value=f"{st.session_state.xp} / 100")
    col_p3.metric(label="⭐ ვარსკვლავები", value=st.session_state.stars)

    if st.session_state.xp >= 100:
        st.session_state.level += 1
        st.session_state.xp -= 100
        save_data()
        st.success(f"🎉 გადავიდა მე-{st.session_state.level} დონეზე!")

    st.divider()

    # ⭐ ბონუს ვარსკვლავების ჩარიცხვა
    st.subheader("⭐ ბონუს ვარსკვლავის გაჩუქება")
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        if st.button("➕ 1 ⭐"):
            st.session_state.stars += 1
            save_data()
            st.success("+1 ⭐ დაემატა!")
            st.rerun()
    with col_b2:
        if st.button("➕ 3 ⭐"):
            st.session_state.stars += 3
            save_data()
            st.success("+3 ⭐ დაემატა!")
            st.rerun()
    with col_b3:
        if st.button("➕ 5 ⭐"):
            st.session_state.stars += 5
            save_data()
            st.success("+5 ⭐ დაემატა!")
            st.rerun()

    st.divider()

    st.subheader("🎁 მოთხოვნილი ჯილდოები (შესასრულებელი)")
    if not st.session_state.requested_rewards:
        st.write("🎉 მომლოდინე ჯილდოები არ არის.")
    else:
        for idx, req_title in enumerate(st.session_state.requested_rewards):
            col_req1, col_req2, col_req3 = st.columns([2, 1, 1])
            with col_req1:
                st.markdown(f"👉 **{req_title}**")
            with col_req2:
                if st.button("✅ შესრულდა", key=f"done_{idx}"):
                    st.session_state.requested_rewards.pop(idx)
                    save_data()
                    st.rerun()
            with col_req3:
                if st.button("⚠️ ვერ ვასრულებ", key=f"fail_{idx}"):
                    st.session_state.requested_rewards.pop(idx)
                    st.session_state.stars += 2
                    st.session_state.parent_penalties += 1
                    save_data()
                    st.rerun()

    st.divider()

    # 📜 ემოციების ისტორია
    st.subheader("📜 ემოციების ისტორია")
    if st.session_state.mood_logs:
        for log in reversed(st.session_state.mood_logs[-5:]):
            st.write(f"• {log}")
    else:
        st.write("ჯერ ემოციების ჩანაწერი არ არის.")

    st.divider()

    st.subheader("➕ ახალი მისიის დამატება")
    new_m_title = st.text_input("მისიის სათაური:")
    new_m_desc = st.text_input("აღწერა:")
    if st.button("➕ მისიის დამატება"):
        if new_m_title and new_m_desc:
            new_id = f"custom_{len(st.session_state.custom_missions) + 1}"
            st.session_state.custom_missions.append({"title": new_m_title, "desc": new_m_desc, "id": new_id})
            save_data()
            st.success("მისია დაემატა!")
            st.rerun()

    st.divider()

    if st.button("🔄 დღის გადატვირთვა"):
        st.session_state.completed_missions.clear()
        save_data()
        st.success("დღიური მისიები განახლდა!")
        st.rerun()
        
