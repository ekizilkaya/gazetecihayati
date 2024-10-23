import gradio as gr
import random
import os
from colorama import init, Fore, Back, Style

# Initialize colorama for colored text
init(autoreset=True)

class Gazeteci:
    def __init__(self):
        self.aboneler = 50
        self.reklamcilar = 50
        self.itibar = 50
        self.yasal_durum = 50
        self.tur = 1
        self.skor = 0

    def durum_guncelle(self, aboneler, reklamcilar, itibar, yasal_durum):
        self.aboneler += aboneler
        self.reklamcilar += reklamcilar
        self.itibar += itibar
        self.yasal_durum += yasal_durum

        self.aboneler = min(max(self.aboneler, 0), 100)
        self.reklamcilar = min(max(self.reklamcilar, 0), 100)
        self.itibar = min(max(self.itibar, 0), 100)
        self.yasal_durum = min(max(self.yasal_durum, 0), 100)

        self.skor += sum([aboneler, reklamcilar, itibar, yasal_durum])

    def oyun_bitti_mi(self):
        return self.yasal_durum <= 0 or any(stat <= 0 for stat in [self.aboneler, self.reklamcilar, self.itibar])

def temizle_ekran():
    os.system('cls' if os.name == 'nt' else 'clear')

def durum_yazdir(gazeteci):
    temizle_ekran()
    print(f"\n{Fore.YELLOW}Ay {gazeteci.tur}")
    print(f"{Fore.CYAN}Aboneler: {Fore.WHITE}{gazeteci.aboneler}")
    print(f"{Fore.CYAN}Reklamverenler: {Fore.WHITE}{gazeteci.reklamcilar}")
    print(f"{Fore.CYAN}İtibarınız: {Fore.WHITE}{gazeteci.itibar}")
    print(f"{Fore.CYAN}Yasal Durum: {Fore.WHITE}{gazeteci.yasal_durum}")
    print(f"{Fore.CYAN}Skor: {Fore.WHITE}{gazeteci.skor}")

def baslik_ekrani():
    temizle_ekran()
    print(Fore.GREEN + """\n
╔═══════════════════════════════════════════════╗
║                                               ║
║              GAZETECİ HAYATI              ║
║                                               ║
╚═══════════════════════════════════════════════╝
""")
    print(Fore.YELLOW + "Oyun Talimatları:")
    print(Fore.WHITE + """\n
1. Gazeteci Hayatı'na hoş geldiniz! Bu oyunda Türkiye'de bir gazetecisiniz.
2. Medya kuruluşunuzu yürütürken kararlarınızla gazetecilik kariyerinize de yön vereceksiniz.
3. Bir yandan okurlarınızı, bir yandan reklamverenleri düşünerek gelir durumunuzu iyi ayarlamalısınız. Markanızın itibarının sıfırlanmasına izin vermemeli, ancak haberlerinizle artabilecek hapis riskini de iyi yönetmelisiniz.
4. Başarısız olursanız şirketiniz iflas edebilir, marka değeriniz sıfırlanabilir veya tutuklanabilirsiniz! Bakalım Türkiye medyasında kaç ay dayanabileceksiniz.

İyi şanslar!
""")
    input(Fore.GREEN + "Başlamak için Enter'a basın...")

def oyun_sonu_ekrani(gazeteci):
    temizle_ekran()
    print(Fore.RED + """\n
╔═══════════════════════════════════════════════╗
║                                               ║
║                  OYUN BİTTİ!                 ║
║                                               ║
╚═══════════════════════════════════════════════╝
""")
    print(f"{Fore.YELLOW}Toplam Tur: {Fore.WHITE}{gazeteci.tur}")
    print(f"{Fore.YELLOW}Final Skor: {Fore.WHITE}{gazeteci.skor}")

    if gazeteci.yasal_durum <= 0:
        print(f"{Fore.RED}Maalesef tutuklandınız ve hapse girdiniz.")
    elif gazeteci.aboneler <= 0:
        print(f"{Fore.RED}Aboneleriniz kalmadı ve gazeteniz kapandı.")
    elif gazeteci.reklamcilar <= 0:
        print(f"{Fore.RED}Reklamverenleriniz kalmadı ve gazeteniz iflas etti.")
    elif gazeteci.itibar <= 0:
        print(f"{Fore.RED}İtibarınız sıfırlandı ve kariyeriniz sona erdi.")
    else:
        print(f"{Fore.GREEN}Tebrikler! {gazeteci.tur} ay boyunca gazetecilik yaptınız ve emekli oldunuz.")

def senaryo_al():
    senaryolar = [
        {
            "prompt": "Hükûmetin tartışmalı bir kararı hakkında haber yapmak istiyorsunuz. Ne yaparsınız?",
            "options": [
                {"text": "Eleştirel bir haber yaz", "effects": (5, -5, 10, -15)},
                {"text": "Tarafsız bir şekilde rapor et", "effects": (0, 0, 5, -5)}
            ]
        },
        # ... rest of the scenarios
    ]

    return random.choice(senaryolar)

def oyunu_oyna():
    while True:
        baslik_ekrani()
        gazeteci = Gazeteci()

        while not gazeteci.oyun_bitti_mi():
            durum_yazdir(gazeteci)
            senaryo = senaryo_al()
            print(f"\n{Fore.MAGENTA}{senaryo['prompt']}")

            for i, option in enumerate(senaryo['options'], 1):
                print(f"{Fore.YELLOW}{i}. {Fore.WHITE}{option['text']}")

            secim = int(input(f"{Fore.GREEN}Seçiminizi yapın (1 veya 2): ")) - 1
            etkiler = senaryo['options'][secim]['effects']
            gazeteci.durum_guncelle(*etkiler)
            gazeteci.tur += 1

        oyun_sonu_ekrani(gazeteci)

        tekrar_oyna = input(f"{Fore.GREEN}Tekrar oynamak ister misiniz? (E/H): ").lower()
        if tekrar_oyna != 'e':
            print(f"{Fore.YELLOW}Oynadığınız için teşekkürler! Hoşça kalın!")
            break

if __name__ == "__main__":
    oyunu_oyna()

# Gradio interface
def gradio_game(choice):
    # Simulate a game turn based on the user's choice
    gazeteci = Gazeteci()  # Create a new journalist instance for each game
    senaryo = senaryo_al()  # Get a random scenario

    # Update the journalist's status based on the choice
    etkiler = senaryo['options'][choice]['effects']
    gazeteci.durum_guncelle(*etkiler)
    gazeteci.tur += 1

    # Generate a text-based output summarizing the game state
    output_text = f"Yeni durumunuz:\nAboneler: {gazeteci.aboneler}\nReklamverenler: {gazeteci.reklamcilar}\nİtibarınız: {gazeteci.itibar}\nYasal Durum: {gazeteci.yasal_durum}"

    return output_text

# Create the Gradio interface
iface = gr.Interface(
    fn=gradio_game,
    inputs=gr.Dropdown(["Option 1", "Option 2", "Option 3"]),  # Replace with actual options
    outputs="text"
)

iface.launch()