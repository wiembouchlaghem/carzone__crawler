# 🚗 Carzone Crawler

A simple Docker + Selenium crawler that extracts used car listing pages from [carzone.ie](https://www.carzone.ie) and saves them as local HTML files for offline processing or analysis.

Each page is saved in the format:

```
0001__used_cars.html
0002__used_cars.html
...
0200__used_cars.html
```

---

## 📁 Repository Structure

```
carzone-crawler/
├── Dockerfile
├── requirements.txt
├── crawler.py
└── README.md
```

---

## 🐳 Setup & Usage

### 1. Build the Docker image

```bash
docker build -t carzone-crawler .
```

### 2. Create the output folder

```bash
mkdir cars_list_200_output
```

### 3. Run the crawler

**Without proxy**

```bash
docker run \
  -v ${PWD}/cars_list_200_output:/app/cars_list_200_output \
  carzone-crawler
```

**With proxy**

```bash
docker run \
  -e PROXY_URL="http://USER:PASS@IP:PORT" \
  -v ${PWD}/cars_list_200_output:/app/cars_list_200_output \
  carzone-crawler
```

---

## ⚙️ Environment Variables

| Variable    | Description                                      | Required |
|-------------|--------------------------------------------------|----------|
| `PROXY_URL` | HTTP/SOCKS proxy (e.g. `http://user:pass@ip:port`) | No, but recommended |

---

## 📦 Output

Scraped pages are saved in the mounted folder:

```
cars_list_200_output/
├── 0001__used_cars.html
├── 0002__used_cars.html
└── ...
```

