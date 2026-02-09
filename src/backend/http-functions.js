/**
 * BANF Wix HTTP Functions
 * ========================
 * Public REST API endpoints for the BANF website
 * 
 * These endpoints are accessible at:
 * https://[your-site-url]/_functions/[endpoint_name]
 * 
 * Example: https://banfwix.wixsite.com/banf1/_functions/get_events
 */

import { ok, badRequest, serverError, notFound, forbidden } from 'wix-http-functions';

// ============================================
// BACKEND MODULE IMPORTS
// ============================================
import * as members from 'backend/members.jsw';
import * as memberAuth from 'backend/member-auth.jsw';
import * as events from 'backend/events.jsw';
import * as radio from 'backend/radio.jsw';
import * as sponsors from 'backend/sponsor-management.jsw';
import * as gallery from 'backend/photo-gallery-service.jsw';
import * as surveys from 'backend/surveys.jsw';
import * as complaints from 'backend/complaints.jsw';
import * as guide from 'backend/guide.jsw';
import * as magazine from 'backend/magazine.jsw';
import * as documents from 'backend/documents.jsw';

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Create a successful JSON response
 */
function jsonResponse(data) {
    return ok({
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        body: JSON.stringify(data)
    });
}

/**
 * Create an error response
 */
function errorResponse(message, statusCode = 500) {
    const response = {
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({ success: false, error: message })
    };
    
    if (statusCode === 400) return badRequest(response);
    if (statusCode === 404) return notFound(response);
    if (statusCode === 403) return forbidden(response);
    return serverError(response);
}

/**
 * Parse JSON body from request
 */
async function parseBody(request) {
    try {
        const body = await request.body.text();
        return JSON.parse(body);
    } catch (e) {
        return null;
    }
}

/**
 * Handle OPTIONS requests for CORS preflight
 */
function handleCors() {
    return ok({
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '86400'
        },
        body: ''
    });
}

// ============================================
// HEALTH CHECK ENDPOINT
// ============================================

/**
 * GET /_functions/get_health
 * Health check endpoint
 */
export function get_health(request) {
    return jsonResponse({
        status: 'ok',
        timestamp: new Date().toISOString(),
        service: 'BANF API',
        version: '1.0.0'
    });
}

// ============================================
// MEMBER AUTHENTICATION ENDPOINTS
// ============================================

/**
 * POST /_functions/member_login
 * Member login endpoint
 * Body: { email: string, password: string }
 */
export async function post_member_login(request) {
    try {
        const body = await parseBody(request);
        
        if (!body || !body.email || !body.password) {
            return errorResponse('Email and password are required', 400);
        }
        
        const result = await memberAuth.loginMember(body.email, body.password);
        return jsonResponse({ success: true, ...result });
        
    } catch (error) {
        console.error('Login error:', error);
        return errorResponse(error.message || 'Login failed', 401);
    }
}

/**
 * POST /_functions/member_signup
 * Member registration endpoint
 * Body: { email, password, firstName, lastName, phone, etc. }
 */
export async function post_member_signup(request) {
    try {
        const body = await parseBody(request);
        
        if (!body || !body.email) {
            return errorResponse('Email is required', 400);
        }
        
        const result = await memberAuth.registerMember(body);
        return jsonResponse({ success: true, ...result });
        
    } catch (error) {
        console.error('Signup error:', error);
        return errorResponse(error.message || 'Registration failed', 400);
    }
}

/**
 * POST /_functions/verify_registration_code
 * Verify email registration code
 * Body: { email: string, code: string }
 */
export async function post_verify_registration_code(request) {
    try {
        const body = await parseBody(request);
        
        if (!body || !body.email || !body.code) {
            return errorResponse('Email and verification code are required', 400);
        }
        
        // Verify the code (implement in member-auth.jsw)
        const result = { success: true, message: 'Code verified successfully' };
        return jsonResponse(result);
        
    } catch (error) {
        return errorResponse(error.message || 'Verification failed', 400);
    }
}

/**
 * POST /_functions/complete_registration
 * Complete member registration after verification
 */
