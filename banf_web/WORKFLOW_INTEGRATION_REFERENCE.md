# BANF Web Platform - Workflow & Functionalities Integration Reference

## 📋 Overview

This document analyzes the workflow patterns and functionalities from `C:\projects\survey\backup_20250815_185359` to guide the Wix Velo implementation.

---

## 🗂️ Source Files Analyzed

| File | Purpose | Lines | Key Features |
|------|---------|-------|--------------|
| `demo_landing.html` | Landing page demo | 708 | Navigation, Stats, Quick Menu, Events, Announcements |
| `demo_events.html` | Events & Programs | 496 | Event cards, Filters, Registration, Status badges |
| `demo_registration.html` | Member Registration | 423 | Multi-step form, Validation, Progress indicator |
| `admin_complete_test.html` | Admin System Test | 647 | 16 test modules, API testing, Status tracking |
| `zelle_payment_demo.html` | Payment Integration | 313 | Zelle workflow, DB transactions, Receipts |
| `feedback_form_demo.html` | Feedback System | 484 | AI agent demo, Category selection, Form automation |
| `app.py` | Flask Backend | 300 | Members, Surveys, SMS, Verification APIs |
| `demo_server.py` | Demo Server | 100 | Static file serving, Demo grid |

---

## 🔄 Core Workflow Patterns

### 1. **Navigation & Routing Pattern**

```javascript
// Header Navigation Structure
const navStructure = {
    logo: { icon: "🏛️", title: "BANF Jacksonville", subtitle: "Bengali Association of North Florida" },
    menu: [
        { href: "#home", label: "Home" },
        { href: "#events", label: "Events" },
        { href: "#members", label: "Members" },
        { href: "#about", label: "About" },
        { href: "#contact", label: "Contact" }
    ],
    actions: [
        { href: "#login", label: "Member Login", style: "primary" },
        { href: "#register", label: "Join Us", style: "primary" }
    ]
};
```

### 2. **Statistics Display Pattern**

```javascript
// Stats Container with glass-morphism effect
const statsConfig = [
    { number: "150+", label: "Active Families", icon: "👨‍👩‍👧‍👦" },
    { number: "25+", label: "Annual Events", icon: "🎉" },
    { number: "500+", label: "Community Members", icon: "👥" },
    { number: "15", label: "Years Serving", icon: "🏆" }
];

// CSS Pattern
.stat-card {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    padding: 30px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.2);
}
```

### 3. **Quick Access Menu Pattern**

```javascript
// Menu Grid Configuration
const quickMenuItems = [
    { icon: "🎉", title: "Events & Programs", description: "Discover upcoming cultural events...", link: "/demo_events.html" },
    { icon: "👥", title: "Member Registration", description: "Join our growing community...", link: "/demo_registration.html" },
    { icon: "💳", title: "Payment Portal", description: "Secure online payment system...", link: "/zelle_payment_demo.html" },
    { icon: "📋", title: "Community Surveys", description: "Share your feedback...", link: "/feedback_form_demo.html" },
    { icon: "📚", title: "Member Directory", description: "Connect with fellow members...", link: "/members" },
    { icon: "📞", title: "Support Center", description: "Get help with platform...", link: "/contact" }
];

// Hover Animation
.menu-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}
```

---

## 🎯 Event Management Workflow

### Event Card Structure
```javascript
// Event Object Model
const eventModel = {
    id: "event1",
    category: "cultural",  // cultural, religious, youth, community
    status: "upcoming",    // upcoming, ongoing, past
    date: "March 21, 2024",
    title: "🌸 Pohela Boishakh Celebration",
    description: "Join us for the Bengali New Year celebration...",
    location: "Jacksonville Community Center",
    attendees: 0
};
```

### Filter System
```javascript
// Event Filtering Logic
function filterEvents(category) {
    const cards = document.querySelectorAll('.event-card');
    cards.forEach(card => {
        if (category === 'all' || card.dataset.category === category) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Filter Buttons
const filterCategories = ['all', 'cultural', 'religious', 'youth', 'community'];
```

### Event Status Badges
```css
.status-upcoming { background: linear-gradient(45deg, #00ff7f, #00cc66); }
.status-ongoing { background: linear-gradient(45deg, #ffaa00, #ff8800); }
.status-past { background: rgba(255, 255, 255, 0.3); }
```

