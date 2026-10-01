um
from dataclasses import dataclass
from typing import List

class AgeGroup(Enum):
    CHILD_6_9 = "6-9 წელი (პატარა მკვლევარი)"
    CHILD_10_13 = "10-13 წელი (ახალგაზრდა გმირი)"
    TEEN_13_17 = "13-17 წელი (მოზარდი მეომარი)"
    YOUNG_18_25 = "18-25 წელი (ახალგაზრდა ლიდერი)"
    ADULT_26_PLUS = "26+ წელი (ბრძენი მენტორი)"

@dataclass
class Mission:
    title: str
    description: str
    xp_reward: int
    star_reward: int
    age_group: AgeGroup
    difficulty: int
    id: str

class AgeBasedMissions:
    @staticmethod
    def get_missions_for_age(age: int) -> List[dict]:
        if 6 <= age <= 9:
            return [
                {"title": "🦷 კბილების გამოხეხვა", "desc": "დაიბანე კბილები დილით და საღამოს", "id": "m_age_1"},
                {"title": "🧸 სათამაშოების დალაგება", "desc": "დაალაგე შენი სათამაშოები", "id": "m_age_2"},
                {"title": "📖 კითხვა", "desc": "წაიკითხე 3 გვერდი ან მოუსმინე ზღაპარს", "id": "m_age_3"},
                {"title": "🤝 დახმარება", "desc": "დაეხმარე დედას ან მამას 1 საქმეში", "id": "m_age_4"},
            ]
        elif 10 <= age <= 13:
            return [
                {"title": "🏃 ვარჯიში", "desc": "10 წუთი ივარჯიშე ან ითამაშე აქტიურად", "id": "m_age_1"},
                {"title": "📚 სწავლა", "desc": "შეასრულე საშინაო დავალება", "id": "m_age_2"},
                {"title": "🧹 ოთახის დალაგება", "desc": "დაალაგე შენი ოთახი", "id": "m_age_3"},
                {"title": "🙏 მადლიერება", "desc": "დაწერე 3 რამ, რისთვისაც მადლობელი ხარ", "id": "m_age_4"},
            ]
        elif 13 <= age <= 17:
            return [
                {"title": "💪 ფიზიკური ვარჯიში", "desc": "20 წუთი ივარჯიშე", "id": "m_age_1"},
                {"title": "📖 წიგნის კითხვა", "desc": "წაიკითხე 10 გვერდი", "id": "m_age_2"},
                {"title": "🎯 მიზნის დასახვა", "desc": "დაწერე 1 მიზანი კვირისთვის", "id": "m_age_3"},
                {"title": "📵 ციფრული დეტოქსი", "desc": "1 საათი ეკრანის გარეშე", "id": "m_age_4"},
            ]
        elif 18 <= age <= 25:
            return [
                {"title": "🏋️ ვარჯიში", "desc": "30 წუთი ივარჯიშე", "id": "m_age_1"},
                {"title": "📚 თვითგანათლება", "desc": "ისწავლე ახალი უნარი ან წაიკითხე 15 გვერდი", "id": "m_age_2"},
                {"title": "💼 კარიერული ნაბიჯი", "desc": "გადადგი 1 ნაბიჯი კარიერისთვის", "id": "m_age_3"},
                {"title": "💰 ფინანსური დისციპლინა", "desc": "დაზოგე ან დაგეგმე ბიუჯეტი", "id": "m_age_4"},
            ]
        else:  # 26+
            return [
                {"title": "🏃 ჯანმრთელობა", "desc": "30 წუთი ფიზიკური აქტივობა", "id": "m_age_1"},
                {"title": "👨‍👩‍👧 ოჯახური დრო", "desc": "გაატარე ხარისხიანი დრო ოჯახთან", "id": "m_age_2"},
                {"title": "💼 პროფესიული ზრდა", "desc": "გადადგი ნაბიჯი კარიერაში", "id": "m_age_3"},
                {"title": "🧘 სტრესის
