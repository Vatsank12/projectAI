let metricsData = {
    cpu: [],
    memory: [],
    timestamps: []
};

let notificationsData = [];
let currentMetrics = {};
let ws = null;

const userProfile = {
    fullname: localStorage.getItem('userFullname') || 'Administrator',
    email: localStorage.getItem('userEmail') || 'admin@vigilantai.local',
    bio: localStorage.getItem('userBio') || 'System Administrator',
    theme: localStorage.getItem('userTheme') || 'Dark (Cyberpunk)',
    soundAlerts: localStorage.getItem('userSoundAlerts') !== 'false',
    emailNotifications: localStorage.getItem('userEmailNotifications') === 'true'
};

function checkAuth() {
    if (!localStorage.getItem('user')) {
        window.location.href = '/';
    }
}

function logout() {
    localStorage.removeItem('user');
    window.location.href = '/';
}

function showSection(sectionName) {
    document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
    document.getElementById(sectionName + '-section').classList.remove('hidden');
    
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    event.target.closest('.nav-item').classList.add('active');
}

async function fetchMetrics() {
    try {
        const response = await fetch('/api/metrics/current');
        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.error('Error fetching metrics:', error);
    }
}

function updateDashboard(data) {
    currentMetrics = data;
    
    const cpu = data.cpu;
    const memory = data.memory.percent;
    const disk = data.disk.percent;
    const health = 100 - (cpu * 0.4 + memory * 0.4 + disk * 0.2);
    
    updateMetricDisplay('cpu-value', cpu.toFixed(1) + '%');
    updateMetricDisplay('memory-value', memory.toFixed(1) + '%');
    updateMetricDisplay('disk-value', disk.toFixed(1) + '%');
    updateMetricDisplay('health-value', Math.max(0, health.toFixed(0)));
    
    updateBar('cpu-bar', cpu);
    updateBar('memory-bar', memory);
    updateBar('disk-bar', disk);
    updateBar('health-bar', Math.max(0, health));
    
    metricsData.cpu.push(cpu);
    metricsData.memory.push(memory);
    metricsData.timestamps.push(new Date().toLocaleTimeString());
    
    if (metricsData.cpu.length > 30) {
        metricsData.cpu.shift();
        metricsData.memory.shift();
        metricsData.timestamps.shift();
    }
    
    updateCharts();
    
    document.getElementById('cpu-cores').textContent = navigator.hardwareConcurrency || 'N/A';
    document.getElementById('total-ram').textContent = (data.memory.total / 1024).toFixed(1) + ' GB';
    document.getElementById('disk-total').textContent = (data.disk.total / 1024).toFixed(1) + ' GB';
}

function updateMetricDisplay(elementId, value) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = value;
    }
}

function updateBar(barId, percentage) {
    const bar = document.getElementById(barId);
    if (bar) {
        bar.style.width = percentage + '%';
    }
}

