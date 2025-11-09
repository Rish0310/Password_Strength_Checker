# 🔐 Password Strength Checker

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://passwordstrengthchecker-bxvjgmavk4zsafrc5blxnp.streamlit.app/)

**AI-Powered Security Analysis with Machine Learning**

🌐 **[Try Live Demo →](https://passwordstrengthchecker-bxvjgmavk4zsafrc5blxnp.streamlit.app/)**

---

## Features

- Real-time password strength analysis
- Character diversity metrics
- ML-based pattern recognition
- Privacy-focused (no data transmission)

## Tech Stack

- **Python 3.12**
- **Streamlit** - Web interface
- **scikit-learn** - Machine learning
- **Logistic Regression** - Classification model
- **TF-IDF** - Text analysis

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Model Details

- **Algorithm**: Logistic Regression with class balancing
- **Features**: TF-IDF (99) + Length + Character frequencies (3)
- **Classes**: Weak (0), Normal (1), Strong (2)
- **Corrections**: Length-based adjustments for edge cases

## Deployment


Deployed on Streamlit Cloud!



