# Leveraging Large Language Models to Automate MBSE Model Creation for Manufacturing Systems

This project is a Streamlit-based web application that enables users to generate and edit concept-level requirements diagrams for Model-Based Systems Engineering (MBSE) — particularly for manufacturing systems. It integrates with Gaphor, a popular SysML/UML modeling tool, and supports multiple modes of requirement generation including manual input, AI-assisted creation using Perplexity, and uploading/modifying existing `.gaphor` files.

## Description

Creating high-quality MBSE models from scratch can be time-consuming and complex. This tool simplifies that process by leveraging large language models to assist engineers and system designers in building structured requirement diagrams aligned with ISO 15288 standards.

It automates:
- Diagram structure generation (based on user-defined or AI-generated requirements)
- Gaphor-compatible `.gaphor` file formatting
- Requirements visualization using Gaphor desktop app

## Features

- Manual input for up to 20 custom requirements
- AI-powered generation using the Perplexity API
- Upload & modify existing `.gaphor` files with editing/deletion/addition support
- Download generated `.gaphor` files
- Open `.gaphor` files directly in the Gaphor desktop application
- Auto-positioning of requirement blocks for clean diagram layouts

## Tech Stack

- Python 3
- Streamlit
- Perplexity AI API
- Gaphor
- xmltodict, uuid, json, subprocess, tempfile

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/nitinbharadwajnataraj/gaphor_with_llm.git
cd gaphor_with_llm
```

### 2. Set Up a Virtual Environment

```bash
python -m venv .venv
# Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install the Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App

```bash
streamlit run app.py
```

> Replace `app.py` with your main script filename if different.

## External Tools Required

- Gaphor (for opening and visualizing `.gaphor` files): https://gaphor.org/
- Perplexity API Key: https://www.perplexity.ai/ (already added in the code)

## Authors

- Ranjith Mahesh - ranjith.mahesh@st.ovgu.de
- Nitin Bharadwaj Nataraj -  nitin.nataraj@ovgu.de
- Kavyashree Byalya Nanjegowda - kavyashree.byalya@st.ovgu.de

## Resources

- Gaphor Documentation: https://docs.gaphor.org/
- Streamlit Docs: https://docs.streamlit.io/
- ISO/IEC/IEEE 15288 Standard: https://www.iso.org/standard/63711.html

Built to accelerate system modeling with the power of AI and MBSE.
