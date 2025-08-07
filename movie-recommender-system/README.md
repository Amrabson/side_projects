# Movie Recommender System

A content-based movie recommendation system implemented in Python.  
Demonstrates preprocessing, feature extraction, and similarity-based recommendations using movie metadata and ratings.

---

## Features

- Loads and processes movie metadata (`movies.csv`) and user ratings (`ratings.csv`)
- Extracts features from genres and titles using vectorization
- Computes cosine similarity between movies
- Generates top-N movie recommendations based on content similarity
- Reproducible and interactive Jupyter notebook

---

## Files

- `MovieRecommenderSystem.ipynb` — Jupyter notebook (main code and analysis)
- `movies.csv` — Dataset with movie titles and genre metadata
- `ratings.csv` — Dataset with user ratings for movies

---

## How to Run

1. **Install requirements:**
   ``` pip install pandas numpy scikit-learn ```
2. **Add your dataset:**  
Place the movie metadata CSV in the same folder as the notebook.
3. **Open the notebook:**
   ```jupyter notebook MovieRecommenderSystem.ipynb```
4. **Follow instructions in the notebook to explore and get recommendations!**

---

## Author

Aharon Rabson  
GitHub: [@Amrabson](https://github.com/Amrabson)
