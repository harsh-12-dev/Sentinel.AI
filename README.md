# Sentinel.AI 🛡️
### AI-Powered URL Threat Detection System

Sentinel.AI is a web-based security project that helps identify potentially malicious URLs. It analyses different URL and domain-level patterns, calculates a risk score, and classifies links based on their potential threat level.

I built this project to explore how machine learning and rule-based analysis can work together to detect suspicious links, especially URLs that may be used for phishing or online scams.

## What it does

- **URL Scanning:** Submit a URL and get its risk assessment.
- **Risk Classification:** Classifies URLs as LOW, SUSPICIOUS, or HIGH.
- **Domain Analysis:** Checks domain structure, suspicious subdomains, IP addresses and other unusual patterns.
- **Brand Impersonation Detection:** Checks for suspicious domains containing names of known brands.
- **ML-Based Prediction:** Uses a Random Forest model to estimate the probability of a URL being dangerous.
- **User Authentication:** Supports registration and login using password hashing and JWT authentication.
- **Scan History:** Stores previous scans so users can review their results later.

## Tech Stack

**Frontend**
- React
- JavaScript
- Vite
- Tailwind CSS
- Axios
- React Router

**Backend**
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Bcrypt

**Machine Learning**
- Scikit-learn
- Random Forest Classifier
- Pandas
- Joblib

## How it works

Sentinel.AI uses a combination of rule-based checks and machine learning.

1. The user submits a URL through the dashboard.
2. The backend analyses the URL and its domain structure.
3. It checks for suspicious keywords, unusual URL lengths, IP-based URLs, suspicious TLDs, excessive subdomains and possible brand impersonation.
4. The ML model generates a risk probability when its trained model files are available.
5. The risk engine combines the analysis results and calculates a final risk score.
6. The result is displayed on the dashboard along with the reasons behind the assessment.
7. Authenticated users can access their previous scan history.

The current risk engine uses a weighted ML signal alongside deterministic rule-based checks. It does not rely on the ML model alone.

## Project Structure

```text
Sentinel.AI/
│
├── ai_engine/
│   ├── domain_intelligence/
│   ├── risk_engine/
│   └── url_analysis/
│
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   └── v1/
│   ├── core/
│   ├── database/
│   └── main.py
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── api/
│       ├── pages/
│       └── assets/
│
├── ml/
│   ├── models/
│   ├── augment_data.py
│   ├── feature_extractor.py
│   ├── train_model.py
│   └── test_model.py
│
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/harsh-12-dev/Sentinel.AI.git

cd Sentinel.AI
```

### 2. Backend Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the backend dependencies:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv bcrypt PyJWT pandas scikit-learn joblib
```

### 3. Environment Variables

Create a `.env` file in the project root directory.

Add the following configuration:

```env
DATABASE_URL=your_postgresql_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Use your own PostgreSQL database URL and a secure secret key. Do not upload this file to GitHub.

### 4. Initialize the Database

After configuring PostgreSQL, run:

```bash
python -m backend.database.init_db
```

### 5. Start the Backend

From the project root:

```bash
uvicorn backend.main:app --reload
```

Backend API:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

Open the local URL shown in your terminal, usually:

```text
http://localhost:5173
```

## Machine Learning Model

The project includes a Random Forest training pipeline.

The feature extractor analyses URL characteristics such as:

- URL and domain length
- Number of dots, hyphens and slashes
- Special characters and digits
- HTTPS usage
- IP address patterns
- Number of subdomains
- Suspicious keywords
- URL shorteners

The training script uses the processed dataset at:

```text
data/processed/clean_urls.csv
```

The dataset is expected to contain `url` and `label` columns.

To train the model:

```bash
python ml/train_model.py
```

The trained model and feature names are saved under `ml/models/`.

**Note:** Dataset files and serialized model files are excluded from this repository through `.gitignore`. You will need to provide the dataset and train the model locally before using the ML prediction component. Without a trained model, the rule-based risk analysis can still run.

## Current Limitations

- Risk scores are indicators, not a guarantee that a website is safe or malicious.
- The system uses URL and domain patterns rather than a live browser or website-content inspection.
- ML predictions depend on the availability and quality of the trained model.
- The current frontend API configuration uses a local backend address.

## Future Improvements

Some areas I would like to work on next:

- Improve detection accuracy with more diverse URL datasets.
- Reduce false positives and false negatives.
- Add more advanced phishing detection techniques.
- Improve the dashboard and scan result visualization.
- Add more testing and performance evaluation.
- Make deployment and configuration easier.

## Author

**Harsh Verma**

GitHub: https://github.com/harsh-12-dev

---

*Sentinel.AI is a personal development project built to explore URL threat detection, machine learning, and web application security.*
