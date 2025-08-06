# GE-Healthcare-Hackathon-PII

## Overview
This repository contains solutions for detecting and handling Personally Identifiable Information (PII) and Protected Health Information (PHI) in healthcare data. It includes models, rule-based approaches, and a web application for demonstration and testing.

## Project Structure
- `models/`: Machine learning and NLP models (DeBERTA, PHI, PII, QLoRA, rule-based, spacyNER, presidio)
- `multiprocessing/` & `multithreading/`: Parallel processing scripts
- `presentation/`: Project presentation
- `testing/`: Utility scripts and database tests
- `website/`: Web application (backend and frontend)
- `assets/`: Sample data and logs

## Setup
1. Clone the repository:
   ```powershell
   git clone https://github.com/kaushiksaravanan/GE-Healthcare-Hackathon-PII.git
   ```
2. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. (Optional) Install backend dependencies:
   ```powershell
   pip install -r website/backend/requirements.txt
   ```
4. (Optional) Install frontend dependencies:
   ```powershell
   cd website/frontend
   npm install
   ```

## Running Locally
### Backend
```powershell
python website/backend/app.py
```

### Frontend
```powershell
cd website/frontend
npm run dev
```


## Deployment (Render)
You can deploy both backend and frontend on Render:

1. Push your repository to GitHub (if not already).
2. Add the provided `render.yaml` to the root of your repository.
3. Go to [Render.com](https://render.com) and create a new "Blueprint" deployment, connecting your GitHub repo.
4. Render will automatically detect the `render.yaml` and set up both services:
   - **Frontend**: Vite app (`website/frontend`)
   - **Backend**: Python app (`website/backend`)
5. Set environment variables as needed (see `render.yaml`).
6. After deployment, update the frontend's `VITE_BACKEND_URL` to point to the backend service URL if needed.

For manual setup, you can also create two separate web services in Render:
- **Frontend**: Root directory `website/frontend`, build command `npm install && npm run build`, start command `npm run preview`.
- **Backend**: Root directory `website/backend`, build command `pip install -r requirements.txt`, start command `python app.py`.

See `render.yaml` for details.

## License
See `LICENSE` for details.