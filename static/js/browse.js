/**
 * Browse Page JavaScript
 * Enhanced listing browsing with filters and pagination
 */

class BrowsePage {
    constructor() {
        this.currentPage = 1;
        this.itemsPerPage = 12;
        this.totalItems = 0;
        this.allListings = [];
        this.filteredListings = [];
        this.filters = {
            category: '',
            minPrice: null,
            maxPrice: null,
            location: '',
            query: '',
            sortBy: 'newest'
        };
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadListings();
    }
    
    setupEventListeners() {
        // Category filters
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.selectCategory(e.target);
            });
        });
        
        // Search form
        const searchForm = document.querySelector('.search-form');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.performSearch();
            });
        }
        
        // Filter buttons
        const applyBtn = document.querySelector('.filter-apply-btn');
        const resetBtn = document.querySelector('.filter-reset-btn');
        
        if (applyBtn) {
            applyBtn.addEventListener('click', () => this.applyFilters());
        }
        
        if (resetBtn) {
            resetBtn.addEventListener('click', () => this.resetFilters());
        }
        
        // Sort dropdown
        const sortSelect = document.getElementById('sort-select');
        if (sortSelect) {
            sortSelect.addEventListener('change', (e) => {
                this.filters.sortBy = e.target.value;
                this.applyFilters();
            });
        }
        
        // Modal functionality
        const modal = document.getElementById('listing-modal');
        const closeBtn = document.querySelector('.modal-close');
        
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.closeModal());
        }
        
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal();
                }
            });
        }
    }
    
    async loadListings() {
        this.showLoading();
        
        try {
            const response = await fetch('/api/v1/listings/?limit=100');
            if (response.ok) {
                this.allListings = await response.json();
                this.filteredListings = [...this.allListings];
                this.totalItems = this.allListings.length;
                this.updateResultsCount();
                this.renderListings();
                this.renderPagination();
            } else {
                this.showError('Kunne ikke laste annonser');
            }
        } catch (error) {
            console.error('Error loading listings:', error);
            this.showError('Feil ved lasting av annonser');
        } finally {
            this.hideLoading();
        }
    }
    
    selectCategory(button) {
        // Update active state
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        button.classList.add('active');
        
        // Update filter
        this.filters.category = button.dataset.category || '';
        this.applyFilters();
    }
    
    performSearch() {
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            this.filters.query = searchInput.value.trim();
            this.applyFilters();
        }
    }
    
    applyFilters() {
        // Get filter values
        const minPriceInput = document.getElementById('min-price');
        const maxPriceInput = document.getElementById('max-price');
        const locationInput = document.getElementById('location-filter');
        
        if (minPriceInput) {
            this.filters.minPrice = minPriceInput.value ? parseInt(minPriceInput.value) : null;
        }
        
        if (maxPriceInput) {
            this.filters.maxPrice = maxPriceInput.value ? parseInt(maxPriceInput.value) : null;
        }
        
        if (locationInput) {
            this.filters.location = locationInput.value.trim();
        }
        
        // Apply filters
        this.filteredListings = this.allListings.filter(listing => {
            // Category filter
            if (this.filters.category && listing.category !== this.filters.category) {
                return false;
            }
            
            // Price filters
            if (this.filters.minPrice !== null && listing.price !== null && listing.price < this.filters.minPrice) {
                return false;
            }
            
            if (this.filters.maxPrice !== null && listing.price !== null && listing.price > this.filters.maxPrice) {
                return false;
            }
            
            // Location filter
            if (this.filters.location && !listing.location.toLowerCase().includes(this.filters.location.toLowerCase())) {
                return false;
            }
            
            // Search query
            if (this.filters.query) {
                const query = this.filters.query.toLowerCase();
                const titleMatch = listing.title.toLowerCase().includes(query);
                const sellerMatch = listing.seller_name && listing.seller_name.toLowerCase().includes(query);
                if (!titleMatch && !sellerMatch) {
                    return false;
                }
            }
            
            return true;
        });
        
        // Apply sorting
        this.sortListings();
        
        // Update display
        this.totalItems = this.filteredListings.length;
        this.currentPage = 1;
        this.updateResultsCount();
        this.renderListings();
        this.renderPagination();
    }
    
    sortListings() {
        switch (this.filters.sortBy) {
            case 'newest':
                this.filteredListings.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                break;
            case 'oldest':
                this.filteredListings.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
                break;
            case 'price-low':
                this.filteredListings.sort((a, b) => (a.price || 0) - (b.price || 0));
                break;
            case 'price-high':
                this.filteredListings.sort((a, b) => (b.price || 0) - (a.price || 0));
                break;
            case 'popular':
                this.filteredListings.sort((a, b) => (b.view_count + b.favorite_count) - (a.view_count + a.favorite_count));
                break;
        }
    }
    
    resetFilters() {
        // Reset filter values
        this.filters = {
            category: '',
            minPrice: null,
            maxPrice: null,
            location: '',
            query: '',
            sortBy: 'newest'
        };
        
        // Reset UI
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector('.category-btn[data-category=""]').classList.add('active');
        
        const minPriceInput = document.getElementById('min-price');
        const maxPriceInput = document.getElementById('max-price');
        const locationInput = document.getElementById('location-filter');
        const searchInput = document.querySelector('.search-input');
        const sortSelect = document.getElementById('sort-select');
        
        if (minPriceInput) minPriceInput.value = '';
        if (maxPriceInput) maxPriceInput.value = '';
        if (locationInput) locationInput.value = '';
        if (searchInput) searchInput.value = '';
        if (sortSelect) sortSelect.value = 'newest';
        
        // Apply reset filters
        this.applyFilters();
    }
    
    renderListings() {
        const container = document.getElementById('listings-container');
        if (!container) return;
        
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        const pageListings = this.filteredListings.slice(startIndex, endIndex);
        
        if (pageListings.length === 0) {
            container.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-search"></i>
                    <h3>Ingen annonser funnet</h3>
                    <p>Prøv å justere søkekriteriene dine</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = pageListings.map(listing => this.createListingCard(listing)).join('');
        
        // Add event listeners to cards
        container.querySelectorAll('.listing-card').forEach(card => {
            card.addEventListener('click', () => {
                const listingId = parseInt(card.dataset.id);
                this.openListingModal(listingId);
            });
        });
    }
    
    createListingCard(listing) {
        return `
            <div class="listing-card" data-id="${listing.id}">
                <div class="listing-image">
                    <img src="${listing.image_url}" alt="${listing.title}" loading="lazy">
                    <button class="favorite-btn" onclick="event.stopPropagation(); toggleFavorite(${listing.id})">
                        <i class="far fa-heart"></i>
                    </button>
                </div>
                <div class="listing-content">
                    <h3 class="listing-title">${listing.title}</h3>
                    <div class="listing-price">
                        ${listing.price ? `${this.formatPrice(listing.price)}` : 'Kontakt for pris'}
                    </div>
                    <div class="listing-location">
                        <i class="fas fa-map-marker-alt"></i>
                        ${listing.location}
                    </div>
                    <div class="listing-meta">
                        <span class="listing-date">${this.formatDate(listing.created_at)}</span>
                        <span class="listing-views">
                            <i class="fas fa-eye"></i>
                            ${listing.view_count}
                        </span>
                    </div>
                </div>
            </div>
        `;
    }
    
    async openListingModal(listingId) {
        const modal = document.getElementById('listing-modal');
        const modalBody = document.getElementById('modal-body');
        
        if (!modal || !modalBody) return;
        
        try {
            const response = await fetch(`/api/v1/listings/${listingId}`);
            if (response.ok) {
                const listing = await response.json();
                modalBody.innerHTML = this.createModalContent(listing);
                modal.style.display = 'block';
                document.body.style.overflow = 'hidden';
            } else {
                this.showError('Kunne ikke laste annonse');
            }
        } catch (error) {
            console.error('Error loading listing:', error);
            this.showError('Feil ved lasting av annonse');
        }
    }
    
    createModalContent(listing) {
        return `
            <div class="modal-listing">
                <div class="modal-image">
                    <img src="${listing.image_url}" alt="${listing.title}">
                </div>
                <div class="modal-details">
                    <h2>${listing.title}</h2>
                    <div class="modal-price">
                        ${listing.price ? this.formatPrice(listing.price) : 'Kontakt for pris'}
                    </div>
                    <div class="modal-location">
                        <i class="fas fa-map-marker-alt"></i>
                        ${listing.location}
                    </div>
                    <div class="modal-description">
                        <p>${listing.description || 'Ingen beskrivelse tilgjengelig.'}</p>
                    </div>
                    <div class="modal-seller">
                        <h4>Selger</h4>
                        <p>${listing.seller_name || listing.company_name || 'Privat'}</p>
                    </div>
                    <div class="modal-actions">
                        <button class="btn btn-primary">
                            <i class="fas fa-envelope"></i>
                            Send melding
                        </button>
                        <button class="btn btn-outline">
                            <i class="fas fa-phone"></i>
                            Ring
                        </button>
                        <button class="btn btn-outline favorite-btn" onclick="toggleFavorite(${listing.id})">
                            <i class="far fa-heart"></i>
                            Favoritt
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    closeModal() {
        const modal = document.getElementById('listing-modal');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }
    
    renderPagination() {
        const pagination = document.getElementById('pagination');
        if (!pagination) return;
        
        const totalPages = Math.ceil(this.totalItems / this.itemsPerPage);
        
        if (totalPages <= 1) {
            pagination.innerHTML = '';
            return;
        }
        
        let paginationHTML = '';
        
        // Previous button
        if (this.currentPage > 1) {
            paginationHTML += `<button class="page-btn" onclick="browsePage.goToPage(${this.currentPage - 1})">Forrige</button>`;
        }
        
        // Page numbers
        const startPage = Math.max(1, this.currentPage - 2);
        const endPage = Math.min(totalPages, this.currentPage + 2);
        
        if (startPage > 1) {
            paginationHTML += `<button class="page-btn" onclick="browsePage.goToPage(1)">1</button>`;
            if (startPage > 2) {
                paginationHTML += `<span class="page-dots">...</span>`;
            }
        }
        
        for (let i = startPage; i <= endPage; i++) {
            const activeClass = i === this.currentPage ? 'active' : '';
            paginationHTML += `<button class="page-btn ${activeClass}" onclick="browsePage.goToPage(${i})">${i}</button>`;
        }
        
        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                paginationHTML += `<span class="page-dots">...</span>`;
            }
            paginationHTML += `<button class="page-btn" onclick="browsePage.goToPage(${totalPages})">${totalPages}</button>`;
        }
        
        // Next button
        if (this.currentPage < totalPages) {
            paginationHTML += `<button class="page-btn" onclick="browsePage.goToPage(${this.currentPage + 1})">Neste</button>`;
        }
        
        pagination.innerHTML = paginationHTML;
    }
    
    goToPage(page) {
        this.currentPage = page;
        this.renderListings();
        this.renderPagination();
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    updateResultsCount() {
        const resultsCount = document.getElementById('results-count');
        if (resultsCount) {
            resultsCount.textContent = `${this.totalItems} annonser funnet`;
        }
    }
    
    formatPrice(price) {
        return new Intl.NumberFormat('no-NO', {
            style: 'currency',
            currency: 'NOK',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(price);
    }
    
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('no-NO', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });
    }
    
    showLoading() {
        const spinner = document.getElementById('loading-spinner');
        if (spinner) {
            spinner.classList.remove('hidden');
        }
    }
    
    hideLoading() {
        const spinner = document.getElementById('loading-spinner');
        if (spinner) {
            spinner.classList.add('hidden');
        }
    }
    
    showError(message) {
        // Simple alert for now - could be enhanced with a toast notification
        alert(message);
    }
}

// Global functions for event handlers
function toggleFavorite(listingId) {
    // Implement favorite functionality
    console.log('Toggle favorite for listing:', listingId);
}

// Initialize the browse page
let browsePage;
document.addEventListener('DOMContentLoaded', () => {
    browsePage = new BrowsePage();
});
