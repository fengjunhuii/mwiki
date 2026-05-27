/**
 * Zoom Functionality for Diagram Templates
 * Provides advanced zoom controls with pan and fit-to-screen
 */

class ZoomController {
    constructor(diagramCore, options = {}) {
        this.core = diagramCore;
        this.options = {
            minZoom: options.minZoom || 0.1,
            maxZoom: options.maxZoom || 5,
            zoomStep: options.zoomStep || 0.1,
            enablePan: options.enablePan !== false,
            enableMouseWheel: options.enableMouseWheel !== false,
            ...options
        };

        this.state = {
            zoom: this.core.state.zoom,
            panX: 0,
            panY: 0,
            isPanning: false,
            lastMouseX: 0,
            lastMouseY: 0
        };

        this.setupEventListeners();
    }

    setupEventListeners() {
        const container = this.core.container;

        if (this.options.enableMouseWheel) {
            container.addEventListener('wheel', this.handleWheel.bind(this), {
                passive: false
            });
        }

        if (this.options.enablePan) {
            container.addEventListener('mousedown', this.handleMouseDown.bind(this));
            document.addEventListener('mousemove', this.handleMouseMove.bind(this));
            document.addEventListener('mouseup', this.handleMouseUp.bind(this));
        }

        // Touch support
        container.addEventListener('touchstart', this.handleTouchStart.bind(this), {
            passive: false
        });
        container.addEventListener('touchmove', this.handleTouchMove.bind(this), {
            passive: false
        });
        container.addEventListener('touchend', this.handleTouchEnd.bind(this));
    }

    handleWheel(e) {
        e.preventDefault();

        const delta = e.deltaY > 0 ? -this.options.zoomStep : this.options.zoomStep;
        const rect = this.core.container.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        this.zoomToPoint(delta, x, y);
    }

    handleMouseDown(e) {
        if (e.button === 1 || (e.button === 0 && e.altKey)) {
            this.state.isPanning = true;
            this.state.lastMouseX = e.clientX;
            this.state.lastMouseY = e.clientY;
            this.core.container.style.cursor = 'grabbing';
            e.preventDefault();
        }
    }

    handleMouseMove(e) {
        if (!this.state.isPanning) return;

        const deltaX = e.clientX - this.state.lastMouseX;
        const deltaY = e.clientY - this.state.lastMouseY;

        this.state.panX += deltaX;
        this.state.panY += deltaY;

        this.state.lastMouseX = e.clientX;
        this.state.lastMouseY = e.clientY;

        this.applyTransform();
    }

    handleMouseUp() {
        if (this.state.isPanning) {
            this.state.isPanning = false;
            this.core.container.style.cursor = '';
        }
    }

    handleTouchStart(e) {
        if (e.touches.length === 2) {
            // Pinch zoom
            const touch1 = e.touches[0];
            const touch2 = e.touches[1];
            this.state.initialPinchDistance = this.getTouchDistance(touch1, touch2);
            this.state.initialZoom = this.state.zoom;
            e.preventDefault();
        } else if (e.touches.length === 1 && this.options.enablePan) {
            // Pan
            this.state.isPanning = true;
            this.state.lastMouseX = e.touches[0].clientX;
            this.state.lastMouseY = e.touches[0].clientY;
        }
    }

    handleTouchMove(e) {
        if (e.touches.length === 2 && this.state.initialPinchDistance) {
            // Pinch zoom
            const touch1 = e.touches[0];
            const touch2 = e.touches[1];
            const currentDistance = this.getTouchDistance(touch1, touch2);
            const scale = currentDistance / this.state.initialPinchDistance;

            const newZoom = Math.max(
                this.options.minZoom,
                Math.min(this.options.maxZoom, this.state.initialZoom * scale)
            );

            this.setZoom(newZoom);
            e.preventDefault();
        } else if (e.touches.length === 1 && this.state.isPanning) {
            // Pan
            const deltaX = e.touches[0].clientX - this.state.lastMouseX;
            const deltaY = e.touches[0].clientY - this.state.lastMouseY;

            this.state.panX += deltaX;
            this.state.panY += deltaY;

            this.state.lastMouseX = e.touches[0].clientX;
            this.state.lastMouseY = e.touches[0].clientY;

            this.applyTransform();
            e.preventDefault();
        }
    }

    handleTouchEnd() {
        this.state.isPanning = false;
        this.state.initialPinchDistance = null;
    }

    getTouchDistance(touch1, touch2) {
        const dx = touch1.clientX - touch2.clientX;
        const dy = touch1.clientY - touch2.clientY;
        return Math.sqrt(dx * dx + dy * dy);
    }

    zoomToPoint(delta, x, y) {
        const newZoom = Math.max(
            this.options.minZoom,
            Math.min(this.options.maxZoom, this.state.zoom + delta)
        );

        if (newZoom !== this.state.zoom) {
            // Adjust pan to zoom toward point
            const zoomRatio = newZoom / this.state.zoom;
            this.state.panX = x - (x - this.state.panX) * zoomRatio;
            this.state.panY = y - (y - this.state.panY) * zoomRatio;

            this.setZoom(newZoom);
        }
    }

    setZoom(zoom) {
        this.state.zoom = zoom;
        this.core.state.zoom = zoom;
        this.applyTransform();
        this.core.triggerEvent('zoomChanged', { zoom: this.state.zoom });
    }

    getZoom() {
        return this.state.zoom;
    }

    zoomIn() {
        this.setZoom(Math.min(this.state.zoom + this.options.zoomStep, this.options.maxZoom));
    }

    zoomOut() {
        this.setZoom(Math.max(this.state.zoom - this.options.zoomStep, this.options.minZoom));
    }

    zoomReset() {
        this.state.zoom = 1;
        this.state.panX = 0;
        this.state.panY = 0;
        this.core.state.zoom = 1;
        this.applyTransform();
        this.core.triggerEvent('zoomChanged', { zoom: 1 });
    }

    zoomToFit(padding = 20) {
        const svg = this.core.getSVG();
        const container = this.core.container;

        if (!svg || !container) return;

        const containerRect = container.getBoundingClientRect();
        const svgRect = svg.getBoundingClientRect();

        const widthRatio = (containerRect.width - padding * 2) / svgRect.width;
        const heightRatio = (containerRect.height - padding * 2) / svgRect.height;

        const fitZoom = Math.min(widthRatio, heightRatio, 1);

        this.setZoom(fitZoom);
        this.state.panX = 0;
        this.state.panY = 0;
        this.applyTransform();
    }

    applyTransform() {
        const svg = this.core.getSVG();
        if (svg) {
            svg.style.transform = `translate(${this.state.panX}px, ${this.state.panY}px) scale(${this.state.zoom})`;
            svg.style.transformOrigin = '0 0';
        }
    }

    setPan(x, y) {
        this.state.panX = x;
        this.state.panY = y;
        this.applyTransform();
    }

    getPan() {
        return { x: this.state.panX, y: this.state.panY };
    }

    reset() {
        this.zoomReset();
    }

    destroy() {
        const container = this.core.container;
        container.removeEventListener('wheel', this.handleWheel);
        container.removeEventListener('mousedown', this.handleMouseDown);
        document.removeEventListener('mousemove', this.handleMouseMove);
        document.removeEventListener('mouseup', this.handleMouseUp);
        container.removeEventListener('touchstart', this.handleTouchStart);
        container.removeEventListener('touchmove', this.handleTouchMove);
        container.removeEventListener('touchend', this.handleTouchEnd);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ZoomController;
}
