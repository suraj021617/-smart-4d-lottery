/**
 * Enhanced JavaScript for Smart 4D System
 * Adds real-time updates, notifications, and better UX
 */

// Toast notification system
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Loading overlay
function showLoading() {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.innerHTML = '<div class="spinner"></div>';
    overlay.id = 'loading-overlay';
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) overlay.remove();
}

// Auto-refresh predictions
let autoRefreshInterval = null;

function startAutoRefresh(intervalMinutes = 5) {
    if (autoRefreshInterval) clearInterval(autoRefreshInterval);
    
    autoRefreshInterval = setInterval(() => {
        console.log('Auto-refreshing predictions...');
        refreshPredictions();
    }, intervalMinutes * 60 * 1000);
    
    showToast('Auto-refresh enabled', 'success');
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
        showToast('Auto-refresh disabled', 'info');
    }
}

// Fetch predictions via API
async function refreshPredictions() {
    try {
        showLoading();
        const response = await fetch('/api/v1/predictions?method=advanced&limit=5');
        const data = await response.json();
        
        if (data.success) {
            updatePredictionDisplay(data.data);
            showToast('Predictions updated!', 'success');
        }
    } catch (error) {
        console.error('Prediction refresh error:', error);
        showToast('Failed to refresh predictions', 'error');
    } finally {
        hideLoading();
    }
}

function updatePredictionDisplay(predictions) {
    predictions.forEach((pred, index) => {
        const element = document.getElementById(`prediction-${index}`);
        if (element) {
            element.classList.add('number-flip');
            element.textContent = pred.number;
            setTimeout(() => element.classList.remove('number-flip'), 600);
        }
    });
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy', 'error');
    });
}

// Save prediction
async function savePrediction(numbers, provider, confidence) {
    try {
        const response = await fetch('/save-prediction', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                predicted_numbers: numbers,
                provider: provider,
                confidence: confidence,
                draw_date: new Date().toISOString().split('T')[0],
                methods: 'API'
            })
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            showToast('Prediction saved!', 'success');
        }
    } catch (error) {
        console.error('Save error:', error);
        showToast('Failed to save prediction', 'error');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Smart 4D Enhanced JS loaded');
});

// Export functions
window.SmartLottery = {
    showToast,
    showLoading,
    hideLoading,
    refreshPredictions,
    startAutoRefresh,
    stopAutoRefresh,
    copyToClipboard,
    savePrediction
};
