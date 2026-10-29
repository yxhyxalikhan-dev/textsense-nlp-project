# TextSense: Natural Language Processing Text Sense & Sentiment Analyzer

![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red?logo=streamlit)
![Domain](https://img.shields.io/badge/Domain-Natural%20Language%20Processing-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

> **Mini-Project of Natural Language Processing Lab**  
> Submitted in partial fulfillment of the requirements for the Fourth Year of Bachelor of Engineering in **Artificial Intelligence & Data Science**  
> **University of Mumbai** (Academic Year 2026–2027)

---

## 👨‍🎓 Project Credits & Academic Details

- **Student Name:** Khan Yahya Shahid Ali
- **Roll No:** 28
- **UIN:** 221A048
- **Department:** Department of Artificial Intelligence & Data Science Engineering
- **Institution:** Rizvi College of Engineering, Bandra (W), Mumbai
- **Affiliation:** University of Mumbai
- **Project Guide:** Prof. Vijay Shankar

---

## 📌 Project Overview

**TextSense** is an interactive, web-based Natural Language Processing (NLP) dashboard developed using **Python** and the **Streamlit** framework. The primary goal of TextSense is to automate the analysis of unstructured textual data (such as product reviews, user comments, articles, and feedback) without depending on heavy third-party cloud APIs or paid services.

The system performs:
1. **Rule-Based Sentiment Analysis:** Evaluates text polarity (Positive, Negative, or Neutral) and generates a calibrated heuristic sentiment score (0 to 100).
2. **Text Statistics:** Automatically computes total word count, sentence count, character length, and estimated reading time.
3. **Keyword Extraction & Stop-word Removal:** Filters grammatical noise and isolates primary semantic key terms.
4. **Word Frequency Distribution:** Generates real-time horizontal bar charts illustrating the most frequent meaningful terms.
5. **Interactive UI:** Provides quick preset test buttons (*Positive*, *Negative*, *Mixed*) and immediate graphical feedback.

---

## 🏗️ System Architecture & NLP Pipeline

```
[ User Text Input ]
        │
        ▼
[ Tokenization (Regex: \b[a-zA-Z]+\b) ]
        │
        ├───► [ Stop-word Filtering (High-frequency grammatical words removal) ]
        │            │
        │            ▼
        │     [ Keyword Extraction & Term Frequency Counter ] ──► [ Bar Chart Visualization ]
        │
        ├───► [ Lexicon Cross-Referencing (Positive / Negative Vocabularies) ]
        │            │
        │            ▼
        │     [ Term Difference & Heuristic Scoring (0 - 100) ] ──► [ Sentiment Badge (Pos/Neg/Neu) ]
        │
        └───► [ Document Statistics: Sentence Split, Word Count, Reading Time ]
```

---

## 📸 Application Screenshot

![TextSense Dashboard](reports/Figure1_TextSense_Dashboard.png)

---

## 🚀 Getting Started Locally

### 1. Clone the Repository
```bash
git clone https://github.com/yxhyxalikhan-dev/textsense-nlp-project.git
cd textsense-nlp-project
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Dashboard
```bash
streamlit run app.py
```
*Alternatively, run in headless CLI mode:*
```bash
python3 app.py
```

The application will launch automatically in your default browser at `http://localhost:8501`.

---

## 📊 Sample Test Results

| Test Case | Input Sample | Detected Sentiment | Score | Key Terms Identified |
|---|---|---|---|---|
| **Positive** | *"The product quality is amazing and fantastic! Fast delivery and excellent support."* | **Positive** | 90 / 100 | product (1), quality (1), amazing (1), fantastic (1), fast (1) |
| **Negative** | *"The service was terrible and awful. Very slow response, broken package."* | **Negative** | 10 / 100 | service (1), terrible (1), awful (1), slow (1), response (1) |
| **Mixed / Neutral** | *"i have a bad day and i have cig i feel good"* | **Neutral** | 50 / 100 | bad (1), day (1), cig (1), feel (1), good (1) |

---

## 📂 Repository Structure

```
textsense-nlp-project/
├── app.py                      # Main Streamlit NLP Application & CLI engine
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation and guide
├── .gitignore                  # Git ignore file
└── reports/                    # Academic Lab Project Reports
    ├── Khan_Yahya_Shahid_Ali_NLP_Mini_Project_Report.docx  # Word Report
    ├── Khan_Yahya_Shahid_Ali_NLP_Mini_Project_Report.pdf   # Print-Ready PDF
    └── Figure1_TextSense_Dashboard.png                    # Dashboard UI Screenshot
```

---

## ⚠️ Limitations & Future Scope

- **Rule-Based Limitation:** As an educational prototype utilizing lexicon matching, the model may misinterpret sarcasm, double negation (e.g., *"not bad"*), or colloquial internet slang.
- **Future Scope:** Integration of transformer-based embeddings (BERT / RoBERTa / DistilBERT), VADER sentiment intensity scoring, and multilingual tokenization.

---

## 📜 Academic Declaration

This submission represents bonafide academic work developed by **Khan Yahya Shahid Ali (221A048 / Roll No: 28)** for the **Natural Language Processing Lab Mini-Project**, Department of Artificial Intelligence & Data Science Engineering, Rizvi College of Engineering, affiliated with the University of Mumbai.
