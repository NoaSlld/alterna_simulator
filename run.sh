#!/bin/bash
echo "Création de l'environnement virtuel..."
python3 -m venv venv
source venv/bin/activate

echo "Installation des dépendances..."
pip install -r requirements.txt

echo "Lancement du Dashboard Streamlit..."
streamlit run app.py
