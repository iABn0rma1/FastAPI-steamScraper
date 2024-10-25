# FastAPI Steam Scraper

A web application that scrapes and displays discounted Steam games using FastAPI.
[Click here for Live demo.](https://vercel.com/iabn0rma1s-projects)

## Objectives

- [x] Scraping discounted games from the Steam store.
- [x] Creating an API to serve game data.
- [ ] Building Backend for user data management.
- [ ] Automated mailing on price updates.

---

## Installation

### Prerequisites

- [Python3](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

### Clone the Repository

```bash
git clone https://github.com/iABn0rma1/FastAPI-steamScraper.git
cd FastAPI-steamScraper
```

### Install Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required dependencies.

```bash
pip install -r requirements.txt
```

### Run the Application

To start the FastAPI server, run the following command:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Visit `localhost:8000/` in your browser.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your proposed changes.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