export async function post_complete_registration(request) {
    try {
        const body = await parseBody(request);
        
        if (!body || !body.email) {
            return errorResponse('Registration data is required', 400);
        }
        
        const result = { success: true, message: 'Registration completed' };
        return jsonResponse(result);
        
    } catch (error) {
        return errorResponse(error.message || 'Registration completion failed', 400);
    }
}

/**
 * POST /_functions/reset_password
 * Request password reset
 * Body: { email: string }
 */
export async function post_reset_password(request) {
    try {
        const body = await parseBody(request);
        
        if (!body || !body.email) {
            return errorResponse('Email is required', 400);
        }
        
        await memberAuth.requestPasswordReset(body.email);
        return jsonResponse({ 
            success: true, 
            message: 'If an account exists, a reset link has been sent.' 
        });
        
    } catch (error) {
        // Don't reveal whether email exists
        return jsonResponse({ 
            success: true, 
            message: 'If an account exists, a reset link has been sent.' 
        });
    }
}

// ============================================
// MEMBERS ENDPOINTS
// ============================================

/**
 * GET /_functions/get_members
 * Get member count (public)
 */
export async function get_members(request) {
    try {
        const stats = await members.getMembershipStats();
        return jsonResponse({ 
            success: true, 
            count: stats.totalMembers || 0,
            stats: stats
        });
    } catch (error) {
        return errorResponse(error.message);
    }
}

/**
 * GET /_functions/get_member_profile
 * Get member profile (requires memberId query param)
 */
export async function get_member_profile(request) {
    try {
        const memberId = request.query.memberId;
        
        if (!memberId) {
            return errorResponse('Member ID is required', 400);
        }
        
        const profile = await members.getMemberById(memberId);
        
        if (!profile) {
            return errorResponse('Member not found', 404);
        }
        
        return jsonResponse({ success: true, member: profile });
        
    } catch (error) {
        return errorResponse(error.message);
    }
}

// ============================================
// EVENTS ENDPOINTS
// ============================================

/**
 * GET /_functions/get_events
 * Get upcoming events (public)
 */
export async function get_events(request) {
    try {
        const limit = parseInt(request.query?.limit) || 20;
        const eventsData = await events.getUpcomingEvents({ limit });
        return jsonResponse({ 
            success: true, 
            events: eventsData || [],
            count: eventsData?.length || 0
        });
    } catch (error) {
        console.error('Events error:', error);
        return errorResponse(error.message);
    }
}

/**
 * GET /_functions/get_past_events
 * Get past events (public)
 */
export async function get_past_events(request) {
    try {
        const limit = parseInt(request.query?.limit) || 50;
        const skip = parseInt(request.query?.skip) || 0;
        const eventsData = await events.getPastEvents({ limit, skip });
        return jsonResponse({ 
            success: true, 
            events: eventsData || [],
            count: eventsData?.length || 0
        });
    } catch (error) {
        return errorResponse(error.message);
    }
}

/**
 * GET /_functions/get_event
 * Get single event by ID
 */
export async function get_event(request) {
    try {
        const eventId = request.query?.eventId;
        
        if (!eventId) {
            return errorResponse('Event ID is required', 400);
        }
        
        const event = await events.getEventById(eventId);
        
        if (!event) {
            return errorResponse('Event not found', 404);
        }
        
        return jsonResponse({ success: true, event });
        
    } catch (error) {
        return errorResponse(error.message);
    }
}

/**
 * POST /_functions/register_event
 * Register for an event
 */
export async function post_register_event(request) {
    try {
        const body = await parseBody(request);
        
        if (!body || !body.eventId || !body.memberId) {
            return errorResponse('Event ID and Member ID are required', 400);
        }
        
        const result = await events.registerForEvent(
            body.eventId, 
            body.memberId, 
            body.attendees || []
        );
        
        return jsonResponse({ success: true, registration: result });
        
    } catch (error) {
        return errorResponse(error.message, 400);
    }
}

// ============================================
// RADIO ENDPOINTS
// ============================================

/**
 * GET /_functions/get_radio
 * Get radio station configuration and current show
 */
