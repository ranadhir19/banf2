# Wix Premium Business Plan - Complete Analysis for BANF Jacksonville

## 📊 Executive Summary

This document analyzes the **Wix Premium Business Plan** capabilities and maps them to BANF Jacksonville's existing web services implemented in the survey folder. The goal is to design a comprehensive application that leverages Wix's platform while maintaining all current functionality.

---

## 🏷️ Wix Premium Business Plan Features

### Plan Details
| Feature | Business Plan Limit |
|---------|-------------------|
| Storage | 100GB |
| Video Hours | 10 hours |
| Bandwidth | Unlimited |
| Free Domain | 1 year |
| Remove Wix Ads | ✅ Yes |
| SSL Certificate | ✅ Included |
| Customer Accounts | ✅ Unlimited |
| Accept Online Payments | ✅ Yes |

---

## 🗄️ Database Capabilities

### Wix CMS (Content Management System)

#### Native Wix Database (Collections)
- **Type**: NoSQL-like document store
- **Max Collections**: Unlimited
- **Max Items per Collection**: 500,000+ (varies by plan)
- **Field Types Supported**:
  - Text (single-line, multi-line, rich text)
  - Number (integer, decimal)
  - Boolean
  - Date/Time
  - Image/File URLs
  - Reference (relationships)
  - Array (multi-reference)
  - Object/JSON
  - Address
  - Rich Media

#### Collection Types
```javascript
// Wix CMS Collection Types
1. Site Content - Public data (events, blog posts)
2. Form Submissions - User-submitted data
3. Member Data - Private member information
4. Custom Collections - Your own data structures
```

### External Database Integration
Wix supports connecting to external databases:
- **Google Cloud SQL** (MySQL, PostgreSQL)
- **Amazon RDS** (MySQL, PostgreSQL)
- **Microsoft Azure SQL**
- **MongoDB Atlas**
- **Custom REST APIs**

---

## 🔌 API Services Available

### Wix Velo APIs (180+ APIs)

#### Core APIs
| API Category | Description | Use Case for BANF |
|--------------|-------------|-------------------|
| **wix-data** | CRUD operations on collections | Member management, events |
| **wix-members** | Member authentication & profiles | Login, registration |
| **wix-users** | User management | Admin access control |
| **wix-crm** | Contact management | Communication tracking |
| **wix-events** | Event management | Durga Puja, cultural events |
| **wix-bookings** | Appointment scheduling | Venue booking |
| **wix-ecom** | E-commerce operations | Membership payments |
| **wix-pay** | Payment processing | Zelle alternative |
| **wix-billing** | Subscription management | Annual memberships |

#### Communication APIs
| API | Function |
|-----|----------|
| **wix-email** | Send transactional emails |
| **wix-chat** | Live chat functionality |
| **wix-notifications** | Push notifications |
| **wix-sms** (via integrations) | SMS notifications |

#### Content APIs
| API | Function |
|-----|----------|
| **wix-media** | Image/video management |
| **wix-blog** | Blog posts & articles |
| **wix-forum** | Community discussions |
| **wix-stores** | Product management |

#### Developer APIs
| API | Function |
|-----|----------|
| **wix-fetch** | HTTP requests to external services |
| **wix-http-functions** | Custom REST endpoints |
| **wix-secrets** | Secure credential storage |
| **wix-router** | Custom URL routing |
| **wix-realtime** | Real-time data sync |
| **wix-storage** | Client-side storage |

---

## 🎯 BANF Existing Services Mapping

### Current Survey Folder Services Analysis

Based on analysis of `C:\projects\survey\models\enhanced_database.py` and `enhanced_app.py`:

