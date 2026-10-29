Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "    Smart Campus Explorer AI - Streamlit Launcher" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Cyan

$pythonExe = ".venv\Scripts\python.exe"
if (-Not (Test-Path $pythonExe)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    & "C:\Users\user\.local\bin\uv.exe" venv --python "C:\Users\user\.local\bin\python3.11.exe" .venv
    & "C:\Users\user\.local\bin\uv.exe" pip install --link-mode=copy --python .venv\Scripts\python.exe -r requirements.txt
}

& .venv\Scripts\streamlit.exe run app.py
