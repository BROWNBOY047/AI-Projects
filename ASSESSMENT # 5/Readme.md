🤖 News Headline Classification — Label Noise Diagnosis & Correction

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white) ![Status](https://img.shields.io/badge/Status-Complete-brightgreen) ![Machine Learning](https://img.shields.io/badge/Machine%20Learning-ScikitLearn-orange?logo=scikitlearn&logoColor=white) ![Embeddings](https://img.shields.io/badge/Embeddings-Sentence--Transformers-blueviolet) ![Label Quality](https://img.shields.io/badge/Label%20Quality-Cleanlab-red) ![Imbalanced Data](https://img.shields.io/badge/Imbalanced%20Data-SMOTE%20%2F%20Class%20Weighting-yellow) ![Ensembling](https://img.shields.io/badge/Ensembling-Voting%20Classifier-9cf) ![Validation](https://img.shields.io/badge/Validation-Cross--Validation-lightgrey) ![Made with](https://img.shields.io/badge/Made%20with-❤️-red)

---

## Overview

This project classifies news headlines into six categories — Business, Markets, Politics, Technology, Health, and Energy — using only the headline text. The initial pipeline showed strong training performance but poor generalization, with a large gap between training and testing accuracy. Rather than treating this purely as a modeling problem, the project investigates and addresses the underlying data quality issue driving that gap.

## Problem Statement

A manually labeled dataset of roughly five thousand headlines was used to train several classical machine learning models. Training accuracy reached the high nineties, while testing accuracy stayed in the low seventies — a large generalization gap. The dataset was also significantly imbalanced across categories, with some classes represented by only a small fraction of the examples available for the largest class.

## Diagnostic Approach

Instead of immediately reaching for more regularization or a different algorithm, the project first asked whether the gap was caused by the model or by the data itself. A confident-learning technique was applied, using cross-validated model predictions to flag headlines whose original label disagreed with what the model consistently and confidently believed the correct label should be. This surfaced a substantial proportion of the dataset as likely mislabeled — closely matching the size of the original accuracy gap, and pointing to label noise as the primary root cause rather than classical overfitting.

## Correction Strategy

Only headlines with high-confidence disagreement were relabeled, to avoid over-trusting any single automated signal. Lower-confidence flags were left untouched, preserving the original human judgment where the evidence for an error wasn't strong. This selective correction aimed to clean the most damaging noise without introducing a new layer of automated mislabeling in its place.

## Feature Representation

Headline text was converted into dense semantic embeddings rather than traditional bag-of-words or keyword-based representations. This allowed the models to capture meaning and context in short headlines, which are often too brief for frequency-based text features to work well.

## Handling Class Imbalance

Two strategies for addressing the imbalance across categories were evaluated: synthetic oversampling of minority classes, and weighting the model's loss function to pay more attention to underrepresented categories during training. The synthetic oversampling approach was found to artificially inflate performance on the smallest categories without genuinely improving generalization, so weighting was adopted as the more reliable approach.

## Modeling Approach

A broad sweep of classical machine learning algorithms was benchmarked to identify strong candidates efficiently. The best-performing approach was then tuned through systematic hyperparameter search, balancing peak accuracy against the size of the train-test gap rather than optimizing for training accuracy alone. Multiple strong models were finally combined into a voting ensemble to further improve robustness by blending different models' error patterns.

## Validation Methodology

The final model's performance was verified using cross-validation across multiple data splits rather than relying on a single train-test split, producing a more trustworthy and stable estimate of real-world accuracy.

## Tech Stack

- **Language:** Python
- **Data Handling:** Pandas, NumPy
- **Text Representation:** Sentence embedding models
- **Label Quality Auditing:** Confident learning framework
- **Classical Machine Learning:** Scikit-learn (discriminant analysis, support vector machines, linear models, ensembling, cross-validation, hyperparameter search)
- **Gradient Boosting (benchmarked):** XGBoost
- **Imbalanced Data Handling:** Synthetic oversampling library (evaluated, not used in final model)
- **Rapid Model Benchmarking:** Automated multi-model comparison tooling
- **Model Persistence:** Joblib

## Outcome

The corrected pipeline substantially reduced the gap between training and testing performance while simultaneously improving testing accuracy, resulting in a model that generalizes meaningfully better than the original baseline. The project also surfaces a broader lesson: a large train-test gap is not always a modeling failure, and diagnosing data quality before tuning algorithms can be the more effective and efficient path to a reliable model.

## Key Learnings

- A generalization gap can originate from label noise rather than model complexity, and this can be diagnosed systematically rather than assumed.
- Synthetic oversampling can create misleading performance improvements on minority classes; loss-based class weighting is often a more honest alternative.
- Semantic embeddings meaningfully outperform frequency-based text features on short text such as headlines.
- Some category boundaries in real-world labeling schemes are inherently ambiguous, and no amount of modeling can fully resolve conceptual overlap between categories — this is a data and problem-definition limitation, not a technical one.