| Existing Service | Current Tech | Wix Equivalent | Migration Complexity |
|-----------------|--------------|----------------|---------------------|
| **Member Management** | SQLAlchemy/SQLite | wix-members + Collections | Medium |
| **Admin Authentication** | Flask-Login | wix-members (roles) | Low |
| **Event Feedback** | Custom Model | wix-forms + Collections | Low |
| **Financial Records** | SQLAlchemy | Collections + wix-pay | Medium |
| **Meeting Minutes** | SQLAlchemy | Collections + Blog | Low |
| **Survey System** | Custom | wix-forms | Low |
| **Complaint System** | Custom (Encrypted) | Collections + Privacy Rules | High |
| **Radio Station** | Custom Streaming | External + wix-fetch | High |
| **Zelle Payments** | Custom Verification | wix-pay + Webhooks | Medium |
| **E-Magazine** | SQLAlchemy | wix-blog + Media | Low |
| **Jacksonville Guide** | SQLAlchemy | Collections + Maps | Low |

---

## 📐 Wix Collection Schema Design

### Members Collection
```javascript
// Members Collection Schema
{
  _id: "system-generated",
  _owner: "member-user-id",
  _createdDate: "auto",
  _updatedDate: "auto",
  
  // Personal Info
  fullName: "Text",
  email: "Text",
  phone: "Text",
  address: "Address",
  
  // Membership
  membershipType: "Text", // individual, family, senior
  membershipStatus: "Text", // active, inactive, pending
  membershipStartDate: "Date",
  membershipEndDate: "Date",
  
  // Family Members (JSON array)
  familyMembers: "Text", // Stored as JSON string
  
  // Financial
  feesDue: "Number",
  totalPaid: "Number",
  
  // Verification
  isVerified: "Boolean",
  verificationDate: "Date"
}
```

### Events Collection
```javascript
// Events Collection Schema
{
  _id: "system-generated",
  _createdDate: "auto",
  
  // Event Details
  title: "Text",
  eventType: "Text", // durga_puja, saraswati_puja, etc.
  description: "RichText",
  
  // Timing
  eventDate: "DateTime",
  endDate: "DateTime",
  registrationDeadline: "Date",
  
  // Venue
  venueName: "Text",
  venueAddress: "Address",
  
  // Capacity & Pricing
  maxAttendees: "Number",
  currentRegistrations: "Number",
  ticketPrice: "Number",
  memberDiscount: "Number",
  
  // Media
  featuredImage: "Image",
  galleryImages: "MediaGallery",
  
  // Status
  isActive: "Boolean",
  isFeatured: "Boolean"
}
```

### Financial Records Collection
```javascript
// FinancialRecords Collection Schema
{
  _id: "system-generated",
  _owner: "admin-id",
  _createdDate: "auto",
  
  // Transaction Type
  transactionType: "Text", // income, expense
  category: "Text", // membership, sponsorship, event, etc.
  subCategory: "Text",
  
  // Amount
  amount: "Number",
  description: "Text",
  transactionDate: "Date",
  
  // Payment Details
  paymentMethod: "Text", // zelle, check, cash, card
  receiptNumber: "Text",
  
  // Association
  memberId: "Reference", // Members collection
  eventId: "Reference", // Events collection
  
  // Approval
  isApproved: "Boolean",
  approvedBy: "Reference", // Admins collection
  approvedDate: "Date",
  
  // Documentation
  receiptFile: "Document"
}
```

---

## 🔧 Wix Velo Code Examples

### Member Registration with Payment Verification

