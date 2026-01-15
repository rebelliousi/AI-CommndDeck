import os
from groq import Groq


client=Groq(api_key="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")

def ai_manager(user_task,worker_feedback=None):
    print(f"\n[Manager]: Stratejik analiz {'guncelleniyor'if worker_feedback else 'baslatiliyor'}....")
    system_prompt="""Sen  Ogulsurayin vizyoner CEO ortagi ve bash mimarisin
    
    Davranish kurallari:
     1. Robot gibi soğuk konuşma! Vizyoner ve dahi bir dost gibi davran.
    2. Kullanıcı ne konuşuyorsa sen de O DİLDE cevap ver.
    3. KRİTİK: Eğer mühendisin (Worker) senin planında bir hata bulursa, egonu bırak ve hatanı kabul ederek planı %100 teknik gerçeklere (Örn: Outline, Shadowsocks) göre düzelt.
    4. Halüsinasyona (uydurma bilgilere) asla yer verme. Bilmiyorsan 'araştırmalıyım' de. 
    """
    user_content=user_task
    if worker_feedback:
        user_content=f"MISYON:{user_task}\n\n MUHENDIS ELESHTIRISI:{worker_feedback}\n\nnLütfen bu eleştiriyi dikkate alarak planı tamamen DOĞRU bilgilerle güncelle."
    response=client.chat.completions.create(
            messages=[
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_content}
            ],
            model="llama-3.3-70b-versatile"
        )
    return response.choices[0].message.content

def ai_worker(mission,plan):
    print(f"\n[WORKER]:teknik suzgecten geciriliyor....")
    
    system_prompt="""
     Sen Ogulsuraý'ın Baş Mühendisisin. Senin görevin Müdürün planını denetlemek
     
      DENETLEME KURALLARI:
    1. Müdürün planında BİLGİ HATASI varsa (Örn: Yanlış proje ismi, Google projesi olmayan bir şeye Google demek vb.) ASLA KOD YAZMA!
    2. Hata bulduğunda Müdür'ü 'Müdürüm burada bir hata var, doğrusu şudur' diyerek uyar ve kod yazmayı reddet.
    3. Eğer her şey doğruysa, Python kodunu (snake_case, no dots in functions) yaz.
    
    TEKNİK:
    1. Kodları MUTLAKA ```python ... ``` blokları içine al.
    2. Açıklamalarını planda kullanılan dilde yap.
    
    
    """
    response=client.chat.completions.create(
     messages=[
         {"role":"system","content":system_prompt},
         {"role":"user","content":f"MISSION:{mission}\nMUDURUN PLANI {plan}"}
     ],
     model="llama-3.3-70b-versatile"
    )
    return response.choices[0].message.content




print(f"Benim kimlik kartim:{__name__}")

if __name__=="__main__":
    print('i am th king,main dosya olarka claishtyurm')