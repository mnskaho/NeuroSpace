# import torch
# import numpy as np
# from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, precision_score, recall_score, classification_report
# import matplotlib.pyplot as plt
# import seaborn as sns

# class Evaluator:
#     """
#     Évaluateur de modèles avec métriques standard
#     """
    
#     def __init__(self, model, device='cuda' if torch.cuda.is_available() else 'cpu'):
#         self.model = model.to(device)
#         self.device = device

#     def predict(self, X):
#         """Prédit les classes pour X"""
#         self.model.eval()
        
#         # Si le modèle a une méthode predict, l'utiliser
#         if hasattr(self.model, 'predict'):
#             return self.model.predict(X)
        
#         # Sinon, utiliser forward
#         X_tensor = torch.FloatTensor(X).to(self.device)
#         with torch.no_grad():
#             outputs = self.model(X_tensor)
#             _, predicted = torch.max(outputs, 1)
#         return predicted.cpu().numpy()

#     def evaluate(self, X, y, class_names=None):
#         """Évalue le modèle et retourne toutes les métriques"""
#         y_pred = self.predict(X)
        
#         acc = accuracy_score(y, y_pred)
#         f1 = f1_score(y, y_pred, average='weighted')
#         precision = precision_score(y, y_pred, average='weighted', zero_division=0)
#         recall = recall_score(y, y_pred, average='weighted', zero_division=0)
#         cm = confusion_matrix(y, y_pred)
        
#         metrics = {
#             'accuracy': float(acc),
#             'f1_score': float(f1),
#             'precision': float(precision),
#             'recall': float(recall),
#             'confusion_matrix': cm.tolist()
#         }
        
#         # Rapport détaillé
#         if class_names:
#             metrics['classification_report'] = classification_report(
#                 y, y_pred, target_names=class_names, output_dict=True
#             )
        
#         return metrics

#     def plot_confusion_matrix(self, y_true, y_pred, class_names, title='Confusion Matrix'):
#         """Trace la matrice de confusion"""
#         cm = confusion_matrix(y_true, y_pred)
#         plt.figure(figsize=(8, 6))
#         sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
#                     xticklabels=class_names, yticklabels=class_names)
#         plt.title(title)
#         plt.ylabel('True Label')
#         plt.xlabel('Predicted Label')
#         plt.tight_layout()
#         return plt.gcf()

#     def plot_training_curves(self, history, title='Training Curves'):
#         """Trace les courbes d'entraînement"""
#         fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
#         # Loss curve
#         axes[0].plot(history.get('train_loss', []), label='Train Loss', linewidth=2)
#         axes[0].plot(history.get('val_loss', []), label='Validation Loss', linewidth=2)
#         axes[0].set_xlabel('Epoch')
#         axes[0].set_ylabel('Loss')
#         axes[0].set_title('Loss Curves')
#         axes[0].legend()
#         axes[0].grid(True, alpha=0.3)
        
#         # Accuracy curve
#         axes[1].plot(history.get('train_acc', []), label='Train Accuracy', linewidth=2)
#         axes[1].plot(history.get('val_acc', []), label='Validation Accuracy', linewidth=2)
#         axes[1].set_xlabel('Epoch')
#         axes[1].set_ylabel('Accuracy')
#         axes[1].set_title('Accuracy Curves')
#         axes[1].legend()
#         axes[1].grid(True, alpha=0.3)
        
#         plt.suptitle(title)
#         plt.tight_layout()
#         return fig

#GROK VERSION 
# import torch
# import numpy as np
# from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix, classification_report

# class Evaluator:
#     def __init__(self, model, device=None):
#         if device is None:
#             device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#         self.model = model.to(device)
#         self.device = device

#     def predict(self, X):
#         self.model.eval()
        
#         if hasattr(self.model, 'predict'):
#             # Si le modèle a une méthode predict native (comme dans Qiskit/PennyLane)
#             return self.model.predict(X)
        
#         # Sinon fallback
#         X_tensor = torch.FloatTensor(X).to(self.device)
#         with torch.no_grad():
#             outputs = self.model(X_tensor)
#             _, predicted = torch.max(outputs, 1)
#         return predicted.cpu().numpy()

#     def evaluate(self, X, y, class_names=None):
#         y_pred = self.predict(X)
        
#         acc = accuracy_score(y, y_pred)
#         f1 = f1_score(y, y_pred, average='weighted')
#         precision = precision_score(y, y_pred, average='weighted', zero_division=0)
#         recall = recall_score(y, y_pred, average='weighted', zero_division=0)
#         cm = confusion_matrix(y, y_pred)
        
#         metrics = {
#             'accuracy': float(acc),
#             'f1_score': float(f1),
#             'precision': float(precision),
#             'recall': float(recall),
#             'confusion_matrix': cm.tolist()
#         }
        
#         if class_names:
#             metrics['classification_report'] = classification_report(
#                 y, y_pred, target_names=class_names, output_dict=True
#             )
        
#         return metrics


#NEW CODE FOR MULTICLASS GPT5 

import torch
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report,
)


class Evaluator:
    """
    Évaluateur flexible pour classification binaire et multi-classe.
    """

    def __init__(self, model, device=None):
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = model.to(device)
        self.device = device

    def predict(self, X):
        self.model.eval()

        if hasattr(self.model, "predict"):
            return self.model.predict(X)

        X_tensor = torch.FloatTensor(X).to(self.device)

        with torch.no_grad():
            outputs = self.model(X_tensor)

            if outputs.ndim != 2:
                raise ValueError(
                    f"Le modèle doit retourner une sortie 2D (batch, num_classes), reçu: {outputs.shape}"
                )

            predicted = torch.argmax(outputs, dim=1)

        return predicted.cpu().numpy()

    def evaluate(self, X, y, class_names=None):
        y_pred = self.predict(X)

        y = np.asarray(y, dtype=np.int64)
        y_pred = np.asarray(y_pred, dtype=np.int64)

        if class_names is not None:
            labels = list(range(len(class_names)))
            target_names = [str(c) for c in class_names]
        else:
            labels = sorted(np.unique(np.concatenate([y, y_pred])).tolist())
            target_names = [str(c) for c in labels]

        acc = accuracy_score(y, y_pred)

        f1 = f1_score(
            y,
            y_pred,
            labels=labels,
            average="weighted",
            zero_division=0,
        )

        precision = precision_score(
            y,
            y_pred,
            labels=labels,
            average="weighted",
            zero_division=0,
        )

        recall = recall_score(
            y,
            y_pred,
            labels=labels,
            average="weighted",
            zero_division=0,
        )

        cm = confusion_matrix(
            y,
            y_pred,
            labels=labels,
        )

        report = classification_report(
            y,
            y_pred,
            labels=labels,
            target_names=target_names,
            output_dict=True,
            zero_division=0,
        )

        return {
            "accuracy": float(acc),
            "f1_score": float(f1),
            "precision": float(precision),
            "recall": float(recall),
            "confusion_matrix": cm.tolist(),
            "classification_report": report,
            "num_classes": int(len(labels)),
            "class_names": target_names,
        }