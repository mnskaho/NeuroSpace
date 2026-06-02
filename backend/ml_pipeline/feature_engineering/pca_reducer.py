import numpy as np
from sklearn.decomposition import PCA
import logging

logger = logging.getLogger(__name__)

class PCAReducer:
    """Réduction PCA pour RNN ou prétraitement général"""
    
    def __init__(self, n_components=None, variance_threshold=0.95):
        self.n_components = n_components
        self.variance_threshold = variance_threshold
        self.pca = None
        
    def fit(self, X):
        """Ajuste le PCA sur les données"""
        if self.n_components is None:
            # Déterminer automatiquement le nombre de composantes
            self.pca = PCA(n_components=min(10, X.shape[1]))
        else:
            self.pca = PCA(n_components=self.n_components)
        
        self.pca.fit(X)
        
        # Log variance expliquée
        cumsum = np.cumsum(self.pca.explained_variance_ratio_)
        n_components_95 = np.argmax(cumsum >= self.variance_threshold) + 1
        logger.info(f"PCA: {X.shape[1]} features → {self.pca.n_components_} composantes")
        logger.info(f"Variance totale expliquée: {sum(self.pca.explained_variance_ratio_):.2%}")
        
        return self.pca
    
    def fit_transform(self, X):
        """Ajuste et transforme les données"""
        self.fit(X)
        return self.pca.transform(X)
    
    def transform(self, X):
        """Transforme les données avec le PCA déjà ajusté"""
        if self.pca is None:
            raise ValueError("PCA must be fitted first")
        return self.pca.transform(X)