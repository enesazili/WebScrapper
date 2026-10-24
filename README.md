# WebScrapper 🐍

A Python-based web scraping project designed to search for products and retrieve price information from Trendyol and Amazon Türkiye.

## Features

- 🔎 Search for products by name
- 🛒 Retrieve product information from supported shopping websites
- 💰 Collect product prices for comparison
- 🐳 Run the application in a Docker container
- ⚙️ Simple command-line interface

## Tech Stack

- **Language:** Python
- **HTTP Requests:** Requests
- **HTML Parsing:** Beautiful Soup 4
- **Containerization:** Docker

## Requirements

- Docker Desktop or Docker Engine

Alternatively, you can run the script directly with Python.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/WebScrapper.git
cd WebScrapper
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Build the Docker image

```bash
docker build -t webscrapper .
```

### 3. Run the application

```bash
docker run -it --rm webscrapper
```

Enter the product name when prompted by the application.

## Run Without Docker

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the scraper:

```bash
python webscrapper.py
```

## Project Structure

```text
WebScrapper/
├── webscrapper.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Notes

- Website layouts and HTML structures may change, which can affect scraping results.
- Some websites may restrict automated requests or return HTTP 403 responses.
- Results depend on website accessibility and the scraper's current implementation.

## Disclaimer

This project is intended for educational and personal use. Please respect the terms of service of the websites you access and their applicable policies.

## License

No license has been specified yet.

---

*Built with Python and Docker.*