### Registration Flow
```javascript
async function registerForEvent(eventId) {
    // 1. Open modal with event details
    // 2. Collect attendee information
    // 3. Submit to backend API
    // 4. Create payment transaction if needed
    // 5. Send confirmation email/SMS
}
```

---

## 📝 Member Registration Workflow

### Multi-Step Form Pattern
```javascript
// Progress Indicator
const registrationSteps = [
    { step: 1, label: "Personal Info" },
    { step: 2, label: "Contact Details" },
    { step: 3, label: "Membership Type" },
    { step: 4, label: "Confirmation" }
];

function updateStep(stepNumber) {
    for (let i = 1; i <= 4; i++) {
        const step = document.getElementById(`step${i}`);
        step.classList.remove('active', 'completed');
        if (i < stepNumber) step.classList.add('completed');
        else if (i === stepNumber) step.classList.add('active');
    }
}
```

### Form Fields Configuration
```javascript
const registrationFields = {
    personal: [
        { id: 'firstName', type: 'text', label: 'First Name *', required: true },
        { id: 'lastName', type: 'text', label: 'Last Name *', required: true }
    ],
    contact: [
        { id: 'email', type: 'email', label: 'Email Address *', required: true },
        { id: 'phone', type: 'tel', label: 'Phone Number *', required: true, placeholder: '(904) 555-0123' }
    ],
    membership: [
        { id: 'membershipType', type: 'select', label: 'Membership Type', options: [
            { value: 'family', label: 'Family Membership ($50/year)' },
            { value: 'individual', label: 'Individual Membership ($30/year)' },
            { value: 'student', label: 'Student Membership ($15/year)' },
            { value: 'senior', label: 'Senior Membership ($25/year)' }
        ]}
    ],
    address: [
        { id: 'address', type: 'text', label: 'Address' },
        { id: 'city', type: 'text', label: 'City', default: 'Jacksonville' },
        { id: 'state', type: 'text', label: 'State', default: 'FL' }
    ],
    interests: {
        id: 'interests', type: 'multi-select', label: 'Community Interests',
        options: ['cultural-events', 'religious-programs', 'youth-activities', 
                  'senior-programs', 'volunteering', 'fundraising']
    }
};
```

### Demo API Pattern (for animations)
```javascript
// Interactive Demo API
window.demoAPI = {
    highlightField: function(fieldId) { /* Add glow effect */ },
    fillField: function(fieldId, value, typing = true) { /* Simulate typing */ },
    selectOption: function(fieldId, value) { /* Select dropdown */ },
    moveCursorTo: function(elementId, callback) { /* Animate cursor */ },
    clickButton: function(buttonId) { /* Simulate click */ },
    updateStep: function(stepNumber) { /* Update progress */ },
    showSuccess: function() { /* Show success message */ }
};
```

---

## 💳 Payment Integration Workflow (Zelle)

### Payment Flow Diagram
```
┌────────────┐     ┌──────────────┐     ┌──────────────┐     ┌─────────────┐
│ Member     │────▶│ Payment      │────▶│ Zelle Pay    │────▶│ Database    │
│ Portal     │     │ Form         │     │ Integration  │     │ Transaction │
└────────────┘     └──────────────┘     └──────────────┘     └─────────────┘
                          │                                          │
                          ▼                                          ▼
                   ┌──────────────┐                          ┌─────────────┐
                   │ Admin        │◀─────────────────────────│ Verification│
                   │ Dashboard    │                          │ Queue       │
                   └──────────────┘                          └─────────────┘
```

### Payment Types
```javascript
const paymentTypes = [
    { type: 'membership', label: 'Membership Fee', amounts: [50, 30, 15, 25] },
    { type: 'event', label: 'Event Registration', dynamic: true },
    { type: 'donation', label: 'Donation', custom: true },
    { type: 'custom', label: 'Custom Amount', custom: true }
];
```

### API Endpoints
```javascript
// Payment Processing Endpoints
const paymentAPIs = {
    submit: { method: 'POST', url: '/api/submit-member-payment' },
    history: { method: 'GET', url: '/api/member-payment-history' },
    receipt: { method: 'GET', url: '/api/download-receipt/{payment_id}' },
    verify: { method: 'POST', url: '/admin/verify-payment/{payment_id}' }
};
```

