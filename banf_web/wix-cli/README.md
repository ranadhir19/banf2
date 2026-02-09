# BANF Wix Velo CLI

This project contains the backend services and configuration for the BANF (Bengali Association of North Florida) Wix website.

## 📁 Project Structure

```
wix-cli/
├── package.json           # Dependencies and scripts
├── wix.config.json        # Wix CLI configuration
├── tsconfig.json          # TypeScript configuration
├── .wixrc                 # Site configuration
└── src/
    ├── backend/           # Velo backend services
    │   ├── index.js       # Main entry point
    │   ├── http-functions.js  # HTTP API endpoints
    │   ├── data.js        # Data hooks
    │   ├── jobs.config.js # Scheduled jobs
    │   ├── members.js     # Member management
    │   ├── member-auth.js # Member authentication
    │   ├── events.js      # Event management
    │   ├── radio.js       # Radio scheduling
    │   ├── sponsors.js    # Sponsor management
    │   ├── payments.js    # Payment processing
    │   └── admin-auth.js  # Admin authentication
    └── public/            # Frontend utilities
        ├── api-client.js  # API client
        └── utils.js       # Utility functions
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd wix-cli
npm install
```

### 2. Login to Wix

```bash
npm run login
# or
npx wix auth login
```

This will open a browser window for authentication.

### 3. Sync Code to Wix

```bash
npm run sync
# or
npx wix sync
```

### 4. Start Development Server

```bash
npm run dev
# or
npx wix dev
```

## 📦 Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start local development server |
| `npm run build` | Build the project |
| `npm run preview` | Preview the site |
| `npm run sync` | Sync code to Wix |
| `npm run login` | Authenticate with Wix |
| `npm run logout` | Log out from Wix |
| `npm run whoami` | Show current authenticated user |
| `npm run generate-types` | Generate TypeScript types for collections |

## 🔌 API Endpoints

The HTTP functions expose the following REST API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/_functions/health` | GET | Health check |
| `/_functions/members` | GET | List all members |
| `/_functions/members` | POST | Create new member |
| `/_functions/events` | GET | List all events |
| `/_functions/events` | POST | Create new event |
| `/_functions/radioSchedule` | GET | Get radio schedule |
| `/_functions/radioStream` | GET | Get stream info |
| `/_functions/sponsors` | GET | List sponsors |
| `/_functions/payments` | POST | Process payment |

## 📊 CMS Collections

The backend services use these Wix CMS collections:

| Collection | Description |
|------------|-------------|
| `Members` | Member profiles and status |
| `Events` | Event listings and details |
| `EventRegistrations` | Event registration records |
| `Sponsors` | Sponsor information |
| `RadioSchedule` | Radio show schedule |
| `Payments` | Payment records |
| `Admins` | Admin users and roles |
| `AdminLogs` | Admin action logs |

## 🔐 Authentication

### Member Authentication
- `registerMember(email, password, memberInfo)` - Register new member
- `loginMember(email, password)` - Login member
- `logoutMember()` - Logout current member
- `getCurrentMember()` - Get current logged-in member

### Admin Authentication
- `isAdmin()` - Check if current user is admin
- `getAdminRole()` - Get current admin's role
- `hasRole(role)` - Check if user has specific role

### Admin Roles
- `super_admin` - Full access
- `admin` - Administrative access
- `moderator` - Moderation access
- `editor` - Content editing access

## 🔧 Configuration

### Site Configuration (`.wixrc`)
```json
{
  "siteId": "c13ae8c5-7053-4f2d-9a9a-371869be4395",
  "siteName": "banf1",
  "siteUrl": "https://banfwix.wixsite.com/banf1"
}
```

### Wix Config (`wix.config.json`)
```json
{
  "siteId": "c13ae8c5-7053-4f2d-9a9a-371869be4395",
  "projectType": "velo",
  "modules": {
    "backend": { "srcDir": "src/backend" },
    "public": { "srcDir": "src/public" }
  }
}
```

## 📅 Scheduled Jobs

| Job | Schedule | Description |
|-----|----------|-------------|
| `dailyCleanup` | 2 AM daily | Clean up expired payments |
| `sendEventReminders` | 9 AM daily | Send event reminders |
| `weeklyMembershipCheck` | 10 AM Sundays | Check expiring memberships |
| `monthlyAnalyticsReport` | 6 AM 1st of month | Generate analytics report |

## 🛠️ Development Workflow

1. **Make changes** to files in `src/`
2. **Sync to Wix**: `npm run sync`
3. **Preview changes**: `npm run preview`
4. **Publish**: Use Wix Editor to publish

## 📚 Resources

- [Wix Velo Documentation](https://www.wix.com/velo/reference/)
- [Wix CLI Documentation](https://www.wix.com/velo/reference/cli)
- [Wix Data API](https://www.wix.com/velo/reference/wix-data)
- [Wix HTTP Functions](https://www.wix.com/velo/reference/wix-http-functions)

## 🆘 Troubleshooting

### Authentication Issues
```bash
# Clear auth and re-login
npm run logout
npm run login
```

### Sync Issues
```bash
# Generate fresh types
npm run generate-types

# Then sync
npm run sync
```

### Build Errors
Check that all imports are correct and all required Wix modules are in `package.json`.

## 📞 Support

For issues with this project, contact the BANF development team.
