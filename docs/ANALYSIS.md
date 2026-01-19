# Analyse de l'existant - Excel to SQLite

**Date :** 19 janvier 2026
**Version du projet :** 0.1.0-alpha
**Statut :** Phase de développement actif

---

## 1. Vue d'ensemble du projet

### 1.1 Objectif principal

Excel to SQLite est un outil en ligne de commande (CLI) qui permet de :
- Importer des fichiers Excel vers une base de données SQLite
- Exporter des données SQL vers Excel (non implémenté)
- Gérer des mappings de colonnes configurables
- Suivre l'historique des imports

### 1.2 Technologie

**Stack technique :**
- **Langage :** Python 3.10+
- **CLI Framework :** Typer
- **Validation :** Pydantic v2
- **Manipulation de données :** Pandas
- **Excel :** openpyxl
- **Base de données :** SQLAlchemy 2.0 avec SQLite
- **Interface console :** Rich

---

## 2. Analyse de la structure du code

### 2.1 Organisation des répertoires

```
excel-to-sqlite/
├── excel_to_sql/               # Package principal
│   ├── __init__.py
│   ├── __main__.py            # Entry point
│   ├── cli.py                 # Interface CLI (268 lignes)
│   ├── entities/              # Entités métier
│   │   ├── project.py         # Gestion de projet
│   │   ├── database.py        # Opérations DB
│   │   ├── excel_file.py      # Fichiers Excel
│   │   ├── dataframe.py       # Traitement de données
│   │   └── table.py           # Opérations de table
│   ├── models/                # Modèles Pydantic
│   │   └── mapping.py         # Mapping de configuration
│   └── config/                # Configuration (vide)
├── tests/                     # Suite de tests complète
│   ├── test_database.py
│   ├── test_dataframe.py
│   ├── test_excel_file.py
│   ├── test_import.py         # Tests d'intégration
│   ├── test_project.py
│   ├── test_table.py
│   └── fixtures/              # Données de test
├── docs/                      # Documentation (à créer)
├── pyproject.toml             # Configuration du projet
└── README.md                  # Documentation basique
```

### 2.2 Architecture en couches

Le projet suit une **architecture orientée entité** avec 5 entités principales :

```
┌─────────────────────────────────────┐
│            CLI (Typer)              │  ← Interface utilisateur
├─────────────────────────────────────┤
│         Entities ( métier )         │  ← Logique métier
│  ┌─────────┐ ┌─────────┐           │
│  │ Project │ │ Database│           │
│  └─────────┘ └─────────┘           │
│  ┌─────────┐ ┌─────────┐           │
│  │ExcelFile│ │DataFrame│           │
│  └─────────┘ └─────────┘           │
│  ┌─────────┐                       │
│  │  Table  │                       │
│  └─────────┘                       │
├─────────────────────────────────────┤
│        Models (Pydantic)            │  ← Validation
│  ┌─────────┐ ┌─────────┐           │
│  │Mappings │ │ Column  │           │
│  │         │ │Mapping  │           │
│  └─────────┘ └─────────┘           │
└─────────────────────────────────────┘
```

---

## 3. Fonctionnalités implémentées

### 3.1 Commande `init` ✅

**Statut :** Implémentée et fonctionnelle

**Fonctionnalité :**
- Initialise la structure du projet
- Crée les répertoires : `imports/`, `exports/`, `data/`, `logs/`, `config/`
- Initialise la base de données SQLite
- Crée un fichier de mapping par défaut

**Usage :**
```bash
excel-to-sql init [--db-path PATH]
```

**Code :** `cli.py:29-44`

---

### 3.2 Commande `import` ✅

**Statut :** Implémentée et testée

**Fonctionnalité :**
- Importe un fichier Excel dans la base de données
- Détecte les changements par hash de contenu
- Nettoie les données (lignes vides, espaces)
- Applique les mappings de colonnes
- Effectue des opérations UPSERT (insert/update)
- Enregistre l'historique des imports

**Workflow complet :**
1. Validation du fichier (existence, extension)
2. Chargement du projet
3. Validation du type de mapping
4. Lecture du fichier Excel
5. Calcul du hash de contenu
6. Vérification si déjà importé
7. Chargement des données
8. Nettoyage des données
9. Application des mappings
10. Import en base (UPSERT)
11. Enregistrement en historique
12. Affichage du résumé

**Usage :**
```bash
excel-to-sql import --file FILE --type TYPE [--force]
```

**Code :** `cli.py:51-203`

**Tests :** `tests/test_import.py` - 14 tests d'intégration

---

### 3.3 Commande `export` ⏳

**Statut :** Placeholder (TODO)

**Fonctionnalité prévue :**
- Exporte des données de la base vers Excel
- Soit une table complète, soit une requête SQL personnalisée

**Signature actuelle :**
```bash
excel-to-sql export --output OUTPUT [--table TABLE] [--query QUERY]
```

**Code :** `cli.py:211-226`

---