async function loadProcesses() {
    try {
        const response = await fetch('/api/processes/list');
        const processes = await response.json();
        
        const tbody = document.getElementById('processes-list');
        tbody.innerHTML = '';
        
        processes.forEach(proc => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="py-2 px-4">${proc.name}</td>
                <td class="py-2 px-4">${proc.pid}</td>
                <td class="py-2 px-4">${(proc.memory_percent || 0).toFixed(2)}%</td>
                <td class="py-2 px-4">${(proc.cpu_percent || 0).toFixed(2)}%</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading processes:', error);
    }
}

async function loadAlerts() {
    try {
        const response = await fetch('/api/alerts/');
        const alerts = await response.json();
        
        const alertsList = document.getElementById('alerts-list');
        alertsList.innerHTML = '';
        
        if (alerts.length === 0) {
            alertsList.innerHTML = '<p class="text-gray-400">No alerts at this time</p>';
            return;
        }
        
        alerts.slice(0, 20).forEach(alert => {
            const alertEl = document.createElement('div');
            alertEl.className = `p-4 rounded border-l-4 ${alert.severity === 'critical' ? 'border-red-500 bg-red-500/10' : alert.severity === 'high' ? 'border-yellow-500 bg-yellow-500/10' : 'border-cyan-500 bg-cyan-500/10'}`;
            alertEl.innerHTML = `
                <div class="flex justify-between items-start">
                    <div>
                        <h4 class="font-semibold">${alert.title}</h4>
                        <p class="text-sm text-gray-400 mt-1">${alert.message}</p>
                        <p class="text-xs text-gray-500 mt-2">${new Date(alert.timestamp).toLocaleString()}</p>
                    </div>
                    <span class="status-badge ${alert.severity}">${alert.severity.toUpperCase()}</span>
                </div>
            `;
            alertsList.appendChild(alertEl);
        });
    } catch (error) {
        console.error('Error loading alerts:', error);
    }
}

let selectedFiles = [];
let scanProgressInterval = null;
let isScanning = false;

function displayFileQueue() {
    const fileQueue = document.getElementById('file-queue');
    if (selectedFiles.length === 0) {
        fileQueue.innerHTML = '';
        return;
    }

    fileQueue.innerHTML = `
        <div class="border border-cyan-500/30 rounded-lg p-4 bg-cyan-500/5">
            <h4 class="text-sm font-semibold mb-3">Selected Files (${selectedFiles.length})</h4>
            <div class="space-y-2 mb-3 max-h-32 overflow-y-auto">
                ${selectedFiles.map((file, idx) => `
                    <div class="flex justify-between items-center text-sm bg-cyan-500/10 p-2 rounded animate__animated animate__fadeIn">
                        <span class="truncate">${file.name}</span>
                        <span class="text-xs text-gray-400 mr-2">${(file.size / 1024).toFixed(1)} KB</span>
                        <button onclick="removeFile(${idx})" class="text-red-400 hover:text-red-300 ml-2 transition">✕</button>
                    </div>
                `).join('')}
            </div>
            <div class="flex gap-2">
                <button onclick="handleFiles(selectedFiles)" class="flex-1 bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 px-4 py-2 rounded text-sm transition ${isScanning ? 'opacity-50 cursor-not-allowed' : ''}" ${isScanning ? 'disabled' : ''}>
                    ${isScanning ? '🔄 Scanning...' : '🔍 Scan Files'}
                </button>
                <button onclick="clearFileQueue()" class="bg-red-500/20 hover:bg-red-500/30 text-red-300 px-4 py-2 rounded text-sm transition">Clear</button>
            </div>
        </div>
    `;
}

function removeFile(idx) {
    selectedFiles.splice(idx, 1);
    displayFileQueue();
}

function clearFileQueue() {
    selectedFiles = [];
    document.getElementById('fileInput').value = '';
    displayFileQueue();
}

let selectedDirectory = null;
let currentScanMode = 'files';

function setScanMode(mode) {
    currentScanMode = mode;

    // Update tab buttons
    document.getElementById('files-mode-btn').className = mode === 'files'
        ? 'flex-1 py-2 px-4 rounded-md text-sm font-medium transition active bg-cyan-500/20 text-cyan-300'
        : 'flex-1 py-2 px-4 rounded-md text-sm font-medium transition text-gray-400 hover:text-white';

    document.getElementById('directory-mode-btn').className = mode === 'directory'
        ? 'flex-1 py-2 px-4 rounded-md text-sm font-medium transition active bg-purple-500/20 text-purple-300'
        : 'flex-1 py-2 px-4 rounded-md text-sm font-medium transition text-gray-400 hover:text-white';

    // Show/hide modes
    document.getElementById('files-mode').classList.toggle('hidden', mode !== 'files');
    document.getElementById('directory-mode').classList.toggle('hidden', mode !== 'directory');

    // Clear selections when switching
    if (mode === 'files') {
        clearDirectorySelection();
    } else {
        clearFileQueue();
    }
}

function setupFileScanner() {
    const dropZone = document.getElementById('dropZone');
    if (!dropZone) return;

    const fileInput = document.getElementById('fileInput');
    if (!fileInput) return;

    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.style.borderColor = '#06b6d4';
        dropZone.style.backgroundColor = 'rgba(6, 182, 212, 0.2)';
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.style.borderColor = 'rgba(6, 182, 212, 0.5)';
        dropZone.style.backgroundColor = 'transparent';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.style.borderColor = 'rgba(6, 182, 212, 0.5)';
        dropZone.style.backgroundColor = 'transparent';

        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            selectedFiles = Array.from(e.dataTransfer.files);
            displayFileQueue();
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            selectedFiles = Array.from(e.target.files);
            displayFileQueue();
        }
    });

    // Directory scanner setup
    const directoryZone = document.getElementById('directoryZone');
    const directoryInput = document.getElementById('directoryInput');

    if (directoryZone && directoryInput) {
        directoryZone.addEventListener('click', () => {
            directoryInput.click();
        });

        directoryInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files.length > 0) {
                const files = Array.from(e.target.files);
                if (files.length > 0) {
                    // Get the directory path from the first file
                    const filePath = files[0].webkitRelativePath;
                    const dirPath = filePath.split('/')[0];
                    selectedDirectory = {
                        name: dirPath,
                        files: files,
                        path: dirPath
                    };
                    displayDirectorySelection();
                }
            }
        });
    }
}

