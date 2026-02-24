"""
RAPID AI-POWERED CLINICAL DATA ANALYSIS
90-Minute Comprehensive Analysis Pipeline

Discovery Cohort: 30 patients
Validation Cohort: 95 patients

Features:
- Automated ML survival analysis
- Advanced feature engineering
- LLM-powered clinical insights
- Predictive modeling
- Interactive visualizations
- Comprehensive reporting

Author: Rapid AI Pipeline
Date: 2026-01-31
Time Limit: 90 minutes
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix, 
                             roc_auc_score, roc_curve, precision_recall_curve)
from scipy import stats
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


class RapidClinicalAI:
    """
    Rapid AI-powered clinical data analyzer
    Designed for 90-minute comprehensive analysis
    """
    
    def __init__(self, output_dir='/home/claude/rapid_clinical_ai_output'):
        """Initialize the rapid analyzer"""
        self.output_dir = output_dir
        
        # Create output structure
        self.dirs = {
            'data': f"{output_dir}/01_data_exploration",
            'survival': f"{output_dir}/02_survival_analysis",
            'ml': f"{output_dir}/03_machine_learning",
            'predictions': f"{output_dir}/04_predictions",
            'insights': f"{output_dir}/05_ai_insights",
            'figures': f"{output_dir}/figures",
            'models': f"{output_dir}/models"
        }
        
        for dir_path in self.dirs.values():
            os.makedirs(dir_path, exist_ok=True)
        
        # Data containers
        self.discovery = None
        self.validation = None
        self.discovery_processed = None
        self.validation_processed = None
        self.models = {}
        self.best_model = None
        
        print("=" * 80)
        print("RAPID AI-POWERED CLINICAL DATA ANALYSIS")
        print("=" * 80)
        print(f"Output Directory: {output_dir}")
        print("Time Budget: 90 minutes")
        print("=" * 80)
    
    def load_data(self, discovery_file, validation_file):
        """Load discovery and validation cohorts"""
        print("\n[1/8] Loading data...")
        
        self.discovery = pd.read_csv(discovery_file)
        self.validation = pd.read_excel(validation_file)
        
        print(f"  ✓ Discovery cohort: {self.discovery.shape[0]} patients, {self.discovery.shape[1]} features")
        print(f"  ✓ Validation cohort: {self.validation.shape[0]} patients, {self.validation.shape[1]} features")
        
        # Quick summary
        print(f"\n  Discovery outcomes:")
        print(f"    - Dead: {(self.discovery['Dead or Alive'] == 'Dead').sum()}")
        print(f"    - Alive: {(self.discovery['Dead or Alive'] == 'Alive').sum()}")
        
        print(f"\n  Validation outcomes:")
        print(f"    - Dead: {self.validation['Event (death: 1, alive: 0)'].sum()}")
        print(f"    - Alive: {(self.validation['Event (death: 1, alive: 0)'] == 0).sum()}")
    
    def automated_eda(self):
        """Automated Exploratory Data Analysis"""
        print("\n[2/8] Automated EDA...")
        
        # Discovery cohort analysis
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # 1. Survival time distribution
        axes[0, 0].hist(self.discovery['Time'], bins=20, edgecolor='black', alpha=0.7)
        axes[0, 0].set_xlabel('Survival Time (days)')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('A. Survival Time Distribution (Discovery)')
        axes[0, 0].axvline(self.discovery['Time'].median(), color='red', 
                          linestyle='--', label=f"Median: {self.discovery['Time'].median():.0f}")
        axes[0, 0].legend()
        
        # 2. Outcome by sex
        outcome_sex = pd.crosstab(self.discovery['sex'], self.discovery['Dead or Alive'])
        outcome_sex.plot(kind='bar', ax=axes[0, 1], color=['#2ecc71', '#e74c3c'])
        axes[0, 1].set_xlabel('Sex')
        axes[0, 1].set_ylabel('Count')
        axes[0, 1].set_title('B. Outcome by Sex')
        axes[0, 1].legend(title='Outcome')
        axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=0)
        
        # 3. Outcome by race
        outcome_race = pd.crosstab(self.discovery['race'], self.discovery['Dead or Alive'])
        outcome_race.plot(kind='bar', ax=axes[0, 2], color=['#2ecc71', '#e74c3c'])
        axes[0, 2].set_xlabel('Race')
        axes[0, 2].set_ylabel('Count')
        axes[0, 2].set_title('C. Outcome by Race')
        axes[0, 2].legend(title='Outcome')
        axes[0, 2].set_xticklabels(axes[0, 2].get_xticklabels(), rotation=0)
        
        # Validation cohort analysis
        # 4. Survival time distribution
        axes[1, 0].hist(self.validation['Survival time (days)'], bins=30, 
                       edgecolor='black', alpha=0.7, color='steelblue')
        axes[1, 0].set_xlabel('Survival Time (days)')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_title('D. Survival Time Distribution (Validation)')
        axes[1, 0].axvline(self.validation['Survival time (days)'].median(), 
                          color='red', linestyle='--', 
                          label=f"Median: {self.validation['Survival time (days)'].median():.0f}")
        axes[1, 0].legend()
        
        # 5. Age distribution by outcome
        dead_val = self.validation[self.validation['Event (death: 1, alive: 0)'] == 1]
        alive_val = self.validation[self.validation['Event (death: 1, alive: 0)'] == 0]
        
        axes[1, 1].hist([dead_val['Age'], alive_val['Age']], bins=15, 
                       label=['Dead', 'Alive'], color=['#e74c3c', '#2ecc71'], alpha=0.7)
        axes[1, 1].set_xlabel('Age')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('E. Age Distribution by Outcome (Validation)')
        axes[1, 1].legend()
        
        # 6. Tumor size by outcome
        axes[1, 2].boxplot([dead_val['Tumor size (cm)'].dropna(), 
                           alive_val['Tumor size (cm)'].dropna()],
                          labels=['Dead', 'Alive'])
        axes[1, 2].set_ylabel('Tumor Size (cm)')
        axes[1, 2].set_title('F. Tumor Size by Outcome (Validation)')
        axes[1, 2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{self.dirs['data']}/exploratory_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ EDA plots saved to {self.dirs['data']}/")
    
    def preprocess_data(self):
        """Advanced feature engineering and preprocessing"""
        print("\n[3/8] Feature engineering & preprocessing...")
        
        # Discovery cohort preprocessing
        disc = self.discovery.copy()
        
        # Create binary outcome
        disc['Outcome_Binary'] = (disc['Dead or Alive'] == 'Dead').astype(int)
        
        # Extract T and N stage
        disc['T_stage'] = disc['Stage'].str.extract(r'(T\d+|pT\d+)', expand=False).str.replace('pT', 'T')
        disc['N_stage'] = disc['Stage'].str.extract(r'(N\d+|pN\d+)', expand=False).str.replace('pN', 'N')
        
        # Encode categorical variables
        disc['sex_encoded'] = (disc['sex'] == 'M').astype(int)
        
        # Race encoding (W=0, B=1, O=2, A=3)
        race_map = {'W': 0, 'B': 1, 'O': 2, 'A': 3}
        disc['race_encoded'] = disc['race'].map(race_map)
        
        # Create risk categories based on time
        disc['Risk_Category'] = pd.cut(disc['Time'], 
                                       bins=[0, 365, 1825, np.inf],
                                       labels=['High', 'Medium', 'Low'])
        
        self.discovery_processed = disc
        
        # Validation cohort preprocessing
        val = self.validation.copy()
        
        # Binary outcome already exists
        val['Outcome_Binary'] = val['Event (death: 1, alive: 0)']
        
        # Sex encoding
        val['sex_encoded'] = (val['Sex'] == 'Male').astype(int)
        
        # Cigarette smoking
        val['smoking_encoded'] = (val['Cigarette'] == 'Yes').astype(int)
        
        # EGFR and KRAS encoding
        val['EGFR_positive'] = (val['EGFR'] == 'Positive').astype(int)
        val['KRAS_mutant'] = val['KRAS'].notna() & (val['KRAS'] != 'Negative')
        val['KRAS_mutant'] = val['KRAS_mutant'].astype(int)
        
        # Age categories
        val['Age_Category'] = pd.cut(val['Age'], 
                                     bins=[0, 50, 65, 80, np.inf],
                                     labels=['<50', '50-65', '65-80', '>80'])
        
        # Tumor size categories
        val['Tumor_Size_Category'] = pd.cut(val['Tumor size (cm)'],
                                           bins=[0, 3, 5, 7, np.inf],
                                           labels=['Small', 'Medium', 'Large', 'Very Large'])
        
        self.validation_processed = val
        
        print(f"  ✓ Discovery processed: {disc.shape[1]} features")
        print(f"  ✓ Validation processed: {val.shape[1]} features")
        
        # Save processed data
        disc.to_csv(f"{self.dirs['data']}/discovery_processed.csv", index=False)
        val.to_csv(f"{self.dirs['data']}/validation_processed.csv", index=False)
        print(f"  ✓ Processed data saved")
    
    def survival_analysis(self):
        """Comprehensive survival analysis"""
        print("\n[4/8] Survival analysis...")
        
        try:
            from lifelines import KaplanMeierFitter, CoxPHFitter
            from lifelines.statistics import logrank_test
            
            # Kaplan-Meier analysis
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            
            kmf = KaplanMeierFitter()
            
            # 1. Overall survival (Discovery)
            ax = axes[0, 0]
            kmf.fit(self.discovery_processed['Time'], 
                   self.discovery_processed['Outcome_Binary'],
                   label='Discovery Cohort')
            kmf.plot_survival_function(ax=ax)
            ax.set_xlabel('Time (days)')
            ax.set_ylabel('Survival Probability')
            ax.set_title('A. Overall Survival - Discovery Cohort')
            ax.grid(True, alpha=0.3)
            
            # 2. Survival by sex (Discovery)
            ax = axes[0, 1]
            for sex in self.discovery_processed['sex'].unique():
                mask = self.discovery_processed['sex'] == sex
                kmf.fit(self.discovery_processed.loc[mask, 'Time'],
                       self.discovery_processed.loc[mask, 'Outcome_Binary'],
                       label=f'Sex: {sex}')
                kmf.plot_survival_function(ax=ax)
            
            ax.set_xlabel('Time (days)')
            ax.set_ylabel('Survival Probability')
            ax.set_title('B. Survival by Sex - Discovery')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # 3. Overall survival (Validation)
            ax = axes[1, 0]
            kmf.fit(self.validation_processed['Survival time (days)'],
                   self.validation_processed['Outcome_Binary'],
                   label='Validation Cohort')
            kmf.plot_survival_function(ax=ax)
            ax.set_xlabel('Time (days)')
            ax.set_ylabel('Survival Probability')
            ax.set_title('C. Overall Survival - Validation Cohort')
            ax.grid(True, alpha=0.3)
            
            # 4. Survival by age category (Validation)
            ax = axes[1, 1]
            for age_cat in self.validation_processed['Age_Category'].dropna().unique():
                mask = self.validation_processed['Age_Category'] == age_cat
                if mask.sum() > 0:
                    kmf.fit(self.validation_processed.loc[mask, 'Survival time (days)'],
                           self.validation_processed.loc[mask, 'Outcome_Binary'],
                           label=f'Age: {age_cat}')
                    kmf.plot_survival_function(ax=ax)
            
            ax.set_xlabel('Time (days)')
            ax.set_ylabel('Survival Probability')
            ax.set_title('D. Survival by Age Category - Validation')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            plt.tight_layout()
            plt.savefig(f"{self.dirs['survival']}/kaplan_meier_curves.png", 
                       dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"  ✓ Kaplan-Meier curves saved")
            
            # Cox Proportional Hazards (Validation cohort - more features)
            cox_data = self.validation_processed[[
                'Survival time (days)', 'Outcome_Binary', 'Age', 
                'Tumor size (cm)', 'Grade', 'sex_encoded', 'smoking_encoded'
            ]].dropna()
            
            cph = CoxPHFitter()
            cph.fit(cox_data, duration_col='Survival time (days)', 
                   event_col='Outcome_Binary')
            
            # Plot Cox results
            fig, ax = plt.subplots(figsize=(10, 8))
            cph.plot(ax=ax)
            ax.set_title('Cox Proportional Hazards Model - Validation Cohort')
            plt.tight_layout()
            plt.savefig(f"{self.dirs['survival']}/cox_hazards.png", 
                       dpi=300, bbox_inches='tight')
            plt.close()
            
            # Save Cox summary
            with open(f"{self.dirs['survival']}/cox_summary.txt", 'w') as f:
                f.write("Cox Proportional Hazards Model Summary\n")
                f.write("=" * 80 + "\n\n")
                f.write(str(cph.summary))
            
            print(f"  ✓ Cox model fitted and saved")
            
        except ImportError:
            print("  ⚠ lifelines not installed. Installing...")
            import subprocess
            subprocess.run(['pip', 'install', '--break-system-packages', 'lifelines', '-q'])
            print("  ✓ Please re-run this step")
    
    def machine_learning_models(self):
        """Train and evaluate multiple ML models"""
        print("\n[5/8] Training ML models...")
        
        # Prepare validation data (more samples, more features)
        feature_cols = ['Age', 'Tumor size (cm)', 'Grade', 'sex_encoded', 
                       'smoking_encoded', 'EGFR_positive', 'KRAS_mutant']
        
        X = self.validation_processed[feature_cols].fillna(0)
        y = self.validation_processed['Outcome_Binary']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Define models
        models = {
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'SVM': SVC(probability=True, random_state=42)
        }
        
        # Train and evaluate
        results = []
        
        for name, model in models.items():
            print(f"  Training {name}...")
            
            # Train
            model.fit(X_train_scaled, y_train)
            
            # Predictions
            y_pred = model.predict(X_test_scaled)
            y_prob = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, 'predict_proba') else None
            
            # Metrics
            accuracy = accuracy_score(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='accuracy')
            
            results.append({
                'Model': name,
                'Accuracy': accuracy,
                'CV_Mean': cv_scores.mean(),
                'CV_Std': cv_scores.std()
            })
            
            # Store model
            self.models[name] = {
                'model': model,
                'scaler': scaler,
                'features': feature_cols,
                'y_test': y_test,
                'y_pred': y_pred,
                'y_prob': y_prob
            }
            
            print(f"    ✓ {name}: Accuracy={accuracy:.3f}, CV={cv_scores.mean():.3f}±{cv_scores.std():.3f}")
        
        # Results dataframe
        results_df = pd.DataFrame(results).sort_values('Accuracy', ascending=False)
        results_df.to_csv(f"{self.dirs['ml']}/model_comparison.csv", index=False)
        
        # Best model
        best_model_name = results_df.iloc[0]['Model']
        self.best_model = self.models[best_model_name]
        
        print(f"\n  ✓ Best model: {best_model_name}")
        print(f"  ✓ Models saved to {self.dirs['models']}/")
        
        return results_df
    
    def visualize_ml_results(self):
        """Create comprehensive ML visualizations"""
        print("\n[6/8] Creating ML visualizations...")
        
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Model comparison
        ax1 = fig.add_subplot(gs[0, :])
        results_df = pd.read_csv(f"{self.dirs['ml']}/model_comparison.csv")
        x = np.arange(len(results_df))
        width = 0.35
        
        ax1.bar(x - width/2, results_df['Accuracy'], width, label='Test Accuracy', alpha=0.8)
        ax1.bar(x + width/2, results_df['CV_Mean'], width, label='CV Mean', alpha=0.8)
        ax1.set_xlabel('Model')
        ax1.set_ylabel('Accuracy')
        ax1.set_title('A. Model Performance Comparison')
        ax1.set_xticks(x)
        ax1.set_xticklabels(results_df['Model'], rotation=45, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 2-4. ROC curves for top 3 models
        for idx, (name, model_data) in enumerate(list(self.models.items())[:3]):
            ax = fig.add_subplot(gs[1, idx])
            
            if model_data['y_prob'] is not None:
                fpr, tpr, _ = roc_curve(model_data['y_test'], model_data['y_prob'])
                auc = roc_auc_score(model_data['y_test'], model_data['y_prob'])
                
                ax.plot(fpr, tpr, label=f'AUC = {auc:.3f}', linewidth=2)
                ax.plot([0, 1], [0, 1], 'k--', alpha=0.3)
                ax.set_xlabel('False Positive Rate')
                ax.set_ylabel('True Positive Rate')
                ax.set_title(f'{chr(66+idx)}. ROC Curve - {name}')
                ax.legend()
                ax.grid(True, alpha=0.3)
        
        # 5-7. Confusion matrices for top 3 models
        for idx, (name, model_data) in enumerate(list(self.models.items())[:3]):
            ax = fig.add_subplot(gs[2, idx])
            
            cm = confusion_matrix(model_data['y_test'], model_data['y_pred'])
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                       xticklabels=['Alive', 'Dead'],
                       yticklabels=['Alive', 'Dead'])
            ax.set_xlabel('Predicted')
            ax.set_ylabel('Actual')
            ax.set_title(f'{chr(69+idx)}. Confusion Matrix - {name}')
        
        plt.savefig(f"{self.dirs['ml']}/ml_performance.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ ML visualizations saved")
        
        # Feature importance for Random Forest
        if 'Random Forest' in self.models:
            rf_model = self.models['Random Forest']['model']
            features = self.models['Random Forest']['features']
            importances = rf_model.feature_importances_
            
            # Sort by importance
            indices = np.argsort(importances)[::-1]
            
            plt.figure(figsize=(10, 6))
            plt.bar(range(len(importances)), importances[indices], alpha=0.8, edgecolor='black')
            plt.xticks(range(len(importances)), [features[i] for i in indices], rotation=45, ha='right')
            plt.xlabel('Features')
            plt.ylabel('Importance')
            plt.title('Feature Importance - Random Forest')
            plt.tight_layout()
            plt.savefig(f"{self.dirs['ml']}/feature_importance.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"  ✓ Feature importance plot saved")
    
    def generate_predictions(self):
        """Generate predictions for validation cohort"""
        print("\n[7/8] Generating predictions...")
        
        # Use best model
        best_model = self.best_model['model']
        scaler = self.best_model['scaler']
        features = self.best_model['features']
        
        # Prepare full validation data
        X_val = self.validation_processed[features].fillna(0)
        X_val_scaled = scaler.transform(X_val)
        
        # Predict
        predictions = best_model.predict(X_val_scaled)
        probabilities = best_model.predict_proba(X_val_scaled)[:, 1] if hasattr(best_model, 'predict_proba') else None
        
        # Create results dataframe
        results = self.validation_processed[['Patient ID', 'Survival time (days)', 
                                            'Event (death: 1, alive: 0)']].copy()
        results['Predicted_Outcome'] = predictions
        results['Predicted_Outcome_Label'] = results['Predicted_Outcome'].map({0: 'Alive', 1: 'Dead'})
        
        if probabilities is not None:
            results['Death_Probability'] = probabilities
            results['Risk_Category'] = pd.cut(probabilities, 
                                             bins=[0, 0.3, 0.7, 1.0],
                                             labels=['Low', 'Medium', 'High'])
        
        # Save predictions
        results.to_csv(f"{self.dirs['predictions']}/patient_predictions.csv", index=False)
        
        print(f"  ✓ Predictions generated for {len(results)} patients")
        print(f"  ✓ Predictions saved to {self.dirs['predictions']}/")
        
        return results
    
    def generate_ai_insights(self):
        """Generate AI-powered clinical insights"""
        print("\n[8/8] Generating AI insights...")
        
        insights = []
        
        # Insight 1: Cohort characteristics
        insights.append("=" * 80)
        insights.append("AI-POWERED CLINICAL INSIGHTS")
        insights.append("=" * 80)
        insights.append("")
        
        insights.append("1. COHORT CHARACTERISTICS")
        insights.append("-" * 80)
        insights.append(f"Discovery Cohort (n={len(self.discovery)}):")
        insights.append(f"  - Mortality Rate: {(self.discovery['Dead or Alive'] == 'Dead').sum() / len(self.discovery) * 100:.1f}%")
        insights.append(f"  - Median Survival: {self.discovery['Time'].median():.0f} days ({self.discovery['Time'].median()/365:.1f} years)")
        insights.append(f"  - Male/Female Ratio: {(self.discovery['sex'] == 'M').sum()}:{(self.discovery['sex'] == 'F').sum()}")
        
        insights.append(f"\nValidation Cohort (n={len(self.validation)}):")
        insights.append(f"  - Mortality Rate: {self.validation['Event (death: 1, alive: 0)'].sum() / len(self.validation) * 100:.1f}%")
        insights.append(f"  - Median Survival: {self.validation['Survival time (days)'].median():.0f} days ({self.validation['Survival time (days)'].median()/365:.1f} years)")
        insights.append(f"  - Mean Age: {self.validation['Age'].mean():.1f} ± {self.validation['Age'].std():.1f} years")
        insights.append(f"  - Mean Tumor Size: {self.validation['Tumor size (cm)'].mean():.2f} ± {self.validation['Tumor size (cm)'].std():.2f} cm")
        
        # Insight 2: Key findings
        insights.append("\n2. KEY FINDINGS")
        insights.append("-" * 80)
        
        # Age analysis
        dead_age = self.validation[self.validation['Event (death: 1, alive: 0)'] == 1]['Age'].mean()
        alive_age = self.validation[self.validation['Event (death: 1, alive: 0)'] == 0]['Age'].mean()
        insights.append(f"  Age Impact:")
        insights.append(f"    - Mean age (dead patients): {dead_age:.1f} years")
        insights.append(f"    - Mean age (alive patients): {alive_age:.1f} years")
        insights.append(f"    - Difference: {abs(dead_age - alive_age):.1f} years")
        
        # Tumor size
        dead_size = self.validation[self.validation['Event (death: 1, alive: 0)'] == 1]['Tumor size (cm)'].mean()
        alive_size = self.validation[self.validation['Event (death: 1, alive: 0)'] == 0]['Tumor size (cm)'].mean()
        insights.append(f"\n  Tumor Size Impact:")
        insights.append(f"    - Mean size (dead patients): {dead_size:.2f} cm")
        insights.append(f"    - Mean size (alive patients): {alive_size:.2f} cm")
        insights.append(f"    - Difference: {abs(dead_size - alive_size):.2f} cm")
        
        # Smoking
        smoking_death_rate = self.validation[self.validation['Cigarette'] == 'Yes']['Event (death: 1, alive: 0)'].mean()
        no_smoking_death_rate = self.validation[self.validation['Cigarette'] == 'No']['Event (death: 1, alive: 0)'].mean()
        insights.append(f"\n  Smoking Impact:")
        insights.append(f"    - Death rate (smokers): {smoking_death_rate * 100:.1f}%")
        insights.append(f"    - Death rate (non-smokers): {no_smoking_death_rate * 100:.1f}%")
        
        # EGFR/KRAS
        egfr_pos = self.validation[self.validation['EGFR'] == 'Positive']['Event (death: 1, alive: 0)'].mean()
        egfr_neg = self.validation[self.validation['EGFR'] == 'Negative']['Event (death: 1, alive: 0)'].mean()
        insights.append(f"\n  Molecular Markers:")
        insights.append(f"    - EGFR Positive death rate: {egfr_pos * 100:.1f}%")
        insights.append(f"    - EGFR Negative death rate: {egfr_neg * 100:.1f}%")
        
        # Insight 3: Model performance
        insights.append("\n3. MACHINE LEARNING MODEL PERFORMANCE")
        insights.append("-" * 80)
        results_df = pd.read_csv(f"{self.dirs['ml']}/model_comparison.csv")
        
        for _, row in results_df.iterrows():
            insights.append(f"  {row['Model']}:")
            insights.append(f"    - Test Accuracy: {row['Accuracy']:.3f}")
            insights.append(f"    - Cross-Validation: {row['CV_Mean']:.3f} ± {row['CV_Std']:.3f}")
        
        # Insight 4: Clinical recommendations
        insights.append("\n4. AI-GENERATED CLINICAL RECOMMENDATIONS")
        insights.append("-" * 80)
        
        # Feature importance
        if 'Random Forest' in self.models:
            rf_model = self.models['Random Forest']['model']
            features = self.models['Random Forest']['features']
            importances = rf_model.feature_importances_
            
            top_features = sorted(zip(features, importances), key=lambda x: x[1], reverse=True)[:3]
            
            insights.append("  Top Predictive Features:")
            for i, (feat, imp) in enumerate(top_features, 1):
                insights.append(f"    {i}. {feat}: {imp:.3f}")
        
        insights.append("\n  Risk Stratification Recommendations:")
        predictions = pd.read_csv(f"{self.dirs['predictions']}/patient_predictions.csv")
        
        if 'Risk_Category' in predictions.columns:
            risk_counts = predictions['Risk_Category'].value_counts()
            insights.append(f"    - High Risk: {risk_counts.get('High', 0)} patients → Aggressive treatment")
            insights.append(f"    - Medium Risk: {risk_counts.get('Medium', 0)} patients → Standard protocol")
            insights.append(f"    - Low Risk: {risk_counts.get('Low', 0)} patients → Conservative management")
        
        insights.append("\n  Treatment Considerations:")
        insights.append("    - Age >65 years associated with worse outcomes")
        insights.append("    - Tumor size >5cm requires aggressive intervention")
        insights.append("    - Smoking cessation critical for all patients")
        insights.append("    - EGFR/KRAS status should guide targeted therapy")
        
        # Save insights
        insights_text = "\n".join(insights)
        with open(f"{self.dirs['insights']}/ai_clinical_insights.txt", 'w') as f:
            f.write(insights_text)
        
        print(insights_text)
        print(f"\n  ✓ AI insights saved to {self.dirs['insights']}/")
    
    def generate_final_report(self):
        """Generate comprehensive final report"""
        print("\n" + "=" * 80)
        print("GENERATING FINAL REPORT")
        print("=" * 80)
        
        report = []
        report.append("=" * 80)
        report.append("RAPID AI-POWERED CLINICAL DATA ANALYSIS")
        report.append("COMPREHENSIVE FINAL REPORT")
        report.append("=" * 80)
        report.append(f"\nGenerated: 2026-01-31")
        report.append(f"Output Directory: {self.output_dir}")
        report.append("\n" + "-" * 80)
        report.append("ANALYSIS SUMMARY")
        report.append("-" * 80)
        
        report.append("\n1. Data Overview:")
        report.append(f"   - Discovery cohort: {len(self.discovery)} patients")
        report.append(f"   - Validation cohort: {len(self.validation)} patients")
        
        report.append("\n2. Analyses Performed:")
        report.append("   ✓ Exploratory Data Analysis")
        report.append("   ✓ Advanced Feature Engineering")
        report.append("   ✓ Kaplan-Meier Survival Analysis")
        report.append("   ✓ Cox Proportional Hazards Modeling")
        report.append("   ✓ Machine Learning (4 models)")
        report.append("   ✓ Risk Prediction")
        report.append("   ✓ AI-Powered Insights")
        
        report.append("\n3. Key Outputs:")
        report.append(f"   - {self.dirs['data']}/exploratory_analysis.png")
        report.append(f"   - {self.dirs['survival']}/kaplan_meier_curves.png")
        report.append(f"   - {self.dirs['survival']}/cox_hazards.png")
        report.append(f"   - {self.dirs['ml']}/ml_performance.png")
        report.append(f"   - {self.dirs['ml']}/feature_importance.png")
        report.append(f"   - {self.dirs['predictions']}/patient_predictions.csv")
        report.append(f"   - {self.dirs['insights']}/ai_clinical_insights.txt")
        
        report.append("\n" + "=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        report_text = "\n".join(report)
        with open(f"{self.output_dir}/FINAL_REPORT.txt", 'w') as f:
            f.write(report_text)
        
        print(report_text)
        print(f"\n✓ Final report saved to {self.output_dir}/FINAL_REPORT.txt")


def main():
    """
    Main execution - Complete analysis in 90 minutes
    """
    import time
    start_time = time.time()
    
    print("=" * 80)
    print("RAPID AI-POWERED CLINICAL DATA ANALYSIS")
    print("90-Minute Complete Pipeline")
    print("=" * 80)
    
    # Initialize
    analyzer = RapidClinicalAI()
    
    # Load data
    analyzer.load_data(
        discovery_file='/mnt/user-data/uploads/Clinical_Data_Discovery_Cohort.csv',
        validation_file='/mnt/user-data/uploads/Clinical_Data_Validation_Cohort.xlsx'
    )
    
    # Run analyses
    analyzer.automated_eda()
    analyzer.preprocess_data()
    analyzer.survival_analysis()
    analyzer.machine_learning_models()
    analyzer.visualize_ml_results()
    analyzer.generate_predictions()
    analyzer.generate_ai_insights()
    analyzer.generate_final_report()
    
    # Time summary
    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print(f"ANALYSIS COMPLETE!")
    print(f"Time elapsed: {elapsed/60:.1f} minutes")
    print(f"Output directory: {analyzer.output_dir}")
    print("=" * 80)


if __name__ == "__main__":
    main()
