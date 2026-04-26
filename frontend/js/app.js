import { initUpload } from './upload.js';
import { initResults } from './results.js';
import { healthCheck } from './api.js';

// Global Application State
const appState = {
    file: null,
    filename: null,
    result: null
};

// Simple router
function navigate(viewId) {
    // Hide all views
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });
    
    // Deactivate all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active', 'text-primary');
    });
    
    // Show target view
    const targetView = document.getElementById(viewId);
    if (targetView) {
        targetView.classList.add('active');
    }
    
    // Highlight active nav link (if exists)
    const activeLink = document.querySelector(`[data-view="${viewId}"]`);
    if (activeLink) {
        activeLink.classList.add('active', 'text-primary');
    }

    // Trigger specific view logic
    if (viewId === 'view-result' && window.renderResultsFn) {
        window.renderResultsFn();
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    // Check Health
    const health = await healthCheck();
    if (!health.weights_loaded && health.status !== 'error') {
        const banner = document.getElementById('healthBanner');
        if (banner) banner.classList.remove('hidden');
    }

    // Initialize modules
    initUpload(appState, navigate);
    window.renderResultsFn = initResults(appState, navigate);

    // Setup navigation listeners
    document.querySelectorAll('[data-view]').forEach(el => {
        el.addEventListener('click', (e) => {
            e.preventDefault();
            const targetView = e.currentTarget.getAttribute('data-view');
            navigate(targetView);
        });
    });

    // Landing page CTA
    const startBtn = document.getElementById('startAnalysisBtn');
    if (startBtn) {
        startBtn.addEventListener('click', () => {
            navigate('view-upload');
        });
    }
    
    // Start at Landing Page
    navigate('view-landing');
    
    // Set dynamic copyright year
    document.getElementById('copyYear').textContent = new Date().getFullYear();
});
