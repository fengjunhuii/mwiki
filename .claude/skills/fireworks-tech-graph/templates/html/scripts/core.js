/**
 * Core HTML Template System
 * Provides foundational functionality for diagram display and interaction
 */

class DiagramCore {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            throw new Error(`Container with id "${containerId}" not found`);
        }

        this.options = {
            style: options.style || 5,
            zoom: options.zoom || 1,
            enableKeyboard: options.enableKeyboard !== false,
            enableFullscreen: options.enableFullscreen !== false,
            enableExport: options.enableExport !== false,
            ...options
        };

        this.state = {
            currentStyle: this.options.style,
            zoom: this.options.zoom,
            isFullscreen: false,
            originalSVG: null
        };

        this.init();
    }

    init() {
        this.state.originalSVG = this.container.innerHTML;
        this.setupEventListeners();
        this.applyStyle(this.state.currentStyle);
        this.applyZoom();
    }

    setupEventListeners() {
        if (this.options.enableKeyboard) {
            document.addEventListener('keydown', this.handleKeyboard.bind(this));
        }
    }

    handleKeyboard(e) {
        // Prevent default for diagram-specific keys
        const keyHandlers = {
            'Escape': () => this.isFullscreen && this.toggleFullscreen(),
            '+': () => this.zoomIn(),
            '=': () => this.zoomIn(),
            '-': () => this.zoomOut(),
            '0': () => this.zoomReset()
        };

        if (keyHandlers[e.key]) {
            e.preventDefault();
            keyHandlers[e.key]();
        }
    }

    applyStyle(styleNum) {
        this.state.currentStyle = styleNum;
        const root = document.documentElement;
        const styles = this.getStyleDefinitions();

        if (styles[styleNum]) {
            Object.entries(styles[styleNum]).forEach(([key, value]) => {
                root.style.setProperty(key, value);
            });
        }

        this.triggerEvent('styleChanged', { style: styleNum });
    }

    getStyleDefinitions() {
        return {
            1: { // Flat
                '--bg-gradient-start': '#ffffff',
                '--bg-gradient-mid': '#f5f5f5',
                '--bg-gradient-end': '#ffffff',
                '--glass-bg': 'rgba(0, 0, 0, 0.02)',
                '--glass-stroke': 'rgba(0, 0, 0, 0.1)',
                '--text-primary': '#1a1a1a',
                '--text-secondary': '#666666'
            },
            2: { // Dark Terminal
                '--bg-gradient-start': '#1a1a2e',
                '--bg-gradient-mid': '#16213e',
                '--bg-gradient-end': '#1a1a2e',
                '--glass-bg': 'rgba(0, 255, 0, 0.03)',
                '--glass-stroke': 'rgba(0, 255, 0, 0.2)',
                '--text-primary': '#00ff00',
                '--text-secondary': '#00cc00'
            },
            3: { // Blueprint
                '--bg-gradient-start': '#1a3a5c',
                '--bg-gradient-mid': '#2d5a87',
                '--bg-gradient-end': '#1a3a5c',
                '--glass-bg': 'rgba(255, 255, 255, 0.05)',
                '--glass-stroke': 'rgba(255, 255, 255, 0.2)',
                '--text-primary': '#ffffff',
                '--text-secondary': '#a0c0e0'
            },
            4: { // Notion Clean
                '--bg-gradient-start': '#ffffff',
                '--bg-gradient-mid': '#f7f6f3',
                '--bg-gradient-end': '#ffffff',
                '--glass-bg': 'rgba(0, 0, 0, 0.02)',
                '--glass-stroke': 'rgba(0, 0, 0, 0.08)',
                '--text-primary': '#37352f',
                '--text-secondary': '#787774'
            },
            5: { // Glassmorphism (default)
                '--bg-gradient-start': '#0d1117',
                '--bg-gradient-mid': '#161b22',
                '--bg-gradient-end': '#0d1117',
                '--glass-bg': 'rgba(255, 255, 255, 0.05)',
                '--glass-stroke': 'rgba(255, 255, 255, 0.15)',
                '--text-primary': '#f0f6fc',
                '--text-secondary': '#8b949e'
            },
            6: { // Claude
                '--bg-gradient-start': '#d97706',
                '--bg-gradient-mid': '#f59e0b',
                '--bg-gradient-end': '#d97706',
                '--glass-bg': 'rgba(255, 255, 255, 0.1)',
                '--glass-stroke': 'rgba(255, 255, 255, 0.3)',
                '--text-primary': '#1a1a1a',
                '--text-secondary': '#4a4a4a'
            },
            7: { // OpenAI
                '--bg-gradient-start': '#10a37f',
                '--bg-gradient-mid': '#1a7f64',
                '--bg-gradient-end': '#10a37f',
                '--glass-bg': 'rgba(255, 255, 255, 0.1)',
                '--glass-stroke': 'rgba(255, 255, 255, 0.3)',
                '--text-primary': '#ffffff',
                '--text-secondary': '#a0e0d0'
            }
        };
    }

    applyZoom() {
        const svg = this.container.querySelector('svg');
        if (svg) {
            svg.style.transform = `scale(${this.state.zoom})`;
            svg.style.transformOrigin = 'center center';
        }
        this.triggerEvent('zoomChanged', { zoom: this.state.zoom });
    }

    zoomIn() {
        this.state.zoom = Math.min(this.state.zoom + 0.1, 3);
        this.applyZoom();
    }

    zoomOut() {
        this.state.zoom = Math.max(this.state.zoom - 0.1, 0.3);
        this.applyZoom();
    }

    zoomReset() {
        this.state.zoom = 1;
        this.applyZoom();
    }

    toggleFullscreen() {
        if (!this.options.enableFullscreen) return;

        this.state.isFullscreen = !this.state.isFullscreen;
        document.body.classList.toggle('fullscreen', this.state.isFullscreen);
        this.triggerEvent('fullscreenChanged', { isFullscreen: this.state.isFullscreen });
    }

    triggerEvent(eventName, detail = {}) {
        const event = new CustomEvent(`diagram:${eventName}`, {
            detail: { ...detail, diagram: this }
        });
        this.container.dispatchEvent(event);
    }

    getSVG() {
        return this.container.querySelector('svg');
    }

    getSVGString() {
        const svg = this.getSVG();
        return svg ? new XMLSerializer().serializeToString(svg) : null;
    }

    destroy() {
        document.removeEventListener('keydown', this.handleKeyboard);
        this.container.innerHTML = this.state.originalSVG;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DiagramCore;
}
