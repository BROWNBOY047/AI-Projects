
# News Recommendation System using Reinforcement Learning

## Overview
A personalized news recommendation engine that models recommendation as a
**contextual multi-armed bandit** problem. 10 synthetic users with realistic,
probabilistic interest profiles interact with the system; 7 RL algorithms
are trained and compared on their ability to learn each user's taste.

## Pipeline
1. **Data cleaning** — deduplicated 4577 news articles across 6 categories
2. **Semantic embeddings** — `all-MiniLM-L6-v2` Sentence-Transformer (384-dim)
3. **Topic discovery** — KMeans clustering (K=14, silhouette=0.020) as an auxiliary signal alongside the original human-labeled categories
4. **User simulation** — 10 users, each with a primary + secondary interest and realistic click probabilities
5. **RL environment** — reward = simulated click (Bernoulli draw based on user-category match)
6. **7 RL agents trained & compared**:
   Random Baseline, Epsilon-Greedy, UCB1, Thompson Sampling, LinUCB (contextual, embedding-based), Q-Learning, DQN

## Results

|   Rank | Model                  |   Total Reward |   Final-500 CTR |   Final Regret |   Overall Accuracy (%) |   Last-500 Accuracy (%) |
|-------:|:-----------------------|---------------:|----------------:|---------------:|-----------------------:|------------------------:|
|      1 | LinUCB                 |           2339 |           0.814 |        101.419 |                94.9    |                   100   |
|      2 | Thompson Sampling      |           2305 |           0.81  |        135.419 |                89      |                    97.6 |
|      3 | DQN                    |           2133 |           0.788 |        311.69  |                81.2667 |                    86.6 |
|      4 | Epsilon-Greedy (e=0.1) |           1840 |           0.712 |        600.908 |                54.8667 |                    77   |
|      5 | UCB1                   |           1713 |           0.648 |        727.419 |                53.9    |                    68.6 |
|      6 | Q-Learning             |           1873 |           0.686 |        567.348 |                52      |                    63.2 |
|      7 | Random Baseline        |            896 |           0.314 |       1546.05  |                16.3333 |                    17.4 |

## Winner: LinUCB
- **94.9% overall recommendation accuracy**, **100% accuracy in the final 500 rounds**
- Outperforms all other models because it's the only agent that uses **semantic
  embeddings as context**, letting it generalize across users/categories instead
  of learning each user independently from scratch — the same principle behind
  real-world systems like YouTube/Netflix contextual bandits.

## Tech Stack
- **pandas / numpy** — data handling, simulation
- **sentence-transformers (`all-MiniLM-L6-v2`)** — semantic title embeddings
- **scikit-learn** — KMeans clustering, PCA, silhouette scoring
- **PyTorch** — DQN implementation
- **matplotlib / seaborn** — visualizations
- **joblib** — model persistence
