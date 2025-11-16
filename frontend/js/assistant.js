async function loadAssistantHistory() {
    try {
        const response = await fetch('/api/assistant/history');
        const history = await response.json();
        
        const messagesDiv = document.getElementById('chat-messages');
        if (!messagesDiv || history.length === 0) return;
        
        messagesDiv.innerHTML = '';
        
        history.slice(-10).forEach(conv => {
            const userBubble = document.createElement('div');
            userBubble.className = 'chat-bubble user';
            userBubble.textContent = conv.user_message;
            messagesDiv.appendChild(userBubble);
            
            const aiBubble = document.createElement('div');
            aiBubble.className = 'chat-bubble ai';
            aiBubble.textContent = conv.ai_response;
            messagesDiv.appendChild(aiBubble);
        });
        
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    } catch (error) {
        console.error('Error loading assistant history:', error);
    }
}

async function getHealthInsight() {
    try {
        const response = await fetch('/api/assistant/health-insight');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error getting health insight:', error);
        return null;
    }
}

async function getQuickActions() {
    try {
        const response = await fetch('/api/assistant/quick-actions');
        const actions = await response.json();
        return actions;
    } catch (error) {
        console.error('Error getting quick actions:', error);
        return [];
    }
}

window.addEventListener('load', () => {
    setTimeout(loadAssistantHistory, 500);
});
