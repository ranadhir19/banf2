# 🚀 BANF Wix Advanced Features & Automation Guide

## Complete Integration Roadmap for Full Member Engagement Automation

**Last Updated:** January 2025  
**Version:** 2.0  
**Target Platform:** Wix Studio + Velo

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Wix Advanced Features Inventory](#wix-advanced-features)
3. [AI Agent Integration](#ai-agents)
4. [Admin Console Architecture](#admin-console)
5. [Video Streaming & Scheduling](#video-streaming)
6. [BANF Radio Scheduler](#radio-scheduler)
7. [Member Engagement Automation](#member-automation)
8. [Payment & Membership Automation](#payment-automation)
9. [Event Management System](#event-management)
10. [Vendor & Sponsor Management](#vendor-sponsor)
11. [Implementation Roadmap](#implementation)

---

## 1. Executive Summary {#executive-summary}

This document outlines the complete automation strategy for BANF's Wix-based website, leveraging all advanced Wix features including:

- **Wix AI Agents** for automated member support
- **Wix Video** for streaming and event recordings
- **Wix Bookings** for event scheduling
- **Wix Automations** for workflow triggers
- **Wix CRM** for member management
- **Wix Payments** for seamless transactions
- **Custom Velo Backend** for advanced functionality

### Goals:
✅ Zero manual work for routine operations  
✅ 24/7 automated member support  
✅ Self-service member portal  
✅ Automated event & payment workflows  
✅ Integrated radio streaming with scheduler  
✅ Real-time analytics dashboard  

---

## 2. Wix Advanced Features Inventory {#wix-advanced-features}

### 2.1 Native Wix Features Available

| Feature | Description | BANF Use Case |
|---------|-------------|---------------|
| **Wix Video** | Video hosting, streaming, live events | Event recordings, live streaming Durga Puja |
| **Wix Bookings** | Appointment/event scheduling | Cultural program registrations, volunteer slots |
| **Wix Events** | Event management with ticketing | All BANF events with RSVP tracking |
| **Wix Stores** | E-commerce | Jagriti magazine, merchandise, prasad orders |
| **Wix Members** | Membership area with login | Member-only content, directories |
| **Wix Chat** | Live chat support | Real-time member assistance |
| **Wix Forms** | Custom form builder | Feedback, registrations, surveys |
| **Wix Automations** | Workflow automation | Auto emails, reminders, notifications |
| **Wix CRM** | Contact management | Member database, communications |
| **Wix Payments** | Payment processing | Memberships, donations, tickets |
| **Wix Analytics** | Website analytics | Member engagement tracking |
| **Wix SEO** | Search optimization | Community outreach |

### 2.2 Premium Features (Wix Studio)

| Feature | Description | Required Plan |
|---------|-------------|---------------|
| **Custom Backend** | Velo server-side code | Business Elite |
| **External APIs** | Third-party integrations | Business Elite |
| **Scheduled Jobs** | Cron-like automation | Business Elite |
| **Custom HTTP Functions** | API endpoints | Business Elite |
| **Advanced Permissions** | Role-based access | Business Elite |
| **White Label** | Remove Wix branding | Scale |

---

## 3. Wix AI Agent Integration {#ai-agents}

### 3.1 Available AI Capabilities

```javascript
// Wix AI Site Assistant - Available through Wix Dashboard
// 1. AI Text Generator - Create content
// 2. AI Image Generator - Create visuals
// 3. AI SEO Tools - Optimize content
// 4. AI Chat Assistant - Member support
```

### 3.2 Custom AI Agent for BANF

**banf-ai-assistant.jsw** (Backend Module)
```javascript
// AI-powered member assistant backend
import { openai } from 'wix-ai-backend';
import wixData from 'wix-data';
import wixCRM from 'wix-crm-backend';

// BANF-specific knowledge base
const BANF_CONTEXT = `
BANF (Bengali Association of North Florida) is a 501(c)(3) cultural organization 
established in 2008. Key information:
- 200+ member families
- Major events: Durga Puja, Saraswati Puja, Pohela Boishakh, Anandadhara
- Membership: Individual $50, Family $100, Senior $35
- Payment: Zelle (treasurer@jaxbengali.org) or Square store
- President 2025-26: Dr. Ranadhir Ghosh
- Website: jaxbengali.org
`;

export async function processAIQuery(userQuery, memberId) {
    const memberContext = memberId ? await getMemberContext(memberId) : '';
    
    const response = await openai.chat.completions.create({
        model: "gpt-4",
        messages: [
            {
                role: "system",
                content: `You are BANF's helpful assistant. ${BANF_CONTEXT} ${memberContext}`
            },
            { role: "user", content: userQuery }
        ],
        max_tokens: 500
    });
    
    // Log interaction for analytics
    await logAIInteraction(userQuery, response.choices[0].message.content, memberId);
    
    return response.choices[0].message.content;
}

async function getMemberContext(memberId) {
    const member = await wixData.get("Members", memberId);
    if (member) {
        return `Member: ${member.name}, Status: ${member.membershipStatus}, Since: ${member.joinDate}`;
    }
    return '';
}

async function logAIInteraction(query, response, memberId) {
    await wixData.insert("AIInteractions", {
        query,
        response,
        memberId,
        timestamp: new Date()
    });
}
```

### 3.3 AI Chat Widget Implementation

**AIAssistant.velo.js** (Page Code)
```javascript
import { processAIQuery } from 'backend/banf-ai-assistant.jsw';
import wixUsers from 'wix-users';

$w.onReady(() => {
    $w('#aiChatInput').onKeyPress((event) => {
        if (event.key === 'Enter') {
            handleAIChat();
        }
    });
    
    $w('#aiSendBtn').onClick(() => handleAIChat());
});

async function handleAIChat() {
    const query = $w('#aiChatInput').value;
    if (!query.trim()) return;
    
    // Show typing indicator
    $w('#aiTyping').show();
    $w('#aiChatInput').value = '';
    
    // Add user message to chat
    addChatMessage(query, 'user');
    
    try {
        const memberId = wixUsers.currentUser.loggedIn ? 
                         wixUsers.currentUser.id : null;
        const response = await processAIQuery(query, memberId);
        addChatMessage(response, 'ai');
    } catch (error) {
        addChatMessage('Sorry, I encountered an error. Please try again.', 'ai');
    } finally {
        $w('#aiTyping').hide();
    }
}

function addChatMessage(message, sender) {
    const chatContainer = $w('#aiChatMessages');
    const className = sender === 'user' ? 'user-message' : 'ai-message';
    // Append message to repeater or text element
    // Implementation depends on UI design
}
```

---

## 4. Admin Console Architecture {#admin-console}

### 4.1 Admin Dashboard Structure

```
/admin (Protected Route - Admin Role Only)
├── /dashboard           - Overview & Analytics
├── /members            - Member Management
├── /events             - Event Management
├── /streaming          - Video Streaming Console
├── /radio              - Radio Scheduler
├── /payments           - Payment Tracking
├── /sponsors           - Sponsor Management
├── /vendors            - Vendor Management
├── /communications     - Email & Notifications
├── /reports            - Financial Reports
└── /settings           - System Configuration
```

### 4.2 Admin Access Control

**admin-auth.jsw** (Backend)
```javascript
import wixUsers from 'wix-users-backend';
import wixData from 'wix-data';

export async function verifyAdminAccess() {
    const currentUser = await wixUsers.currentUser;
    if (!currentUser.loggedIn) {
        return { authorized: false, reason: 'Not logged in' };
    }
    
    const userRoles = await currentUser.getRoles();
    const isAdmin = userRoles.some(role => 
        ['Admin', 'EC Member', 'Super Admin'].includes(role.name)
    );
    
    if (!isAdmin) {
        // Log unauthorized access attempt
        await wixData.insert("SecurityLogs", {
            userId: currentUser.id,
            action: "Unauthorized Admin Access Attempt",
            timestamp: new Date()
        });
    }
    
    return { authorized: isAdmin, roles: userRoles.map(r => r.name) };
}

export async function getAdminPermissions(userId) {
    const permissions = await wixData.query("AdminPermissions")
        .eq("userId", userId)
        .find();
    
    return permissions.items.length > 0 ? permissions.items[0] : {
        canManageMembers: false,
        canManageEvents: false,
        canManagePayments: false,
        canManageStreaming: false,
        canManageRadio: false
    };
}
```

---

## 5. Video Streaming & Scheduling {#video-streaming}

### 5.1 Live Streaming Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  BANF Live Streaming System              │
├─────────────────────────────────────────────────────────┤
│  Admin Creates Event → Schedule Stored in DB            │
│         ↓                                                │
│  Automated Email 24hr before → Members get link         │
│         ↓                                                │
│  Stream goes live → Wix Video or YouTube Live embed     │
│         ↓                                                │
│  Recording saved → Video Archive automatically updated  │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Streaming Console Backend

**streaming-service.jsw**
```javascript
import wixData from 'wix-data';
import { emails } from 'wix-crm-backend';
import { triggeredEmails } from 'wix-crm-backend';

// Create/Schedule a streaming event
export async function createStreamingEvent(eventData) {
    const { title, description, scheduledTime, streamUrl, category, thumbnail } = eventData;
    
    // Generate unique stream link
    const uniqueStreamId = generateStreamId();
    const publicUrl = `https://www.jaxbengali.org/live/${uniqueStreamId}`;
    
    const event = await wixData.insert("StreamingEvents", {
        title,
        description,
        scheduledTime: new Date(scheduledTime),
        streamUrl,  // YouTube Live, Vimeo, or Wix Video URL
        publicUrl,
        uniqueStreamId,
        category,  // 'durga-puja', 'cultural', 'community'
        thumbnail,
        status: 'scheduled',
        viewerCount: 0,
        createdAt: new Date()
    });
    
    // Schedule reminder emails
    await scheduleStreamReminders(event._id, scheduledTime, title, publicUrl);
    
    return { success: true, event, shareableLink: publicUrl };
}

// Schedule automated reminders
async function scheduleStreamReminders(eventId, scheduledTime, title, link) {
    const eventDate = new Date(scheduledTime);
    
    // 24-hour reminder
    const reminder24h = new Date(eventDate.getTime() - 24 * 60 * 60 * 1000);
    
    // 1-hour reminder
    const reminder1h = new Date(eventDate.getTime() - 60 * 60 * 1000);
    
    // Store reminders to be processed by scheduled job
    await wixData.insert("ScheduledReminders", {
        eventId,
        type: '24h',
        scheduledFor: reminder24h,
        emailTemplate: 'stream-reminder-24h',
        variables: { title, link, time: eventDate.toLocaleString() },
        sent: false
    });
    
    await wixData.insert("ScheduledReminders", {
        eventId,
        type: '1h',
        scheduledFor: reminder1h,
        emailTemplate: 'stream-reminder-1h',
        variables: { title, link },
        sent: false
    });
}

// Get upcoming streams for members
export async function getUpcomingStreams() {
    const now = new Date();
    const streams = await wixData.query("StreamingEvents")
        .ge("scheduledTime", now)
        .eq("status", "scheduled")
        .ascending("scheduledTime")
        .limit(10)
        .find();
    
    return streams.items;
}

// Start stream (admin action)
export async function goLive(eventId) {
    await wixData.update("StreamingEvents", {
        _id: eventId,
        status: 'live',
        actualStartTime: new Date()
    });
    
    // Send "We're Live!" notification
    const event = await wixData.get("StreamingEvents", eventId);
    await sendLiveNotification(event);
    
    return { success: true, message: 'Stream is now live!' };
}

// End stream
export async function endStream(eventId) {
    const event = await wixData.get("StreamingEvents", eventId);
    
    await wixData.update("StreamingEvents", {
        _id: eventId,
        status: 'ended',
        endTime: new Date(),
        duration: calculateDuration(event.actualStartTime, new Date())
    });
    
    // Auto-archive to Video Library
    await archiveStreamRecording(event);
    
    return { success: true };
}

function generateStreamId() {
    return 'stream-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
}
```

### 5.3 Streaming Admin UI

**StreamingConsole.velo.js**
```javascript
import { createStreamingEvent, getUpcomingStreams, goLive, endStream } from 'backend/streaming-service.jsw';
import { verifyAdminAccess } from 'backend/admin-auth.jsw';

$w.onReady(async () => {
    const { authorized } = await verifyAdminAccess();
    if (!authorized) {
        $w('#adminPanel').collapse();
        $w('#accessDenied').expand();
        return;
    }
    
    await loadUpcomingStreams();
    
    $w('#createStreamBtn').onClick(() => $w('#createStreamModal').show());
    $w('#submitStreamBtn').onClick(handleCreateStream);
});

async function handleCreateStream() {
    const eventData = {
        title: $w('#streamTitle').value,
        description: $w('#streamDescription').value,
        scheduledTime: $w('#streamDateTime').value,
        streamUrl: $w('#streamSourceUrl').value,  // YouTube/Vimeo embed URL
        category: $w('#streamCategory').value,
        thumbnail: $w('#streamThumbnail').value
    };
    
    $w('#submitStreamBtn').disable();
    $w('#submitStreamBtn').label = 'Creating...';
    
    try {
        const result = await createStreamingEvent(eventData);
        
        // Show success with shareable link
        $w('#shareableLink').text = result.shareableLink;
        $w('#successModal').show();
        
        // Copy to clipboard functionality
        $w('#copyLinkBtn').onClick(() => {
            navigator.clipboard.writeText(result.shareableLink);
            $w('#copyLinkBtn').label = 'Copied!';
        });
        
        // Refresh list
        await loadUpcomingStreams();
        
        // Clear form
        $w('#createStreamModal').hide();
        clearStreamForm();
        
    } catch (error) {
        console.error('Error creating stream:', error);
        $w('#errorMessage').text = 'Failed to create stream. Please try again.';
        $w('#errorMessage').show();
    } finally {
        $w('#submitStreamBtn').enable();
        $w('#submitStreamBtn').label = 'Create Stream Event';
    }
}

async function loadUpcomingStreams() {
    const streams = await getUpcomingStreams();
    
    $w('#streamsRepeater').data = streams.map(stream => ({
        _id: stream._id,
        title: stream.title,
        scheduledTime: formatDateTime(stream.scheduledTime),
        status: stream.status,
        publicUrl: stream.publicUrl,
        category: stream.category
    }));
}

$w('#streamsRepeater').onItemReady(($item, itemData) => {
    $item('#streamTitle').text = itemData.title;
    $item('#streamTime').text = itemData.scheduledTime;
    $item('#streamStatus').text = itemData.status.toUpperCase();
    
    if (itemData.status === 'scheduled') {
        $item('#goLiveBtn').show();
        $item('#endStreamBtn').hide();
        $item('#goLiveBtn').onClick(async () => {
            await goLive(itemData._id);
            await loadUpcomingStreams();
        });
    } else if (itemData.status === 'live') {
        $item('#goLiveBtn').hide();
        $item('#endStreamBtn').show();
        $item('#endStreamBtn').onClick(async () => {
            await endStream(itemData._id);
            await loadUpcomingStreams();
        });
    }
    
    $item('#copyStreamLink').onClick(() => {
        navigator.clipboard.writeText(itemData.publicUrl);
    });
});
```

---

## 6. BANF Radio Scheduler {#radio-scheduler}

### 6.1 Radio Programming Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   BANF Radio System                      │
├─────────────────────────────────────────────────────────┤
│  Program Schedule (Weekly Recurring)                     │
│  ├── Morning: Bengali Songs Playlist (6 AM - 10 AM)     │
│  ├── Midday: Rabindra Sangeet (10 AM - 2 PM)            │
│  ├── Afternoon: Modern Bengali Music (2 PM - 6 PM)      │
│  ├── Evening: Adhunik/Film Songs (6 PM - 9 PM)          │
│  ├── Night: Instrumental/Classical (9 PM - 12 AM)       │
│  └── Late Night: Mixed Playlist (12 AM - 6 AM)          │
├─────────────────────────────────────────────────────────┤
│  Special Programs (Scheduled)                            │
│  ├── Sunday 10 AM: Mahalaya Special (Oct)               │
│  ├── Friday 7 PM: Community Hour                         │
│  └── Cultural Events: Live Stream Integration            │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Radio Schedule Backend

**radio-scheduler.jsw**
```javascript
import wixData from 'wix-data';

// Define program categories
const PROGRAM_CATEGORIES = {
    BENGALI_SONGS: 'bengali-songs',
    RABINDRA_SANGEET: 'rabindra-sangeet',
    MODERN_BENGALI: 'modern-bengali',
    ADHUNIK_FILM: 'adhunik-film',
    INSTRUMENTAL: 'instrumental-classical',
    MIXED: 'mixed-playlist',
    SPECIAL: 'special-program',
    LIVE: 'live-event'
};

// Weekly schedule template
const DEFAULT_SCHEDULE = [
    { dayOfWeek: 0, startHour: 6, endHour: 10, category: 'BENGALI_SONGS', title: 'সকালের সুর' },
    { dayOfWeek: 0, startHour: 10, endHour: 14, category: 'RABINDRA_SANGEET', title: 'রবীন্দ্র সঙ্গীত' },
    { dayOfWeek: 0, startHour: 14, endHour: 18, category: 'MODERN_BENGALI', title: 'আধুনিক বাংলা' },
    { dayOfWeek: 0, startHour: 18, endHour: 21, category: 'ADHUNIK_FILM', title: 'চলচ্চিত্রের গান' },
    { dayOfWeek: 0, startHour: 21, endHour: 24, category: 'INSTRUMENTAL', title: 'যন্ত্র সঙ্গীত' },
    // ... repeat for all days
];

// Get current program based on time
export async function getCurrentProgram() {
    const now = new Date();
    const dayOfWeek = now.getDay();
    const currentHour = now.getHours();
    
    // Check for special/override programs first
    const specialProgram = await wixData.query("RadioScheduleOverrides")
        .le("startTime", now)
        .ge("endTime", now)
        .eq("active", true)
        .find();
    
    if (specialProgram.items.length > 0) {
        return specialProgram.items[0];
    }
    
    // Fall back to regular schedule
    const regularProgram = await wixData.query("RadioSchedule")
        .eq("dayOfWeek", dayOfWeek)
        .le("startHour", currentHour)
        .gt("endHour", currentHour)
        .find();
    
    return regularProgram.items.length > 0 ? regularProgram.items[0] : getDefaultProgram(currentHour);
}

// Get playlist for current program
export async function getCurrentPlaylist() {
    const program = await getCurrentProgram();
    
    const playlist = await wixData.query("RadioPlaylists")
        .eq("category", program.category)
        .ascending("order")
        .find();
    
    return {
        program,
        tracks: playlist.items,
        streamUrl: getStreamUrl(program.category)
    };
}

// Admin: Update schedule
export async function updateScheduleSlot(slotId, updateData) {
    return await wixData.update("RadioSchedule", {
        _id: slotId,
        ...updateData
    });
}

// Admin: Add special program (override)
export async function addSpecialProgram(programData) {
    const { title, description, startTime, endTime, streamUrl, category } = programData;
    
    return await wixData.insert("RadioScheduleOverrides", {
        title,
        description,
        startTime: new Date(startTime),
        endTime: new Date(endTime),
        streamUrl,
        category,
        active: true,
        createdAt: new Date()
    });
}

// Admin: Manage playlists
export async function addTrackToPlaylist(trackData) {
    const { title, artist, audioUrl, category, duration } = trackData;
    
    // Get current max order for category
    const existing = await wixData.query("RadioPlaylists")
        .eq("category", category)
        .descending("order")
        .limit(1)
        .find();
    
    const order = existing.items.length > 0 ? existing.items[0].order + 1 : 1;
    
    return await wixData.insert("RadioPlaylists", {
        title,
        artist,
        audioUrl,
        category,
        duration,
        order,
        addedAt: new Date()
    });
}

function getStreamUrl(category) {
    // Map categories to stream sources (could be Icecast, YouTube, etc.)
    const streams = {
        'bengali-songs': 'https://stream.jaxbengali.org/bengali-songs',
        'rabindra-sangeet': 'https://stream.jaxbengali.org/rabindra',
        'modern-bengali': 'https://stream.jaxbengali.org/modern',
        'adhunik-film': 'https://stream.jaxbengali.org/film',
        'instrumental-classical': 'https://stream.jaxbengali.org/instrumental',
        'mixed-playlist': 'https://stream.jaxbengali.org/mixed'
    };
    return streams[category] || streams['mixed-playlist'];
}
```

### 6.3 Radio Player Widget

**RadioPlayer.velo.js**
```javascript
import { getCurrentPlaylist, getCurrentProgram } from 'backend/radio-scheduler.jsw';

let currentTrackIndex = 0;
let audioPlayer;
let isPlaying = false;
let updateInterval;

$w.onReady(async () => {
    await initializeRadio();
    
    // Update "Now Playing" every minute
    updateInterval = setInterval(updateNowPlaying, 60000);
    
    $w('#playPauseBtn').onClick(togglePlayPause);
    $w('#volumeSlider').onChange(adjustVolume);
    $w('#scheduleBtn').onClick(() => $w('#scheduleModal').show());
});

async function initializeRadio() {
    try {
        const { program, tracks, streamUrl } = await getCurrentPlaylist();
        
        // Update UI
        $w('#programTitle').text = program.title;
        $w('#programDescription').text = program.description || '';
        $w('#currentCategory').text = formatCategory(program.category);
        
        // Initialize HTML5 audio (using WixAudio or custom player)
        $w('#audioPlayer').src = streamUrl;
        
        // Load schedule preview
        await loadSchedulePreview();
        
    } catch (error) {
        console.error('Radio init error:', error);
        $w('#radioStatus').text = 'Offline - Check back later';
    }
}

function togglePlayPause() {
    const player = $w('#audioPlayer');
    
    if (isPlaying) {
        player.pause();
        $w('#playPauseBtn').icon = 'play';
        $w('#playPauseBtn').label = 'Play';
    } else {
        player.play();
        $w('#playPauseBtn').icon = 'pause';
        $w('#playPauseBtn').label = 'Pause';
    }
    
    isPlaying = !isPlaying;
}

function adjustVolume(event) {
    const volume = event.target.value / 100;
    $w('#audioPlayer').volume = volume;
}

async function updateNowPlaying() {
    const program = await getCurrentProgram();
    $w('#programTitle').text = program.title;
    $w('#currentCategory').text = formatCategory(program.category);
}

function formatCategory(category) {
    const labels = {
        'bengali-songs': '🎵 Bengali Songs',
        'rabindra-sangeet': '🎼 Rabindra Sangeet',
        'modern-bengali': '🎤 Modern Bengali',
        'adhunik-film': '🎬 Film Songs',
        'instrumental-classical': '🎻 Classical',
        'mixed-playlist': '📻 Mixed',
        'special-program': '⭐ Special',
        'live-event': '🔴 LIVE'
    };
    return labels[category] || '📻 BANF Radio';
}

async function loadSchedulePreview() {
    // Load today's schedule for preview
    const today = new Date().getDay();
    // Populate schedule repeater
}
```

---

## 7. Member Engagement Automation {#member-automation}

### 7.1 Automated Workflows

```javascript
// Wix Automations Triggers & Actions

// TRIGGER: New Member Signs Up
// ACTIONS:
// 1. Send welcome email
// 2. Add to "New Members" list
// 3. Create CRM contact
// 4. Assign welcome tasks to EC

// TRIGGER: Membership Expiring (30 days before)
// ACTIONS:
// 1. Send renewal reminder
// 2. Create renewal task
// 3. If Elite member, personal call reminder

// TRIGGER: Event RSVP
// ACTIONS:
// 1. Confirmation email
// 2. Add to attendee list
// 3. Calendar invite
// 4. Reminder 24h before

// TRIGGER: Payment Received
// ACTIONS:
// 1. Receipt email
// 2. Update membership status
// 3. Thank you notification
// 4. Add to contributor list
```

### 7.2 Member Lifecycle Automation

**member-automation.jsw**
```javascript
import { triggeredEmails } from 'wix-crm-backend';
import wixData from 'wix-data';
import wixCRM from 'wix-crm-backend';

// New member onboarding flow
export async function onboardNewMember(memberId) {
    const member = await wixData.get("Members", memberId);
    
    // Step 1: Welcome Email
    await triggeredEmails.emailMember('welcome-email', memberId, {
        variables: {
            firstName: member.firstName,
            membershipType: member.membershipType,
            memberSince: formatDate(member.joinDate)
        }
    });
    
    // Step 2: Add to new members segment
    await wixCRM.updateContact(memberId, {
        labels: ['New Member', 'Active', member.membershipType]
    });
    
    // Step 3: Schedule 7-day follow-up
    await wixData.insert("ScheduledTasks", {
        memberId,
        taskType: 'follow-up',
        scheduledFor: addDays(new Date(), 7),
        assignedTo: 'general-secretary',
        template: 'welcome-followup',
        completed: false
    });
    
    // Step 4: Send digital member card
    await generateAndSendMemberCard(memberId);
    
    return { success: true };
}

// Membership renewal flow
export async function handleMembershipRenewal(memberId) {
    const member = await wixData.get("Members", memberId);
    const expiryDate = new Date(member.membershipExpiry);
    const daysUntilExpiry = daysBetween(new Date(), expiryDate);
    
    if (daysUntilExpiry <= 30 && !member.renewalReminderSent30) {
        await sendRenewalReminder(memberId, '30-day');
        await wixData.update("Members", { _id: memberId, renewalReminderSent30: true });
    }
    
    if (daysUntilExpiry <= 7 && !member.renewalReminderSent7) {
        await sendRenewalReminder(memberId, '7-day');
        await wixData.update("Members", { _id: memberId, renewalReminderSent7: true });
    }
    
    if (daysUntilExpiry <= 1 && !member.renewalReminderSent1) {
        await sendRenewalReminder(memberId, 'final');
        await wixData.update("Members", { _id: memberId, renewalReminderSent1: true });
    }
}

// Birthday/Anniversary automation
export async function checkBirthdayWishes() {
    const today = new Date();
    const month = today.getMonth() + 1;
    const day = today.getDate();
    
    const birthdayMembers = await wixData.query("Members")
        .eq("birthMonth", month)
        .eq("birthDay", day)
        .find();
    
    for (const member of birthdayMembers.items) {
        await triggeredEmails.emailMember('birthday-wish', member._id, {
            variables: {
                firstName: member.firstName,
                specialOffer: 'Enjoy 10% off on event tickets this month!'
            }
        });
    }
}

// Event engagement tracking
export async function trackMemberEngagement(memberId, eventId, engagementType) {
    await wixData.insert("MemberEngagement", {
        memberId,
        eventId,
        type: engagementType,  // 'rsvp', 'attended', 'volunteered', 'performed'
        timestamp: new Date()
    });
    
    // Update member engagement score
    const engagements = await wixData.query("MemberEngagement")
        .eq("memberId", memberId)
        .count();
    
    await wixData.update("Members", {
        _id: memberId,
        engagementScore: calculateEngagementScore(engagements)
    });
}
```

---

## 8. Payment & Membership Automation {#payment-automation}

### 8.1 Payment Integration

```javascript
// payment-automation.jsw

import wixPaymentBackend from 'wix-payments-backend';
import wixData from 'wix-data';
import { triggeredEmails } from 'wix-crm-backend';

// Handle successful payment
export async function onPaymentComplete(paymentInfo) {
    const { orderId, amount, payerEmail, paymentMethod, items } = paymentInfo;
    
    // Determine payment type
    const paymentType = determinePaymentType(items);
    
    switch (paymentType) {
        case 'membership':
            await processMembershipPayment(paymentInfo);
            break;
        case 'event-ticket':
            await processEventTicketPayment(paymentInfo);
            break;
        case 'donation':
            await processDonation(paymentInfo);
            break;
        case 'sponsorship':
            await processSponsorshipPayment(paymentInfo);
            break;
    }
    
    // Record transaction
    await wixData.insert("Transactions", {
        orderId,
        amount,
        payerEmail,
        paymentMethod,
        type: paymentType,
        items: JSON.stringify(items),
        status: 'completed',
        timestamp: new Date()
    });
    
    // Send receipt
    await sendPaymentReceipt(payerEmail, paymentInfo);
}

async function processMembershipPayment(paymentInfo) {
    const { payerEmail, items } = paymentInfo;
    const membershipItem = items.find(i => i.type === 'membership');
    
    // Find or create member
    let member = await wixData.query("Members")
        .eq("email", payerEmail)
        .find();
    
    if (member.items.length === 0) {
        // New member
        member = await wixData.insert("Members", {
            email: payerEmail,
            membershipType: membershipItem.name,
            membershipStatus: 'active',
            joinDate: new Date(),
            membershipExpiry: addYears(new Date(), 1),
            paymentHistory: [paymentInfo.orderId]
        });
        
        await onboardNewMember(member._id);
    } else {
        // Renewal
        const existingMember = member.items[0];
        const newExpiry = new Date(existingMember.membershipExpiry) > new Date() ?
            addYears(new Date(existingMember.membershipExpiry), 1) :
            addYears(new Date(), 1);
        
        await wixData.update("Members", {
            _id: existingMember._id,
            membershipStatus: 'active',
            membershipExpiry: newExpiry,
            paymentHistory: [...(existingMember.paymentHistory || []), paymentInfo.orderId],
            renewalReminderSent30: false,
            renewalReminderSent7: false,
            renewalReminderSent1: false
        });
    }
}

// Auto-generate 501(c)(3) donation receipt
async function generateTaxReceipt(donorInfo, amount, year) {
    const receiptData = {
        organizationName: 'Bengali Association of North Florida',
        ein: 'XX-XXXXXXX',  // BANF EIN
        donorName: donorInfo.name,
        donorAddress: donorInfo.address,
        donationAmount: amount,
        donationDate: new Date(),
        receiptNumber: `BANF-${year}-${generateReceiptNumber()}`,
        noGoodsOrServices: true,  // For pure donations
        description: 'Charitable contribution to 501(c)(3) organization'
    };
    
    // Store receipt
    await wixData.insert("TaxReceipts", receiptData);
    
    // Send email with PDF attachment
    await sendTaxReceiptEmail(donorInfo.email, receiptData);
    
    return receiptData;
}
```

---

## 9. Event Management System {#event-management}

### 9.1 Automated Event Workflow

```javascript
// event-automation.jsw

import wixData from 'wix-data';
import { triggeredEmails } from 'wix-crm-backend';
import wixEvents from 'wix-events-backend';

// Create event with full automation
export async function createEvent(eventData) {
    const {
        title, description, date, time, venue, capacity,
        ticketTypes, registrationDeadline, category
    } = eventData;
    
    // Create in Wix Events
    const wixEvent = await wixEvents.createEvent({
        title,
        description,
        location: { name: venue },
        scheduling: {
            startDate: combineDateTime(date, time)
        },
        guestLimit: capacity,
        registration: {
            deadline: new Date(registrationDeadline)
        }
    });
    
    // Create in custom events table for extended functionality
    const event = await wixData.insert("Events", {
        wixEventId: wixEvent.id,
        title,
        description,
        date: new Date(date),
        time,
        venue,
        capacity,
        registeredCount: 0,
        ticketTypes: JSON.stringify(ticketTypes),
        registrationDeadline: new Date(registrationDeadline),
        category,
        status: 'upcoming',
        createdAt: new Date(),
        // Automation flags
        reminder7DaysSent: false,
        reminder24HoursSent: false,
        followUpSent: false
    });
    
    // Announce to all members
    await announceEvent(event);
    
    return { success: true, event, wixEventId: wixEvent.id };
}

// Handle RSVP
export async function processRSVP(eventId, memberId, ticketType, guests) {
    // Check capacity
    const event = await wixData.get("Events", eventId);
    if (event.registeredCount >= event.capacity) {
        return { success: false, reason: 'Event is full', waitlist: true };
    }
    
    // Create registration
    const registration = await wixData.insert("EventRegistrations", {
        eventId,
        memberId,
        ticketType,
        guestCount: guests,
        totalAttendees: 1 + guests,
        status: 'confirmed',
        registeredAt: new Date()
    });
    
    // Update event count
    await wixData.update("Events", {
        _id: eventId,
        registeredCount: event.registeredCount + 1 + guests
    });
    
    // Send confirmation
    const member = await wixData.get("Members", memberId);
    await triggeredEmails.emailMember('event-confirmation', memberId, {
        variables: {
            eventTitle: event.title,
            eventDate: formatDate(event.date),
            eventTime: event.time,
            venue: event.venue,
            ticketType,
            guests
        }
    });
    
    // Track engagement
    await trackMemberEngagement(memberId, eventId, 'rsvp');
    
    return { success: true, registration };
}

// Automated event reminders (called by scheduled job)
export async function sendEventReminders() {
    const now = new Date();
    const sevenDaysAhead = addDays(now, 7);
    const oneDayAhead = addDays(now, 1);
    
    // 7-day reminders
    const eventsIn7Days = await wixData.query("Events")
        .ge("date", sevenDaysAhead)
        .lt("date", addDays(sevenDaysAhead, 1))
        .eq("reminder7DaysSent", false)
        .find();
    
    for (const event of eventsIn7Days.items) {
        await sendEventReminder(event, '7-day');
        await wixData.update("Events", { _id: event._id, reminder7DaysSent: true });
    }
    
    // 24-hour reminders
    const eventsIn24Hours = await wixData.query("Events")
        .ge("date", oneDayAhead)
        .lt("date", addDays(oneDayAhead, 1))
        .eq("reminder24HoursSent", false)
        .find();
    
    for (const event of eventsIn24Hours.items) {
        await sendEventReminder(event, '24-hour');
        await wixData.update("Events", { _id: event._id, reminder24HoursSent: true });
    }
}

// Post-event automation
export async function processPostEvent(eventId) {
    const event = await wixData.get("Events", eventId);
    const registrations = await wixData.query("EventRegistrations")
        .eq("eventId", eventId)
        .eq("status", "confirmed")
        .find();
    
    for (const reg of registrations.items) {
        // Send thank you / feedback request
        await triggeredEmails.emailMember('event-feedback', reg.memberId, {
            variables: {
                eventTitle: event.title,
                feedbackLink: `https://www.jaxbengali.org/feedback/${eventId}`
            }
        });
        
        // Update engagement (if they attended)
        if (reg.checkedIn) {
            await trackMemberEngagement(reg.memberId, eventId, 'attended');
        }
    }
    
    // Update event status
    await wixData.update("Events", {
        _id: eventId,
        status: 'completed',
        followUpSent: true,
        completedAt: new Date()
    });
}
```

---

## 10. Vendor & Sponsor Management {#vendor-sponsor}

### 10.1 Vendor Portal

```javascript
// vendor-management.jsw

import wixData from 'wix-data';

// Register vendor
export async function registerVendor(vendorData) {
    const {
        businessName, contactName, email, phone,
        category, services, yearsInBusiness
    } = vendorData;
    
    const vendor = await wixData.insert("Vendors", {
        businessName,
        contactName,
        email,
        phone,
        category,  // 'catering', 'decoration', 'entertainment', 'supplies'
        services: JSON.stringify(services),
        yearsInBusiness,
        status: 'pending',  // pending, approved, rejected, inactive
        rating: 0,
        totalJobs: 0,
        createdAt: new Date()
    });
    
    // Notify admin for review
    await notifyAdminNewVendor(vendor);
    
    return { success: true, vendor };
}

// Get approved vendors by category
export async function getVendorsByCategory(category) {
    return await wixData.query("Vendors")
        .eq("category", category)
        .eq("status", "approved")
        .descending("rating")
        .find();
}

// Submit vendor rating after event
export async function rateVendor(vendorId, eventId, rating, review) {
    // Add review
    await wixData.insert("VendorReviews", {
        vendorId,
        eventId,
        rating,
        review,
        createdAt: new Date()
    });
    
    // Update vendor average rating
    const reviews = await wixData.query("VendorReviews")
        .eq("vendorId", vendorId)
        .find();
    
    const avgRating = reviews.items.reduce((sum, r) => sum + r.rating, 0) / reviews.items.length;
    
    await wixData.update("Vendors", {
        _id: vendorId,
        rating: avgRating,
        totalJobs: reviews.items.length
    });
}
```

### 10.2 Sponsor Management

```javascript
// sponsor-management.jsw

import wixData from 'wix-data';
import { triggeredEmails } from 'wix-crm-backend';

// Sponsorship tiers
const SPONSORSHIP_TIERS = {
    PLATINUM: { amount: 2500, benefits: ['Full-page ad', 'Logo on banners', '10 VIP seats', 'MC acknowledgment'] },
    GOLD: { amount: 1000, benefits: ['Half-page ad', 'Logo on main banner', '6 VIP seats'] },
    SILVER: { amount: 500, benefits: ['Quarter-page ad', 'Banner mention', '4 reserved seats'] },
    BRONZE: { amount: 250, benefits: ['Business card ad', 'Name on banner', '2 seats'] }
};

// Register sponsor
export async function registerSponsor(sponsorData) {
    const {
        businessName, contactName, email, phone,
        tier, paymentMethod, sponsorshipYear
    } = sponsorData;
    
    const tierInfo = SPONSORSHIP_TIERS[tier];
    
    const sponsor = await wixData.insert("Sponsors", {
        businessName,
        contactName,
        email,
        phone,
        tier,
        amount: tierInfo.amount,
        benefits: JSON.stringify(tierInfo.benefits),
        sponsorshipYear,
        paymentStatus: 'pending',
        benefitsDelivered: {},
        createdAt: new Date()
    });
    
    // Send payment instructions
    await triggeredEmails.emailContact(email, 'sponsorship-payment', {
        variables: {
            businessName,
            tier,
            amount: tierInfo.amount,
            paymentLink: 'https://squareup.com/store/bengali-association-of-north-florida'
        }
    });
    
    return { success: true, sponsor };
}

// Track benefit delivery
export async function markBenefitDelivered(sponsorId, benefit) {
    const sponsor = await wixData.get("Sponsors", sponsorId);
    const benefitsDelivered = sponsor.benefitsDelivered || {};
    benefitsDelivered[benefit] = new Date();
    
    await wixData.update("Sponsors", {
        _id: sponsorId,
        benefitsDelivered
    });
    
    // Check if all benefits delivered
    const allBenefits = JSON.parse(sponsor.benefits);
    const allDelivered = allBenefits.every(b => benefitsDelivered[b]);
    
    if (allDelivered) {
        await triggeredEmails.emailContact(sponsor.email, 'sponsorship-complete', {
            variables: { businessName: sponsor.businessName }
        });
    }
}

// Generate sponsor visibility report
export async function getSponsorReport(year) {
    const sponsors = await wixData.query("Sponsors")
        .eq("sponsorshipYear", year)
        .eq("paymentStatus", "completed")
        .find();
    
    const totalRevenue = sponsors.items.reduce((sum, s) => sum + s.amount, 0);
    const byTier = sponsors.items.reduce((acc, s) => {
        acc[s.tier] = (acc[s.tier] || 0) + 1;
        return acc;
    }, {});
    
    return {
        year,
        totalSponsors: sponsors.items.length,
        totalRevenue,
        byTier,
        sponsors: sponsors.items
    };
}
```

---

## 11. Implementation Roadmap {#implementation}

### Phase 1: Foundation (Week 1-2)
- [ ] Set up Wix Studio with Business Elite plan
- [ ] Create CMS collections for all data types
- [ ] Implement admin authentication system
- [ ] Build base admin dashboard

### Phase 2: Member System (Week 3-4)
- [ ] Member registration flow
- [ ] Payment integration
- [ ] Automated email templates
- [ ] Member portal

### Phase 3: Event System (Week 5-6)
- [ ] Event creation workflow
- [ ] RSVP system
- [ ] Ticket management
- [ ] Automated reminders

### Phase 4: Streaming & Radio (Week 7-8)
- [ ] Video streaming console
- [ ] Radio scheduler backend
- [ ] Radio player widget
- [ ] Content management

### Phase 5: Advanced Features (Week 9-10)
- [ ] AI chat assistant
- [ ] Vendor portal
- [ ] Sponsor management
- [ ] Analytics dashboard

### Phase 6: Testing & Launch (Week 11-12)
- [ ] End-to-end testing
- [ ] Member UAT
- [ ] Performance optimization
- [ ] Go-live

---

## 📞 Support & Contact

For implementation assistance:
- **Technical:** tech@jaxbengali.org
- **Admin Questions:** admin@jaxbengali.org
- **General:** info@jaxbengali.org

---

*Document Version: 2.0 | Created for BANF 2025-26 Digital Transformation*
