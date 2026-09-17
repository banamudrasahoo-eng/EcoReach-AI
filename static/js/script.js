/**
 * EcoReach AI - Main Application Script
 * Developed for 1M1B AI for Sustainability Virtual Internship
 */

document.addEventListener('DOMContentLoaded', () => {

    // =========================================================================
    // 1. NAVIGATION & TAB SYSTEM
    // =========================================================================
    
    // Mobile Nav Toggle
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // Assistant Tab Switching
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');

            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            button.classList.add('active');
            const activeContent = document.getElementById(targetTab);
            if (activeContent) {
                activeContent.classList.add('active');
            }
        });
    });

    // =========================================================================
    // 2. CHATBOT ASSISTANT LOGIC
    // =========================================================================
    
    const chatMessages = document.getElementById('chatMessages');
    const chatInput = document.getElementById('chatInput');
    const btnSend = document.getElementById('btnSend');

    if (chatInput && btnSend) {
        btnSend.addEventListener('click', sendChatMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendChatMessage();
        });
    }

    function sendChatMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        // Render User Message
        appendMessage('user', text);
        chatInput.value = '';

        // Show Typing Indicator
        const typingId = appendTypingIndicator();

        // Call Backend API
        fetch('/api/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        })
        .then(res => res.json())
        .then(data => {
            removeTypingIndicator(typingId);
            if (data.status === 'success' || data.status === 'out_of_scope') {
                renderAssistantResponse(data);
            } else {
                appendMessage('assistant', `⚠️ ${data.message || 'An error occurred.'}`);
            }
        })
        .catch(err => {
            removeTypingIndicator(typingId);
            console.error('Chat error:', err);
            appendMessage('assistant', '⚠️ Unable to connect to EcoReach AI service. Please try again.');
        });
    }

    function appendMessage(sender, contentText) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.innerHTML = sender === 'user' ? '👤' : '🌱';

        const content = document.createElement('div');
        content.className = 'message-content';
        content.textContent = contentText;

        msgDiv.appendChild(avatar);
        msgDiv.appendChild(content);

        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function renderAssistantResponse(data) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message assistant';

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.innerHTML = '🌱';

        const content = document.createElement('div');
        content.className = 'message-content';

        let html = `<span class="category-tag">Category: ${data.category || 'General'}</span>`;
        
        if (data.ai_recommendation) {
            html += `<p style="font-weight:600; margin-bottom:0.5rem; color:#1b4332;">💡 AI Recommendation:</p>`;
            html += `<p style="margin-bottom:0.75rem;">${data.ai_recommendation}</p>`;
        }

        if (data.recommended_actions && data.recommended_actions.length > 0) {
            html += `<div class="rec-box">`;
            html += `<h4>📋 Recommended Actions:</h4><ul>`;
            data.recommended_actions.forEach(act => {
                html += `<li>${act}</li>`;
            });
            html += `</ul></div>`;
        }

        if (data.sustainable_action) {
            html += `<div class="sust-action-banner">🌱 Sustainable Action: ${data.sustainable_action}</div>`;
        }

        content.innerHTML = html;
        msgDiv.appendChild(avatar);
        msgDiv.appendChild(content);

        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function appendTypingIndicator() {
        const id = 'typing_' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message assistant';
        msgDiv.id = id;

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.innerHTML = '🌱';

        const content = document.createElement('div');
        content.className = 'message-content';
        content.style.fontStyle = 'italic';
        content.style.color = '#6b7280';
        content.textContent = 'EcoReach AI is processing your request...';

        msgDiv.appendChild(avatar);
        msgDiv.appendChild(content);
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    // Helper for suggested prompt chips
    window.setPrompt = function(promptText) {
        if (chatInput) {
            chatInput.value = promptText;
            sendChatMessage();
        }
    };

    // =========================================================================
    // 3. WASTE SEGREGATION TOOL
    // =========================================================================

    const btnClassifyWaste = document.getElementById('btnClassifyWaste');
    const wasteInput = document.getElementById('wasteInput');
    const wasteResultCard = document.getElementById('wasteResultCard');

    if (btnClassifyWaste && wasteInput) {
        btnClassifyWaste.addEventListener('click', () => {
            const item = wasteInput.value.trim();
            if (!item) return;

            fetch('/api/waste', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ item: item })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success' || data.status === 'uncertain') {
                    wasteResultCard.style.display = 'block';
                    wasteResultCard.innerHTML = `
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
                            <h3 style="color:${data.color || '#1b4332'};">📦 ${data.item}</h3>
                            <span class="category-tag" style="background:${data.color}; color:white;">${data.category}</span>
                        </div>
                        <p><strong>Recommended Disposal:</strong> ${data.recommendation}</p>
                        <p style="margin-top:0.5rem;"><strong>💡 Sustainability Tip:</strong> ${data.sustainability_tip}</p>
                        ${data.needs_verification ? `
                            <div style="margin-top:0.75rem; padding:0.5rem; background:#fff3cd; color:#856404; border-radius:6px; font-size:0.85rem;">
                                ⚠️ <strong>Note:</strong> EcoReach AI recommends verifying with local campus waste rules if material composition is uncertain.
                            </div>` : ''}
                    `;
                } else {
                    alert(data.message || 'Error classifying waste item.');
                }
            })
            .catch(err => console.error('Waste classification error:', err));
        });
    }

    // Quick Waste Pill Selectors
    window.quickSelectWaste = function(itemName) {
        if (wasteInput) {
            wasteInput.value = itemName;
            if (btnClassifyWaste) btnClassifyWaste.click();
        }
    };

    // =========================================================================
    // 4. ENERGY SAVINGS CALCULATOR TOOL
    // =========================================================================

    const btnCalcEnergy = document.getElementById('btnCalcEnergy');
    const energyResultCard = document.getElementById('energyResultCard');

    if (btnCalcEnergy) {
        btnCalcEnergy.addEventListener('click', () => {
            const lights = document.getElementById('numLights').value;
            const fans = document.getElementById('numFans').value;
            const acs = document.getElementById('numACs').value;
            const hours = document.getElementById('usageHours').value;

            fetch('/api/energy', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lights, fans, acs, hours })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    energyResultCard.style.display = 'block';
                    let recsHtml = data.recommendations.map(r => `<li>${r}</li>`).join('');
                    energyResultCard.innerHTML = `
                        <h3 style="color:var(--primary-color); margin-bottom:0.5rem;">⚡ Energy Recommendations</h3>
                        <p style="font-size:0.95rem; color:var(--text-secondary); margin-bottom:0.75rem;">${data.fixtures_summary}</p>
                        <div style="background:white; padding:0.75rem; border-radius:8px; border:1px solid #e5e7eb; margin-bottom:0.75rem;">
                            <strong>Estimated Baseline Load:</strong> ~${data.estimated_daily_kwh} kWh / day
                        </div>
                        <h4 style="color:var(--secondary-color); font-size:0.95rem; margin-bottom:0.4rem;">Actionable Advice:</h4>
                        <ul style="padding-left:1.2rem; font-size:0.92rem; color:var(--text-secondary);">${recsHtml}</ul>
                        <p style="font-size:0.78rem; color:#888; margin-top:0.75rem; font-style:italic;">* ${data.disclaimer}</p>
                    `;
                } else {
                    alert(data.message || 'Error processing energy data.');
                }
            })
            .catch(err => console.error('Energy calculation error:', err));
        });
    }

    // =========================================================================
    // 5. WATER CONSERVATION TOOL
    // =========================================================================

    const btnAnalyzeWater = document.getElementById('btnAnalyzeWater');
    const waterInput = document.getElementById('waterInput');
    const waterResultCard = document.getElementById('waterResultCard');

    if (btnAnalyzeWater && waterInput) {
        btnAnalyzeWater.addEventListener('click', () => {
            const query = waterInput.value.trim();
            if (!query) return;

            fetch('/api/water', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    waterResultCard.style.display = 'block';
                    waterResultCard.innerHTML = `
                        <h3 style="color:#0288d1; margin-bottom:0.5rem;">💧 Water Sustainability Assessment</h3>
                        <p><strong>Problem Identified:</strong> ${data.problem}</p>
                        <p style="margin-top:0.5rem;"><strong>Recommended Action:</strong> ${data.recommended_action}</p>
                        <div class="sust-action-banner" style="margin-top:0.75rem;">
                            💡 <strong>Sustainability Tip:</strong> ${data.sustainability_tip}
                        </div>
                    `;
                } else {
                    alert(data.message || 'Error analyzing water query.');
                }
            })
            .catch(err => console.error('Water analysis error:', err));
        });
    }
});
