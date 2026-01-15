from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
import re
import sys
from agent import ai_manager, ai_worker 

app = FastAPI()

# GÜVENLİK: Frontend bağlantı izni
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SANDBOX (GÜVENLİ BÖLGE) AYARLARI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SANDBOX_DIR = os.path.join(BASE_DIR, "rebel_sandbox")
VENV_PATH = os.path.join(SANDBOX_DIR, "venv")
PYTHON_BIN = os.path.join(VENV_PATH, "bin", "python3")
PIP_BIN = os.path.join(VENV_PATH, "bin", "pip")

def setup_sandbox():
    """Venv'i hazırlar."""
    if not os.path.exists(SANDBOX_DIR):
        os.makedirs(SANDBOX_DIR)
    if not os.path.exists(VENV_PATH):
        print("[SYSTEM]: Güvenli bölge (venv) inşa ediliyor...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_PATH])

def install_dependencies(code):
    """Kütüphaneleri sandbox venv içine yükler."""
    setup_sandbox()
    imports = re.findall(r"(?:import|from)\s+(\w+)", code)
    std_libs = ["os", "sys", "time", "socket", "platform", "subprocess", "re", "json", "datetime", "random", "math"]
    for lib in imports:
        if lib not in std_libs:
            try:
                print(f"[AUTO-INSTALL]: '{lib}' kontrol ediliyor...")
                subprocess.check_call([
                    PIP_BIN, "install", lib, "--proxy", "http://127.0.0.1:2081"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass

# --- ENDPOINT 1: Ajanlar Arası Tartışma ve Üretim ---
@app.get("/run-agents")
async def run_mission(mission: str, language: str = "python"):
    print(f"\n[SYSTEM]: Tur 1 Başlatılıyor...")
    # 1. Müdür ilk planı yapar
    plan_1 = ai_manager(mission)
    # 2. İşçi planı kontrol eder (Kod yazabilir veya itiraz edebilir)
    worker_output_1 = ai_worker(mission, plan_1)
    
    # EĞER İŞÇİ KOD YAZMADIYSA (Hata bulup itiraz ettiyse)
    if "```python" not in worker_output_1:
        print("[SYSTEM]: İşçi plana itiraz etti! Hata düzeltme döngüsü başlatılıyor...")
        
        # 3. Müdür hatasını düzeltir
        corrected_plan = ai_manager(mission, worker_feedback=worker_output_1)
        # 4. İşçi yeni planı alıp final kodunu yazar
        final_worker_output = ai_worker(mission, corrected_plan)
        
        return {
            "plan": corrected_plan,
            "code": final_worker_output
        }
    
    # Eğer ilk seferde her şey doğruysa
    return {
        "plan": plan_1,
        "code": worker_output_1
    }

# --- ENDPOINT 2: Üretilen Kodun Sandbox'ta Çalıştırılması ---
@app.post("/execute-code")
async def execute_code(payload: dict = Body(...)):
    full_text = payload.get("code")
    if not full_text:
        return {"output": "Hata: Kod bulunamadı."}

    # Sadece python bloğunu ayıkla
    code_match = re.search(r"```python\n(.*?)```", full_text, re.DOTALL)
    clean_code = code_match.group(1) if code_match else full_text

    # 1. Kütüphaneleri izole ortama kur
    install_dependencies(clean_code)

    file_path = os.path.join(SANDBOX_DIR, "rebel_script.py")
    with open(file_path, "w") as f:
        f.write(clean_code)
    
    try:
        # 2. Kodu SANDBOX VENV içinde çalıştır
        print(f"[EXECUTING]: Sandbox üzerinde çalıştırılıyor...")
        result = subprocess.check_output(
            [PYTHON_BIN, file_path], 
            stderr=subprocess.STDOUT, 
            universal_newlines=True,
            timeout=30
        )
        return {"output": result}
    except subprocess.CalledProcessError as e:
        return {"output": f"KOD HATASI (Sandbox):\n{e.output}"}
    except Exception as e:
        return {"output": f"SİSTEM HATASI: {str(e)}"}