### 3.4 Commande `status` ⏳

**Statut :** Placeholder (TODO)

**Fonctionnalité prévue :**
- Affiche l'historique des imports
- Montre les statistiques d'import

**Signature actuelle :**
```bash
excel-to-sql status
```

**Code :** `cli.py:234-240`

---

### 3.5 Commande `config` ⏳

**Statut :** Partiellement implémentée (TODO)

**Fonctionnalité prévue :**
- Gère les configurations de mapping
- Ajoute de nouveaux types

**Signature actuelle :**
```bash
excel-to-sql config --add-type TYPE --table TABLE
```

**Code :** `cli.py:248-259`

---

## 4. Entités métier

### 4.1 Project ✅

**Responsabilités :**
- Gérer la structure du projet
- Créer et initialiser les répertoires
- Charger et sauvegarder les mappings
- Fournir l'accès à la base de données

**Méthodes clés :**
- `initialize()` - Initialisation du projet
- `add_mapping()` - Ajouter un mapping
- `get_mapping()` - Récupérer un mapping
- `list_types()` - Lister les types configurés

**Code :** `entities/project.py` (229 lignes)

---

### 4.2 Database ✅

**Responsabilités :**
- Gérer la connexion SQLite
- Créer les tables
- Exécuter des requêtes
- Gérer l'historique des imports

**Fonctionnalités :**
- Connexion SQLAlchemy
- Table `_import_history` pour le suivi
- Méthode `get_table()` pour accéder aux tables
- Méthodes `query()`, `execute()`

**Code :** `entities/database.py`

---

### 4.3 ExcelFile ✅

**Responsabilités :**
- Lire des fichiers Excel
- Calculer le hash de contenu
- Valider les fichiers

**Fonctionnalités :**
- Lecture avec pandas
- Hash SHA256 pour détecter les changements
- Validation du format

**Code :** `entities/excel_file.py`

---

### 4.4 DataFrame ✅

**Responsabilités :**
- Nettoyer les données
- Appliquer les mappings
- Convertir les types

**Fonctionnalités :**
- Suppression des lignes vides
- Nettoyage des espaces
- Conversion de types (string, integer, float, boolean, date)
- Application des mappings de colonnes

**Code :** `entities/dataframe.py`

---

### 4.5 Table ✅

**Responsabilités :**
- Représenter une table SQL
- Effectuer des opérations UPSERT
- Gérer le schéma

**Fonctionnalités :**
- Création automatique de table
- UPSERT avec clé primaire (composite supporté)
- Méthodes `select_all()`, `row_count`

**Code :** `entities/table.py`

**⚠️ Note :** Il y a un problème connu avec les clés primaires composites (voir `test_import.py:327`)

---

## 5. Configuration et Mapping

### 5.1 Structure des mappings

Les mappings sont stockés dans `config/mappings.json` :

```json
{
  "_example": {
    "target_table": "example_table",
    "primary_key": ["id"],
    "column_mappings": {
      "ID": {
        "target": "id",
        "type": "integer",
        "required": false
      },
      "Name": {
        "target": "name",
        "type": "string",
        "required": false
      }
    }
  }
}
```

### 5.2 Types de colonnes supportés

- `string` - Texte
- `integer` - Entier
- `float` - Nombre décimal
- `boolean` - Booléen
- `date` - Date

### 5.3 Modèles Pydantic

**ColumnMapping :**
- `target`: nom de la colonne cible
- `type`: type SQL
- `required`: si null doit être rejeté
- `default`: valeur par défaut

**TypeMapping :**
- `target_table`: table de destination
- `primary_key`: colonnes de la clé primaire
- `column_mappings`: mapping des colonnes

**Code :** `models/mapping.py` (59 lignes)

---

## 6. Tests

### 6.1 Couverture de tests

**Tests unitaires :**
- `test_database.py` - Tests de l'entité Database
- `test_dataframe.py` - Tests de l'entité DataFrame
- `test_excel_file.py` - Tests de l'entité ExcelFile
- `test_project.py` - Tests de l'entité Project
- `test_table.py` - Tests de l'entité Table

**Tests d'intégration :**
- `test_import.py` - 14 tests du workflow complet d'import

### 6.2 Scénarios testés

1. Import d'un nouveau fichier ✅
2. Import idempotent (même fichier) ✅
3. Import avec --force ✅
4. Mise à jour de lignes existantes ✅
5. Gestion des erreurs (fichier manquant, type inconnu) ✅
6. Gestion des lignes vides ✅
7. Gestion des valeurs null ✅
8. Coercition de types invalides ✅
9. Historique des imports ✅
10. Affichage du tableau récapitulatif ✅
11. Clé primaire composite ⚠️ (connu comme buggy)

---

## 7. Points forts du code actuel

### 7.1 Architecture

✅ **Architecture modulaire et claire**
- Séparation des préoccupations bien définie
- Entités cohérentes et réutilisables
- Code organisé et facile à naviguer

