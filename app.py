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

# ==========================================
# 1. ენების ლექსიკონი (TRANSLATIONS)
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
        "urge_button": "⏱️️ Переждать волну (пауза 10 сек)",
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
    },
    "Türkçe": {
        "title": "⭐ GameOfUs: Family Edition",
        "subtitle": "Çocuk için oyun • Ebeveyn için destek • Her ikisi için gelişim",
        "profile": "👤 Profil",
        "enter_age": "Yaşı giriniz:",
        "group_label": "📌 Grup:",
        "tab_child": "👦 Çocuk / Kahraman Alanı",
        "tab_parent": "👨‍👩‍👧 Ebeveyn / Rehber Paneli",
        "hello_hero": "Merhaba, Kahraman! 👋",
        "stars_label": "⭐ Yıldızların:",
        "level_label": "🏆 Seviye:",
        "xp_label": "✨ XP:",
        "energy_label": "⚡ Enerjin:",
        "energy_plus": "🔋 Enerji Artır (+2)",
        "energy_minus": "🪫 Yoruldum (-2)",
        "mood_title": "💭 Bugün nasıl hissediyorsun?",
        "mood_happy": "😃 Mutlu",
        "mood_calm": "🧘 Sakin",
        "mood_tired": "😴 Yorgun",
        "mood_sad": "😔 Üzgün",
        "mood_angry": "😡 Kızgın",
        "mood_note_placeholder": "Duygunuzla ilgili küçük bir not ekleyin (isteğe bağlı):",
        "save_mood": "💾 Duyguyu Kaydet",
        "mood_saved": "Duygu kaydedildi! 🌿",
        "urge_title": "🌊 Urge Surfing — Dalgayı Yakala",
        "urge_button": "⏱️ Dalgayı geçiştir (10 sn duraklat)",
        "urge_spinner": "Dalga geçiyor... Derin nefes al... 🌬️",
        "urge_success": "✅ Harika! Dalga geçti!",
        "missions_title": "📋 Bugünkü Görevler",
        "completed": "✅ Tamamlandı",
        "do_mission": "Tamamla",
        "rewards_title": "🎁 Ödül Mağazası",
        "rewards_locked_msg": "🔒 **Ödüller sadece Cuma ve Pazar günleri arasında alınabilir!** Şimdilik yıldız topla. ✨",
        "claim_reward": "Al",
        "locked_button": "🔒 Kilitli",
        "reward_requested": "🎉 İstek gönderildi!",
        "no_stars": "Yeterli yıldız yok!",
        "pending_rewards": "⏳ Bekleyen Ödüllerin",
        "preparing_reward": "Ebeveyn bu ödülü hazırlıyor!",
        "parent_panel": "👨‍👩‍‍👧 Ebeveyn / Rehber Paneli",
        "level_up": "🎉 Seviye {} ulaşıldı!",
        "bonus_stars": "⭐ Hediye Yıldız Ver",
        "bonus_added": "+{} ⭐ eklendi!",
        "requested_rewards_parent": "🎁 İstenen Ödüller",
        "no_pending_rewards": "🎉 Bekleyen ödül yok.",
        "mark_done": "✅ Tamamlandı",
        "cant_do": "⚠️ Yapılamıyor",
        "mood_history": "📜 Duygu Geçmişi",
        "no_moods": "Henüz duygu kaydı yok.",
        "add_mission": "➕ Yeni Görev Ekle",
        "mission_title_input": "Görev Başlığı:",
        "mission_desc_input": "Açıklama:",
        "add_mission_btn": "➕ Görev Ekle",
        "mission_added": "Görev eklendi!",
        "reset_day": "🔄 Günü Sıfırla",
        "reset_success": "Günlük görevler yenilendi!",
        "select_language": "🌐 Dil Seçin",
        "settings": "⚙️ Ayarlar"
    },
    "中文": {
        "title": "⭐ GameOfUs: 家庭版",
        "subtitle": "孩子的游戏 • 父母的助力 • 共同的成长",
        "profile": "👤 个人资料",
        "enter_age": "输入年龄：",
        "group_label": "📌 组别：",
        "tab_child": "👦 英雄 / 孩子空间",
        "tab_parent": "👨‍👩‍👧 父母 / 导师面板",
        "hello_hero": "你好，小英雄！👋",
        "stars_label": "⭐ 你的星星：",
        "level_label": "🏆 等级：",
        "xp_label": "✨ 经验值 (XP)：",
        "energy_label": "⚡ 你的体力：",
        "energy_plus": "🔋 补充体力 (+2)",
        "energy_minus": "🪫 感到累了 (-2)",
        "mood_title": "💭 你今天感觉怎么样？",
        "mood_happy": "😃 开心",
        "mood_calm": "🧘 平静",
        "mood_tired": "😴 疲惫",
        "mood_sad": "😔 难过",
        "mood_angry": "😡 生气",
        "mood_note_placeholder": "写下你的心情笔记（选填）：",
        "save_mood": "💾 保存心情",
        "mood_saved": "心情已记录！🌿",
        "urge_title": "🌊 冲浪体验 — 战胜冲动",
        "urge_button": "⏱️ 跨越冲动（暂停10秒）",
        "urge_spinner": "冲动正在退去... 深呼吸... 🌬️",
        "urge_success": "✅ 太棒了！冲动已平息！",
        "missions_title": "📋 今日任务",
        "completed": "✅ 已完成",
        "do_mission": "去完成",
        "rewards_title": "🎁 奖励商店",
        "rewards_locked_msg": "🔒 **奖励兑换仅在周五至周日开放！** 现在先积累星星吧。✨",
        "claim_reward": "兑换",
        "locked_button": "🔒 未解锁",
        "reward_requested": "🎉 申请已发送！",
        "no_stars": "星星数量不足！",
        "pending_rewards": "⏳ 待兑换的奖励",
        "preparing_reward": "家长正在为你准备这项奖励！",
        "parent_panel": "👨‍👩‍👧 父母 / 导师控制台",
        "level_up": "🎉 升到了第 {} 级！",
        "bonus_stars": "⭐ 赠送奖励星星",
        "bonus_added": "已添加 +{} ⭐！",
        "requested_rewards_parent": "🎁 申请中的奖励",
        "no_pending_rewards": "🎉 暂无待处理的奖励。",
        "mark_done": "✅ 已完成",
        "cant_do": "⚠️ 无法完成",
        "mood_history": "📜 心情历史记录",
        "no_moods": "暂无心情记录。",
        "add_mission": "➕ 添加新任务",
        "mission_title_input": "任务名称：",
        "mission_desc_input": "任务描述：",
        "add_mission_btn": "➕ 添加任务",
        "mission_added": "任务添加成功！",
        "reset_day": "🔄 重置当天任务",
        "reset_success": "每日任务已刷新！",
        "select_language": "🌐 选择语言",
        "settings": "⚙️ 设置"
    },
    "日本語": {
        "title": "⭐ GameOfUs: ファミリーエディション",
        "subtitle": "子どものためのゲーム • 親のためのサポート • 共に育む未来",
        "profile": "👤 プロフィール",
        "enter_age": "年齢を入力:",
        "group_label": "📌 グループ:",
        "tab_child": "👦 ヒーロー / 子どもエリア",
        "tab_parent": "👨‍👩‍👧 保護者 / メンターパネル",
        "hello_hero": "こんにちは、ヒーロー！ 👋",
        "stars_label": "⭐ 集めたスター:",
        "level_label": "🏆 レベル:",
        "xp_label": "✨ 経験値 (XP):",
        "energy_label": "⚡ 現在の体力:",
        "energy_plus": "🔋 体力回復 (+2)",
        "energy_minus": "🪫 疲れた (-2)",
        "mood_title": "💭 今日はどんな気分ですか？",
        "mood_happy": "😃 楽しい",
        "mood_calm": "🧘 穏やか",
        "mood_tired": "😴 疲れた",
        "mood_sad": "😔 悲しい",
        "mood_angry": "😡 怒っている",
        "mood_note_placeholder": "今の気持ちを書きみましょう（任意）:",
        "save_mood": "💾 気分を保存",
        "mood_saved": "記録しました！ 🌿",
        "urge_title": "🌊 衝動サーフィン — 波を乗り越えよう",
        "urge_button": "⏱ 波をやり過ごす（10秒間ストップ）",
        "urge_spinner": "波が引いていきます... 深呼吸しましょう... 🌬️",
        "urge_success": "✅ よくできました！波が去りました！",
        "missions_title": "📋 今日のミッション",
        "completed": "✅ 達成済み",
        "do_mission": "挑戦する",
        "rewards_title": "🎁 ご褒美ストア",
        "rewards_locked_msg": "🔒 **ご褒美の交換は金曜日から日曜日まで可能です！** 今はスターを貯めましょう。✨",
        "claim_reward": "交換する",
        "locked_button": "🔒 ロック中",
        "reward_requested": "🎉 リクエストを送信しました！",
        "no_stars": "スターが足りません！",
        "pending_rewards": "⏳ 準備中のご褒美",
        "preparing_reward": "保護者がご褒美を準備しています！",
        "parent_panel": "👨‍👩‍👧 保護者 / メンターパネル",
        "level_up": "🎉 レベル {} に上がりました！",
        "bonus_stars": "⭐ ボーナススターをあげる",
        "bonus_added": "+{} ⭐ 追加されました！",
        "requested_rewards_parent": "🎁 リクエストされたご褒美",
        "no_pending_rewards": "🎉 保留中のご褒美はありません。",
        "mark_done": "✅ 完了",
        "cant_do": "⚠️ 実行不可",
        "mood_history": "📜 感情の履歴",
        "no_moods": "まだ記録がありません。",
        "add_mission": "➕ 新しいミッションを追加",
        "mission_title_input": "ミッションのタイトル:",
        "mission_desc_input": "説明:",
        "add_mission_btn": "➕ ミッション追加",
        "mission_added": "ミッションを追加しました！",
        "reset_day": "🔄 日付のリセット",
        "reset_success": "デイリーミッションが更新されました！",
        "select_language": "🌐 言語を選択",
        "settings": "⚙️ 設定"
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
        "rewards": st.session_state.rewards
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

# ენის არჩევა
language_list = ["ქართული", "English", "Русский", "Türkçe", "中文", "日本語"]
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

tab1, tab2 = st.tabs([t("tab_child"), t("tab_parent")])

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

    # 📋 მისიები (აქ გადაეცემა არჩეული ენა)
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

    # 🎁 ჯილდოების მაღაზია + 📅 დღეების გრაფიკი
    st.subheader(t("rewards_title"))
    weekday = datetime.now().weekday()  # 0=ორშ, 4=პარ, 5=შაბ, 6=კვ
    is_weekend_window = weekday in [4, 5, 6]  # პარასკევი, შაბათი, კვირა

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

    # ⭐ ბონუს ვარსკვლავების ჩარიცხვა
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
