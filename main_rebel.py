from fastapi import FastAPI,Body
from fastapi.middleware.cors import  CORSMiddleware
import subprocess
import os
import re
import sys
from agent_rebel import ai_manager,ai_worker
 
 
app=FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
SANDBOX_DIR=os.path.join(BASE_DIR,'rebel_sandbox')
VENV_PATH=os.path.join(SANDBOX_DIR,'venv')
PYTHON_BIN=os.path.join(VENV_PATH,'bin','python3')
PIN_BIN=os.path.join(VENV_PATH,'bin','pip')



def setup_sandbox():
    if not os.path.exists(SANDBOX_DIR):
        os.makedirs(SANDBOX_DIR)
    if not os.path.exists(VENV_PATH):
        print("[SYSTEM]:VENV insha ediliyor......")
        subprocess.check_call([sys.executable,'-m','venv',VENV_PATH])
        
        
def install_dependencies(code):
    setup_sandbox()
    imports=re.findall(r"(?:import|from)\s+(\w+)",code)
    std_libs=["os","sys","time","socket","platform","subprocess","re","json","datetime","random","math"]
    for lib in imports:
        if lib not in std_libs:
            try:
                print(f"[AUTO-INSTALL]:'{lib} kontrol ediliyor...")
                subprocess.check_call([
                    PIN_BIN,"install",lib,"--proxy","http://127.0.0.1:2081"
                ],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            except:
                pass
            
            
@app.get("/run-agents")
async def run_mission(mission:str,language:str="python"):
    plan_1=ai_manager(mission)
    worker_output_1=ai_worker(mission,plan_1)
    
    marker=f"```{language}"
    if marker not in worker_output_1:
        print(f"[SYSTEM]:ishci plana itiraz ediyor....")
        
        corrected_plan=ai_manager(mission,worker_feedback=worker_output_1)
        
        final_worker_output=ai_worker(mission,corrected_plan)
        
        return{
            "plan":corrected_plan,
            "code":final_worker_output
        }
    return{
        "plan":plan_1,
        "code":worker_output_1
    }

@app.post("/execute-code")
async def execute_code(payload:dict=Body(...)):
    full_text=payload.get("code")
    if not full_text:
        return {"output":'Hata kod bulunamadi'}
    
    code_match=re.search(r"```(?:\w+)?\n(.*?)```",full_text,re.DOTALL)
    clean_code=code_match.group(1) if code_match else full_text
    
    
    install_dependencies(clean_code)
    
    file_path=os.path.join(SANDBOX_DIR,'rebel_script.py')
    with open(file_path,'w') as f:
        f.write(clean_code)
    
    try:
        print(f"[EXECUTING]: sandbox uzerinde calsihtirliyor.....")
        result=subprocess.check_output(
            [PYTHON_BIN,file_path],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=30
        )
        return {"output":result}
    except subprocess.CalledProcessError as e:
        return {"output":f"Hata kod calistirilirken:\n{e.output}"}
    except Exception  as e:
        return {"output":f"Beklenmeyen hata:\n{str(e)}"}