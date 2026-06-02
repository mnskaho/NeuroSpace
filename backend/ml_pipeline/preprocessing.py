# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler, LabelEncoder
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class DataPreprocessor:
#     """
#     Preprocessing des données: chargement, split, standardisation
#     """
    
#     def __init__(self, test_size=0.2, val_size=0.1, random_state=42):
#         self.test_size = test_size
#         self.val_size = val_size
#         self.random_state = random_state
#         self.scaler = StandardScaler()
#         self.label_encoder = LabelEncoder()

#     def load_and_validate(self, file_path):
#         """Charge le CSV et identifie la colonne cible"""
#         df = pd.read_csv(file_path)
#         logger.info(f"Dataset chargé: {df.shape[0]} samples, {df.shape[1]} colonnes")

#         # Chercher colonne cible
#         possible_targets = ['target', 'class', 'label', 'y', 'output', 'diagnosis']
#         target_col = None
#         for col in df.columns:
#             if col.lower() in possible_targets:
#                 target_col = col
#                 break
#         if target_col is None:
#             target_col = df.columns[-1]
#             logger.warning(f"Utilisation de la dernière colonne comme cible: {target_col}")

#         # Séparer features et target
#         X = df.drop(columns=[target_col])
#         y = df[target_col]

#         # Encoder la cible - CORRECTION IMPORTANTE
#         if y.dtype == 'object' or y.dtype.name == 'category':
#             y = self.label_encoder.fit_transform(y)
#             class_names = self.label_encoder.classes_.tolist()
#         else:
#             # Conversion en numpy array pour éviter l'erreur .tolist()
#             y = y.values if hasattr(y, 'values') else np.array(y)
#             y = y.astype(np.int64)
#             class_names = np.unique(y).tolist()

#         feature_names = X.columns.tolist()
#         return X.values, y, feature_names, class_names

#     def split_data(self, X, y):
#         """Split train/val/test"""
#         X_temp, X_test, y_temp, y_test = train_test_split(
#             X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
#         )
#         val_ratio = self.val_size / (1 - self.test_size)
#         X_train, X_val, y_train, y_val = train_test_split(
#             X_temp, y_temp, test_size=val_ratio, random_state=self.random_state, stratify=y_temp
#         )
#         logger.info(f"Split: train={X_train.shape[0]}, val={X_val.shape[0]}, test={X_test.shape[0]}")
#         return X_train, X_val, X_test, y_train, y_val, y_test

#     def preprocess(self, X_train, X_val, X_test):
#         """Standardisation uniquement"""
#         X_train_scaled = self.scaler.fit_transform(X_train)
#         X_val_scaled = self.scaler.transform(X_val)
#         X_test_scaled = self.scaler.transform(X_test)
#         return X_train_scaled, X_val_scaled, X_test_scaled

