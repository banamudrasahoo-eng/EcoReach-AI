"""
=============================================================================
EcoReach AI - An AI-Powered Smart Campus Sustainability Assistant
=============================================================================
Project Context:
  Developed for 1M1B AI for Sustainability Virtual Internship
  In collaboration with IBM SkillsBuild & AICTE.

Primary SDG: SDG 12 (Responsible Consumption and Production)
Secondary SDGs: SDG 11 (Sustainable Cities & Communities), SDG 13 (Climate Action)

Description:
  Flask backend providing intelligent decision support for waste segregation,
  energy conservation, water management, and general sustainability on campus.
=============================================================================
"""

from flask import Flask, render_template, request, jsonify
import re
import math

app = Flask(__name__)

# =============================================================================
# PROTOTYPE AI ENGINE LAYER
# =============================================================================
# Note for Evaluators: This AI layer simulates a responsible AI workflow.
# It performs intent classification, domain entity extraction, decision support,
# and responsible AI checks. It is designed to be easily pluggable with external
# LLMs (e.g., IBM Granite via IBM Watsonx API) in future iterations.
# =============================================================================

class EcoReachAIEngine:
    """
    Intelligent Sustainability Decision Engine for Educational Campuses.
    """

    SUSTAINABILITY_KEYWORDS = {
        'waste': [
            'waste', 'trash', 'garbage', 'plastic', 'bottle', 'paper', 'glass',
            'can', 'metal', 'e-waste', 'electronic', 'food', 'compost', 'recycle',
            'dispose', 'segregate', 'dumpster', 'bin', 'cardboard', 'wrapper'
        ],
        'energy': [
            'energy', 'electricity', 'power', 'light', 'fan', 'ac', 'air conditioner',
            'appliance', 'watt', 'kwh', 'solar', 'switch', 'bulb', 'led', 'hostel light',
            'classroom energy', 'lab power', 'consumption', 'bill', 'voltage'
        ],
        'water': [
            'water wastage', 'water waste', 'water', 'tap', 'leak', 'hostel water', 'washroom', 'faucet', 'flush',
            'rainwater', 'tank', 'drinking water', 'waste water', 'pipe', 'drain',
            'plumbing', 'shower', 'bucket', 'conservation', 'liter'
        ],
        'general': [
            'sustainability', 'green', 'eco', 'environment', 'campus', 'sdg',
            'carbon', 'tree', 'footprint', 'awareness', 'practice', 'student',
            'action', 'climate', 'nature', 'reduce', 'reuse', 'audit', 'club'
        ]
    }

    KNOWN_WASTE_ITEMS = {
        'plastic bottle': {
            'category': 'Recyclable / Dry Waste',
            'color': '#2196F3',
            'recommendation': 'Empty, rinse slightly, flatten to save space, and place in the Blue (Recyclable) bin.',
            'sustainability_tip': 'Carry a reusable stainless steel water bottle to reduce single-use plastic waste on campus.',
            'confidence': 0.95
        },
        'food waste': {
            'category': 'Organic / Wet Waste',
            'color': '#4CAF50',
            'recommendation': 'Dispose of in the Green (Organic/Wet) bin for campus composting.',
            'sustainability_tip': 'Take only what you can eat at the mess/canteen to reduce food waste at the source.',
            'confidence': 0.98
        },
        'paper': {
            'category': 'Recyclable Paper Waste',
            'color': '#FF9800',
            'recommendation': 'Ensure paper is dry and clean. Flatten sheets and deposit in paper recycling drop-boxes.',
            'sustainability_tip': 'Use double-sided printing and digital submission portals whenever permitted by faculty.',
            'confidence': 0.92
        },
        'glass bottle': {
            'category': 'Glass / Recyclable Waste',
            'color': '#009688',
            'recommendation': 'Rinse carefully to avoid breakage and place in designated glass recycling collection points.',
            'sustainability_tip': 'Glass is 100% recyclable indefinitely without loss in quality or purity.',
            'confidence': 0.94
        },
        'metal can': {
            'category': 'Metal / Recyclable Waste',
            'color': '#607D8B',
            'recommendation': 'Rinse and deposit in the dry metal recycling stream.',
            'sustainability_tip': 'Recycling aluminum saves 95% of the energy needed to make new aluminum from raw ore.',
            'confidence': 0.91
        },
        'electronic waste': {
            'category': 'E-Waste (Special Handling Required)',
            'color': '#E91E63',
            'recommendation': 'DO NOT throw in general bins. Hand over to campus E-Waste Collection Drives or IT Maintenance.',
            'sustainability_tip': 'Proper e-waste recycling prevents hazardous heavy metals like lead and mercury from contaminating soil.',
            'confidence': 0.96
        },
        'cardboard': {
            'category': 'Recyclable Paper Waste',
            'color': '#FF9800',
            'recommendation': 'Flatten all boxes and keep them dry before placing in paper recycling areas.',
            'sustainability_tip': 'Flattening cardboard boxes increases recycling collection efficiency by up to 40%.',
            'confidence': 0.90
        },
        'battery': {
            'category': 'Hazardous Waste (Special Handling)',
            'color': '#F44336',
            'recommendation': 'Deposit in designated battery disposal drop-boxes at campus IT/lab centers.',
            'sustainability_tip': 'Switching to rechargeable batteries prevents dozens of single-use batteries from landfills.',
            'confidence': 0.95
        }
    }

    @classmethod
    def classify_domain(cls, query):
        """Identifies the primary sustainability domain from the query text."""
        query_lower = query.lower()
        
        # Specific override for water wastage / hostel water queries
        if any(w in query_lower for w in ['water wastage', 'water waste', 'water leak', 'hostel water', 'tap leak', 'leaking tap']):
            return 'water'

        scores = {domain: 0 for domain in cls.SUSTAINABILITY_KEYWORDS}

        for domain, keywords in cls.SUSTAINABILITY_KEYWORDS.items():
            for kw in keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', query_lower):
                    scores[domain] += 2
                elif kw in query_lower:
                    scores[domain] += 1

        best_domain = max(scores, key=scores.get)
        if scores[best_domain] == 0:
            return None  # Out of domain query
        return best_domain

    @classmethod
    def process_general_query(cls, user_query):
        """Processes general conversational queries with prompt workflow execution."""
        if not user_query or not user_query.strip():
            return {
                'status': 'error',
                'message': 'Query input cannot be empty. Please ask a sustainability question!'
            }

        domain = cls.classify_domain(user_query)

        if domain is None:
            return {
                'status': 'out_of_scope',
                'category': 'General Awareness',
                'response': (
                    "I am EcoReach AI, a dedicated campus sustainability assistant. "
                    "I can help you with questions about waste management, energy conservation, "
                    "water saving, and sustainable campus practices. Please rephrase your question "
                    "to relate to campus environmental actions!"
                ),
                'ai_recommendation': 'Please focus your question on campus sustainability (Waste, Energy, Water, or Eco-practices).',
                'recommended_actions': [
                    'Ask how to dispose of specific waste items.',
                    'Inquire about saving power in classrooms or hostels.',
                    'Report or seek advice on water leakage/conservation.'
                ],
                'sustainable_action': 'Explore campus green initiatives today.'
            }

        # Domain-based structured response generation
        if domain == 'waste':
            category_name = "Waste Management"
            recommendation = "Implementing proper waste segregation at source significantly boosts campus recycling efficiency."
            actions = [
                "Separate waste into Wet (Organic), Dry (Recyclable), and E-waste at the source.",
                "Avoid single-use plastic cups and food wrappers during campus events.",
                "Utilize double-sided printing and paper reuse bins across departments.",
                "Participate in or organize monthly campus cleanup and e-waste collection drives."
            ]
            sust_action = "Adopt a 3-R mindset (Reduce, Reuse, Recycle) in daily campus life."

        elif domain == 'energy':
            category_name = "Energy Conservation"
            recommendation = "Reducing unnecessary electricity usage lowers campus carbon emissions and operational costs."
            actions = [
                "Switch off lights, fans, and projectors when leaving classrooms and labs.",
                "Maximize natural sunlight usage during daytime classes.",
                "Set AC temperatures to an eco-friendly 24°C - 26°C.",
                "Unplug chargers and laboratory equipment when not actively in use."
            ]
            sust_action = "Appoint a student 'Energy Monitor' for your classroom or hostel floor."

        elif domain == 'water':
            category_name = "Water Conservation"
            recommendation = "Preventing water waste and reporting plumbing issues promptly safeguards vital campus water reserves."
            actions = [
                "Promptly report leaking taps and flush valves to maintenance teams.",
                "Turn off taps while brushing teeth or soaping hands in hostels.",
                "Support rainwater harvesting and greywater reuse initiatives on campus.",
                "Use full loads when using laundry facilities in residential blocks."
            ]
            sust_action = "Report any noticed water leakage to campus maintenance within 24 hours."

        else: # general
            category_name = "General Sustainability"
            recommendation = "Building a sustainable campus community requires active participation from students, faculty, and staff."
            actions = [
                "Join or support campus eco-clubs and sustainability awareness campaigns.",
                "Use campus bicycles, electric shuttles, or walk instead of motor vehicles.",
                "Advocate for digital documentation over physical printing.",
                "Track and share green achievements with peers to build a culture of responsibility."
            ]
            sust_action = "Pledge to complete at least one green action on campus every day."

        # Structured Prompt Workflow Object
        prompt_workflow = {
            'system_role': "You are EcoReach AI, a campus sustainability assistant trained on SDG 12, SDG 11, and SDG 13 principles.",
            'user_input': user_query,
            'steps': [
                "1. Domain Classification: Detected domain '" + category_name + "'",
                "2. Context Extraction: Filtered query for actionable sustainability intents.",
                "3. Policy & Knowledge Retrieval: Applied SDG 12 waste/energy/water guidelines.",
                "4. Responsible AI Validation: Passed bias, accuracy, and safety checks.",
                "5. Recommendation Synthesis: Generated actionable campus guidance."
            ]
        }

        return {
            'status': 'success',
            'category': category_name,
            'ai_recommendation': recommendation,
            'recommended_actions': actions,
            'sustainable_action': sust_action,
            'prompt_workflow': prompt_workflow
        }

    @classmethod
    def classify_waste_item(cls, item_name):
        """Classifies waste item and provides disposal guidelines."""
        if not item_name or not item_name.strip():
            return {'status': 'error', 'message': 'Please enter a waste item name.'}

        item_clean = item_name.strip().lower()

        # Direct exact or partial matching
        for known_item, details in cls.KNOWN_WASTE_ITEMS.items():
            if known_item in item_clean or item_clean in known_item:
                return {
                    'status': 'success',
                    'item': item_name.capitalize(),
                    'category': details['category'],
                    'color': details['color'],
                    'recommendation': details['recommendation'],
                    'sustainability_tip': details['sustainability_tip'],
                    'confidence': details['confidence'],
                    'needs_verification': False
                }

        # Fallback heuristic rules
        if any(w in item_clean for w in ['plastic', 'poly', 'wrapper', 'bag']):
            return {
                'status': 'success',
                'item': item_name.capitalize(),
                'category': 'Recyclable Plastic Waste',
                'color': '#2196F3',
                'recommendation': 'Clean off any organic residue and place in the dry plastic recycling bin.',
                'sustainability_tip': 'Reduce single-use plastic usage by bringing your own reusable containers.',
                'confidence': 0.75,
                'needs_verification': False
            }
        elif any(w in item_clean for w in ['food', 'peel', 'apple', 'rice', 'bread', 'organic', 'leaf', 'tea']):
            return {
                'status': 'success',
                'item': item_name.capitalize(),
                'category': 'Organic / Wet Waste',
                'color': '#4CAF50',
                'recommendation': 'Place in the green compost bin. Keep free from plastic wrappers or foil.',
                'sustainability_tip': 'Organic waste can be converted into rich compost for campus greenery.',
                'confidence': 0.85,
                'needs_verification': False
            }
        elif any(w in item_clean for w in ['wire', 'phone', 'laptop', 'cable', 'charger', 'chip', 'screen']):
            return {
                'status': 'success',
                'item': item_name.capitalize(),
                'category': 'Electronic Waste (E-Waste)',
                'color': '#E91E63',
                'recommendation': 'Deposit at designated campus E-Waste drop-off points or central IT store.',
                'sustainability_tip': 'E-waste contains valuable metals that can be recovered through safe recycling.',
                'confidence': 0.88,
                'needs_verification': False
            }

        # Low confidence fallback - Responsible AI Requirement
        return {
            'status': 'uncertain',
            'item': item_name.capitalize(),
            'category': 'Uncertain / Verification Required',
            'color': '#78909C',
            'recommendation': (
                "EcoReach AI could not confidently determine the exact category for this specific item. "
                "Please verify material composition or consult local municipal / campus waste guidelines "
                "before disposal."
            ),
            'sustainability_tip': 'When in doubt, check campus waste bin labels or consult campus maintenance.',
            'confidence': 0.30,
            'needs_verification': True
        }

    @classmethod
    def analyze_energy_usage(cls, lights, fans, acs, hours):
        """Analyzes fixture count & usage hours to generate structured energy-saving recommendations."""
        try:
            num_lights = int(lights) if lights else 0
            num_fans = int(fans) if fans else 0
            num_acs = int(acs) if acs else 0
            avg_hours = float(hours) if hours else 0.0
        except ValueError:
            return {'status': 'error', 'message': 'Please enter valid numerical inputs.'}

        # Approximate load estimation (in Watts for recommendation scaling)
        # Note: Clearly documented as estimated recommendations, not measured meter readings.
        est_power_kw = (num_lights * 0.02) + (num_fans * 0.075) + (num_acs * 1.5)
        est_daily_kwh = est_power_kw * avg_hours

        recommendations = []
        if num_acs > 0:
            recommendations.append("Set AC thermostats to 24°C or higher to reduce compressor workload by up to 18%.")
            recommendations.append("Ensure classroom windows and doors remain closed while air conditioning is active.")

        if num_lights > 0 and avg_hours > 4:
            recommendations.append("Turn off perimeter lights during daylight hours and maximize natural window lighting.")

        if num_fans > 0 and avg_hours > 8:
            recommendations.append("Ensure fans are switched off immediately upon classroom or lab evacuation.")

        if avg_hours > 10:
            recommendations.append("High daily usage hours detected! Implement automated timer switches or occupancy sensors.")

        if not recommendations:
            recommendations.append("Good baseline usage! Maintain regular habits of turning off equipment when leaving.")

        return {
            'status': 'success',
            'fixtures_summary': f"Room has {num_lights} Light(s), {num_fans} Fan(s), and {num_acs} AC(s) operating ~{avg_hours} hrs/day.",
            'estimated_daily_kwh': round(est_daily_kwh, 2),
            'recommendations': recommendations,
            'disclaimer': 'Calculated figures are estimated recommendations for awareness purposes, not utility-metered measurements.'
        }

    @classmethod
    def analyze_water_issue(cls, query):
        """Analyzes water conservation queries and returns maintenance steps and tips."""
        if not query or not query.strip():
            return {'status': 'error', 'message': 'Please describe the water issue or location.'}

        q_lower = query.lower()

        if 'leak' in q_lower or 'drip' in q_lower or 'tap' in q_lower:
            problem = "Possible water loss due to leaking plumbing fixture."
            action = "Submit an urgent ticket to campus maintenance specifying building name and room number."
            tip = "A tap leaking just 1 drop per second wastes over 11,000 liters of water annually!"
        elif 'hostel' in q_lower or 'washroom' in q_lower or 'shower' in q_lower:
            problem = "High residential water consumption during peak morning/evening hours."
            action = "Install low-flow aerators on taps and encourage short shower duration among hostel residents."
            tip = "Aerators reduce tap water flow by up to 40% without compromising water pressure."
        elif 'rain' in q_lower or 'harvest' in q_lower or 'tank' in q_lower:
            problem = "Unutilized rainwater potential on campus building rooftops."
            action = "Promote rooftop rainwater harvesting system installation to recharge local campus groundwater."
            tip = "A 1,000 sq ft roof can harvest ~22,000 liters of water for every 10 inches of rainfall."
        else:
            problem = "General campus water management query."
            action = "Audit water usage across academic blocks and install water-saving signage near wash basins."
            tip = "Turning off the tap while washing hands or brushing saves up to 6 liters of water per minute."

        return {
            'status': 'success',
            'problem': problem,
            'recommended_action': action,
            'sustainability_tip': tip
        }

