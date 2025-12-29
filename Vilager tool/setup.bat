@echo off
title Installation Villager Tool
echo [1/2] Verification de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH.
    pause
    exit
)

echo [2/2] Installation des bibliotheques...
pip install -r requirements.txt

echo.
echo [SUCCES] Environnement pret !
echo Lancez 'Vilager tool.py' pour commencer.
pause