#NEW CODE FOR MULTICLASS 
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """
    Preprocessing flexible pour classification binaire et multi-classe.

    Garanties:
    - target détectée proprement
    - labels encodés en 0..num_classes-1
    - class_names conserve les noms originaux
    - features numériques uniquement
    """

    def __init__(self, test_size=0.2, val_size=0.1, random_state=42):
        self.test_size = test_size
        self.val_size = val_size
        self.random_state = random_state

        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()

        self.target_col = None
        self.feature_names = None
        self.class_names = None

    def detect_target_column(self, df: pd.DataFrame) -> str:
        """
        Détecte la colonne target de façon robuste.

        Important:
        - "class" est accepté.
        - "target" est accepté.
        - "y" est accepté seulement si le nom exact est "y".
        - "size_uniformity" ne sera PAS détecté comme target juste parce qu'il contient y.
        """
        columns = list(df.columns)

        if not columns:
            raise ValueError("Le dataset ne contient aucune colonne.")

        normalized = {col: str(col).lower().strip() for col in columns}

        exact_targets = {
            "class",
            "target",
            "label",
            "labels",
            "output",
            "result",
            "diagnosis",
            "diagnostic",
            "y",
        }

        for col, col_lower in normalized.items():
            if col_lower in exact_targets:
                return col

        safe_patterns = [
            "_class",
            "class_",
            "_target",
            "target_",
            "_label",
            "label_",
            "_output",
            "output_",
            "_result",
            "result_",
            "_diagnosis",
            "diagnosis_",
        ]

        for col, col_lower in normalized.items():
            if any(pattern in col_lower for pattern in safe_patterns):
                return col

        logger.warning(f"Aucune target explicite trouvée. Utilisation de la dernière colonne: {columns[-1]}")
        return columns[-1]

    def load_and_validate(self, file_path):
        """
        Charge et valide le dataset.

        Retourne:
        - X: features float32
        - y: labels encodés int64 en 0..C-1
        - feature_names
        - class_names: noms originaux des classes
        """
        df = pd.read_csv(file_path)

        logger.info(f"Dataset chargé: {df.shape[0]} samples, {df.shape[1]} colonnes")

        if df.empty:
            raise ValueError("Le dataset est vide.")

        target_col = self.detect_target_column(df)
        self.target_col = target_col

        X_df = df.drop(columns=[target_col]).copy()
        y_raw = df[target_col].copy()

        # Supprimer les lignes avec target manquante
        valid_mask = y_raw.notna()
        X_df = X_df.loc[valid_mask].copy()
        y_raw = y_raw.loc[valid_mask].copy()

        if len(y_raw) == 0:
            raise ValueError("La colonne target ne contient aucune valeur valide.")

        # Conversion des features en numériques
        for col in X_df.columns:
            X_df[col] = pd.to_numeric(X_df[col], errors="coerce")

        # Supprimer colonnes entièrement vides après conversion
        empty_cols = X_df.columns[X_df.isna().all()].tolist()
        if empty_cols:
            raise ValueError(
                f"Colonnes features non numériques ou vides détectées: {empty_cols}. "
                "Encode ou supprime ces colonnes avant l'entraînement."
            )

        # Remplir les valeurs manquantes numériques avec la médiane
        X_df = X_df.fillna(X_df.median(numeric_only=True))

        # Vérification finale des colonnes non numériques
        non_numeric_cols = X_df.select_dtypes(exclude=[np.number]).columns.tolist()
        if non_numeric_cols:
            raise ValueError(
                f"Colonnes non numériques détectées dans les features: {non_numeric_cols}. "
                "Encode-les avant l'entraînement."
            )

        # Encodage target TOUJOURS avec LabelEncoder.
        # C'est obligatoire pour multi-classe avec CrossEntropyLoss.
        y_encoded = self.label_encoder.fit_transform(y_raw.astype(str))

        class_names = [str(c) for c in self.label_encoder.classes_]

        if len(class_names) < 2:
            raise ValueError("Le dataset doit contenir au moins 2 classes.")

        self.feature_names = X_df.columns.tolist()
        self.class_names = class_names

        logger.info(f"Target column: {target_col}")
        logger.info(f"Classes détectées: {class_names}")
        logger.info(f"Nombre de classes: {len(class_names)}")
        logger.info(f"Nombre de features: {len(self.feature_names)}")

        return (
            X_df.values.astype(np.float32),
            y_encoded.astype(np.int64),
            self.feature_names,
            class_names,
        )

    def split_data(self, X, y):
        """
        Split train/val/test stratifié.

        Si stratify échoue à cause d'un dataset trop petit ou d'une classe rare,
        fallback sans stratify.
        """
        try:
            X_temp, X_test, y_temp, y_test = train_test_split(
                X,
                y,
                test_size=self.test_size,
                random_state=self.random_state,
                stratify=y,
            )

            val_ratio = self.val_size / (1 - self.test_size)

            X_train, X_val, y_train, y_val = train_test_split(
                X_temp,
                y_temp,
                test_size=val_ratio,
                random_state=self.random_state,
                stratify=y_temp,
            )

        except ValueError as e:
            logger.warning(f"Split stratifié impossible: {e}")
            logger.warning("Fallback vers split non stratifié.")

            X_temp, X_test, y_temp, y_test = train_test_split(
                X,
                y,
                test_size=self.test_size,
                random_state=self.random_state,
                stratify=None,
            )

            val_ratio = self.val_size / (1 - self.test_size)

            X_train, X_val, y_train, y_val = train_test_split(
                X_temp,
                y_temp,
                test_size=val_ratio,
                random_state=self.random_state,
                stratify=None,
            )

        logger.info(
            f"Split: train={X_train.shape[0]}, val={X_val.shape[0]}, test={X_test.shape[0]}"
        )

        return X_train, X_val, X_test, y_train, y_val, y_test

    def preprocess(self, X_train, X_val, X_test):
        """
        Standardisation des features.
        """
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)

        return (
            X_train_scaled.astype(np.float32),
            X_val_scaled.astype(np.float32),
            X_test_scaled.astype(np.float32),
        )