export async function get_radio(request) {
    try {
        const [config, currentShow] = await Promise.all([
            radio.getRadioStationConfig(),
            radio.getCurrentShow().catch(() => null)
        ]);
        
        return jsonResponse({ 
            success: true, 
            config: config,
            currentShow: currentShow,
            isLive: config?.isLive || false
        });
    } catch (error) {
        console.error('Radio error:', error);
        return errorResponse(error.message);
    }
}

/**
 * GET /_functions/get_radio_schedule
 * Get radio schedule
 */
export async function get_radio_schedule(request) {
    try {
        const schedule = await radio.getWeeklySchedule();
        return jsonResponse({ success: true, schedule });
    } catch (error) {
        return errorResponse(error.message);
    }
}

/**
 * POST /_functions/submit_song_request
 * Submit a song request
 */
export async function post_submit_song_request(request) {
    try {
        const body = await parseBody(request);
        
        if (!body || !body.songTitle) {
            return errorResponse('Song title is required', 400);
        }
        
        const result = await radio.submitSongRequest(body);
        return jsonResponse({ success: true, request: result });
        
    } catch (error) {
        return errorResponse(error.message, 400);
    }
}

// ============================================
// SPONSORS ENDPOINTS
// ============================================

/**
 * GET /_functions/get_sponsors
 * Get all active sponsors (public)
 */
export async function get_sponsors(request) {
    try {
        const sponsorsList = await sponsors.getAllSponsors({ status: 'active' });
        const tiers = sponsors.getSponsorshipTiers();
        
        return jsonResponse({ 
            success: true, 
            sponsors: sponsorsList || [],
            tiers: tiers,
            count: sponsorsList?.length || 0
        });
    } catch (error) {
        console.error('Sponsors error:', error);
        return errorResponse(error.message);
    }
}

/**
 * GET /_functions/get_sponsor_tiers
 * Get sponsorship tiers
 */
export async function get_sponsor_tiers(request) {
    try {
        const tiers = sponsors.getSponsorshipTiers();
        return jsonResponse({ success: true, tiers });
    } catch (error) {
        return errorResponse(error.message);
    }
}

/**
 * POST /_functions/submit_sponsor_application
 * Submit sponsorship application
 */
export async function post_submit_sponsor_application(request) {
    try {
        const body = await parseBody(request);
        
        if (!body || !body.companyName || !body.tier) {
            return errorResponse('Company name and tier are required', 400);
        }
        
        const result = await sponsors.submitSponsorApplication(body);
        return jsonResponse({ success: true, application: result });
        
    } catch (error) {
        return errorResponse(error.message, 400);
    }
}

// ============================================
// GALLERY ENDPOINTS
// ============================================

/**
 * GET /_functions/get_gallery
 * Get public photo galleries
 */
export async function get_gallery(request) {
    try {
        const limit = parseInt(request.query?.limit) || 20;
        const galleries = await gallery.getPublicAlbums({ limit });
        
        return jsonResponse({ 
            success: true, 
            galleries: galleries || [],
            count: galleries?.length || 0
        });
    } catch (error) {
        console.error('Gallery error:', error);
        return errorResponse(error.message);
    }
}

/**
 * GET /_functions/get_album_photos
 * Get photos from a specific album
 */
export async function get_album_photos(request) {
    try {
        const albumId = request.query?.albumId;
        
        if (!albumId) {
            return errorResponse('Album ID is required', 400);
        }
        
        const photos = await gallery.getAlbumPhotos(albumId);
        return jsonResponse({ success: true, photos });
        
    } catch (error) {
        return errorResponse(error.message);
    }
}

// ============================================
// SURVEYS ENDPOINTS
// ============================================

/**
 * GET /_functions/get_surveys
 * Get active surveys
 */
export async function get_surveys(request) {
    try {
        const activeSurveys = await surveys.getActiveSurveys();
        return jsonResponse({ 
            success: true, 
            surveys: activeSurveys || [],
            count: activeSurveys?.length || 0
        });
    } catch (error) {
        return errorResponse(error.message);
    }
}

/**
 * GET /_functions/get_survey
 * Get a specific survey
 */
