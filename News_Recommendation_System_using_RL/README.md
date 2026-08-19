# News Recommendation System using Reinforcement Learning

Personalized news recommender modeled as a contextual multi-armed bandit.
10 simulated users, 7 RL algorithms compared (Random, Epsilon-Greedy, UCB1,
Thompson Sampling, LinUCB, Q-Learning, DQN). See PROJECT_SUMMARY.md for
full methodology and results.

## Run
1. Open the notebook in Google Colab
2. Upload your news CSV (columns: URL, Title, Category, Group Leader)
3. Run all cells top to bottom

## Results
LinUCB achieved the best performance: 94.9% recommendation accuracy.
Full comparison table in `model_comparison_results.csv`.
