from app.models import User
import ollama

class DoctorRecommendationService:
    @staticmethod
    def recommend_doctors(complaint):
        all_doctors = User.query.filter(User.user_type == 'doctor').all()
        doctor_list = [
            {
                'id': d.id,
                'name': d.name,
                'surname': d.surname,
                'specialty': d.specialty,
                'email': d.email,
            }
            for d in all_doctors
        ]

        prompt = f"Скарга пацієнта: {complaint}\n\nОсь список лікарів:\n"
        for i, d in enumerate(doctor_list, 1):
            prompt += f"{i}. email: {d['email']} {d['name']} {d['surname']}, спеціальність: {d['specialty']}\n"

        prompt += "\nВибери лікарів, які підходять для цієї скарги. Якщо лікар чітко не підходить, не згадуй його взагалі, наприклад, гінеколог не лікує проблеми болю в спині. Згадуй або всіх лікарів однієї професії, або нікого. Поверни коротку відповідь, лише їхні email у форматі списку Python."


        response = ollama.chat(model="mistral", messages=[
            {"role": "user", "content": prompt}
        ])

        recommended_emails = response['message']['content']
        print(recommended_emails)

        filtered = [
            d for d in doctor_list
            if d['email'] in recommended_emails
        ]

        return filtered
