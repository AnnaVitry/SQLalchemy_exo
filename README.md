# Docs - SPHINX

Objectif :  

**Installation + principale commande** 
- Installation
- Installer la doc et Read the Doc
- Pour lire le markdown
- Compiler la documentation  

**Configuration**
- Changer le thème
- Définir les chemins pour trouver notre code  

**index.rst**
- Inclure le Readme.md (myst_parser)
- Créer l’auto doc
- Arborescence plus complète  

**Workflow et GitHub Pages**
- GitHub Pages
- Workflow

---

## Objectif :
L’objectif de ce tutoriel est de transformer votre code source en une documentation vivante, structurée et esthétique, capable de survivre à votre départ du projet.  En utilisant **Sphinx** avec le thème moderne **Furo** (ou le standard **Read the Docs**), vous apprendrez à générer automatiquement une documentation technique à partir de vos docstrings, tout en intégrant des guides utilisateurs en Markdown ou reStructuredText. Nous mettrons l’accent sur la création d'un "contrat de maintenance" clair : chaque module (`app_data`, `app_ia`) doit être capable d'expliquer ses propres schémas de données et ses choix de modèles, garantissant ainsi que votre architecture distribuée reste compréhensible et évolutive pour tout futur collaborateur.

## Installation + principale commande
### Installation 
Installer la doc et Read the Doc
```bash
uv add --dev "sphinx-rtd-theme>=3.0.0rc1"
```
Pour lire le markdown
```bash
uv add myst_parser
```
Créer un dossier docs et aller dedans:
```bash
uv run sphinx-quickstart
```
Compiler la documentation (lancer depuis la racine):
```bash
uv run sphinx-build -b html docs/source public
```

## Configuration (conf.py)
Dans le dossier `docs`>`source`>`conf.py` on peut gérer la configuration
```python
import sphinx_rtd_theme


extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.autodoc',  # Pour extraire la doc du code
    'sphinx.ext.napoleon', # Pour supporter les docstrings style Google/NumPy
    'sphinx.ext.mathjax',  # Pour latex
    "sphinx.ext.viewcode", # pour afficher code source
    "myst_parser",         # pour le markdown
]
```

### Changer le thème
On change
```python
html_theme = 'alabaster'
```
par 
```python
html_theme = "sphinx_rtd_theme"
```

On peut aussi ajouter un logo, il faut créer manuellement le dossier docs/source/_static:
```python
html_logo = "_static/img/logo.png"
```

Changer le texte de l’onglet de la page
```python
html_title = "Documentation - Sphinx - UV"
```

### Définir les chemins pour trouver notre code
```python
import os
import sys


# On remonte à la racine, puis on descend dans 'app'
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../app'))
```

> Au choix, tout dépend si le projet est directement à la racine ou si le projet est rangé dans un dossier de projet (ici app).

## Autodoc (index.rst)
Le fichier `index.rst` est la **page d'accueil** qui définit la structure de ton site.  
Son rôle principal est de contenir la directive `.. toctree::` (Table of Contents Tree). C'est ce bloc qui indique à Sphinx :
1. Quels fichiers inclure dans la documentation.
2. Dans quel ordre les afficher.
3. Comment construire le menu de navigation latéral.  
**En résumé :** Si un fichier .rst ou .md n'est pas listé dans index.rst, il n'apparaîtra jamais dans ton site final, même s'il existe dans ton dossier.

### Inclure le `Readme.md` (myst_parser)
```python
.. include:: ../../README.md
   :parser: myst_parser.sphinx_
```
### Créer l’auto doc: 
Si vous avez votre **api** dans un dossier mon_api, je vous conseille de créer un fichier `mon_api.rst` (pour rester consistant) dans le même dossier que `index.rst`.
Puis de l’appeler depuis `mon_api.rst`: 
```python
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   self
   mon_api
```
Attention, retour à la ligne obligatoire entre caption et self  

et mon_api.rst sera du genre: 
```python
Documentation de l'api
======================

Mon application
---------------

.. automodule:: mon_api.api
   :members:
   :undoc-members:
   :show-inheritance:
```

Dans cette exemple votre api : `apy.py` se trouve dans le dossier `mon_api`

### Arborescence plus complète
Imaginons qu’on ait plusieurs fichiers dans un dossier de l’application, le dossier module qui contiendrait deux fichiers:

- modules/modules.py
- modules/my_maths.py

