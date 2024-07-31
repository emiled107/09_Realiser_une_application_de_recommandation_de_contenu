# train_model.py
from collaborative_filtering import CollaborativeFiltering

def main():
    articles_metadata_path = '../data/articles_metadata.csv'
    clicks_path = '../data/clicks'

    # Initialisation et entraînement du modèle
    cf = CollaborativeFiltering(articles_metadata_path, clicks_path)
    clicks_df, _ = cf.load_data()
    clicks_df = cf.clean_and_prepare_data(clicks_df)
    interaction_matrix = cf.build_interaction_matrix(clicks_df)
    cf.train_model(interaction_matrix)
    cf.save_model('svd_model.joblib')

if __name__ == '__main__':
    main()
