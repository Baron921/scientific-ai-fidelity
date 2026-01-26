# PROJET TER 2026 : Évaluer la fidélité factuelle des réécritures scientifiques générées par IA

---

## Description du projet

Les grands modèles de langue (Large Language Models, LLM) sont de plus en plus utilisés pour améliorer la clarté et la lisibilité des textes scientifiques par reformulation. Cependant, ces modèles peuvent introduire des **altérations factuelles** lors de la réécriture, telles que la modification de nombres, d’unités, de références ou de noms propres, etc.

Ce projet vise à **évaluer automatiquement et manuellement (si possible) la fidélité factuelle** des réécritures scientifiques générées par un LLM, en fonction du **niveau de précision des consignes de réécriture (prompt)** fournies au modèle.

---

## Objectifs

Les objectifs principaux du projet sont :

- mesurer la **fréquence des erreurs factuelles** introduites lors de la réécriture de textes scientifiques ;
- comparer l’impact de **différentes instructions de réécriture** sur la fidélité factuelle ;
- proposer une **méthode simple de détection automatique** des altérations factuelles ;
- analyser le compromis entre **fidélité factuelle** et **qualité rédactionnelle**.

---

## Données

- **100 articles scientifiques open-access**, répartis en **5 domaines (20 articles / domaine)** :
  - Traitement Automatique des Langues (TALN)
  - Computer science
  - Statistics
  - Chemistry
  - Health
  - Economics / Finance
- Pour chaque article, un **paragraphe** est extrait, contenant :
  - au moins un **nombre**
  - une **unité**
  - un **nom propre ou une référence**


