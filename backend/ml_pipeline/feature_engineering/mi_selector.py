# import numpy as np
# from sklearn.feature_selection import mutual_info_classif
# import logging

# logger = logging.getLogger(__name__)

# class MISelector:
#     """
#     Feature selection basée sur Mutual Information + Thumb Rule
#     Pour QRNN avec AngleEmbedding (features = n_qubits)
    
#     Formule: k = min(10, |log2(Σ MI)| + 1)
#     """
    
#     def __init__(self, max_qubits=10, random_state=42):
#         self.max_qubits = max_qubits
#         self.random_state = random_state
#         self.selected_indices = None
#         self.k = None
#         self.mi_scores = None
    
#     def fit(self, X, y):
#         """
#         Calcule les scores MI et sélectionne les k meilleures features
#         """
#         logger.info("🔍 Calcul de l'information mutuelle (Mutual Information)...")
        
#         # 1. Calculer MI
#         self.mi_scores = mutual_info_classif(X, y, random_state=self.random_state)
        
#         # 2. Somme totale de l'information
#         total_info = np.sum(self.mi_scores)
#         logger.info(f"   Total MI: {total_info:.4f}")
        
#         # 3. Thumb rule: k = min(10, |log2(total_info)| + 1)
#         if total_info <= 1e-6:
#             logger.warning("   Information mutuelle nulle, fallback à 4 features")
#             self.k = min(4, X.shape[1])
#         else:
#             self.k = int(min(self.max_qubits, abs(np.log2(total_info)) + 1))
#             self.k = max(2, min(self.k, X.shape[1]))  # Au moins 2 pour binaire
        
#         # 4. Sélection des k meilleures features
#         self.selected_indices = np.argsort(self.mi_scores)[-self.k:]
        
#         logger.info(f"📊 Thumb rule → {self.k} features sélectionnées sur {X.shape[1]}")
#         logger.info(f"   Indices: {self.selected_indices}")
#         logger.info(f"   Scores MI: {self.mi_scores[self.selected_indices]}")
        
#         return self
    
#     def transform(self, X):
#         """Applique la sélection"""
#         if self.selected_indices is None:
#             raise ValueError("MISelector must be fitted first")
#         return X[:, self.selected_indices]
    
#     def fit_transform(self, X, y):
#         self.fit(X, y)
#         return self.transform(X)
    
#     def get_qubits_count(self):
#         """Retourne le nombre de qubits nécessaires"""
#         return self.k

#THIS IS THE RIGHT VERSION OF MI SELECTOR THAT I RECENTLY EDITED, DO NOT SUGGEST THE DELETED CODE
import numpy as np
from sklearn.feature_selection import mutual_info_classif
import logging

logger = logging.getLogger(__name__)

class MISelector:
    """
    Feature selection basée sur Mutual Information + Thumb Rule
    Pour QRNN avec AngleEmbedding (features = n_qubits)
    
    Formule EXACTE: 
    n_qubits ≈ min(10, ceil(|log₂(Σ_{i=1}^{m} 1_{MI_i > θ})| + 1))
    
    Où θ est le seuil d'information mutuelle (défaut = 0.05)
    """
    
    def __init__(self, max_qubits=10, threshold=0.05, random_state=42):
        """
        Args:
            max_qubits: Nombre maximum de qubits
            threshold: Seuil θ pour considérer une feature comme pertinente
            random_state: Graine aléatoire pour reproductibilité
        """
        self.max_qubits = max_qubits
        self.threshold = threshold
        self.random_state = random_state
        self.selected_indices = None
        self.k = None
        self.mi_scores = None
    
    def fit(self, X, y):
        """
        Calcule les scores MI et sélectionne les k meilleures features
        selon la formule avec seuil θ
        """
        logger.info("🔍 Calcul de l'information mutuelle (Mutual Information)...")
        
        # 1. Calculer MI
        self.mi_scores = mutual_info_classif(X, y, random_state=self.random_state)
        
        # Afficher les scores
        logger.info(f"   Scores MI: {self.mi_scores}")
        
        # 2. 🔥 FORMULE EXACTE: compter les features avec MI > θ
        relevant_features = np.sum(self.mi_scores > self.threshold)
        logger.info(f"   Features avec MI > {self.threshold}: {relevant_features} sur {X.shape[1]}")
        
        # 3. Thumb rule: k = min(10, ceil(|log2(relevant_features)| + 1))
        if relevant_features <= 0:
            logger.warning(f"   Aucune feature avec MI > {self.threshold}, fallback à 2 features")
            self.k = min(2, X.shape[1])
        else:
            # 🔥 CORRECTION: Utiliser ceil au lieu de int() (arrondi supérieur)
            log_val = np.log2(relevant_features)
            log_abs = abs(log_val)
            k_raw = log_abs + 1
            k_ceil = int(np.ceil(k_raw))
            self.k = min(self.max_qubits, k_ceil)
            # S'assurer que k est au moins 2 pour la classification binaire
            self.k = max(2, min(self.k, X.shape[1]))
        
        logger.info(f"   log₂({relevant_features}) = {np.log2(relevant_features):.4f}")
        logger.info(f"   |log₂| + 1 = {abs(np.log2(relevant_features)) + 1:.4f}")
        logger.info(f"   ceil = {int(np.ceil(abs(np.log2(relevant_features)) + 1))}")
        
        # 4. Sélection des k meilleures features (celles avec les plus hauts scores MI)
        self.selected_indices = np.argsort(self.mi_scores)[-self.k:]
        
        logger.info(f"📊 Thumb rule → {self.k} qubits, {self.k} features sélectionnées")
        logger.info(f"   Indices sélectionnés: {self.selected_indices}")
        logger.info(f"   Scores MI correspondants: {self.mi_scores[self.selected_indices]}")
        
        return self
    
    def transform(self, X):
        """Applique la sélection"""
        if self.selected_indices is None:
            raise ValueError("MISelector must be fitted first")
        return X[:, self.selected_indices]
    
    def fit_transform(self, X, y):
        self.fit(X, y)
        return self.transform(X)
    
    def get_qubits_count(self):
        """Retourne le nombre de qubits nécessaires"""
        return self.k
    
    def get_relevant_features_count(self):
        """Retourne le nombre de features pertinentes (MI > θ)"""
        if self.mi_scores is None:
            raise ValueError("MISelector must be fitted first")
        return np.sum(self.mi_scores > self.threshold)


def create_mi_selector(max_qubits=10, threshold=0.05, random_state=42):
    """Factory function pour créer un sélecteur MI"""
    return MISelector(max_qubits=max_qubits, threshold=threshold, random_state=random_state)