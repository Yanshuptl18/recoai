# RecoAI – Session-Based Recommendation System

## Live Demo
https://recoai.streamlit.app/

---

## Table of Contents
- Overview
- Key Features
- Tech Stack
- Dataset
- Approach
  - Candidate Generation
  - Feature Engineering
  - Ranking
- Results
- Optimizations
- Demo
- How to Run
- Key Learnings
- Future Work
- Author
---

## Overview

RecoAI is a scalable session-based recommendation system designed to generate real-time personalized item suggestions using user interaction sequences such as clicks carts and orders.

This project focuses on predicting user intent within a session without relying on long-term user history. It is ideal for anonymous environments like ecommerce platforms.

- 80K plus sessions  
- 1M plus interactions  
- Metric Recall at 20 equals 0.48  
- Latency less than 200ms  

---

## Key Features

- Session based recommendation without user history  
- Hybrid pipeline using co visitation and Bayesian ranking  
- Real time recommendation system  
- Cold start handling for new users  
- Lightweight and optimized deployment  

---

## Tech Stack

- Python  
- Pandas NumPy  
- Scikit learn  
- Bayesian Ranking Model  
- Streamlit frontend  

---

## Dataset

- 80K plus sessions  
- 1M plus user interactions  
- Event types clicks carts orders  

---

## Approach

### Candidate Generation
- Co visitation matrix to find related items  
- Popular items fallback for sparse sessions  

### Feature Engineering
- Recency recent interactions weighted more  
- Frequency interaction count  
- Event weights click less than cart less than order  
- Time decay  

### Ranking
- Bayesian based ranking approach  
- Probability based scoring of item relevance  
- Prioritized high intent actions  
- Optimized for Recall at 20  

---

## Results

| Metric | Value |
|--------|------|
| Recall at 20 | 0.48 |
| Latency | less than 200ms |
| Model Size | 463MB to less than 25MB |

---

## Optimizations

- Top K pruning K equals 20 reduced model size by 95 percent  
- Precomputed co visitation matrix  
- Efficient memory usage less than 1GB RAM  
- Fast inference pipeline  

---

## Demo

- Real time recommendations via Streamlit UI  
- Dynamic session updates  
- Explainable scoring  

---

## How to Run

```bash
git clone https://github.com/yourusername/recoai.git
cd recoai
pip install -r requirements.txt
streamlit run app.py
```
---

## Key Learnings

- Session based models work well for anonymous users  
- Candidate generation is critical for scalability  
- Feature engineering is more important than complex models  
- Optimization is key for real world deployment  

---

## Future Work

- Add deep learning models like GRU4Rec or Transformers  
- Use real time streaming with Kafka  
- Improve personalization with contextual features  

---

## Author

Yanshu Patel  
LinkedIn  
GitHub  

---

