"""
TextSense: Text Sense & Sentiment Analysis Using Natural Language Processing
Author: Khan Yahya Shahid Ali
UIN: 221A048 | Roll No: 28
Department of Artificial Intelligence & Data Science Engineering
Rizvi College of Engineering | University of Mumbai (2026-2027)
"""

import re
import math
from collections import Counter

# Try importing streamlit and pandas; if not present, provide CLI fallback
try:
    import streamlit as st
    import pandas as pd
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

# ==========================================
# 1. NLP PREDEFINED LEXICONS & STOP WORDS
# ==========================================
POSITIVE_WORDS = {
    'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'superb',
    'outstanding', 'terrific', 'splendid', 'marvelous', 'fabulous', 'awesome',
    'positive', 'happy', 'delighted', 'pleased', 'glad', 'joyful', 'cheerful',
    'love', 'loved', 'loving', 'like', 'liked', 'best', 'better', 'nice', 'sweet',
    'perfect', 'flawless', 'brilliant', 'impressive', 'helpful', 'valuable',
    'effective', 'efficient', 'productive', 'safe', 'secure', 'smooth', 'clean',
    'easy', 'simple', 'fast', 'quick', 'rapid', 'reliable', 'enjoy', 'enjoyed',
    'satisfaction', 'satisfied', 'satisfying', 'success', 'successful', 'win',
    'winner', 'winning', 'recommend', 'recommended', 'worthy', 'worth', 'ideal',
    'smart', 'clever', 'genius', 'bright', 'beautiful', 'attractive', 'fine'
}

NEGATIVE_WORDS = {
    'bad', 'poor', 'terrible', 'horrible', 'awful', 'dreadful', 'atrocious',
    'abysmal', 'inferior', 'subpar', 'negative', 'sad', 'unhappy', 'depressed',
    'angry', 'upset', 'annoyed', 'frustrated', 'irritated', 'hate', 'hated',
    'dislike', 'disliked', 'worst', 'worse', 'flawed', 'broken', 'damaged',
    'defective', 'useless', 'worthless', 'unhelpful', 'ineffective', 'inefficient',
    'slow', 'laggy', 'buggy', 'glitchy', 'hard', 'difficult', 'painful', 'pain',
    'dirty', 'unsafe', 'insecure', 'fail', 'failed', 'failing', 'failure',
    'disaster', 'catastrophe', 'problem', 'issue', 'error', 'mistake', 'loss',
    'lost', 'losing', 'reject', 'rejected', 'disappoint', 'disappointed',
    'disappointing', 'terrible', 'boring', 'ugly', 'stupid', 'dumb', 'waste'
}

STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
    'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
    'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
    'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
    'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
    'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
    'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
    'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's',
    't', 'can', 'will', 'just', 'don', 'should', 'now'
}

# ==========================================
# 2. CORE NLP ANALYSIS ENGINE
# ==========================================
def analyze_text(text: str):
    """
    Performs comprehensive text analysis:
    - Tokenization
    - Rule-based Sentiment Classification
    - Heuristic Score calculation
    - Keyword & Word Frequency Extraction
    - Basic Text Statistics (Words, Sentences, Reading Time)
    """
    raw_text = text.strip()
    if not raw_text:
        return None

    # Tokenization: extract all word tokens (lowercase)
    words = re.findall(r'\b[a-zA-Z]+\b', raw_text.lower())
    total_words = len(words)
    total_chars = len(raw_text)

    # Sentence count: split by . ! ?
    sentences = [s.strip() for s in re.split(r'[.!?]+', raw_text) if s.strip()]
    sentence_count = max(1, len(sentences))

    # Estimated Reading Time (based on standard 200 words per minute)
    reading_time_min = max(1, math.ceil(total_words / 200)) if total_words > 0 else 0

    # Count positive and negative terms
    pos_matches = [w for w in words if w in POSITIVE_WORDS]
    neg_matches = [w for w in words if w in NEGATIVE_WORDS]
    pos_count = len(pos_matches)
    neg_count = len(neg_matches)

    # Sentiment Classification & Heuristic Score
    # Neutral baseline = 50. Positive shifts towards 100, Negative towards 0.
    total_sentiment_terms = pos_count + neg_count
    if total_sentiment_terms == 0:
        sentiment = "Neutral"
        score = 50
        interpretation = "No strong positive or negative sentiment terms were detected in the text."
    else:
        diff = pos_count - neg_count
        # Bound score between 5 and 95
        shift = (diff / max(total_sentiment_terms, 1)) * 40
        score = int(round(50 + shift))
        score = max(5, min(95, score))

        if pos_count > neg_count:
            sentiment = "Positive"
            interpretation = f"Detected {pos_count} positive and {neg_count} negative sentiment terms; overall tone is positive."
        elif neg_count > pos_count:
            sentiment = "Negative"
            interpretation = f"Detected {neg_count} negative and {pos_count} positive sentiment terms; overall tone is negative."
        else:
            sentiment = "Neutral"
            score = 50
            interpretation = f"Detected {pos_count} positive and {neg_count} negative sentiment terms; the counts are equal."

    # Meaningful Words & Keywords (Excluding Stop Words)
    meaningful_words = [w for w in words if w not in STOP_WORDS and len(w) > 1]
    word_freq = Counter(meaningful_words)
    top_freq = word_freq.most_common(10)

    # Key terms list formatted as term (count)
    key_terms = [f"{w} ({c})" for w, c in word_freq.most_common(8)]

    return {
        'sentiment': sentiment,
        'score': score,
        'total_words': total_words,
        'total_chars': total_chars,
        'sentence_count': sentence_count,
        'reading_time_min': reading_time_min,
        'pos_count': pos_count,
        'neg_count': neg_count,
        'pos_matches': pos_matches,
        'neg_matches': neg_matches,
        'interpretation': interpretation,
        'top_freq': top_freq,
        'key_terms': key_terms
    }

