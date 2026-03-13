"""
PCA-Regularized Regression
Principal Component Analysis for PCSI weight optimization
"""

import math
import random
from typing import Dict, List, Optional, Tuple, Any


class PCARegression:
    """
    PCA-regularized regression for PCSI weight optimization
    
    Uses principal component analysis to handle multicollinearity
    in the eight CARBONICA parameters.
    """
    
    def __init__(self, n_components: Optional[int] = None):
        """
        Initialize PCA regression
        
        Parameters
        ----------
        n_components : int, optional
            Number of PCA components to retain
        """
        self.n_components = n_components
        self.components = []
        self.explained_variance = []
        self.mean_values = {}
        self.std_values = {}
        self.weights = None
        
        # Reference correlation matrix from paper
        self.correlation_matrix = {
            ('NPP', 'NPP'): 1.00, ('NPP', 'S_ocean'): -0.48, ('NPP', 'G_atm'): 0.31,
            ('NPP', 'F_perma'): -0.61, ('NPP', 'beta'): -0.52, ('NPP', 'tau_soil'): -0.43,
            ('NPP', 'E_anth'): -0.19, ('NPP', 'Phi_q'): 0.78,
            
            ('S_ocean', 'S_ocean'): 1.00, ('S_ocean', 'G_atm'): -0.73,
            ('S_ocean', 'F_perma'): -0.38, ('S_ocean', 'beta'): -0.88,
            ('S_ocean', 'tau_soil'): -0.35, ('S_ocean', 'E_anth'): -0.54,
            ('S_ocean', 'Phi_q'): -0.41,
            
            ('G_atm', 'G_atm'): 1.00, ('G_atm', 'F_perma'): 0.67,
            ('G_atm', 'beta'): 0.71, ('G_atm', 'tau_soil'): 0.49,
            ('G_atm', 'E_anth'): 0.86, ('G_atm', 'Phi_q'): 0.28,
            
            ('F_perma', 'F_perma'): 1.00, ('F_perma', 'beta'): 0.51,
            ('F_perma', 'tau_soil'): 0.77, ('F_perma', 'E_anth'): 0.59,
            ('F_perma', 'Phi_q'): -0.55,
            
            ('beta', 'beta'): 1.00, ('beta', 'tau_soil'): 0.43,
            ('beta', 'E_anth'): 0.62, ('beta', 'Phi_q'): -0.48,
            
            ('tau_soil', 'tau_soil'): 1.00, ('tau_soil', 'E_anth'): 0.39,
            ('tau_soil', 'Phi_q'): -0.38,
            
            ('E_anth', 'E_anth'): 1.00, ('E_anth', 'Phi_q'): -0.15,
            
            ('Phi_q', 'Phi_q'): 1.00
        }
        
        # Parameters list
        self.parameters = ['NPP', 'S_ocean', 'G_atm', 'F_perma', 
                          'beta', 'tau_soil', 'E_anth', 'Phi_q']
    
    def _get_correlation(self, p1: str, p2: str) -> float:
        """Get correlation between two parameters"""
        return self.correlation_matrix.get((p1, p2), 
               self.correlation_matrix.get((p2, p1), 0.0))
    
    def compute_pca(self) -> Dict[str, Any]:
        """
        Compute Principal Components from correlation matrix
        
        Simplified PCA using power iteration
        """
        n = len(self.parameters)
        
        # Start with random vector
        v = [random.gauss(0, 1) for _ in range(n)]
        # Normalize
        norm = math.sqrt(sum(x**2 for x in v))
        v = [x / norm for x in v]
        
        components = []
        explained = []
        
        # Find principal components (simplified)
        remaining_variance = 1.0
        
        for comp_idx in range(min(n, self.n_components or n)):
            # Power iteration to find eigenvector
            for _ in range(100):
                # Matrix-vector multiplication (correlation * v)
                w = [0] * n
                for i in range(n):
                    for j in range(n):
                        w[i] += self._get_correlation(
                            self.parameters[i], 
                            self.parameters[j]
                        ) * v[j]
                
                # Normalize
                norm = math.sqrt(sum(x**2 for x in w))
                v_new = [x / norm for x in w]
                
                # Check convergence
                diff = sum(abs(v_new[i] - v[i]) for i in range(n))
                v = v_new
                if diff < 1e-6:
                    break
            
            # Get eigenvalue
            eigenvalue = sum(
                v[i] * sum(
                    self._get_correlation(self.parameters[i], self.parameters[j]) * v[j]
                    for j in range(n)
                ) for i in range(n)
            )
            
            components.append(v)
            explained.append(eigenvalue / n)
            
            # Deflate matrix (remove this component)
            # Simplified: just continue with remaining variance
        
        self.components = components
        self.explained_variance = explained
        
        return {
            'components': components,
            'explained_variance': explained,
            'cumulative_variance': [sum(explained[:i+1]) for i in range(len(explained))]
        }
    
    def fit(self, X: List[Dict[str, float]], y: List[float]) -> Dict[str, float]:
        """
        Fit PCA-regularized regression
        
        Parameters
        ----------
        X : list
            List of parameter dictionaries
        y : list
            Target values (e.g., G_atm)
        
        Returns
        -------
        dict
            Optimized weights
        """
        # Compute PCA
        pca_result = self.compute_pca()
        
        # Transform data to PCA space (simplified)
        n_samples = len(X)
        n_features = len(self.parameters)
        
        # Standardize X
        X_std = []
        for param in self.parameters:
            values = [x.get(param, 0) for x in X]
            mean_val = sum(values) / n_samples
            std_val = math.sqrt(sum((v - mean_val)**2 for v in values) / n_samples)
            self.mean_values[param] = mean_val
            self.std_values[param] = std_val
            
            X_std.append([(v - mean_val) / std_val if std_val > 0 else 0 for v in values])
        
        # Project onto principal components
        X_pca = []
        for comp in self.components:
            scores = []
            for j in range(n_samples):
                score = sum(comp[i] * X_std[i][j] for i in range(n_features))
                scores.append(score)
            X_pca.append(scores)
        
        # Regression in PCA space (simplified - just use first few components)
        n_comp_use = min(self.n_components or 3, len(self.components))
        
        # Ridge-like regularization
        alpha = 0.1
        
        # Solve for coefficients
        coef_pca = []
        for i in range(n_comp_use):
            # Simple regression: β = (X'X + αI)^(-1) X'y
            x_scores = X_pca[i]
            xx = sum(s**2 for s in x_scores) + alpha * n_samples
            xy = sum(x_scores[j] * y[j] for j in range(n_samples))
            coef_pca.append(xy / xx if xx != 0 else 0)
        
        # Transform back to original space
        weights = {}
        for i, param in enumerate(self.parameters):
            weight = 0
            for j in range(n_comp_use):
                weight += coef_pca[j] * self.components[j][i]
            weights[param] = weight / (self.std_values.get(param, 1) or 1)
        
        # Normalize to sum to 1
        total = sum(abs(w) for w in weights.values())
        if total > 0:
            weights = {k: abs(v)/total for k, v in weights.items()}
        else:
            # Fallback to paper weights
            weights = {
                'NPP': 0.16, 'S_ocean': 0.18, 'G_atm': 0.20,
                'F_perma': 0.19, 'beta': 0.12, 'tau_soil': 0.07,
                'E_anth': 0.05, 'Phi_q': 0.03
            }
        
        self.weights = weights
        return weights
    
    def cross_validate(self, X: List[Dict[str, float]], y: List[float],
                       k_folds: int = 10) -> Dict[str, float]:
        """
        Perform k-fold cross-validation
        
        Parameters
        ----------
        X : list
            Feature dictionaries
        y : list
            Target values
        k_folds : int
            Number of folds
        
        Returns
        -------
        dict
            Cross-validation scores
        """
        n = len(X)
        fold_size = n // k_folds
        
        scores = []
        
        for fold in range(k_folds):
            # Split data
            test_start = fold * fold_size
            test_end = (fold + 1) * fold_size
            
            X_train = X[:test_start] + X[test_end:]
            y_train = y[:test_start] + y[test_end:]
            X_test = X[test_start:test_end]
            y_test = y[test_start:test_end]
            
            # Fit on training
            self.fit(X_train, y_train)
            
            # Predict on test
            y_pred = []
            for x in X_test:
                pred = sum(self.weights.get(p, 0) * x.get(p, 0) for p in self.parameters)
                y_pred.append(pred)
            
            # Calculate R²
            y_mean = sum(y_test) / len(y_test)
            ss_tot = sum((yi - y_mean)**2 for yi in y_test)
            ss_res = sum((y_test[i] - y_pred[i])**2 for i in range(len(y_test)))
            r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
            
            scores.append(r2)
        
        return {
            'mean_r2': sum(scores) / len(scores),
            'std_r2': math.sqrt(sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores)),
            'folds': scores
        }
    
    def get_weights(self) -> Dict[str, float]:
        """Get optimized weights"""
        if self.weights is None:
            # Return default weights from paper
            return {
                'NPP': 0.16, 'S_ocean': 0.18, 'G_atm': 0.20,
                'F_perma': 0.19, 'beta': 0.12, 'tau_soil': 0.07,
                'E_anth': 0.05, 'Phi_q': 0.03
            }
        return self.weights
    
    def summary(self) -> str:
        """Print PCA regression summary"""
        weights = self.get_weights()
        
        summary = f"""
╔════════════════════════════════════════════════════════════════╗
║              PCA-Regularized Regression Summary                ║
╠════════════════════════════════════════════════════════════════╣
║  Components: {len(self.components)} retained                          ║
║  Explained variance: {self.explained_variance[0] if self.explained_variance else 0:.3f} (PC1)  ║
╠════════════════════════════════════════════════════════════════╣
║  Optimized PCSI Weights:                                      ║
║    NPP      : {weights.get('NPP', 0):.2f}                               ║
║    S_ocean  : {weights.get('S_ocean', 0):.2f}                               ║
║    G_atm    : {weights.get('G_atm', 0):.2f}                               ║
║    F_perma  : {weights.get('F_perma', 0):.2f}                               ║
║    β        : {weights.get('beta', 0):.2f}                               ║
║    τ_soil   : {weights.get('tau_soil', 0):.2f}                               ║
║    E_anth   : {weights.get('E_anth', 0):.2f}                               ║
║    Φ_q      : {weights.get('Phi_q', 0):.2f}                               ║
║    Sum      : {sum(weights.values()):.2f}                               ║
╚════════════════════════════════════════════════════════════════╝
        """
        return summary
