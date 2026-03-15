import requests
import os
import json
import base64
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st

class RTEApiAdapter:
    """Adaptateur pour l'API RTE France (Réseau de Transport d'Électricité) avec cache persistant."""
    
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("EPEX_CLIENT_ID")
        self.client_secret = os.getenv("EPEX_CLIENT_SECRET")
        self.token_url = "https://digital.iservices.rte-france.com/token/oauth/"
        self.base_url = "https://digital.iservices.rte-france.com/open_api/wholesale_market/v3/france_power_exchanges"
        self.cache_file = "market_data_cache.json"

    def _get_token(self):
        """Récupère le token OAuth2 RTE via authentification Basic Base64."""
        if not self.client_id or not self.client_secret or "votre_id" in self.client_id:
            return None
            
        try:
            auth_str = f"{self.client_id}:{self.client_secret}"
            b64_auth = base64.b64encode(auth_str.encode()).decode()
            
            headers = {
                "Authorization": f"Basic {b64_auth}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            response = requests.post(self.token_url, headers=headers, data={"grant_type": "client_credentials"}, timeout=10)
            
            if response.status_code != 200:
                st.error(f"Erreur d'authentification RTE ({response.status_code})")
                return None
                
            return response.json().get("access_token")
        except Exception as e:
            st.error(f"Erreur technique lors de l'appel RTE : {e}")
            return None

    def fetch_latest_market_price(self):
        """Récupère le dernier prix Spot (Day-Ahead) via RTE avec cache persistant."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # vérif cache local
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
                    if cache.get("date") == today:
                        return cache.get("price")
            except Exception: pass

        # appel API
        token = self._get_token()
        if not token:
            return None

        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(self.base_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                exchanges = data.get("france_power_exchanges", [])
                
                for exchange in exchanges:
                    values = exchange.get("values", [])
                    if values:
                        # extrait les prix (€/MWh)
                        prices = [v.get("price") for v in values if v.get("price") is not None]
                        if prices:
                            avg_price = sum(prices) / len(prices)
                            
                            # mise à jour du cache local
                            with open(self.cache_file, 'w') as f:
                                json.dump({"date": today, "price": avg_price}, f)
                            return avg_price
            return None
        except Exception as e:
            st.warning(f"Impossible de rafraîchir le prix de marché : {e}")
            return None