```bash
racine/
├── mon_api/
│   ├── __init__.py        # Indique que mon_api est un package
│   ├── app.py             # Ton fichier principal
│   └── modules/
│       ├── __init__.py    # Indique que modules est un sous-package
│       ├── my_maths.py
│       └── modules.py
├── docs/
│   └── source/
│       ├── conf.py        # sys.path.insert(0, os.path.abspath('../../'))
│       ├── mon_api.rst        
│       └── index.rst
└── pyproject.toml
```
```bash
Modules
===================

Outils Mathématiques
--------------------

.. automodule:: api.modules.my_maths
   :members:
   :undoc-members:
   :show-inheritance:

Logique métier
--------------

.. automodule:: api.modules.modules
   :members:
   :undoc-members:
   :show-inheritance:

.. _references:

Bibliographie
-------------

.. [1] Schutz, A. (2026). *Manuel de Packaging pour l'IA*.
```

La citation peut être appelé dans le documentation:

```python
def calculer_moyenne(data: list) -> float:
    r"""
    Calcule la moyenne arithmétique d'une liste de nombres.
    La formule mathématique est la suivante :

    .. math::
       \bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i

    Comme indiqué dans la littérature [1]_, la moyenne est sensible
    aux valeurs aberrantes.

    Args:
        data (list): Une liste ou un array de nombres.

    Returns:
        float: La moyenne calculée.
    """
    return data.sum() / len(data)
```

## Workflow et GitHub Pages
### GitHub Pages: 
Sur GitHub, allez dans les setting de votre projet et choisissez `Pages`, réglez le `Build and deployment` sur `GitHub Actions` 


### Workflow
Mettre dans le fichier `.github/workflows/docs.yml` 
```yaml
name: Deploy Documentation


on:
  push:
    branches: [main] # Se lance à chaque fois que tu push sur main


permissions:
  contents: write
  pages: write
  id-token: write


jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3
        with:
          version: "latest"

      - name: Install dependencies
        run: uv sync --all-extras # Installe Sphinx et le thème RTD définis dans le fichier toml

      - name: Build Sphinx Documentation
        # On génère le HTML dans le dossier "public"
        run: uv run sphinx-build docs/source public

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: 'public'

  deploy-docs:
    needs: build-docs
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

## Encore plus joli
### Les commentaires

On peut améliorer le visuel des commentaires en utilisant des lignes commençant par >>>

```python
"""Description de dossier.mon_module.py
:cite:p:`vaswani2023attentionneed`
>>> exemple d'utilisation
>>> uv add mon_module
>>> from mon_module import exe_app
>>> exe_app()
"""
```

### Bibliographie type BibTex


Le `BibTeX` est un format de fichier standard (**.bib**) permettant de stocker des références bibliographiques de manière structurée et réutilisable. Il est massivement utilisé par **les chercheurs, les universitaires et les ingénieurs** (notamment en IA et Data Science) pour automatiser la citation de sources dans des documents LaTeX ou Sphinx.

#### Installation de l’extension et configuration de conf.py
On installe le package : uv add sphinxcontrib-bibtex
Configuration dans `conf.py` :
```python 
extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.autodoc',  # Pour extraire la doc du code
    'sphinx.ext.napoleon', # Pour supporter les docstrings style Google/NumPy
    'sphinx.ext.mathjax',  # Pour latex
    "sphinx.ext.viewcode", # pour afficher code source
    "myst_parser",         # pour le markdown
    'sphinxcontrib.bibtex',
]
bibtex_bibfiles = ['refs.bib']
```

Le fichier `refs.bib` se trouve dans le dossier `source` et contient toutes les citations

#### Exemple de citation bibtex (Attention is All You Need)

Provenant de https://arxiv.org/abs/1706.03762 en cliquant sur `export BibTeX citation`
```bibtex
@misc{vaswani2023attentionneed,
      title={Attention Is All You Need}, 
      author={Ashish Vaswani and Noam Shazeer and Niki Parmar and Jakob Uszkoreit and Llion Jones and Aidan N. Gomez and Lukasz Kaiser and Illia Polosukhin},
      year={2023},
      eprint={1706.03762},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/1706.03762}, 
}
```

#### Afficher toutes les références
Vous pouvez très bien créer un `biblio.rst` et mettre cela dedans

```bash
Bibliographie
-------------

.. bibliography::
   :filter: cited
```

#### Citer une référence dans la docstring d’un de vos code
On utilise :cite:p:`nom_de_le_référence` pour afficher (avec lien) la référence.

```python
"""Description de dossier.mon_module.py
Comme indiqué dans la littérature :cite:p:`vaswani2023attentionneed`
"""
```
