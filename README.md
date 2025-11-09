# 🔐 Password Strength Checker

An AI-powered password strength analyzer built with Machine Learning and Streamlit.

## Features

- Real-time password strength analysis
- Character diversity metrics
- ML-based pattern recognition
- Privacy-focused (no data transmission)

## Tech Stack

- **Python 3.x**
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
- **Features**: TF-IDF (100) + Length + Character frequencies (4)
- **Classes**: Weak (0), Normal (1), Strong (2)
- **Corrections**: Length-based adjustments for edge cases

## Deployment

Deploy on Streamlit Cloud for free!