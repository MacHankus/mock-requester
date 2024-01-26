# Cel serwisu
Celem serwisu jest odbiberanie i wysyłanie predefiniowanych requestów

# Instrukcja użycia 
Głównym punktem użytkownia aplikacji jest plik config.yaml - zmienna `CONFIG_FILE_PATH` przechowuje ścieżkę do pliku konfiguracyjnego.
Plik konfiguracyjny składa się z segmenów 
```
mock-external-weight-api: # Nazwa bloku dla lepszej orientacji - bloków może być wiele
  incoming: 
    type: http
    path: start_weighing # ścieżka, pod którą aplikacja ma nasłuchiwać bez poprzedzającego slasha np. start_weighing - aplikacja będzie nasłuchiwać pod [POST] http://localhost:9050/start_weighing
  outcoming: # lista wychodzących requestów - można zdefiniować ich wiele
    type: http
    url: "http://localhost:9006/weighting" # url na który ma zostać wysłany request
    method: post # post, get albo put
    payload: # payload jest dowolnym dictem/mapą
      id_route: ${idRoute} # w payloadzi można używać zmiennych odnoszących się do body, które aplikacja odebrała
      type_route: ${typeRoute}
      result: 1
      weight: 4
    headers: 
      Content-Type: application/json

```
Powyżej został opisany plik konfiguracyjny.

Ważniejsze kwestie:
- sekcja outcoming może przechowywać tablicę, więc requestów można wysłać więcej niż 1
- sekcja payload może zawierać słownik z wartościami, które odnoszą się do body , które aplikacja otrzymała, czyli kiedy do aplikacji wysłany jest payload : {"key": "SECRET"}, to można podać w payloadzie outcoming :
    ```
        payload: 
        name: Random_name
        key: ${key}
    ```
    wówczas zostanie wysłany request z payloadem 
    ```
    {
        "name": "Random_name", 
        "key" : "SECRET"
    }
    ```