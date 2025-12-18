# 🧪 Exemples de Transactions pour Tests et Démonstration

Ce document contient des exemples de transactions pour tester et présenter le système de détection de fraude.

## Table des Matières
1. [Transactions Légitimes](#transactions-légitimes)
2. [Transactions Frauduleuses](#transactions-frauduleuses)
3. [Guide d'Utilisation](#guide-dutilisation)

---

## Transactions Légitimes

### 1. Achat Normal en Épicerie 🛒

**Description**: Transaction typique d'épicerie locale, montant habituel, appareil connu.

**Payload JSON**:
```json
{
  "transaction_hour": 14,
  "day_of_week": 2,
  "age": 35,
  "gender": "F",
  "home_country": "US",
  "transaction_country": "US",
  "merchant_category": "grocery",
  "merchant_base_risk": 0.05,
  "transaction_type": "in_store",
  "card_type": "Visa",
  "device": "pos_terminal",
  "amount": 45.80,
  "avg_30d_amount": 50.00,
  "previous_transactions_24h": 1,
  "last_hour_transactions": 0,
  "balance": 2500.00,
  "ip_risk_score": 10.5,
  "is_foreign": 0,
  "device_mismatch": 0,
  "location_change": 0,
  "amount_anomaly": -0.08,
  "hour_anomaly": 0
}
```

**Résultat Attendu**: ✅ Transaction Sûre (Probabilité < 5%)

---

### 2. Achat en Ligne - Électronique 💻

**Description**: Achat d'un ordinateur portable en ligne, montant élevé mais client régulier.

**Payload JSON**:
```json
{
  "transaction_hour": 20,
  "day_of_week": 5,
  "age": 28,
  "gender": "M",
  "home_country": "FR",
  "transaction_country": "FR",
  "merchant_category": "electronics",
  "merchant_base_risk": 0.12,
  "transaction_type": "online",
  "card_type": "Mastercard",
  "device": "desktop",
  "amount": 899.99,
  "avg_30d_amount": 120.00,
  "previous_transactions_24h": 2,
  "last_hour_transactions": 0,
  "balance": 4500.00,
  "ip_risk_score": 15.0,
  "is_foreign": 0,
  "device_mismatch": 0,
  "location_change": 0,
  "amount_anomaly": 0.45,
  "hour_anomaly": 0
}
```

**Résultat Attendu**: ✅ Transaction Sûre (Probabilité 10-20%)

---

### 3. Restaurant en Soirée 🍽️

**Description**: Dîner au restaurant avec des amis, heure normale.

**Payload JSON**:
```json
{
  "transaction_hour": 19,
  "day_of_week": 6,
  "age": 42,
  "gender": "M",
  "home_country": "CM",
  "transaction_country": "CM",
  "merchant_category": "restaurants",
  "merchant_base_risk": 0.08,
  "transaction_type": "in_store",
  "card_type": "Visa",
  "device": "pos_terminal",
  "amount": 85.50,
  "avg_30d_amount": 65.00,
  "previous_transactions_24h": 0,
  "last_hour_transactions": 0,
  "balance": 1800.00,
  "ip_risk_score": 8.5,
  "is_foreign": 0,
  "device_mismatch": 0,
  "location_change": 0,
  "amount_anomaly": 0.12,
  "hour_anomaly": 0
}
```

**Résultat Attendu**: ✅ Transaction Sûre (Probabilité < 5%)

---

## Transactions Frauduleuses

### 4. 🚨 Card Testing - Petites Transactions Multiples

**Description**: Fraudeur teste une carte volée avec plusieurs petites transactions rapides.

**Payload JSON**:
```json
{
  "transaction_hour": 3,
  "day_of_week": 1,
  "age": 55,
  "gender": "F",
  "home_country": "US",
  "transaction_country": "US",
  "merchant_category": "gaming",
  "merchant_base_risk": 0.35,
  "transaction_type": "online",
  "card_type": "Visa",
  "device": "mobile",
  "amount": 9.99,
  "avg_30d_amount": 120.00,
  "previous_transactions_24h": 8,
  "last_hour_transactions": 5,
  "balance": 3200.00,
  "ip_risk_score": 75.5,
  "is_foreign": 0,
  "device_mismatch": 1,
  "location_change": 0,
  "amount_anomaly": -0.65,
  "hour_anomaly": 1
}
```

**Résultat Attendu**: 🚨 FRAUDE DÉTECTÉE (Probabilité > 80%)

**Indicateurs de Fraude**:
- ⚠️ Heure inhabituelle (3h du matin)
- ⚠️ Multiples transactions en 1 heure (5)
- ⚠️ IP à haut risque (75.5)
- ⚠️ Appareil inhabituel
- ⚠️ Catégorie suspecte (gaming à risque)

---

### 5. 🚨 Account Takeover - Achat Massif après Prise de Contrôle

**Description**: Compte piraté, gros achat immédiatement après changement d'appareil.

**Payload JSON**:
```json
{
  "transaction_hour": 2,
  "day_of_week": 3,
  "age": 38,
  "gender": "M",
  "home_country": "GB",
  "transaction_country": "CN",
  "merchant_category": "electronics",
  "merchant_base_risk": 0.45,
  "transaction_type": "online",
  "card_type": "Amex",
  "device": "tablet",
  "amount": 2499.00,
  "avg_30d_amount": 85.00,
  "previous_transactions_24h": 1,
  "last_hour_transactions": 0,
  "balance": 5600.00,
  "ip_risk_score": 92.0,
  "is_foreign": 1,
  "device_mismatch": 1,
  "location_change": 1,
  "amount_anomaly": 0.95,
  "hour_anomaly": 1
}
```

**Résultat Attendu**: 🚨 FRAUDE DÉTECTÉE (Probabilité > 90%)

**Indicateurs de Fraude**:
- ⚠️ Transaction à l'étranger (GB → CN)
- ⚠️ Montant anormalement élevé (2499 vs moyenne 85)
- ⚠️ IP à très haut risque (92.0)
- ⚠️ Appareil inhabituel (tablet)
- ⚠️ Heure suspecte (2h du matin)
- ⚠️ Marchand à risque élevé (0.45)

---

### 6. 🚨 Fraude Internationale en Ligne

**Description**: Achat en ligne depuis un pays étranger, IP suspecte, montant inhabituel.

**Payload JSON**:
```json
{
  "transaction_hour": 4,
  "day_of_week": 2,
  "age": 29,
  "gender": "F",
  "home_country": "FR",
  "transaction_country": "NG",
  "merchant_category": "fashion",
  "merchant_base_risk": 0.28,
  "transaction_type": "online",
  "card_type": "Mastercard",
  "device": "desktop",
  "amount": 1200.00,
  "avg_30d_amount": 60.00,
  "previous_transactions_24h": 0,
  "last_hour_transactions": 0,
  "balance": 2100.00,
  "ip_risk_score": 88.5,
  "is_foreign": 1,
  "device_mismatch": 1,
  "location_change": 1,
  "amount_anomaly": 0.87,
  "hour_anomaly": 1
}
```

**Résultat Attendu**: 🚨 FRAUDE DÉTECTÉE (Probabilité > 85%)

**Indicateurs de Fraude**:
- ⚠️ Transaction internationale (FR → NG)
- ⚠️ IP à très haut risque (88.5)
- ⚠️ Montant 20x supérieur à la moyenne
- ⚠️ Heure anormale (4h du matin)
- ⚠️ Appareil différent

---

### 7. 🚨 Escalade après Card Testing

**Description**: Grosse transaction juste après plusieurs petites (pattern typique de fraude).

**Payload JSON**:
```json
{
  "transaction_hour": 1,
  "day_of_week": 4,
  "age": 65,
  "gender": "M",
  "home_country": "US",
  "transaction_country": "US",
  "merchant_category": "travel",
  "merchant_base_risk": 0.55,
  "transaction_type": "online",
  "card_type": "Visa",
  "device": "mobile",
  "amount": 3500.00,
  "avg_30d_amount": 95.00,
  "previous_transactions_24h": 12,
  "last_hour_transactions": 3,
  "balance": 1200.00,
  "ip_risk_score": 81.0,
  "is_foreign": 0,
  "device_mismatch": 1,
  "location_change": 0,
  "amount_anomaly": 0.92,
  "hour_anomaly": 1
}
```

**Résultat Attendu**: 🚨 FRAUDE DÉTECTÉE (Probabilité > 95%)

**Indicateurs de Fraude**:
- ⚠️ Énorme montant après multiples petites transactions
- ⚠️ 12 transactions dans les 24h (inhabituel)
- ⚠️ 3 transactions dans la dernière heure
- ⚠️ Solde insuffisant (1200 pour 3500)
- ⚠️ IP à haut risque (81.0)
- ⚠️ Catégorie à très haut risque (travel: 0.55)

---

### 8. ⚠️ Transaction Limite - Cas Borderline

**Description**: Transaction qui pourrait être légitime mais présente certains signaux d'alerte.

**Payload JSON**:
```json
{
  "transaction_hour": 23,
  "day_of_week": 5,
  "age": 31,
  "gender": "F",
  "home_country": "DE",
  "transaction_country": "FR",
  "merchant_category": "fashion",
  "merchant_base_risk": 0.18,
  "transaction_type": "online",
  "card_type": "Visa",
  "device": "mobile",
  "amount": 350.00,
  "avg_30d_amount": 100.00,
  "previous_transactions_24h": 2,
  "last_hour_transactions": 0,
  "balance": 2800.00,
  "ip_risk_score": 45.0,
  "is_foreign": 1,
  "device_mismatch": 0,
  "location_change": 1,
  "amount_anomaly": 0.35,
  "hour_anomaly": 0
}
```

**Résultat Attendu**: ⚠️ Risque Moyen (Probabilité 30-50%)

**Indicateurs Mixtes**:
- ✅ Solde suffisant
- ✅ Appareil habituel
- ⚠️ Transaction pays voisin (DE → FR) - pourrait être en voyage
- ⚠️ IP à risque modéré (45.0)
- ⚠️ Montant 3.5x supérieur à la moyenne

---

### 9. 🚨 Fraude avec Balance Négative

**Description**: Transaction qui rendrait le solde négatif, combiné à d'autres signaux.

**Payload JSON**:
```json
{
  "transaction_hour": 5,
  "day_of_week": 1,
  "age": 47,
  "gender": "M",
  "home_country": "CM",
  "transaction_country": "US",
  "merchant_category": "electronics",
  "merchant_base_risk": 0.38,
  "transaction_type": "online",
  "card_type": "Mastercard",
  "device": "desktop",
  "amount": 1800.00,
  "avg_30d_amount": 70.00,
  "previous_transactions_24h": 0,
  "last_hour_transactions": 0,
  "balance": 150.00,
  "ip_risk_score": 78.5,
  "is_foreign": 1,
  "device_mismatch": 1,
  "location_change": 1,
  "amount_anomaly": 0.88,
  "hour_anomaly": 1
}
```

**Résultat Attendu**: 🚨 FRAUDE DÉTECTÉE (Probabilité > 90%)

**Indicateurs de Fraude**:
- ⚠️ Solde insuffisant (150 vs 1800)
- ⚠️ Transaction internationale suspecte (CM → US)
- ⚠️ Montant 25x supérieur à la moyenne
- ⚠️ IP à haut risque (78.5)
- ⚠️ Heure anormale (5h du matin)

---

### 10. 🚨 Ring Fraud - Réseau de Fraudeurs

**Description**: Transaction typique d'un réseau de fraude organisé, IP très faible, marchand suspect.

**Payload JSON**:
```json
{
  "transaction_hour": 14,
  "day_of_week": 3,
  "age": 52,
  "gender": "M",
  "home_country": "US",
  "transaction_country": "US",
  "merchant_category": "services",
  "merchant_base_risk": 0.72,
  "transaction_type": "online",
  "card_type": "Visa",
  "device": "mobile",
  "amount": 450.00,
  "avg_30d_amount": 180.00,
  "previous_transactions_24h": 1,
  "last_hour_transactions": 0,
  "balance": 3500.00,
  "ip_risk_score": 5.0,
  "is_foreign": 0,
  "device_mismatch": 0,
  "location_change": 0,
  "amount_anomaly": 0.28,
  "hour_anomaly": 0
}
```

**Résultat Attendu**: 🚨 FRAUDE DÉTECTÉE (Probabilité > 70%)

**Indicateurs de Fraude**:
- ⚠️ Marchand à TRÈS haut risque (0.72) - typique des rings
- ⚠️ IP anormalement faible (5.0) - proxy/VPN
- ⚠️ Catégorie suspecte (services)
- ✅ Autres indicateurs normaux (pour masquer la fraude)

---

## Guide d'Utilisation

### Pour l'API (Ligne de Commande)

```bash
# Exemple avec curl
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_hour": 3,
    "day_of_week": 1,
    "age": 55,
    ...
  }'
```

### Pour le Dashboard Streamlit

1. Lancez le dashboard: `streamlit run dashboard.py`
2. Allez sur la page **"Inférence Temps Réel"**
3. Remplissez les champs du formulaire avec les valeurs des exemples
4. Cliquez sur **"Analyser la Transaction"**

### Pour une Présentation

**Scénario Recommandé**:

1. **Commencez par une transaction légitime** (Exemple 1 ou 2)
   - Montrez que le système ne bloque pas les transactions normales
   - Résultat: Probabilité < 10%, Transaction Sûre ✅

2. **Montrez un cas de Card Testing** (Exemple 4)
   - Expliquez les indicateurs: multiples transactions, IP suspecte, heure anormale
   - Résultat: FRAUDE DÉTECTÉE 🚨

3. **Démontrez un Account Takeover** (Exemple 5)
   - Mettez en avant le changement de pays et d'appareil
   - Montrant anormalement élevé
   - Résultat: Probabilité > 90%

4. **Cas limite** (Exemple 8)
   - Montrez que le système identifie aussi les cas ambigus
   - Discutez du trade-off Précision/Rappel

---

## Tableau Récapitulatif

| # | Type | Catégorie | Montant | Pays | Probabilité Attendue | Verdict |
|---|------|-----------|---------|------|---------------------|---------|
| 1 | Légitime | Grocery | 45.80 | US → US | < 5% | ✅ Sûre |
| 2 | Légitime | Electronics | 899.99 | FR → FR | 10-20% | ✅ Sûre |
| 3 | Légitime | Restaurants | 85.50 | CM → CM | < 5% | ✅ Sûre |
| 4 | Fraude | Gaming | 9.99 | US → US | > 80% | 🚨 Fraude |
| 5 | Fraude | Electronics | 2499.00 | GB → CN | > 90% | 🚨 Fraude |
| 6 | Fraude | Fashion | 1200.00 | FR → NG | > 85% | 🚨 Fraude |
| 7 | Fraude | Travel | 3500.00 | US → US | > 95% | 🚨 Fraude |
| 8 | Limite | Fashion | 350.00 | DE → FR | 30-50% | ⚠️ Moyen |
| 9 | Fraude | Electronics | 1800.00 | CM → US | > 90% | 🚨 Fraude |
| 10 | Fraude | Services | 450.00 | US → US | > 70% | 🚨 Fraude |

---

## Notes Techniques

### Facteurs Clés de Détection

Les principaux indicateurs utilisés par le modèle:

1. **IP Risk Score** (0-100): Plus élevé = Plus suspect
2. **Amount Anomaly** (-1 à 1): Écart par rapport à la moyenne du client
3. **Transaction Hour**: Les transactions nocturnes sont suspectes
4. **Foreign Transaction**: Changement de pays
5. **Device Mismatch**: Appareil différent de l'habituel
6. **Merchant Risk**: Certaines catégories sont plus risquées
7. **Velocity**: Nombre de transactions récentes
8. **Balance**: Solde vs montant de la transaction

### Seuil de Décision

Le modèle utilise un **seuil optimisé de ~0.0174** pour atteindre:
- **95% de Recall**: Détecte 95% des fraudes réelles
- **Trade-off**: Plus de faux positifs acceptés

---

## Contact

Pour toute question sur ces exemples:
- **Email**: tizeAhmed750@gmail.com
- **GitHub**: git@github.com:Tizeibm/Fraud-detection.git

**Dernière mise à jour**: 30 Novembre 2025
