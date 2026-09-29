import streamlit as st
import time

# გვერდის კონფიგურაცია
st.set_page_config(
    page_title="GameOfUs: Family Edition",
    page_icon="⭐",
    layout="centered"
)

# სესიის მდგომარეობის ინიციალიზაცია
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'stars' not in st.session_state:
    st.session_state.stars = 0
if 'energy' not in st.session_state:
    st.session_state.energy = 5
if 'completed_missions' not in st.session_state:
    st.session_state.completed_missions = set()
if 'rewards' not in st.session_state:
    st.session_state.rewards = [
        {"title": "🚲 30 წუთი ველოსიპედით სეირნობა", "cost": 3},
        {"title": "🍦 საყვარელი ნაყინი", "cost": 5},
        {"title": "🎬 საღამოს ანიმაციური ფილმი", "cost": 7},
        {"title": "🎡 კვირას პარკში წასვლა", "cost": 10},
    ]

st.title("⭐ GameOfUs: Family Edition")
st.caption("თამაში ბავშვისთვის • მხარდაჭერა მშობლისთვის • ზრდა ორივესთვის")

# ტაბების შექმნა
tab1, tab2 = st.tabs(["👦 ბავშვის სივრცე", "👨‍👩‍👧 მშობლის პანელი"])

with tab1:
    st.header("გამარჯობა, გმირო! 👋")
    st.info(f"⭐ შენი ვარსკვლავების ბალანსი: **{st.session_state.stars} ⭐** | 🏆 დონე: **{st.session_state.level}**")
    
    # ენერგიის მაჩვენებელი
    st.subheader(f"⚡ შენი ენერგია: {st.session_state.energy}/10")
    
    if st.session_state.energy >= 7:
        st.success("მიმდინარე ზონა: 🟢 მწვანე (ოპტიმალური / Focus) — საუკეთესო დროა სწავლისა და შემოქმედებისთვის!")
    elif st.session_state.energy >= 4:
        st.warning("მიმდინარე ზონა: 🟡 ყვითელი (დაღლილი / Caution) — დროა ცოტა დაისვენო ან წყალი დალიო.")
    else:
        st.error("მიმდინარე ზონა: 🔴 წითელი (გადაღლილი / Danger) — გჭირდება მშვიდი პაუზა და განტვირთვა!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔋 ენერგიის მომატება (+2)"):
            st.session_state.energy = min(10, st.session_state.energy + 2)
            st.rerun()
    with col2:
        if st.button("🪫 დავიღალე (-2)"):
            st.session_state.energy = max(1, st.session_state.energy - 2)
            st.rerun()

    st.divider()

    # Urge Surfing (იმპულსის ტალღა)
    st.subheader("🌊 Urge Surfing — იმპულსის ტალღა")
    st.write("თუ იგრძენი ბრაზი ან იმპულსი, ჩართე ტაიმერი და დაელოდე ტალღის გადაგორებას!")
    
    if st.button("⏱️ ტალღის გადაგორება (10 წამიანი პაუზა)"):
        with st.spinner("ტალღა გადადის... ისუნთქე ღრმად... 🌬️"):
            time.sleep(10)
        st.success("✅ ყოჩაღ! ტალღამ ჩაიარა. შენ დაამარცხე იმპულსი!")
        st.session_state.xp += 15
        st.session_state.stars += 1
        st.balloons()

    st.divider()

    # დღევანდელი მისიები
    st.subheader("📋 დღევანდელი მისიები")
    
    missions = [
        ("🏀 რაინდის ვარჯიში", "10 წუთი ივარჯიშე ან ითამაშე აქტიურად", "m1"),
        ("📚 სიბრძნის წიგნი", "წაიკითხე 5 გვერდი ან ისწავლე 3 ახალი სიტყვა", "m2"),
        ("🧹 ციხესიმაგრის მოწესრიგება", "დაეხმარე დედას/მამას 1 საქმეში ან დაალაგე ოთახი", "m3"),
        ("🐾 ცხოველების მფარველი", "დაუსხი წყალი/საჭმელი შინაურ ან ეზოს ცხოველს", "m4"),
        ("🤝 სიკეთის ტალღა", "გააკეთე 1 კეთილი საქმე (დაეხმარე მეგობარს/და-ძმას)", "m5"),
    ]

    for title, desc, m_id in missions:
        col_m1, col_m2 = st.columns([3, 1])
        with col_m1:
            st.markdown(f"**{title}**\n\n*{desc}*")
        with col_m2:
            if m_id in st.session_state.completed_missions:
                st.success("✅ შესრულებულია")
            else:
                if st.button("შესრულება", key=m_id):
                    st.session_state.completed_missions.add(m_id)
                    st.session_state.xp += 20
                    st.session_state.stars += 1
                    st.rerun()

    st.divider()

    # ჯილდოების მაღაზია ბავშვისთვის
    st.subheader("🎁 ჯილდოების მაღაზია")
    st.write("გადაცვალე შენი დაგროვილი ვარსკვლავები საჩუქრებში!")
    
    for idx, r in enumerate(st.session_state.rewards):
        col_r1, col_r2 = st.columns([3, 1])
        with col_r1:
            st.markdown(f"**{r['title']}** — `{r['cost']} ⭐`")
        with col_r2:
            if st.button("მიღება", key=f"req_{idx}"):
                if st.session_state.stars >= r['cost']:
                    st.session_state.stars -= r['cost']
                    st.success(f"🎉 ყოჩაღ! შენ აირჩიე: {r['title']}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("არ გყოფნის ვარსკვლავები!")

with tab2:
    st.header("👨‍👩‍👧 მშობლის მართვის პანელი")
    st.info("აქ შეგიძლიათ თვალი ადევნოთ პროგრესს, დააჯილდოოთ ბავშვი და მართოთ ჯილდოები.")

    # პროგრესი
    col_p1, col_p2, col_p3 = st.columns(3)
    col_p1.metric(label="🏆 დონე", value=st.session_state.level)
    col_p2.metric(label="✨ XP", value=f"{st.session_state.xp} / 100")
    col_p3.metric(label="⭐ ვარსკვლავები", value=st.session_state.stars)

    # დონის ავტომატური მომატება
    if st.session_state.xp >= 100:
        st.session_state.level += 1
        st.session_state.xp -= 100
        st.success(f"🎉 ლოცავთ! ბავშვი გადავიდა მე-{st.session_state.level} დონეზე!")

    st.divider()

    # შექება და ბონუსები
    st.subheader("🌟 ბონუსის მიცემა")
    bonus_xp = st.number_input("წახალისების XP:", min_value=5, max_value=50, step=5)
    bonus_stars = st.number_input("წახალისების ვარსკვლავები (⭐):", min_value=1, max_value=5, step=1)
    if st.button("🎁 ბონუსის გაცემა"):
        st.session_state.xp += bonus_xp
        st.session_state.stars += bonus_stars
        st.success(f"ბავშვს დაემატა {bonus_xp} XP და {bonus_stars} ⭐!")
        st.rerun()

    st.divider()

    # ახალი ჯილდოების დამატება მშობლის მიერ
    st.subheader("➕ ახალი ჯილდოს დამატება")
    new_reward_title = st.text_input("ჯილდოს დასახელება (მაგ: 🍦 ნაყინი):")
    new_reward_cost = st.number_input("ღირებულება ვარსკვლავებში (⭐):", min_value=1, max_value=50, value=3)
    
    if st.button("➕ ჯილდოს დამატება"):
        if new_reward_title:
            st.session_state.rewards.append({"title": new_reward_title, "cost": new_reward_cost})
            st.success(f"ჯილდო '{new_reward_title}' წარმატებით დაემატა!")
            st.rerun()

    st.divider()

    if st.button("🔄 დღის გადატვირთვა (ახალი დღის დაწყება)"):
        st.session_state.completed_missions.clear()
        st.success("დღიური მისიები განახლდა!")
        st.rerun()
        