✅ **Bonne utilisation des dépendances**
- Typer pour la CLI
- Pydantic pour la validation
- Pandas pour la manipulation de données
- Rich pour l'interface utilisateur

✅ **Code orienté objet**
- Encapsulation appropriée
- Utilisation de propriétés
- Méthodes bien nommées

### 7.2 Qualité du code

✅ **Type hints**
- Code entièrement typé
- Annotations de type cohérentes

✅ **Documentation**
- Docstrings complètes
- Commentaires explicatifs

✅ **Gestion des erreurs**
- Validation des entrées
- Messages d'erreur clairs
- Codes de sortie appropriés

✅ **Tests**
- Couverture de tests complète
- Tests d'intégration robustes
- Fixtures bien organisées

### 7.3 Fonctionnalités

✅ **Détection des changements**
- Hash de contenu SHA256
- Évite les imports inutiles

✅ **UPSERT**
- Mise à jour intelligente des données
- Support de clé primaire composite (partiellement)

✅ **Nettoyage des données**
- Suppression des lignes vides
- Nettoyage des espaces
- Coercition de types

---

## 8. Problèmes et limitations

### 8.1 Problèmes connus

⚠️ **Clé primaire composite**
- L'UPSERT avec clé composite a un problème
- Test marqué comme skip dans `test_import.py:327`
- Commentaire : "The Table.upsert method doesn't properly handle composite primary keys"

### 8.2 Fonctionnalités manquantes

❌ **Export vers Excel**
- Placeholder seulement
- Aucune implémentation

❌ **Status**
- Affichage "No imports yet" en dur
- Pas d'interrogation de l'historique

❌ **Config**
- Seule la signature est définie
- Pas de logique d'ajout de mapping

### 8.3 Limitations

📝 **Documentation**
- README basique
- Pas de documentation détaillée
- Pas de guide utilisateur

📝 **Configuration**
- Mappings manuels dans JSON
- Pas de CLI pour gérer les mappings
- Pas de validation des mappings au chargement

📝 **Base de données**
- SQLite seulement (pas d'extension à d'autres DB)
- Pas de migrations de schéma

---

## 9. Dépendances

### 9.1 Dépendances principales

```
typer>=0.12.0         # CLI framework
pydantic>=2.0.0       # Validation
pandas>=2.0.0         # Manipulation de données
openpyxl>=3.0.0       # Excel files
sqlalchemy>=2.0.0     # ORM / DB abstraction
rich>=13.0.0          # Terminal UI
```

### 9.2 Dépendances de développement

```
pytest>=8.0.0         # Testing framework
pytest-cov>=4.0.0     # Coverage reporting
```

---

## 10. État du développement

### 10.1 Phase actuelle

**Phase 2-3** : L'import est complété, l'export et la gestion sont à faire

### 10.2 Historique des commits récents

```
24680d1 feat: implement complete import command with integration tests
aa8dd84 feat: implement full import command with complete workflow
4a54923 test: update Database.get_table test for Phase 2 implementation
b48ce49 test: add Table entity tests with UPSERT operations
5763ec9 test: add DataFrame wrapper tests with type conversion
```

### 10.3 Métriques de code

- **Lignes de code CLI** : ~270
- **Entités** : 5 modules
- **Tests** : 6 fichiers de test
- **Couverture** : Tests d'intégration + tests unitaires

---

## 11. Recommandations

### 11.1 Priorités à court terme

1. **Corriger la clé primaire composite**
   - Problème identifié dans `Table.upsert()`
   - Test existant mais skipé

2. **Implémenter la commande `status`**
   - Afficher l'historique des imports
   - Fonctionnalité simple à ajouter

3. **Implémenter la commande `export`**
   - Inverse de l'import
   - Export Excel avec formatting

### 11.2 Priorités à moyen terme

4. **Compléter la commande `config`**
   - Ajout/édition/suppression de mappings
   - Validation des mappings

5. **Améliorer la documentation**
   - Guide utilisateur complet
   - Documentation API
   - Exemples d'utilisation

6. **Gestion des erreurs**
   - Meilleure gestion des erreurs SQL
   - Logs détaillés
   - Mode debug

### 11.3 Améliorations futures

7. **Performance**
   - Import par lots pour gros fichiers
   - Barre de progression pour l'import
   - Parallélisation

8. **Fonctionnalités avancées**
   - Validation de données avant import
   - Transformations personnalisées
   - Support de plusieurs bases de données

---

## 12. Conclusion

Le projet **Excel to SQLite** est dans un état **solide mais incomplet** :

**Points forts :**
- Architecture bien conçue
- Code de qualité
- Tests complets
- Fonctionnalité d'import robuste

**Points à améliorer :**
- Export non implémenté
- Gestion de configuration incomplète
- Documentation limitée
- Bug avec clé primaire composite

**Recommandation principale :**
Définir clairement le périmètre du projet (MVP) et prioriser les fonctionnalités manquantes avant d'ajouter de nouvelles fonctionnalités avancées.
