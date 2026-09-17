# EcoReach AI – An AI-Powered Smart Campus Sustainability Assistant

Developed for the **1M1B AI for Sustainability Virtual Internship** in collaboration with **IBM SkillsBuild** and **AICTE**.

---

## 📌 Project Overview & Description

**EcoReach AI** is a smart campus sustainability assistant designed to help students, faculty, administrators, and maintenance teams make responsible decisions regarding waste management, energy conservation, and water sustainability.

Educational institutions generate significant daily waste and consume substantial electricity and water. EcoReach AI provides intelligent decision support, waste segregation guidance, energy optimization estimates, water issue tracking, and analytics dashboards to transition campuses into sustainable eco-hubs.

---

## 🎯 Problem Statement

> *"How might we use AI to help students and educational institutions make better decisions about waste, water, and energy consumption so that college campuses can become more sustainable?"*

---

## 🌍 SDG Alignment

- **Primary SDG:** **SDG 12 – Responsible Consumption and Production** (Target 12.5: Substantially reduce waste generation through prevention, reduction, recycling, and reuse).
- **Secondary SDG:** **SDG 11 – Sustainable Cities and Communities** (Target 11.6: Reduce environmental impact of cities/campuses).
- **Secondary SDG:** **SDG 13 – Climate Action** (Target 13.3: Improve education, awareness, and capacity on climate change mitigation).

---

## 👥 Target Users

1. **College Students:** Learn waste disposal rules, hostel water saving tips, and classroom energy habits.
2. **Faculty & Staff:** Adopt eco-friendly classroom practices and digital-first documentation.
3. **Campus Administrators:** Review sustainability analytics to inform institutional green policies.
4. **Maintenance & Sustainability Teams:** Track reported water leaks and waste stream data.

---

## 🚀 Key Features

1. **Modern Sustainability Landing Page:** Includes project overview, SDG alignment badges, problem statement, and quick action buttons.
2. **Conversational AI Sustainability Assistant:** Interactive chatbot that classifies queries into Waste, Energy, Water, or General Sustainability and returns structured recommendations.
3. **Waste Segregation Assistant:** Instant classification of items (plastics, organics, paper, glass, metals, e-waste) into bin categories with recycling tips and confidence scores.
4. **Energy Saver Assistant:** Calculates estimated daily power baseline loads from classroom fixture counts (lights, fans, ACs) and outputs actionable efficiency steps.
5. **Water Conservation Assistant:** Analyzes reported water issues (taps, hostel usage, rainwater harvesting) to generate maintenance actions and saving tips.
6. **Sustainability Dashboard:** Interactive visual charts powered by Chart.js displaying demo metrics for electricity, water, and waste segregation along with automated AI Insights.
7. **AI & Prompt Workflow Visualizer:** 7-step interactive pipeline breakdown and full LLM system/user prompt orchestration demo.
8. **Responsible AI Framework:** Dedicated section covering **Fairness**, **Transparency**, **Ethics**, and **Privacy**, along with explicit AI limitations.
9. **Expected Impact Section:** Comprehensive breakdown of planned sustainability benefits.
10. **About & Future Scope:** Transparent architecture summary and future roadmap items.

---

## 🤖 Role of AI in EcoReach AI

EcoReach AI demonstrates how AI can be responsibly applied to environmental challenges:
- **Classification:** Domain intent detection and waste item material identification.
- **Pattern Recognition:** Identifying high energy consumption patterns based on appliance usage.
- **Knowledge Retrieval:** Mapping query contexts to SDG target guidelines.
- **Conversational Decision Support:** Providing structured actionable guidance for campus users.
- **Responsible Guardrails:** Identifying out-of-domain queries and flagging unverified materials.

---

## 💻 Tech Stack

- **Backend:** Python 3, Flask framework
- **Frontend:** HTML5, CSS3 (Eco Green Design System), JavaScript (ES6+)
- **Visualization:** Chart.js (via CDN)
- **Database / Storage:** Lightweight in-memory Python structures (Zero complex dependencies required)

---

## 📁 Project Structure

```text
EcoReach-AI/
│
├── app.py                  # Main Flask backend & prototype AI engine logic
├── requirements.txt        # Python dependency specifications
├── README.md               # Complete project documentation
│
├── templates/
│   ├── base.html           # Master layout with header, navigation & footer
│   ├── index.html          # Sustainability landing page
│   ├── assistant.html      # 4-in-1 AI Assistant tool hub
│   ├── dashboard.html      # Campus sustainability analytics dashboard
│   ├── workflow.html       # Visual 7-step AI pipeline & prompt workflow
│   ├── responsible_ai.html # Responsible AI principles & expected impact
│   └── about.html          # About project, SDGs, tech stack & future scope
│
└── static/
    ├── css/
    │   └── style.css       # Custom eco-inspired responsive CSS design system
    ├── js/
    │   ├── script.js       # Main application & REST API client interactivity
    │   └── dashboard.js    # Chart.js visualization initialization
    └── assets/             # Project graphics and resources
```

---

## 🛠️ Installation & Setup Instructions

### Prerequisites
- Python 3.8+ installed on your computer.
- VS Code (or standard terminal shell).

### Step 1: Open Terminal in Project Directory
Navigate to the project directory:
```bash
cd EcoReach-AI
```

### Step 2: Install Dependencies
Run the following command to install Flask:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
Start the local Flask development server:
```bash
python app.py
```

### Step 4: Open in Web Browser
Open your browser and navigate to the local Flask URL:
```text
http://127.0.0.1:5000
```

---

## 💬 Example Questions to Try in EcoReach AI

- *"How should I dispose of a plastic bottle?"*
- *"How can I reduce electricity consumption in my classroom?"*
- *"There is a leaking tap in my hostel washroom."*
- *"What are some sustainable practices students can follow?"*
- *"Where do I throw e-waste or old chargers?"*

---

## 🛡️ Responsible AI & Ethical Design

- **Fairness:** Provides equitable, non-discriminatory advice for all campus users.
- **Transparency:** Explicitly labels demo metrics with `Demo Data – For Prototype Demonstration Only`.
- **Ethics:** Avoids misleading environmental claims or unverified greenwashing.
- **Privacy:** Collects zero personal user data or confidential credentials.
- **Limitations:** Advises users to verify specific local municipal waste rules when confidence is low.

---

## 🎯 Expected Impact & Planned Outcomes

- **Increased Segregation Rate:** Higher awareness of wet/dry/e-waste source separation.
- **Energy Conservation:** Reduced classroom energy waste through habit formation.
- **Water Saving:** Faster reporting of campus plumbing leaks.
- **Student Empowerment:** Active engagement with SDG 12, 11, and 13 metrics.

---

## 🚀 Future Scope (Post-Prototype Roadmap)

1. **IBM Granite Integration:** Connecting the prompt workflow to IBM Granite via IBM Watsonx API.
2. **RAG Knowledge Base:** Indexing campus-specific sustainability handbooks and schedules.
3. **IoT Sensor Integration:** Real-time electricity and water smart meter streaming.
4. **Computer Vision Waste Scanner:** Camera-based automated trash classification.
5. **Predictive Analytics:** Forecasting monthly campus utility bills and carbon footprint.

---

*EcoReach AI | 1M1B AI for Sustainability Virtual Internship | IBM SkillsBuild | AICTE*