```javascript
// backend/members.jsw (Wix Velo Backend)
import wixData from 'wix-data';
import wixPay from 'wix-pay-backend';
import wixMembers from 'wix-members-backend';
import { sendEmail } from 'backend/email.jsw';

/**
 * Register a new member with payment verification
 */
export async function registerMember(memberData, paymentInfo) {
    try {
        // 1. Verify payment
        const paymentVerified = await verifyPayment(paymentInfo);
        if (!paymentVerified) {
            return { success: false, error: 'Payment verification failed' };
        }
        
        // 2. Create member in CMS
        const memberRecord = {
            fullName: memberData.fullName,
            email: memberData.email,
            phone: memberData.phone,
            membershipType: memberData.membershipType,
            membershipStatus: 'pending',
            membershipStartDate: new Date(),
            feesDue: 0,
            isVerified: false
        };
        
        const result = await wixData.insert('Members', memberRecord);
        
        // 3. Create Wix Member account
        const wixMember = await wixMembers.register(memberData.email, memberData.password, {
            contactInfo: {
                firstName: memberData.firstName,
                lastName: memberData.lastName,
                phones: [memberData.phone]
            }
        });
        
        // 4. Record payment
        await recordPayment({
            memberId: result._id,
            amount: paymentInfo.amount,
            paymentMethod: paymentInfo.method,
            transactionType: 'income',
            category: 'membership'
        });
        
        // 5. Send confirmation email
        await sendEmail(memberData.email, 'welcome', {
            name: memberData.fullName,
            membershipType: memberData.membershipType
        });
        
        return { success: true, memberId: result._id };
        
    } catch (error) {
        console.error('Registration error:', error);
        return { success: false, error: error.message };
    }
}
```

### Event Management System

```javascript
// backend/events.jsw (Wix Velo Backend)
import wixData from 'wix-data';

/**
 * Get all upcoming events
 */
export async function getUpcomingEvents() {
    const now = new Date();
    
    return wixData.query('Events')
        .ge('eventDate', now)
        .eq('isActive', true)
        .ascending('eventDate')
        .find();
}

/**
 * Register member for event
 */
export async function registerForEvent(eventId, memberId, attendees) {
    // Check capacity
    const event = await wixData.get('Events', eventId);
    if (event.currentRegistrations >= event.maxAttendees) {
        return { success: false, error: 'Event is full' };
    }
    
    // Create registration
    const registration = {
        eventId: eventId,
        memberId: memberId,
        attendeeCount: attendees.length,
        attendeeDetails: JSON.stringify(attendees),
        registrationDate: new Date(),
        status: 'confirmed'
    };
    
    await wixData.insert('EventRegistrations', registration);
    
    // Update event count
    await wixData.update('Events', {
        _id: eventId,
        currentRegistrations: event.currentRegistrations + attendees.length
    });
    
    return { success: true };
}
```

### Admin Dashboard Data Aggregation

```javascript
// backend/admin.jsw (Wix Velo Backend)
import wixData from 'wix-data';

/**
 * Get dashboard statistics
 */
export async function getDashboardStats() {
    const now = new Date();
    const yearStart = new Date(now.getFullYear(), 0, 1);
    
    // Parallel queries for performance
    const [members, income, expenses, events] = await Promise.all([
        // Total active members
        wixData.query('Members')
            .eq('membershipStatus', 'active')
            .count(),
        
        // Total income this year
        wixData.query('FinancialRecords')
            .eq('transactionType', 'income')
            .ge('transactionDate', yearStart)
            .sum('amount'),
        
        // Total expenses this year
        wixData.query('FinancialRecords')
            .eq('transactionType', 'expense')
            .ge('transactionDate', yearStart)
            .sum('amount'),
        
        // Upcoming events
        wixData.query('Events')
            .ge('eventDate', now)
            .eq('isActive', true)
            .count()
    ]);
    
    return {
        totalMembers: members,
        totalIncome: income || 0,
        totalExpenses: expenses || 0,
        netBalance: (income || 0) - (expenses || 0),
        upcomingEvents: events
    };
}
```

---

## 🔐 Security & Privacy Implementation

### Data Privacy Rules
```javascript
// collections/Members.json (Permissions)
{
    "permissions": {
        "read": {
            "anyone": false,
            "member": "owner", // Members can only see their own data
            "admin": true
        },
        "create": {
            "anyone": true, // For registration
            "member": false,
            "admin": true
        },
        "update": {
            "anyone": false,
            "member": "owner",
            "admin": true
        },
        "delete": {
            "anyone": false,
            "member": false,
            "admin": true
        }
    }
}
```