export async function get_survey(request) {
    try {
        const surveyId = request.query?.surveyId;
        
        if (!surveyId) {
            return errorResponse('Survey ID is required', 400);
        }
        
        const survey = await surveys.getSurveyById(surveyId);
        
        if (!survey) {
            return errorResponse('Survey not found', 404);
        }
        
        return jsonResponse({ success: true, survey });
        
    } catch (error) {
        return errorResponse(error.message);
    }
}

/**
 * POST /_functions/submit_survey
 * Submit survey response
 */
export async function post_submit_survey(request) {
    try {
        const body = await parseBody(request);
        
        if (!body || !body.surveyId || !body.responses) {
            return errorResponse('Survey ID and responses are required', 400);
        }
        
        const result = await surveys.submitSurveyResponse(
            body.surveyId, 
            body.responses, 
            body.respondentInfo
        );
        
        return jsonResponse({ success: true, response: result });
        
    } catch (error) {
        return errorResponse(error.message, 400);
    }
}

// ============================================
// COMPLAINTS ENDPOINTS
// ============================================

/**
 * POST /_functions/submit_complaint
 * Submit anonymous complaint
 */
export async function post_submit_complaint(request) {
    try {
        const body = await parseBody(request);
        
        if (!body || !body.category || !body.description) {
            return errorResponse('Category and description are required', 400);
        }
        
        const result = await complaints.submitComplaint(body);
        return jsonResponse({ 
            success: true, 
            complaint: result,
            message: 'Complaint submitted successfully. Save your access code to check status.'
        });
        
    } catch (error) {
        return errorResponse(error.message, 400);
    }
}

/**
 * GET /_functions/check_complaint_status
 * Check complaint status
 */
export async function get_check_complaint_status(request) {
    try {
        const complaintId = request.query?.complaintId;
        const accessCode = request.query?.accessCode;
        
        if (!complaintId || !accessCode) {
            return errorResponse('Complaint ID and access code are required', 400);
        }
        
        const status = await complaints.checkComplaintStatus(complaintId, accessCode);
        return jsonResponse({ success: true, status });
        
    } catch (error) {
        return errorResponse(error.message, 400);
    }
}

/**
 * POST /_functions/complaint_followup
 * Add follow-up to complaint
 */
export async function post_complaint_followup(request) {
    try {
        const body = await parseBody(request);
        
        if (!body || !body.complaintId || !body.accessCode || !body.message) {
            return errorResponse('Complaint ID, access code, and message are required', 400);
        }
        
        const result = await complaints.addComplaintFollowUp(
            body.complaintId, 
            body.accessCode, 
            body.message
        );
        
        return jsonResponse({ success: true, followUp: result });
        
    } catch (error) {
        return errorResponse(error.message, 400);
    }
}

// ============================================
// CONTACT ENDPOINT
// ============================================

/**
 * POST /_functions/submit_contact
 * Submit contact form
 */
export async function post_submit_contact(request) {
    try {
        const body = await parseBody(request);
        
        if (!body || !body.name || !body.email || !body.message) {
            return errorResponse('Name, email, and message are required', 400);
        }
        
        // Store contact submission (implement in a contact.jsw module)
        const result = {
            success: true,
            message: 'Thank you for your message. We will get back to you soon.',
            submittedAt: new Date().toISOString()
        };
        
        return jsonResponse(result);
        
    } catch (error) {
        return errorResponse(error.message, 400);
    }
}

// ============================================
// OPTIONS HANDLERS (CORS)
// ============================================

export function options_member_login(request) { return handleCors(); }
export function options_member_signup(request) { return handleCors(); }
export function options_verify_registration_code(request) { return handleCors(); }
export function options_complete_registration(request) { return handleCors(); }
export function options_reset_password(request) { return handleCors(); }
export function options_register_event(request) { return handleCors(); }
export function options_submit_song_request(request) { return handleCors(); }
export function options_submit_sponsor_application(request) { return handleCors(); }
export function options_submit_survey(request) { return handleCors(); }
export function options_submit_complaint(request) { return handleCors(); }
export function options_complaint_followup(request) { return handleCors(); }
export function options_submit_contact(request) { return handleCors(); }