function displayDirectorySelection() {
    const directoryInfo = document.getElementById('directory-info');
    const selectedDirectoryEl = document.getElementById('selected-directory');

    if (selectedDirectory) {
        selectedDirectoryEl.textContent = `${selectedDirectory.name} (${selectedDirectory.files.length} files)`;
        directoryInfo.classList.remove('hidden');
    } else {
        directoryInfo.classList.add('hidden');
    }
}

function clearDirectorySelection() {
    selectedDirectory = null;
    document.getElementById('directoryInput').value = '';
    displayDirectorySelection();
}

async function scanSelectedDirectory() {
    if (!selectedDirectory || isScanning) return;

    const resultsDiv = document.getElementById('scan-results');
    if (!resultsDiv) return;

    isScanning = true;

    // Show progress UI
    resultsDiv.innerHTML = `
        <div class="scan-progress-container animate__animated animate__fadeIn">
            <div class="flex justify-between items-center mb-4">
                <h4 class="text-lg font-semibold text-purple-400">🔍 Scanning Directory...</h4>
                <button onclick="abortScan()" class="bg-red-500/20 hover:bg-red-500/30 text-red-300 px-4 py-2 rounded text-sm transition abort-btn">
                    🛑 Abort Scan
                </button>
            </div>
            <div class="progress-bar-container mb-4">
                <div class="flex justify-between text-sm mb-2">
                    <span id="progress-text">Preparing directory scan...</span>
                    <span id="progress-percent">0%</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" id="progress-bar" style="width: 0%"></div>
                </div>
            </div>
            <div class="scan-stats grid grid-cols-2 gap-4 text-sm">
                <div>Files Processed: <span id="files-processed">0</span></div>
                <div>Total Files: <span id="total-files">${selectedDirectory.files.length}</span></div>
                <div>Current File: <span id="current-file" class="truncate">...</span></div>
                <div>Elapsed Time: <span id="elapsed-time">0s</span></div>
            </div>
        </div>
    `;

    const startTime = Date.now();
    currentAbortController = new AbortController();

    // Start progress polling
    scanProgressInterval = setInterval(() => {
        updateScanProgress();
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        document.getElementById('elapsed-time').textContent = `${elapsed}s`;
    }, 500);

    try {
        // For directory scanning, we'll use the existing directory scan endpoint
        // First, we need to get the actual directory path - this is tricky with webkitdirectory
        // For now, we'll batch process the files we have
        const formData = new FormData();
        selectedDirectory.files.forEach(file => formData.append('files', file));

        const response = await fetch('/api/scanner/batch-scan', {
            method: 'POST',
            body: formData,
            signal: currentAbortController.signal
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayScanResults(data.results);

    } catch (error) {
        if (error.name === 'AbortError') {
            resultsDiv.innerHTML = '<p class="text-yellow-400">⚠️ Scan aborted by user</p>';
        } else {
            console.error('Error scanning directory:', error);
            resultsDiv.innerHTML = `<p class="text-red-400">❌ Error: ${error.message}</p>`;
            showNotification('Directory scan failed', 'error');
        }
    } finally {
        isScanning = false;
        clearInterval(scanProgressInterval);
        clearDirectorySelection();
        currentAbortController = null;
    }
}

async function handleFiles(files) {
    if (isScanning) return;

    const resultsDiv = document.getElementById('scan-results');
    if (!resultsDiv) return;

    isScanning = true;
    displayFileQueue(); // Update button state

    // Show progress UI
    resultsDiv.innerHTML = `
        <div class="scan-progress-container animate__animated animate__fadeIn">
            <div class="flex justify-between items-center mb-4">
                <h4 class="text-lg font-semibold text-cyan-400">🔍 Scanning Files...</h4>
                <button onclick="abortScan()" class="bg-red-500/20 hover:bg-red-500/30 text-red-300 px-4 py-2 rounded text-sm transition abort-btn">
                    🛑 Abort Scan
                </button>
            </div>
            <div class="progress-bar-container mb-4">
                <div class="flex justify-between text-sm mb-2">
                    <span id="progress-text">Preparing scan...</span>
                    <span id="progress-percent">0%</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" id="progress-bar" style="width: 0%"></div>
                </div>
            </div>
            <div class="scan-stats grid grid-cols-2 gap-4 text-sm">
                <div>Files Processed: <span id="files-processed">0</span></div>
                <div>Total Files: <span id="total-files">${files.length}</span></div>
                <div>Current File: <span id="current-file" class="truncate">...</span></div>
                <div>Elapsed Time: <span id="elapsed-time">0s</span></div>
            </div>
        </div>
    `;

    const startTime = Date.now();
    currentAbortController = new AbortController();

    // Start progress polling
    scanProgressInterval = setInterval(() => {
        updateScanProgress();
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        document.getElementById('elapsed-time').textContent = `${elapsed}s`;
    }, 500);

    try {
        const formData = new FormData();
        files.forEach(file => formData.append('files', file));

        const response = await fetch('/api/scanner/batch-scan', {
            method: 'POST',
            body: formData,
            signal: currentAbortController.signal
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayScanResults(data.results);

    } catch (error) {
        if (error.name === 'AbortError') {
            resultsDiv.innerHTML = '<p class="text-yellow-400">⚠️ Scan aborted by user</p>';
        } else {
            console.error('Error scanning files:', error);
            resultsDiv.innerHTML = `<p class="text-red-400">❌ Error: ${error.message}</p>`;
            showNotification('Scan failed', 'error');
        }
    } finally {
        isScanning = false;
        clearInterval(scanProgressInterval);
        displayFileQueue(); // Update button state
        clearFileQueue();
        currentAbortController = null;
    }
}

async function updateScanProgress() {
    try {
        const response = await fetch('/api/scanner/progress');
        const progress = await response.json();

        if (progress.is_scanning) {
            const progressBar = document.getElementById('progress-bar');
            const progressText = document.getElementById('progress-text');
            const progressPercent = document.getElementById('progress-percent');
            const filesProcessed = document.getElementById('files-processed');
            const currentFile = document.getElementById('current-file');

            if (progressBar) progressBar.style.width = `${progress.progress}%`;
            if (progressPercent) progressPercent.textContent = `${progress.progress}%`;
            if (filesProcessed) filesProcessed.textContent = progress.processed_files;
            if (currentFile) {
                const filename = progress.current_file.split(/[/\\]/).pop() || '...';
                currentFile.textContent = filename.length > 20 ? filename.substring(0, 20) + '...' : filename;
            }

            if (progressText) {
                progressText.textContent = `Scanning: ${progress.processed_files}/${progress.total_files} files`;
            }
        }
    } catch (error) {
        console.error('Error updating progress:', error);
    }
}

// Global abort controller for current scan
let currentAbortController = null;

async function abortScan() {
    try {
        // Abort the frontend request
        if (currentAbortController) {
            currentAbortController.abort();
            currentAbortController = null;
        }

        // Also notify backend to abort
        await fetch('/api/scanner/abort', { method: 'POST' });
        showNotification('Scan abort requested', 'warning');
    } catch (error) {
        console.error('Error aborting scan:', error);
    }
}

function displayScanResults(results) {
    const resultsDiv = document.getElementById('scan-results');
    resultsDiv.innerHTML = '<h4 class="text-lg font-semibold mb-4 text-cyan-400">📋 Scan Results</h4>';

    if (!results || results.length === 0) {
        resultsDiv.innerHTML += '<p class="text-gray-400">No results to display</p>';
        return;
    }

    results.forEach((result, index) => {
        const resultEl = document.createElement('div');
        resultEl.className = 'scan-result-card animate__animated animate__fadeInUp';
        resultEl.style.animationDelay = `${index * 0.1}s`;

        if (result.error) {
            resultEl.className += ' error';
            resultEl.innerHTML = `
                <div class="flex items-start space-x-3">
                    <div class="text-red-400 text-xl">❌</div>
                    <div class="flex-1">
                        <h5 class="font-semibold text-red-400">${result.filename || 'Unknown File'}</h5>
                        <p class="text-sm text-red-300">Error: ${result.error}</p>
                    </div>
                </div>
            `;
        } else {
            const isThreat = result.threat_score >= 50;
            const threatColor = isThreat ? 'red' : 'green';
            const threatIcon = isThreat ? '⚠️' : '✅';

            resultEl.innerHTML = `
                <div class="flex items-start space-x-3">
                    <div class="text-${threatColor}-400 text-xl">${threatIcon}</div>
                    <div class="flex-1">
                        <div class="flex justify-between items-start">
                            <h5 class="font-semibold text-${threatColor}-400">${result.filename}</h5>
                            <span class="status-badge ${result.threat_level?.toLowerCase() || 'unknown'} text-xs">
                                ${result.threat_level || 'UNKNOWN'}
                            </span>
                        </div>

                        <div class="grid grid-cols-2 gap-2 mt-2 text-xs text-gray-400">
                            <div>Size: ${result.size_human || 'N/A'}</div>
                            <div>Type: ${result.mime_type || 'N/A'}</div>
                            <div>Permissions: ${result.permissions || 'N/A'}</div>
                            <div>Age: ${result.file_age_days || 0} days</div>
                        </div>

                        <div class="mt-2">
                            <div class="flex justify-between text-xs mb-1">
                                <span>Threat Score</span>
                                <span>${result.threat_score || 0}/100</span>
                            </div>
                            <div class="threat-bar">
                                <div class="threat-fill ${result.threat_level?.toLowerCase() || 'low'}" style="width: ${result.threat_score || 0}%"></div>
                            </div>
                        </div>

                        ${result.suspicious_indicators && result.suspicious_indicators.length > 0 ?
                            `<div class="mt-2 text-xs text-yellow-400">
                                <strong>Indicators:</strong> ${result.suspicious_indicators.join(', ')}
                            </div>` : ''}

                        <div class="mt-2 text-xs text-gray-500 truncate">
                            Hash: ${result.hash ? result.hash.substring(0, 32) + '...' : 'N/A'}
                        </div>
                    </div>
                </div>
            `;
        }

        resultsDiv.appendChild(resultEl);
    });

    // Summary stats
    const threatCount = results.filter(r => !r.error && r.threat_score >= 50).length;
    const cleanCount = results.filter(r => !r.error && r.threat_score < 50).length;
    const errorCount = results.filter(r => r.error).length;

    const summaryEl = document.createElement('div');
    summaryEl.className = 'scan-summary mt-6 p-4 bg-gray-800/50 rounded-lg animate__animated animate__fadeIn';
    summaryEl.innerHTML = `
        <h5 class="font-semibold mb-3 text-cyan-400">📊 Scan Summary</h5>
        <div class="grid grid-cols-3 gap-4 text-center">
            <div class="summary-stat">
                <div class="text-2xl text-green-400">${cleanCount}</div>
                <div class="text-xs text-gray-400">Clean</div>
            </div>
            <div class="summary-stat">
                <div class="text-2xl text-red-400">${threatCount}</div>
                <div class="text-xs text-gray-400">Threats</div>
            </div>
            <div class="summary-stat">
                <div class="text-2xl text-yellow-400">${errorCount}</div>
                <div class="text-xs text-gray-400">Errors</div>
            </div>
        </div>
    `;

    resultsDiv.appendChild(summaryEl);
}

function toggleAssistant() {
    const panel = document.getElementById('assistant-panel');
    panel.classList.toggle('active');
}

async function sendAssistantMessage() {
    const input = document.getElementById('assistant-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    const messagesDiv = document.getElementById('chat-messages');
    
    const userBubble = document.createElement('div');
    userBubble.className = 'chat-bubble user';
    userBubble.textContent = message;
    messagesDiv.appendChild(userBubble);
    
    input.value = '';
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    const typingBubble = document.createElement('div');
    typingBubble.className = 'typing-indicator';
    typingBubble.innerHTML = '<span></span><span></span><span></span><div class="thinking-text">AI is thinking...</div>';
    messagesDiv.appendChild(typingBubble);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 15000); // Increased to 15 seconds
        
        const response = await fetch(`/api/assistant/message?message=${encodeURIComponent(message)}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        
        if (messagesDiv.contains(typingBubble)) {
            messagesDiv.removeChild(typingBubble);
        }
        
        const aiBubble = document.createElement('div');
        aiBubble.className = 'chat-bubble ai';
        aiBubble.textContent = data.ai_response;
        messagesDiv.appendChild(aiBubble);
        
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    } catch (error) {
        console.error('Error sending message:', error);
        if (messagesDiv.contains(typingBubble)) {
            messagesDiv.removeChild(typingBubble);
        }

        const errorBubble = document.createElement('div');
        errorBubble.className = 'chat-bubble ai';
        errorBubble.style.borderLeftColor = '#ef4444';

        let errorMsg;
        if (error.name === 'AbortError') {
            errorMsg = 'Response timeout - the AI might be busy. Please try again in a moment.';
        } else if (error.message.includes('fetch')) {
            errorMsg = 'Connection error - please check your internet connection and try again.';
        } else if (error.message.includes('500')) {
            errorMsg = 'Server error - the AI service is temporarily unavailable. Please try again.';
        } else {
            errorMsg = `Error: ${error.message || 'Unknown error occurred'}`;
        }

        errorBubble.textContent = errorMsg;
        messagesDiv.appendChild(errorBubble);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        // Show notification for errors
        showNotification('AI Assistant Error', 'error');
    }
}

document.getElementById('assistant-input')?.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendAssistantMessage();
    }
});

function loadProfileData() {
    document.getElementById('profile-username').textContent = userProfile.fullname;
    document.getElementById('fullname').value = userProfile.fullname;
    document.getElementById('email').value = userProfile.email;
    document.getElementById('bio').value = userProfile.bio;
    document.getElementById('theme-select').value = userProfile.theme;
    document.getElementById('notification-sound').checked = userProfile.soundAlerts;
    document.getElementById('email-notifications').checked = userProfile.emailNotifications;
    
    applyTheme(userProfile.theme);
}

function saveProfileChanges() {
    userProfile.fullname = document.getElementById('fullname').value;
    userProfile.email = document.getElementById('email').value;
    userProfile.bio = document.getElementById('bio').value;
    
    localStorage.setItem('userFullname', userProfile.fullname);
    localStorage.setItem('userEmail', userProfile.email);
    localStorage.setItem('userBio', userProfile.bio);
    
    document.getElementById('profile-username').textContent = userProfile.fullname;
    showNotification('Profile updated successfully', 'success');
}

function savePreferences() {
    userProfile.theme = document.getElementById('theme-select').value;
    userProfile.soundAlerts = document.getElementById('notification-sound').checked;
    userProfile.emailNotifications = document.getElementById('email-notifications').checked;
    
    localStorage.setItem('userTheme', userProfile.theme);
    localStorage.setItem('userSoundAlerts', userProfile.soundAlerts);
    localStorage.setItem('userEmailNotifications', userProfile.emailNotifications);
    
    applyTheme(userProfile.theme);
    showNotification('Preferences saved successfully', 'success');
}

function applyTheme(theme) {
    const root = document.documentElement;
    const body = document.body;
    
    if (theme === 'Light') {
        body.style.background = '#f5f5f5';
        body.style.color = '#333';
        root.style.setProperty('--dark-bg', '#f5f5f5');
        root.style.setProperty('--glass-bg', 'rgba(255, 255, 255, 0.9)');
        
        document.querySelectorAll('.metric-card, .glass-card, .profile-section, .report-card').forEach(el => {
            el.style.background = 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(240, 240, 240, 0.7) 100%)';
            el.style.color = '#333';
        });
        
        document.querySelectorAll('.sidebar').forEach(el => {
            el.style.background = 'rgba(240, 240, 240, 0.8)';
            el.style.color = '#333';
        });
        
        document.querySelectorAll('.nav-item').forEach(el => {
            el.style.color = '#666';
        });
        
        showNotification('Switched to Light Theme', 'info');
    } else if (theme === 'Dark (Cyberpunk)') {
        body.style.background = '';
        body.style.color = '';
        root.style.setProperty('--dark-bg', '#0a0e27');
        root.style.setProperty('--glass-bg', 'rgba(15, 23, 42, 0.8)');
        
        document.querySelectorAll('.metric-card, .glass-card, .profile-section, .report-card').forEach(el => {
            el.style.background = '';
            el.style.color = '';
        });
        
        document.querySelectorAll('.sidebar').forEach(el => {
            el.style.background = '';
            el.style.color = '';
        });
        
        document.querySelectorAll('.nav-item').forEach(el => {
            el.style.color = '';
        });
        
        showNotification('Switched to Dark (Cyberpunk) Theme', 'info');
    } else if (theme === 'Auto') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        applyTheme(prefersDark ? 'Dark (Cyberpunk)' : 'Light');
        showNotification('Theme set to Auto', 'info');
    }
}

function changePassword() {
    const current = document.getElementById('current-password').value;
    const newPass = document.getElementById('new-password').value;
    const confirm = document.getElementById('confirm-password').value;
    
    if (!current || !newPass || !confirm) {
        showNotification('Please fill all fields', 'warning');
        return;
    }
    
    if (newPass !== confirm) {
        showNotification('Passwords do not match', 'error');
        return;
    }
    
    if (newPass.length < 6) {
        showNotification('Password must be at least 6 characters', 'warning');
        return;
    }
    
    document.getElementById('current-password').value = '';
    document.getElementById('new-password').value = '';
    document.getElementById('confirm-password').value = '';
    
    showNotification('Password changed successfully', 'success');
}

function switchProfileTab(tabName) {
    document.querySelectorAll('#profile-section .tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('#profile-section .tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');
}

function switchReportTab(tabName) {
    document.querySelectorAll('#reports-section .tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('#reports-section .tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');
}

async function updateAnalytics() {
    if (metricsData.cpu.length === 0) return;
    
    const avgCpu = (metricsData.cpu.reduce((a, b) => a + b, 0) / metricsData.cpu.length).toFixed(1);
    const peakCpu = Math.max(...metricsData.cpu).toFixed(1);
    const avgMemory = (metricsData.memory.reduce((a, b) => a + b, 0) / metricsData.memory.length).toFixed(1);
    const peakMemory = Math.max(...metricsData.memory).toFixed(1);
    
    document.getElementById('avg-cpu').textContent = avgCpu + '%';
    document.getElementById('peak-cpu').textContent = peakCpu + '%';
    document.getElementById('avg-memory').textContent = avgMemory + '%';
    document.getElementById('peak-memory').textContent = peakMemory + '%';
    
    updateReportData(avgCpu, peakCpu, avgMemory, peakMemory);
}

function updateReportData(avgCpu, peakCpu, avgMemory, peakMemory) {
    const currentCpu = metricsData.cpu[metricsData.cpu.length - 1] || 0;
    const currentMemory = metricsData.memory[metricsData.memory.length - 1] || 0;
    
    document.getElementById('report-cpu-current').textContent = currentCpu.toFixed(1) + '%';
    document.getElementById('report-cpu-avg').textContent = avgCpu + '%';
    document.getElementById('report-cpu-bar').style.width = avgCpu + '%';
    
    document.getElementById('report-mem-current').textContent = currentMemory.toFixed(1) + '%';
    document.getElementById('report-mem-avg').textContent = avgMemory + '%';
    document.getElementById('report-mem-bar').style.width = avgMemory + '%';
    
    const health = Math.max(0, 100 - (avgCpu * 0.4 + avgMemory * 0.4 + 20));
    document.getElementById('report-health-score').textContent = Math.round(health);
}

function addNotification(title, message, type = 'info') {
    const notification = {
        id: Date.now(),
        title,
        message,
        type,
        timestamp: new Date(),
        read: false
    };
    
    notificationsData.unshift(notification);
    if (notificationsData.length > 100) notificationsData.pop();
    
    displayNotifications();
    
    if (userProfile.soundAlerts && type !== 'info') {
        playNotificationSound();
    }
}

function displayNotifications() {
    const list = document.getElementById('notifications-list');
    if (!list) return;
    
    list.innerHTML = '';
    
    if (notificationsData.length === 0) {
        list.innerHTML = '<p class="text-gray-400">No notifications</p>';
        return;
    }
    
    notificationsData.slice(0, 50).forEach(notif => {
        const div = document.createElement('div');
        div.className = `notification-item ${notif.read ? '' : 'unread'} ${notif.type}`;
        div.innerHTML = `
            <div class="notification-content">
                <h4>${notif.title}</h4>
                <p>${notif.message}</p>
            </div>
            <div class="notification-time">${notif.timestamp.toLocaleTimeString()}</div>
        `;
        list.appendChild(div);
    });
}

function clearAllNotifications() {
    notificationsData = [];
    displayNotifications();
    showNotification('All notifications cleared', 'success');
}

function showNotification(message, type = 'info') {
    addNotification('System', message, type);
}

function playNotificationSound() {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = 800;
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.1);
}

function updateRangeDisplay(inputId, unit) {
    const input = document.getElementById(inputId);
    const display = document.getElementById(inputId + '-display');
    if (input && display) {
        display.textContent = input.value + unit;
    }
}

window.addEventListener('load', () => {
    checkAuth();
    setupFileScanner();
    loadProfileData();
    
    fetchMetrics();
    setInterval(fetchMetrics, 1000);
    setInterval(updateAnalytics, 2000);
    
    setInterval(loadProcesses, 2000);
    setInterval(loadAlerts, 3000);
    
    addNotification('Welcome', 'VigilantAI Dashboard loaded successfully', 'success');
});
