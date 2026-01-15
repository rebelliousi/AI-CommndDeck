class TunnelingProtocols:
    def __init__(self):
        self.protocols = [
            {"name": "shadowsocks", "description": "Çin'de geliştirilmiş bir tünelleme protokolü"},
            {"name": "v2ray", "description": "Trafiği çeşitli protokollerde gizleyerek DPI tarafından tespit edilmesini zorlaştıran bir tünelleme protokolü"},
            {"name": "wireguard", "description": "Modern ve güvenli bir tünelleme protokolü"},
            {"name": "tor", "description": "Anonim internet erişimi için kullanılan bir ağ"}
        ]

    def print_protocols(self):
        for protocol in self.protocols:
            print(f"Protocol: {protocol['name']}")
            print(f"Description: {protocol['description']}")
            print()

    def why_better_than_vpn(self):
        reasons = [
            "Gelişmiş trafik gizleme",
            "Yüksek güvenlik",
            "Topluluk odaklı",
            "Esneklik"
        ]
        for reason in reasons:
            print(f"- {reason}")

# Örnek kullanım
tunneling_protocols = TunnelingProtocols()
tunneling_protocols.print_protocols()
print("Neden Standart VPN'lerden Üstün:")
tunneling_protocols.why_better_than_vpn()