### Anonymous Complaint System
```javascript
// backend/complaints.jsw
import wixData from 'wix-data';
import wixSecretsBackend from 'wix-secrets-backend';
import { encrypt, decrypt } from 'backend/encryption.jsw';

/**
 * Submit anonymous complaint
 */
export async function submitAnonymousComplaint(complaintData, memberInfo, isAnonymous) {
    const encryptionKey = await wixSecretsBackend.getSecret('ENCRYPTION_KEY');
    
    let record = {
        title: complaintData.title,
        description: complaintData.description,
        category: complaintData.category,
        priority: complaintData.priority || 'medium',
        isAnonymous: isAnonymous,
        status: 'submitted',
        submittedAt: new Date()
    };
    
    if (isAnonymous && memberInfo) {
        // Encrypt sensitive data
        record.memberNameEncrypted = await encrypt(memberInfo.name, encryptionKey);
        record.memberEmailEncrypted = await encrypt(memberInfo.email, encryptionKey);
        record.memberPhoneEncrypted = await encrypt(memberInfo.phone, encryptionKey);
    } else if (!isAnonymous) {
        record.memberName = memberInfo.name;
        record.memberEmail = memberInfo.email;
        record.memberPhone = memberInfo.phone;
    }
    
    return wixData.insert('Complaints', record);
}
```

---

## 📱 Mobile Responsiveness

Wix automatically provides:
- Responsive design breakpoints
- Mobile-specific layouts
- Touch-optimized interactions
- PWA capabilities (installable web app)

---

## 💳 Payment Integration

### Supported Payment Methods
| Method | Integration |
|--------|-------------|
| Credit/Debit Cards | Wix Payments (Stripe) |
| PayPal | Native integration |
| Apple Pay | Supported |
| Google Pay | Supported |
| Manual (Check/Cash) | Custom tracking |
| Zelle | Manual verification + tracking |

### Zelle Payment Tracking
```javascript
// backend/payments.jsw
import wixData from 'wix-data';

/**
 * Record and verify Zelle payment
 */
export async function recordZellePayment(paymentData) {
    const payment = {
        zelleCode: paymentData.zelleCode,
        senderName: paymentData.senderName,
        senderEmail: paymentData.senderEmail,
        amount: paymentData.amount,
        paymentType: paymentData.paymentType, // membership, event, donation
        description: paymentData.description,
        paymentDate: new Date(paymentData.paymentDate),
        isVerified: false,
        status: 'pending'
    };
    
    return wixData.insert('ZellePayments', payment);
}

/**
 * Admin verifies Zelle payment
 */
export async function verifyZellePayment(paymentId, adminId, notes) {
    return wixData.update('ZellePayments', {
        _id: paymentId,
        isVerified: true,
        status: 'verified',
        verifiedBy: adminId,
        verificationNotes: notes,
        verifiedAt: new Date()
    });
}
```

---

## 🎨 Third-Party Integrations

### Available via Wix App Market (500+ apps)
| Category | Recommended Apps |
|----------|-----------------|
| Email Marketing | Mailchimp, Constant Contact |
| CRM | HubSpot, Salesforce |
| Analytics | Google Analytics, Hotjar |
| Social Media | Facebook, Instagram feeds |
| Communication | WhatsApp, Twilio SMS |
| Scheduling | Calendly, Acuity |
| Forms | JotForm, Typeform |