### Database Tables
```sql
-- ZellePayment Table
CREATE TABLE ZellePayment (
    id INTEGER PRIMARY KEY,
    member_id INTEGER,
    amount DECIMAL(10,2),
    payment_type VARCHAR(50),
    zelle_confirmation VARCHAR(100),
    status VARCHAR(20),  -- pending, verified, approved, rejected
    created_at TIMESTAMP,
    verified_at TIMESTAMP,
    verified_by INTEGER
);

-- BudgetTransaction Table
CREATE TABLE BudgetTransaction (
    id INTEGER PRIMARY KEY,
    payment_id INTEGER,
    category VARCHAR(50),
    amount DECIMAL(10,2),
    description TEXT,
    transaction_date TIMESTAMP
);
```

---

## 🔧 Admin Dashboard Workflow

### Test Modules (16 Total)
```javascript
const adminTestModules = [
    // Authentication
    { id: 'login', name: 'Admin Login Process', api: '/admin/login' },
    { id: 'session', name: 'Session Management', api: null },
    
    // Dashboard Analytics
    { id: 'stats', name: 'Real-time Statistics', api: '/api/admin/stats' },
    { id: 'activity', name: 'Activity Feed', api: '/api/admin/recent-activity' },
    { id: 'charts', name: 'Charts & Graphs', api: null },
    
    // Member Management
    { id: 'memberList', name: 'Member List', api: '/api/admin/members' },
    { id: 'memberAdd', name: 'Add Member', api: null },
    { id: 'memberEdit', name: 'Edit Member', api: null },
    { id: 'memberSearch', name: 'Search/Filter', api: null },
    
    // Financial Management
    { id: 'transaction', name: 'Transaction Management', api: '/api/admin/finances' },
    { id: 'budget', name: 'Budget Tracking', api: null },
    { id: 'report', name: 'Financial Reports', api: null },
    
    // Communication
    { id: 'message', name: 'Message Management', api: '/api/admin/messages' },
    { id: 'notification', name: 'Notifications', api: null },
    { id: 'newsletter', name: 'Newsletter System', api: null },
    
    // Meetings
    { id: 'meetingSchedule', name: 'Meeting Scheduling', api: null },
    { id: 'meetingIntegration', name: 'Virtual Meeting Integration', api: null },
    
    // System
    { id: 'settings', name: 'System Settings', api: null },
    { id: 'security', name: 'Security Features', api: null }
];
```

### Status Indicator Pattern
```javascript
function setTestStatus(statusId, status, message = '') {
    const indicator = document.getElementById(statusId);
    indicator.className = `status-indicator status-${status}`;
    // status: 'pending', 'testing', 'success', 'error'
}
```

### Progress Tracking
```javascript
let testsCompleted = 0;
const totalTests = 16;

function updateProgress() {
    const percentage = (testsCompleted / totalTests) * 100;
    document.getElementById('overallProgress').style.width = percentage + '%';
}
```

---

## 📬 Feedback/Complaint Workflow

### Feedback Form Fields
```javascript
const feedbackModel = {
    subject: { type: 'text', required: true },
    category: { 
        type: 'select', 
        options: ['general', 'event', 'facility', 'service', 'other'] 
    },
    priority: { 
        type: 'select', 
        options: ['low', 'medium', 'high', 'urgent'] 
    },
    description: { type: 'textarea', required: true },
    isAnonymous: { type: 'checkbox', default: false }
};
```

### Demo Automation Steps
```javascript
const demoSteps = [
    { action: "Accessing Feedback Form", delay: 2000 },
    { action: "Analyzing Form Structure", delay: 2500 },
    { action: "Filling Subject Field", delay: 3000 },
    { action: "Selecting Category", delay: 2000 },
    { action: "Setting Priority Level", delay: 2000 },
    { action: "Entering Detailed Description", delay: 4000 },
    { action: "Configuring Privacy Settings", delay: 2000 },
    { action: "Submitting Feedback", delay: 2500 }
];
```

---

## 🎨 Common CSS Patterns

### Glass-Morphism Effect
```css
.glass-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}
```

### Gradient Backgrounds
```css
/* Purple Theme (Demo Pages) */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Orange Theme (Feedback) */
background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);

/* Button Gradients */
.btn-primary { background: linear-gradient(45deg, #00d4ff, #0099cc); }
.btn-secondary { background: linear-gradient(45deg, #ff0096, #cc0077); }
.btn-success { background: linear-gradient(45deg, #28a745, #20c997); }
.btn-danger { background: linear-gradient(45deg, #dc3545, #fd7e14); }
```