# ==========================================
# 3. STREAMLIT WEB DASHBOARD
# ==========================================
def run_streamlit_app():
    st.set_page_config(
        page_title="TextSense - NLP Text Analyzer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Custom CSS for dark card-based dashboard
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.8rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 0px;
            letter-spacing: -0.5px;
        }
        .sub-header {
            font-size: 2.6rem;
            font-weight: 800;
            background: linear-gradient(90deg, #38BDF8, #818CF8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: -10px;
            margin-bottom: 8px;
        }
        .tagline {
            color: #94A3B8;
            font-size: 1.05rem;
            margin-bottom: 25px;
        }
        .metric-card {
            background-color: #0F172A;
            border: 1px solid #1E293B;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }
        .metric-val {
            font-size: 2.2rem;
            font-weight: 700;
            color: #F8FAFC;
        }
        .metric-lbl {
            font-size: 0.85rem;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .sentiment-badge {
            padding: 12px 18px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 15px;
        }
        .sentiment-neutral {
            background-color: #1E293B;
            color: #38BDF8;
            border-left: 5px solid #38BDF8;
        }
        .sentiment-positive {
            background-color: #064E3B;
            color: #34D399;
            border-left: 5px solid #10B981;
        }
        .sentiment-negative {
            background-color: #7F1D1D;
            color: #F87171;
            border-left: 5px solid #EF4444;
        }
        .disclaimer-box {
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 12px 16px;
            color: #CBD5E1;
            font-size: 0.85rem;
            margin-top: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header section
    st.markdown('<div class="main-header">TextSense</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Understand the meaning.</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">A simple NLP dashboard for sentiment analysis, keywords, word frequency, and text statistics.</div>', unsafe_allow_html=True)

    # Initialize session state for text input
    if 'input_text' not in st.session_state:
        st.session_state.input_text = "i have a bad day and i have cig i feel good"

    # Columns layout: Left = Input (01), Right = Results (02)
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 01 / Input text")
        
        # Example buttons
        bcol1, bcol2, bcol3 = st.columns(3)
        if bcol1.button("Positive example"):
            st.session_state.input_text = "The product quality is amazing and fantastic! Fast delivery and excellent customer support."
        if bcol2.button("Negative example"):
            st.session_state.input_text = "The service was terrible and awful. Very slow response, broken package and worst experience."
        if bcol3.button("Mixed example"):
            st.session_state.input_text = "i have a bad day and i have cig i feel good"

        user_text = st.text_area(
            "Enter text to analyze",
            value=st.session_state.input_text,
            height=240,
            label_visibility="collapsed"
        )
        
        analyze_clicked = st.button("✦ Analyze text", type="primary", use_container_width=True)
        st.caption(f"{len(user_text)} characters • Text is processed in this app session.")

    with col2:
        st.markdown("### 02 / Analysis results")
        
        results = analyze_text(user_text)
        if results:
            # Sentiment Badge
            badge_class = (
                "sentiment-positive" if results['sentiment'] == "Positive"
                else "sentiment-negative" if results['sentiment'] == "Negative"
                else "sentiment-neutral"
            )
            st.markdown(
                f'<div class="sentiment-badge {badge_class}">Detected sentiment: {results["sentiment"]}</div>',
                unsafe_allow_html=True
            )

            # Heuristic score progress
            st.write(f"**Heuristic sentiment score:** {results['score']} / 100")
            st.progress(results['score'] / 100.0)

            # Statistics 3-column cards
            mcol1, mcol2, mcol3 = st.columns(3)
            with mcol1:
                st.markdown(f'<div class="metric-card"><div class="metric-lbl">Words</div><div class="metric-val">{results["total_words"]}</div></div>', unsafe_allow_html=True)
            with mcol2:
                st.markdown(f'<div class="metric-card"><div class="metric-lbl">Sentences</div><div class="metric-val">{results["sentence_count"]}</div></div>', unsafe_allow_html=True)
            with mcol3:
                st.markdown(f'<div class="metric-card"><div class="metric-lbl">Reading time</div><div class="metric-val">{results["reading_time_min"]} min</div></div>', unsafe_allow_html=True)

            st.markdown("---")

            # Key terms
            st.markdown("#### Key terms")
            if results['key_terms']:
                st.write(" • ".join(results['key_terms']))
            else:
                st.write("No distinct key terms found.")

            # Most frequent meaningful words chart
            st.markdown("#### Most frequent meaningful words")
            if results['top_freq']:
                chart_df = pd.DataFrame(results['top_freq'], columns=['Word', 'Frequency'])
                chart_df = chart_df.sort_values(by='Frequency', ascending=True)
                st.bar_chart(chart_df.set_index('Word'), horizontal=True, color="#38BDF8")
            else:
                st.info("No frequent meaningful words to display.")

            # Quick interpretation
            st.markdown("#### Quick interpretation")
            st.write(results['interpretation'])
        else:
            st.info("Please enter some text in the left panel and click 'Analyze text'.")

    # Lower expandable section
    with st.expander("› How does the NLP pipeline work?"):
        st.markdown("""
        **TextSense Pipeline Steps:**
        1. **Text Normalization & Tokenization**: Raw user text is converted to lowercase and cleaned of punctuation using regular expressions (`\\b[a-zA-Z]+\\b`).
        2. **Stop-word Filtering**: High-frequency grammatical words (e.g., *the, is, and, i, have*) are filtered out using an optimized stop-word vocabulary.
        3. **Lexicon Sentiment Matching**: Remaining tokens are cross-referenced with curated positive and negative sentiment lexicons.
        4. **Heuristic Scoring**: A balanced score on a scale from 0 to 100 is computed based on relative term dominance.
        5. **Frequency Distribution**: Most frequent meaningful words are ranked and visualized using horizontal frequency bars.
        """)

    # Project Limitation Note
    st.markdown("""
        <div class="disclaimer-box">
            <strong>Project limitation:</strong> This is a rule-based educational prototype developed for the NLP Lab Mini-Project, not a large pre-trained transformer model. It can misread negation ("not good"), sarcasm, complex context, and colloquial slang. The score is a heuristic index, not a Bayesian probability.
        </div>
    """, unsafe_allow_html=True)

    # Footer attribution
    st.markdown("---")
    fcol1, fcol2 = st.columns([1, 1])
    with fcol1:
        st.caption("TextSense • Python + Streamlit • Natural Language Processing Lab Mini-Project")
    with fcol2:
        st.caption("Developed by **Khan Yahya Shahid Ali** (UIN: 221A048 | Roll No: 28) • Rizvi College of Engineering")


# ==========================================
# 4. STANDALONE CLI FALLBACK
# ==========================================
def run_cli_demo():
    print("=" * 65)
    print("  TextSense: Text Sense & Sentiment Analysis (NLP Mini-Project)")
    print("  Author: Khan Yahya Shahid Ali | UIN: 221A048 | Roll: 28")
    print("  Rizvi College of Engineering - University of Mumbai (2026-2027)")
    print("=" * 65)
    
    sample_texts = [
        "The product quality is amazing and fantastic! Fast delivery and excellent customer support.",
        "The service was terrible and awful. Very slow response, broken package and worst experience.",
        "i have a bad day and i have cig i feel good"
    ]
    
    for i, txt in enumerate(sample_texts, 1):
        print(f"\n[Test Case {i}]: \"{txt}\"")
        res = analyze_text(txt)
        print(f"  • Sentiment:       {res['sentiment']}")
        print(f"  • Heuristic Score: {res['score']}/100")
        print(f"  • Words/Sentences: {res['total_words']} words, {res['sentence_count']} sentence(s)")
        print(f"  • Key Terms:       {', '.join(res['key_terms'][:5])}")
        print(f"  • Interpretation:  {res['interpretation']}")
    
    print("\n" + "=" * 65)
    print("To launch the interactive web dashboard:")
    print("  1. pip install streamlit pandas")
    print("  2. streamlit run app.py")
    print("=" * 65)


if __name__ == '__main__':
    if HAS_STREAMLIT:
        try:
            # Check if running under streamlit runtime
            from streamlit.runtime.scriptrunner import get_script_run_ctx
            if get_script_run_ctx():
                run_streamlit_app()
            else:
                run_cli_demo()
        except Exception:
            run_cli_demo()
    else:
        run_cli_demo()
