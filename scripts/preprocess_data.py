import pandas as pd

def preprocess_data():
    articles = pd.read_csv('data/articles.csv')
    user_interactions = pd.read_csv('data/user_interactions.csv')
    # Implémentez votre logique de prétraitement ici
    return articles, user_interactions

if __name__ == "__main__":
    preprocess_data()
