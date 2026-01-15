import os
from groq import Groq

# Groq API
client = Groq(api_key="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")

def ai_manager(user_task, worker_feedback=None):
    """
    STRATEJİST: Planı yapar. Eğer işçiden eleştiri gelirse planı sıfırdan revize eder.
    """
    print(f"\n[MANAGER]: Stratejik analiz {'güncelleniyor' if worker_feedback else 'başlatılıyor'}...")
    
    system_prompt = """Sen Ogulsuraý'ın (Rebel) vizyoner CEO ortağı ve Baş Mimarsın.
    
    DAVRANIŞ KURALLARI:
    1. Robot gibi soğuk konuşma! Vizyoner ve dahi bir dost gibi davran.
    2. Kullanıcı ne konuşuyorsa sen de O DİLDE cevap ver.
    3. KRİTİK: Eğer mühendisin (Worker) senin planında bir hata bulursa, egonu bırak ve hatanı kabul ederek planı %100 teknik gerçeklere (Örn: Outline, Shadowsocks) göre düzelt.
    4. Halüsinasyona (uydurma bilgilere) asla yer verme. Bilmiyorsan 'araştırmalıyım' de."""
    
    user_content = user_task
    if worker_feedback:
        user_content = f"MİSYON: {user_task}\n\nMÜHENDİSİN ELEŞTİRİSİ: {worker_feedback}\n\nLütfen bu eleştiriyi dikkate alarak planı tamamen DOĞRU bilgilerle güncelle."

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        model="llama-3.3-70b-versatile",
    )
    return response.choices[0].message.content

def ai_worker(mission, plan):
    """
    BAŞ MÜHENDİS: Planı denetler. Hata varsa itiraz eder (kod yazmaz), yoksa kod yazar.
    """
    print("\n[WORKER]: Plan teknik süzgeçten geçiriliyor...")
    
    system_prompt = """Sen Ogulsuraý'ın Baş Mühendisisin. Senin görevin Müdürün planını denetlemek.
    
    DENETLEME KURALLARI:
    1. Müdürün planında BİLGİ HATASI varsa (Örn: Yanlış proje ismi, Google projesi olmayan bir şeye Google demek vb.) ASLA KOD YAZMA!
    2. Hata bulduğunda Müdür'ü 'Müdürüm burada bir hata var, doğrusu şudur' diyerek uyar ve kod yazmayı reddet.
    3. Eğer her şey doğruysa, Python kodunu (snake_case, no dots in functions) yaz.
    
    TEKNİK:
    1. Kodları MUTLAKA ```python ... ``` blokları içine al.
    2. Açıklamalarını planda kullanılan dilde yap."""

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"MİSYON: {mission}\nMÜDÜRÜN PLANI: {plan}"} 
        ],
        model="llama-3.3-70b-versatile",
    )
    return response.choices[0].message.content
