# Faktury

## Opis
Projekt służy do zarządzania fakturami w systemie Fakturownia. Umożliwia import faktur z pliku CSV, pobieranie faktur w formacie PDF oraz zarządzanie logami.

## Wymagania
- Python 3.8 lub nowszy
- Biblioteki wymienione w `requirements.txt`

## Instalacja
1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/mprse/faktury.git
   ```
2. Przejdź do katalogu projektu:
   ```bash
   cd faktury
   ```
3. Zainstaluj wymagane biblioteki:
   ```bash
   pip install -r requirements.txt
   ```

## Konfiguracja
Plik konfiguracyjny `config.json` powinien zawierać dane takie jak:
- `api_token`: Token API do autoryzacji w systemie Fakturownia.
- `fakturownia_subdomain`: Subdomena konta w Fakturowni.
- `company_details`: Szczegóły firmy (nazwa, NIP, adres).

Przykład pliku `config.json`:
```json
{
  "api_token": "your_api_token",
  "fakturownia_subdomain": "your_subdomain",
  "company_details": {
    "name": "Twoja Firma",
    "tax_no": "1234567890",
    "street": "ul. Przykładowa 1",
    "city": "Miasto",
    "post_code": "00-000"
  }
}
```

## Użycie
### Import faktur z pliku CSV
Uruchom skrypt z opcją `--csv` i podaj ścieżkę do pliku CSV:
```bash
python fakapp.py --csv sample.csv
```

### Pobieranie faktury w formacie PDF
Uruchom skrypt z opcją `--get-invoice` i podaj numer faktury:
```bash
python fakapp.py --get-invoice INV-2025-001
```

### Czyszczenie logów
Uruchom skrypt z opcją `--clean-logs`:
```bash
python fakapp.py --clean-logs
```

## Przykładowe wywołania
### Import faktur z pliku CSV
```bash
python fakapp.py --csv invoices.csv
```

### Pobieranie faktury w formacie PDF
```bash
python fakapp.py --get-invoice INV-2025-002
```

### Czyszczenie logów
```bash
python fakapp.py --clean-logs
```

## Przykład
```
PS C:\src\faktury> python .\fakapp.py --csv sample.csv
INFO: Utworzono katalog na logi: C:\src\faktury\log
2025-09-22 20:47:37,671 [INFO] - Rozpoczynam przetwarzanie pliku sample.csv...
2025-09-22 20:47:37,672 [INFO] - Próba utworzenia faktury: INV-2025-001...
2025-09-22 20:47:38,091 [INFO] - Sukces! Faktura INV-2025-001 została pomyślnie utworzona.
2025-09-22 20:47:38,093 [INFO] - Próba utworzenia faktury: INV-2025-002...
2025-09-22 20:47:38,500 [INFO] - Sukces! Faktura INV-2025-002 została pomyślnie utworzona.
2025-09-22 20:47:38,501 [INFO] - Zakończono przetwarzanie pliku.
PS C:\src\faktury> python .\fakapp.py --get-invoice "INV-2025-001"
2025-09-22 20:47:41,438 [INFO] - Utworzono katalog na pobrane pliki: C:\src\faktury\download
2025-09-22 20:47:41,438 [INFO] - Rozpoczynam wyszukiwanie faktury o numerze: INV-2025-001
2025-09-22 20:47:41,646 [INFO] - Znaleziono fakturę. ID: 418903747
2025-09-22 20:47:42,532 [INFO] - Sukces! Faktura została zapisana do pliku: download\INV-2025-001.pdf
```

## Licencja
Projekt jest dostępny na licencji MIT.
