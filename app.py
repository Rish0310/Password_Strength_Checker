import streamlit as st
import numpy as np
import joblib

st.set_page_config(
    page_title='Password Strength Checker',
    page_icon='🔐',
    layout='centered',
    initial_sidebar_state='collapsed'
)

@st.cache_resource
def load_models():
    try:
        clf = joblib.load('password_model.pkl')
        vectorizer = joblib.load('vectorizer.pkl')
        return clf, vectorizer
    except Exception as e:
        st.error(f"Error loading models: {e}")
        st.stop()
        return None, None

clf, vectorizer = load_models()

def predict_password_strength(password):
    """
    Predict password strength with smart corrections
    Returns: (result, probabilities, reason)
    """
    
    if len(password) == 0:
        return 0, [1.0, 0.0, 0.0], "Empty password"
    
    length_pass = len(password)
    
    if length_pass == 0:
        return 0, [1.0, 0.0, 0.0], "Empty password"
    
    length_normalised_lowercase = sum(1 for c in password if c.islower()) / length_pass
    length_normalised_uppercase = sum(1 for c in password if c.isupper()) / length_pass
    length_normalised_digit = sum(1 for c in password if c.isdigit()) / length_pass
    
    sample_array = np.array([password])
    sample_matrix = vectorizer.transform(sample_array)
    
    new_matrix = np.append(
        sample_matrix.toarray(), 
        (length_pass, length_normalised_lowercase, length_normalised_uppercase, length_normalised_digit)
    ).reshape(1, -1)
    
    result = clf.predict(new_matrix)[0]
    probabilities = clf.predict_proba(new_matrix)[0]
    
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    char_types = sum([has_lower, has_upper, has_digit, has_special])
    
    reason = "Model prediction"
    original_result = result
    
    # Rule 1: Very short passwords = WEAK
    if length_pass <= 6:
        result = 0
        reason = "Too short (≤6 characters)"
    
    # Rule 2: Medium-short passwords can't be STRONG
    elif length_pass <= 12 and result == 2:
        result = 1
        reason = "Too short to be strong (≤12 chars)"
    
    # Rule 3: Long passwords with diversity = STRONG
    elif length_pass >= 18 and char_types >= 3:
        # If password is 18+ chars with 3+ character types, it's STRONG
        result = 2
        reason = f"Long password ({length_pass} chars) with good diversity ({char_types}/4 types)"
    
    # Rule 4: Very long passwords = STRONG regardless
    elif length_pass >= 30:
        result = 2
        reason = "Very long password (≥30 chars)"
    
    # Rule 5: Medium-long passwords can't be WEAK
    elif length_pass >= 15 and result == 0:
        result = 1
        reason = "Too long to be weak (≥15 chars)"
    
    return result, probabilities, reason


st.markdown("""
    <style>
    .main {
        padding: 2rem 1rem;
    }
    
    .title-container {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: #666;
        font-weight: 400;
    }
    
    .result-card {
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .result-weak {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .result-normal {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    .result-strong {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
    }
    
    .result-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .info-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 1.5rem 0;
    }
    
    .metric {
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    .stTextInput input {
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    
    .stTextInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    .tip-box {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    
    .tip-title {
        font-weight: 600;
        color: #856404;
        margin-bottom: 0.5rem;
    }
    
    .tip-text {
        color: #856404;
        font-size: 0.95rem;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div class="title-container">
        <h1 class="main-title">🔐 Password Strength Checker</h1>
        <p class="subtitle">ML-Powered Security Analysis</p>
    </div>
""", unsafe_allow_html=True)


password = st.text_input(
    '🔑 Enter your password',
    type='password',
    placeholder='Type your password here...',
    help='Your password is analyzed locally and never stored or transmitted'
)


show_password = st.checkbox('👁️ Show password')
if show_password and password:
    st.code(password, language=None)


