import requests
import csv
import json
import argparse
import logging
from datetime import datetime
import sys
import os

def setup_logging():
    """Konfiguruje system logowania, tworząc katalog 'log'."""
    log_dir = "log"
    # Sprawdzenie i utworzenie katalogu 'log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"INFO: Utworzono katalog na logi: {os.path.abspath(log_dir)}")
    
    log_filename = os.path.join(log_dir, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] - %(message)s",
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def clean_logs():
    """Usuwa wszystkie pliki z katalogu 'log'."""
    log_dir = "log"
    if not os.path.isdir(log_dir):
        print(f"INFO: Katalog '{log_dir}' nie istnieje. Nie ma nic do usunięcia.")
        return
    
    log_files = [f for f in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, f))]
    
    if not log_files:
        print(f"INFO: Katalog '{log_dir}' jest pusty.")
        return
        
    print(f"Znaleziono {len(log_files)} plików logów do usunięcia. Czy na pewno chcesz kontynuować? [t/n]")
    choice = input().lower()
    
    if choice == 't':
        for filename in log_files:
            try:
                file_path = os.path.join(log_dir, filename)
                os.remove(file_path)
                print(f"Usunięto: {filename}")
            except Exception as e:
                print(f"Błąd podczas usuwania pliku {filename}: {e}")
        print("Sukces! Wszystkie pliki logów zostały usunięte.")
    else:
        print("Anulowano operację.")

def load_config(config_path):
    # ... (bez zmian)
    if not os.path.exists(config_path):
        logging.error(f"Plik konfiguracyjny nie został znaleziony: {config_path}")
        sys.exit(1)
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        logging.error(f"Błąd dekodowania pliku JSON. Sprawdź poprawność składni w {config_path}")
        sys.exit(1)

def get_invoice_pdf(invoice_number, config):
    # ... (poprawiona ścieżka zapisu)
    api_token = config.get("api_token")
    subdomain = config.get("fakturownia_subdomain")
    base_url = f"https://{subdomain}.fakturownia.pl"
    
    download_dir = "download"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        logging.info(f"Utworzono katalog na pobrane pliki: {os.path.abspath(download_dir)}")

    logging.info(f"Rozpoczynam wyszukiwanie faktury o numerze: {invoice_number}")
    
    try:
        search_params = {'api_token': api_token, 'q': invoice_number}
        response = requests.get(f"{base_url}/invoices.json", params=search_params)
        response.raise_for_status()
        
        invoices = response.json()
        if not invoices:
            logging.warning(f"Nie znaleziono faktury o numerze: {invoice_number}")
            return
            
        invoice_id = invoices[0].get('id')
        logging.info(f"Znaleziono fakturę. ID: {invoice_id}")
        
        pdf_params = {'api_token': api_token}
        pdf_response = requests.get(f"{base_url}/invoices/{invoice_id}.pdf", params=pdf_params)
        pdf_response.raise_for_status()
        
        safe_filename = invoice_number.replace('/', '-') + ".pdf"
        save_path = os.path.join(download_dir, safe_filename)
        with open(save_path, 'wb') as f:
            f.write(pdf_response.content)
        logging.info(f"Sukces! Faktura została zapisana do pliku: {save_path}")
        
    except requests.exceptions.RequestException as e:
        logging.critical(f"Krytyczny błąd połączenia z API: {e}")
    except Exception as e:
        logging.error(f"Wystąpił nieoczekiwany błąd podczas pobierania PDF: {e}")

def import_invoices_from_csv(csv_path, config):
    # ... (bez zmian)
    try:
        with open(csv_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            logging.info(f"Rozpoczynam przetwarzanie pliku {csv_path}...")
            for row in reader:
                create_cost_invoice(row, config)
            logging.info("Zakończono przetwarzanie pliku.")
    except FileNotFoundError:
        logging.error(f"Plik CSV nie został znaleziony: {csv_path}")
    except Exception as e:
        logging.error(f"Wystąpił nieoczekiwany błąd podczas przetwarzania pliku CSV: {e}")


def create_cost_invoice(invoice_data, config):
    # ... (bez zmian)
    api_token = config.get("api_token")
    api_url = f"https://{config.get('fakturownia_subdomain')}.fakturownia.pl/invoices.json"
    your_company_details = config.get("company_details", {})

    position = {
        "name": invoice_data.get("position_name"), "quantity": invoice_data.get("quantity", 1),
        "total_price_gross": invoice_data.get("total_price_gross"), "price_net": invoice_data.get("price_net"),
        "tax": invoice_data.get("tax")
    }
    
    payload = {
        "api_token": api_token, "invoice": {
            "kind": "cost", "number": invoice_data.get("invoice_ref"), "issue_date": invoice_data.get("issue_date"),
            "sell_date": invoice_data.get("sell_date"), "payment_to": invoice_data.get("payment_to"),
            "seller_name": invoice_data.get("buyer_name"), "seller_tax_no": invoice_data.get("buyer_tax_no"),
            "seller_street": invoice_data.get("buyer_street"), "seller_city": invoice_data.get("buyer_city"),
            "seller_post_code": invoice_data.get("buyer_post_code"), "buyer_name": your_company_details.get("name"),
            "buyer_tax_no": your_company_details.get("tax_no"), "buyer_street": your_company_details.get("street"),
            "buyer_city": your_company_details.get("city"), "buyer_post_code": your_company_details.get("post_code"),
            "positions": [position], "description": invoice_data.get("notes")
        }
    }
    payload["invoice"]["positions"][0] = {k: v for k, v in payload["invoice"]["positions"][0].items() if v is not None and v != ''}

    try:
        logging.info(f"Próba utworzenia faktury: {payload['invoice']['number']}...")
        response = requests.post(api_url, json=payload)

        if response.status_code == 201:
            logging.info(f"✅ Sukces! Faktura {invoice_data.get('invoice_ref')} została pomyślnie utworzona.")
        else:
            error_message = json.dumps(response.json(), indent=2, ensure_ascii=False)
            logging.error(f"Błąd! Nie udało się utworzyć faktury {invoice_data.get('invoice_ref')}.")
            logging.error(f"Status: {response.status_code}")
            logging.error(f"Treść błędu: {error_message}")
    except requests.exceptions.RequestException as e:
        logging.critical(f"Krytyczny błąd połączenia z API: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Importer i menedżer faktur dla Fakturowni.")
    parser.add_argument("--config", default="config.json", nargs="?", help="Ścieżka do pliku konfiguracyjnego (domyślnie: config.json).")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--csv", help="Ścieżka do pliku CSV w celu importu faktur.")
    group.add_argument("--get-invoice", help="Numer faktury do pobrania w formacie PDF.")
    group.add_argument("--clean-logs", action="store_true", help="Usuwa wszystkie pliki z katalogu log.")
    
    args = parser.parse_args()
    
    if args.clean_logs:
        clean_logs()
    else:
        # Uruchom logowanie tylko dla operacji importu lub pobierania
        setup_logging()
        config = load_config(args.config)
        
        if args.csv:
            import_invoices_from_csv(args.csv, config)
        elif args.get_invoice:
            get_invoice_pdf(args.get_invoice, config)