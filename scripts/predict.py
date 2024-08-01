import logging
from collaborative_filtering import CollaborativeFiltering

def main():
    # Configuration du logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Chemins vers le modèle et la matrice d'interaction
    model_dir = '../models/'  # Chemin vers le répertoire contenant le modèle
    model_path = model_dir + 'svd_model.joblib'
    matrix_path = model_dir + 'user_article_matrix.csv'
    
    try:
        # Initialisation et chargement des ressources
        cf = CollaborativeFiltering(None, None)
        cf.load_model(model_path)
        cf.load_user_article_matrix(matrix_path)
        
        # Demande d'ID utilisateur et recommandation
        user_id = input("Enter user ID: ")
        recommended_articles = cf.recommend_articles(int(user_id), top_n=5)
        print("Recommended articles:", recommended_articles)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
