// Icon Library Helper
class IconLibrary {
    constructor(basePath = '../static/icons/') {
        this.basePath = basePath;
        // UPDATE ICON MAPPINGS HERE
        // Format: 'icon-name': 'filename.png'
        this.iconMap = {
            // UI Icons
            'sign-out': 'sign-out.png',
            'edit': 'edit.png',
            'close': 'close.png',
            'user': 'user.png',
            'email': 'email.png',
            'phone': 'phone.png',
            'membership': 'membership.png',
            'calendar': 'calendar.png',
            'clock': 'clock.png',
            'anniversary': 'anniversary.png',
            'rollover': 'rollover.png',
            
            // Action Icons
            'save': 'save.png',
            'cancel': 'cancel.png',
            'reset': 'reset.png',
            
            // Feature Icons
            'marketplace': 'marketplace.png',
            'swap': 'swap.png',
            'booking': 'booking.png',
            'shield': 'shield.png',
            'vacation': 'vacation.png'
            
            // TO ADD NEW ICONS:
            // 1. Add the PNG file to /Users/loganbn2/cvd/static/icons/
            // 2. Add a new line here: 'icon-name': 'filename.png',
        };
    }

    // Get icon HTML element
    getIcon(iconName, className = 'icon', alt = '') {
        if (!this.iconMap[iconName]) {
            console.warn(`Icon "${iconName}" not found in icon library`);
            return '';
        }
        
        const iconPath = this.basePath + this.iconMap[iconName];
        return `<img src="${iconPath}" alt="${alt || iconName}" class="${className}">`;
    }

    // Get just the icon path
    getIconPath(iconName) {
        if (!this.iconMap[iconName]) {
            console.warn(`Icon "${iconName}" not found in icon library`);
            return '';
        }
        return this.basePath + this.iconMap[iconName];
    }

    // Create icon element programmatically
    createElement(iconName, className = 'icon', alt = '') {
        if (!this.iconMap[iconName]) {
            console.warn(`Icon "${iconName}" not found in icon library`);
            return null;
        }
        
        const img = document.createElement('img');
        img.src = this.basePath + this.iconMap[iconName];
        img.alt = alt || iconName;
        img.className = className;
        return img;
    }

    // Get all available icons
    getAvailableIcons() {
        return Object.keys(this.iconMap);
    }
}

// Initialize icon library
const icons = new IconLibrary();

// Helper function for quick icon access
function getIcon(name, className, alt) {
    return icons.getIcon(name, className, alt);
}
