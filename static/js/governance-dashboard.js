/**
 * AI Governance Dashboard JavaScript
 * Cutting-edge dashboard with real-time data visualization
 */

class GovernanceDashboard {
    constructor() {
        this.apiBaseUrl = '/api/v1/dashboard/governance';
        this.charts = {};
        this.currentSection = 'overview';
        this.updateInterval = 30000; // 30 seconds
        this.updateTimer = null;
        
        this.init();
    }

    async init() {
        this.showLoading();
        await this.setupEventListeners();
        await this.loadInitialData();
        this.startAutoUpdate();
        this.hideLoading();
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const section = e.currentTarget.dataset.section;
                this.switchSection(section);
            });
        });

        // Content scanner
        const scanButton = document.getElementById('scan-button');
        if (scanButton) {
            scanButton.addEventListener('click', () => this.scanContent());
        }

        // Auto-resize charts on window resize
        window.addEventListener('resize', () => {
            Object.values(this.charts).forEach(chart => {
                if (chart && typeof chart.resize === 'function') {
                    chart.resize();
                }
            });
        });
    }

    switchSection(sectionName) {
        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-section="${sectionName}"]`).classList.add('active');

        // Update content
        document.querySelectorAll('.dashboard-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(`${sectionName}-section`).classList.add('active');

        // Update header
        this.updateHeader(sectionName);

        // Load section-specific data
        this.loadSectionData(sectionName);
        
        this.currentSection = sectionName;
    }

    updateHeader(sectionName) {
        const titles = {
            overview: { title: 'AI Governance Oversikt', subtitle: 'Sanntidsovervåkning av AI-systemer og compliance' },
            compliance: { title: 'Compliance Rapport', subtitle: 'Detaljert GDPR og rettighetshåndhevelse analyse' },
            risk: { title: 'Risikoanalyse', subtitle: 'Identifikasjon og vurdering av AI-relaterte risikoer' },
            content: { title: 'Innhold Skanning', subtitle: 'Automatisk skanning for compliance og sikkerhet' },
            policies: { title: 'Retningslinjer', subtitle: 'Aktive AI governance retningslinjer og overholdelse' },
            analytics: { title: 'Analyse og Innsikt', subtitle: 'Avansert analyse av AI governance ytelse' }
        };

        const pageTitle = document.getElementById('page-title');
        const pageSubtitle = document.getElementById('page-subtitle');
        
        if (titles[sectionName]) {
            pageTitle.textContent = titles[sectionName].title;
            pageSubtitle.textContent = titles[sectionName].subtitle;
        }
    }

    async loadInitialData() {
        try {
            await Promise.all([
                this.loadOverviewData(),
                this.updateLastUpdatedTime()
            ]);
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showError('Feil ved lasting av data. Prøver igjen...');
        }
    }

    async loadSectionData(section) {
        try {
            switch (section) {
                case 'overview':
                    await this.loadOverviewData();
                    break;
                case 'compliance':
                    await this.loadComplianceData();
                    break;
                case 'risk':
                    await this.loadRiskData();
                    break;
                case 'content':
                    await this.loadContentData();
                    break;
                case 'policies':
                    await this.loadPoliciesData();
                    break;
                case 'analytics':
                    await this.loadAnalyticsData();
                    break;
            }
        } catch (error) {
            console.error(`Error loading ${section} data:`, error);
            this.showError(`Feil ved lasting av ${section} data`);
        }
    }

    async loadOverviewData() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/overview`);
            const data = await response.json();

            // Update metrics
            document.getElementById('governance-score').textContent = data.governance_score || '--';
            document.getElementById('compliance-rate').textContent = `${data.compliance_rate || 0}%`;
            document.getElementById('risk-level').textContent = data.overall_risk_level || '--';
            document.getElementById('scanned-items').textContent = data.scanned_items_today || '--';

            // Update activities
            this.updateActivities(data.recent_activities || []);

            // Create charts
            await this.createOverviewCharts(data);

        } catch (error) {
            console.error('Error loading overview data:', error);
            throw error;
        }
    }

    async loadComplianceData() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/compliance-report`);
            const data = await response.json();

            // Update compliance scores
            document.getElementById('gdpr-score').textContent = `${data.gdpr_compliance || 0}%`;
            document.getElementById('fairness-score').textContent = `${data.fairness_score || 0}%`;
            document.getElementById('data-protection-score').textContent = `${data.data_protection || 0}%`;

            // Update progress bars
            document.getElementById('gdpr-progress').style.width = `${data.gdpr_compliance || 0}%`;
            document.getElementById('fairness-progress').style.width = `${data.fairness_score || 0}%`;
            document.getElementById('data-protection-progress').style.width = `${data.data_protection || 0}%`;

            // Update compliance details
            this.updateComplianceDetails(data.compliance_details || []);

        } catch (error) {
            console.error('Error loading compliance data:', error);
            throw error;
        }
    }

    async loadRiskData() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/risk-assessment`);
            const data = await response.json();

            // Update risk matrix
            this.updateRiskMatrix(data.risk_matrix || []);

            // Update risk categories
            this.updateRiskCategories(data.risk_categories || []);

            // Update recommendations
            this.updateRecommendations(data.recommendations || []);

        } catch (error) {
            console.error('Error loading risk data:', error);
            throw error;
        }
    }

    async loadContentData() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/scan-content`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: '' })
            });
            
            // Load scan history instead of scanning empty content
            // This is just to test the endpoint
            
        } catch (error) {
            console.error('Error loading content data:', error);
        }
    }

    async loadPoliciesData() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/policies`);
            const data = await response.json();

            // Update policies list
            this.updatePoliciesList(data.policies || []);

            // Create policy compliance chart
            this.createPolicyComplianceChart(data);

        } catch (error) {
            console.error('Error loading policies data:', error);
            throw error;
        }
    }

    async loadAnalyticsData() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/analytics`);
            const data = await response.json();

            // Create analytics charts
            this.createAnalyticsCharts(data);

            // Update insights
            this.updateInsights(data.insights || []);

        } catch (error) {
            console.error('Error loading analytics data:', error);
            throw error;
        }
    }

    updateActivities(activities) {
        const activitiesList = document.getElementById('activities-list');
        if (!activitiesList) return;

        activitiesList.innerHTML = activities.map(activity => `
            <div class="activity-item">
                <div class="activity-icon">
                    <i class="fas ${this.getActivityIcon(activity.type)}"></i>
                </div>
                <div class="activity-content">
                    <h5>${activity.title}</h5>
                    <p>${activity.description}</p>
                </div>
                <div class="activity-time">${this.formatTime(activity.timestamp)}</div>
            </div>
        `).join('');
    }

    updateComplianceDetails(details) {
        const detailsList = document.getElementById('compliance-details-list');
        if (!detailsList) return;

        detailsList.innerHTML = details.map(detail => `
            <div class="detail-item">
                <div>
                    <h5>${detail.category}</h5>
                    <p>${detail.description}</p>
                </div>
                <span class="detail-status ${detail.status.toLowerCase()}">${detail.status}</span>
            </div>
        `).join('');
    }

    updateRiskMatrix(matrix) {
        const matrixGrid = document.getElementById('risk-matrix-grid');
        if (!matrixGrid) return;

        matrixGrid.innerHTML = matrix.map(cell => `
            <div class="matrix-cell ${cell.level.toLowerCase()}">
                ${cell.category}<br>
                <small>${cell.count} issues</small>
            </div>
        `).join('');
    }

    updateRiskCategories(categories) {
        const categoriesList = document.getElementById('risk-categories-list');
        if (!categoriesList) return;

        categoriesList.innerHTML = categories.map(category => `
            <div class="category-item">
                <div>
                    <h5>${category.name}</h5>
                    <p>${category.description}</p>
                </div>
                <span class="risk-level ${category.level.toLowerCase()}">${category.level}</span>
            </div>
        `).join('');
    }

    updateRecommendations(recommendations) {
        const recommendationsList = document.getElementById('recommendations-list');
        if (!recommendationsList) return;

        recommendationsList.innerHTML = recommendations.map(rec => `
            <div class="recommendation-item">
                <h5>${rec.title}</h5>
                <p>${rec.description}</p>
                <small>Prioritet: ${rec.priority}</small>
            </div>
        `).join('');
    }

    updatePoliciesList(policies) {
        const policiesList = document.getElementById('policies-list');
        if (!policiesList) return;

        policiesList.innerHTML = policies.map(policy => `
            <div class="policy-item">
                <div>
                    <h5>${policy.name}</h5>
                    <p>${policy.description}</p>
                </div>
                <span class="policy-status ${policy.status.toLowerCase()}">${policy.status}</span>
            </div>
        `).join('');
    }

    updateInsights(insights) {
        const insightsList = document.getElementById('insights-list');
        if (!insightsList) return;

        insightsList.innerHTML = insights.map(insight => `
            <div class="insight-item">
                <h5>${insight.title}</h5>
                <p>${insight.description}</p>
                <small>Konfidensgrad: ${insight.confidence}%</small>
            </div>
        `).join('');
    }

    async createOverviewCharts(data) {
        // Compliance Trend Chart
        const complianceCtx = document.getElementById('complianceChart');
        if (complianceCtx && data.compliance_trend) {
            if (this.charts.compliance) {
                this.charts.compliance.destroy();
            }
            
            this.charts.compliance = new Chart(complianceCtx, {
                type: 'line',
                data: {
                    labels: data.compliance_trend.labels || [],
                    datasets: [{
                        label: 'Compliance Rate',
                        data: data.compliance_trend.values || [],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            ticks: {
                                callback: function(value) {
                                    return value + '%';
                                }
                            }
                        }
                    }
                }
            });
        }

        // Risk Distribution Chart
        const riskCtx = document.getElementById('riskChart');
        if (riskCtx && data.risk_distribution) {
            if (this.charts.risk) {
                this.charts.risk.destroy();
            }
            
            this.charts.risk = new Chart(riskCtx, {
                type: 'doughnut',
                data: {
                    labels: data.risk_distribution.labels || ['Lav', 'Medium', 'Høy'],
                    datasets: [{
                        data: data.risk_distribution.values || [0, 0, 0],
                        backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '60%',
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
    }

    createPolicyComplianceChart(data) {
        const ctx = document.getElementById('policyComplianceChart');
        if (!ctx) return;

        if (this.charts.policyCompliance) {
            this.charts.policyCompliance.destroy();
        }

        this.charts.policyCompliance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.policy_compliance?.labels || [],
                datasets: [{
                    label: 'Compliance %',
                    data: data.policy_compliance?.values || [],
                    backgroundColor: '#6366f1',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }

    createAnalyticsCharts(data) {
        // Performance Chart
        const performanceCtx = document.getElementById('performanceChart');
        if (performanceCtx && data.performance_metrics) {
            if (this.charts.performance) {
                this.charts.performance.destroy();
            }
            
            this.charts.performance = new Chart(performanceCtx, {
                type: 'radar',
                data: {
                    labels: data.performance_metrics.labels || [],
                    datasets: [{
                        label: 'Current',
                        data: data.performance_metrics.current || [],
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        borderWidth: 2
                    }, {
                        label: 'Target',
                        data: data.performance_metrics.target || [],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }

        // Trends Chart
        const trendsCtx = document.getElementById('trendsChart');
        if (trendsCtx && data.monthly_trends) {
            if (this.charts.trends) {
                this.charts.trends.destroy();
            }
            
            this.charts.trends = new Chart(trendsCtx, {
                type: 'line',
                data: {
                    labels: data.monthly_trends.labels || [],
                    datasets: [{
                        label: 'Governance Score',
                        data: data.monthly_trends.governance || [],
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4
                    }, {
                        label: 'Compliance Rate',
                        data: data.monthly_trends.compliance || [],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        borderWidth: 3,
                        fill: false,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }
    }

    async scanContent() {
        const content = document.getElementById('content-input').value.trim();
        if (!content) {
            this.showError('Vennligst skriv inn innhold for skanning');
            return;
        }

        const scanButton = document.getElementById('scan-button');
        const originalText = scanButton.innerHTML;
        
        try {
            scanButton.disabled = true;
            scanButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Skanner...';

            const response = await fetch(`${this.apiBaseUrl}/scan-content`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ content })
            });

            const data = await response.json();
            this.displayScanResults(data);

        } catch (error) {
            console.error('Error scanning content:', error);
            this.showError('Feil ved skanning av innhold');
        } finally {
            scanButton.disabled = false;
            scanButton.innerHTML = originalText;
        }
    }

    displayScanResults(results) {
        const scanResults = document.getElementById('scan-results');
        if (!scanResults) return;

        scanResults.innerHTML = `
            <h5>Skanningsresultater</h5>
            <div class="scan-result-item">
                <span>Compliance Score:</span>
                <strong>${results.compliance_score || 0}%</strong>
            </div>
            <div class="scan-result-item">
                <span>Risiko Nivå:</span>
                <strong class="risk-level ${(results.risk_level || 'low').toLowerCase()}">${results.risk_level || 'Low'}</strong>
            </div>
            ${results.issues ? results.issues.map(issue => `
                <div class="scan-result-item">
                    <span>${issue.type}:</span>
                    <span>${issue.description}</span>
                </div>
            `).join('') : ''}
        `;
    }

    startAutoUpdate() {
        this.updateTimer = setInterval(() => {
            this.loadSectionData(this.currentSection);
            this.updateLastUpdatedTime();
        }, this.updateInterval);
    }

    stopAutoUpdate() {
        if (this.updateTimer) {
            clearInterval(this.updateTimer);
            this.updateTimer = null;
        }
    }

    updateLastUpdatedTime() {
        const timeElement = document.getElementById('last-updated-time');
        if (timeElement) {
            const now = new Date();
            timeElement.textContent = now.toLocaleTimeString('no-NO', {
                hour: '2-digit',
                minute: '2-digit'
            });
        }
    }

    getActivityIcon(type) {
        const icons = {
            scan: 'fa-search',
            alert: 'fa-exclamation-triangle',
            compliance: 'fa-check-circle',
            policy: 'fa-file-contract',
            risk: 'fa-shield-alt',
            default: 'fa-info-circle'
        };
        return icons[type] || icons.default;
    }

    formatTime(timestamp) {
        if (!timestamp) return '';
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'akkurat nå';
        if (diff < 3600000) return `${Math.floor(diff / 60000)} min siden`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)} timer siden`;
        return date.toLocaleDateString('no-NO');
    }

    showLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.classList.remove('hidden');
    }

    hideLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.classList.add('hidden');
    }

    showError(message) {
        // Create a simple toast notification
        const toast = document.createElement('div');
        toast.className = 'error-toast';
        toast.innerHTML = `
            <i class="fas fa-exclamation-circle"></i>
            <span>${message}</span>
        `;
        
        // Add toast styles
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ef4444;
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 500;
            animation: slideIn 0.3s ease-out;
        `;

        document.body.appendChild(toast);

        // Remove toast after 5 seconds
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 5000);
    }

    destroy() {
        this.stopAutoUpdate();
        Object.values(this.charts).forEach(chart => {
            if (chart && typeof chart.destroy === 'function') {
                chart.destroy();
            }
        });
    }
}

// Add CSS animations for toasts
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new GovernanceDashboard();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.dashboard) {
        window.dashboard.destroy();
    }
});