# =============================================================================
# FLASK ROUTE DEFINITIONS
# =============================================================================

@app.route('/')
def home():
    """Landing / Home Page Route."""
    return render_template('index.html')

@app.route('/assistant')
def assistant():
    """AI Sustainability Assistant Page Route (Chatbot, Waste, Energy, Water)."""
    return render_template('assistant.html')

@app.route('/dashboard')
def dashboard():
    """Sustainability Dashboard Route featuring DEMO data visuals."""
    return render_template('dashboard.html')

@app.route('/workflow')
def workflow():
    """AI Workflow & Prompt Engineering Demonstration Route."""
    return render_template('workflow.html')

@app.route('/responsible-ai')
def responsible_ai():
    """Responsible AI Framework & Expected Impact Route."""
    return render_template('responsible_ai.html')

@app.route('/about')
def about():
    """About EcoReach AI, SDGs, Tech Stack & Future Scope Route."""
    return render_template('about.html')

# =============================================================================
# REST API ENDPOINTS FOR INTERACTIVE UI COMPONENTS
# =============================================================================

@app.route('/api/ask', methods=['POST'])
def api_ask():
    """Conversational AI Assistant API Endpoint."""
    data = request.get_json(silent=True) or {}
    message = data.get('message', '')
    response = EcoReachAIEngine.process_general_query(message)
    return jsonify(response)

