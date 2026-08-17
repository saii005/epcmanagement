import os
import json

def run():
    public_dir = "apps/epc_management/epc_management/public"
    js_dir = os.path.join(public_dir, "js")
    icons_dir = os.path.join(public_dir, "icons")
    
    os.makedirs(js_dir, exist_ok=True)
    os.makedirs(icons_dir, exist_ok=True)

    # 1. Create Web App Manifest
    manifest = {
        "name": "Apex Infra - EPC Field App",
        "short_name": "Apex Infra",
        "description": "Construction Site Execution, DPR, and Field Management App",
        "start_url": "/app",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#171717",
        "orientation": "portrait",
        "icons": [
            {
                "src": "/assets/epc_management/icons/icon-192.svg",
                "sizes": "192x192",
                "type": "image/svg+xml",
                "purpose": "any maskable"
            },
            {
                "src": "/assets/epc_management/icons/icon-512.svg",
                "sizes": "512x512",
                "type": "image/svg+xml",
                "purpose": "any maskable"
            }
        ]
    }

    with open(os.path.join(public_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=4)
    print("Created: manifest.json")

    # 2. Create Branded SVG App Icon (Construction Hardhat / Building Theme)
    icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
    <rect width="512" height="512" rx="100" fill="#171717"/>
    <path d="M256 120 L380 340 L132 340 Z" fill="none" stroke="#F59E0B" stroke-width="24" stroke-linejoin="round"/>
    <path d="M256 190 L330 320 L182 320 Z" fill="#F59E0B"/>
    <rect x="236" y="340" width="40" height="60" fill="#F59E0B"/>
    <text x="256" y="450" font-family="Arial, sans-serif" font-size="42" font-weight="bold" fill="#FFFFFF" text-anchor="middle">APEX INFRA</text>
</svg>"""

    with open(os.path.join(icons_dir, "icon-192.svg"), "w") as f:
        f.write(icon_svg)
    with open(os.path.join(icons_dir, "icon-512.svg"), "w") as f:
        f.write(icon_svg)
    print("Created: App Icons in /public/icons/")

    # 3. Create PWA Registration Script
    pwa_js = """
// PWA Registration for Apex Infra
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Dynamically inject manifest link if not present
        if (!document.querySelector('link[rel="manifest"]')) {
            var link = document.createElement('link');
            link.rel = 'manifest';
            link.href = '/assets/epc_management/manifest.json';
            document.head.appendChild(link);
        }
        
        // Add meta theme color for mobile status bar
        if (!document.querySelector('meta[name="theme-color"]')) {
            var meta = document.createElement('meta');
            meta.name = 'theme-color';
            meta.content = '#171717';
            document.head.appendChild(meta);
        }
    });
}
"""
    with open(os.path.join(js_dir, "pwa.js"), "w") as f:
        f.write(pwa_js.strip())
    print("Created: pwa.js")

if __name__ == "__main__":
    run()