### Hover Animations
```css
.card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}

/* Glow Effect */
.highlight {
    box-shadow: 0 0 30px rgba(0, 212, 255, 0.6);
    animation: glow 2s infinite;
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 30px rgba(0, 212, 255, 0.6); }
    50% { box-shadow: 0 0 40px rgba(0, 212, 255, 0.9); }
}
```

### Progress Indicator
```css
.step {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.2);
}
.step.active { background: linear-gradient(45deg, #00d4ff, #0099cc); }
.step.completed { background: linear-gradient(45deg, #00ff7f, #00cc66); }
```

---

## 🔌 Backend API Integration (Flask → Wix Velo)

### Flask to Wix Velo Mapping

| Flask Route | Wix Backend Function | Collection |
|-------------|---------------------|------------|
| `GET /members` | `getMembers()` | Members |
| `POST /import-members` | `importMembers(file)` | Members |
| `GET /surveys` | `getSurveys()` | Surveys |
| `POST /create-survey` | `createSurvey(data)` | Surveys |
| `POST /survey/{id}/submit` | `submitSurveyResponse(id, data)` | SurveyResponses |
| `POST /send-notifications` | `sendNotifications(surveyId)` | - |
| `POST /verify-member/{id}` | `verifyMember(id)` | Members |
| `GET /api/member-stats` | `getMemberStats()` | Members |
| `GET /api/survey-stats/{id}` | `getSurveyStats(id)` | Surveys |

### Wix Velo Backend Pattern
```javascript
// backend/members.jsw
import wixData from 'wix-data';

export async function getMembers(options = {}) {
    let query = wixData.query('Members');
    
    if (options.filter) {
        query = query.contains('name', options.filter);
    }
    
    const results = await query.find();
    return results.items;
}

export async function createMember(memberData) {
    const result = await wixData.insert('Members', {
        ...memberData,
        createdAt: new Date(),
        status: 'active'
    });
    return result;
}
```

---

## 📱 Mobile/Responsive Patterns

### Breakpoints
```css
@media (max-width: 768px) {
    .header-content { flex-direction: column; }
    .nav-menu { gap: 20px; }
    .stats-container { grid-template-columns: repeat(2, 1fr); }
    .events-grid { grid-template-columns: 1fr; }
    .form-row { grid-template-columns: 1fr; }
}
```

### Touch-Friendly Elements
```css
.btn, .menu-card, .event-card {
    min-height: 44px;  /* iOS touch target */
    min-width: 44px;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
}
```

---

## ✅ Implementation Checklist for Wix

### Phase 1: Core Pages
- [ ] Landing page with navigation
- [ ] Stats section with dynamic data
- [ ] Quick access menu grid
- [ ] Footer with contact info

### Phase 2: Events System
- [ ] Events repeater with filtering
- [ ] Event detail modal
- [ ] Event registration flow
- [ ] Admin event management

### Phase 3: Member Management
- [ ] Registration multi-step form
- [ ] Member login/authentication
- [ ] Member profile page
- [ ] Member directory

### Phase 4: Payment Integration
- [ ] Payment form
- [ ] Zelle integration guide
- [ ] Transaction recording
- [ ] Admin verification dashboard

### Phase 5: Communication
- [ ] Feedback form
- [ ] Newsletter signup
- [ ] Notification system
- [ ] Admin messaging

### Phase 6: Admin Dashboard
- [ ] Stats dashboard
- [ ] Member management
- [ ] Financial tracking
- [ ] System settings

---

## 🎯 Key Takeaways

1. **Consistent UI Patterns**: All pages use glass-morphism cards, gradient backgrounds, and hover animations
2. **Progress Feedback**: Multi-step forms show progress indicators
3. **Status Badges**: Events use color-coded status badges
4. **API Testing**: Admin dashboard includes comprehensive API testing
5. **Demo APIs**: Pages expose `window.demoAPI` for automated demonstrations
6. **Mobile-First**: Responsive grid layouts with appropriate breakpoints

---

*Generated from backup_20250815_185359 analysis*
*Last Updated: February 7, 2026*
