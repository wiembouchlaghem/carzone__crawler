# Carzone Crawler (Docker + Selenium)

Crawler simple et dockerisé pour extraire les pages HTML de carzone.ie.  
Les pages sont enregistrées dans un dossier local sous le format :

```
0001__used_cars.html
0002__used_cars.html
...
0200__used_cars.html
```

---

## 📂 Structure du projet

```
carzone-crawler/
├── Dockerfile
├── requirements.txt
├── README.md
└── crawler.py
```

---

## 🐳 1 — Build de l'image Docker

```bash
docker build -t carzone-crawler .
```

---

## 📁 2 — Créer le dossier de sortie

```bash
mkdir cars_list_200_output
```

---

## ▶️ 3 — Lancer le crawler

### 🔵 Sans proxy (test uniquement)

```bash
docker run \
  -v ${PWD}/cars_list_200_output:/app/cars_list_200_output \
  carzone-crawler
```

### 🟢 Avec proxy (recommandé pour carzone.ie)

```bash
docker run \
  -e PROXY_URL="http://USER:PASS@IP:PORT" \
  -v ${PWD}/cars_list_200_output:/app/cars_list_200_output \
  carzone-crawler
```

Exemple :

```bash
docker run \
  -e PROXY_URL="http://ikcaoxcx:xbn0e0v6mgpn@45.38.107.97:6014" \
  -v ${PWD}/cars_list_200_output:/app/cars_list_200_output \
  carzone-crawler
```

---

## 📦 Résultats

Les fichiers HTML apparaîtront dans :

```
cars_list_200_output/
   0001__used_cars.html
   0002__used_cars.html
   ...
   0200__used_cars.html
```

---

## ⚙️ Variables d'environnement

| Variable | Description |
|---|---|
| `PROXY_URL` | URL proxy HTTP/SOCKS (obligatoire pour Carzone) |
| `START` / `END` | Pages à scraper (fixées dans le script par défaut) |
| `MAX_ATTEMPTS` | Tentatives avant abandon |

---

## 🛡 Mesures anti-détection

- Chrome headless réel
- User-agent aléatoire
- `navigator.webdriver` désactivé
- Taille de fenêtre randomisée
- Délais naturalisés (`2–4 sec`)
- Retry automatique si CAPTCHA

---

## ❗ Note importante

Carzone utilise Cloudflare :
- ➡️ Les proxys gratuits / datacenter sont rejetés
- ➡️ Le scraper fonctionne, mais dépend uniquement du proxy utilisé
