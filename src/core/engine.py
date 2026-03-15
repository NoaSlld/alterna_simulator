from dataclasses import dataclass
from typing import Dict, List

@dataclass
class SimulationResult:
    prix_revient_ht: float
    prix_vente_final_ht: float
    prix_vente_final_ttc: float
    nouvelle_marge: float
    tva_montant: float
    params: Dict[str, any]

class AlternaSourcingEngine:
    """Cœur de calcul de simulation d'offres."""
    
    @staticmethod
    def calculate_simulation(
        prix_gros: float,
        turpe: float,
        taxes_fix: float,
        tva_rate: float,
        marge_cible: float,
        maintien_prix: bool,
        prix_bloque_ttc: float = 247.0
    ) -> SimulationResult:
        
        prix_revient_ht = prix_gros + turpe + taxes_fix
        
        if maintien_prix:
            prix_vente_final_ttc = prix_bloque_ttc
            prix_vente_final_ht = prix_vente_final_ttc / (1 + tva_rate)
            nouvelle_marge = prix_vente_final_ht - prix_revient_ht
        else:
            nouvelle_marge = marge_cible
            prix_vente_final_ht = prix_revient_ht + nouvelle_marge
            prix_vente_final_ttc = prix_vente_final_ht * (1 + tva_rate)
            
        tva_montant = prix_vente_final_ht * tva_rate
        
        params = {
            "Prix de Gros": f"{prix_gros} EUR/MWh",
            "TURPE": f"{turpe} EUR/MWh",
            "Taxes (TICFE+CTA)": f"{taxes_fix} EUR/MWh",
            "TVA": f"{tva_rate*100:.0f} %",
            "Marge Cible": f"{marge_cible} EUR/MWh",
            "Maintien Prix": "Oui" if maintien_prix else "Non",
            "Prix Final (TTC)": f"{prix_vente_final_ttc:.2f} EUR/MWh",
            "Marge Réelle": f"{nouvelle_marge:.2f} EUR/MWh"
        }
        
        return SimulationResult(
            prix_revient_ht=prix_revient_ht,
            prix_vente_final_ht=prix_vente_final_ht,
            prix_vente_final_ttc=prix_vente_final_ttc,
            nouvelle_marge=nouvelle_marge,
            tva_montant=tva_montant,
            params=params
        )

    @staticmethod
    def get_bench_data(prix_alterna: float, competitors: Dict[str, float]) -> List[Dict]:
        """Prépare les données de comparaison."""
        data = [{"Fournisseur": "Alterna (Simulé)", "Prix TTC": prix_alterna}]
        for name, price in competitors.items():
            data.append({"Fournisseur": name, "Prix TTC": price})
        return data