if st.button('🔍 Analyze Password', type='primary', use_container_width=True):
    if not password:
        st.warning('⚠️ Please enter a password to analyze')
    else:
        with st.spinner('🔐 Analyzing password strength...'):
            
            result, probabilities, reason = predict_password_strength(password)
            
            strength_names = ['Weak', 'Normal', 'Strong']
            strength_colors = ['weak', 'normal', 'strong']
            strength_emojis = ['🔴', '🟡', '🟢']
            
            
            st.markdown(f"""
                <div class="result-card result-{strength_colors[result]}">
                    <div class="result-title">
                        {strength_emojis[result]} Password Strength: {strength_names[result].upper()}
                    </div>
                    <p style="font-size: 1.1rem; margin-bottom: 0;">
                        {reason}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            
            st.markdown("### 📊 Password Analysis")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                    <div class="metric">
                        <div class="metric-value">{len(password)}</div>
                        <div class="metric-label">Characters</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                lowercase_pct = sum(1 for c in password if c.islower()) / len(password) * 100
                st.markdown(f"""
                    <div class="metric">
                        <div class="metric-value">{lowercase_pct:.0f}%</div>
                        <div class="metric-label">Lowercase</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                uppercase_pct = sum(1 for c in password if c.isupper()) / len(password) * 100
                st.markdown(f"""
                    <div class="metric">
                        <div class="metric-value">{uppercase_pct:.0f}%</div>
                        <div class="metric-label">Uppercase</div>
                    </div>
                """, unsafe_allow_html=True)
            
            col4, col5, col6 = st.columns(3)
            
            with col4:
                digit_pct = sum(1 for c in password if c.isdigit()) / len(password) * 100
                st.markdown(f"""
                    <div class="metric">
                        <div class="metric-value">{digit_pct:.0f}%</div>
                        <div class="metric-label">Digits</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col5:
                special_pct = sum(1 for c in password if not c.isalnum()) / len(password) * 100
                st.markdown(f"""
                    <div class="metric">
                        <div class="metric-value">{special_pct:.0f}%</div>
                        <div class="metric-label">Special Chars</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col6:
                char_types = sum([
                    any(c.islower() for c in password),
                    any(c.isupper() for c in password),
                    any(c.isdigit() for c in password),
                    any(not c.isalnum() for c in password)
                ])
                st.markdown(f"""
                    <div class="metric">
                        <div class="metric-value">{char_types}/4</div>
                        <div class="metric-label">Char Types</div>
                    </div>
                """, unsafe_allow_html=True)
                        
            
            st.markdown("### 💡 Recommendations")
            
            if result == 0:
                st.markdown("""
                    <div class="tip-box">
                        <div class="tip-title">⚠️ Your password is weak. Improve it by:</div>
                        <div class="tip-text">
                            • Increasing length to at least 12 characters<br>
                            • Adding uppercase letters (A-Z)<br>
                            • Including numbers (0-9)<br>
                            • Using special characters (!@#$%^&*)
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            elif result == 1:
                st.markdown("""
                    <div class="tip-box">
                        <div class="tip-title">✅ Your password is decent. Make it stronger by:</div>
                        <div class="tip-text">
                            • Increasing length to 18+ characters<br>
                            • Adding more character variety<br>
                            • Avoiding common words or patterns<br>
                            • Consider using a passphrase
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="tip-box">
                        <div class="tip-title">🎉 Excellent! Your password is strong!</div>
                        <div class="tip-text">
                            • Remember to use unique passwords for each account<br>
                            • Consider using a password manager<br>
                            • Enable two-factor authentication when possible<br>
                            • Change passwords regularly
                        </div>
                    </div>
                """, unsafe_allow_html=True)


st.markdown("---")
st.markdown("### 🧪 Try These Examples")

col1, col2, col3 = st.columns(3)

example_passwords = {
    "Weak": "abc123",
    "Normal": "Password123!",
    "Strong": "TheQuixy#234522wish"
}

with col1:
    if st.button("🔴 Weak Example", use_container_width=True):
        st.info(f"Try: `{example_passwords['Weak']}`")

with col2:
    if st.button("🟡 Normal Example", use_container_width=True):
        st.info(f"Try: `{example_passwords['Normal']}`")

with col3:
    if st.button("🟢 Strong Example", use_container_width=True):
        st.info(f"Try: `{example_passwords['Strong']}`")


with st.sidebar:
    st.markdown("## 📖 About")
    st.markdown("""
        This app uses **Machine Learning** to analyze password strength based on:
        
        - 🔤 **Character patterns** (TF-IDF analysis)
        - 📏 **Length** (18+ chars recommended)
        - 🎨 **Character diversity** (lowercase, uppercase, digits, special)
        
        The model was trained on thousands of passwords with smart correction rules for edge cases.
    """)
    
    st.markdown("## 🎯 Strength Criteria")
    st.markdown("""
        **🔴 Weak:**
        - ≤6 characters, OR
        - Poor character diversity
        
        **🟡 Normal:**
        - 7-17 characters
        - Some character variety
        
        **🟢 Strong:**
        - 18+ characters AND
        - 3+ character types (lowercase, uppercase, digits, special)
    """)
    
    st.markdown("## 🔒 Privacy")
    st.markdown("""
        Your password is:
        - ✅ Analyzed locally
        - ✅ Never stored
        - ✅ Never transmitted
        - ✅ Completely private
    """)
    
    st.markdown("## 💪 Password Tips")
    st.markdown("""
        **Create strong passwords:**
        - Use 18+ characters
        - Mix all character types
        - Avoid dictionary words
        - Use passphrases (e.g., "coffee-Dragon-89-Blue!")
        - Use password managers
        - Enable 2FA when available
    """)
    
    st.markdown("---")
    st.markdown("**Built with ❤️ using:**")
    st.markdown("- Streamlit")
    st.markdown("- Scikit-learn")
    st.markdown("- Logistic Regression")


st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p><strong>🔐 Password Strength Checker</strong></p>
        <p>Powered by Machine Learning • Built with Streamlit</p>
        <p style="font-size: 0.85rem; margin-top: 1rem;">
            ⚠️ This tool provides guidance only. Always follow your organization's password policies.
        </p>
    </div>
""", unsafe_allow_html=True)
