# GE-Healthcare-Hackathon-PII

## Overview
A practical solution for detecting and handling Personally Identifiable Information (PII) and Protected Health Information (PHI) in healthcare data. This project combines machine learning, rule-based methods, and a web app for easy testing and demonstration.

## Project Structure
- `models/`: NLP models (DeBERTA, PHI, PII, QLoRA, rule-based, spaCyNER, presidio)
- `multiprocessing/` & `multithreading/`: Parallel processing scripts
- `presentation/`: Project slides
- `testing/`: Utility scripts and database tests
- `website/`: Web app (backend & frontend)
- `assets/`: Sample data and logs

## Quick Start
1. Clone the repo:
   ```powershell
   git clone https://github.com/kaushiksaravanan/GE-Healthcare-Hackathon-PII.git
   ```
2. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. (Optional) Backend dependencies:
   ```powershell
   pip install -r website/backend/requirements.txt
   ```
4. (Optional) Frontend dependencies:
   ```powershell
   cd website/frontend
   npm install
   ```

## Run Locally
- **Backend:**
  ```powershell
  python website/backend/app.py
  ```
- **Frontend:**
  ```powershell
  cd website/frontend
  npm run dev
  ```

# GE Healthcare Hackathon Finals

## Top 12 Team: Sliverine Artana

Welcome! This project was selected as a top 12 finalist in the GE Healthcare Hackathon.

## Precision Healthcare Challenge
Built for the Precision Healthcare Challenge, our goal is to make healthcare data safer and smarter by detecting and protecting sensitive information.

### What We Did
- Used Indian language datasets for multilingual NER
- Fine-tuned models like DeBERTA and BERT
- Added spaCy and rule-based methods for extra coverage
- Evaluated with seqeval for reliable metrics
- Designed everything to be modular and easy to extend

### Main Folders
- `models/` - Model code and training scripts
- `assets/` - Sample data and logs
- `website/` - Web app (backend & frontend)
- `presentation/` - Slides and materials
- `PII Fine tuning.ipynb` - Main notebook for data and training

### How to Use
1. Install dependencies
2. Run `PII Fine tuning.ipynb` for data and training
3. Try out model scripts in `models/`
4. Launch the web app in `website/`

### Team
- Sliverine Artana

### License
See `LICENSE` for details.

---
Questions or want to collaborate? Open an issue in this repo!