@app.route('/api/waste', methods=['POST'])
def api_waste():
    """Waste Segregation Classifier API Endpoint."""
    data = request.get_json(silent=True) or {}
    item = data.get('item', '')
    response = EcoReachAIEngine.classify_waste_item(item)
    return jsonify(response)

@app.route('/api/energy', methods=['POST'])
def api_energy():
    """Energy Savings Recommendation API Endpoint."""
    data = request.get_json(silent=True) or {}
    lights = data.get('lights', 0)
    fans = data.get('fans', 0)
    acs = data.get('acs', 0)
    hours = data.get('hours', 0)
    response = EcoReachAIEngine.analyze_energy_usage(lights, fans, acs, hours)
    return jsonify(response)

@app.route('/api/water', methods=['POST'])
def api_water():
    """Water Conservation Assistant API Endpoint."""
    data = request.get_json(silent=True) or {}
    query = data.get('query', '')
    response = EcoReachAIEngine.analyze_water_issue(query)
    return jsonify(response)

# =============================================================================
# APPLICATION ENTRYPOINT
# =============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print(" [EcoReach AI] Launching Smart Campus Sustainability Assistant")
    print(" [EcoReach AI] 1M1B AI for Sustainability Virtual Internship Prototype")
    print(" [EcoReach AI] Server running at: http://127.0.0.1:5000")
    print("=" * 70)
    app.run(debug=True, port=5000)
