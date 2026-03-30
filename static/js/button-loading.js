/**
 * Simple Button Loading Handler
 * Add this to any page to show loading on button clicks
 */

// Auto-add loading to all navigation links
document.addEventListener('DOMContentLoaded', function() {
    // Add loading to all links that navigate to analysis pages
    const analysisLinks = document.querySelectorAll('a[href*="/pattern-analyzer"], a[href*="/ultimate-predictor"], a[href*="/statistics"], a[href*="/day-to-day"], a[href*="/accuracy-dashboard"]');
    
    analysisLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Show loading overlay
            showLoadingOverlay();
        });
    });
    
    // Add loading to form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            showLoadingOverlay();
        });
    });
});

function showLoadingOverlay() {
    // Check if overlay already exists
    if (document.getElementById('loading-overlay')) return;
    
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
        <div style="text-align: center;">
            <div class="spinner"></div>
            <p style="color: white; margin-top: 20px; font-size: 18px;">Loading predictions...</p>
        </div>
    `;
    document.body.appendChild(overlay);
}

// Remove loading on page load
window.addEventListener('load', function() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
});
