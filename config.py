import os

# 1. NETWORK AYARLARI (SOCKS Destanı burada yaşıyor)
# İnternet trafiğini yerel SOCKS5 proxy (Port 2080) üzerinden geçir.
# 'socks5h' sayesinde DNS sorgularını da gizle/yönlendir.
# Ancak yerel bağlantıları (localhost) bu tünele sokma, direkt bağlansın.
os.environ['https_proxy']='socks5h://127.0.0.1:2080'
os.environ['http_proxy']='socks5h://127.0.0.1:2080'
os.environ["no_proxy"]='localhost,127.0.0.1'


# 2. API VE YOLLAR
GROQ_API_KEY="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"

# Projenin çalıştığı ana dizini (root folder) dinamik olarak bulur. 
# Böylece proje başka bilgisayara taşınsa bile dosya yolları bozulmaz.
#/home/proje
BASE_DIR=os.path.dirname(os.path.abspath(__file__))

# Ana dizinin (BASE_DIR) sonuna 'rebel_sandbox' klasörünü ekleyerek tam yolu oluşturur.
# Windows/Linux fark etmeksizin araya doğru \ veya / işaretini kendi koyar.
#/home/proje + /rebel_sandbox
SANDBOX_DIR=os.path.join(BASE_DIR,'rebel_sandbox')


# Sandbox klasörünün içindeki Python Sanal Ortam (Virtual Environment) yolunu tanımlar.
# Bu klasörde projenin kütüphaneleri (pip install ile kurulanlar) bulunur.
#/home/proje/rebel_sandbox + /venv
VENV_PATH=os.path.join(SANDBOX_DIR,'venv')

# Sanal ortamı terminaldeki gibi 'activate' etmemize gerek yok.
# Doğrudan venv içindeki Python dosyasını (binary) çağırdığımızda, 
# o zaten kendi kütüphanelerini otomatik olarak tanır ve kullanır.
# VENV_PATH'in üzerine '/bin' klasörünü ve '/python3' dosyasını ekler.



# 3. EXECUTABLE YOLLARI

#/home/proje/rebel_sandbox/venv + /bin + /python3
PYTHON_BIN=os.path.join(VENV_PATH,'bin','python3')

#/home/proje/rebel_sandbox/venv + /bin + /pip
#YAGNY 2 AYRY YOL DOREDES /home/proje/rebel_sandbox/venv SHUNDAN SON
PIP_BIN=os.path.join(VENV_PATH,'bin','pip')



# 3. EXECUTABLE YOLLARI

