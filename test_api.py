from src.infrastructure.market_api import RTEApiAdapter
import os

def test_connection():
    print("--- Test de connexion API RTE France ---")
    
    # verif pas utiliser cache pour le test
    if os.path.exists("market_data_cache.json"):
        print("Suppression du cache local pour forcer un appel API réel...")
        os.remove("market_data_cache.json")
    
    adapter = RTEApiAdapter()
    
    # debug: vérif ID sont bien chargés
    print(f"DEBUG: Client ID chargé (tronqué) : '{adapter.client_id[:5]}...'")
    print(f"DEBUG: Secret ID chargé (tronqué) : '{adapter.client_secret[:5]}...'")
    
    if not adapter.client_id or not adapter.client_secret or "votre_id" in adapter.client_id:
        print("❌ Erreur : Identifiants non chargés ou encore à 'votre_id'. Vérifiez le fichier .env")
        return

    print("--- Début de l'appel ---")
    price = adapter.fetch_latest_market_price()
    
    if price:
        print(f" Succès ! Prix récupéré : {price:.2f} €/MWh")
    else:
        print("\n❌ Échec de la récupération du prix.")
        print("Vérifiez les points suivants :")
        print("1. Vos identifiants dans le fichier .env (pas d'espaces, pas de guillemets nécessaires).")
        print("2. Que votre application sur le portail RTE est bien 'Active' et abonnée à l'API 'Wholesale Market'.")
        print("3. Si une erreur 'Invalid Client' apparaît, essayez de regénérer votre Secret ID sur le portail.")

if __name__ == "__main__":
    test_connection()
