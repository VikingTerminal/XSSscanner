import sys
import time
from bs4 import BeautifulSoup
import requests
from colorama import init, Fore

init(autoreset=True)

def print_magenta_with_typing_effect(text):
    for char in text:
        sys.stdout.write(Fore.MAGENTA + char)
        sys.stdout.flush()
        time.sleep(0.01)  
    print()  

def print_cyan_with_typing_effect(text):
    for char in text:
        sys.stdout.write(Fore.CYAN + char)
        sys.stdout.flush()
        time.sleep(0.05)  
    print()  

def find_xss_vulnerabilities(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        
        vulnerable_tags = soup.find_all(['script', 'iframe', 'input', 'a', 'img', 'form', 'textarea', 'div', 'span', 'button', 'select', 'label', 'link', 'style', 'table', 'tr', 'td', 'th', 'nav', 'header', 'footer', 'article'])
        found_vulnerabilities = False
        for tag in vulnerable_tags:
            if tag.string and any(xss_keyword in tag.string for xss_keyword in ['<script>', 'javascript:', 'onerror=', 'eval(', 'document.cookie']):
                print_magenta_with_typing_effect("Potenziale vulnerabilità XSS trovata nel tag: " + tag.name)
                print_magenta_with_typing_effect("Contenuto del tag: " + tag.string.strip())
                print_magenta_with_typing_effect("Posizione nel documento: " + str(soup.get_text().find(tag.string.strip())))
                print_magenta_with_typing_effect("Linea nel documento: " + str(soup.get_text().count('\n', 0, soup.get_text().find(tag.string.strip())) + 1))
                print_magenta_with_typing_effect("---------------")
                found_vulnerabilities = True
        
        if not found_vulnerabilities:
            print_cyan_with_typing_effect("Nessuna potenziale vulnerabilità XSS trovata.")
    except requests.RequestException as e:
        print(Fore.RED + "Errore durante la richiesta HTTP:", e)

print(Fore.RED + "█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
print(Fore.RED + "█░░╦─╦╔╗╦─╔╗╔╗╔╦╗╔╗░░█")
print(Fore.RED + "█░░║║║╠─║─║─║║║║║╠─░░█")
print(Fore.RED + "█░░╚╩╝╚╝╚╝╚╝╚╝╩─╩╚╝░░█")
print(Fore.RED + "█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")

def main():
    print_cyan_with_typing_effect("Grazie per aver provato questo tool. Visita t.me/VikingTERMINAL per provare altre utility.\n")

    while True:
        url = input(Fore.YELLOW + "Inserisci il link da analizzare (scrivi 'exit' per uscire): ")
        if url.lower() == 'exit':
            print_cyan_with_typing_effect("Grazie per aver provato questo tool. Visita t.me/VikingTERMINAL per provare altre utility.\n")
            break
        find_xss_vulnerabilities(url)

if __name__ == "__main__":
    main()
