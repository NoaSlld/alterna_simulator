# Simulateur d'Offres - Alterna Énergie

Bienvenue dans l'outil de simulation interactif fait pour Alterna Énergie. Ce tableau de bord permet de comprendre comment les variations des prix du marché de l'électricité impactent les offres d'énergie et la rentabilité de l'entreprise.

---

## Comment lancer l'application ?

Le lancement a été simplifié par un script automatique. Suivez ces étapes :

### 1. Ouvrir le Terminal
Sur votre Mac, appuyez sur les touches `Commande (⌘) + Espace`, tapez **Terminal** et appuyez sur `Entrée`.

### 2. Se placer dans le bon dossier
Allez dans le dossier du projet :
```bash
cd /xx/xx/alterna_simulator/
```

## Installation et Lancement

1. **Configuration des identifiants API** :
   - Ouvrez le fichier `.env` à la racine.
   - Remplissez vos clés `EPEX_CLIENT_ID` et `EPEX_CLIENT_SECRET` obtenues sur le portail [RTE Data France](https://data.rte-france.com/).
   - Assurez-vous d'être abonné à l'API **Wholesale Market v3**.

2. **Lancer le simulateur** :
   ```bash
   bash run.sh
   ```

## Intégration API Marché (RTE)

Le simulateur est connecté en temps réel aux données de **RTE France** pour récupérer les prix Spot (Day-Ahead).

- **Pré-remplissage automatique** : Au lancement, le curseur "Prix de Gros" se cale sur la dernière valeur moyenne du marché.
- **Cache Persistant** : Pour économiser votre quota d'appels, l'application stocke le prix dans un fichier `market_data_cache.json`. Elle ne fait qu'un seul appel par jour.
- **Sécurité** : Vos identifiants sont protégés via le fichier `.env`.

## Fonctionnalités du Dashboard
**Que va-t-il se passer ?**
- Lors du premier lancement, le script va préparer un environnement sécurisé pour Python et installer les outils nécessaires (Streamlit, Pandas, Plotly).
- Ensuite, une page internet s'ouvrira automatiquement dans votre navigateur par défaut avec le Dashboard interactif.

---

## Comment utiliser le Dashboard ?

### 1. Volet Pédagogique (Graphique Circulaire)
Ce graphique montre exactement de quoi se compose l'offre pour 1 MWh :
- **Part Énergie** : Prix d'achat sur le marché de gros.
- **Acheminement** : Coûts fixes pour transporter l'électricité (réseaux Enedis/RTE).
- **Taxes** : Les parts obligatoires prélevées par l'État.
- **Marge** : Ce qui revient réellement à Alterna.

### 2. Le Stress Test (Barre Latérale à gauche)
Utilisez les curseurs pour simuler des crises ou des changements :
- **Variation du Prix de Gros** : Simulez une hausse (ex: +30% suite à une crise géopolitique).
- **Variation de la TICFE** : Simulez une hausse des taxes gouvernementales.
- **Option Stratégique** : Cochez "Maintenir le prix de vente" pour voir comment Alterna perd de la marge si elle refuse d'augmenter ses tarifs clients malgré la hausse des coûts.

### 3. Benchmark Concurrentiel
Comparez instantanément le prix simulé d'Alterna avec les tarifs actuels d'**EDF**, **Engie** et **TotalEnergies**. Un indicateur vous dira si vous êtes "Leader Prix", "Compétitif" ou "Hors Marché".

---

## Informations Techniques
- **Langage** : Python
- **Interface** : Streamlit
- **Données** : Modélisation basée sur les structures de coûts types du marché français du détail.
