// Master Page Code - Global Navigation and Site-wide Functionality
// This code runs on every page

import wixWindow from 'wix-window';
import wixLocation from 'wix-location';
import wixUsers from 'wix-users';
// Static import to avoid webpack bundling issues
import { verifyAdmin } from 'backend/admin-auth.jsw';

$w.onReady(function () {
    initializeNavigation();
    initializeUserMenu();
    initializeFooter();
    highlightCurrentPage();
});

// Main Navigation Setup
function initializeNavigation() {
    const navItems = [
        { id: 'navHome', path: '/', label: 'Home' },
        { id: 'navEvents', path: '/events', label: 'Events' },
        { id: 'navMembers', path: '/members', label: 'Members' },
        { id: 'navGallery', path: '/gallery', label: 'Gallery' },
        { id: 'navMagazine', path: '/magazine', label: 'Magazine' },
        { id: 'navRadio', path: '/radio', label: 'Radio' },
        { id: 'navSponsors', path: '/sponsors', label: 'Sponsors' },
        { id: 'navVolunteer', path: '/volunteer', label: 'Volunteer' },
        { id: 'navContact', path: '/contact', label: 'Contact' }
    ];
    
    navItems.forEach(item => {
        const element = $w(`#${item.id}`);
        if (element && element.onClick) {
            element.onClick(() => {
                wixLocation.to(item.path);
            });
        }
    });
    
    // Mobile menu toggle
    if ($w('#btnMobileMenu').onClick) {
        $w('#btnMobileMenu').onClick(() => {
            if ($w('#boxMobileNav').hidden) {
                $w('#boxMobileNav').show();
            } else {
                $w('#boxMobileNav').hide();
            }
        });
    }
    
    // Logo click goes to home
    if ($w('#imgLogo').onClick) {
        $w('#imgLogo').onClick(() => {
            wixLocation.to('/');
        });
    }
}

// User Authentication Menu
function initializeUserMenu() {
    const user = wixUsers.currentUser;
    
    if (user.loggedIn) {
        // Show logged in state
        if ($w('#btnLogin').hide) $w('#btnLogin').hide();
        if ($w('#btnUserMenu').show) $w('#btnUserMenu').show();
        
        // Get user info
        user.getEmail().then(email => {
            if ($w('#txtUserEmail').text !== undefined) {
                $w('#txtUserEmail').text = email;
            }
        });
        
        // Logout handler
        if ($w('#btnLogout').onClick) {
            $w('#btnLogout').onClick(() => {
                wixUsers.logout().then(() => {
                    wixLocation.to('/');
                });
            });
        }
        
        // Profile link
        if ($w('#btnMyProfile').onClick) {
            $w('#btnMyProfile').onClick(() => {
                wixLocation.to('/members/profile');
            });
        }
        
        // Admin link (check if admin)
        checkAdminStatus();
        
    } else {
        // Show login button
        if ($w('#btnLogin').show) $w('#btnLogin').show();
        if ($w('#btnUserMenu').hide) $w('#btnUserMenu').hide();
        
        // Login handler
        if ($w('#btnLogin').onClick) {
            $w('#btnLogin').onClick(() => {
                wixLocation.to('/members');
            });
        }
    }
}

async function checkAdminStatus() {
    try {
        // Using static import at top of file instead of dynamic import
        const result = await verifyAdmin();
        
        if (result.isAdmin && $w('#btnAdminDashboard').show) {
            $w('#btnAdminDashboard').show();
            $w('#btnAdminDashboard').onClick(() => {
                wixLocation.to('/admin');
            });
        }
    } catch (e) {
        // Not admin or error - silently fail
        console.log('Admin check skipped');
    }
}

// Footer Setup
function initializeFooter() {
    // Quick links
    const footerLinks = [
        { id: 'footerAbout', path: '/about' },
        { id: 'footerPrivacy', path: '/privacy' },
        { id: 'footerTerms', path: '/terms' },
        { id: 'footerContact', path: '/contact' }
    ];
    
    footerLinks.forEach(link => {
        if ($w(`#${link.id}`).onClick) {
            $w(`#${link.id}`).onClick(() => {
                wixLocation.to(link.path);
            });
        }
    });
    
    // Social media links
    const socialLinks = {
        'btnFacebook': 'https://facebook.com/banfjax',
        'btnInstagram': 'https://instagram.com/banfjax',
        'btnYoutube': 'https://youtube.com/banfjax',
        'btnTwitter': 'https://twitter.com/banfjax'
    };
    
    Object.entries(socialLinks).forEach(([id, url]) => {
        if ($w(`#${id}`).onClick) {
            $w(`#${id}`).onClick(() => {
                wixWindow.openLightbox(url);
            });
        }
    });
    
    // Copyright year
    if ($w('#txtCopyright').text !== undefined) {
        const year = new Date().getFullYear();
        $w('#txtCopyright').text = `© ${year} Bengal Association of North Florida. All rights reserved.`;
    }
}

// Highlight current page in navigation
function highlightCurrentPage() {
    const currentPath = wixLocation.path[0] || '';
    
    const pathToNav = {
        '': 'navHome',
        'events': 'navEvents',
        'members': 'navMembers',
        'gallery': 'navGallery',
        'magazine': 'navMagazine',
        'radio': 'navRadio',
        'sponsors': 'navSponsors',
        'volunteer': 'navVolunteer',
        'contact': 'navContact'
    };
    
    const activeNavId = pathToNav[currentPath];
    
    if (activeNavId && $w(`#${activeNavId}`).style) {
        // Add active styling
        $w(`#${activeNavId}`).style.fontWeight = 'bold';
        $w(`#${activeNavId}`).style.color = '#FF6B35'; // BANF orange
    }
}
