# BANF Wix Web Application

A comprehensive Wix Velo-based web application for Bay Area Natun Fasal (BANF) community organization, migrating from Flask/SQLAlchemy to Wix Premium Business platform.

## 📁 Project Structure

```
banf_web/
├── README.md                           # This file
├── WIX_PREMIUM_BUSINESS_ANALYSIS.md    # Detailed Wix capabilities analysis
├── wix_migration_agent.py              # Python agent for migration planning
├── collection_schemas.json             # Wix CMS collection definitions
└── velo_backend/                       # Wix Velo backend modules
    ├── members.jsw                     # Member management
    ├── events.jsw                      # Events & registration
    ├── finance.jsw                     # Financial records & Zelle
    ├── admin.jsw                       # Admin dashboard & activities
    ├── complaints.jsw                  # Anonymous complaint system
    ├── surveys.jsw                     # Survey creation & responses
    ├── radio.jsw                       # Community radio integration
    ├── magazine.jsw                    # E-Magazine management
    ├── guide.jsw                       # Jacksonville newcomer guide
    └── email.jsw                       # Email notification service
```

## 🎯 Features

### Member Management
- Member registration & verification
- Profile management with family tracking
- Membership types (General, Family, Student, Senior)
- Membership expiration & renewal tracking

### Events System
- Event creation & management
- Online registration with guest handling
- Payment integration (Wix Pay + Zelle verification)
- Event feedback with sentiment analysis
- Capacity management

### Financial Management
- Income/expense tracking
- Transaction categorization
- Zelle payment verification workflow
- Membership fee tracking
- Financial reporting & export

### Survey System
- Multiple question types (text, choice, rating, scale)
- Anonymous & authenticated responses
- Real-time analytics
- Survey cloning for templates

### Anonymous Complaint System
- Confidential submission with access codes
- Status tracking without login
- Follow-up messaging
- Admin review workflow

### Community Radio
- Stream configuration
- Show scheduling
- Song library management
- Song request system
- Listener statistics

### E-Magazine
- Issue management
- Article submission & review workflow
- Category-based browsing
- Popular articles tracking
- Member contributions

### Jacksonville Newcomer Guide
- Location-based search
- Bengali-friendly business highlighting
- User reviews & ratings
- Category filtering
- Geolocation support

## 🚀 Getting Started

### Prerequisites
- Wix Premium Business Plan
- Wix Editor with Velo enabled
- Access to Wix Dashboard

### Installation Steps

1. **Enable Velo in your Wix site**
   - Go to Wix Editor
   - Click Dev Mode → Turn on Dev Mode

2. **Create CMS Collections**
   - Open `collection_schemas.json`
   - Create each collection in Wix CMS with matching fields
   - Set appropriate permissions

3. **Add Backend Code**
   - In Wix Editor, open the code panel
   - Create a `backend` folder
   - Copy each `.jsw` file from `velo_backend/`

4. **Configure Triggered Emails**
   - Go to Automations in Wix Dashboard
   - Create triggered email templates:
     - `welcome_email`
     - `event_confirmation`
     - `payment_receipt`
     - `renewal_reminder`
     - etc.

5. **Set Up Members Area**
   - Add Wix Members area to your site
   - Configure member signup fields
   - Set up member roles (Admin, Member)

## 📊 CMS Collections Overview

| Collection | Purpose | Records Est. |
|-----------|---------|--------------|
| Members | Member profiles | 500+ |
| Admins | Administrator accounts | 10-20 |
| Events | Community events | 50+/year |
| EventRegistrations | Event signups | 1000+/year |
| EventFeedback | Post-event surveys | 500+/year |
| FinancialRecords | Income/expenses | 200+/year |
| ZellePayments | Zelle verification | 100+/year |
| Surveys | Survey definitions | 20+/year |
| SurveyResponses | Survey answers | 500+/year |
| Complaints | Anonymous complaints | Variable |
| MeetingMinutes | EC meeting records | 12+/year |
| EMagazines | Magazine issues | 4-6/year |
| EMagazineArticles | Magazine content | 50+/year |
| JacksonvilleGuide | Local resources | 200+ |
| GuideReviews | User reviews | 500+ |
| RadioStations | Station config | 1 |
| RadioSchedule | Show schedule | 20+ |
| BengaliSongs | Song library | 1000+ |
| SongRequests | User requests | Variable |
| ImportantMessages | Announcements | Variable |
| ActivityLog | Admin actions | Auto-generated |

## 🔐 Security Considerations

1. **Data Permissions**
   - Set collection permissions appropriately
   - Use `suppressAuth` sparingly and only for public features

2. **Admin Verification**
   - Always verify admin status before sensitive operations
   - Log all admin activities

3. **Anonymous Systems**
   - Complaint access codes are hashed before storage
   - No PII stored for anonymous submissions

4. **Payments**
   - Use Wix Pay for secure transactions
   - Zelle verification requires admin approval

## 📧 Email Templates Required

Create these triggered email templates in Wix:

1. `welcome_email` - New member welcome
2. `event_confirmation` - Event registration confirmation
3. `payment_receipt` - Payment confirmation
4. `renewal_reminder` - Membership renewal reminder
5. `event_reminder` - Event reminder (1 day, 1 week)
6. `survey_invitation` - Survey participation request
7. `complaint_acknowledgment` - Complaint received
8. `admin_notification` - Admin alerts
9. `newsletter` - Community newsletter
10. `article_submission` - Article submission confirmation
11. `article_approved` / `article_rejected` - Article review results
12. `password_reset` - Password reset link
13. `zelle_verification` - Zelle payment verification

## 🔄 Migration from Flask

### Data Migration Steps

1. Export existing SQLite data to JSON
2. Transform data to match Wix collection schemas
3. Use Wix Data API to import records
4. Verify data integrity

### Feature Mapping

| Flask Feature | Wix Equivalent | Status |
|--------------|----------------|--------|
| SQLAlchemy Models | CMS Collections | ✅ Ready |
| Flask Routes | Velo Backend (.jsw) | ✅ Ready |
| Jinja Templates | Wix Pages | 📝 Manual |
| Flask-Login | Wix Members | ✅ Native |
| SMTP Email | Triggered Emails | ✅ Ready |
| File Upload | Wix Media | ✅ Native |
| Zelle Tracking | Custom Collection | ✅ Ready |

## 📈 Analytics & Reporting

Built-in support for:
- Membership statistics
- Event attendance tracking
- Financial summaries
- Survey analytics
- Complaint resolution rates
- Radio listener stats
- Magazine engagement

## 🛠 Development Notes

### Velo Best Practices
- Use `wix-data` for all database operations
- Implement error handling in all functions
- Use JSON.stringify/parse for complex data
- Leverage parallel queries with `Promise.all`

### Testing
- Use Wix Preview for testing
- Test with different user roles
- Verify email delivery
- Test payment flows in sandbox

## 📞 Support

For questions about this implementation:
- Review `WIX_PREMIUM_BUSINESS_ANALYSIS.md` for capabilities
- Run `wix_migration_agent.py` for migration assessment
- Consult Wix Velo documentation: https://www.wix.com/velo

## 📄 License

This project is developed for BANF community use.

---

**Generated**: January 2025  
**Platform**: Wix Premium Business Plan  
**Technology**: Wix Velo (JavaScript)