### Custom Integrations via wix-fetch
```javascript
// backend/integrations.jsw
import { fetch } from 'wix-fetch';

/**
 * Send SMS via Twilio
 */
export async function sendSMS(to, message) {
    const accountSid = await wixSecretsBackend.getSecret('TWILIO_SID');
    const authToken = await wixSecretsBackend.getSecret('TWILIO_TOKEN');
    const fromNumber = await wixSecretsBackend.getSecret('TWILIO_PHONE');
    
    const response = await fetch(
        `https://api.twilio.com/2010-04-01/Accounts/${accountSid}/Messages.json`,
        {
            method: 'POST',
            headers: {
                'Authorization': 'Basic ' + btoa(`${accountSid}:${authToken}`),
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `To=${to}&From=${fromNumber}&Body=${encodeURIComponent(message)}`
        }
    );
    
    return response.json();
}
```

---

## 📊 Feature Availability Matrix

### Current BANF Features vs Wix Capabilities

| Feature | Current Implementation | Wix Capability | Notes |
|---------|----------------------|----------------|-------|
| ✅ Member Registration | Flask + SQLite | wix-members + Collections | Full support |
| ✅ Member Login | Flask-Login | wix-members | SSO ready |
| ✅ Family Members | JSON in SQLite | Collections (nested) | Full support |
| ✅ Admin Dashboard | Flask Templates | Wix Dashboard + Custom | Enhanced |
| ✅ Event Management | SQLAlchemy | wix-events + Collections | Better features |
| ✅ Event Feedback | Custom Model | wix-forms | Built-in analytics |
| ✅ Financial Tracking | SQLAlchemy | Collections | Full support |
| ✅ Meeting Minutes | SQLAlchemy | Collections + Blog | Better formatting |
| ✅ Survey System | Custom | wix-forms | Much easier |
| ⚠️ Complaint System | Encrypted | Collections + Secrets | Needs custom encryption |
| ⚠️ Radio Station | Custom streaming | External integration | Limited native support |
| ✅ Zelle Payments | Manual tracking | Collections + workflow | Full support |
| ✅ E-Magazine | SQLAlchemy | wix-blog + Media | Better media handling |
| ✅ Jacksonville Guide | SQLAlchemy | Collections + Maps | Google Maps integration |

**Legend**: ✅ Full Support | ⚠️ Partial/Custom Required | ❌ Not Supported

---

## 🚀 Migration Strategy

### Phase 1: Core Setup (Week 1-2)
1. Set up Wix Premium Business account
2. Create all database collections
3. Configure member authentication
4. Set up admin roles and permissions

### Phase 2: Data Migration (Week 3-4)
1. Export existing SQLite data
2. Transform to Wix collection format
3. Import via Wix Data API
4. Verify data integrity

### Phase 3: Feature Implementation (Week 5-8)
1. Member portal pages
2. Event management system
3. Payment tracking
4. Admin dashboard

### Phase 4: Advanced Features (Week 9-12)
1. Radio integration (external)
2. Survey system
3. Complaint system with encryption
4. E-Magazine integration

---

## 📝 Recommendations

### High Priority
1. ✅ Use Wix Members for authentication (built-in, secure)
2. ✅ Use Collections for all data storage (no migration needed)
3. ✅ Leverage Wix Events app for event management
4. ✅ Use wix-pay for payment processing

### Medium Priority
1. ⚠️ Keep radio streaming external, integrate via API
2. ⚠️ Use Wix Forms for surveys (easier than custom)
3. ⚠️ Implement Zelle tracking as custom collection

### Consider Alternatives
1. 🔄 Complaint encryption - use Wix Secrets + custom backend code
2. 🔄 Radio station - consider dedicated streaming service + embed

---

## 📚 Resources

- [Wix Velo Documentation](https://dev.wix.com/docs/develop-websites)
- [Wix CMS Guide](https://support.wix.com/en/article/cms-formerly-content-manager-creating-a-collection)
- [Wix Members API](https://www.wix.com/velo/reference/wix-members-backend)
- [Wix Pay API](https://www.wix.com/velo/reference/wix-pay-backend)
- [Wix HTTP Functions](https://www.wix.com/velo/reference/wix-http-functions)

---

*Document Version: 1.0*  
*Created: February 6, 2026*  
*For: BANF Jacksonville Wix Migration Project*
