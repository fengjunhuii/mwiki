/**
 * Export Functionality for Diagram Templates
 * Handles PNG export and SVG clipboard operations
 */

class DiagramExporter {
    constructor(diagramCore) {
        this.core = diagramCore;
        this.quality = 2; // 2x for high quality
    }

    async exportAsPNG(filename = 'diagram.png', quality = 2) {
        const svg = this.core.getSVG();
        if (!svg) {
            throw new Error('No SVG found to export');
        }

        return new Promise((resolve, reject) => {
            try {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                const svgData = new XMLSerializer().serializeToString(svg);

                // Create blob with proper namespace
                const svgBlob = new Blob([svgData], {
                    type: 'image/svg+xml;charset=utf-8'
                });
                const url = URL.createObjectURL(svgBlob);

                const img = new Image();
                img.onload = () => {
                    // Set canvas size (scaled for quality)
                    canvas.width = img.width * quality;
                    canvas.height = img.height * quality;

                    // Scale context
                    ctx.scale(quality, quality);

                    // Draw white background for transparency
                    ctx.fillStyle = 'white';
                    ctx.fillRect(0, 0, img.width, img.height);

                    // Draw SVG
                    ctx.drawImage(img, 0, 0);

                    // Convert to PNG and download
                    canvas.toBlob(blob => {
                        const pngUrl = URL.createObjectURL(blob);
                        const downloadLink = document.createElement('a');
                        downloadLink.href = pngUrl;
                        downloadLink.download = filename;
                        downloadLink.click();

                        // Cleanup
                        URL.revokeObjectURL(url);
                        URL.revokeObjectURL(pngUrl);
                        resolve(pngUrl);
                    }, 'image/png');
                };

                img.onerror = () => {
                    URL.revokeObjectURL(url);
                    reject(new Error('Failed to load SVG image'));
                };

                img.src = url;
            } catch (error) {
                reject(error);
            }
        });
    }

    async exportAsSVG(filename = 'diagram.svg') {
        const svgString = this.core.getSVGString();
        if (!svgString) {
            throw new Error('No SVG found to export');
        }

        try {
            const blob = new Blob([svgString], {
                type: 'image/svg+xml;charset=utf-8'
            });
            const url = URL.createObjectURL(blob);

            const downloadLink = document.createElement('a');
            downloadLink.href = url;
            downloadLink.download = filename;
            downloadLink.click();

            URL.revokeObjectURL(url);
            return url;
        } catch (error) {
            throw new Error(`Failed to export SVG: ${error.message}`);
        }
    }

    async copySVGToClipboard() {
        const svgString = this.core.getSVGString();
        if (!svgString) {
            throw new Error('No SVG found to copy');
        }

        try {
            // Try modern clipboard API first
            if (navigator.clipboard && navigator.clipboard.writeText) {
                await navigator.clipboard.writeText(svgString);
                return true;
            }

            // Fallback for older browsers
            const textarea = document.createElement('textarea');
            textarea.value = svgString;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();

            const successful = document.execCommand('copy');
            document.body.removeChild(textarea);

            return successful;
        } catch (error) {
            throw new Error(`Failed to copy SVG: ${error.message}`);
        }
    }

    async copyAsPNG() {
        const svg = this.core.getSVG();
        if (!svg) {
            throw new Error('No SVG found to copy');
        }

        return new Promise((resolve, reject) => {
            try {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                const svgData = new XMLSerializer().serializeToString(svg);
                const svgBlob = new Blob([svgData], {
                    type: 'image/svg+xml;charset=utf-8'
                });
                const url = URL.createObjectURL(svgBlob);

                const img = new Image();
                img.onload = async () => {
                    canvas.width = img.width * this.quality;
                    canvas.height = img.height * this.quality;
                    ctx.scale(this.quality, this.quality);
                    ctx.drawImage(img, 0, 0);

                    canvas.toBlob(async blob => {
                        try {
                            await navigator.clipboard.write([
                                new ClipboardItem({ 'image/png': blob })
                            ]);
                            URL.revokeObjectURL(url);
                            resolve(true);
                        } catch (error) {
                            URL.revokeObjectURL(url);
                            reject(error);
                        }
                    }, 'image/png');
                };

                img.onerror = () => {
                    URL.revokeObjectURL(url);
                    reject(new Error('Failed to load SVG image'));
                };

                img.src = url;
            } catch (error) {
                reject(error);
            }
        });
    }

    setQuality(quality) {
        this.quality = Math.max(1, Math.min(4, quality));
    }

    getQuality() {
        return this.quality;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DiagramExporter;
}
