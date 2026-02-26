# 🎨 Ai Creative Analyzer

**Ai Creative Analyzer** is a professional-grade desktop application designed for social media managers and graphic designers. It leverages the multimodal power of **Gemini 2.5 Flash** to provide instant, structured feedback on visual post designs. 

The app audits your designs for spelling, visual hierarchy, layout balance, and platform-specific engagement potential, ensuring your content is "Socialmedia-ready" before you hit publish.

---
## 🚀 1. Initial Setup (First-Time Only)

When you launch the app for the first time, you will see a **System Configuration** popup.

### 🔑 Get Your API Key
Create a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### ✅ Verify Credentials
1. Paste your API key into the popup  
2. Click **Verify Credentials**

### 🔒 Security
- The app checks whether your key is active  
- Once verified, it is saved locally in `config.json`  
- You won’t need to enter it again

---

## 🚀 Key Features

* **AI Design Audit:** Deep-scan analysis of any JPG/PNG post design.
* **High-DPI Support:** Native `CTkImage` implementation ensures a crisp preview on 4K and Retina displays.
* **Secure API Management:** Encrypted-style setup popup that verifies your Gemini API key before saving it locally.
* **Rate-Limit Protection:** Intelligent handling of `429 RESOURCE_EXHAUSTED` errors with user-friendly cooldown notifications.
* **One-Click Copy:** Instantly copy the full AI report to your clipboard for design briefs.

---

## 🛠️ Technical Workflow



1.  **Initialization:** On launch, the app checks for `config.json`. If missing, a verification popup appears.
2.  **Image Processing:** Selected images are handled via `Pillow` and converted for both UI preview and AI analysis.
3.  **Background Threading:** Analysis runs on a separate thread to keep the UI responsive and prevent "Not Responding" errors.
4.  **JSON Parsing:** The AI's raw output is cleaned of markdown backticks and parsed into a structured report.

---

## 📦 Environment Setup (Python)

Follow these steps to set up your development environment in a virtual container.

### 1. Create a Virtual Environment
Open your terminal in the project folder and run:
```bash
python -m venv pip_venv
```
### 2. Activate Virtual Environment
```bash
.\pip_venv\Scripts\activate
```

### 3. Install Dependencies
This will install all the packages listed in requirements.txt
```bash
pip install -r requirements.txt
```


### 3. Install Dependencies
This will install all the packages listed in requirements.txt
```bash
pip install -r requirements.txt
```

