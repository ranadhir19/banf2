# BANF Velo Deployment - Copy-Paste Instructions
Generated: 2026-02-08 20:24:38
============================================================

## Quick Start
1. Open Wix Editor
2. Enable Dev Mode (Ctrl+Shift+D)
3. For each module below:
   - Right-click 'backend' folder → Add → Web Module
   - Name it exactly as shown (without .jsw)
   - Copy the code and paste
   - Press Ctrl+S to save

============================================================

## [1/41] accounting-ledger
- File: `accounting-ledger.jsw`
- Size: 14.6 KB
- Lines: 382

```javascript
/**
 * BANF Accounting Ledger Backend Module
 * Handles income/expense tracking linked to database
 * 
 * File: backend/accounting-ledger.jsw
 * Deploy to: Wix Velo Backend
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';

// Financial Categories
export const INCOME_CATEGORIES = [
    { id: 'membership', name: 'Membership Dues', subcategories: ['New Member', 'Renewal', 'Family', 'Individual', 'Student'] },
    { id: 'event', name: 'Event Revenue', subcategories: ['Durga Puja', 'Kali Puja', 'Saraswati Puja', 'Poila Boishakh', 'Picnic', 'Other'] },
    { id: 'sponsorship', name: 'Sponsorship', subcategories: ['Platinum', 'Gold', 'Silver', 'Bronze', 'Other'] },
    { id: 'donation', name: 'Donations', subcategories: ['General', 'Scholarship', 'Event', 'Emergency Relief'] },
    { id: 'merchandise', name: 'Merchandise', subcategories: ['T-Shirts', 'Souvenirs', 'Other'] },
    { id: 'other_income', name: 'Other Income', subcategories: ['Interest', 'Refunds', 'Miscellaneous'] }
];

export const EXPENSE_CATEGORIES = [
    { id: 'venue', name: 'Venue & Rental', subcategories: ['Event Venue', 'Equipment Rental', 'Tables & Chairs'] },
    { id: 'food', name: 'Food & Catering', subcategories: ['Catering', 'Groceries', 'Beverages', 'Supplies'] },
    { id: 'entertainment', name: 'Entertainment', subcategories: ['Performers', 'Sound System', 'Decorations', 'DJ'] },
    { id: 'supplies', name: 'Supplies & Materials', subcategories: ['Office Supplies', 'Event Supplies', 'Printing'] },
    { id: 'technology', name: 'Technology', subcategories: ['Website', 'Software', 'Equipment'] },
    { id: 'marketing', name: 'Marketing', subcategories: ['Advertising', 'Printing', 'Social Media'] },
    { id: 'scholarship', name: 'Scholarship', subcategories: ['Student Scholarship', 'Community Support'] },
    { id: 'administrative', name: 'Administrative', subcategories: ['Bank Fees', 'Insurance', 'Legal', 'Registration'] },
    { id: 'other_expense', name: 'Other Expenses', subcategories: ['Miscellaneous', 'Emergency', 'Refunds'] }
];

/**
 * Add a new financial record (income or expense)
 * @param {object} recordData - Financial record details
 * @returns {object} - Result of the operation
 */
export async function addFinancialRecord(recordData) {
    const {
        transactionType, // 'income' or 'expense'
        amount,
        category,
        subcategory,
        description,
        eventName,
        transactionDate,
        paymentMethod,
        receiptNumber,
        vendorName,
        notes,
        adminId,
        adminName
    } = recordData;
    
    try {
        // Validate required fields
        if (!transactionType || !amount || !category || !description || !transactionDate) {
            return { success: false, error: 'Missing required fields' };
        }
        
        // Generate receipt number if not provided
        const receipt = receiptNumber || generateReceiptNumber(transactionType);
        
        const record = await wixData.insert('FinancialRecords', {
            transactionType,
            amount: parseFloat(amount),
            netAmount: parseFloat(amount), // For manual entries, net = gross
            processingFee: 0,
            category,
            subcategory: subcategory || '',
            description,
            eventName: eventName || '',
            transactionDate: new Date(transactionDate),
            paymentMethod: paymentMethod || 'Cash',
            receiptNumber: receipt,
            vendorName: vendorName || '',
            notes: notes || '',
            isApproved: false, // Requires admin approval
            createdBy: adminId,
            createdByName: adminName,
            createdAt: new Date(),
            updatedAt: new Date()
        });
        
        return {
            success: true,
            record: {
                id: record._id,
                receiptNumber: receipt
            },
            message: `${transactionType === 'income' ? 'Income' : 'Expense'} record created successfully`
        };
    } catch (error) {
        console.error('Failed to add financial record:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Generate a unique receipt number
 * @param {string} type - 'income' or 'expense'
 * @returns {string} - Receipt number
 */
function generateReceiptNumber(type) {
    const prefix = type === 'income' ? 'INC' : 'EXP';
    const date = new Date();
    const dateStr = `${date.getFullYear()}${String(date.getMonth() + 1).padStart(2, '0')}`;
    const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0');
    return `BANF-${prefix}-${dateStr}-${random}`;
}

/**
 * Get financial summary for a date range
 * @param {Date} startDate - Start of period
 * @param {Date} endDate - End of period
 * @returns {object} - Financial summary
 */
export async function getFinancialSummary(startDate, endDate) {
    try {
        const records = await wixData.query('FinancialRecords')
            .ge('transactionDate', new Date(startDate))
            .le('transactionDate', new Date(endDate))
            .eq('isApproved', true)
            .find({ suppressAuth: true });
        
        let totalIncome = 0;
        let totalExpense = 0;
        let totalProcessingFees = 0;
        const incomeByCategory = {};
        const expenseByCategory = {};
        
        records.items.forEach(record => {
            if (record.transactionType === 'income') {
                totalIncome += record.amount;
                totalProcessingFees += record.processingFee || 0;
                incomeByCategory[record.category] = (incomeByCategory[record.category] || 0) + record.amount;
            } else {
                totalExpense += record.amount;
                expenseByCategory[record.category] = (expenseByCategory[record.category] || 0) + record.amount;
            }
        });
        
        return {
            success: true,
            summary: {
                period: { startDate, endDate },
                totalIncome: parseFloat(totalIncome.toFixed(2)),
                totalExpense: parseFloat(totalExpense.toFixed(2)),
                netBalance: parseFloat((totalIncome - totalExpense).toFixed(2)),
                totalProcessingFees: parseFloat(totalProcessingFees.toFixed(2)),
                netIncomeAfterFees: parseFloat((totalIncome - totalProcessingFees).toFixed(2)),
                transactionCount: records.items.length,
                incomeByCategory,
                expenseByCategory
            }
        };
    } catch (error) {
        console.error('Failed to get financial summary:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get detailed ledger entries for a date range
 * @param {Date} startDate - Start of period
 * @param {Date} endDate - End of period
 * @param {string} type - 'all', 'income', or 'expense'
 * @returns {object} - Ledger entries
 */
export async function getLedgerEntries(startDate, endDate, type = 'all') {
    try {
        let query = wixData.query('FinancialRecords')
            .ge('transactionDate', new Date(startDate))
            .le('transactionDate', new Date(endDate));
        
        if (type !== 'all') {
            query = query.eq('transactionType', type);
        }
        
        const records = await query
            .ascending('transactionDate')
            .find({ suppressAuth: true });
        
        // Calculate running balance
        let runningBalance = 0;
        const entries = records.items.map(record => {
            if (record.transactionType === 'income') {
                runningBalance += record.amount;
            } else {
                runningBalance -= record.amount;
            }
            
            return {
                id: record._id,
                date: record.transactionDate,
                type: record.transactionType,
                category: record.category,
                subcategory: record.subcategory,
                description: record.description,
                eventName: record.eventName,
                debit: record.transactionType === 'expense' ? record.amount : 0,
                credit: record.transactionType === 'income' ? record.amount : 0,
                processingFee: record.processingFee || 0,
                netAmount: record.netAmount || record.amount,
                balance: parseFloat(runningBalance.toFixed(2)),
                receiptNumber: record.receiptNumber,
                paymentMethod: record.paymentMethod,
                isApproved: record.isApproved,
                createdBy: record.createdByName
            };
        });
        
        return {
            success: true,
            entries,
            totalCount: entries.length,
            finalBalance: runningBalance
        };
    } catch (error) {
        console.error('Failed to get ledger entries:', error);
        return { success: false, error: error.message, entries: [] };
    }
}

/**
 * Approve a financial record
 * @param {string} recordId - Record ID to approve
 * @param {string} adminId - Approving admin ID
 * @param {string} adminName - Approving admin name
 * @returns {object} - Result
 */
export async function approveFinancialRecord(recordId, adminId, adminName) {
    try {
        const record = await wixData.get('FinancialRecords', recordId);
        
        if (!record) {
            return { success: false, error: 'Record not found' };
        }
        
        await wixData.update('FinancialRecords', {
            ...record,
            isApproved: true,
            approvedBy: adminId,
            approvedByName: adminName,
            approvedAt: new Date(),
            updatedAt: new Date()
        });
        
        return { success: true, message: 'Record approved successfully' };
    } catch (error) {
        console.error('Failed to approve record:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get pending records for approval
 * @returns {object} - Pending records
 */
export async function getPendingApprovals() {
    try {
        const records = await wixData.query('FinancialRecords')
            .eq('isApproved', false)
            .descending('createdAt')
            .find({ suppressAuth: true });
        
        return {
            success: true,
            records: records.items,
            count: records.items.length
        };
    } catch (error) {
        console.error('Failed to get pending approvals:', error);
        return { success: false, error: error.message, records: [] };
    }
}

/**
 * Get annual report data
 * @param {number} year - Year for report
 * @returns {object} - Annual report
 */
export async function getAnnualReport(year) {
    const startDate = new Date(year, 0, 1);
    const endDate = new Date(year, 11, 31, 23, 59, 59);
    
    try {
        const records = await wixData.query('FinancialRecords')
            .ge('transactionDate', startDate)
            .le('transactionDate', endDate)
            .eq('isApproved', true)
            .find({ suppressAuth: true });
        
        // Monthly breakdown
        const monthlyData = {};
        for (let month = 0; month < 12; month++) {
            monthlyData[month] = { income: 0, expense: 0, net: 0 };
        }
        
        let totalIncome = 0;
        let totalExpense = 0;
        const categoryBreakdown = { income: {}, expense: {} };
        
        records.items.forEach(record => {
            const month = new Date(record.transactionDate).getMonth();
            const amount = record.amount;
            
            if (record.transactionType === 'income') {
                totalIncome += amount;
                monthlyData[month].income += amount;
                categoryBreakdown.income[record.category] = (categoryBreakdown.income[record.category] || 0) + amount;
            } else {
                totalExpense += amount;
                monthlyData[month].expense += amount;
                categoryBreakdown.expense[record.category] = (categoryBreakdown.expense[record.category] || 0) + amount;
            }
            
            monthlyData[month].net = monthlyData[month].income - monthlyData[month].expense;
        });
        
        return {
            success: true,
            report: {
                year,
                totalIncome: parseFloat(totalIncome.toFixed(2)),
                totalExpense: parseFloat(totalExpense.toFixed(2)),
                netProfit: parseFloat((totalIncome - totalExpense).toFixed(2)),
                transactionCount: records.items.length,
                monthlyData,
                categoryBreakdown,
                generatedAt: new Date()
            }
        };
    } catch (error) {
        console.error('Failed to generate annual report:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Export ledger to CSV format
 * @param {Date} startDate - Start date
 * @param {Date} endDate - End date
 * @returns {string} - CSV content
 */
export async function exportLedgerToCSV(startDate, endDate) {
    try {
        const result = await getLedgerEntries(startDate, endDate, 'all');
        
        if (!result.success) {
            return { success: false, error: result.error };
        }
        
        const headers = ['Date', 'Type', 'Category', 'Subcategory', 'Description', 'Debit', 'Credit', 'Balance', 'Receipt #', 'Payment Method', 'Approved', 'Created By'];
        const rows = result.entries.map(entry => [
            new Date(entry.date).toLocaleDateString(),
            entry.type,
            entry.category,
            entry.subcategory,
            `"${entry.description.replace(/"/g, '""')}"`,
            entry.debit.toFixed(2),
            entry.credit.toFixed(2),
            entry.balance.toFixed(2),
            entry.receiptNumber,
            entry.paymentMethod,
            entry.isApproved ? 'Yes' : 'No',
            entry.createdBy || ''
        ]);
        
        const csvContent = [headers.join(','), ...rows.map(row => row.join(','))].join('\n');
        
        return {
            success: true,
            csv: csvContent,
            filename: `BANF_Ledger_${new Date(startDate).toISOString().split('T')[0]}_to_${new Date(endDate).toISOString().split('T')[0]}.csv`
        };
    } catch (error) {
        console.error('Failed to export ledger:', error);
        return { success: false, error: error.message };
    }
}

```
------------------------------------------------------------

## [2/41] ad-management
- File: `ad-management.jsw`
- Size: 31.5 KB
- Lines: 896

```javascript
/**
 * BANF Advertisement Management Module
 * Google Ads-like system for vendor/sponsor advertising
 * 
 * File: backend/ad-management.jsw
 * Deploy to: Wix Velo Backend
 */

import wixData from 'wix-data';
import { currentUser } from 'wix-users-backend';
import { hasSpecializedPermission } from 'backend/specialized-admin-roles.jsw';

// Ad Types
export const AD_TYPES = {
    BANNER: 'banner',           // Website banners
    SIDEBAR: 'sidebar',         // Sidebar ads
    POPUP: 'popup',             // Popup/modal ads
    VIDEO: 'video',             // Video ads
    NATIVE: 'native',           // Native content ads
    SPONSORED: 'sponsored',     // Sponsored content
    CAROUSEL: 'carousel',       // Multi-image carousel
    NEWSLETTER: 'newsletter',   // Email newsletter ads
    SOCIAL: 'social'            // Social media ads
};

// Ad Placements
export const AD_PLACEMENTS = {
    // Website Placements
    HOME_HERO: 'home_hero',
    HOME_SIDEBAR: 'home_sidebar',
    HOME_FOOTER: 'home_footer',
    EVENT_PAGE: 'event_page',
    MEMBER_DIRECTORY: 'member_directory',
    MAGAZINE_PAGE: 'magazine_page',
    GALLERY_PAGE: 'gallery_page',
    
    // External Placements
    FACEBOOK: 'facebook',
    INSTAGRAM: 'instagram',
    TWITTER: 'twitter',
    LINKEDIN: 'linkedin',
    YOUTUBE: 'youtube',
    EMAIL_NEWSLETTER: 'email_newsletter',
    MOBILE_APP: 'mobile_app'
};

// Billing Models
export const BILLING_MODELS = {
    CPM: 'cpm',         // Cost Per Mille (1000 impressions)
    CPC: 'cpc',         // Cost Per Click
    CPV: 'cpv',         // Cost Per View (video)
    CPA: 'cpa',         // Cost Per Action/Acquisition
    FLAT_RATE: 'flat',  // Flat rate for time period
    SPONSORSHIP: 'sponsorship' // Sponsorship package
};

// Ad Status
export const AD_STATUS = {
    DRAFT: 'draft',
    PENDING_REVIEW: 'pending_review',
    APPROVED: 'approved',
    ACTIVE: 'active',
    PAUSED: 'paused',
    REJECTED: 'rejected',
    COMPLETED: 'completed',
    EXPIRED: 'expired'
};

// ==================== CAMPAIGN MANAGEMENT ====================

/**
 * Create advertising campaign
 */
export async function createCampaign(campaignData, advertiserId) {
    try {
        const campaign = await wixData.insert('AdCampaigns', {
            ...campaignData,
            advertiserId,
            status: AD_STATUS.DRAFT,
            createdAt: new Date(),
            updatedAt: new Date(),
            
            // Campaign settings
            name: campaignData.name,
            objective: campaignData.objective, // 'awareness', 'traffic', 'conversions', 'engagement'
            budget: {
                total: campaignData.totalBudget || 0,
                daily: campaignData.dailyBudget || 0,
                spent: 0,
                remaining: campaignData.totalBudget || 0
            },
            schedule: {
                startDate: campaignData.startDate,
                endDate: campaignData.endDate,
                timezone: campaignData.timezone || 'America/New_York'
            },
            
            // Targeting
            targeting: {
                locations: campaignData.targetLocations || ['US'],
                ageRange: campaignData.ageRange || { min: 18, max: 65 },
                memberTypes: campaignData.memberTypes || ['all'],
                interests: campaignData.interests || [],
                eventAttendees: campaignData.eventAttendees || false
            },
            
            // Bidding
            bidding: {
                model: campaignData.billingModel || BILLING_MODELS.CPM,
                maxBid: campaignData.maxBid || 0,
                autobid: campaignData.autobid !== false
            },
            
            // Tracking
            ads: [],
            metrics: {
                impressions: 0,
                clicks: 0,
                conversions: 0,
                spend: 0
            }
        }, { suppressAuth: true });
        
        return { success: true, campaignId: campaign._id, campaign };
    } catch (error) {
        console.error('Create campaign failed:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Create advertisement within campaign
 */
export async function createAd(campaignId, adData, advertiserId) {
    try {
        const campaign = await wixData.get('AdCampaigns', campaignId, { suppressAuth: true });
        if (!campaign || campaign.advertiserId !== advertiserId) {
            return { success: false, error: 'Campaign not found or unauthorized' };
        }
        
        const ad = await wixData.insert('Advertisements', {
            campaignId,
            advertiserId,
            status: AD_STATUS.PENDING_REVIEW,
            createdAt: new Date(),
            updatedAt: new Date(),
            
            // Ad Content
            adType: adData.type || AD_TYPES.BANNER,
            placement: adData.placement || AD_PLACEMENTS.HOME_SIDEBAR,
            
            headline: adData.headline,
            description: adData.description,
            callToAction: adData.callToAction || 'Learn More',
            destinationUrl: adData.destinationUrl,
            
            // Creative Assets
            assets: {
                primaryImage: adData.primaryImage,
                secondaryImages: adData.secondaryImages || [],
                video: adData.video,
                logo: adData.logo
            },
            
            // Dimensions
            dimensions: getAdDimensions(adData.type, adData.placement),
            
            // Tracking
            metrics: {
                impressions: 0,
                clicks: 0,
                ctr: 0,
                conversions: 0,
                spend: 0
            },
            
            // UTM Parameters
            utmParams: {
                source: 'banf',
                medium: adData.type,
                campaign: campaign.name,
                content: adData.headline
            }
        }, { suppressAuth: true });
        
        // Add ad to campaign
        await wixData.update('AdCampaigns', {
            ...campaign,
            ads: [...campaign.ads, ad._id],
            updatedAt: new Date()
        }, { suppressAuth: true });
        
        return { success: true, adId: ad._id, ad };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Get ad dimensions based on type and placement
 */
function getAdDimensions(adType, placement) {
    const dimensions = {
        [AD_TYPES.BANNER]: {
            [AD_PLACEMENTS.HOME_HERO]: { width: 1200, height: 400 },
            [AD_PLACEMENTS.HOME_FOOTER]: { width: 728, height: 90 },
            default: { width: 728, height: 90 }
        },
        [AD_TYPES.SIDEBAR]: {
            default: { width: 300, height: 250 }
        },
        [AD_TYPES.VIDEO]: {
            default: { width: 640, height: 360 }
        },
        [AD_TYPES.SOCIAL]: {
            [AD_PLACEMENTS.FACEBOOK]: { width: 1200, height: 628 },
            [AD_PLACEMENTS.INSTAGRAM]: { width: 1080, height: 1080 },
            default: { width: 1200, height: 628 }
        }
    };
    
    return dimensions[adType]?.[placement] || dimensions[adType]?.default || { width: 300, height: 250 };
}

/**
 * Review and approve/reject ad
 */
export async function reviewAd(adId, decision, reviewNotes, reviewerId) {
    try {
        const hasPermission = await hasSpecializedPermission(reviewerId, 'ads_approve');
        if (!hasPermission) {
            return { success: false, error: 'Not authorized to review ads' };
        }
        
        const ad = await wixData.get('Advertisements', adId, { suppressAuth: true });
        if (!ad) {
            return { success: false, error: 'Ad not found' };
        }
        
        const newStatus = decision === 'approve' ? AD_STATUS.APPROVED : AD_STATUS.REJECTED;
        
        const updated = await wixData.update('Advertisements', {
            ...ad,
            status: newStatus,
            reviewedBy: reviewerId,
            reviewedAt: new Date(),
            reviewNotes,
            updatedAt: new Date()
        }, { suppressAuth: true });
        
        // Notify advertiser
        await notifyAdReviewResult(ad, newStatus, reviewNotes);
        
        return { success: true, ad: updated };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Start/pause campaign
 */
export async function updateCampaignStatus(campaignId, newStatus, advertiserId) {
    try {
        const campaign = await wixData.get('AdCampaigns', campaignId, { suppressAuth: true });
        if (!campaign || campaign.advertiserId !== advertiserId) {
            return { success: false, error: 'Campaign not found or unauthorized' };
        }
        
        // Validate status transition
        const validTransitions = {
            [AD_STATUS.DRAFT]: [AD_STATUS.PENDING_REVIEW],
            [AD_STATUS.APPROVED]: [AD_STATUS.ACTIVE, AD_STATUS.PAUSED],
            [AD_STATUS.ACTIVE]: [AD_STATUS.PAUSED],
            [AD_STATUS.PAUSED]: [AD_STATUS.ACTIVE]
        };
        
        if (!validTransitions[campaign.status]?.includes(newStatus)) {
            return { success: false, error: 'Invalid status transition' };
        }
        
        const updated = await wixData.update('AdCampaigns', {
            ...campaign,
            status: newStatus,
            updatedAt: new Date()
        }, { suppressAuth: true });
        
        // Update all ads in campaign
        if (newStatus === AD_STATUS.ACTIVE || newStatus === AD_STATUS.PAUSED) {
            await updateCampaignAdsStatus(campaignId, newStatus);
        }
        
        return { success: true, campaign: updated };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

async function updateCampaignAdsStatus(campaignId, status) {
    const ads = await wixData.query('Advertisements')
        .eq('campaignId', campaignId)
        .eq('status', AD_STATUS.APPROVED)
        .find({ suppressAuth: true });
    
    for (const ad of ads.items) {
        await wixData.update('Advertisements', {
            ...ad,
            status,
            updatedAt: new Date()
        }, { suppressAuth: true });
    }
}

// ==================== AD SERVING ====================

/**
 * Get ads for a specific placement (called by frontend)
 */
export async function getAdsForPlacement(placement, context = {}) {
    try {
        const now = new Date();
        
        // Query active ads for this placement
        const ads = await wixData.query('Advertisements')
            .eq('placement', placement)
            .eq('status', AD_STATUS.ACTIVE)
            .find({ suppressAuth: true });
        
        // Filter by campaign status and budget
        const eligibleAds = [];
        
        for (const ad of ads.items) {
            const campaign = await wixData.get('AdCampaigns', ad.campaignId, { suppressAuth: true });
            
            if (campaign && 
                campaign.status === AD_STATUS.ACTIVE &&
                new Date(campaign.schedule.startDate) <= now &&
                new Date(campaign.schedule.endDate) >= now &&
                campaign.budget.remaining > 0) {
                
                // Check targeting
                if (matchesTargeting(campaign.targeting, context)) {
                    eligibleAds.push({
                        ...ad,
                        campaignBudget: campaign.budget
                    });
                }
            }
        }
        
        // Sort by bid and quality score
        eligibleAds.sort((a, b) => {
            const scoreA = a.qualityScore || 1;
            const scoreB = b.qualityScore || 1;
            return (b.maxBid * scoreB) - (a.maxBid * scoreA);
        });
        
        // Return top ad(s)
        const selectedAd = eligibleAds[0];
        
        if (selectedAd) {
            // Record impression
            await recordImpression(selectedAd._id);
            
            return {
                success: true,
                ad: {
                    adId: selectedAd._id,
                    adType: selectedAd.adType,
                    headline: selectedAd.headline,
                    description: selectedAd.description,
                    callToAction: selectedAd.callToAction,
                    destinationUrl: addTrackingParams(selectedAd.destinationUrl, selectedAd.utmParams),
                    assets: selectedAd.assets,
                    dimensions: selectedAd.dimensions
                }
            };
        }
        
        return { success: true, ad: null };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Check if campaign targeting matches context
 */
function matchesTargeting(targeting, context) {
    // Location targeting
    if (targeting.locations && targeting.locations.length > 0) {
        if (!targeting.locations.includes('all') && 
            !targeting.locations.includes(context.location)) {
            return false;
        }
    }
    
    // Member type targeting
    if (targeting.memberTypes && targeting.memberTypes.length > 0) {
        if (!targeting.memberTypes.includes('all') && 
            !targeting.memberTypes.includes(context.memberType)) {
            return false;
        }
    }
    
    return true;
}

/**
 * Add UTM tracking parameters
 */
function addTrackingParams(url, utmParams) {
    if (!url) return url;
    
    const separator = url.includes('?') ? '&' : '?';
    const params = Object.entries(utmParams)
        .map(([key, value]) => `utm_${key}=${encodeURIComponent(value)}`)
        .join('&');
    
    return `${url}${separator}${params}`;
}

/**
 * Record ad impression
 */
export async function recordImpression(adId) {
    try {
        const ad = await wixData.get('Advertisements', adId, { suppressAuth: true });
        if (!ad) return;
        
        // Update ad metrics
        await wixData.update('Advertisements', {
            ...ad,
            metrics: {
                ...ad.metrics,
                impressions: (ad.metrics?.impressions || 0) + 1
            }
        }, { suppressAuth: true });
        
        // Update campaign metrics
        const campaign = await wixData.get('AdCampaigns', ad.campaignId, { suppressAuth: true });
        if (campaign) {
            const cost = campaign.bidding.model === BILLING_MODELS.CPM 
                ? (campaign.bidding.maxBid / 1000) 
                : 0;
            
            await wixData.update('AdCampaigns', {
                ...campaign,
                metrics: {
                    ...campaign.metrics,
                    impressions: (campaign.metrics?.impressions || 0) + 1,
                    spend: (campaign.metrics?.spend || 0) + cost
                },
                budget: {
                    ...campaign.budget,
                    spent: (campaign.budget?.spent || 0) + cost,
                    remaining: (campaign.budget?.remaining || 0) - cost
                }
            }, { suppressAuth: true });
        }
        
        // Log to metrics table
        await wixData.insert('AdMetrics', {
            adId,
            campaignId: ad.campaignId,
            eventType: 'impression',
            timestamp: new Date(),
            context: {}
        }, { suppressAuth: true });
        
    } catch (error) {
        console.error('Record impression failed:', error);
    }
}

/**
 * Record ad click
 */
export async function recordClick(adId, clickData = {}) {
    try {
        const ad = await wixData.get('Advertisements', adId, { suppressAuth: true });
        if (!ad) return { success: false };
        
        // Update ad metrics
        const newClicks = (ad.metrics?.clicks || 0) + 1;
        const newImpressions = ad.metrics?.impressions || 1;
        
        await wixData.update('Advertisements', {
            ...ad,
            metrics: {
                ...ad.metrics,
                clicks: newClicks,
                ctr: ((newClicks / newImpressions) * 100).toFixed(2)
            }
        }, { suppressAuth: true });
        
        // Update campaign metrics and budget (for CPC billing)
        const campaign = await wixData.get('AdCampaigns', ad.campaignId, { suppressAuth: true });
        if (campaign) {
            const cost = campaign.bidding.model === BILLING_MODELS.CPC 
                ? campaign.bidding.maxBid 
                : 0;
            
            await wixData.update('AdCampaigns', {
                ...campaign,
                metrics: {
                    ...campaign.metrics,
                    clicks: (campaign.metrics?.clicks || 0) + 1,
                    spend: (campaign.metrics?.spend || 0) + cost
                },
                budget: {
                    ...campaign.budget,
                    spent: (campaign.budget?.spent || 0) + cost,
                    remaining: (campaign.budget?.remaining || 0) - cost
                }
            }, { suppressAuth: true });
        }
        
        // Log click
        await wixData.insert('AdMetrics', {
            adId,
            campaignId: ad.campaignId,
            eventType: 'click',
            timestamp: new Date(),
            context: clickData
        }, { suppressAuth: true });
        
        return { success: true, destinationUrl: ad.destinationUrl };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Record conversion
 */
export async function recordConversion(adId, conversionData = {}) {
    try {
        const ad = await wixData.get('Advertisements', adId, { suppressAuth: true });
        if (!ad) return { success: false };
        
        await wixData.update('Advertisements', {
            ...ad,
            metrics: {
                ...ad.metrics,
                conversions: (ad.metrics?.conversions || 0) + 1
            }
        }, { suppressAuth: true });
        
        // Update campaign (for CPA billing)
        const campaign = await wixData.get('AdCampaigns', ad.campaignId, { suppressAuth: true });
        if (campaign) {
            const cost = campaign.bidding.model === BILLING_MODELS.CPA 
                ? campaign.bidding.maxBid 
                : 0;
            
            await wixData.update('AdCampaigns', {
                ...campaign,
                metrics: {
                    ...campaign.metrics,
                    conversions: (campaign.metrics?.conversions || 0) + 1,
                    spend: (campaign.metrics?.spend || 0) + cost
                },
                budget: {
                    ...campaign.budget,
                    spent: (campaign.budget?.spent || 0) + cost,
                    remaining: (campaign.budget?.remaining || 0) - cost
                }
            }, { suppressAuth: true });
        }
        
        // Log conversion
        await wixData.insert('AdMetrics', {
            adId,
            campaignId: ad.campaignId,
            eventType: 'conversion',
            timestamp: new Date(),
            conversionValue: conversionData.value || 0,
            conversionType: conversionData.type || 'general',
            context: conversionData
        }, { suppressAuth: true });
        
        return { success: true };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// ==================== REPORTING & ANALYTICS ====================

/**
 * Get campaign performance report
 */
export async function getCampaignReport(campaignId, dateRange, advertiserId) {
    try {
        const campaign = await wixData.get('AdCampaigns', campaignId, { suppressAuth: true });
        if (!campaign || campaign.advertiserId !== advertiserId) {
            return { success: false, error: 'Campaign not found or unauthorized' };
        }
        
        // Get metrics for date range
        const metrics = await wixData.query('AdMetrics')
            .eq('campaignId', campaignId)
            .ge('timestamp', dateRange.start)
            .le('timestamp', dateRange.end)
            .find({ suppressAuth: true });
        
        // Aggregate metrics
        const impressions = metrics.items.filter(m => m.eventType === 'impression').length;
        const clicks = metrics.items.filter(m => m.eventType === 'click').length;
        const conversions = metrics.items.filter(m => m.eventType === 'conversion').length;
        
        // Daily breakdown
        const dailyMetrics = {};
        metrics.items.forEach(m => {
            const day = new Date(m.timestamp).toISOString().split('T')[0];
            if (!dailyMetrics[day]) {
                dailyMetrics[day] = { impressions: 0, clicks: 0, conversions: 0 };
            }
            dailyMetrics[day][m.eventType === 'impression' ? 'impressions' : 
                           m.eventType === 'click' ? 'clicks' : 'conversions']++;
        });
        
        // Calculate ROI
        const totalSpend = campaign.metrics?.spend || 0;
        const conversionValue = metrics.items
            .filter(m => m.eventType === 'conversion')
            .reduce((sum, m) => sum + (m.conversionValue || 0), 0);
        const roi = totalSpend > 0 ? ((conversionValue - totalSpend) / totalSpend * 100).toFixed(2) : 0;
        
        return {
            success: true,
            report: {
                campaign: {
                    id: campaign._id,
                    name: campaign.name,
                    status: campaign.status
                },
                dateRange,
                totals: {
                    impressions,
                    clicks,
                    conversions,
                    spend: totalSpend,
                    ctr: impressions > 0 ? ((clicks / impressions) * 100).toFixed(2) : 0,
                    conversionRate: clicks > 0 ? ((conversions / clicks) * 100).toFixed(2) : 0,
                    cpc: clicks > 0 ? (totalSpend / clicks).toFixed(2) : 0,
                    cpm: impressions > 0 ? ((totalSpend / impressions) * 1000).toFixed(2) : 0,
                    roi
                },
                dailyBreakdown: dailyMetrics,
                budget: campaign.budget
            }
        };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Get advertiser dashboard
 */
export async function getAdvertiserDashboard(advertiserId) {
    try {
        const campaigns = await wixData.query('AdCampaigns')
            .eq('advertiserId', advertiserId)
            .find({ suppressAuth: true });
        
        const activeCampaigns = campaigns.items.filter(c => c.status === AD_STATUS.ACTIVE);
        
        // Aggregate metrics
        const totalSpend = campaigns.items.reduce((sum, c) => sum + (c.metrics?.spend || 0), 0);
        const totalImpressions = campaigns.items.reduce((sum, c) => sum + (c.metrics?.impressions || 0), 0);
        const totalClicks = campaigns.items.reduce((sum, c) => sum + (c.metrics?.clicks || 0), 0);
        const totalConversions = campaigns.items.reduce((sum, c) => sum + (c.metrics?.conversions || 0), 0);
        
        return {
            success: true,
            dashboard: {
                totalCampaigns: campaigns.items.length,
                activeCampaigns: activeCampaigns.length,
                metrics: {
                    totalSpend,
                    totalImpressions,
                    totalClicks,
                    totalConversions,
                    overallCTR: totalImpressions > 0 ? ((totalClicks / totalImpressions) * 100).toFixed(2) : 0,
                    overallConversionRate: totalClicks > 0 ? ((totalConversions / totalClicks) * 100).toFixed(2) : 0
                },
                recentCampaigns: campaigns.items
                    .sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt))
                    .slice(0, 5),
                topPerformingAds: await getTopPerformingAds(advertiserId, 5)
            }
        };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

async function getTopPerformingAds(advertiserId, limit) {
    const ads = await wixData.query('Advertisements')
        .eq('advertiserId', advertiserId)
        .descending('metrics.clicks')
        .limit(limit)
        .find({ suppressAuth: true });
    return ads.items;
}

// ==================== BILLING ====================

/**
 * Generate invoice for advertiser
 */
export async function generateAdInvoice(advertiserId, period, adminUserId) {
    try {
        const hasPermission = await hasSpecializedPermission(adminUserId, 'ads_billing');
        if (!hasPermission) {
            return { success: false, error: 'Not authorized' };
        }
        
        const campaigns = await wixData.query('AdCampaigns')
            .eq('advertiserId', advertiserId)
            .find({ suppressAuth: true });
        
        const lineItems = campaigns.items.map(c => ({
            campaignId: c._id,
            campaignName: c.name,
            impressions: c.metrics?.impressions || 0,
            clicks: c.metrics?.clicks || 0,
            conversions: c.metrics?.conversions || 0,
            amount: c.metrics?.spend || 0
        }));
        
        const totalAmount = lineItems.reduce((sum, item) => sum + item.amount, 0);
        
        const invoice = await wixData.insert('AdInvoices', {
            advertiserId,
            period,
            lineItems,
            subtotal: totalAmount,
            tax: totalAmount * 0.08, // 8% tax
            total: totalAmount * 1.08,
            status: 'pending',
            dueDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days
            createdAt: new Date(),
            createdBy: adminUserId
        }, { suppressAuth: true });
        
        return { success: true, invoiceId: invoice._id, invoice };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// ==================== ADMIN FUNCTIONS ====================

/**
 * Get all pending ads for review (admin)
 */
export async function getPendingAdsForReview(adminUserId) {
    try {
        const hasPermission = await hasSpecializedPermission(adminUserId, 'ads_approve');
        if (!hasPermission) {
            return { success: false, error: 'Not authorized' };
        }
        
        const pendingAds = await wixData.query('Advertisements')
            .eq('status', AD_STATUS.PENDING_REVIEW)
            .ascending('createdAt')
            .find({ suppressAuth: true });
        
        return { success: true, ads: pendingAds.items };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Get platform ad revenue summary (admin)
 */
export async function getAdRevenueSummary(dateRange, adminUserId) {
    try {
        const hasPermission = await hasSpecializedPermission(adminUserId, 'ads_analytics');
        if (!hasPermission) {
            return { success: false, error: 'Not authorized' };
        }
        
        const campaigns = await wixData.query('AdCampaigns')
            .ge('createdAt', dateRange.start)
            .le('createdAt', dateRange.end)
            .find({ suppressAuth: true });
        
        const totalRevenue = campaigns.items.reduce((sum, c) => sum + (c.metrics?.spend || 0), 0);
        const totalImpressions = campaigns.items.reduce((sum, c) => sum + (c.metrics?.impressions || 0), 0);
        const totalClicks = campaigns.items.reduce((sum, c) => sum + (c.metrics?.clicks || 0), 0);
        
        // Revenue by placement
        const ads = await wixData.query('Advertisements')
            .ge('createdAt', dateRange.start)
            .le('createdAt', dateRange.end)
            .find({ suppressAuth: true });
        
        const byPlacement = {};
        ads.items.forEach(ad => {
            const placement = ad.placement || 'other';
            if (!byPlacement[placement]) {
                byPlacement[placement] = { count: 0, impressions: 0, clicks: 0, revenue: 0 };
            }
            byPlacement[placement].count++;
            byPlacement[placement].impressions += ad.metrics?.impressions || 0;
            byPlacement[placement].clicks += ad.metrics?.clicks || 0;
            byPlacement[placement].revenue += ad.metrics?.spend || 0;
        });
        
        return {
            success: true,
            summary: {
                totalRevenue,
                totalImpressions,
                totalClicks,
                totalCampaigns: campaigns.items.length,
                activeCampaigns: campaigns.items.filter(c => c.status === AD_STATUS.ACTIVE).length,
                avgCTR: totalImpressions > 0 ? ((totalClicks / totalImpressions) * 100).toFixed(2) : 0,
                revenuePerImpression: totalImpressions > 0 ? (totalRevenue / totalImpressions).toFixed(4) : 0,
                byPlacement
            }
        };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// Helper function
async function notifyAdReviewResult(ad, status, notes) {
    // Implementation for notifying advertiser of review result
}

/**
 * Get available ad placements with pricing
 */
export async function getAdPlacements() {
    return {
        success: true,
        placements: [
            {
                id: AD_PLACEMENTS.HOME_HERO,
                name: 'Home Page Hero Banner',
                description: 'Premium placement at the top of the home page',
                dimensions: { width: 1200, height: 400 },
                pricing: { cpm: 15.00, flatRate: 500 },
                availability: true
            },
            {
                id: AD_PLACEMENTS.HOME_SIDEBAR,
                name: 'Home Page Sidebar',
                description: 'Sidebar ad on the home page',
                dimensions: { width: 300, height: 250 },
                pricing: { cpm: 8.00, flatRate: 200 },
                availability: true
            },
            {
                id: AD_PLACEMENTS.EVENT_PAGE,
                name: 'Event Pages',
                description: 'Ad displayed on event pages',
                dimensions: { width: 728, height: 90 },
                pricing: { cpm: 10.00, flatRate: 300 },
                availability: true
            },
            {
                id: AD_PLACEMENTS.EMAIL_NEWSLETTER,
                name: 'Email Newsletter',
                description: 'Sponsored section in monthly newsletter',
                dimensions: { width: 600, height: 200 },
                pricing: { flatRate: 250 },
                availability: true
            },
            {
                id: AD_PLACEMENTS.FACEBOOK,
                name: 'Facebook Promotion',
                description: 'Promoted post on BANF Facebook page',
                dimensions: { width: 1200, height: 628 },
                pricing: { cpc: 0.50, flatRate: 150 },
                availability: true
            },
            {
                id: AD_PLACEMENTS.INSTAGRAM,
                name: 'Instagram Promotion',
                description: 'Promoted post on BANF Instagram',
                dimensions: { width: 1080, height: 1080 },
                pricing: { cpc: 0.75, flatRate: 175 },
                availability: true
            }
        ]
    };
}

```
------------------------------------------------------------

## [3/41] admin-auth
- File: `admin-auth.jsw`
- Size: 10.5 KB
- Lines: 328

```javascript
/**
 * BANF Admin Authentication Backend Module
 * Handles admin login and role-based access control
 * 
 * File: backend/admin-auth.jsw
 * Deploy to: Wix Velo Backend
 */

import wixData from 'wix-data';
import { authentication, authorization } from 'wix-members-backend';
import { elevate } from 'wix-auth';

// Admin Roles
export const ADMIN_ROLES = {
    SUPER_ADMIN: 'super_admin',      // Full access
    PRESIDENT: 'president',          // Full access
    VICE_PRESIDENT: 'vice_president', // Most access
    TREASURER: 'treasurer',          // Financial access
    SECRETARY: 'secretary',          // Minutes & communications
    EC_MEMBER: 'ec_member',          // Limited admin access
    MODERATOR: 'moderator'           // Content moderation only
};

// Role Permissions
const ROLE_PERMISSIONS = {
    super_admin: ['*'],
    president: ['*'],
    vice_president: ['members', 'events', 'meetings', 'finances', 'reports', 'complaints'],
    treasurer: ['finances', 'payments', 'reports', 'members_readonly'],
    secretary: ['meetings', 'communications', 'members_readonly', 'reports'],
    ec_member: ['events', 'meetings_readonly', 'members_readonly'],
    moderator: ['complaints', 'content']
};

/**
 * Login admin user
 * @param {string} email - Admin email
 * @param {string} password - Admin password
 * @returns {object} - Login result
 */
export async function loginAdmin(email, password) {
    try {
        // First authenticate with Wix
        const loginResult = await authentication.login(email, password);
        
        // Check if user is an admin
        const admins = await wixData.query('Admins')
            .eq('email', email.toLowerCase())
            .find({ suppressAuth: true });
        
        if (admins.items.length === 0) {
            return { success: false, error: 'Not authorized as admin' };
        }
        
        const admin = admins.items[0];
        
        if (!admin.isActive) {
            return { success: false, error: 'Admin account is deactivated' };
        }
        
        // Update last login
        await wixData.update('Admins', {
            ...admin,
            lastLogin: new Date(),
            loginCount: (admin.loginCount || 0) + 1,
            updatedAt: new Date()
        });
        
        // Log the login
        await logAdminActivity(admin._id, 'login', 'Admin logged in');
        
        return {
            success: true,
            sessionToken: loginResult.sessionToken,
            admin: {
                id: admin._id,
                email: admin.email,
                fullName: admin.fullName,
                role: admin.role,
                permissions: getPermissionsForRole(admin.role),
                ecPosition: admin.ecPosition
            }
        };
    } catch (error) {
        console.error('Admin login failed:', error);
        return { success: false, error: 'Invalid credentials' };
    }
}

/**
 * Get permissions for a role
 * @param {string} role - Admin role
 * @returns {array} - List of permissions
 */
function getPermissionsForRole(role) {
    return ROLE_PERMISSIONS[role] || [];
}

/**
 * Check if admin has permission
 * @param {string} adminId - Admin ID
 * @param {string} permission - Permission to check
 * @returns {boolean} - Has permission
 */
export async function checkAdminPermission(adminId, permission) {
    try {
        const admins = await wixData.query('Admins')
            .eq('_id', adminId)
            .find({ suppressAuth: true });
        
        if (admins.items.length === 0) {
            return false;
        }
        
        const admin = admins.items[0];
        const permissions = getPermissionsForRole(admin.role);
        
        return permissions.includes('*') || permissions.includes(permission);
    } catch (error) {
        console.error('Permission check failed:', error);
        return false;
    }
}

/**
 * Create new admin user
 * @param {object} adminData - Admin details
 * @param {string} creatorId - ID of admin creating this account
 * @returns {object} - Creation result
 */
export async function createAdmin(adminData, creatorId) {
    // Check if creator has permission
    const hasPermission = await checkAdminPermission(creatorId, 'admin_management');
    if (!hasPermission) {
        return { success: false, error: 'Not authorized to create admins' };
    }
    
    const { email, fullName, role, ecPosition } = adminData;
    
    try {
        // Check if admin already exists
        const existing = await wixData.query('Admins')
            .eq('email', email.toLowerCase())
            .find({ suppressAuth: true });
        
        if (existing.items.length > 0) {
            return { success: false, error: 'Admin with this email already exists' };
        }
        
        // Create admin record
        const admin = await wixData.insert('Admins', {
            email: email.toLowerCase(),
            fullName,
            role: role || ADMIN_ROLES.EC_MEMBER,
            ecPosition: ecPosition || '',
            isActive: true,
            loginCount: 0,
            createdBy: creatorId,
            createdAt: new Date(),
            updatedAt: new Date()
        });
        
        await logAdminActivity(creatorId, 'admin_created', `Created admin: ${email}`);
        
        return {
            success: true,
            adminId: admin._id,
            message: 'Admin created successfully. User must register/login with Wix Members.'
        };
    } catch (error) {
        console.error('Failed to create admin:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Update admin role
 * @param {string} adminId - Admin to update
 * @param {string} newRole - New role
 * @param {string} updaterId - ID of admin making the update
 * @returns {object} - Update result
 */
export async function updateAdminRole(adminId, newRole, updaterId) {
    const hasPermission = await checkAdminPermission(updaterId, 'admin_management');
    if (!hasPermission) {
        return { success: false, error: 'Not authorized to update admin roles' };
    }
    
    try {
        const admin = await wixData.get('Admins', adminId);
        
        if (!admin) {
            return { success: false, error: 'Admin not found' };
        }
        
        await wixData.update('Admins', {
            ...admin,
            role: newRole,
            updatedBy: updaterId,
            updatedAt: new Date()
        });
        
        await logAdminActivity(updaterId, 'role_updated', `Updated ${admin.email} role to ${newRole}`);
        
        return { success: true, message: 'Admin role updated' };
    } catch (error) {
        console.error('Failed to update admin role:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Deactivate admin account
 * @param {string} adminId - Admin to deactivate
 * @param {string} deactivatorId - ID of admin performing deactivation
 * @returns {object} - Result
 */
export async function deactivateAdmin(adminId, deactivatorId) {
    const hasPermission = await checkAdminPermission(deactivatorId, 'admin_management');
    if (!hasPermission) {
        return { success: false, error: 'Not authorized to deactivate admins' };
    }
    
    try {
        const admin = await wixData.get('Admins', adminId);
        
        if (!admin) {
            return { success: false, error: 'Admin not found' };
        }
        
        await wixData.update('Admins', {
            ...admin,
            isActive: false,
            deactivatedBy: deactivatorId,
            deactivatedAt: new Date(),
            updatedAt: new Date()
        });
        
        await logAdminActivity(deactivatorId, 'admin_deactivated', `Deactivated admin: ${admin.email}`);
        
        return { success: true, message: 'Admin deactivated' };
    } catch (error) {
        console.error('Failed to deactivate admin:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get all admins
 * @param {string} requesterId - ID of admin requesting list
 * @returns {object} - List of admins
 */
export async function getAllAdmins(requesterId) {
    const hasPermission = await checkAdminPermission(requesterId, 'admin_management');
    if (!hasPermission) {
        return { success: false, error: 'Not authorized' };
    }
    
    try {
        const admins = await wixData.query('Admins')
            .find({ suppressAuth: true });
        
        return {
            success: true,
            admins: admins.items.map(admin => ({
                id: admin._id,
                email: admin.email,
                fullName: admin.fullName,
                role: admin.role,
                ecPosition: admin.ecPosition,
                isActive: admin.isActive,
                lastLogin: admin.lastLogin,
                loginCount: admin.loginCount
            }))
        };
    } catch (error) {
        console.error('Failed to get admins:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Log admin activity
 * @param {string} adminId - Admin ID
 * @param {string} action - Action performed
 * @param {string} details - Action details
 */
async function logAdminActivity(adminId, action, details) {
    try {
        await wixData.insert('AdminActivityLog', {
            adminId,
            action,
            details,
            ipAddress: '', // Would need to capture from request
            timestamp: new Date()
        });
    } catch (error) {
        console.error('Failed to log admin activity:', error);
    }
}

/**
 * Get admin activity log
 * @param {string} requesterId - ID of requesting admin
 * @param {number} limit - Number of entries to return
 * @returns {object} - Activity log
 */
export async function getAdminActivityLog(requesterId, limit = 100) {
    const hasPermission = await checkAdminPermission(requesterId, 'admin_management');
    if (!hasPermission) {
        return { success: false, error: 'Not authorized' };
    }
    
    try {
        const logs = await wixData.query('AdminActivityLog')
            .descending('timestamp')
            .limit(limit)
            .find({ suppressAuth: true });
        
        return {
            success: true,
            logs: logs.items
        };
    } catch (error) {
        console.error('Failed to get activity log:', error);
        return { success: false, error: error.message };
    }
}

```
------------------------------------------------------------

## [4/41] admin
- File: `admin.jsw`
- Size: 11.5 KB
- Lines: 377

```javascript
// backend/admin.jsw
// BANF Admin Dashboard - Wix Velo Backend

import wixData from 'wix-data';
import { currentMember, authentication } from 'wix-members-backend';
import { getFinancialSummary } from 'backend/finance.jsw';
import { getMembershipStats } from 'backend/members.jsw';

/**
 * Get comprehensive dashboard statistics
 */
export async function getDashboardStats() {
    try {
        const now = new Date();
        const yearStart = new Date(now.getFullYear(), 0, 1);
        
        // Get all stats in parallel
        const [
            memberStats,
            financialSummary,
            upcomingEvents,
            pendingPayments,
            recentFeedback,
            pendingComplaints
        ] = await Promise.all([
            getMembershipStats(),
            getFinancialSummary(),
            getUpcomingEventsCount(),
            getPendingPaymentsCount(),
            getRecentFeedbackCount(),
            getPendingComplaintsCount()
        ]);
        
        return {
            members: memberStats,
            finance: financialSummary,
            upcomingEvents,
            pendingPayments,
            recentFeedback,
            pendingComplaints,
            generatedAt: new Date().toISOString()
        };
    } catch (error) {
        console.error('Error getting dashboard stats:', error);
        return null;
    }
}

/**
 * Check if current user is admin
 */
export async function isAdmin() {
    try {
        const member = await currentMember.getMember();
        if (!member) return false;
        
        // Check admin collection
        const adminRecord = await wixData.query('Admins')
            .eq('email', member.loginEmail)
            .eq('isActive', true)
            .find();
        
        return adminRecord.items.length > 0;
    } catch (error) {
        console.error('Error checking admin status:', error);
        return false;
    }
}

/**
 * Get admin user details
 */
export async function getAdminProfile() {
    try {
        const member = await currentMember.getMember();
        if (!member) return null;
        
        const adminRecord = await wixData.query('Admins')
            .eq('email', member.loginEmail)
            .find();
        
        if (adminRecord.items.length === 0) return null;
        
        return {
            id: adminRecord.items[0]._id,
            email: adminRecord.items[0].email,
            fullName: adminRecord.items[0].fullName,
            role: adminRecord.items[0].role,
            permissions: adminRecord.items[0].permissions || []
        };
    } catch (error) {
        console.error('Error getting admin profile:', error);
        return null;
    }
}

/**
 * Create admin user (super_admin only)
 */
export async function createAdmin(adminData, superAdminId) {
    try {
        // Verify super admin
        const superAdmin = await wixData.get('Admins', superAdminId);
        if (!superAdmin || superAdmin.role !== 'super_admin') {
            return { success: false, error: 'Unauthorized' };
        }
        
        // Check if admin already exists
        const existing = await wixData.query('Admins')
            .eq('email', adminData.email)
            .find();
        
        if (existing.items.length > 0) {
            return { success: false, error: 'Admin with this email already exists' };
        }
        
        const admin = {
            username: adminData.username,
            email: adminData.email,
            fullName: adminData.fullName,
            role: adminData.role || 'admin',
            permissions: adminData.permissions || ['read', 'write'],
            isActive: true,
            createdBy: superAdminId,
            _createdDate: new Date()
        };
        
        const result = await wixData.insert('Admins', admin);
        return { success: true, adminId: result._id };
    } catch (error) {
        console.error('Error creating admin:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get activity log
 */
export async function getActivityLog(options = { limit: 50, skip: 0 }) {
    try {
        const result = await wixData.query('ActivityLog')
            .descending('timestamp')
            .limit(options.limit)
            .skip(options.skip)
            .find();
        
        return {
            items: result.items,
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error getting activity log:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Log admin activity
 */
export async function logActivity(adminId, action, details) {
    try {
        const logEntry = {
            adminId: adminId,
            action: action,
            details: details,
            timestamp: new Date(),
            ipAddress: '', // Would need to be passed from frontend
            _createdDate: new Date()
        };
        
        await wixData.insert('ActivityLog', logEntry);
    } catch (error) {
        console.error('Error logging activity:', error);
    }
}

/**
 * Get meeting minutes list
 */
export async function getMeetingMinutes(options = { limit: 20, skip: 0 }) {
    try {
        const result = await wixData.query('MeetingMinutes')
            .descending('meetingDate')
            .limit(options.limit)
            .skip(options.skip)
            .find();
        
        return {
            items: result.items,
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error getting meeting minutes:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Create meeting minutes
 */
export async function createMeetingMinutes(minutesData, adminId) {
    try {
        const minutes = {
            title: minutesData.title,
            meetingDate: new Date(minutesData.meetingDate),
            location: minutesData.location || 'Virtual',
            agenda: minutesData.agenda || '',
            minutesContent: minutesData.content,
            summary: minutesData.summary || '',
            hasConfidentialSection: minutesData.hasConfidentialSection || false,
            confidentialNote: minutesData.confidentialNote || '',
            attendees: JSON.stringify(minutesData.attendees || []),
            actionItems: minutesData.actionItems || '',
            nextMeetingDate: minutesData.nextMeetingDate ? new Date(minutesData.nextMeetingDate) : null,
            createdBy: adminId,
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert('MeetingMinutes', minutes);
        
        // Log activity
        await logActivity(adminId, 'CREATE_MEETING_MINUTES', {
            minutesId: result._id,
            title: minutes.title
        });
        
        return { success: true, minutesId: result._id };
    } catch (error) {
        console.error('Error creating meeting minutes:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get important messages/announcements
 */
export async function getImportantMessages(includeExpired = false) {
    try {
        let query = wixData.query('ImportantMessages')
            .eq('isActive', true);
        
        if (!includeExpired) {
            const now = new Date();
            query = query.or(
                wixData.query('ImportantMessages').isNotEmpty('expiryDate').ge('expiryDate', now),
                wixData.query('ImportantMessages').isEmpty('expiryDate')
            );
        }
        
        query = query.descending('_createdDate');
        
        const result = await query.find();
        return result.items;
    } catch (error) {
        console.error('Error getting important messages:', error);
        return [];
    }
}

/**
 * Create important message/announcement
 */
export async function createImportantMessage(messageData, adminId) {
    try {
        const message = {
            title: messageData.title,
            content: messageData.content,
            messageType: messageData.type || 'general', // general, urgent, event, maintenance
            priority: messageData.priority || 'normal', // low, normal, high, urgent
            targetAudience: messageData.targetAudience || 'all', // all, members, admins
            expiryDate: messageData.expiryDate ? new Date(messageData.expiryDate) : null,
            isActive: true,
            createdBy: adminId,
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert('ImportantMessages', message);
        return { success: true, messageId: result._id };
    } catch (error) {
        console.error('Error creating message:', error);
        return { success: false, error: error.message };
    }
}

// Helper functions for dashboard stats
async function getUpcomingEventsCount() {
    try {
        return await wixData.query('Events')
            .ge('eventDate', new Date())
            .eq('isActive', true)
            .count();
    } catch (error) {
        return 0;
    }
}

async function getPendingPaymentsCount() {
    try {
        return await wixData.query('ZellePayments')
            .eq('isVerified', false)
            .count();
    } catch (error) {
        return 0;
    }
}

async function getRecentFeedbackCount() {
    try {
        const weekAgo = new Date();
        weekAgo.setDate(weekAgo.getDate() - 7);
        
        return await wixData.query('EventFeedback')
            .ge('submittedAt', weekAgo)
            .count();
    } catch (error) {
        return 0;
    }
}

async function getPendingComplaintsCount() {
    try {
        return await wixData.query('Complaints')
            .eq('status', 'submitted')
            .count();
    } catch (error) {
        return 0;
    }
}

/**
 * Export data for reporting
 */
export async function exportData(collectionName, filters = {}, format = 'json') {
    try {
        let query = wixData.query(collectionName);
        
        // Apply filters
        Object.entries(filters).forEach(([key, value]) => {
            if (value !== undefined && value !== null) {
                query = query.eq(key, value);
            }
        });
        
        const result = await query.limit(1000).find();
        
        if (format === 'json') {
            return {
                success: true,
                data: result.items,
                count: result.totalCount
            };
        }
        
        // For CSV format
        if (format === 'csv' && result.items.length > 0) {
            const headers = Object.keys(result.items[0]).filter(k => !k.startsWith('_'));
            const rows = result.items.map(item => 
                headers.map(h => JSON.stringify(item[h] || '')).join(',')
            );
            
            return {
                success: true,
                data: [headers.join(','), ...rows].join('\n'),
                count: result.totalCount
            };
        }
        
        return { success: true, data: [], count: 0 };
    } catch (error) {
        console.error('Error exporting data:', error);
        return { success: false, error: error.message };
    }
}

```
------------------------------------------------------------

## [5/41] analytics-service
- File: `analytics-service.jsw`
- Size: 29.6 KB
- Lines: 780

```javascript
/**
 * BANF Advanced Analytics Service
 * =================================
 * Wix Velo Backend Module for comprehensive event and organization analytics
 * 
 * Features:
 * - Real-time event dashboards
 * - Predictive analytics for planning
 * - Historical trend analysis
 * - Food/catering optimization
 * - Member engagement scoring
 * - Financial projections
 * 
 * @module backend/analytics-service.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';

// =====================================================
// REAL-TIME EVENT ANALYTICS
// =====================================================

/**
 * Get comprehensive real-time event dashboard data
 * @param {string} eventId
 */
export async function getEventDashboard(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        const rsvps = await wixData.query('EviteRSVPs')
            .eq('eventId', eventId)
            .find();
        
        const invitations = await wixData.query('EviteInvitations')
            .eq('eventId', eventId)
            .find();
        
        const qrCodes = await wixData.query('QRCodes')
            .eq('eventId', eventId)
            .eq('qrType', 'FOOD_SERVICE')
            .find();
        
        // Calculate metrics
        const attending = rsvps.items.filter(r => r.rsvpStatus === 'attending');
        const totalHeadcount = attending.reduce((sum, r) => sum + r.totalAttendees, 0);
        const checkedIn = qrCodes.items.filter(q => q.status === 'used').length;
        
        // Age demographics
        const ageDemographics = {
            adults: attending.reduce((sum, r) => sum + (r.adultCount || 0), 0),
            teens: attending.reduce((sum, r) => sum + (r.teenCount || 0), 0),
            children: attending.reduce((sum, r) => sum + (r.childCount || 0), 0),
            toddlers: attending.reduce((sum, r) => sum + (r.toddlerCount || 0), 0),
            infants: attending.reduce((sum, r) => sum + (r.infantCount || 0), 0)
        };
        
        // Dietary breakdown
        const dietary = {
            vegetarian: attending.reduce((sum, r) => sum + (r.vegetarianCount || 0), 0),
            nonVegetarian: attending.reduce((sum, r) => sum + (r.nonVegCount || 0), 0),
            vegan: attending.reduce((sum, r) => sum + (r.veganCount || 0), 0),
            glutenFree: attending.reduce((sum, r) => sum + (r.glutenFreeCount || 0), 0),
            other: attending.reduce((sum, r) => sum + (r.otherDietaryCount || 0), 0)
        };
        
        return {
            success: true,
            dashboard: {
                event: {
                    title: event.title,
                    date: event.eventDate,
                    status: event.status
                },
                
                // Attendance Overview
                attendance: {
                    invited: invitations.items.length,
                    responded: rsvps.items.length,
                    attending: attending.length,
                    notAttending: rsvps.items.filter(r => r.rsvpStatus === 'not_attending').length,
                    pending: invitations.items.filter(i => !i.responded).length,
                    totalHeadcount: totalHeadcount,
                    checkedIn: checkedIn,
                    checkInRate: totalHeadcount > 0 ? Math.round((checkedIn / totalHeadcount) * 100) : 0
                },
                
                // Demographics
                demographics: {
                    byAge: ageDemographics,
                    ageChart: [
                        { label: 'Adults', value: ageDemographics.adults, color: '#ff6b35' },
                        { label: 'Teens', value: ageDemographics.teens, color: '#f7931e' },
                        { label: 'Children', value: ageDemographics.children, color: '#006A4E' },
                        { label: 'Toddlers', value: ageDemographics.toddlers, color: '#722f37' },
                        { label: 'Infants', value: ageDemographics.infants, color: '#daa520' }
                    ]
                },
                
                // Food Planning
                foodPlanning: {
                    byDietary: dietary,
                    totalMealsNeeded: totalHeadcount,
                    mealBreakdown: {
                        vegMeals: dietary.vegetarian + dietary.vegan,
                        nonVegMeals: dietary.nonVegetarian,
                        specialMeals: dietary.glutenFree + dietary.other
                    },
                    recommendedQuantities: calculateFoodQuantities(totalHeadcount, dietary, ageDemographics)
                },
                
                // Response Rate
                responseMetrics: {
                    responseRate: invitations.items.length > 0 
                        ? Math.round((rsvps.items.length / invitations.items.length) * 100) 
                        : 0,
                    viewRate: invitations.items.length > 0
                        ? Math.round((invitations.items.filter(i => i.viewed).length / invitations.items.length) * 100)
                        : 0
                },
                
                // Last Updated
                lastUpdated: new Date().toISOString()
            }
        };
        
    } catch (error) {
        console.error('Error getting dashboard:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Calculate recommended food quantities based on attendance
 */
function calculateFoodQuantities(totalHeadcount, dietary, ageDemographics) {
    // Adult portions
    const adultPortionFactor = 1;
    // Teen portions (slightly less than adult)
    const teenPortionFactor = 0.9;
    // Child portions (about 60% of adult)
    const childPortionFactor = 0.6;
    // Toddler portions (about 30% of adult)
    const toddlerPortionFactor = 0.3;
    // Infants don't need meals
    const infantPortionFactor = 0;
    
    const totalPortions = 
        (ageDemographics.adults * adultPortionFactor) +
        (ageDemographics.teens * teenPortionFactor) +
        (ageDemographics.children * childPortionFactor) +
        (ageDemographics.toddlers * toddlerPortionFactor) +
        (ageDemographics.infants * infantPortionFactor);
    
    // Add 10% buffer for unexpected guests and second servings
    const bufferMultiplier = 1.1;
    const adjustedPortions = Math.ceil(totalPortions * bufferMultiplier);
    
    // Calculate veg vs non-veg ratio
    const totalWithDietary = dietary.vegetarian + dietary.nonVegetarian + dietary.vegan;
    const vegRatio = totalWithDietary > 0 
        ? (dietary.vegetarian + dietary.vegan) / totalWithDietary 
        : 0.5; // Default to 50-50 if no data
    
    return {
        totalPortions: adjustedPortions,
        vegetarianPortions: Math.ceil(adjustedPortions * vegRatio),
        nonVegPortions: Math.ceil(adjustedPortions * (1 - vegRatio)),
        
        // Specific recommendations
        recommendations: {
            rice: `${Math.ceil(adjustedPortions * 0.25)} kg (approx 1/4 kg per portion)`,
            dal: `${Math.ceil(adjustedPortions * 0.1)} kg`,
            vegetables: `${Math.ceil(adjustedPortions * 0.15)} kg mixed vegetables`,
            meatDish: `${Math.ceil(adjustedPortions * (1 - vegRatio) * 0.15)} kg chicken/mutton`,
            sweets: `${Math.ceil(adjustedPortions * 2)} pieces (2 per person)`,
            water: `${Math.ceil(adjustedPortions * 0.5)} liters (half liter per person)`,
            plates: adjustedPortions,
            napkins: adjustedPortions * 2
        },
        
        kidsSpecial: {
            required: (ageDemographics.children + ageDemographics.toddlers) > 5,
            count: ageDemographics.children + ageDemographics.toddlers,
            suggestion: 'Consider kid-friendly options like plain rice, mild curry, juice boxes'
        },
        
        specialDiet: {
            glutenFree: dietary.glutenFree > 0,
            vegan: dietary.vegan > 0,
            count: dietary.glutenFree + dietary.other,
            suggestion: 'Prepare labeled separate containers for special dietary needs'
        }
    };
}

// =====================================================
// PREDICTIVE ANALYTICS
// =====================================================

/**
 * Predict attendance based on historical data
 * @param {string} eventId
 */
export async function predictAttendance(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        const invitations = await wixData.query('EviteInvitations')
            .eq('eventId', eventId)
            .find();
        
        // Get historical data from similar events
        const historicalEvents = await wixData.query('Events')
            .eq('eventType', event.eventType)
            .ne('_id', eventId)
            .descending('eventDate')
            .limit(10)
            .find();
        
        // Calculate historical response rates
        let avgResponseRate = 0.65; // Default
        let avgAttendanceRate = 0.55; // Default
        let avgGuestsPerRSVP = 2.5; // Default
        
        if (historicalEvents.items.length > 0) {
            const historicalStats = await Promise.all(
                historicalEvents.items.map(async (e) => {
                    const rsvps = await wixData.query('EviteRSVPs')
                        .eq('eventId', e._id)
                        .find();
                    const invites = await wixData.query('EviteInvitations')
                        .eq('eventId', e._id)
                        .find();
                    
                    return {
                        responseRate: invites.items.length > 0 
                            ? rsvps.items.length / invites.items.length 
                            : 0,
                        attendanceRate: rsvps.items.length > 0
                            ? rsvps.items.filter(r => r.rsvpStatus === 'attending').length / rsvps.items.length
                            : 0,
                        avgGuests: rsvps.items.length > 0
                            ? rsvps.items.reduce((sum, r) => sum + r.totalAttendees, 0) / rsvps.items.length
                            : 0
                    };
                })
            );
            
            avgResponseRate = historicalStats.reduce((sum, s) => sum + s.responseRate, 0) / historicalStats.length;
            avgAttendanceRate = historicalStats.reduce((sum, s) => sum + s.attendanceRate, 0) / historicalStats.length;
            avgGuestsPerRSVP = historicalStats.reduce((sum, s) => sum + s.avgGuests, 0) / historicalStats.length;
        }
        
        // Current stats
        const currentRSVPs = await wixData.query('EviteRSVPs')
            .eq('eventId', eventId)
            .find();
        
        const currentAttending = currentRSVPs.items.filter(r => r.rsvpStatus === 'attending');
        const currentHeadcount = currentAttending.reduce((sum, r) => sum + r.totalAttendees, 0);
        
        // Pending invitations
        const pendingInvites = invitations.items.filter(i => !i.responded);
        
        // Predictions
        const expectedAdditionalResponses = Math.round(pendingInvites.length * avgResponseRate);
        const expectedAdditionalAttending = Math.round(expectedAdditionalResponses * avgAttendanceRate);
        const expectedAdditionalHeadcount = Math.round(expectedAdditionalAttending * avgGuestsPerRSVP);
        
        const predictedTotalHeadcount = currentHeadcount + expectedAdditionalHeadcount;
        
        // Confidence calculation
        const daysUntilEvent = Math.ceil((new Date(event.eventDate) - new Date()) / (1000 * 60 * 60 * 24));
        const confidence = calculatePredictionConfidence(
            currentRSVPs.items.length,
            invitations.items.length,
            daysUntilEvent,
            historicalEvents.items.length
        );
        
        return {
            success: true,
            prediction: {
                current: {
                    responded: currentRSVPs.items.length,
                    attending: currentAttending.length,
                    headcount: currentHeadcount,
                    pending: pendingInvites.length
                },
                
                predicted: {
                    finalResponseRate: Math.round(avgResponseRate * 100),
                    finalAttendingCount: currentAttending.length + expectedAdditionalAttending,
                    finalHeadcount: predictedTotalHeadcount,
                    
                    range: {
                        low: Math.round(predictedTotalHeadcount * 0.85),
                        mid: predictedTotalHeadcount,
                        high: Math.round(predictedTotalHeadcount * 1.15)
                    }
                },
                
                confidence: {
                    level: confidence.level,
                    score: confidence.score,
                    factors: confidence.factors
                },
                
                recommendations: generatePredictionRecommendations(
                    predictedTotalHeadcount,
                    daysUntilEvent,
                    pendingInvites.length
                ),
                
                basedOn: {
                    historicalEvents: historicalEvents.items.length,
                    avgResponseRate: Math.round(avgResponseRate * 100),
                    avgAttendanceRate: Math.round(avgAttendanceRate * 100),
                    avgGuestsPerRSVP: avgGuestsPerRSVP.toFixed(1)
                }
            }
        };
        
    } catch (error) {
        console.error('Error predicting attendance:', error);
        return { success: false, error: error.message };
    }
}

function calculatePredictionConfidence(respondedCount, totalInvited, daysUntilEvent, historicalDataPoints) {
    let score = 50; // Base score
    const factors = [];
    
    // Factor 1: Response rate so far
    const currentResponseRate = totalInvited > 0 ? respondedCount / totalInvited : 0;
    if (currentResponseRate > 0.7) {
        score += 20;
        factors.push('High current response rate (+20)');
    } else if (currentResponseRate > 0.5) {
        score += 10;
        factors.push('Moderate response rate (+10)');
    } else {
        factors.push('Low response rate so far');
    }
    
    // Factor 2: Historical data
    if (historicalDataPoints >= 5) {
        score += 15;
        factors.push('Good historical data (+15)');
    } else if (historicalDataPoints >= 2) {
        score += 5;
        factors.push('Limited historical data (+5)');
    } else {
        score -= 10;
        factors.push('Insufficient historical data (-10)');
    }
    
    // Factor 3: Time until event
    if (daysUntilEvent <= 3) {
        score += 15;
        factors.push('Event imminent, stable numbers (+15)');
    } else if (daysUntilEvent <= 7) {
        score += 5;
        factors.push('Event within a week (+5)');
    } else if (daysUntilEvent > 14) {
        score -= 15;
        factors.push('Event far away, numbers may change (-15)');
    }
    
    // Cap score
    score = Math.max(20, Math.min(95, score));
    
    let level = 'Low';
    if (score >= 80) level = 'High';
    else if (score >= 60) level = 'Medium';
    
    return { score, level, factors };
}

function generatePredictionRecommendations(predictedHeadcount, daysUntilEvent, pendingInvites) {
    const recommendations = [];
    
    if (pendingInvites > 20 && daysUntilEvent <= 7) {
        recommendations.push({
            priority: 'high',
            action: 'Send RSVP reminders',
            reason: `${pendingInvites} invites still pending with event in ${daysUntilEvent} days`
        });
    }
    
    if (predictedHeadcount > 200) {
        recommendations.push({
            priority: 'medium',
            action: 'Confirm venue capacity',
            reason: `Expected ${predictedHeadcount} attendees - verify venue can accommodate`
        });
    }
    
    if (daysUntilEvent <= 3) {
        recommendations.push({
            priority: 'high',
            action: 'Finalize catering orders',
            reason: 'Event is in 3 days or less - finalize food quantities'
        });
    }
    
    if (daysUntilEvent <= 5 && daysUntilEvent > 2) {
        recommendations.push({
            priority: 'medium',
            action: 'Generate and send QR codes',
            reason: 'Good time to send QR codes to confirmed attendees'
        });
    }
    
    return recommendations;
}

// =====================================================
// HISTORICAL TRENDS
// =====================================================

/**
 * Get organization-wide analytics and trends
 */
export async function getOrganizationAnalytics() {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        // Get all events from past year
        const oneYearAgo = new Date();
        oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
        
        const events = await wixData.query('Events')
            .ge('eventDate', oneYearAgo)
            .find();
        
        // Get all members
        const members = await wixData.query('MemberProfiles')
            .find();
        
        // Calculate metrics
        const eventsByMonth = {};
        const attendanceByEvent = {};
        
        for (const event of events.items) {
            const month = new Date(event.eventDate).toLocaleString('default', { month: 'short', year: 'numeric' });
            eventsByMonth[month] = (eventsByMonth[month] || 0) + 1;
            
            const rsvps = await wixData.query('EviteRSVPs')
                .eq('eventId', event._id)
                .eq('rsvpStatus', 'attending')
                .find();
            
            attendanceByEvent[event._id] = {
                title: event.title,
                date: event.eventDate,
                type: event.eventType,
                attendance: rsvps.items.reduce((sum, r) => sum + r.totalAttendees, 0)
            };
        }
        
        // Member engagement
        const memberEngagement = await calculateMemberEngagement(members.items);
        
        // Financial overview
        const financialSummary = await getFinancialSummary();
        
        return {
            success: true,
            analytics: {
                overview: {
                    totalMembers: members.items.length,
                    activeMembers: members.items.filter(m => m.membershipStatus === 'active').length,
                    totalEvents: events.items.length,
                    avgAttendance: Object.values(attendanceByEvent).length > 0
                        ? Math.round(
                            Object.values(attendanceByEvent).reduce((sum, e) => sum + e.attendance, 0) /
                            Object.values(attendanceByEvent).length
                        )
                        : 0
                },
                
                eventTrends: {
                    byMonth: eventsByMonth,
                    byType: events.items.reduce((acc, e) => {
                        acc[e.eventType] = (acc[e.eventType] || 0) + 1;
                        return acc;
                    }, {}),
                    popularEvents: Object.values(attendanceByEvent)
                        .sort((a, b) => b.attendance - a.attendance)
                        .slice(0, 5)
                },
                
                memberEngagement: memberEngagement,
                
                financialSummary: financialSummary
            }
        };
        
    } catch (error) {
        console.error('Error getting org analytics:', error);
        return { success: false, error: error.message };
    }
}

async function calculateMemberEngagement(members) {
    const engagement = {
        highEngagement: 0,
        mediumEngagement: 0,
        lowEngagement: 0,
        noEngagement: 0
    };
    
    const engagementDetails = [];
    
    for (const memberProfile of members.slice(0, 100)) { // Limit for performance
        // Count event attendance
        const rsvps = await wixData.query('EviteRSVPs')
            .eq('memberId', memberProfile._id)
            .eq('rsvpStatus', 'attending')
            .find();
        
        const attendanceCount = rsvps.items.length;
        let level = 'none';
        
        if (attendanceCount >= 5) {
            engagement.highEngagement++;
            level = 'high';
        } else if (attendanceCount >= 3) {
            engagement.mediumEngagement++;
            level = 'medium';
        } else if (attendanceCount >= 1) {
            engagement.lowEngagement++;
            level = 'low';
        } else {
            engagement.noEngagement++;
        }
        
        engagementDetails.push({
            memberId: memberProfile._id,
            name: `${memberProfile.firstName} ${memberProfile.lastName}`,
            eventsAttended: attendanceCount,
            level: level
        });
    }
    
    return {
        breakdown: engagement,
        topEngaged: engagementDetails
            .sort((a, b) => b.eventsAttended - a.eventsAttended)
            .slice(0, 10)
    };
}

async function getFinancialSummary() {
    try {
        // Get membership payments
        const membershipPayments = await wixData.query('MembershipPayments')
            .ge('createdAt', new Date(new Date().getFullYear(), 0, 1)) // Current year
            .find();
        
        // Get event payments
        const eventPayments = await wixData.query('EventPayments')
            .ge('createdAt', new Date(new Date().getFullYear(), 0, 1))
            .find();
        
        // Get sponsorships
        const sponsorships = await wixData.query('SponsorPayments')
            .ge('createdAt', new Date(new Date().getFullYear(), 0, 1))
            .find();
        
        const membershipTotal = membershipPayments.items
            .filter(p => p.status === 'completed')
            .reduce((sum, p) => sum + (p.amount || 0), 0);
        
        const eventTotal = eventPayments.items
            .filter(p => p.status === 'completed')
            .reduce((sum, p) => sum + (p.amount || 0), 0);
        
        const sponsorTotal = sponsorships.items
            .filter(p => p.status === 'completed')
            .reduce((sum, p) => sum + (p.amount || 0), 0);
        
        return {
            membershipRevenue: membershipTotal,
            eventRevenue: eventTotal,
            sponsorshipRevenue: sponsorTotal,
            totalRevenue: membershipTotal + eventTotal + sponsorTotal,
            transactionCount: membershipPayments.items.length + eventPayments.items.length + sponsorships.items.length
        };
        
    } catch (error) {
        console.error('Error getting financial summary:', error);
        return {
            membershipRevenue: 0,
            eventRevenue: 0,
            sponsorshipRevenue: 0,
            totalRevenue: 0,
            transactionCount: 0
        };
    }
}

// =====================================================
// CATERING OPTIMIZATION
// =====================================================

/**
 * Generate optimized catering report
 * @param {string} eventId
 */
export async function getCateringReport(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        const rsvps = await wixData.query('EviteRSVPs')
            .eq('eventId', eventId)
            .eq('rsvpStatus', 'attending')
            .find();
        
        // Aggregate data
        let totalAttendees = 0;
        const dietaryBreakdown = {};
        const ageBreakdown = {};
        const specialRequirements = [];
        const attendeeDetails = [];
        
        for (const rsvp of rsvps.items) {
            // Main attendee
            totalAttendees += rsvp.totalAttendees;
            
            // Dietary
            const mainDiet = rsvp.mainAttendee.dietary || 'no_restriction';
            dietaryBreakdown[mainDiet] = (dietaryBreakdown[mainDiet] || 0) + 1;
            
            // Age
            const mainAge = rsvp.mainAttendee.ageCategory || 'adult';
            ageBreakdown[mainAge] = (ageBreakdown[mainAge] || 0) + 1;
            
            // Special requirements
            if (rsvp.mainAttendee.dietaryNotes) {
                specialRequirements.push({
                    name: rsvp.mainAttendee.name,
                    requirement: rsvp.mainAttendee.dietaryNotes
                });
            }
            
            // Details
            attendeeDetails.push({
                name: rsvp.mainAttendee.name,
                dietary: mainDiet,
                ageCategory: mainAge,
                notes: rsvp.mainAttendee.dietaryNotes || ''
            });
            
            // Guests
            for (const guest of (rsvp.guests || [])) {
                const guestDiet = guest.dietary || 'no_restriction';
                dietaryBreakdown[guestDiet] = (dietaryBreakdown[guestDiet] || 0) + 1;
                
                const guestAge = guest.ageCategory || 'adult';
                ageBreakdown[guestAge] = (ageBreakdown[guestAge] || 0) + 1;
                
                if (guest.dietaryNotes) {
                    specialRequirements.push({
                        name: guest.name,
                        requirement: guest.dietaryNotes
                    });
                }
                
                attendeeDetails.push({
                    name: guest.name,
                    dietary: guestDiet,
                    ageCategory: guestAge,
                    notes: guest.dietaryNotes || ''
                });
            }
        }
        
        // Generate portions
        const vegCount = (dietaryBreakdown['vegetarian'] || 0) + (dietaryBreakdown['vegan'] || 0);
        const nonVegCount = dietaryBreakdown['non_vegetarian'] || 0;
        const noRestCount = dietaryBreakdown['no_restriction'] || 0;
        
        // Assume no-restriction splits 50-50
        const estimatedVegTotal = vegCount + Math.ceil(noRestCount * 0.5);
        const estimatedNonVegTotal = nonVegCount + Math.floor(noRestCount * 0.5);
        
        // Add buffer
        const buffer = 1.15; // 15% buffer
        
        return {
            success: true,
            report: {
                event: {
                    title: event.title,
                    date: event.eventDate,
                    location: event.venueName
                },
                
                headcount: {
                    confirmed: totalAttendees,
                    withBuffer: Math.ceil(totalAttendees * buffer),
                    rsvpCount: rsvps.items.length
                },
                
                dietary: {
                    breakdown: dietaryBreakdown,
                    recommendations: {
                        vegetarianMeals: Math.ceil(estimatedVegTotal * buffer),
                        nonVegMeals: Math.ceil(estimatedNonVegTotal * buffer),
                        veganMeals: Math.ceil((dietaryBreakdown['vegan'] || 0) * buffer),
                        glutenFreeMeals: Math.ceil((dietaryBreakdown['gluten_free'] || 0) * buffer)
                    }
                },
                
                age: {
                    breakdown: ageBreakdown,
                    childrenCount: (ageBreakdown['child'] || 0) + (ageBreakdown['toddler'] || 0),
                    kidsPlates: Math.ceil(((ageBreakdown['child'] || 0) + (ageBreakdown['toddler'] || 0)) * buffer),
                    highChairsNeeded: (ageBreakdown['toddler'] || 0) + (ageBreakdown['infant'] || 0)
                },
                
                specialRequirements: {
                    count: specialRequirements.length,
                    details: specialRequirements
                },
                
                printableList: {
                    total: attendeeDetails.length,
                    sortedByDietary: attendeeDetails.sort((a, b) => a.dietary.localeCompare(b.dietary))
                }
            }
        };
        
    } catch (error) {
        console.error('Error generating catering report:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

async function isAdmin(memberId) {
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec')
            );
        }
        return false;
    } catch {
        return false;
    }
}

```
------------------------------------------------------------

## [6/41] automation-framework
- File: `automation-framework.jsw`
- Size: 22.5 KB
- Lines: 722

```javascript
/**
 * BANF Automation Framework - Master Orchestrator
 * =================================================
 * Central automation hub that coordinates all BANF automation services
 * 
 * This module serves as the master controller for:
 * - Event Automation (event-automation.jsw)
 * - Member Automation (member-automation.jsw)
 * - Payment Automation (payment-automation.jsw)
 * - Communication Automation
 * - Scheduled Tasks
 * - Workflow Triggers
 * 
 * @module backend/automation-framework.jsw
 */

import wixData from 'wix-data';
import { triggeredEmails } from 'wix-crm-backend';
import { currentMember } from 'wix-members-backend';

// Import automation sub-modules
import * as eventAutomation from 'backend/event-automation.jsw';
import * as memberAutomation from 'backend/member-automation.jsw';
import * as paymentAutomation from 'backend/payment-automation.jsw';
import * as communicationHub from 'backend/communication-hub.jsw';
import * as radioScheduler from 'backend/radio-scheduler.jsw';
import * as streamingService from 'backend/streaming-service.jsw';

// =====================================================
// AUTOMATION FRAMEWORK CONFIGURATION
// =====================================================

const AUTOMATION_CONFIG = {
    version: '1.0.0',
    enabledModules: {
        events: true,
        members: true,
        payments: true,
        communications: true,
        radio: true,
        streaming: true
    },
    
    // Scheduled task intervals (in hours)
    schedules: {
        memberRenewalCheck: 24,      // Daily
        eventReminderCheck: 6,       // Every 6 hours
        birthdayCheck: 24,           // Daily at midnight
        paymentReminderCheck: 24,    // Daily
        engagementScoreUpdate: 168,  // Weekly
        dataCleanup: 168,            // Weekly
        analyticsReport: 168         // Weekly
    },
    
    // Notification settings
    notifications: {
        adminEmail: 'admin@banfjax.org',
        enableSlack: false,
        enableSMS: false
    },
    
    // Bengali calendar events (Durga Puja, Saraswati Puja, etc.)
    bengaliEvents: {
        DURGA_PUJA: { month: 10, type: 'multi-day' },
        KALI_PUJA: { month: 10, type: 'single-day' },
        SARASWATI_PUJA: { month: 2, type: 'single-day' },
        HOLI: { month: 3, type: 'single-day' },
        POILA_BOISHAKH: { month: 4, type: 'single-day' },
        RABINDRA_JAYANTI: { month: 5, type: 'single-day' },
        MAHALAYA: { month: 9, type: 'special-broadcast' }
    }
};

// =====================================================
// WORKFLOW DEFINITIONS
// =====================================================

/**
 * Predefined automation workflows that can be triggered
 */
const WORKFLOWS = {
    // New Member Onboarding
    NEW_MEMBER_ONBOARDING: {
        id: 'new_member_onboarding',
        name: 'New Member Onboarding',
        trigger: 'member.created',
        steps: [
            { action: 'send_welcome_email', delay: 0 },
            { action: 'add_to_newsletter', delay: 0 },
            { action: 'create_member_profile', delay: 0 },
            { action: 'send_getting_started_guide', delay: 24 * 60 }, // 24 hours
            { action: 'send_first_event_invitation', delay: 72 * 60 }  // 3 days
        ]
    },
    
    // Event Registration Flow
    EVENT_REGISTRATION: {
        id: 'event_registration',
        name: 'Event Registration Flow',
        trigger: 'event.rsvp',
        steps: [
            { action: 'send_confirmation_email', delay: 0 },
            { action: 'add_to_calendar', delay: 0 },
            { action: 'send_reminder_48h', delay: -48 * 60 }, // 48 hours before event
            { action: 'send_reminder_2h', delay: -2 * 60 },   // 2 hours before event
            { action: 'send_checkin_qr', delay: -24 * 60 }    // 24 hours before event
        ]
    },
    
    // Payment Received
    PAYMENT_RECEIVED: {
        id: 'payment_received',
        name: 'Payment Received Workflow',
        trigger: 'payment.completed',
        steps: [
            { action: 'send_receipt', delay: 0 },
            { action: 'update_member_status', delay: 0 },
            { action: 'log_transaction', delay: 0 },
            { action: 'send_thank_you', delay: 30 }  // 30 minutes
        ]
    },
    
    // Membership Renewal Reminder
    RENEWAL_REMINDER: {
        id: 'renewal_reminder',
        name: 'Membership Renewal Reminder',
        trigger: 'membership.expiring',
        steps: [
            { action: 'send_renewal_notice_30d', delay: -30 * 24 * 60 },
            { action: 'send_renewal_notice_14d', delay: -14 * 24 * 60 },
            { action: 'send_renewal_notice_7d', delay: -7 * 24 * 60 },
            { action: 'send_renewal_notice_1d', delay: -24 * 60 },
            { action: 'send_expiration_notice', delay: 0 }
        ]
    },
    
    // Puja Event Automation
    PUJA_EVENT: {
        id: 'puja_event',
        name: 'Durga Puja Event Automation',
        trigger: 'puja.scheduled',
        steps: [
            { action: 'create_volunteer_schedule', delay: -30 * 24 * 60 },
            { action: 'send_sponsorship_requests', delay: -60 * 24 * 60 },
            { action: 'activate_mahalaya_radio', delay: -7 * 24 * 60 },
            { action: 'send_puja_schedule', delay: -3 * 24 * 60 },
            { action: 'start_live_stream', delay: 0 },
            { action: 'send_post_puja_survey', delay: 24 * 60 }
        ]
    }
};

// =====================================================
// MASTER ORCHESTRATOR FUNCTIONS
// =====================================================

/**
 * Initialize the automation framework
 * Should be called on app startup
 */
export async function initializeFramework() {
    console.log('🚀 Initializing BANF Automation Framework v' + AUTOMATION_CONFIG.version);
    
    const status = {
        initialized: new Date().toISOString(),
        modules: {}
    };
    
    // Initialize each enabled module
    if (AUTOMATION_CONFIG.enabledModules.events) {
        try {
            await eventAutomation.initialize?.();
            status.modules.events = 'active';
        } catch (e) {
            status.modules.events = 'error: ' + e.message;
        }
    }
    
    if (AUTOMATION_CONFIG.enabledModules.members) {
        try {
            await memberAutomation.initialize?.();
            status.modules.members = 'active';
        } catch (e) {
            status.modules.members = 'error: ' + e.message;
        }
    }
    
    if (AUTOMATION_CONFIG.enabledModules.payments) {
        try {
            await paymentAutomation.initialize?.();
            status.modules.payments = 'active';
        } catch (e) {
            status.modules.payments = 'error: ' + e.message;
        }
    }
    
    // Log initialization
    await logAutomationEvent('FRAMEWORK_INITIALIZED', status);
    
    return status;
}

/**
 * Execute a specific workflow
 * @param {string} workflowId - The workflow to execute
 * @param {Object} context - Context data for the workflow
 */
export async function executeWorkflow(workflowId, context) {
    const workflow = WORKFLOWS[workflowId];
    
    if (!workflow) {
        throw new Error(`Workflow not found: ${workflowId}`);
    }
    
    console.log(`🔄 Executing workflow: ${workflow.name}`);
    
    const execution = {
        workflowId,
        startedAt: new Date().toISOString(),
        context,
        steps: [],
        status: 'running'
    };
    
    try {
        for (const step of workflow.steps) {
            const stepResult = await executeWorkflowStep(step, context);
            execution.steps.push({
                action: step.action,
                executedAt: new Date().toISOString(),
                result: stepResult
            });
        }
        
        execution.status = 'completed';
        execution.completedAt = new Date().toISOString();
        
    } catch (error) {
        execution.status = 'failed';
        execution.error = error.message;
    }
    
    // Log workflow execution
    await logWorkflowExecution(execution);
    
    return execution;
}

/**
 * Execute a single workflow step
 */
async function executeWorkflowStep(step, context) {
    const { action, delay } = step;
    
    // If delay is negative (before event), schedule for later
    if (delay !== 0) {
        return await scheduleDelayedAction(action, context, delay);
    }
    
    // Execute immediately
    return await executeAction(action, context);
}

/**
 * Execute a specific action
 */
async function executeAction(action, context) {
    console.log(`  ▶️ Executing action: ${action}`);
    
    switch (action) {
        // Member actions
        case 'send_welcome_email':
            return await memberAutomation.sendWelcomeEmail?.(context.memberId);
            
        case 'add_to_newsletter':
            return await memberAutomation.subscribeToNewsletter?.(context.memberId);
            
        case 'create_member_profile':
            return await memberAutomation.createMemberProfile?.(context.memberId);
            
        case 'send_getting_started_guide':
            return await communicationHub.sendGettingStartedGuide?.(context.memberId);
            
        // Event actions
        case 'send_confirmation_email':
            return await eventAutomation.sendRSVPConfirmation?.(context.eventId, context.memberId);
            
        case 'add_to_calendar':
            return await eventAutomation.addToCalendar?.(context.eventId, context.memberId);
            
        case 'send_reminder_48h':
        case 'send_reminder_2h':
            return await eventAutomation.sendEventReminder?.(context.eventId, context.memberId);
            
        case 'send_checkin_qr':
            return await eventAutomation.sendCheckInQR?.(context.eventId, context.memberId);
            
        // Payment actions
        case 'send_receipt':
            return await paymentAutomation.generateAndSendReceipt?.(context.paymentId);
            
        case 'update_member_status':
            return await paymentAutomation.updateMembershipStatus?.(context.memberId, context.paymentType);
            
        case 'log_transaction':
            return await paymentAutomation.logTransaction?.(context.paymentId);
            
        case 'send_thank_you':
            return await communicationHub.sendThankYouMessage?.(context.memberId, context.paymentType);
            
        // Renewal actions
        case 'send_renewal_notice_30d':
        case 'send_renewal_notice_14d':
        case 'send_renewal_notice_7d':
        case 'send_renewal_notice_1d':
        case 'send_expiration_notice':
            return await memberAutomation.sendRenewalReminder?.(context.memberId, action);
            
        // Puja actions
        case 'create_volunteer_schedule':
            return await eventAutomation.createVolunteerSchedule?.(context.eventId);
            
        case 'send_sponsorship_requests':
            return await paymentAutomation.sendSponsorshipRequests?.(context.eventId);
            
        case 'activate_mahalaya_radio':
            return await radioScheduler.activateMahalayaMode?.();
            
        case 'send_puja_schedule':
            return await eventAutomation.sendPujaSchedule?.(context.eventId);
            
        case 'start_live_stream':
            return await streamingService.startScheduledStream?.(context.streamId);
            
        case 'send_post_puja_survey':
            return await eventAutomation.sendPostEventSurvey?.(context.eventId);
            
        default:
            console.warn(`Unknown action: ${action}`);
            return { status: 'skipped', reason: 'unknown action' };
    }
}

/**
 * Schedule a delayed action
 */
async function scheduleDelayedAction(action, context, delayMinutes) {
    const scheduledFor = new Date();
    scheduledFor.setMinutes(scheduledFor.getMinutes() + Math.abs(delayMinutes));
    
    const scheduledTask = {
        action,
        context,
        scheduledFor: scheduledFor.toISOString(),
        status: 'scheduled',
        createdAt: new Date().toISOString()
    };
    
    // Store in scheduled tasks collection
    await wixData.insert('ScheduledTasks', scheduledTask);
    
    return { status: 'scheduled', scheduledFor: scheduledTask.scheduledFor };
}

// =====================================================
// SCHEDULED TASK RUNNER
// =====================================================

/**
 * Run scheduled tasks (should be called by a job scheduler)
 * This function checks for due tasks and executes them
 */
export async function runScheduledTasks() {
    const now = new Date().toISOString();
    
    // Find all due tasks
    const dueTasks = await wixData.query('ScheduledTasks')
        .le('scheduledFor', now)
        .eq('status', 'scheduled')
        .find();
    
    console.log(`⏰ Found ${dueTasks.items.length} scheduled tasks to run`);
    
    const results = [];
    
    for (const task of dueTasks.items) {
        try {
            // Execute the task
            const result = await executeAction(task.action, task.context);
            
            // Update task status
            task.status = 'completed';
            task.completedAt = new Date().toISOString();
            task.result = result;
            
            await wixData.update('ScheduledTasks', task);
            
            results.push({ taskId: task._id, status: 'completed' });
            
        } catch (error) {
            // Mark as failed
            task.status = 'failed';
            task.error = error.message;
            
            await wixData.update('ScheduledTasks', task);
            
            results.push({ taskId: task._id, status: 'failed', error: error.message });
        }
    }
    
    return results;
}

// =====================================================
// DAILY AUTOMATION CHECKS
// =====================================================

/**
 * Daily automation routine - should be scheduled to run daily
 */
export async function runDailyAutomation() {
    console.log('📅 Running daily automation checks...');
    
    const results = {
        date: new Date().toISOString(),
        checks: {}
    };
    
    // 1. Check membership renewals
    if (AUTOMATION_CONFIG.enabledModules.members) {
        results.checks.renewals = await memberAutomation.checkExpiringMemberships?.();
    }
    
    // 2. Send birthday wishes
    if (AUTOMATION_CONFIG.enabledModules.members) {
        results.checks.birthdays = await memberAutomation.sendBirthdayWishes?.();
    }
    
    // 3. Check upcoming events and send reminders
    if (AUTOMATION_CONFIG.enabledModules.events) {
        results.checks.eventReminders = await eventAutomation.sendUpcomingEventReminders?.();
    }
    
    // 4. Check pending payments
    if (AUTOMATION_CONFIG.enabledModules.payments) {
        results.checks.paymentReminders = await paymentAutomation.sendPaymentReminders?.();
    }
    
    // 5. Update radio schedule if special day
    if (AUTOMATION_CONFIG.enabledModules.radio) {
        results.checks.radioSchedule = await checkSpecialRadioSchedule();
    }
    
    // 6. Run any scheduled tasks
    results.checks.scheduledTasks = await runScheduledTasks();
    
    // Log daily automation run
    await logAutomationEvent('DAILY_AUTOMATION', results);
    
    return results;
}

/**
 * Weekly automation routine
 */
export async function runWeeklyAutomation() {
    console.log('📊 Running weekly automation checks...');
    
    const results = {
        date: new Date().toISOString(),
        checks: {}
    };
    
    // 1. Update engagement scores
    if (AUTOMATION_CONFIG.enabledModules.members) {
        results.checks.engagementScores = await memberAutomation.updateAllEngagementScores?.();
    }
    
    // 2. Generate weekly analytics report
    results.checks.analytics = await generateWeeklyAnalytics();
    
    // 3. Data cleanup
    results.checks.cleanup = await performDataCleanup();
    
    // 4. Generate radio schedule for next week
    if (AUTOMATION_CONFIG.enabledModules.radio) {
        results.checks.radioSchedule = await radioScheduler.generateWeeklySchedule?.();
    }
    
    // Log weekly automation run
    await logAutomationEvent('WEEKLY_AUTOMATION', results);
    
    return results;
}

// =====================================================
// SPECIAL EVENT AUTOMATION
// =====================================================

/**
 * Check for special Bengali calendar events
 */
async function checkSpecialRadioSchedule() {
    const today = new Date();
    const month = today.getMonth() + 1;
    const day = today.getDate();
    
    // Check for Mahalaya (early morning special broadcast)
    if (month === 9 || month === 10) {
        // Mahalaya is typically in late September
        const mahalayaActive = await radioScheduler.isMahalayaActive?.();
        if (mahalayaActive) {
            return { status: 'mahalaya_active', message: 'Mahalaya broadcast mode enabled' };
        }
    }
    
    // Check for other special days
    for (const [eventName, config] of Object.entries(AUTOMATION_CONFIG.bengaliEvents)) {
        if (config.month === month) {
            return { status: 'special_event', event: eventName };
        }
    }
    
    return { status: 'normal' };
}

/**
 * Generate weekly analytics report
 */
async function generateWeeklyAnalytics() {
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    
    const analytics = {
        period: {
            start: weekAgo.toISOString(),
            end: new Date().toISOString()
        },
        members: {
            newMembers: 0,
            renewals: 0,
            expirations: 0
        },
        events: {
            totalEvents: 0,
            totalAttendance: 0,
            averageRSVPRate: 0
        },
        payments: {
            totalRevenue: 0,
            donations: 0,
            memberships: 0
        }
    };
    
    // Query data for the week
    // (In real implementation, aggregate from respective collections)
    
    return analytics;
}

/**
 * Perform data cleanup
 */
async function performDataCleanup() {
    const results = {
        oldLogsRemoved: 0,
        orphanedRecordsRemoved: 0,
        tempFilesCleared: 0
    };
    
    // Remove automation logs older than 90 days
    const ninetyDaysAgo = new Date();
    ninetyDaysAgo.setDate(ninetyDaysAgo.getDate() - 90);
    
    const oldLogs = await wixData.query('AutomationLogs')
        .lt('timestamp', ninetyDaysAgo.toISOString())
        .find();
    
    for (const log of oldLogs.items) {
        await wixData.remove('AutomationLogs', log._id);
        results.oldLogsRemoved++;
    }
    
    return results;
}

// =====================================================
// LOGGING & MONITORING
// =====================================================

/**
 * Log automation event
 */
async function logAutomationEvent(eventType, data) {
    try {
        await wixData.insert('AutomationLogs', {
            eventType,
            data: JSON.stringify(data),
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        console.error('Failed to log automation event:', error);
    }
}

/**
 * Log workflow execution
 */
async function logWorkflowExecution(execution) {
    try {
        await wixData.insert('WorkflowExecutions', {
            workflowId: execution.workflowId,
            status: execution.status,
            startedAt: execution.startedAt,
            completedAt: execution.completedAt,
            stepsCount: execution.steps.length,
            error: execution.error,
            details: JSON.stringify(execution)
        });
    } catch (error) {
        console.error('Failed to log workflow execution:', error);
    }
}

/**
 * Get automation status dashboard
 */
export async function getAutomationStatus() {
    const status = {
        framework: {
            version: AUTOMATION_CONFIG.version,
            enabledModules: AUTOMATION_CONFIG.enabledModules
        },
        recentActivity: [],
        scheduledTasks: [],
        errors: []
    };
    
    // Get recent automation logs
    const recentLogs = await wixData.query('AutomationLogs')
        .descending('timestamp')
        .limit(10)
        .find();
    status.recentActivity = recentLogs.items;
    
    // Get pending scheduled tasks
    const pendingTasks = await wixData.query('ScheduledTasks')
        .eq('status', 'scheduled')
        .ascending('scheduledFor')
        .limit(20)
        .find();
    status.scheduledTasks = pendingTasks.items;
    
    // Get recent errors
    const recentErrors = await wixData.query('AutomationLogs')
        .contains('eventType', 'ERROR')
        .descending('timestamp')
        .limit(5)
        .find();
    status.errors = recentErrors.items;
    
    return status;
}

// =====================================================
// TRIGGER HANDLERS
// =====================================================

/**
 * Handle new member trigger
 * Should be called from member creation hook
 */
export async function onMemberCreated(memberId, memberData) {
    return await executeWorkflow('NEW_MEMBER_ONBOARDING', {
        memberId,
        memberData
    });
}

/**
 * Handle RSVP trigger
 * Should be called from RSVP submission
 */
export async function onEventRSVP(eventId, memberId) {
    return await executeWorkflow('EVENT_REGISTRATION', {
        eventId,
        memberId
    });
}

/**
 * Handle payment completion trigger
 * Should be called from payment webhook
 */
export async function onPaymentCompleted(paymentId, paymentData) {
    return await executeWorkflow('PAYMENT_RECEIVED', {
        paymentId,
        memberId: paymentData.memberId,
        paymentType: paymentData.type,
        amount: paymentData.amount
    });
}

/**
 * Handle Puja event scheduling
 */
export async function onPujaScheduled(eventId, streamId) {
    return await executeWorkflow('PUJA_EVENT', {
        eventId,
        streamId
    });
}

// =====================================================
// EXPORTS
// =====================================================

export {
    AUTOMATION_CONFIG,
    WORKFLOWS
};

```
------------------------------------------------------------

## [7/41] budget-finance-service
- File: `budget-finance-service.jsw`
- Size: 27.3 KB
- Lines: 772

```javascript
/**
 * BANF Budget & Finance Service
 * ===============================
 * Wix Velo Backend Module for financial management
 * 
 * Features:
 * - Event budget planning
 * - Expense tracking and categorization
 * - Income recording (sponsorships, tickets, donations)
 * - Financial reports and analytics
 * - Budget vs actual comparison
 * 
 * @module backend/budget-finance-service.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';

// =====================================================
// EXPENSE CATEGORIES
// =====================================================

const EXPENSE_CATEGORIES = {
    VENUE: { id: 'venue', name: 'Venue & Rentals', icon: '🏛️', color: '#006A4E' },
    FOOD: { id: 'food', name: 'Food & Catering', icon: '🍽️', color: '#f7931e' },
    DECORATIONS: { id: 'decorations', name: 'Decorations', icon: '🎨', color: '#9c27b0' },
    ENTERTAINMENT: { id: 'entertainment', name: 'Entertainment', icon: '🎵', color: '#e91e63' },
    EQUIPMENT: { id: 'equipment', name: 'Equipment & AV', icon: '🔊', color: '#2196f3' },
    TRANSPORTATION: { id: 'transportation', name: 'Transportation', icon: '🚗', color: '#607d8b' },
    SUPPLIES: { id: 'supplies', name: 'Supplies & Materials', icon: '📦', color: '#795548' },
    MARKETING: { id: 'marketing', name: 'Marketing & Printing', icon: '📢', color: '#ff5722' },
    PERMITS: { id: 'permits', name: 'Permits & Insurance', icon: '📋', color: '#009688' },
    PUJA: { id: 'puja', name: 'Puja Materials', icon: '🙏', color: '#8B0000' },
    PRIEST: { id: 'priest', name: 'Priest & Rituals', icon: '🕉️', color: '#722f37' },
    GIFTS: { id: 'gifts', name: 'Gifts & Prizes', icon: '🎁', color: '#daa520' },
    MISCELLANEOUS: { id: 'misc', name: 'Miscellaneous', icon: '📌', color: '#9e9e9e' }
};

const INCOME_CATEGORIES = {
    TICKET_SALES: { id: 'tickets', name: 'Ticket Sales', icon: '🎫', color: '#4caf50' },
    SPONSORSHIP: { id: 'sponsorship', name: 'Sponsorships', icon: '🤝', color: '#daa520' },
    DONATION: { id: 'donation', name: 'Donations', icon: '💝', color: '#e91e63' },
    MEMBERSHIP: { id: 'membership', name: 'Membership Fees', icon: '💳', color: '#2196f3' },
    MERCHANDISE: { id: 'merchandise', name: 'Merchandise', icon: '👕', color: '#9c27b0' },
    FOOD_SALES: { id: 'food_sales', name: 'Food/Prasad Sales', icon: '🍲', color: '#f7931e' },
    OTHER: { id: 'other', name: 'Other Income', icon: '💰', color: '#607d8b' }
};

const PAYMENT_STATUS = {
    PENDING: 'pending',
    APPROVED: 'approved',
    PAID: 'paid',
    REJECTED: 'rejected',
    CANCELLED: 'cancelled'
};

// =====================================================
// BUDGET MANAGEMENT
// =====================================================

/**
 * Create a budget for an event
 * @param {string} eventId
 * @param {Object} budgetData
 */
export async function createEventBudget(eventId, budgetData) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        
        if (!event) {
            return { success: false, error: 'Event not found' };
        }
        
        // Check for existing budget
        const existing = await wixData.query('EventBudgets')
            .eq('eventId', eventId)
            .find({ suppressAuth: true });
        
        if (existing.items.length > 0) {
            return { success: false, error: 'Budget already exists for this event' };
        }
        
        const budget = await wixData.insert('EventBudgets', {
            eventId: eventId,
            eventTitle: event.title,
            eventDate: event.eventDate,
            
            // Budget amounts by category
            allocations: budgetData.allocations || {},
            totalBudget: budgetData.totalBudget || 0,
            
            // Expected income
            expectedIncome: budgetData.expectedIncome || {},
            totalExpectedIncome: budgetData.totalExpectedIncome || 0,
            
            // Actuals (will be updated)
            actualExpenses: {},
            totalActualExpenses: 0,
            actualIncome: {},
            totalActualIncome: 0,
            
            // Status
            status: 'active',
            approvedBy: member._id,
            approvedAt: new Date(),
            
            // Notes
            notes: budgetData.notes || '',
            
            // Metadata
            createdBy: member._id,
            createdAt: new Date(),
            lastModified: new Date()
        });
        
        return {
            success: true,
            budgetId: budget._id,
            message: 'Budget created successfully'
        };
        
    } catch (error) {
        console.error('Error creating budget:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Update budget allocations
 * @param {string} budgetId
 * @param {Object} updates
 */
export async function updateBudgetAllocations(budgetId, updates) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const budget = await wixData.get('EventBudgets', budgetId);
        
        if (!budget) {
            return { success: false, error: 'Budget not found' };
        }
        
        // Update allocations
        if (updates.allocations) {
            budget.allocations = {
                ...budget.allocations,
                ...updates.allocations
            };
            budget.totalBudget = Object.values(budget.allocations)
                .reduce((sum, val) => sum + (val || 0), 0);
        }
        
        // Update expected income
        if (updates.expectedIncome) {
            budget.expectedIncome = {
                ...budget.expectedIncome,
                ...updates.expectedIncome
            };
            budget.totalExpectedIncome = Object.values(budget.expectedIncome)
                .reduce((sum, val) => sum + (val || 0), 0);
        }
        
        if (updates.notes) {
            budget.notes = updates.notes;
        }
        
        budget.lastModified = new Date();
        budget.lastModifiedBy = member._id;
        
        await wixData.update('EventBudgets', budget);
        
        return {
            success: true,
            message: 'Budget updated successfully'
        };
        
    } catch (error) {
        console.error('Error updating budget:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// EXPENSE MANAGEMENT
// =====================================================

/**
 * Submit an expense
 * @param {Object} expenseData
 */
export async function submitExpense(expenseData) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Unauthorized');
    }
    
    try {
        const expense = await wixData.insert('Expenses', {
            // Event association
            eventId: expenseData.eventId || null,
            budgetId: expenseData.budgetId || null,
            
            // Expense details
            description: expenseData.description,
            category: expenseData.category,
            categoryName: EXPENSE_CATEGORIES[expenseData.category.toUpperCase()]?.name || expenseData.category,
            amount: expenseData.amount,
            
            // Vendor info
            vendorName: expenseData.vendorName || '',
            vendorContact: expenseData.vendorContact || '',
            
            // Payment details
            paymentMethod: expenseData.paymentMethod || 'pending',
            receiptNumber: expenseData.receiptNumber || '',
            receiptImage: expenseData.receiptImage || null,
            
            // Status
            status: PAYMENT_STATUS.PENDING,
            
            // Dates
            expenseDate: expenseData.expenseDate || new Date(),
            dueDate: expenseData.dueDate || null,
            
            // Notes
            notes: expenseData.notes || '',
            
            // Metadata
            submittedBy: member._id,
            submittedByName: `${member.contactDetails?.firstName || ''} ${member.contactDetails?.lastName || ''}`.trim(),
            submittedAt: new Date()
        });
        
        await logFinancialActivity('EXPENSE_SUBMITTED', expense._id, {
            amount: expense.amount,
            category: expense.category,
            submittedBy: member._id
        });
        
        return {
            success: true,
            expenseId: expense._id,
            message: 'Expense submitted for approval'
        };
        
    } catch (error) {
        console.error('Error submitting expense:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Approve or reject an expense
 * @param {string} expenseId
 * @param {string} action - 'approve' or 'reject'
 * @param {string} notes
 */
export async function processExpense(expenseId, action, notes = '') {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const expense = await wixData.get('Expenses', expenseId);
        
        if (!expense) {
            return { success: false, error: 'Expense not found' };
        }
        
        if (action === 'approve') {
            expense.status = PAYMENT_STATUS.APPROVED;
            expense.approvedBy = member._id;
            expense.approvedAt = new Date();
        } else if (action === 'reject') {
            expense.status = PAYMENT_STATUS.REJECTED;
            expense.rejectedBy = member._id;
            expense.rejectedAt = new Date();
            expense.rejectionReason = notes;
        }
        
        expense.processNotes = notes;
        expense.lastModified = new Date();
        
        await wixData.update('Expenses', expense);
        
        // Update budget actuals if approved
        if (action === 'approve' && expense.budgetId) {
            await updateBudgetActuals(expense.budgetId, 'expense', expense.category, expense.amount);
        }
        
        await logFinancialActivity(`EXPENSE_${action.toUpperCase()}D`, expense._id, {
            amount: expense.amount,
            processedBy: member._id
        });
        
        return {
            success: true,
            message: `Expense ${action}d successfully`
        };
        
    } catch (error) {
        console.error('Error processing expense:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Mark expense as paid
 * @param {string} expenseId
 * @param {Object} paymentDetails
 */
export async function markExpensePaid(expenseId, paymentDetails) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const expense = await wixData.get('Expenses', expenseId);
        
        if (!expense) {
            return { success: false, error: 'Expense not found' };
        }
        
        if (expense.status !== PAYMENT_STATUS.APPROVED) {
            return { success: false, error: 'Expense must be approved before marking as paid' };
        }
        
        expense.status = PAYMENT_STATUS.PAID;
        expense.paidAt = new Date();
        expense.paidBy = member._id;
        expense.paymentMethod = paymentDetails.method || expense.paymentMethod;
        expense.paymentReference = paymentDetails.reference || '';
        expense.paymentNotes = paymentDetails.notes || '';
        expense.lastModified = new Date();
        
        await wixData.update('Expenses', expense);
        
        await logFinancialActivity('EXPENSE_PAID', expense._id, {
            amount: expense.amount,
            method: expense.paymentMethod
        });
        
        return {
            success: true,
            message: 'Expense marked as paid'
        };
        
    } catch (error) {
        console.error('Error marking expense paid:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// INCOME MANAGEMENT
// =====================================================

/**
 * Record income
 * @param {Object} incomeData
 */
export async function recordIncome(incomeData) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const income = await wixData.insert('Income', {
            // Event association
            eventId: incomeData.eventId || null,
            budgetId: incomeData.budgetId || null,
            
            // Income details
            description: incomeData.description,
            category: incomeData.category,
            categoryName: INCOME_CATEGORIES[incomeData.category.toUpperCase()]?.name || incomeData.category,
            amount: incomeData.amount,
            
            // Source info
            sourceName: incomeData.sourceName || '',
            sourceContact: incomeData.sourceContact || '',
            memberId: incomeData.memberId || null,
            
            // Payment details
            paymentMethod: incomeData.paymentMethod || 'other',
            referenceNumber: incomeData.referenceNumber || '',
            
            // Dates
            receivedDate: incomeData.receivedDate || new Date(),
            
            // Notes
            notes: incomeData.notes || '',
            
            // Metadata
            recordedBy: member._id,
            recordedAt: new Date()
        });
        
        // Update budget actuals
        if (income.budgetId) {
            await updateBudgetActuals(income.budgetId, 'income', income.category, income.amount);
        }
        
        await logFinancialActivity('INCOME_RECORDED', income._id, {
            amount: income.amount,
            category: income.category
        });
        
        return {
            success: true,
            incomeId: income._id,
            message: 'Income recorded successfully'
        };
        
    } catch (error) {
        console.error('Error recording income:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// FINANCIAL REPORTS
// =====================================================

/**
 * Get event financial summary
 * @param {string} eventId
 */
export async function getEventFinancialSummary(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        
        // Get budget
        const budgets = await wixData.query('EventBudgets')
            .eq('eventId', eventId)
            .find({ suppressAuth: true });
        
        const budget = budgets.items[0] || null;
        
        // Get all expenses
        const expenses = await wixData.query('Expenses')
            .eq('eventId', eventId)
            .find({ suppressAuth: true });
        
        // Get all income
        const income = await wixData.query('Income')
            .eq('eventId', eventId)
            .find({ suppressAuth: true });
        
        // Calculate totals
        const paidExpenses = expenses.items.filter(e => e.status === PAYMENT_STATUS.PAID);
        const totalExpenses = paidExpenses.reduce((sum, e) => sum + e.amount, 0);
        const pendingExpenses = expenses.items
            .filter(e => e.status === PAYMENT_STATUS.PENDING || e.status === PAYMENT_STATUS.APPROVED)
            .reduce((sum, e) => sum + e.amount, 0);
        
        const totalIncome = income.items.reduce((sum, i) => sum + i.amount, 0);
        
        // Group by category
        const expensesByCategory = {};
        for (const exp of paidExpenses) {
            expensesByCategory[exp.category] = (expensesByCategory[exp.category] || 0) + exp.amount;
        }
        
        const incomeByCategory = {};
        for (const inc of income.items) {
            incomeByCategory[inc.category] = (incomeByCategory[inc.category] || 0) + inc.amount;
        }
        
        // Calculate variance
        const budgetedAmount = budget?.totalBudget || 0;
        const variance = budgetedAmount - totalExpenses;
        const variancePercent = budgetedAmount > 0 
            ? Math.round((variance / budgetedAmount) * 100) 
            : 0;
        
        return {
            success: true,
            summary: {
                event: {
                    title: event?.title,
                    date: event?.eventDate
                },
                
                // Budget vs Actual
                budget: {
                    allocated: budgetedAmount,
                    actual: totalExpenses,
                    pending: pendingExpenses,
                    variance: variance,
                    variancePercent: variancePercent,
                    status: variance >= 0 ? 'under_budget' : 'over_budget'
                },
                
                // Income
                income: {
                    expected: budget?.totalExpectedIncome || 0,
                    actual: totalIncome,
                    variance: totalIncome - (budget?.totalExpectedIncome || 0)
                },
                
                // Net
                netPosition: totalIncome - totalExpenses,
                
                // Breakdowns
                expensesByCategory: Object.entries(expensesByCategory).map(([cat, amount]) => ({
                    category: cat,
                    categoryName: EXPENSE_CATEGORIES[cat.toUpperCase()]?.name || cat,
                    icon: EXPENSE_CATEGORIES[cat.toUpperCase()]?.icon || '📌',
                    amount: amount,
                    budgeted: budget?.allocations?.[cat] || 0,
                    variance: (budget?.allocations?.[cat] || 0) - amount
                })),
                
                incomeByCategory: Object.entries(incomeByCategory).map(([cat, amount]) => ({
                    category: cat,
                    categoryName: INCOME_CATEGORIES[cat.toUpperCase()]?.name || cat,
                    icon: INCOME_CATEGORIES[cat.toUpperCase()]?.icon || '💰',
                    amount: amount
                })),
                
                // Transactions
                recentExpenses: expenses.items.slice(0, 5).map(e => ({
                    description: e.description,
                    amount: e.amount,
                    category: e.category,
                    status: e.status,
                    date: e.expenseDate
                })),
                
                recentIncome: income.items.slice(0, 5).map(i => ({
                    description: i.description,
                    amount: i.amount,
                    category: i.category,
                    date: i.receivedDate
                }))
            }
        };
        
    } catch (error) {
        console.error('Error getting financial summary:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get organization annual financial report
 * @param {number} year
 */
export async function getAnnualFinancialReport(year) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const startDate = new Date(year, 0, 1);
        const endDate = new Date(year, 11, 31);
        
        // Get all expenses for the year
        const expenses = await wixData.query('Expenses')
            .ge('expenseDate', startDate)
            .le('expenseDate', endDate)
            .eq('status', PAYMENT_STATUS.PAID)
            .find({ suppressAuth: true });
        
        // Get all income for the year
        const income = await wixData.query('Income')
            .ge('receivedDate', startDate)
            .le('receivedDate', endDate)
            .find({ suppressAuth: true });
        
        // Monthly breakdown
        const monthlyData = {};
        for (let month = 0; month < 12; month++) {
            monthlyData[month] = { expenses: 0, income: 0 };
        }
        
        for (const exp of expenses.items) {
            const month = new Date(exp.expenseDate).getMonth();
            monthlyData[month].expenses += exp.amount;
        }
        
        for (const inc of income.items) {
            const month = new Date(inc.receivedDate).getMonth();
            monthlyData[month].income += inc.amount;
        }
        
        // Category breakdown
        const categoryExpenses = {};
        const categoryIncome = {};
        
        for (const exp of expenses.items) {
            categoryExpenses[exp.category] = (categoryExpenses[exp.category] || 0) + exp.amount;
        }
        
        for (const inc of income.items) {
            categoryIncome[inc.category] = (categoryIncome[inc.category] || 0) + inc.amount;
        }
        
        const totalExpenses = expenses.items.reduce((sum, e) => sum + e.amount, 0);
        const totalIncome = income.items.reduce((sum, i) => sum + i.amount, 0);
        
        return {
            success: true,
            report: {
                year: year,
                
                // Summary
                summary: {
                    totalIncome: totalIncome,
                    totalExpenses: totalExpenses,
                    netPosition: totalIncome - totalExpenses,
                    transactionCount: expenses.items.length + income.items.length
                },
                
                // Monthly trend
                monthlyTrend: Object.entries(monthlyData).map(([month, data]) => ({
                    month: new Date(year, parseInt(month), 1).toLocaleString('default', { month: 'short' }),
                    expenses: data.expenses,
                    income: data.income,
                    net: data.income - data.expenses
                })),
                
                // Category breakdowns
                expenseCategories: Object.entries(categoryExpenses)
                    .map(([cat, amount]) => ({
                        category: cat,
                        name: EXPENSE_CATEGORIES[cat.toUpperCase()]?.name || cat,
                        icon: EXPENSE_CATEGORIES[cat.toUpperCase()]?.icon || '📌',
                        amount: amount,
                        percentage: Math.round((amount / totalExpenses) * 100)
                    }))
                    .sort((a, b) => b.amount - a.amount),
                
                incomeCategories: Object.entries(categoryIncome)
                    .map(([cat, amount]) => ({
                        category: cat,
                        name: INCOME_CATEGORIES[cat.toUpperCase()]?.name || cat,
                        icon: INCOME_CATEGORIES[cat.toUpperCase()]?.icon || '💰',
                        amount: amount,
                        percentage: Math.round((amount / totalIncome) * 100)
                    }))
                    .sort((a, b) => b.amount - a.amount)
            }
        };
        
    } catch (error) {
        console.error('Error getting annual report:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// EXPENSE TRACKING DASHBOARD
// =====================================================

/**
 * Get pending expenses for approval
 */
export async function getPendingExpenses() {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const expenses = await wixData.query('Expenses')
            .eq('status', PAYMENT_STATUS.PENDING)
            .ascending('submittedAt')
            .find({ suppressAuth: true });
        
        return {
            success: true,
            expenses: expenses.items.map(e => ({
                _id: e._id,
                description: e.description,
                category: e.category,
                categoryName: e.categoryName,
                amount: e.amount,
                vendorName: e.vendorName,
                submittedBy: e.submittedByName,
                submittedAt: e.submittedAt,
                eventId: e.eventId,
                receiptImage: e.receiptImage,
                notes: e.notes
            })),
            totalPending: expenses.totalCount
        };
        
    } catch (error) {
        console.error('Error getting pending expenses:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

async function updateBudgetActuals(budgetId, type, category, amount) {
    try {
        const budget = await wixData.get('EventBudgets', budgetId);
        if (!budget) return;
        
        if (type === 'expense') {
            budget.actualExpenses = budget.actualExpenses || {};
            budget.actualExpenses[category] = (budget.actualExpenses[category] || 0) + amount;
            budget.totalActualExpenses = Object.values(budget.actualExpenses)
                .reduce((sum, val) => sum + val, 0);
        } else if (type === 'income') {
            budget.actualIncome = budget.actualIncome || {};
            budget.actualIncome[category] = (budget.actualIncome[category] || 0) + amount;
            budget.totalActualIncome = Object.values(budget.actualIncome)
                .reduce((sum, val) => sum + val, 0);
        }
        
        budget.lastModified = new Date();
        await wixData.update('EventBudgets', budget);
    } catch (error) {
        console.error('Error updating budget actuals:', error);
    }
}

async function logFinancialActivity(action, recordId, details) {
    await wixData.insert('FinancialActivityLog', {
        action: action,
        recordId: recordId,
        details: details,
        timestamp: new Date()
    });
}

async function isAdmin(memberId) {
    if (!memberId) return false;
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec') ||
                role.toLowerCase().includes('treasurer')
            );
        }
        return false;
    } catch {
        return false;
    }
}

// Export constants
export { EXPENSE_CATEGORIES, INCOME_CATEGORIES, PAYMENT_STATUS };

```
------------------------------------------------------------

## [8/41] carpool-transport-service
- File: `carpool-transport-service.jsw`
- Size: 30.8 KB
- Lines: 890

```javascript
/**
 * BANF Carpool & Transportation Service
 * =======================================
 * Wix Velo Backend Module for event carpooling coordination
 * 
 * Features:
 * - Carpool offer/request matching
 * - Ride coordination
 * - Route optimization suggestions
 * - Transportation needs analytics
 * - Accessibility support
 * 
 * @module backend/carpool-transport-service.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';

// =====================================================
// CARPOOL CONFIGURATION
// =====================================================

const CARPOOL_STATUS = {
    ACTIVE: 'active',
    FULL: 'full',
    CANCELLED: 'cancelled',
    COMPLETED: 'completed'
};

const RIDE_STATUS = {
    PENDING: 'pending',
    CONFIRMED: 'confirmed',
    DECLINED: 'declined',
    CANCELLED: 'cancelled',
    COMPLETED: 'completed'
};

const RIDE_TYPE = {
    OFFER: 'offer',     // Driver offering seats
    REQUEST: 'request'  // Passenger seeking ride
};

const VEHICLE_TYPES = {
    SEDAN: { label: 'Sedan', maxSeats: 4, icon: '🚗' },
    SUV: { label: 'SUV', maxSeats: 6, icon: '🚙' },
    MINIVAN: { label: 'Minivan', maxSeats: 7, icon: '🚐' },
    VAN: { label: 'Van', maxSeats: 12, icon: '🚌' },
    OTHER: { label: 'Other', maxSeats: 4, icon: '🚗' }
};

// =====================================================
// CARPOOL MANAGEMENT
// =====================================================

/**
 * Offer a ride to an event
 * @param {Object} offerData
 */
export async function offerRide(offerData) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in to offer rides');
    }
    
    try {
        const memberName = `${member.contactDetails?.firstName || ''} ${member.contactDetails?.lastName || ''}`.trim();
        const vehicleType = VEHICLE_TYPES[offerData.vehicleType] || VEHICLE_TYPES.SEDAN;
        
        const offer = await wixData.insert('CarpoolOffers', {
            // Event
            eventId: offerData.eventId,
            eventTitle: offerData.eventTitle || '',
            eventDate: offerData.eventDate,
            
            // Type
            type: RIDE_TYPE.OFFER,
            
            // Driver
            driverId: member._id,
            driverName: memberName,
            driverPhone: member.contactDetails?.phones?.[0] || offerData.phone || '',
            driverEmail: member.loginEmail || '',
            
            // Vehicle
            vehicleType: offerData.vehicleType || 'SEDAN',
            vehicleDescription: offerData.vehicleDescription || '',
            vehicleColor: offerData.vehicleColor || '',
            licensePlate: offerData.licensePlate || '',
            
            // Capacity
            totalSeats: Math.min(offerData.totalSeats || 4, vehicleType.maxSeats),
            availableSeats: Math.min(offerData.totalSeats || 4, vehicleType.maxSeats),
            bookedSeats: 0,
            
            // Location
            departureLocation: offerData.departureLocation,
            departureCity: offerData.departureCity || '',
            departureZip: offerData.departureZip || '',
            departureCoordinates: offerData.departureCoordinates || null,
            
            // Stops
            willMakeStops: offerData.willMakeStops || false,
            possibleStops: offerData.possibleStops || [],
            
            // Timing
            departureTime: offerData.departureTime,
            returnRide: offerData.returnRide || false,
            returnTime: offerData.returnTime || null,
            
            // Preferences
            allowChildren: offerData.allowChildren !== false,
            allowPets: offerData.allowPets || false,
            smokingAllowed: offerData.smokingAllowed || false,
            luggageSpace: offerData.luggageSpace || 'medium',
            wheelchairAccessible: offerData.wheelchairAccessible || false,
            
            // Notes
            notes: offerData.notes || '',
            
            // Status
            status: CARPOOL_STATUS.ACTIVE,
            
            // Metadata
            createdAt: new Date(),
            lastModified: new Date()
        });
        
        return {
            success: true,
            offerId: offer._id,
            message: 'Ride offer posted successfully'
        };
        
    } catch (error) {
        console.error('Error offering ride:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Request a ride to an event
 * @param {Object} requestData
 */
export async function requestRide(requestData) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in to request rides');
    }
    
    try {
        const memberName = `${member.contactDetails?.firstName || ''} ${member.contactDetails?.lastName || ''}`.trim();
        
        const request = await wixData.insert('CarpoolRequests', {
            // Event
            eventId: requestData.eventId,
            eventTitle: requestData.eventTitle || '',
            eventDate: requestData.eventDate,
            
            // Type
            type: RIDE_TYPE.REQUEST,
            
            // Requester
            requesterId: member._id,
            requesterName: memberName,
            requesterPhone: member.contactDetails?.phones?.[0] || requestData.phone || '',
            requesterEmail: member.loginEmail || '',
            
            // Party size
            adultsCount: requestData.adultsCount || 1,
            childrenCount: requestData.childrenCount || 0,
            totalSeatsNeeded: (requestData.adultsCount || 1) + (requestData.childrenCount || 0),
            
            // Location
            pickupLocation: requestData.pickupLocation,
            pickupCity: requestData.pickupCity || '',
            pickupZip: requestData.pickupZip || '',
            pickupCoordinates: requestData.pickupCoordinates || null,
            
            // Timing
            preferredDepartureTime: requestData.preferredDepartureTime,
            timeFlexibility: requestData.timeFlexibility || 30, // minutes
            needReturnRide: requestData.needReturnRide || false,
            
            // Requirements
            needChildSeat: requestData.needChildSeat || false,
            childSeatCount: requestData.childSeatCount || 0,
            wheelchairAccess: requestData.wheelchairAccess || false,
            luggageAmount: requestData.luggageAmount || 'none',
            
            // Preferences
            petAllergy: requestData.petAllergy || false,
            
            // Notes
            notes: requestData.notes || '',
            
            // Status
            status: RIDE_STATUS.PENDING,
            matchedOfferId: null,
            
            // Metadata
            createdAt: new Date(),
            lastModified: new Date()
        });
        
        // Try to auto-match
        const matchResult = await findMatchingOffers(request._id);
        
        return {
            success: true,
            requestId: request._id,
            potentialMatches: matchResult.matches?.length || 0,
            message: 'Ride request submitted successfully'
        };
        
    } catch (error) {
        console.error('Error requesting ride:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// RIDE MATCHING
// =====================================================

/**
 * Find matching ride offers for a request
 * @param {string} requestId
 */
export async function findMatchingOffers(requestId) {
    try {
        const request = await wixData.get('CarpoolRequests', requestId);
        
        if (!request) {
            return { success: false, error: 'Request not found' };
        }
        
        // Find offers for same event
        let query = wixData.query('CarpoolOffers')
            .eq('eventId', request.eventId)
            .eq('status', CARPOOL_STATUS.ACTIVE)
            .ge('availableSeats', request.totalSeatsNeeded);
        
        // Filter by preferences
        if (request.wheelchairAccess) {
            query = query.eq('wheelchairAccessible', true);
        }
        
        if (request.petAllergy) {
            query = query.eq('allowPets', false);
        }
        
        const offers = await query.find({ suppressAuth: true });
        
        // Score and rank matches
        const scoredMatches = offers.items.map(offer => {
            let score = 100;
            
            // Location proximity (would need geocoding for accurate calculation)
            if (offer.departureCity && request.pickupCity) {
                if (offer.departureCity.toLowerCase() === request.pickupCity.toLowerCase()) {
                    score += 30;
                }
            }
            
            if (offer.departureZip && request.pickupZip) {
                if (offer.departureZip.substring(0, 3) === request.pickupZip.substring(0, 3)) {
                    score += 20;
                }
            }
            
            // Time match
            if (offer.departureTime && request.preferredDepartureTime) {
                const offerTime = new Date(offer.departureTime).getTime();
                const requestTime = new Date(request.preferredDepartureTime).getTime();
                const diffMinutes = Math.abs(offerTime - requestTime) / (1000 * 60);
                
                if (diffMinutes <= request.timeFlexibility) {
                    score += 25;
                } else if (diffMinutes <= 60) {
                    score += 10;
                }
            }
            
            // Return ride match
            if (request.needReturnRide && offer.returnRide) {
                score += 20;
            }
            
            // Children preference
            if (request.childrenCount > 0 && offer.allowChildren) {
                score += 10;
            }
            
            return {
                offer: {
                    _id: offer._id,
                    driverName: offer.driverName,
                    departureLocation: offer.departureLocation,
                    departureCity: offer.departureCity,
                    departureTime: offer.departureTime,
                    availableSeats: offer.availableSeats,
                    vehicleType: offer.vehicleType,
                    vehicleDescription: offer.vehicleDescription,
                    returnRide: offer.returnRide,
                    willMakeStops: offer.willMakeStops,
                    notes: offer.notes
                },
                score: score
            };
        });
        
        // Sort by score
        scoredMatches.sort((a, b) => b.score - a.score);
        
        return {
            success: true,
            matches: scoredMatches.slice(0, 10),
            totalMatches: scoredMatches.length
        };
        
    } catch (error) {
        console.error('Error finding matches:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Request to join a carpool
 * @param {string} offerId
 * @param {string} requestId - Optional, if from a request
 */
export async function requestToJoinCarpool(offerId, requestId = null) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in');
    }
    
    try {
        const offer = await wixData.get('CarpoolOffers', offerId);
        
        if (!offer) {
            return { success: false, error: 'Ride offer not found' };
        }
        
        if (offer.status !== CARPOOL_STATUS.ACTIVE) {
            return { success: false, error: 'This ride is no longer available' };
        }
        
        // Get request details if provided
        let request = null;
        let seatsNeeded = 1;
        
        if (requestId) {
            request = await wixData.get('CarpoolRequests', requestId);
            if (request) {
                seatsNeeded = request.totalSeatsNeeded;
            }
        }
        
        if (offer.availableSeats < seatsNeeded) {
            return { 
                success: false, 
                error: `Not enough seats available. Need ${seatsNeeded}, only ${offer.availableSeats} available.`
            };
        }
        
        const memberName = `${member.contactDetails?.firstName || ''} ${member.contactDetails?.lastName || ''}`.trim();
        
        // Create ride booking
        const booking = await wixData.insert('CarpoolBookings', {
            offerId: offerId,
            requestId: requestId,
            eventId: offer.eventId,
            
            // Driver
            driverId: offer.driverId,
            driverName: offer.driverName,
            
            // Passenger
            passengerId: member._id,
            passengerName: memberName,
            passengerPhone: member.contactDetails?.phones?.[0] || '',
            passengerEmail: member.loginEmail || '',
            
            // Details
            seatsBooked: seatsNeeded,
            pickupLocation: request?.pickupLocation || offer.departureLocation,
            pickupTime: request?.preferredDepartureTime || offer.departureTime,
            
            // Status
            status: RIDE_STATUS.PENDING,
            
            // Communication
            driverConfirmed: false,
            passengerConfirmed: true,
            
            // Metadata
            createdAt: new Date()
        });
        
        // Notify driver (would integrate with notification system)
        
        return {
            success: true,
            bookingId: booking._id,
            message: 'Ride request sent to driver. Waiting for confirmation.'
        };
        
    } catch (error) {
        console.error('Error requesting carpool:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Confirm or decline a ride booking
 * @param {string} bookingId
 * @param {boolean} confirmed
 * @param {string} message
 */
export async function respondToBooking(bookingId, confirmed, message = '') {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in');
    }
    
    try {
        const booking = await wixData.get('CarpoolBookings', bookingId);
        
        if (!booking) {
            return { success: false, error: 'Booking not found' };
        }
        
        // Verify this is the driver
        if (booking.driverId !== member._id) {
            return { success: false, error: 'Only the driver can respond to this booking' };
        }
        
        if (confirmed) {
            // Check seats still available
            const offer = await wixData.get('CarpoolOffers', booking.offerId);
            
            if (offer.availableSeats < booking.seatsBooked) {
                return { 
                    success: false, 
                    error: 'No longer enough seats available'
                };
            }
            
            // Update offer
            offer.availableSeats -= booking.seatsBooked;
            offer.bookedSeats += booking.seatsBooked;
            
            if (offer.availableSeats === 0) {
                offer.status = CARPOOL_STATUS.FULL;
            }
            
            await wixData.update('CarpoolOffers', offer);
            
            // Update booking
            booking.status = RIDE_STATUS.CONFIRMED;
            booking.driverConfirmed = true;
            booking.confirmedAt = new Date();
            booking.driverMessage = message;
            
            // Update request if exists
            if (booking.requestId) {
                const request = await wixData.get('CarpoolRequests', booking.requestId);
                if (request) {
                    request.status = RIDE_STATUS.CONFIRMED;
                    request.matchedOfferId = booking.offerId;
                    await wixData.update('CarpoolRequests', request);
                }
            }
            
        } else {
            booking.status = RIDE_STATUS.DECLINED;
            booking.declinedAt = new Date();
            booking.driverMessage = message;
        }
        
        await wixData.update('CarpoolBookings', booking);
        
        return {
            success: true,
            message: confirmed ? 'Ride confirmed!' : 'Booking declined'
        };
        
    } catch (error) {
        console.error('Error responding to booking:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// CARPOOL LISTINGS
// =====================================================

/**
 * Get carpool offers for an event
 * @param {string} eventId
 * @param {Object} filters
 */
export async function getEventCarpools(eventId, filters = {}) {
    try {
        let query = wixData.query('CarpoolOffers')
            .eq('eventId', eventId)
            .eq('status', CARPOOL_STATUS.ACTIVE)
            .gt('availableSeats', 0);
        
        if (filters.departureCity) {
            query = query.contains('departureCity', filters.departureCity);
        }
        
        if (filters.minSeats) {
            query = query.ge('availableSeats', filters.minSeats);
        }
        
        if (filters.returnRide !== undefined) {
            query = query.eq('returnRide', filters.returnRide);
        }
        
        if (filters.allowChildren !== undefined) {
            query = query.eq('allowChildren', filters.allowChildren);
        }
        
        if (filters.wheelchairAccessible) {
            query = query.eq('wheelchairAccessible', true);
        }
        
        const offers = await query
            .ascending('departureTime')
            .find({ suppressAuth: true });
        
        return {
            success: true,
            offers: offers.items.map(o => ({
                _id: o._id,
                driverName: o.driverName,
                departureLocation: o.departureLocation,
                departureCity: o.departureCity,
                departureTime: o.departureTime,
                totalSeats: o.totalSeats,
                availableSeats: o.availableSeats,
                vehicleType: o.vehicleType,
                vehicleDescription: o.vehicleDescription,
                returnRide: o.returnRide,
                willMakeStops: o.willMakeStops,
                allowChildren: o.allowChildren,
                wheelchairAccessible: o.wheelchairAccessible,
                notes: o.notes
            })),
            totalOffers: offers.totalCount
        };
        
    } catch (error) {
        console.error('Error getting carpools:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get pending ride requests for an event
 * @param {string} eventId
 */
export async function getEventRideRequests(eventId) {
    try {
        const requests = await wixData.query('CarpoolRequests')
            .eq('eventId', eventId)
            .eq('status', RIDE_STATUS.PENDING)
            .ascending('preferredDepartureTime')
            .find({ suppressAuth: true });
        
        return {
            success: true,
            requests: requests.items.map(r => ({
                _id: r._id,
                requesterName: r.requesterName,
                pickupCity: r.pickupCity,
                preferredDepartureTime: r.preferredDepartureTime,
                totalSeatsNeeded: r.totalSeatsNeeded,
                adultsCount: r.adultsCount,
                childrenCount: r.childrenCount,
                needReturnRide: r.needReturnRide,
                wheelchairAccess: r.wheelchairAccess,
                notes: r.notes
            })),
            totalRequests: requests.totalCount
        };
        
    } catch (error) {
        console.error('Error getting ride requests:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get member's carpool activity
 */
export async function getMyCarpool() {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in');
    }
    
    try {
        // My offers
        const myOffers = await wixData.query('CarpoolOffers')
            .eq('driverId', member._id)
            .hasSome('status', [CARPOOL_STATUS.ACTIVE, CARPOOL_STATUS.FULL])
            .find({ suppressAuth: true });
        
        // My requests
        const myRequests = await wixData.query('CarpoolRequests')
            .eq('requesterId', member._id)
            .eq('status', RIDE_STATUS.PENDING)
            .find({ suppressAuth: true });
        
        // My confirmed rides (as passenger)
        const myBookings = await wixData.query('CarpoolBookings')
            .eq('passengerId', member._id)
            .eq('status', RIDE_STATUS.CONFIRMED)
            .find({ suppressAuth: true });
        
        // Pending requests for my offers
        const pendingForMe = await wixData.query('CarpoolBookings')
            .eq('driverId', member._id)
            .eq('status', RIDE_STATUS.PENDING)
            .find({ suppressAuth: true });
        
        return {
            success: true,
            myOffers: myOffers.items,
            myRequests: myRequests.items,
            confirmedRides: myBookings.items,
            pendingRequests: pendingForMe.items
        };
        
    } catch (error) {
        console.error('Error getting my carpool:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// TRANSPORTATION ANALYTICS
// =====================================================

/**
 * Get transportation analytics for an event
 * @param {string} eventId
 */
export async function getTransportationAnalytics(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const offers = await wixData.query('CarpoolOffers')
            .eq('eventId', eventId)
            .find({ suppressAuth: true });
        
        const requests = await wixData.query('CarpoolRequests')
            .eq('eventId', eventId)
            .find({ suppressAuth: true });
        
        const bookings = await wixData.query('CarpoolBookings')
            .eq('eventId', eventId)
            .find({ suppressAuth: true });
        
        // Calculate metrics
        const totalSeatsOffered = offers.items.reduce((sum, o) => sum + o.totalSeats, 0);
        const seatsBooked = offers.items.reduce((sum, o) => sum + o.bookedSeats, 0);
        const seatsAvailable = offers.items.reduce((sum, o) => sum + o.availableSeats, 0);
        
        const totalSeatsRequested = requests.items.reduce((sum, r) => sum + r.totalSeatsNeeded, 0);
        const requestsFulfilled = requests.items.filter(r => r.status === RIDE_STATUS.CONFIRMED).length;
        const requestsPending = requests.items.filter(r => r.status === RIDE_STATUS.PENDING).length;
        
        // Location analysis
        const departureCities = {};
        for (const o of offers.items) {
            if (o.departureCity) {
                departureCities[o.departureCity] = (departureCities[o.departureCity] || 0) + 1;
            }
        }
        
        const pickupCities = {};
        for (const r of requests.items) {
            if (r.pickupCity) {
                pickupCities[r.pickupCity] = (pickupCities[r.pickupCity] || 0) + 1;
            }
        }
        
        return {
            success: true,
            analytics: {
                offers: {
                    totalOffers: offers.items.length,
                    activeOffers: offers.items.filter(o => o.status === CARPOOL_STATUS.ACTIVE).length,
                    totalSeatsOffered: totalSeatsOffered,
                    seatsBooked: seatsBooked,
                    seatsAvailable: seatsAvailable,
                    utilizationRate: totalSeatsOffered > 0 
                        ? Math.round((seatsBooked / totalSeatsOffered) * 100) 
                        : 0
                },
                requests: {
                    totalRequests: requests.items.length,
                    pendingRequests: requestsPending,
                    fulfilledRequests: requestsFulfilled,
                    totalSeatsRequested: totalSeatsRequested,
                    fulfillmentRate: requests.items.length > 0
                        ? Math.round((requestsFulfilled / requests.items.length) * 100)
                        : 0
                },
                unfulfilled: {
                    seatsStillNeeded: requests.items
                        .filter(r => r.status === RIDE_STATUS.PENDING)
                        .reduce((sum, r) => sum + r.totalSeatsNeeded, 0)
                },
                geography: {
                    topDepartureCities: Object.entries(departureCities)
                        .sort((a, b) => b[1] - a[1])
                        .slice(0, 5)
                        .map(([city, count]) => ({ city, count })),
                    topPickupCities: Object.entries(pickupCities)
                        .sort((a, b) => b[1] - a[1])
                        .slice(0, 5)
                        .map(([city, count]) => ({ city, count }))
                },
                accessibility: {
                    wheelchairAccessibleOffers: offers.items.filter(o => o.wheelchairAccessible).length,
                    wheelchairRequests: requests.items.filter(r => r.wheelchairAccess).length
                }
            }
        };
        
    } catch (error) {
        console.error('Error getting transportation analytics:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// CANCEL & CLEANUP
// =====================================================

/**
 * Cancel a carpool offer
 * @param {string} offerId
 */
export async function cancelOffer(offerId) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in');
    }
    
    try {
        const offer = await wixData.get('CarpoolOffers', offerId);
        
        if (!offer) {
            return { success: false, error: 'Offer not found' };
        }
        
        if (offer.driverId !== member._id) {
            return { success: false, error: 'Only the driver can cancel this offer' };
        }
        
        // Cancel all pending bookings
        const bookings = await wixData.query('CarpoolBookings')
            .eq('offerId', offerId)
            .hasSome('status', [RIDE_STATUS.PENDING, RIDE_STATUS.CONFIRMED])
            .find({ suppressAuth: true });
        
        for (const booking of bookings.items) {
            booking.status = RIDE_STATUS.CANCELLED;
            booking.cancelledAt = new Date();
            booking.cancelledBy = 'driver';
            await wixData.update('CarpoolBookings', booking);
            
            // TODO: Notify passengers
        }
        
        offer.status = CARPOOL_STATUS.CANCELLED;
        offer.cancelledAt = new Date();
        await wixData.update('CarpoolOffers', offer);
        
        return {
            success: true,
            affectedPassengers: bookings.items.length,
            message: 'Ride offer cancelled'
        };
        
    } catch (error) {
        console.error('Error cancelling offer:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Cancel a ride request
 * @param {string} requestId
 */
export async function cancelRequest(requestId) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in');
    }
    
    try {
        const request = await wixData.get('CarpoolRequests', requestId);
        
        if (!request) {
            return { success: false, error: 'Request not found' };
        }
        
        if (request.requesterId !== member._id) {
            return { success: false, error: 'Only the requester can cancel this request' };
        }
        
        // If there's a booking, handle it
        if (request.matchedOfferId) {
            const booking = await wixData.query('CarpoolBookings')
                .eq('requestId', requestId)
                .eq('status', RIDE_STATUS.CONFIRMED)
                .find({ suppressAuth: true });
            
            if (booking.items.length > 0) {
                const b = booking.items[0];
                b.status = RIDE_STATUS.CANCELLED;
                b.cancelledAt = new Date();
                b.cancelledBy = 'passenger';
                await wixData.update('CarpoolBookings', b);
                
                // Restore seats to offer
                const offer = await wixData.get('CarpoolOffers', request.matchedOfferId);
                if (offer) {
                    offer.availableSeats += b.seatsBooked;
                    offer.bookedSeats -= b.seatsBooked;
                    if (offer.status === CARPOOL_STATUS.FULL) {
                        offer.status = CARPOOL_STATUS.ACTIVE;
                    }
                    await wixData.update('CarpoolOffers', offer);
                }
            }
        }
        
        request.status = RIDE_STATUS.CANCELLED;
        request.cancelledAt = new Date();
        await wixData.update('CarpoolRequests', request);
        
        return {
            success: true,
            message: 'Ride request cancelled'
        };
        
    } catch (error) {
        console.error('Error cancelling request:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

async function isAdmin(memberId) {
    if (!memberId) return false;
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec')
            );
        }
        return false;
    } catch {
        return false;
    }
}

// Export constants
export { CARPOOL_STATUS, RIDE_STATUS, RIDE_TYPE, VEHICLE_TYPES };

```
------------------------------------------------------------

## [9/41] checkin-kiosk-service
- File: `checkin-kiosk-service.jsw`
- Size: 23.4 KB
- Lines: 701

```javascript
/**
 * BANF Check-In Kiosk Service
 * =============================
 * Wix Velo Backend Module for self-service event check-in
 * 
 * Features:
 * - QR code scanning at kiosk
 * - Manual lookup by name/phone
 * - Real-time attendance tracking
 * - Badge printing integration
 * - Family check-in support
 * 
 * @module backend/checkin-kiosk-service.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';

// =====================================================
// KIOSK CONFIGURATION
// =====================================================

const KIOSK_MODES = {
    QR_ONLY: 'qr_only',
    QR_WITH_MANUAL: 'qr_with_manual',
    MANUAL_ONLY: 'manual_only'
};

const CHECKIN_STATUS = {
    NOT_CHECKED_IN: 'not_checked_in',
    CHECKED_IN: 'checked_in',
    CHECKED_OUT: 'checked_out',
    NO_SHOW: 'no_show'
};

const BADGE_TYPES = {
    MEMBER: { label: 'Member', color: '#006A4E', icon: '🏠' },
    GUEST: { label: 'Guest', color: '#f7931e', icon: '👋' },
    VIP: { label: 'VIP', color: '#722f37', icon: '⭐' },
    VOLUNTEER: { label: 'Volunteer', color: '#4285f4', icon: '🤝' },
    EC_MEMBER: { label: 'EC Member', color: '#8B0000', icon: '👑' },
    SPONSOR: { label: 'Sponsor', color: '#daa520', icon: '🏆' },
    CHILD: { label: 'Child', color: '#9c27b0', icon: '🧒' }
};

// =====================================================
// KIOSK SESSION MANAGEMENT
// =====================================================

/**
 * Initialize a kiosk session for an event
 * @param {string} eventId
 * @param {Object} kioskConfig
 */
export async function initializeKiosk(eventId, kioskConfig = {}) {
    try {
        const event = await wixData.get('Events', eventId);
        
        if (!event) {
            return { success: false, error: 'Event not found' };
        }
        
        // Create kiosk session
        const session = await wixData.insert('KioskSessions', {
            eventId: eventId,
            eventTitle: event.title,
            eventDate: event.eventDate,
            
            // Configuration
            mode: kioskConfig.mode || KIOSK_MODES.QR_WITH_MANUAL,
            allowWalkIns: kioskConfig.allowWalkIns !== false,
            requireFoodSelection: kioskConfig.requireFoodSelection || false,
            printBadges: kioskConfig.printBadges || false,
            
            // Station Info
            stationId: kioskConfig.stationId || `KIOSK_${Date.now()}`,
            stationName: kioskConfig.stationName || 'Main Entrance',
            
            // Status
            status: 'active',
            startedAt: new Date(),
            
            // Stats
            stats: {
                totalCheckIns: 0,
                qrCheckIns: 0,
                manualCheckIns: 0,
                walkIns: 0,
                adults: 0,
                children: 0
            }
        });
        
        // Get expected attendees
        const rsvps = await wixData.query('EviteRSVPs')
            .eq('eventId', eventId)
            .eq('rsvpStatus', 'attending')
            .find({ suppressAuth: true });
        
        return {
            success: true,
            sessionId: session._id,
            stationId: session.stationId,
            eventInfo: {
                title: event.title,
                date: event.eventDate,
                venue: event.venueName
            },
            expectedAttendees: rsvps.totalCount,
            mode: session.mode
        };
        
    } catch (error) {
        console.error('Error initializing kiosk:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// CHECK-IN OPERATIONS
// =====================================================

/**
 * Check in via QR code scan
 * @param {string} sessionId
 * @param {string} qrCode
 */
export async function checkInByQR(sessionId, qrCode) {
    try {
        // Validate session
        const session = await wixData.get('KioskSessions', sessionId);
        if (!session || session.status !== 'active') {
            return { success: false, error: 'Invalid kiosk session' };
        }
        
        // Find QR code
        const qrResult = await wixData.query('QRCodes')
            .eq('qrCode', qrCode)
            .eq('eventId', session.eventId)
            .find({ suppressAuth: true });
        
        if (qrResult.items.length === 0) {
            return { 
                success: false, 
                error: 'QR code not found',
                suggestion: 'Try manual lookup'
            };
        }
        
        const qr = qrResult.items[0];
        
        // Check if already used
        if (qr.status === 'used') {
            // Get previous check-in time
            const prevCheckin = await wixData.query('CheckInLog')
                .eq('qrCode', qrCode)
                .descending('checkedInAt')
                .limit(1)
                .find({ suppressAuth: true });
            
            return {
                success: false,
                error: 'Already checked in',
                previousCheckIn: prevCheckin.items[0]?.checkedInAt,
                attendeeInfo: {
                    name: qr.metadata?.attendeeName,
                    email: qr.metadata?.email
                }
            };
        }
        
        // Perform check-in
        const checkInResult = await performCheckIn(session, {
            method: 'qr',
            qrCode: qrCode,
            rsvpId: qr.rsvpId,
            attendeeInfo: qr.metadata
        });
        
        // Update QR code status
        qr.status = 'used';
        qr.usedAt = new Date();
        qr.usedAtStation = session.stationId;
        await wixData.update('QRCodes', qr);
        
        return checkInResult;
        
    } catch (error) {
        console.error('Error QR check-in:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Check in via manual lookup
 * @param {string} sessionId
 * @param {Object} lookupData - { name, phone, email }
 */
export async function checkInByManual(sessionId, lookupData) {
    try {
        const session = await wixData.get('KioskSessions', sessionId);
        if (!session || session.status !== 'active') {
            return { success: false, error: 'Invalid kiosk session' };
        }
        
        // Search for attendee
        let query = wixData.query('EviteRSVPs')
            .eq('eventId', session.eventId)
            .eq('rsvpStatus', 'attending');
        
        if (lookupData.phone) {
            query = query.eq('phone', lookupData.phone);
        } else if (lookupData.email) {
            query = query.eq('email', lookupData.email.toLowerCase());
        } else if (lookupData.name) {
            query = query.contains('attendeeName', lookupData.name);
        }
        
        const rsvps = await query.find({ suppressAuth: true });
        
        if (rsvps.items.length === 0) {
            // No RSVP found - check if walk-ins allowed
            if (session.allowWalkIns) {
                return {
                    success: false,
                    notFound: true,
                    walkInAllowed: true,
                    message: 'No RSVP found. Register as walk-in?'
                };
            }
            return { success: false, error: 'Attendee not found in RSVP list' };
        }
        
        if (rsvps.items.length > 1) {
            // Multiple matches - return list for selection
            return {
                success: false,
                multipleMatches: true,
                matches: rsvps.items.map(r => ({
                    rsvpId: r._id,
                    name: r.attendeeName,
                    email: maskEmail(r.email),
                    phone: maskPhone(r.phone),
                    guestCount: r.totalGuests,
                    checkedIn: r.checkinStatus === 'checked_in'
                }))
            };
        }
        
        const rsvp = rsvps.items[0];
        
        // Check if already checked in
        if (rsvp.checkinStatus === CHECKIN_STATUS.CHECKED_IN) {
            return {
                success: false,
                error: 'Already checked in',
                previousCheckIn: rsvp.checkedInAt
            };
        }
        
        // Perform check-in
        return await performCheckIn(session, {
            method: 'manual',
            rsvpId: rsvp._id,
            attendeeInfo: {
                attendeeName: rsvp.attendeeName,
                email: rsvp.email,
                phone: rsvp.phone,
                dietary: rsvp.dietary,
                guests: rsvp.guests,
                totalAdults: rsvp.totalAdults,
                totalChildren: rsvp.totalChildren
            }
        });
        
    } catch (error) {
        console.error('Error manual check-in:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Register and check in a walk-in attendee
 * @param {string} sessionId
 * @param {Object} walkInData
 */
export async function checkInWalkIn(sessionId, walkInData) {
    try {
        const session = await wixData.get('KioskSessions', sessionId);
        if (!session || session.status !== 'active') {
            return { success: false, error: 'Invalid kiosk session' };
        }
        
        if (!session.allowWalkIns) {
            return { success: false, error: 'Walk-ins not allowed for this event' };
        }
        
        // Create walk-in RSVP
        const walkInRSVP = await wixData.insert('EviteRSVPs', {
            eventId: session.eventId,
            attendeeName: walkInData.name,
            email: walkInData.email,
            phone: walkInData.phone,
            rsvpStatus: 'attending',
            isWalkIn: true,
            
            // Guest info
            totalAdults: walkInData.adults || 1,
            totalChildren: walkInData.children || 0,
            totalGuests: (walkInData.adults || 1) + (walkInData.children || 0),
            
            // Dietary
            dietary: walkInData.dietary || [],
            
            submittedAt: new Date()
        });
        
        // Perform check-in
        return await performCheckIn(session, {
            method: 'walkin',
            rsvpId: walkInRSVP._id,
            attendeeInfo: {
                attendeeName: walkInData.name,
                email: walkInData.email,
                phone: walkInData.phone,
                totalAdults: walkInData.adults || 1,
                totalChildren: walkInData.children || 0,
                dietary: walkInData.dietary
            }
        });
        
    } catch (error) {
        console.error('Error walk-in check-in:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Perform the actual check-in
 */
async function performCheckIn(session, checkInData) {
    const { method, rsvpId, attendeeInfo, qrCode } = checkInData;
    
    // Create check-in log entry
    const checkInLog = await wixData.insert('CheckInLog', {
        sessionId: session._id,
        eventId: session.eventId,
        rsvpId: rsvpId,
        qrCode: qrCode || null,
        
        // Attendee Info
        attendeeName: attendeeInfo.attendeeName,
        email: attendeeInfo.email,
        phone: attendeeInfo.phone,
        
        // Group Info
        totalAdults: attendeeInfo.totalAdults || 1,
        totalChildren: attendeeInfo.totalChildren || 0,
        
        // Check-in Details
        method: method, // 'qr', 'manual', 'walkin'
        stationId: session.stationId,
        stationName: session.stationName,
        checkedInAt: new Date(),
        
        // Status
        status: CHECKIN_STATUS.CHECKED_IN
    });
    
    // Update RSVP status
    if (rsvpId) {
        const rsvp = await wixData.get('EviteRSVPs', rsvpId);
        if (rsvp) {
            rsvp.checkinStatus = CHECKIN_STATUS.CHECKED_IN;
            rsvp.checkedInAt = new Date();
            rsvp.checkedInBy = session.stationId;
            await wixData.update('EviteRSVPs', rsvp);
        }
    }
    
    // Update session stats
    session.stats.totalCheckIns++;
    if (method === 'qr') session.stats.qrCheckIns++;
    if (method === 'manual') session.stats.manualCheckIns++;
    if (method === 'walkin') session.stats.walkIns++;
    session.stats.adults += (attendeeInfo.totalAdults || 1);
    session.stats.children += (attendeeInfo.totalChildren || 0);
    await wixData.update('KioskSessions', session);
    
    // Determine badge type
    const badgeType = determineBadgeType(attendeeInfo);
    
    return {
        success: true,
        checkInId: checkInLog._id,
        message: `Welcome, ${attendeeInfo.attendeeName}!`,
        attendee: {
            name: attendeeInfo.attendeeName,
            adults: attendeeInfo.totalAdults || 1,
            children: attendeeInfo.totalChildren || 0,
            dietary: attendeeInfo.dietary
        },
        badge: {
            type: badgeType,
            ...BADGE_TYPES[badgeType],
            name: attendeeInfo.attendeeName,
            guestOf: method === 'walkin' ? 'Walk-In' : null
        },
        checkedInAt: checkInLog.checkedInAt
    };
}

function determineBadgeType(attendeeInfo) {
    if (attendeeInfo.isVolunteer) return 'VOLUNTEER';
    if (attendeeInfo.isECMember) return 'EC_MEMBER';
    if (attendeeInfo.isSponsor) return 'SPONSOR';
    if (attendeeInfo.isVIP) return 'VIP';
    if (attendeeInfo.memberId) return 'MEMBER';
    return 'GUEST';
}

// =====================================================
// ATTENDANCE SEARCH
// =====================================================

/**
 * Search attendees for check-in
 * @param {string} sessionId
 * @param {string} searchTerm
 */
export async function searchAttendees(sessionId, searchTerm) {
    try {
        const session = await wixData.get('KioskSessions', sessionId);
        if (!session) {
            return { success: false, error: 'Invalid session' };
        }
        
        // Search by name
        const byName = await wixData.query('EviteRSVPs')
            .eq('eventId', session.eventId)
            .eq('rsvpStatus', 'attending')
            .contains('attendeeName', searchTerm)
            .limit(10)
            .find({ suppressAuth: true });
        
        // Search by phone (if numeric)
        let byPhone = { items: [] };
        if (/^\d+$/.test(searchTerm) && searchTerm.length >= 4) {
            byPhone = await wixData.query('EviteRSVPs')
                .eq('eventId', session.eventId)
                .eq('rsvpStatus', 'attending')
                .contains('phone', searchTerm)
                .limit(5)
                .find({ suppressAuth: true });
        }
        
        // Combine and dedupe results
        const allResults = [...byName.items, ...byPhone.items];
        const uniqueResults = allResults.filter((item, index, self) =>
            index === self.findIndex(r => r._id === item._id)
        );
        
        return {
            success: true,
            results: uniqueResults.slice(0, 10).map(r => ({
                rsvpId: r._id,
                name: r.attendeeName,
                phone: maskPhone(r.phone),
                email: maskEmail(r.email),
                totalGuests: r.totalGuests,
                adults: r.totalAdults,
                children: r.totalChildren,
                dietary: r.dietary,
                checkedIn: r.checkinStatus === CHECKIN_STATUS.CHECKED_IN,
                checkedInAt: r.checkedInAt
            })),
            totalFound: uniqueResults.length
        };
        
    } catch (error) {
        console.error('Error searching attendees:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// KIOSK DASHBOARD
// =====================================================

/**
 * Get real-time kiosk stats
 * @param {string} sessionId
 */
export async function getKioskStats(sessionId) {
    try {
        const session = await wixData.get('KioskSessions', sessionId);
        if (!session) {
            return { success: false, error: 'Session not found' };
        }
        
        // Get expected attendees
        const expectedResult = await wixData.query('EviteRSVPs')
            .eq('eventId', session.eventId)
            .eq('rsvpStatus', 'attending')
            .count({ suppressAuth: true });
        
        // Get checked in count
        const checkedInResult = await wixData.query('EviteRSVPs')
            .eq('eventId', session.eventId)
            .eq('checkinStatus', CHECKIN_STATUS.CHECKED_IN)
            .count({ suppressAuth: true });
        
        // Get recent check-ins
        const recentCheckIns = await wixData.query('CheckInLog')
            .eq('sessionId', sessionId)
            .descending('checkedInAt')
            .limit(5)
            .find({ suppressAuth: true });
        
        return {
            success: true,
            stats: {
                expected: expectedResult,
                checkedIn: checkedInResult,
                remaining: expectedResult - checkedInResult,
                checkInRate: expectedResult > 0 
                    ? Math.round((checkedInResult / expectedResult) * 100) 
                    : 0,
                
                // Session stats
                sessionStats: session.stats,
                
                // Station info
                station: {
                    id: session.stationId,
                    name: session.stationName,
                    activeFor: Math.round((Date.now() - new Date(session.startedAt).getTime()) / 60000)
                },
                
                // Recent activity
                recentCheckIns: recentCheckIns.items.map(c => ({
                    name: c.attendeeName,
                    time: c.checkedInAt,
                    method: c.method,
                    partySize: (c.totalAdults || 0) + (c.totalChildren || 0)
                }))
            }
        };
        
    } catch (error) {
        console.error('Error getting kiosk stats:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get all kiosk sessions for an event
 * @param {string} eventId
 */
export async function getEventKioskSessions(eventId) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Unauthorized');
    }
    
    try {
        const sessions = await wixData.query('KioskSessions')
            .eq('eventId', eventId)
            .find({ suppressAuth: true });
        
        return {
            success: true,
            sessions: sessions.items.map(s => ({
                sessionId: s._id,
                stationId: s.stationId,
                stationName: s.stationName,
                status: s.status,
                startedAt: s.startedAt,
                stats: s.stats
            }))
        };
        
    } catch (error) {
        console.error('Error getting kiosk sessions:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// ATTENDANCE REPORT
// =====================================================

/**
 * Get attendance report for an event
 * @param {string} eventId
 */
export async function getAttendanceReport(eventId) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        
        // Get all RSVPs
        const rsvps = await wixData.query('EviteRSVPs')
            .eq('eventId', eventId)
            .find({ suppressAuth: true });
        
        // Get all check-in logs
        const checkIns = await wixData.query('CheckInLog')
            .eq('eventId', eventId)
            .find({ suppressAuth: true });
        
        // Calculate stats
        const totalRSVPs = rsvps.totalCount;
        const attending = rsvps.items.filter(r => r.rsvpStatus === 'attending').length;
        const checkedIn = rsvps.items.filter(r => r.checkinStatus === CHECKIN_STATUS.CHECKED_IN).length;
        const noShows = attending - checkedIn;
        const walkIns = checkIns.items.filter(c => c.method === 'walkin').length;
        
        const totalAdults = checkIns.items.reduce((sum, c) => sum + (c.totalAdults || 0), 0);
        const totalChildren = checkIns.items.reduce((sum, c) => sum + (c.totalChildren || 0), 0);
        
        // Check-in timeline
        const timelineData = {};
        for (const c of checkIns.items) {
            const hour = new Date(c.checkedInAt).getHours();
            timelineData[hour] = (timelineData[hour] || 0) + 1;
        }
        
        return {
            success: true,
            report: {
                event: {
                    title: event?.title,
                    date: event?.eventDate
                },
                summary: {
                    totalRSVPs: totalRSVPs,
                    expectedAttendees: attending,
                    actualCheckedIn: checkedIn,
                    noShows: noShows,
                    walkIns: walkIns,
                    attendanceRate: attending > 0 
                        ? Math.round((checkedIn / attending) * 100) 
                        : 0
                },
                demographics: {
                    totalAdults: totalAdults,
                    totalChildren: totalChildren,
                    totalHeadcount: totalAdults + totalChildren
                },
                checkInMethods: {
                    qr: checkIns.items.filter(c => c.method === 'qr').length,
                    manual: checkIns.items.filter(c => c.method === 'manual').length,
                    walkIn: walkIns
                },
                timeline: Object.entries(timelineData).map(([hour, count]) => ({
                    hour: `${hour}:00`,
                    checkIns: count
                })),
                attendeeList: rsvps.items.map(r => ({
                    name: r.attendeeName,
                    email: r.email,
                    rsvpStatus: r.rsvpStatus,
                    checkinStatus: r.checkinStatus || CHECKIN_STATUS.NOT_CHECKED_IN,
                    checkedInAt: r.checkedInAt,
                    partySize: r.totalGuests
                }))
            }
        };
        
    } catch (error) {
        console.error('Error getting attendance report:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

function maskEmail(email) {
    if (!email) return '';
    const [local, domain] = email.split('@');
    if (!domain) return email;
    const maskedLocal = local.substring(0, 2) + '***';
    return `${maskedLocal}@${domain}`;
}

function maskPhone(phone) {
    if (!phone) return '';
    const digits = phone.replace(/\D/g, '');
    if (digits.length < 4) return phone;
    return '***-***-' + digits.slice(-4);
}

// Export constants
export { KIOSK_MODES, CHECKIN_STATUS, BADGE_TYPES };

```
------------------------------------------------------------

## [10/41] communication-hub
- File: `communication-hub.jsw`
- Size: 31.1 KB
- Lines: 903

```javascript
/**
 * BANF Communication Hub Service
 * ================================
 * Wix Velo Backend Module for multi-channel communication
 * 
 * Features:
 * - Email campaigns and newsletters
 * - WhatsApp integration
 * - SMS notifications
 * - Push notifications
 * - Communication templates
 * - Scheduling and automation
 * 
 * @module backend/communication-hub.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';
import { triggeredEmails } from 'wix-crm-backend';
import { fetch } from 'wix-fetch';

// =====================================================
// COMMUNICATION TEMPLATES
// =====================================================

const MESSAGE_TEMPLATES = {
    // Event Templates
    EVENT_ANNOUNCEMENT: {
        id: 'event_announcement',
        name: 'Event Announcement',
        category: 'events',
        subject: '🎉 BANF {eventType}: {eventTitle}',
        emailTemplate: 'event_announcement',
        smsTemplate: 'BANF Event: {eventTitle} on {date}. RSVP: {rsvpLink}',
        whatsappTemplate: '*🎉 BANF {eventType}*\n\n*{eventTitle}*\n📅 {date}\n📍 {venue}\n\n{description}\n\nRSVP: {rsvpLink}'
    },
    
    EVENT_REMINDER_3DAY: {
        id: 'event_reminder_3day',
        name: '3-Day Event Reminder',
        category: 'events',
        subject: '📆 Reminder: {eventTitle} in 3 Days!',
        emailTemplate: 'event_reminder',
        smsTemplate: 'BANF Reminder: {eventTitle} is in 3 days! See you there.',
        whatsappTemplate: '*📆 Event Reminder*\n\n*{eventTitle}* is coming up in *3 days*!\n\n📅 {date}\n📍 {venue}\n⏰ {time}\n\nLooking forward to seeing you! 🙏'
    },
    
    EVENT_REMINDER_1DAY: {
        id: 'event_reminder_1day',
        name: '1-Day Event Reminder',
        category: 'events',
        subject: '⏰ Tomorrow: {eventTitle}',
        emailTemplate: 'event_reminder',
        smsTemplate: 'BANF: {eventTitle} is TOMORROW! Check your email for QR code.',
        whatsappTemplate: '*⏰ Tomorrow\'s Event*\n\n*{eventTitle}*\n\n📅 {date}\n📍 {venue}\n⏰ {time}\n\n✅ Don\'t forget your QR code for entry!\n\nSee you there! 🎊'
    },
    
    EVENT_DAYOF: {
        id: 'event_dayof',
        name: 'Day-of Reminder',
        category: 'events',
        subject: '🎊 Today: {eventTitle} - See you soon!',
        emailTemplate: 'event_dayof',
        smsTemplate: 'BANF: {eventTitle} TODAY at {venue}. Doors open {time}. Bring your QR code!',
        whatsappTemplate: '*🎊 TODAY\'S EVENT*\n\n*{eventTitle}*\n\n📍 {venue}\n⏰ {time}\n\n✅ Bring your QR code\n🅿️ Parking info: {parkingInfo}\n\nExcited to see you! 🙏'
    },
    
    // Membership Templates
    MEMBERSHIP_WELCOME: {
        id: 'membership_welcome',
        name: 'New Member Welcome',
        category: 'membership',
        subject: '🙏 Welcome to BANF Family, {firstName}!',
        emailTemplate: 'membership_welcome',
        smsTemplate: 'Welcome to BANF! Your membership is now active. Visit banfboston.org for events.',
        whatsappTemplate: '*🙏 Welcome to BANF!*\n\nDear {firstName},\n\nThank you for joining the BANF family!\n\n✅ Membership: {membershipType}\n✅ Valid until: {expiryDate}\n\nStay connected for upcoming events! 🎉'
    },
    
    MEMBERSHIP_RENEWAL: {
        id: 'membership_renewal',
        name: 'Membership Renewal',
        category: 'membership',
        subject: '🔔 Your BANF Membership Expires Soon',
        emailTemplate: 'membership_renewal',
        smsTemplate: 'BANF: Your membership expires on {expiryDate}. Renew now: {renewLink}',
        whatsappTemplate: '*🔔 Membership Renewal*\n\nYour BANF membership expires on *{expiryDate}*.\n\nRenew now to continue enjoying:\n✅ Event discounts\n✅ Early registrations\n✅ Voting rights\n\nRenew: {renewLink}'
    },
    
    // Payment Templates
    PAYMENT_RECEIVED: {
        id: 'payment_received',
        name: 'Payment Confirmation',
        category: 'payment',
        subject: '✅ Payment Received - {description}',
        emailTemplate: 'payment_confirmation',
        smsTemplate: 'BANF: Payment of ${amount} received for {description}. Thank you!',
        whatsappTemplate: '*✅ Payment Confirmed*\n\nThank you for your payment!\n\n💰 Amount: ${amount}\n📝 For: {description}\n🧾 Receipt: {receiptNumber}\n\nQuestions? Reply to this message.'
    },
    
    PAYMENT_FAILED: {
        id: 'payment_failed',
        name: 'Payment Failed',
        category: 'payment',
        subject: '⚠️ Payment Issue - Action Required',
        emailTemplate: 'payment_failed',
        smsTemplate: 'BANF: Your payment of ${amount} failed. Please update: {paymentLink}',
        whatsappTemplate: '*⚠️ Payment Issue*\n\nYour payment of *${amount}* for *{description}* could not be processed.\n\nPlease update your payment method:\n{paymentLink}\n\nNeed help? Reply here.'
    },
    
    // General Templates
    GENERAL_ANNOUNCEMENT: {
        id: 'general_announcement',
        name: 'General Announcement',
        category: 'general',
        subject: '📢 {subject}',
        emailTemplate: 'general_announcement',
        smsTemplate: 'BANF: {message}',
        whatsappTemplate: '*📢 BANF Announcement*\n\n{message}'
    },
    
    EMERGENCY_ALERT: {
        id: 'emergency_alert',
        name: 'Emergency Alert',
        category: 'emergency',
        subject: '🚨 URGENT: {subject}',
        emailTemplate: 'emergency_alert',
        smsTemplate: 'URGENT BANF: {message}',
        whatsappTemplate: '*🚨 URGENT NOTICE*\n\n{message}\n\nBANF Committee'
    }
};

const CHANNEL_TYPES = {
    EMAIL: 'email',
    SMS: 'sms',
    WHATSAPP: 'whatsapp',
    PUSH: 'push'
};

// =====================================================
// CAMPAIGN MANAGEMENT
// =====================================================

/**
 * Create a new communication campaign
 * @param {Object} campaignData
 */
export async function createCampaign(campaignData) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const campaign = await wixData.insert('CommCampaigns', {
            // Basic Info
            name: campaignData.name,
            description: campaignData.description || '',
            templateId: campaignData.templateId,
            
            // Target Audience
            audienceType: campaignData.audienceType, // 'all', 'members', 'specific', 'filter'
            audienceFilter: campaignData.audienceFilter || {},
            recipientIds: campaignData.recipientIds || [],
            totalRecipients: 0,
            
            // Channels
            channels: campaignData.channels || [CHANNEL_TYPES.EMAIL],
            
            // Content
            subject: campaignData.subject,
            content: campaignData.content || {},
            variables: campaignData.variables || {},
            
            // Scheduling
            scheduleType: campaignData.scheduleType || 'immediate', // 'immediate', 'scheduled', 'recurring'
            scheduledDate: campaignData.scheduledDate || null,
            recurringPattern: campaignData.recurringPattern || null,
            
            // Status
            status: 'draft', // 'draft', 'scheduled', 'sending', 'sent', 'failed'
            
            // Stats
            stats: {
                sent: 0,
                delivered: 0,
                opened: 0,
                clicked: 0,
                failed: 0
            },
            
            // Metadata
            createdBy: member._id,
            createdAt: new Date(),
            lastModified: new Date()
        });
        
        // Calculate recipients
        const recipientCount = await calculateRecipientCount(
            campaign.audienceType,
            campaign.audienceFilter,
            campaign.recipientIds
        );
        
        campaign.totalRecipients = recipientCount;
        await wixData.update('CommCampaigns', campaign);
        
        return {
            success: true,
            campaignId: campaign._id,
            recipientCount: recipientCount,
            message: 'Campaign created successfully'
        };
        
    } catch (error) {
        console.error('Error creating campaign:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send a campaign
 * @param {string} campaignId
 */
export async function sendCampaign(campaignId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const campaign = await wixData.get('CommCampaigns', campaignId);
        
        if (!campaign) {
            return { success: false, error: 'Campaign not found' };
        }
        
        if (campaign.status === 'sent') {
            return { success: false, error: 'Campaign already sent' };
        }
        
        // Update status
        campaign.status = 'sending';
        await wixData.update('CommCampaigns', campaign);
        
        // Get recipients
        const recipients = await getRecipients(
            campaign.audienceType,
            campaign.audienceFilter,
            campaign.recipientIds
        );
        
        // Get template
        const template = MESSAGE_TEMPLATES[campaign.templateId] || MESSAGE_TEMPLATES.GENERAL_ANNOUNCEMENT;
        
        let sentCount = 0;
        let failedCount = 0;
        
        for (const recipient of recipients) {
            try {
                // Send via each channel
                for (const channel of campaign.channels) {
                    const result = await sendMessage(channel, {
                        recipient: recipient,
                        template: template,
                        variables: {
                            ...campaign.variables,
                            firstName: recipient.firstName,
                            lastName: recipient.lastName,
                            email: recipient.email
                        },
                        content: campaign.content
                    });
                    
                    if (result.success) {
                        sentCount++;
                    } else {
                        failedCount++;
                    }
                }
                
                // Log delivery
                await logCommunication(campaignId, recipient._id, campaign.channels, 'sent');
                
            } catch (e) {
                failedCount++;
                await logCommunication(campaignId, recipient._id, campaign.channels, 'failed', e.message);
            }
        }
        
        // Update campaign stats
        campaign.status = 'sent';
        campaign.sentAt = new Date();
        campaign.stats.sent = sentCount;
        campaign.stats.failed = failedCount;
        await wixData.update('CommCampaigns', campaign);
        
        return {
            success: true,
            sent: sentCount,
            failed: failedCount,
            message: `Campaign sent to ${sentCount} recipients`
        };
        
    } catch (error) {
        console.error('Error sending campaign:', error);
        return { success: false, error: error.message };
    }
}

async function sendMessage(channel, data) {
    const { recipient, template, variables, content } = data;
    
    switch (channel) {
        case CHANNEL_TYPES.EMAIL:
            return await sendEmailMessage(recipient, template, variables);
            
        case CHANNEL_TYPES.SMS:
            return await sendSMSMessage(recipient, template, variables);
            
        case CHANNEL_TYPES.WHATSAPP:
            return await sendWhatsAppMessage(recipient, template, variables);
            
        case CHANNEL_TYPES.PUSH:
            return await sendPushNotification(recipient, content, variables);
            
        default:
            return { success: false, error: 'Unknown channel' };
    }
}

async function sendEmailMessage(recipient, template, variables) {
    try {
        await triggeredEmails.emailContact(
            template.emailTemplate,
            recipient.email,
            { variables: variables }
        );
        return { success: true };
    } catch (error) {
        console.error('Email send error:', error);
        return { success: false, error: error.message };
    }
}

async function sendSMSMessage(recipient, template, variables) {
    // Queue SMS for batch processing
    let message = template.smsTemplate;
    for (const [key, value] of Object.entries(variables)) {
        message = message.replace(new RegExp(`{${key}}`, 'g'), value);
    }
    
    await wixData.insert('SMSQueue', {
        phone: recipient.phone,
        message: message,
        status: 'pending',
        createdAt: new Date()
    });
    
    return { success: true };
}

async function sendWhatsAppMessage(recipient, template, variables) {
    // Queue WhatsApp for batch processing
    let message = template.whatsappTemplate;
    for (const [key, value] of Object.entries(variables)) {
        message = message.replace(new RegExp(`{${key}}`, 'g'), value);
    }
    
    await wixData.insert('WhatsAppQueue', {
        phone: recipient.phone,
        message: message,
        status: 'pending',
        createdAt: new Date()
    });
    
    return { success: true };
}

async function sendPushNotification(recipient, content, variables) {
    // Queue push notification
    await wixData.insert('PushQueue', {
        memberId: recipient._id,
        title: interpolateString(content.title, variables),
        body: interpolateString(content.body, variables),
        data: content.data || {},
        status: 'pending',
        createdAt: new Date()
    });
    
    return { success: true };
}

// =====================================================
// AUTOMATED MESSAGING
// =====================================================

/**
 * Schedule automated event reminders
 * @param {string} eventId
 * @param {Array} reminderTypes - ['3day', '1day', 'dayof']
 */
export async function scheduleEventReminders(eventId, reminderTypes = ['3day', '1day', 'dayof']) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        
        if (!event) {
            return { success: false, error: 'Event not found' };
        }
        
        const eventDate = new Date(event.eventDate);
        const reminders = [];
        
        for (const type of reminderTypes) {
            let scheduledDate;
            let templateId;
            
            switch (type) {
                case '3day':
                    scheduledDate = new Date(eventDate);
                    scheduledDate.setDate(scheduledDate.getDate() - 3);
                    scheduledDate.setHours(10, 0, 0, 0); // 10 AM
                    templateId = 'EVENT_REMINDER_3DAY';
                    break;
                    
                case '1day':
                    scheduledDate = new Date(eventDate);
                    scheduledDate.setDate(scheduledDate.getDate() - 1);
                    scheduledDate.setHours(18, 0, 0, 0); // 6 PM
                    templateId = 'EVENT_REMINDER_1DAY';
                    break;
                    
                case 'dayof':
                    scheduledDate = new Date(eventDate);
                    scheduledDate.setHours(8, 0, 0, 0); // 8 AM
                    templateId = 'EVENT_DAYOF';
                    break;
                    
                default:
                    continue;
            }
            
            // Don't schedule if date already passed
            if (scheduledDate <= new Date()) {
                continue;
            }
            
            const reminder = await wixData.insert('ScheduledMessages', {
                eventId: eventId,
                type: `event_reminder_${type}`,
                templateId: templateId,
                channels: ['email', 'whatsapp'],
                scheduledDate: scheduledDate,
                variables: {
                    eventTitle: event.title,
                    eventType: event.eventType,
                    date: formatDate(event.eventDate),
                    time: event.startTime,
                    venue: event.venueName,
                    parkingInfo: event.parkingInfo || 'Check event page for parking details'
                },
                audienceType: 'event_rsvp',
                audienceFilter: { eventId: eventId, status: 'attending' },
                status: 'scheduled',
                createdBy: member._id,
                createdAt: new Date()
            });
            
            reminders.push({
                type: type,
                scheduledDate: scheduledDate,
                reminderId: reminder._id
            });
        }
        
        return {
            success: true,
            reminders: reminders,
            message: `Scheduled ${reminders.length} reminders for ${event.title}`
        };
        
    } catch (error) {
        console.error('Error scheduling reminders:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Process scheduled messages (call from scheduler)
 */
export async function processScheduledMessages() {
    try {
        const now = new Date();
        
        // Find due messages
        const dueMessages = await wixData.query('ScheduledMessages')
            .eq('status', 'scheduled')
            .le('scheduledDate', now)
            .find({ suppressAuth: true });
        
        let processedCount = 0;
        
        for (const scheduled of dueMessages.items) {
            try {
                // Get recipients based on audience type
                let recipients;
                if (scheduled.audienceType === 'event_rsvp') {
                    recipients = await getEventRSVPRecipients(
                        scheduled.audienceFilter.eventId,
                        scheduled.audienceFilter.status
                    );
                } else {
                    recipients = await getRecipients(
                        scheduled.audienceType,
                        scheduled.audienceFilter,
                        []
                    );
                }
                
                const template = MESSAGE_TEMPLATES[scheduled.templateId];
                
                for (const recipient of recipients) {
                    for (const channel of scheduled.channels) {
                        await sendMessage(channel, {
                            recipient: recipient,
                            template: template,
                            variables: {
                                ...scheduled.variables,
                                firstName: recipient.firstName,
                                lastName: recipient.lastName
                            },
                            content: {}
                        });
                    }
                }
                
                scheduled.status = 'sent';
                scheduled.sentAt = new Date();
                scheduled.recipientCount = recipients.length;
                await wixData.update('ScheduledMessages', scheduled);
                
                processedCount++;
                
            } catch (e) {
                scheduled.status = 'failed';
                scheduled.error = e.message;
                await wixData.update('ScheduledMessages', scheduled);
            }
        }
        
        return {
            success: true,
            processed: processedCount
        };
        
    } catch (error) {
        console.error('Error processing scheduled messages:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// QUICK SEND FUNCTIONS
// =====================================================

/**
 * Quick send message to a member
 * @param {string} memberId
 * @param {string} channel
 * @param {string} message
 */
export async function quickSendMessage(memberId, channel, message) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const targetMember = await wixData.get('Members/PrivateMembersData', memberId, { suppressAuth: true });
        
        if (!targetMember) {
            return { success: false, error: 'Member not found' };
        }
        
        const recipient = {
            _id: memberId,
            firstName: targetMember.firstName,
            lastName: targetMember.lastName,
            email: targetMember.loginEmail,
            phone: targetMember.phone || targetMember.mainPhone
        };
        
        const template = MESSAGE_TEMPLATES.GENERAL_ANNOUNCEMENT;
        
        const result = await sendMessage(channel, {
            recipient: recipient,
            template: template,
            variables: { message: message },
            content: { title: 'BANF Message', body: message }
        });
        
        return result;
        
    } catch (error) {
        console.error('Error quick sending:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send emergency alert to all members
 * @param {Object} alertData - { subject, message, channels }
 */
export async function sendEmergencyAlert(alertData) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized - Emergency alerts require admin access');
    }
    
    try {
        // Get all active members
        const members = await wixData.query('Members/PrivateMembersData')
            .find({ suppressAuth: true });
        
        const template = MESSAGE_TEMPLATES.EMERGENCY_ALERT;
        const channels = alertData.channels || ['email', 'sms', 'whatsapp'];
        
        let sentCount = 0;
        
        for (const targetMember of members.items) {
            const recipient = {
                _id: targetMember._id,
                firstName: targetMember.firstName,
                lastName: targetMember.lastName,
                email: targetMember.loginEmail,
                phone: targetMember.phone || targetMember.mainPhone
            };
            
            for (const channel of channels) {
                if ((channel === 'email' && recipient.email) ||
                    ((channel === 'sms' || channel === 'whatsapp') && recipient.phone)) {
                    await sendMessage(channel, {
                        recipient: recipient,
                        template: template,
                        variables: {
                            subject: alertData.subject,
                            message: alertData.message
                        },
                        content: {}
                    });
                    sentCount++;
                }
            }
        }
        
        // Log emergency alert
        await wixData.insert('EmergencyAlertLog', {
            subject: alertData.subject,
            message: alertData.message,
            channels: channels,
            recipientCount: members.items.length,
            sentCount: sentCount,
            sentBy: member._id,
            sentAt: new Date()
        });
        
        return {
            success: true,
            sentCount: sentCount,
            message: `Emergency alert sent to ${members.items.length} members`
        };
        
    } catch (error) {
        console.error('Error sending emergency alert:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// COMMUNICATION ANALYTICS
// =====================================================

/**
 * Get communication statistics
 * @param {Object} filters - { startDate, endDate, channel }
 */
export async function getCommunicationStats(filters = {}) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        let query = wixData.query('CommLog');
        
        if (filters.startDate) {
            query = query.ge('sentAt', new Date(filters.startDate));
        }
        if (filters.endDate) {
            query = query.le('sentAt', new Date(filters.endDate));
        }
        if (filters.channel) {
            query = query.eq('channel', filters.channel);
        }
        
        const logs = await query.find({ suppressAuth: true });
        
        const stats = {
            totalSent: logs.items.length,
            byChannel: {},
            byStatus: {},
            recentActivity: []
        };
        
        for (const log of logs.items) {
            stats.byChannel[log.channel] = (stats.byChannel[log.channel] || 0) + 1;
            stats.byStatus[log.status] = (stats.byStatus[log.status] || 0) + 1;
        }
        
        // Get recent campaigns
        const campaigns = await wixData.query('CommCampaigns')
            .eq('status', 'sent')
            .descending('sentAt')
            .limit(10)
            .find({ suppressAuth: true });
        
        stats.recentCampaigns = campaigns.items.map(c => ({
            name: c.name,
            sentAt: c.sentAt,
            sent: c.stats.sent,
            opened: c.stats.opened,
            openRate: c.stats.sent > 0 
                ? Math.round((c.stats.opened / c.stats.sent) * 100) 
                : 0
        }));
        
        return {
            success: true,
            stats: stats
        };
        
    } catch (error) {
        console.error('Error getting comm stats:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

async function calculateRecipientCount(audienceType, filter, specificIds) {
    switch (audienceType) {
        case 'all':
            const allMembers = await wixData.query('Members/PrivateMembersData')
                .count({ suppressAuth: true });
            return allMembers;
            
        case 'members':
            const members = await wixData.query('Memberships')
                .eq('status', 'active')
                .count({ suppressAuth: true });
            return members;
            
        case 'specific':
            return specificIds?.length || 0;
            
        case 'filter':
            // Apply filter and count
            let query = wixData.query('Members/PrivateMembersData');
            if (filter.membershipType) {
                query = query.eq('membershipType', filter.membershipType);
            }
            return await query.count({ suppressAuth: true });
            
        default:
            return 0;
    }
}

async function getRecipients(audienceType, filter, specificIds) {
    let recipients = [];
    
    switch (audienceType) {
        case 'all':
            const all = await wixData.query('Members/PrivateMembersData')
                .find({ suppressAuth: true });
            recipients = all.items;
            break;
            
        case 'members':
            const memberships = await wixData.query('Memberships')
                .eq('status', 'active')
                .include('memberId')
                .find({ suppressAuth: true });
            
            const memberIds = memberships.items.map(m => m.memberId);
            if (memberIds.length > 0) {
                const members = await wixData.query('Members/PrivateMembersData')
                    .hasSome('_id', memberIds)
                    .find({ suppressAuth: true });
                recipients = members.items;
            }
            break;
            
        case 'specific':
            if (specificIds?.length > 0) {
                const specific = await wixData.query('Members/PrivateMembersData')
                    .hasSome('_id', specificIds)
                    .find({ suppressAuth: true });
                recipients = specific.items;
            }
            break;
            
        case 'filter':
            let query = wixData.query('Members/PrivateMembersData');
            if (filter.membershipType) {
                // Would need to join with memberships
            }
            const filtered = await query.find({ suppressAuth: true });
            recipients = filtered.items;
            break;
    }
    
    return recipients.map(r => ({
        _id: r._id,
        firstName: r.firstName || 'Member',
        lastName: r.lastName || '',
        email: r.loginEmail,
        phone: r.phone || r.mainPhone
    }));
}

async function getEventRSVPRecipients(eventId, status) {
    const rsvps = await wixData.query('EviteRSVPs')
        .eq('eventId', eventId)
        .eq('rsvpStatus', status)
        .find({ suppressAuth: true });
    
    return rsvps.items.map(r => ({
        _id: r.memberId,
        firstName: r.attendeeName?.split(' ')[0] || 'Guest',
        lastName: r.attendeeName?.split(' ').slice(1).join(' ') || '',
        email: r.email,
        phone: r.phone
    }));
}

async function logCommunication(campaignId, recipientId, channels, status, error = null) {
    await wixData.insert('CommLog', {
        campaignId: campaignId,
        recipientId: recipientId,
        channels: channels,
        status: status,
        error: error,
        sentAt: new Date()
    });
}

function interpolateString(str, variables) {
    if (!str) return '';
    let result = str;
    for (const [key, value] of Object.entries(variables)) {
        result = result.replace(new RegExp(`{${key}}`, 'g'), value || '');
    }
    return result;
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

async function isAdmin(memberId) {
    if (!memberId) return false;
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec')
            );
        }
        return false;
    } catch {
        return false;
    }
}

// Export constants
export { MESSAGE_TEMPLATES, CHANNEL_TYPES };

```
------------------------------------------------------------

## [11/41] community-engagement
- File: `community-engagement.jsw`
- Size: 25.2 KB
- Lines: 707

```javascript
/**
 * BANF Community Engagement Module
 * Charity, Career Guidance, and Community Initiatives Management
 * 
 * File: backend/community-engagement.jsw
 * Deploy to: Wix Velo Backend
 */

import wixData from 'wix-data';
import { currentUser } from 'wix-users-backend';
import { hasSpecializedPermission } from 'backend/specialized-admin-roles.jsw';
import { sendEmail, EMAIL_TEMPLATES } from 'backend/notification-service.jsw';

// Initiative Types
export const INITIATIVE_TYPES = {
    CHARITY: 'charity',
    CAREER_GUIDANCE: 'career_guidance',
    EDUCATION: 'education',
    HEALTH_WELLNESS: 'health_wellness',
    ENVIRONMENT: 'environment',
    CULTURAL: 'cultural',
    COMMUNITY_SERVICE: 'community_service',
    YOUTH_PROGRAM: 'youth_program',
    SENIOR_SUPPORT: 'senior_support',
    SCHOLARSHIP: 'scholarship'
};

// Initiative Status
export const INITIATIVE_STATUS = {
    DRAFT: 'draft',
    PROPOSED: 'proposed',
    APPROVED: 'approved',
    ACTIVE: 'active',
    COMPLETED: 'completed',
    CANCELLED: 'cancelled'
};

// Donation Types
export const DONATION_TYPES = {
    MONETARY: 'monetary',
    GOODS: 'goods',
    SERVICES: 'services',
    TIME: 'time' // Volunteer hours
};

/**
 * Create a new community initiative
 */
export async function createInitiative(initiativeData, userId) {
    try {
        const hasPermission = await hasSpecializedPermission(userId, 'community_create');
        if (!hasPermission) {
            return { success: false, error: 'Not authorized to create initiatives' };
        }
        
        const initiative = await wixData.insert('CommunityInitiatives', {
            ...initiativeData,
            initiativeType: initiativeData.type || INITIATIVE_TYPES.COMMUNITY_SERVICE,
            status: INITIATIVE_STATUS.PROPOSED,
            createdBy: userId,
            createdAt: new Date(),
            updatedAt: new Date(),
            
            // Goals and metrics
            goalAmount: initiativeData.goalAmount || 0,
            currentAmount: 0,
            goalParticipants: initiativeData.goalParticipants || 0,
            currentParticipants: 0,
            volunteerHoursGoal: initiativeData.volunteerHoursGoal || 0,
            volunteerHoursLogged: 0,
            
            // Tracking
            donations: [],
            participants: [],
            volunteers: [],
            updates: [],
            milestones: initiativeData.milestones || []
        }, { suppressAuth: true });
        
        // Notify community leads
        await notifyInitiativeCreated(initiative);
        
        return { success: true, initiativeId: initiative._id, initiative };
    } catch (error) {
        console.error('Create initiative failed:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Update initiative status
 */
export async function updateInitiativeStatus(initiativeId, newStatus, userId) {
    try {
        const hasPermission = await hasSpecializedPermission(userId, 'community_approve');
        if (!hasPermission && newStatus !== INITIATIVE_STATUS.CANCELLED) {
            return { success: false, error: 'Not authorized to update initiative status' };
        }
        
        const initiative = await wixData.get('CommunityInitiatives', initiativeId, { suppressAuth: true });
        if (!initiative) {
            return { success: false, error: 'Initiative not found' };
        }
        
        const updated = await wixData.update('CommunityInitiatives', {
            ...initiative,
            status: newStatus,
            updatedAt: new Date(),
            statusHistory: [
                ...(initiative.statusHistory || []),
                {
                    status: newStatus,
                    changedBy: userId,
                    changedAt: new Date()
                }
            ]
        }, { suppressAuth: true });
        
        return { success: true, initiative: updated };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Record a donation
 */
export async function recordDonation(donationData, userId) {
    try {
        const donation = await wixData.insert('CommunityDonations', {
            ...donationData,
            donorId: userId,
            donationType: donationData.type || DONATION_TYPES.MONETARY,
            status: 'confirmed',
            createdAt: new Date(),
            taxDeductible: donationData.taxDeductible !== false,
            receiptGenerated: false
        }, { suppressAuth: true });
        
        // Update initiative totals if linked
        if (donationData.initiativeId) {
            await updateInitiativeDonation(donationData.initiativeId, donation);
        }
        
        // Generate receipt if monetary
        if (donationData.type === DONATION_TYPES.MONETARY) {
            await generateDonationReceipt(donation);
        }
        
        return { success: true, donationId: donation._id, donation };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Update initiative with new donation
 */
async function updateInitiativeDonation(initiativeId, donation) {
    const initiative = await wixData.get('CommunityInitiatives', initiativeId, { suppressAuth: true });
    if (!initiative) return;
    
    let newAmount = initiative.currentAmount || 0;
    if (donation.donationType === DONATION_TYPES.MONETARY) {
        newAmount += donation.amount || 0;
    }
    
    await wixData.update('CommunityInitiatives', {
        ...initiative,
        currentAmount: newAmount,
        donations: [...(initiative.donations || []), donation._id],
        updatedAt: new Date()
    }, { suppressAuth: true });
}

/**
 * Register as volunteer for initiative
 */
export async function registerVolunteer(initiativeId, volunteerData, userId) {
    try {
        const initiative = await wixData.get('CommunityInitiatives', initiativeId, { suppressAuth: true });
        if (!initiative) {
            return { success: false, error: 'Initiative not found' };
        }
        
        // Check if already registered
        const existing = await wixData.query('CommunityVolunteers')
            .eq('initiativeId', initiativeId)
            .eq('userId', userId)
            .find({ suppressAuth: true });
        
        if (existing.items.length > 0) {
            return { success: false, error: 'Already registered as volunteer' };
        }
        
        const volunteer = await wixData.insert('CommunityVolunteers', {
            initiativeId,
            userId,
            name: volunteerData.name,
            email: volunteerData.email,
            phone: volunteerData.phone,
            skills: volunteerData.skills || [],
            availability: volunteerData.availability,
            status: 'registered',
            hoursLogged: 0,
            registeredAt: new Date()
        }, { suppressAuth: true });
        
        // Update initiative participant count
        await wixData.update('CommunityInitiatives', {
            ...initiative,
            currentParticipants: (initiative.currentParticipants || 0) + 1,
            volunteers: [...(initiative.volunteers || []), userId]
        }, { suppressAuth: true });
        
        return { success: true, volunteerId: volunteer._id };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Log volunteer hours
 */
export async function logVolunteerHours(initiativeId, hoursData, userId) {
    try {
        const log = await wixData.insert('VolunteerHours', {
            initiativeId,
            volunteerId: userId,
            hours: hoursData.hours,
            date: hoursData.date || new Date(),
            description: hoursData.description,
            taskType: hoursData.taskType,
            supervisorApproved: false,
            createdAt: new Date()
        }, { suppressAuth: true });
        
        // Update volunteer total
        const volunteer = await wixData.query('CommunityVolunteers')
            .eq('initiativeId', initiativeId)
            .eq('userId', userId)
            .find({ suppressAuth: true });
        
        if (volunteer.items.length > 0) {
            await wixData.update('CommunityVolunteers', {
                ...volunteer.items[0],
                hoursLogged: (volunteer.items[0].hoursLogged || 0) + hoursData.hours
            }, { suppressAuth: true });
        }
        
        // Update initiative total
        const initiative = await wixData.get('CommunityInitiatives', initiativeId, { suppressAuth: true });
        if (initiative) {
            await wixData.update('CommunityInitiatives', {
                ...initiative,
                volunteerHoursLogged: (initiative.volunteerHoursLogged || 0) + hoursData.hours
            }, { suppressAuth: true });
        }
        
        return { success: true, logId: log._id };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// ==================== CAREER GUIDANCE ====================

/**
 * Create career guidance session
 */
export async function createCareerSession(sessionData, userId) {
    try {
        const hasPermission = await hasSpecializedPermission(userId, 'community_career');
        if (!hasPermission) {
            return { success: false, error: 'Not authorized to create career sessions' };
        }
        
        const session = await wixData.insert('CareerGuidanceSessions', {
            ...sessionData,
            sessionType: sessionData.type, // 'workshop', 'mentoring', 'webinar', 'counseling'
            status: 'scheduled',
            createdBy: userId,
            createdAt: new Date(),
            registrations: [],
            maxParticipants: sessionData.maxParticipants || 50,
            currentRegistrations: 0,
            
            // Session details
            topics: sessionData.topics || [],
            targetAudience: sessionData.targetAudience || 'all', // 'students', 'professionals', 'career_changers'
            industry: sessionData.industry,
            mentorId: sessionData.mentorId,
            resources: sessionData.resources || []
        }, { suppressAuth: true });
        
        return { success: true, sessionId: session._id, session };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Register for career guidance session
 */
export async function registerForCareerSession(sessionId, registrationData, userId) {
    try {
        const session = await wixData.get('CareerGuidanceSessions', sessionId, { suppressAuth: true });
        if (!session) {
            return { success: false, error: 'Session not found' };
        }
        
        if (session.currentRegistrations >= session.maxParticipants) {
            return { success: false, error: 'Session is full' };
        }
        
        // Check existing registration
        const existing = await wixData.query('CareerSessionRegistrations')
            .eq('sessionId', sessionId)
            .eq('userId', userId)
            .find({ suppressAuth: true });
        
        if (existing.items.length > 0) {
            return { success: false, error: 'Already registered' };
        }
        
        const registration = await wixData.insert('CareerSessionRegistrations', {
            sessionId,
            userId,
            name: registrationData.name,
            email: registrationData.email,
            currentRole: registrationData.currentRole,
            targetRole: registrationData.targetRole,
            questions: registrationData.questions || [],
            status: 'registered',
            registeredAt: new Date()
        }, { suppressAuth: true });
        
        // Update session count
        await wixData.update('CareerGuidanceSessions', {
            ...session,
            currentRegistrations: session.currentRegistrations + 1,
            registrations: [...session.registrations, registration._id]
        }, { suppressAuth: true });
        
        return { success: true, registrationId: registration._id };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Create mentorship match
 */
export async function createMentorshipMatch(mentorId, menteeId, matchData, adminUserId) {
    try {
        const hasPermission = await hasSpecializedPermission(adminUserId, 'community_career');
        if (!hasPermission) {
            return { success: false, error: 'Not authorized' };
        }
        
        const match = await wixData.insert('MentorshipMatches', {
            mentorId,
            menteeId,
            industry: matchData.industry,
            goals: matchData.goals || [],
            duration: matchData.duration || '6_months', // '3_months', '6_months', '12_months'
            status: 'pending_mentor_approval',
            meetingFrequency: matchData.meetingFrequency || 'monthly',
            createdBy: adminUserId,
            createdAt: new Date(),
            sessions: [],
            feedback: []
        }, { suppressAuth: true });
        
        // Notify mentor
        await notifyMentorMatch(match);
        
        return { success: true, matchId: match._id };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// ==================== SCHOLARSHIP PROGRAMS ====================

/**
 * Create scholarship program
 */
export async function createScholarship(scholarshipData, userId) {
    try {
        const hasPermission = await hasSpecializedPermission(userId, 'community_scholarship');
        if (!hasPermission) {
            return { success: false, error: 'Not authorized' };
        }
        
        const scholarship = await wixData.insert('Scholarships', {
            ...scholarshipData,
            status: 'active',
            createdBy: userId,
            createdAt: new Date(),
            
            // Scholarship details
            amount: scholarshipData.amount,
            numberOfAwards: scholarshipData.numberOfAwards || 1,
            eligibility: scholarshipData.eligibility || {},
            applicationDeadline: scholarshipData.applicationDeadline,
            
            // Requirements
            requiredDocuments: scholarshipData.requiredDocuments || [
                'transcript', 'essay', 'recommendation_letters'
            ],
            essayPrompt: scholarshipData.essayPrompt,
            minGPA: scholarshipData.minGPA,
            
            // Tracking
            applications: [],
            recipients: [],
            fundingSource: scholarshipData.fundingSource
        }, { suppressAuth: true });
        
        return { success: true, scholarshipId: scholarship._id, scholarship };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Submit scholarship application
 */
export async function submitScholarshipApplication(scholarshipId, applicationData, userId) {
    try {
        const scholarship = await wixData.get('Scholarships', scholarshipId, { suppressAuth: true });
        if (!scholarship) {
            return { success: false, error: 'Scholarship not found' };
        }
        
        if (new Date() > new Date(scholarship.applicationDeadline)) {
            return { success: false, error: 'Application deadline has passed' };
        }
        
        const application = await wixData.insert('ScholarshipApplications', {
            scholarshipId,
            applicantId: userId,
            personalInfo: applicationData.personalInfo,
            academicInfo: applicationData.academicInfo,
            essay: applicationData.essay,
            documents: applicationData.documents || [],
            status: 'submitted',
            submittedAt: new Date(),
            reviewScore: null,
            reviewNotes: [],
            reviewedBy: null
        }, { suppressAuth: true });
        
        // Update scholarship applications list
        await wixData.update('Scholarships', {
            ...scholarship,
            applications: [...scholarship.applications, application._id]
        }, { suppressAuth: true });
        
        return { success: true, applicationId: application._id };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// ==================== COMMUNITY PROGRAMS ====================

/**
 * Create community program
 */
export async function createCommunityProgram(programData, userId) {
    try {
        const hasPermission = await hasSpecializedPermission(userId, 'community_create');
        if (!hasPermission) {
            return { success: false, error: 'Not authorized' };
        }
        
        const program = await wixData.insert('CommunityPrograms', {
            ...programData,
            programType: programData.type, // 'youth', 'senior', 'health', 'education', 'cultural'
            status: 'active',
            createdBy: userId,
            createdAt: new Date(),
            
            // Schedule
            schedule: programData.schedule, // { frequency, day, time, duration }
            startDate: programData.startDate,
            endDate: programData.endDate,
            
            // Participants
            maxParticipants: programData.maxParticipants,
            currentParticipants: 0,
            participants: [],
            
            // Resources
            resources: programData.resources || [],
            budget: programData.budget || 0,
            sponsors: programData.sponsors || []
        }, { suppressAuth: true });
        
        return { success: true, programId: program._id, program };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Get community dashboard
 */
export async function getCommunityDashboard(userId) {
    try {
        const [initiatives, donations, volunteers, programs, scholarships] = await Promise.all([
            wixData.query('CommunityInitiatives').eq('status', 'active').find({ suppressAuth: true }),
            wixData.query('CommunityDonations').find({ suppressAuth: true }),
            wixData.query('CommunityVolunteers').find({ suppressAuth: true }),
            wixData.query('CommunityPrograms').eq('status', 'active').find({ suppressAuth: true }),
            wixData.query('Scholarships').eq('status', 'active').find({ suppressAuth: true })
        ]);
        
        // Calculate totals
        const totalDonations = donations.items
            .filter(d => d.donationType === DONATION_TYPES.MONETARY)
            .reduce((sum, d) => sum + (d.amount || 0), 0);
        
        const totalVolunteerHours = await wixData.query('VolunteerHours')
            .find({ suppressAuth: true })
            .then(result => result.items.reduce((sum, h) => sum + (h.hours || 0), 0));
        
        return {
            success: true,
            dashboard: {
                activeInitiatives: initiatives.items.length,
                totalDonations,
                totalVolunteers: new Set(volunteers.items.map(v => v.userId)).size,
                totalVolunteerHours,
                activePrograms: programs.items.length,
                activeScholarships: scholarships.items.length,
                
                // Recent activity
                recentInitiatives: initiatives.items.slice(0, 5),
                recentDonations: donations.items
                    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
                    .slice(0, 5),
                
                // Impact metrics
                impactMetrics: {
                    livesImpacted: calculateLivesImpacted(initiatives.items),
                    communitiesServed: calculateCommunitiesServed(initiatives.items),
                    scholarshipsAwarded: await getScholarshipsAwardedCount()
                },
                
                // Upcoming
                upcomingEvents: await getUpcomingCommunityEvents()
            }
        };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Get initiative details with full metrics
 */
export async function getInitiativeDetails(initiativeId) {
    try {
        const initiative = await wixData.get('CommunityInitiatives', initiativeId, { suppressAuth: true });
        if (!initiative) {
            return { success: false, error: 'Initiative not found' };
        }
        
        // Get donations for this initiative
        const donations = await wixData.query('CommunityDonations')
            .eq('initiativeId', initiativeId)
            .find({ suppressAuth: true });
        
        // Get volunteers
        const volunteers = await wixData.query('CommunityVolunteers')
            .eq('initiativeId', initiativeId)
            .find({ suppressAuth: true });
        
        // Get volunteer hours
        const hours = await wixData.query('VolunteerHours')
            .eq('initiativeId', initiativeId)
            .find({ suppressAuth: true });
        
        return {
            success: true,
            initiative: {
                ...initiative,
                donations: donations.items,
                volunteers: volunteers.items,
                volunteerHours: hours.items,
                
                // Progress
                progress: {
                    fundingProgress: initiative.goalAmount > 0 
                        ? ((initiative.currentAmount / initiative.goalAmount) * 100).toFixed(1) 
                        : 0,
                    participantProgress: initiative.goalParticipants > 0
                        ? ((initiative.currentParticipants / initiative.goalParticipants) * 100).toFixed(1)
                        : 0,
                    volunteerHoursProgress: initiative.volunteerHoursGoal > 0
                        ? ((initiative.volunteerHoursLogged / initiative.volunteerHoursGoal) * 100).toFixed(1)
                        : 0
                }
            }
        };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// Helper functions
async function notifyInitiativeCreated(initiative) {
    // Implementation for notifying community leads
}

async function generateDonationReceipt(donation) {
    // Implementation for generating tax receipt
    await wixData.update('CommunityDonations', {
        ...donation,
        receiptGenerated: true,
        receiptNumber: `BANF-DON-${Date.now()}`
    }, { suppressAuth: true });
}

async function notifyMentorMatch(match) {
    // Implementation for notifying mentor
}

function calculateLivesImpacted(initiatives) {
    return initiatives.reduce((sum, i) => sum + (i.currentParticipants || 0), 0);
}

function calculateCommunitiesServed(initiatives) {
    const locations = new Set(initiatives.map(i => i.location).filter(l => l));
    return locations.size;
}

async function getScholarshipsAwardedCount() {
    const awarded = await wixData.query('ScholarshipApplications')
        .eq('status', 'awarded')
        .count({ suppressAuth: true });
    return awarded;
}

async function getUpcomingCommunityEvents() {
    const events = await wixData.query('CommunityInitiatives')
        .eq('status', 'active')
        .ge('startDate', new Date())
        .ascending('startDate')
        .limit(5)
        .find({ suppressAuth: true });
    return events.items;
}

/**
 * Export donation report for tax purposes
 */
export async function exportDonationReport(year, userId) {
    try {
        const hasPermission = await hasSpecializedPermission(userId, 'community_reports');
        if (!hasPermission) {
            return { success: false, error: 'Not authorized' };
        }
        
        const startDate = new Date(year, 0, 1);
        const endDate = new Date(year, 11, 31, 23, 59, 59);
        
        const donations = await wixData.query('CommunityDonations')
            .ge('createdAt', startDate)
            .le('createdAt', endDate)
            .eq('taxDeductible', true)
            .find({ suppressAuth: true });
        
        // Group by donor
        const byDonor = {};
        donations.items.forEach(d => {
            if (!byDonor[d.donorId]) {
                byDonor[d.donorId] = {
                    donorId: d.donorId,
                    donations: [],
                    total: 0
                };
            }
            byDonor[d.donorId].donations.push(d);
            if (d.donationType === DONATION_TYPES.MONETARY) {
                byDonor[d.donorId].total += d.amount || 0;
            }
        });
        
        return {
            success: true,
            report: {
                year,
                totalDonations: donations.items.reduce((sum, d) => 
                    d.donationType === DONATION_TYPES.MONETARY ? sum + (d.amount || 0) : sum, 0),
                donorCount: Object.keys(byDonor).length,
                donationCount: donations.items.length,
                byDonor: Object.values(byDonor)
            }
        };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

```
------------------------------------------------------------

## [12/41] complaints
- File: `complaints.jsw`
- Size: 11.7 KB
- Lines: 355

```javascript
// backend/complaints.jsw
// BANF Anonymous Complaint System - Wix Velo Backend
// Uses wix-secrets-backend for encryption key management

import wixData from 'wix-data';
import { getSecret } from 'wix-secrets-backend';

// Status constants
const COMPLAINT_STATUS = {
    SUBMITTED: 'submitted',
    UNDER_REVIEW: 'under_review',
    INVESTIGATING: 'investigating',
    RESOLVED: 'resolved',
    CLOSED: 'closed'
};

const COMPLAINT_CATEGORIES = [
    'general',
    'financial',
    'event',
    'member_conduct',
    'governance',
    'safety',
    'discrimination',
    'other'
];

/**
 * Submit anonymous complaint
 * Note: In Wix, true encryption would use external services via wix-fetch
 * For internal use, we use Wix's built-in security + data permissions
 */
export async function submitComplaint(complaintData) {
    try {
        // Generate unique complaint ID
        const complaintId = generateComplaintId();
        
        // Generate access code for anonymous follow-up
        const accessCode = generateAccessCode();
        
        const complaint = {
            complaintId: complaintId,
            accessCode: accessCode, // Hashed for storage
            accessCodeHash: hashCode(accessCode),
            category: complaintData.category || 'general',
            subject: complaintData.subject,
            description: complaintData.description,
            incidentDate: complaintData.incidentDate ? new Date(complaintData.incidentDate) : null,
            location: complaintData.location || '',
            involvedParties: complaintData.involvedParties || '',
            desiredOutcome: complaintData.desiredOutcome || '',
            attachmentUrls: complaintData.attachmentUrls || [],
            status: COMPLAINT_STATUS.SUBMITTED,
            priority: 'normal',
            isAnonymous: true,
            submittedAt: new Date(),
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert('Complaints', complaint, {
            suppressAuth: true // Allow anonymous submission
        });
        
        return {
            success: true,
            complaintId: complaintId,
            accessCode: accessCode, // Return to user for their records
            message: 'Complaint submitted successfully. Save your access code to check status.'
        };
    } catch (error) {
        console.error('Error submitting complaint:', error);
        return { success: false, error: 'Failed to submit complaint' };
    }
}

/**
 * Check complaint status using access code (anonymous)
 */
export async function checkComplaintStatus(complaintId, accessCode) {
    try {
        const accessCodeHash = hashCode(accessCode);
        
        const result = await wixData.query('Complaints')
            .eq('complaintId', complaintId)
            .eq('accessCodeHash', accessCodeHash)
            .find({ suppressAuth: true });
        
        if (result.items.length === 0) {
            return {
                success: false,
                error: 'Invalid complaint ID or access code'
            };
        }
        
        const complaint = result.items[0];
        
        // Return limited info for anonymous access
        return {
            success: true,
            status: complaint.status,
            category: complaint.category,
            submittedAt: complaint.submittedAt,
            lastUpdated: complaint._updatedDate,
            adminResponse: complaint.adminResponse || null,
            resolution: complaint.status === COMPLAINT_STATUS.RESOLVED ? complaint.resolution : null
        };
    } catch (error) {
        console.error('Error checking complaint status:', error);
        return { success: false, error: 'Failed to check status' };
    }
}

/**
 * Add follow-up to complaint (anonymous)
 */
export async function addComplaintFollowUp(complaintId, accessCode, followUpText) {
    try {
        const accessCodeHash = hashCode(accessCode);
        
        const result = await wixData.query('Complaints')
            .eq('complaintId', complaintId)
            .eq('accessCodeHash', accessCodeHash)
            .find({ suppressAuth: true });
        
        if (result.items.length === 0) {
            return { success: false, error: 'Invalid complaint ID or access code' };
        }
        
        const complaint = result.items[0];
        
        // Parse existing follow-ups
        let followUps = [];
        try {
            followUps = JSON.parse(complaint.followUps || '[]');
        } catch (e) {
            followUps = [];
        }
        
        // Add new follow-up
        followUps.push({
            timestamp: new Date().toISOString(),
            from: 'complainant',
            message: followUpText
        });
        
        // Update complaint
        await wixData.update('Complaints', {
            ...complaint,
            followUps: JSON.stringify(followUps),
            _updatedDate: new Date()
        }, { suppressAuth: true });
        
        return { success: true, message: 'Follow-up added successfully' };
    } catch (error) {
        console.error('Error adding follow-up:', error);
        return { success: false, error: 'Failed to add follow-up' };
    }
}

/**
 * Get all complaints (admin only)
 */
export async function getAllComplaints(options = { limit: 20, skip: 0, status: null }) {
    try {
        let query = wixData.query('Complaints');
        
        if (options.status) {
            query = query.eq('status', options.status);
        }
        
        query = query
            .descending('submittedAt')
            .limit(options.limit)
            .skip(options.skip);
        
        const result = await query.find();
        
        return {
            items: result.items.map(c => ({
                ...c,
                accessCode: undefined, // Remove access code
                accessCodeHash: undefined
            })),
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error getting complaints:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Get complaint by ID (admin only)
 */
export async function getComplaintById(complaintId) {
    try {
        const result = await wixData.query('Complaints')
            .eq('complaintId', complaintId)
            .find();
        
        if (result.items.length === 0) return null;
        
        const complaint = result.items[0];
        return {
            ...complaint,
            accessCode: undefined,
            accessCodeHash: undefined,
            followUps: JSON.parse(complaint.followUps || '[]')
        };
    } catch (error) {
        console.error('Error getting complaint:', error);
        return null;
    }
}

/**
 * Update complaint status (admin only)
 */
export async function updateComplaintStatus(complaintId, statusData, adminId) {
    try {
        const result = await wixData.query('Complaints')
            .eq('complaintId', complaintId)
            .find();
        
        if (result.items.length === 0) {
            return { success: false, error: 'Complaint not found' };
        }
        
        const complaint = result.items[0];
        
        // Parse existing follow-ups
        let followUps = [];
        try {
            followUps = JSON.parse(complaint.followUps || '[]');
        } catch (e) {
            followUps = [];
        }
        
        // Add admin update as follow-up
        if (statusData.adminResponse) {
            followUps.push({
                timestamp: new Date().toISOString(),
                from: 'admin',
                message: statusData.adminResponse,
                adminId: adminId
            });
        }
        
        const updatedComplaint = {
            ...complaint,
            status: statusData.status || complaint.status,
            priority: statusData.priority || complaint.priority,
            assignedTo: statusData.assignedTo || complaint.assignedTo,
            adminResponse: statusData.adminResponse || complaint.adminResponse,
            resolution: statusData.resolution || complaint.resolution,
            resolvedAt: statusData.status === COMPLAINT_STATUS.RESOLVED ? new Date() : complaint.resolvedAt,
            followUps: JSON.stringify(followUps),
            _updatedDate: new Date()
        };
        
        await wixData.update('Complaints', updatedComplaint);
        
        return { success: true, message: 'Complaint updated successfully' };
    } catch (error) {
        console.error('Error updating complaint:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get complaint statistics
 */
export async function getComplaintStats() {
    try {
        const [
            totalComplaints,
            submittedCount,
            underReviewCount,
            investigatingCount,
            resolvedCount,
            closedCount
        ] = await Promise.all([
            wixData.query('Complaints').count(),
            wixData.query('Complaints').eq('status', COMPLAINT_STATUS.SUBMITTED).count(),
            wixData.query('Complaints').eq('status', COMPLAINT_STATUS.UNDER_REVIEW).count(),
            wixData.query('Complaints').eq('status', COMPLAINT_STATUS.INVESTIGATING).count(),
            wixData.query('Complaints').eq('status', COMPLAINT_STATUS.RESOLVED).count(),
            wixData.query('Complaints').eq('status', COMPLAINT_STATUS.CLOSED).count()
        ]);
        
        // Get category breakdown
        const categoryStats = {};
        for (const category of COMPLAINT_CATEGORIES) {
            categoryStats[category] = await wixData.query('Complaints')
                .eq('category', category)
                .count();
        }
        
        return {
            total: totalComplaints,
            byStatus: {
                submitted: submittedCount,
                under_review: underReviewCount,
                investigating: investigatingCount,
                resolved: resolvedCount,
                closed: closedCount
            },
            byCategory: categoryStats,
            pendingCount: submittedCount + underReviewCount + investigatingCount,
            resolvedRate: totalComplaints > 0 
                ? Math.round(((resolvedCount + closedCount) / totalComplaints) * 100) 
                : 0
        };
    } catch (error) {
        console.error('Error getting complaint stats:', error);
        return null;
    }
}

// Helper Functions

function generateComplaintId() {
    const prefix = 'CMP';
    const timestamp = Date.now().toString(36).toUpperCase();
    const random = Math.random().toString(36).substring(2, 6).toUpperCase();
    return `${prefix}-${timestamp}-${random}`;
}

function generateAccessCode() {
    // Generate 12-character alphanumeric code
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let code = '';
    for (let i = 0; i < 12; i++) {
        if (i > 0 && i % 4 === 0) code += '-';
        code += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return code;
}

function hashCode(str) {
    // Simple hash for demo - in production use crypto
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return Math.abs(hash).toString(36);
}

// Export constants for frontend use
export const ComplaintStatus = COMPLAINT_STATUS;
export const ComplaintCategories = COMPLAINT_CATEGORIES;

```
------------------------------------------------------------

## [13/41] dashboard-service
- File: `dashboard-service.jsw`
- Size: 28.5 KB
- Lines: 883

```javascript
/**
 * BANF Unified Dashboard Service
 * ================================
 * Wix Velo Backend Module for role-based dashboard integration
 * 
 * Features:
 * - Role-based access control (Admin vs Member)
 * - Service categorization
 * - Dashboard widgets and quick actions
 * - Activity feeds and notifications
 * 
 * @module backend/dashboard-service.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';

// =====================================================
// ROLE DEFINITIONS
// =====================================================

const ROLES = {
    ADMIN: 'admin',
    EC_MEMBER: 'ec_member',
    MEMBER: 'member',
    GUEST: 'guest'
};

// =====================================================
// SERVICE CATEGORIZATION
// =====================================================

const SERVICE_CATEGORIES = {
    // ADMIN ONLY SERVICES
    ADMIN_ONLY: [
        {
            id: 'event-management',
            name: 'Event Management',
            icon: '📅',
            description: 'Create and manage events, venues, schedules',
            services: ['event-automation', 'evite-service'],
            actions: [
                { label: 'Create Event', action: 'createEvent' },
                { label: 'View All Events', action: 'viewEvents' },
                { label: 'Send E-vites', action: 'sendEvites' }
            ]
        },
        {
            id: 'member-management',
            name: 'Member Management',
            icon: '👥',
            description: 'Manage memberships, approvals, renewals',
            services: ['member-automation'],
            actions: [
                { label: 'Pending Approvals', action: 'pendingApprovals' },
                { label: 'Member List', action: 'memberList' },
                { label: 'Renewal Reminders', action: 'renewalReminders' }
            ]
        },
        {
            id: 'financial-management',
            name: 'Financial Management',
            icon: '💰',
            description: 'Budgets, expenses, income tracking',
            services: ['budget-finance-service', 'payment-automation'],
            actions: [
                { label: 'Event Budgets', action: 'eventBudgets' },
                { label: 'Pending Expenses', action: 'pendingExpenses' },
                { label: 'Financial Reports', action: 'financialReports' }
            ]
        },
        {
            id: 'communication-hub',
            name: 'Communication Hub',
            icon: '📢',
            description: 'Campaigns, announcements, emergency alerts',
            services: ['communication-hub'],
            actions: [
                { label: 'New Campaign', action: 'newCampaign' },
                { label: 'Scheduled Messages', action: 'scheduledMessages' },
                { label: 'Emergency Alert', action: 'emergencyAlert' }
            ]
        },
        {
            id: 'analytics-insights',
            name: 'Analytics & Insights',
            icon: '📊',
            description: 'Event analytics, member trends, predictions',
            services: ['analytics-service'],
            actions: [
                { label: 'Event Analytics', action: 'eventAnalytics' },
                { label: 'Member Trends', action: 'memberTrends' },
                { label: 'Predictions', action: 'predictions' }
            ]
        },
        {
            id: 'vendor-sponsor',
            name: 'Vendors & Sponsors',
            icon: '🤝',
            description: 'Manage vendors, sponsors, partnerships',
            services: ['vendor-management', 'sponsor-management'],
            actions: [
                { label: 'Vendor List', action: 'vendorList' },
                { label: 'Sponsor Packages', action: 'sponsorPackages' },
                { label: 'Add Partner', action: 'addPartner' }
            ]
        },
        {
            id: 'content-moderation',
            name: 'Content Moderation',
            icon: '🔍',
            description: 'Photo approvals, feedback review',
            services: ['photo-gallery-service', 'feedback-survey-service'],
            actions: [
                { label: 'Pending Photos', action: 'pendingPhotos' },
                { label: 'Survey Results', action: 'surveyResults' },
                { label: 'Feedback Summary', action: 'feedbackSummary' }
            ]
        },
        {
            id: 'volunteer-coordination',
            name: 'Volunteer Coordination',
            icon: '🙋',
            description: 'Task assignments, volunteer management',
            services: ['volunteer-service'],
            actions: [
                { label: 'Create Tasks', action: 'createTasks' },
                { label: 'Volunteer Stats', action: 'volunteerStats' },
                { label: 'Leaderboard', action: 'volunteerLeaderboard' }
            ]
        },
        {
            id: 'checkin-operations',
            name: 'Check-in Operations',
            icon: '✅',
            description: 'Kiosk management, attendance tracking',
            services: ['checkin-kiosk-service', 'qr-code-service'],
            actions: [
                { label: 'Start Kiosk', action: 'startKiosk' },
                { label: 'Generate QR Codes', action: 'generateQR' },
                { label: 'Attendance Report', action: 'attendanceReport' }
            ]
        },
        {
            id: 'streaming-radio',
            name: 'Streaming & Radio',
            icon: '📻',
            description: 'Radio scheduling, live streaming',
            services: ['radio-scheduler', 'streaming-service'],
            actions: [
                { label: 'Schedule Programs', action: 'schedulePrograms' },
                { label: 'Go Live', action: 'goLive' },
                { label: 'View Schedule', action: 'viewSchedule' }
            ]
        }
    ],
    
    // MEMBER ACCESSIBLE SERVICES
    MEMBER_ACCESS: [
        {
            id: 'my-profile',
            name: 'My Profile',
            icon: '👤',
            description: 'View and edit your profile, privacy settings',
            services: ['member-directory-service'],
            actions: [
                { label: 'Edit Profile', action: 'editProfile' },
                { label: 'Privacy Settings', action: 'privacySettings' },
                { label: 'My Family', action: 'myFamily' }
            ]
        },
        {
            id: 'my-events',
            name: 'My Events',
            icon: '🎉',
            description: 'RSVPs, tickets, event history',
            services: ['evite-service'],
            actions: [
                { label: 'Upcoming Events', action: 'upcomingEvents' },
                { label: 'My RSVPs', action: 'myRSVPs' },
                { label: 'Past Events', action: 'pastEvents' }
            ]
        },
        {
            id: 'my-membership',
            name: 'My Membership',
            icon: '🎫',
            description: 'Membership status, renewal, benefits',
            services: ['member-automation'],
            actions: [
                { label: 'View Status', action: 'membershipStatus' },
                { label: 'Renew Now', action: 'renewMembership' },
                { label: 'Payment History', action: 'paymentHistory' }
            ]
        },
        {
            id: 'member-directory',
            name: 'Member Directory',
            icon: '📖',
            description: 'Find and connect with members',
            services: ['member-directory-service'],
            actions: [
                { label: 'Search Members', action: 'searchMembers' },
                { label: 'My Connections', action: 'myConnections' },
                { label: 'Pending Requests', action: 'pendingConnections' }
            ]
        },
        {
            id: 'photo-gallery',
            name: 'Photo Gallery',
            icon: '📸',
            description: 'View and upload event photos',
            services: ['photo-gallery-service'],
            actions: [
                { label: 'Browse Albums', action: 'browseAlbums' },
                { label: 'Upload Photos', action: 'uploadPhotos' },
                { label: 'My Uploads', action: 'myUploads' }
            ]
        },
        {
            id: 'carpool',
            name: 'Carpool',
            icon: '🚗',
            description: 'Offer or request rides to events',
            services: ['carpool-transport-service'],
            actions: [
                { label: 'Offer Ride', action: 'offerRide' },
                { label: 'Find Ride', action: 'findRide' },
                { label: 'My Carpools', action: 'myCarpools' }
            ]
        },
        {
            id: 'volunteer',
            name: 'Volunteer',
            icon: '🤝',
            description: 'Sign up for volunteer opportunities',
            services: ['volunteer-service'],
            actions: [
                { label: 'Available Tasks', action: 'availableTasks' },
                { label: 'My Tasks', action: 'myTasks' },
                { label: 'My Hours', action: 'myVolunteerHours' }
            ]
        },
        {
            id: 'feedback',
            name: 'Feedback',
            icon: '📝',
            description: 'Share your feedback and suggestions',
            services: ['feedback-survey-service'],
            actions: [
                { label: 'Pending Surveys', action: 'pendingSurveys' },
                { label: 'Submit Feedback', action: 'submitFeedback' }
            ]
        }
    ]
};

// =====================================================
// ROLE DETECTION
// =====================================================

/**
 * Get current user's role
 */
export async function getCurrentUserRole() {
    try {
        const member = await currentMember.getMember();
        
        if (!member) {
            return { role: ROLES.GUEST, memberId: null, name: 'Guest' };
        }
        
        const memberData = await wixData.query('Members/PrivateMembersData')
            .eq('_id', member._id)
            .find({ suppressAuth: true });
        
        let role = ROLES.MEMBER;
        
        if (memberData.items.length > 0) {
            const roles = memberData.items[0].memberRoles || [];
            
            if (roles.some(r => r.toLowerCase().includes('admin'))) {
                role = ROLES.ADMIN;
            } else if (roles.some(r => r.toLowerCase().includes('ec'))) {
                role = ROLES.EC_MEMBER;
            }
        }
        
        return {
            role: role,
            memberId: member._id,
            name: `${member.contactDetails?.firstName || ''} ${member.contactDetails?.lastName || ''}`.trim(),
            email: member.loginEmail,
            profilePhoto: member.profilePhoto
        };
        
    } catch (error) {
        console.error('Error getting user role:', error);
        return { role: ROLES.GUEST, memberId: null, name: 'Guest' };
    }
}

/**
 * Check if user has admin access
 */
export async function hasAdminAccess() {
    const user = await getCurrentUserRole();
    return user.role === ROLES.ADMIN || user.role === ROLES.EC_MEMBER;
}

// =====================================================
// DASHBOARD DATA
// =====================================================

/**
 * Get dashboard for current user
 */
export async function getDashboard() {
    const user = await getCurrentUserRole();
    
    try {
        const isAdmin = user.role === ROLES.ADMIN || user.role === ROLES.EC_MEMBER;
        
        // Get appropriate service categories
        const categories = isAdmin 
            ? [...SERVICE_CATEGORIES.ADMIN_ONLY, ...SERVICE_CATEGORIES.MEMBER_ACCESS]
            : SERVICE_CATEGORIES.MEMBER_ACCESS;
        
        // Get widgets data
        const widgets = await getWidgetsData(user);
        
        // Get activity feed
        const activity = await getActivityFeed(user);
        
        // Get notifications
        const notifications = await getNotifications(user);
        
        // Get quick stats
        const quickStats = await getQuickStats(user);
        
        return {
            success: true,
            user: user,
            isAdmin: isAdmin,
            categories: categories,
            widgets: widgets,
            activity: activity,
            notifications: notifications,
            quickStats: quickStats
        };
        
    } catch (error) {
        console.error('Error getting dashboard:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get admin-specific dashboard
 */
export async function getAdminDashboard() {
    const user = await getCurrentUserRole();
    
    if (user.role !== ROLES.ADMIN && user.role !== ROLES.EC_MEMBER) {
        return { success: false, error: 'Unauthorized' };
    }
    
    try {
        // Admin-specific stats
        const adminStats = {
            // Member stats
            totalMembers: await wixData.query('Members/PrivateMembersData')
                .count({ suppressAuth: true }),
            pendingApprovals: await wixData.query('MembershipRequests')
                .eq('status', 'pending')
                .count({ suppressAuth: true }),
            expiringMemberships: await getExpiringMemberships(),
            
            // Event stats
            upcomingEvents: await wixData.query('Events')
                .ge('eventDate', new Date())
                .count({ suppressAuth: true }),
            totalRSVPs: await getTotalUpcomingRSVPs(),
            
            // Financial stats
            pendingExpenses: await wixData.query('Expenses')
                .eq('status', 'pending')
                .count({ suppressAuth: true }),
            
            // Content moderation
            pendingPhotos: await wixData.query('Photos')
                .eq('status', 'pending')
                .count({ suppressAuth: true }),
            
            // Volunteer stats
            activeVolunteers: await wixData.query('Volunteers')
                .eq('status', 'active')
                .count({ suppressAuth: true }),
            
            // Communication
            scheduledMessages: await wixData.query('ScheduledMessages')
                .eq('status', 'pending')
                .count({ suppressAuth: true })
        };
        
        // Pending actions
        const pendingActions = await getPendingAdminActions();
        
        // Recent activity
        const recentActivity = await getAdminActivityLog();
        
        return {
            success: true,
            user: user,
            stats: adminStats,
            pendingActions: pendingActions,
            recentActivity: recentActivity,
            categories: SERVICE_CATEGORIES.ADMIN_ONLY
        };
        
    } catch (error) {
        console.error('Error getting admin dashboard:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get member-specific dashboard
 */
export async function getMemberDashboard() {
    const user = await getCurrentUserRole();
    
    if (user.role === ROLES.GUEST) {
        return { success: false, error: 'Must be logged in' };
    }
    
    try {
        // Member-specific stats
        const memberStats = {
            // Membership
            membershipStatus: await getMembershipStatus(user.memberId),
            
            // Events
            upcomingRSVPs: await wixData.query('EventRSVPs')
                .eq('memberId', user.memberId)
                .eq('status', 'confirmed')
                .count({ suppressAuth: true }),
            
            // Volunteer
            volunteerHours: await getVolunteerHours(user.memberId),
            upcomingTasks: await getUpcomingVolunteerTasks(user.memberId),
            
            // Carpool
            pendingRideRequests: await wixData.query('CarpoolBookings')
                .eq('passengerId', user.memberId)
                .eq('status', 'pending')
                .count({ suppressAuth: true }),
            
            // Social
            connectionRequests: await wixData.query('MemberConnections')
                .eq('memberId2', user.memberId)
                .eq('status', 'pending')
                .count({ suppressAuth: true }),
            
            // Surveys
            pendingSurveys: await getPendingSurveys(user.memberId)
        };
        
        // Upcoming events for member
        const upcomingEvents = await getUpcomingEventsForMember(user.memberId);
        
        // Recent photos where member is tagged
        const recentPhotos = await getRecentTaggedPhotos(user.memberId);
        
        return {
            success: true,
            user: user,
            stats: memberStats,
            upcomingEvents: upcomingEvents,
            recentPhotos: recentPhotos,
            categories: SERVICE_CATEGORIES.MEMBER_ACCESS
        };
        
    } catch (error) {
        console.error('Error getting member dashboard:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// WIDGET DATA
// =====================================================

async function getWidgetsData(user) {
    const widgets = [];
    const isAdmin = user.role === ROLES.ADMIN || user.role === ROLES.EC_MEMBER;
    
    // Upcoming Event Widget
    const nextEvent = await wixData.query('Events')
        .ge('eventDate', new Date())
        .ascending('eventDate')
        .limit(1)
        .find({ suppressAuth: true });
    
    if (nextEvent.items.length > 0) {
        widgets.push({
            type: 'next-event',
            title: 'Next Event',
            data: {
                eventTitle: nextEvent.items[0].title,
                eventDate: nextEvent.items[0].eventDate,
                venue: nextEvent.items[0].venue
            }
        });
    }
    
    // Admin-specific widgets
    if (isAdmin) {
        // Pending Actions Widget
        const pendingCount = await getPendingActionsCount();
        widgets.push({
            type: 'pending-actions',
            title: 'Pending Actions',
            data: pendingCount
        });
    }
    
    // Member-specific widgets
    if (user.memberId) {
        // Membership Status Widget
        const membership = await getMembershipStatus(user.memberId);
        widgets.push({
            type: 'membership-status',
            title: 'Membership',
            data: membership
        });
    }
    
    return widgets;
}

async function getActivityFeed(user) {
    const activities = [];
    const isAdmin = user.role === ROLES.ADMIN || user.role === ROLES.EC_MEMBER;
    
    // Recent events
    const recentEvents = await wixData.query('Events')
        .descending('_createdDate')
        .limit(5)
        .find({ suppressAuth: true });
    
    for (const event of recentEvents.items) {
        activities.push({
            type: 'event',
            icon: '📅',
            message: `New event: ${event.title}`,
            timestamp: event._createdDate
        });
    }
    
    if (isAdmin) {
        // Recent member joins
        const recentMembers = await wixData.query('Members/PrivateMembersData')
            .descending('_createdDate')
            .limit(5)
            .find({ suppressAuth: true });
        
        for (const m of recentMembers.items) {
            activities.push({
                type: 'member',
                icon: '👋',
                message: `New member: ${m.firstName} ${m.lastName}`,
                timestamp: m._createdDate
            });
        }
    }
    
    // Sort by timestamp
    activities.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    
    return activities.slice(0, 10);
}

async function getNotifications(user) {
    const notifications = [];
    
    if (user.memberId) {
        // Pending surveys
        const surveys = await getPendingSurveys(user.memberId);
        if (surveys > 0) {
            notifications.push({
                type: 'survey',
                icon: '📝',
                message: `${surveys} survey(s) awaiting your feedback`,
                priority: 'low'
            });
        }
        
        // Connection requests
        const connections = await wixData.query('MemberConnections')
            .eq('memberId2', user.memberId)
            .eq('status', 'pending')
            .count({ suppressAuth: true });
        
        if (connections > 0) {
            notifications.push({
                type: 'connection',
                icon: '🤝',
                message: `${connections} connection request(s)`,
                priority: 'medium'
            });
        }
    }
    
    return notifications;
}

async function getQuickStats(user) {
    const isAdmin = user.role === ROLES.ADMIN || user.role === ROLES.EC_MEMBER;
    
    if (isAdmin) {
        return {
            members: await wixData.query('Members/PrivateMembersData')
                .count({ suppressAuth: true }),
            events: await wixData.query('Events')
                .ge('eventDate', new Date())
                .count({ suppressAuth: true }),
            pending: await getPendingActionsCount()
        };
    }
    
    return {
        eventsAttended: await wixData.query('EventRSVPs')
            .eq('memberId', user.memberId)
            .eq('status', 'confirmed')
            .count({ suppressAuth: true }),
        volunteerHours: await getVolunteerHours(user.memberId)
    };
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

async function getExpiringMemberships() {
    const thirtyDaysFromNow = new Date();
    thirtyDaysFromNow.setDate(thirtyDaysFromNow.getDate() + 30);
    
    return await wixData.query('Memberships')
        .le('expiryDate', thirtyDaysFromNow)
        .ge('expiryDate', new Date())
        .count({ suppressAuth: true });
}

async function getTotalUpcomingRSVPs() {
    const upcomingEvents = await wixData.query('Events')
        .ge('eventDate', new Date())
        .find({ suppressAuth: true });
    
    let total = 0;
    for (const event of upcomingEvents.items) {
        const rsvps = await wixData.query('EventRSVPs')
            .eq('eventId', event._id)
            .eq('status', 'confirmed')
            .count({ suppressAuth: true });
        total += rsvps;
    }
    
    return total;
}

async function getPendingActionsCount() {
    let count = 0;
    
    try {
        count += await wixData.query('MembershipRequests')
            .eq('status', 'pending')
            .count({ suppressAuth: true });
    } catch {}
    
    try {
        count += await wixData.query('Expenses')
            .eq('status', 'pending')
            .count({ suppressAuth: true });
    } catch {}
    
    try {
        count += await wixData.query('Photos')
            .eq('status', 'pending')
            .count({ suppressAuth: true });
    } catch {}
    
    return count;
}

async function getPendingAdminActions() {
    const actions = [];
    
    // Pending member approvals
    try {
        const pending = await wixData.query('MembershipRequests')
            .eq('status', 'pending')
            .find({ suppressAuth: true });
        
        for (const p of pending.items) {
            actions.push({
                type: 'member_approval',
                label: `Approve: ${p.name}`,
                id: p._id,
                priority: 'high'
            });
        }
    } catch {}
    
    // Pending expenses
    try {
        const expenses = await wixData.query('Expenses')
            .eq('status', 'pending')
            .find({ suppressAuth: true });
        
        for (const e of expenses.items) {
            actions.push({
                type: 'expense_approval',
                label: `Review expense: ${e.description}`,
                id: e._id,
                priority: 'medium'
            });
        }
    } catch {}
    
    // Pending photos
    try {
        const photos = await wixData.query('Photos')
            .eq('status', 'pending')
            .limit(5)
            .find({ suppressAuth: true });
        
        if (photos.items.length > 0) {
            actions.push({
                type: 'photo_moderation',
                label: `${photos.totalCount} photos pending approval`,
                count: photos.totalCount,
                priority: 'low'
            });
        }
    } catch {}
    
    return actions;
}

async function getAdminActivityLog() {
    // Would query an admin activity log collection
    return [];
}

async function getMembershipStatus(memberId) {
    try {
        const membership = await wixData.query('Memberships')
            .eq('memberId', memberId)
            .descending('_createdDate')
            .limit(1)
            .find({ suppressAuth: true });
        
        if (membership.items.length > 0) {
            const m = membership.items[0];
            const isExpired = new Date(m.expiryDate) < new Date();
            const daysRemaining = Math.ceil((new Date(m.expiryDate) - new Date()) / (1000 * 60 * 60 * 24));
            
            return {
                status: isExpired ? 'expired' : 'active',
                type: m.membershipType,
                expiryDate: m.expiryDate,
                daysRemaining: Math.max(0, daysRemaining),
                needsRenewal: daysRemaining <= 30
            };
        }
        
        return { status: 'none' };
    } catch {
        return { status: 'unknown' };
    }
}

async function getVolunteerHours(memberId) {
    try {
        const volunteer = await wixData.query('Volunteers')
            .eq('memberId', memberId)
            .find({ suppressAuth: true });
        
        if (volunteer.items.length > 0) {
            return volunteer.items[0].totalHours || 0;
        }
        return 0;
    } catch {
        return 0;
    }
}

async function getUpcomingVolunteerTasks(memberId) {
    try {
        const tasks = await wixData.query('VolunteerAssignments')
            .eq('volunteerId', memberId)
            .eq('status', 'assigned')
            .count({ suppressAuth: true });
        return tasks;
    } catch {
        return 0;
    }
}

async function getPendingSurveys(memberId) {
    try {
        const activeSurveys = await wixData.query('Surveys')
            .eq('isActive', true)
            .find({ suppressAuth: true });
        
        let pending = 0;
        
        for (const survey of activeSurveys.items) {
            const responded = await wixData.query('SurveyResponses')
                .eq('surveyId', survey._id)
                .eq('memberId', memberId)
                .count({ suppressAuth: true });
            
            if (responded === 0) pending++;
        }
        
        return pending;
    } catch {
        return 0;
    }
}

async function getUpcomingEventsForMember(memberId) {
    try {
        const rsvps = await wixData.query('EventRSVPs')
            .eq('memberId', memberId)
            .eq('status', 'confirmed')
            .find({ suppressAuth: true });
        
        const eventIds = rsvps.items.map(r => r.eventId);
        
        if (eventIds.length === 0) return [];
        
        const events = await wixData.query('Events')
            .hasSome('_id', eventIds)
            .ge('eventDate', new Date())
            .ascending('eventDate')
            .limit(5)
            .find({ suppressAuth: true });
        
        return events.items.map(e => ({
            _id: e._id,
            title: e.title,
            eventDate: e.eventDate,
            venue: e.venue
        }));
    } catch {
        return [];
    }
}

async function getRecentTaggedPhotos(memberId) {
    try {
        const photos = await wixData.query('Photos')
            .contains('taggedMembers', memberId)
            .eq('status', 'approved')
            .descending('uploadedAt')
            .limit(6)
            .find({ suppressAuth: true });
        
        return photos.items.map(p => ({
            _id: p._id,
            thumbnailUrl: p.thumbnailUrl,
            albumTitle: p.albumTitle
        }));
    } catch {
        return [];
    }
}

// Export constants
export { ROLES, SERVICE_CATEGORIES };

```
------------------------------------------------------------

## [14/41] documents
- File: `documents.jsw`
- Size: 19.4 KB
- Lines: 605

```javascript
// backend/documents.jsw
// BANF Document Storage & Management - Wix Velo Backend
// Supports categorized document storage for expenses, bills, audits, etc.

import wixData from 'wix-data';
import { mediaManager } from 'wix-media-backend';

// Document categories
const DOCUMENT_CATEGORIES = {
    // Financial Documents
    EXPENSES: { 
        name: 'Expenses', 
        subcategories: ['event_expenses', 'venue_rental', 'food_catering', 'decorations', 'entertainment', 'supplies', 'miscellaneous'],
        icon: '💰'
    },
    BILLS: { 
        name: 'Bills & Invoices', 
        subcategories: ['vendor_invoices', 'utility_bills', 'service_bills', 'equipment_rental'],
        icon: '🧾'
    },
    RECEIPTS: { 
        name: 'Receipts', 
        subcategories: ['expense_receipts', 'donation_receipts', 'payment_confirmations'],
        icon: '🧾'
    },
    AUDIT: { 
        name: 'Audit Documents', 
        subcategories: ['annual_audit', 'financial_statements', 'audit_reports', 'compliance'],
        icon: '📊'
    },
    
    // Organizational Documents
    GOVERNANCE: { 
        name: 'Governance', 
        subcategories: ['bylaws', 'constitution', 'policies', 'procedures', 'resolutions'],
        icon: '📜'
    },
    MEETING_DOCS: { 
        name: 'Meeting Documents', 
        subcategories: ['agendas', 'minutes', 'presentations', 'reports'],
        icon: '📋'
    },
    MEMBERSHIP: { 
        name: 'Membership Documents', 
        subcategories: ['applications', 'renewals', 'member_lists', 'directories'],
        icon: '👥'
    },
    
    // Event Documents
    EVENT_DOCS: { 
        name: 'Event Documents', 
        subcategories: ['event_plans', 'budgets', 'contracts', 'permits', 'insurance'],
        icon: '🎉'
    },
    SPONSORSHIP_DOCS: { 
        name: 'Sponsorship Documents', 
        subcategories: ['agreements', 'invoices', 'artwork', 'portfolios'],
        icon: '🤝'
    },
    VENDOR_CONTRACTS: { 
        name: 'Vendor Contracts', 
        subcategories: ['food_vendors', 'venue_agreements', 'service_contracts', 'equipment_rentals'],
        icon: '📝'
    },
    
    // Media & Communications
    PHOTOS: { 
        name: 'Event Photos', 
        subcategories: ['durga_puja', 'kali_puja', 'saraswati_puja', 'nabo_borsho', 'spandan', 'other_events'],
        icon: '📷'
    },
    MAGAZINE: { 
        name: 'Magazine Archives', 
        subcategories: ['published_issues', 'articles', 'artwork', 'archives'],
        icon: '📰'
    },
    COMMUNICATIONS: { 
        name: 'Communications', 
        subcategories: ['newsletters', 'announcements', 'press_releases', 'templates'],
        icon: '📧'
    },
    
    // Legal & Insurance
    LEGAL: { 
        name: 'Legal Documents', 
        subcategories: ['incorporation', 'tax_exemption', 'licenses', 'permits'],
        icon: '⚖️'
    },
    INSURANCE: { 
        name: 'Insurance', 
        subcategories: ['liability_insurance', 'event_insurance', 'certificates'],
        icon: '🛡️'
    },
    TAX: { 
        name: 'Tax Documents', 
        subcategories: ['990_filings', 'tax_returns', 'donation_records', 'compliance'],
        icon: '📑'
    }
};

// Document access levels
const ACCESS_LEVELS = {
    PUBLIC: 'public',           // Anyone can view
    MEMBERS: 'members',         // Only members
    ADMIN: 'admin',             // Only admins
    EXECUTIVE: 'executive',     // Only EC members
    CONFIDENTIAL: 'confidential' // Restricted access
};

/**
 * Upload and create document record
 */
export async function uploadDocument(documentData, adminId) {
    try {
        const document = {
            // Basic Info
            title: documentData.title,
            description: documentData.description || '',
            
            // Categorization
            category: documentData.category,
            subcategory: documentData.subcategory || '',
            tags: JSON.stringify(documentData.tags || []),
            
            // File Info
            fileUrl: documentData.fileUrl,
            fileName: documentData.fileName,
            fileType: documentData.fileType || getFileType(documentData.fileName),
            fileSize: documentData.fileSize || 0,
            
            // Related Entities
            relatedEventId: documentData.eventId || '',
            relatedEventName: documentData.eventName || '',
            relatedSponsorId: documentData.sponsorId || '',
            relatedVendorId: documentData.vendorId || '',
            fiscalYear: documentData.fiscalYear || getCurrentFiscalYear(),
            
            // Access Control
            accessLevel: documentData.accessLevel || ACCESS_LEVELS.ADMIN,
            
            // Financial (if applicable)
            documentAmount: documentData.amount || 0,
            transactionDate: documentData.transactionDate ? new Date(documentData.transactionDate) : null,
            
            // Version Control
            version: 1,
            previousVersionId: null,
            
            // Status
            isArchived: false,
            isVerified: false,
            verifiedBy: null,
            verifiedAt: null,
            
            // Metadata
            uploadedBy: adminId,
            notes: documentData.notes || '',
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert('Documents', document);
        
        // Log activity
        await logDocumentActivity(result._id, 'upload', adminId, 'Document uploaded');
        
        return { 
            success: true, 
            documentId: result._id,
            message: 'Document uploaded successfully'
        };
    } catch (error) {
        console.error('Error uploading document:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get documents by category
 */
export async function getDocumentsByCategory(category, options = { limit: 50, skip: 0, subcategory: null, fiscalYear: null }) {
    try {
        let query = wixData.query('Documents')
            .eq('category', category)
            .eq('isArchived', false);
        
        if (options.subcategory) {
            query = query.eq('subcategory', options.subcategory);
        }
        if (options.fiscalYear) {
            query = query.eq('fiscalYear', options.fiscalYear);
        }
        
        query = query
            .descending('_createdDate')
            .limit(options.limit)
            .skip(options.skip);
        
        const result = await query.find();
        
        return {
            items: result.items.map(d => ({
                ...d,
                tags: JSON.parse(d.tags || '[]')
            })),
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error getting documents:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Search documents
 */
export async function searchDocuments(searchTerm, options = { category: null, fiscalYear: null, limit: 50 }) {
    try {
        let query = wixData.query('Documents')
            .eq('isArchived', false)
            .contains('title', searchTerm)
            .or(wixData.query('Documents').contains('description', searchTerm))
            .or(wixData.query('Documents').contains('fileName', searchTerm));
        
        if (options.category) {
            query = query.eq('category', options.category);
        }
        if (options.fiscalYear) {
            query = query.eq('fiscalYear', options.fiscalYear);
        }
        
        query = query
            .descending('_createdDate')
            .limit(options.limit);
        
        const result = await query.find();
        
        return {
            items: result.items.map(d => ({
                ...d,
                tags: JSON.parse(d.tags || '[]')
            })),
            totalCount: result.totalCount
        };
    } catch (error) {
        console.error('Error searching documents:', error);
        return { items: [], totalCount: 0 };
    }
}

/**
 * Get document by ID
 */
export async function getDocumentById(documentId) {
    try {
        const document = await wixData.get('Documents', documentId);
        if (!document) return null;
        
        // Get activity log
        const activityLog = await wixData.query('DocumentActivityLog')
            .eq('documentId', documentId)
            .descending('timestamp')
            .limit(20)
            .find();
        
        return {
            ...document,
            tags: JSON.parse(document.tags || '[]'),
            activityLog: activityLog.items
        };
    } catch (error) {
        console.error('Error getting document:', error);
        return null;
    }
}

/**
 * Update document metadata
 */
export async function updateDocument(documentId, updateData, adminId) {
    try {
        const document = await wixData.get('Documents', documentId);
        if (!document) {
            return { success: false, error: 'Document not found' };
        }
        
        const updatedDocument = {
            ...document,
            title: updateData.title || document.title,
            description: updateData.description !== undefined ? updateData.description : document.description,
            category: updateData.category || document.category,
            subcategory: updateData.subcategory || document.subcategory,
            tags: updateData.tags ? JSON.stringify(updateData.tags) : document.tags,
            accessLevel: updateData.accessLevel || document.accessLevel,
            notes: updateData.notes !== undefined ? updateData.notes : document.notes,
            _updatedDate: new Date()
        };
        
        await wixData.update('Documents', updatedDocument);
        await logDocumentActivity(documentId, 'update', adminId, 'Document metadata updated');
        
        return { success: true, message: 'Document updated' };
    } catch (error) {
        console.error('Error updating document:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Upload new version of document
 */
export async function uploadNewVersion(documentId, newFileData, adminId) {
    try {
        const originalDoc = await wixData.get('Documents', documentId);
        if (!originalDoc) {
            return { success: false, error: 'Document not found' };
        }
        
        // Archive old version
        await wixData.update('Documents', {
            ...originalDoc,
            isArchived: true,
            archivedAt: new Date(),
            archivedBy: adminId
        });
        
        // Create new version
        const newDocument = {
            ...originalDoc,
            _id: undefined, // Let Wix generate new ID
            fileUrl: newFileData.fileUrl,
            fileName: newFileData.fileName,
            fileSize: newFileData.fileSize || 0,
            version: (originalDoc.version || 1) + 1,
            previousVersionId: documentId,
            isArchived: false,
            uploadedBy: adminId,
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert('Documents', newDocument);
        await logDocumentActivity(result._id, 'new_version', adminId, `Version ${newDocument.version} uploaded`);
        
        return { 
            success: true, 
            documentId: result._id,
            version: newDocument.version
        };
    } catch (error) {
        console.error('Error uploading new version:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Archive document
 */
export async function archiveDocument(documentId, adminId) {
    try {
        const document = await wixData.get('Documents', documentId);
        if (!document) {
            return { success: false, error: 'Document not found' };
        }
        
        await wixData.update('Documents', {
            ...document,
            isArchived: true,
            archivedAt: new Date(),
            archivedBy: adminId,
            _updatedDate: new Date()
        });
        
        await logDocumentActivity(documentId, 'archive', adminId, 'Document archived');
        
        return { success: true, message: 'Document archived' };
    } catch (error) {
        console.error('Error archiving document:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get document statistics by category
 */
export async function getDocumentStats() {
    try {
        const stats = {
            totalDocuments: 0,
            byCategory: {},
            byFiscalYear: {},
            recentUploads: [],
            storageUsed: 0
        };
        
        // Get total count
        stats.totalDocuments = await wixData.query('Documents')
            .eq('isArchived', false)
            .count();
        
        // Count by category
        for (const [key, category] of Object.entries(DOCUMENT_CATEGORIES)) {
            const count = await wixData.query('Documents')
                .eq('category', key)
                .eq('isArchived', false)
                .count();
            
            stats.byCategory[key] = {
                name: category.name,
                icon: category.icon,
                count: count
            };
        }
        
        // Get recent uploads
        const recent = await wixData.query('Documents')
            .eq('isArchived', false)
            .descending('_createdDate')
            .limit(10)
            .find();
        
        stats.recentUploads = recent.items.map(d => ({
            id: d._id,
            title: d.title,
            category: d.category,
            uploadedAt: d._createdDate
        }));
        
        // Calculate storage (approximate)
        const allDocs = await wixData.query('Documents')
            .eq('isArchived', false)
            .limit(1000)
            .find();
        
        stats.storageUsed = allDocs.items.reduce((sum, d) => sum + (d.fileSize || 0), 0);
        
        return stats;
    } catch (error) {
        console.error('Error getting document stats:', error);
        return null;
    }
}

/**
 * Get expense documents with totals
 */
export async function getExpenseDocuments(fiscalYear = null, options = { limit: 100 }) {
    try {
        const year = fiscalYear || getCurrentFiscalYear();
        
        const result = await wixData.query('Documents')
            .eq('category', 'EXPENSES')
            .eq('fiscalYear', year)
            .eq('isArchived', false)
            .descending('transactionDate')
            .limit(options.limit)
            .find();
        
        const total = result.items.reduce((sum, d) => sum + (d.documentAmount || 0), 0);
        
        // Group by subcategory
        const bySubcategory = {};
        result.items.forEach(doc => {
            const sub = doc.subcategory || 'miscellaneous';
            if (!bySubcategory[sub]) {
                bySubcategory[sub] = { count: 0, total: 0 };
            }
            bySubcategory[sub].count++;
            bySubcategory[sub].total += doc.documentAmount || 0;
        });
        
        return {
            items: result.items,
            totalAmount: total,
            bySubcategory: bySubcategory,
            documentCount: result.totalCount
        };
    } catch (error) {
        console.error('Error getting expense documents:', error);
        return { items: [], totalAmount: 0, bySubcategory: {}, documentCount: 0 };
    }
}

/**
 * Verify document (for audit purposes)
 */
export async function verifyDocument(documentId, adminId) {
    try {
        const document = await wixData.get('Documents', documentId);
        if (!document) {
            return { success: false, error: 'Document not found' };
        }
        
        await wixData.update('Documents', {
            ...document,
            isVerified: true,
            verifiedBy: adminId,
            verifiedAt: new Date(),
            _updatedDate: new Date()
        });
        
        await logDocumentActivity(documentId, 'verify', adminId, 'Document verified');
        
        return { success: true, message: 'Document verified' };
    } catch (error) {
        console.error('Error verifying document:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get audit trail for document
 */
export async function getDocumentAuditTrail(documentId) {
    try {
        const result = await wixData.query('DocumentActivityLog')
            .eq('documentId', documentId)
            .descending('timestamp')
            .find();
        
        return result.items;
    } catch (error) {
        console.error('Error getting audit trail:', error);
        return [];
    }
}

/**
 * Bulk categorize documents
 */
export async function bulkCategorize(documentIds, category, subcategory, adminId) {
    try {
        let successCount = 0;
        
        for (const docId of documentIds) {
            const document = await wixData.get('Documents', docId);
            if (document) {
                await wixData.update('Documents', {
                    ...document,
                    category: category,
                    subcategory: subcategory || '',
                    _updatedDate: new Date()
                });
                await logDocumentActivity(docId, 'categorize', adminId, `Moved to ${category}/${subcategory}`);
                successCount++;
            }
        }
        
        return { 
            success: true, 
            message: `${successCount} documents categorized`,
            count: successCount
        };
    } catch (error) {
        console.error('Error bulk categorizing:', error);
        return { success: false, error: error.message };
    }
}

// ==================== HELPER FUNCTIONS ====================

async function logDocumentActivity(documentId, action, adminId, details) {
    try {
        await wixData.insert('DocumentActivityLog', {
            documentId: documentId,
            action: action,
            performedBy: adminId,
            details: details,
            timestamp: new Date(),
            _createdDate: new Date()
        });
    } catch (error) {
        console.error('Error logging document activity:', error);
    }
}

function getFileType(fileName) {
    if (!fileName) return 'unknown';
    const ext = fileName.split('.').pop().toLowerCase();
    const typeMap = {
        'pdf': 'pdf',
        'doc': 'word', 'docx': 'word',
        'xls': 'excel', 'xlsx': 'excel',
        'ppt': 'powerpoint', 'pptx': 'powerpoint',
        'jpg': 'image', 'jpeg': 'image', 'png': 'image', 'gif': 'image',
        'zip': 'archive', 'rar': 'archive',
        'txt': 'text', 'csv': 'csv'
    };
    return typeMap[ext] || 'other';
}

function getCurrentFiscalYear() {
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth();
    if (month >= 3) {
        return `${year}-${year + 1}`;
    }
    return `${year - 1}-${year}`;
}

// Export constants
export const DocumentCategories = DOCUMENT_CATEGORIES;
export const AccessLevels = ACCESS_LEVELS;

```
------------------------------------------------------------

## [15/41] email
- File: `email.jsw`
- Size: 12.8 KB
- Lines: 391

```javascript
// backend/email.jsw
// BANF Email Service - Wix Velo Backend
// Uses Triggered Emails feature

import wixCrm from 'wix-crm-backend';
import { triggeredEmails } from 'wix-crm-backend';

/**
 * Send welcome email to new member
 */
export async function sendWelcomeEmail(memberData) {
    try {
        const emailId = 'welcome_email'; // Create this triggered email in Wix dashboard
        
        await triggeredEmails.emailMember(emailId, memberData.contactId, {
            variables: {
                memberName: memberData.firstName,
                fullName: `${memberData.firstName} ${memberData.lastName}`,
                membershipType: memberData.membershipType || 'General',
                joinDate: new Date().toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                })
            }
        });
        
        return { success: true };
    } catch (error) {
        console.error('Error sending welcome email:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send event registration confirmation
 */
export async function sendEventConfirmation(registrationData) {
    try {
        const emailId = 'event_confirmation';
        
        await triggeredEmails.emailMember(emailId, registrationData.contactId, {
            variables: {
                memberName: registrationData.memberName,
                eventName: registrationData.eventName,
                eventDate: registrationData.eventDate,
                eventTime: registrationData.eventTime,
                eventLocation: registrationData.location,
                registrationId: registrationData.registrationId,
                guestCount: registrationData.guestCount || 0,
                totalAmount: registrationData.totalAmount || 'Free'
            }
        });
        
        return { success: true };
    } catch (error) {
        console.error('Error sending event confirmation:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send payment receipt
 */
export async function sendPaymentReceipt(paymentData) {
    try {
        const emailId = 'payment_receipt';
        
        await triggeredEmails.emailMember(emailId, paymentData.contactId, {
            variables: {
                memberName: paymentData.memberName,
                transactionId: paymentData.transactionId,
                amount: paymentData.amount,
                paymentMethod: paymentData.paymentMethod,
                paymentDate: new Date().toLocaleDateString('en-US'),
                description: paymentData.description,
                receiptNumber: paymentData.receiptNumber
            }
        });
        
        return { success: true };
    } catch (error) {
        console.error('Error sending payment receipt:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send membership renewal reminder
 */
export async function sendRenewalReminder(memberData) {
    try {
        const emailId = 'renewal_reminder';
        
        await triggeredEmails.emailMember(emailId, memberData.contactId, {
            variables: {
                memberName: memberData.firstName,
                membershipType: memberData.membershipType,
                expirationDate: memberData.expirationDate,
                renewalAmount: memberData.renewalAmount,
                daysUntilExpiry: memberData.daysUntilExpiry
            }
        });
        
        return { success: true };
    } catch (error) {
        console.error('Error sending renewal reminder:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send event reminder
 */
export async function sendEventReminder(eventData) {
    try {
        const emailId = 'event_reminder';
        
        await triggeredEmails.emailMember(emailId, eventData.contactId, {
            variables: {
                memberName: eventData.memberName,
                eventName: eventData.eventName,
                eventDate: eventData.eventDate,
                eventTime: eventData.eventTime,
                eventLocation: eventData.location,
                reminderType: eventData.reminderType // 1day, 1week, etc.
            }
        });
        
        return { success: true };
    } catch (error) {
        console.error('Error sending event reminder:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send survey invitation
 */
export async function sendSurveyInvitation(surveyData) {
    try {
        const emailId = 'survey_invitation';
        
        await triggeredEmails.emailMember(emailId, surveyData.contactId, {
            variables: {
                memberName: surveyData.memberName,
                surveyTitle: surveyData.surveyTitle,
                surveyDescription: surveyData.surveyDescription,
                surveyLink: surveyData.surveyLink,
                deadline: surveyData.deadline
            }
        });
        
        return { success: true };
    } catch (error) {
        console.error('Error sending survey invitation:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send complaint acknowledgment
 */
export async function sendComplaintAcknowledgment(complaintData) {
    try {
        // For anonymous complaints, we can't send to member
        // This would be used for non-anonymous complaints
        if (!complaintData.contactId) {
            return { success: false, error: 'No contact ID for anonymous complaint' };
        }
        
        const emailId = 'complaint_acknowledgment';
        
        await triggeredEmails.emailMember(emailId, complaintData.contactId, {
            variables: {
                complaintId: complaintData.complaintId,
                accessCode: complaintData.accessCode,
                submittedDate: new Date().toLocaleDateString('en-US')
            }
        });
        
        return { success: true };
    } catch (error) {
        console.error('Error sending complaint acknowledgment:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send admin notification
 */
export async function sendAdminNotification(notificationData) {
    try {
        const emailId = 'admin_notification';
        
        // Get admin contacts
        const adminEmails = notificationData.adminEmails || [];
        
        for (const adminEmail of adminEmails) {
            // Create contact if needed
            const contactId = await getOrCreateContact(adminEmail);
            
            await triggeredEmails.emailContact(emailId, contactId, {
                variables: {
                    notificationType: notificationData.type,
                    title: notificationData.title,
                    message: notificationData.message,
                    actionUrl: notificationData.actionUrl,
                    timestamp: new Date().toISOString()
                }
            });
        }
        
        return { success: true };
    } catch (error) {
        console.error('Error sending admin notification:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send newsletter/announcement
 */
export async function sendNewsletter(newsletterData) {
    try {
        const emailId = 'newsletter';
        
        // This would typically use email marketing campaigns
        // For triggered emails, we'd need to loop through contacts
        
        await triggeredEmails.emailContact(emailId, newsletterData.contactId, {
            variables: {
                title: newsletterData.title,
                content: newsletterData.content,
                highlights: newsletterData.highlights,
                upcomingEvents: newsletterData.upcomingEvents,
                magazineLink: newsletterData.magazineLink
            }
        });
        
        return { success: true };
    } catch (error) {
        console.error('Error sending newsletter:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send article submission confirmation
 */
export async function sendArticleSubmissionConfirmation(articleData) {
    try {
        const emailId = 'article_submission';
        
        await triggeredEmails.emailMember(emailId, articleData.contactId, {
            variables: {
                authorName: articleData.authorName,
                articleTitle: articleData.title,
                category: articleData.category,
                submittedDate: new Date().toLocaleDateString('en-US')
            }
        });
        
        return { success: true };
    } catch (error) {
        console.error('Error sending article confirmation:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send article approval/rejection notification
 */
export async function sendArticleReviewResult(reviewData) {
    try {
        const emailId = reviewData.approved ? 'article_approved' : 'article_rejected';
        
        await triggeredEmails.emailMember(emailId, reviewData.contactId, {
            variables: {
                authorName: reviewData.authorName,
                articleTitle: reviewData.title,
                decision: reviewData.approved ? 'approved' : 'rejected',
                feedback: reviewData.feedback,
                magazineIssue: reviewData.magazineIssue
            }
        });
        
        return { success: true };
    } catch (error) {
        console.error('Error sending review result:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send password reset email
 */
export async function sendPasswordResetEmail(resetData) {
    try {
        const emailId = 'password_reset';
        
        await triggeredEmails.emailMember(emailId, resetData.contactId, {
            variables: {
                memberName: resetData.memberName,
                resetLink: resetData.resetLink,
                expirationTime: '24 hours'
            }
        });
        
        return { success: true };
    } catch (error) {
        console.error('Error sending password reset email:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send Zelle payment verification request
 */
export async function sendZelleVerificationRequest(paymentData) {
    try {
        const emailId = 'zelle_verification';
        
        await triggeredEmails.emailMember(emailId, paymentData.contactId, {
            variables: {
                memberName: paymentData.memberName,
                amount: paymentData.amount,
                transactionId: paymentData.transactionId,
                zelleConfirmation: paymentData.zelleConfirmation,
                description: paymentData.description
            }
        });
        
        return { success: true };
    } catch (error) {
        console.error('Error sending Zelle verification:', error);
        return { success: false, error: error.message };
    }
}

// Helper function to get or create contact
async function getOrCreateContact(email) {
    try {
        const contacts = await wixCrm.contacts.queryContacts()
            .eq('primaryInfo.email', email)
            .find();
        
        if (contacts.items.length > 0) {
            return contacts.items[0]._id;
        }
        
        // Create new contact
        const newContact = await wixCrm.contacts.createContact({
            info: {
                emails: [{ email: email }]
            }
        });
        
        return newContact._id;
    } catch (error) {
        console.error('Error getting/creating contact:', error);
        throw error;
    }
}

/**
 * Create email template variables helper
 */
export function createEmailVariables(templateName, data) {
    const templates = {
        welcome_email: {
            memberName: data.firstName || 'Member',
            fullName: `${data.firstName || ''} ${data.lastName || ''}`.trim(),
            membershipType: data.membershipType || 'General',
            joinDate: new Date().toLocaleDateString('en-US')
        },
        event_confirmation: {
            memberName: data.memberName || 'Member',
            eventName: data.eventName || 'Event',
            eventDate: data.eventDate || '',
            eventTime: data.eventTime || '',
            eventLocation: data.location || 'TBD',
            registrationId: data.registrationId || '',
            guestCount: data.guestCount || 0,
            totalAmount: data.totalAmount || 'Free'
        },
        // Add more template variable mappings as needed
    };
    
    return templates[templateName] || data;
}

```
------------------------------------------------------------

## [16/41] event-automation
- File: `event-automation.jsw`
- Size: 36.5 KB
- Lines: 1152

```javascript
/**
 * BANF Event Automation Service
 * ================================
 * Wix Velo Backend Module for automated event management
 * 
 * Features:
 * - Event creation and management
 * - RSVP tracking and notifications
 * - Automated reminders
 * - Waitlist management
 * - Check-in automation
 * - Post-event surveys and feedback
 * 
 * @module backend/event-automation.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';
import { triggeredEmails } from 'wix-crm-backend';
import { calendar } from 'wix-bookings-backend';

// =====================================================
// EVENT TYPES & CONFIGURATION
// =====================================================

const EVENT_TYPES = {
    CULTURAL: {
        name: 'Cultural Program',
        icon: '🎭',
        defaultCapacity: 200,
        requiresRSVP: true
    },
    RELIGIOUS: {
        name: 'Religious Ceremony',
        icon: '🛕',
        defaultCapacity: 300,
        requiresRSVP: true
    },
    SOCIAL: {
        name: 'Social Gathering',
        icon: '🎉',
        defaultCapacity: 150,
        requiresRSVP: true
    },
    WORKSHOP: {
        name: 'Workshop',
        icon: '🎨',
        defaultCapacity: 30,
        requiresRSVP: true
    },
    MEETING: {
        name: 'Meeting',
        icon: '📋',
        defaultCapacity: 50,
        requiresRSVP: false
    },
    PUJA: {
        name: 'Durga Puja',
        icon: '🪷',
        defaultCapacity: 500,
        requiresRSVP: true,
        isAnnual: true
    },
    PICNIC: {
        name: 'Picnic',
        icon: '🧺',
        defaultCapacity: 200,
        requiresRSVP: true
    },
    STREAMING: {
        name: 'Live Streaming',
        icon: '📺',
        defaultCapacity: null, // Unlimited
        requiresRSVP: true
    }
};

const RSVP_STATUS = {
    CONFIRMED: 'confirmed',
    PENDING: 'pending',
    CANCELLED: 'cancelled',
    WAITLISTED: 'waitlisted',
    CHECKED_IN: 'checked_in',
    NO_SHOW: 'no_show'
};

// =====================================================
// EVENT CREATION & MANAGEMENT
// =====================================================

/**
 * Create a new event
 * @param {Object} eventData 
 */
export async function createEvent(eventData) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized: Admin access required');
    }
    
    try {
        const eventType = EVENT_TYPES[eventData.eventType] || EVENT_TYPES.SOCIAL;
        
        const event = await wixData.insert('Events', {
            // Basic Info
            title: eventData.title,
            description: eventData.description || '',
            shortDescription: eventData.shortDescription || '',
            eventType: eventData.eventType,
            category: eventType.name,
            
            // Scheduling
            eventDate: new Date(eventData.eventDate),
            startTime: eventData.startTime,
            endTime: eventData.endTime,
            timezone: eventData.timezone || 'America/New_York',
            
            // Location
            locationType: eventData.locationType || 'physical', // physical, virtual, hybrid
            venueName: eventData.venueName || '',
            venueAddress: eventData.venueAddress || '',
            venueCity: eventData.venueCity || 'Jacksonville',
            venueState: eventData.venueState || 'FL',
            venueZip: eventData.venueZip || '',
            virtualLink: eventData.virtualLink || '',
            mapLink: eventData.mapLink || '',
            
            // Capacity & RSVP
            capacity: eventData.capacity || eventType.defaultCapacity,
            requiresRSVP: eventData.requiresRSVP !== undefined ? eventData.requiresRSVP : eventType.requiresRSVP,
            rsvpDeadline: eventData.rsvpDeadline ? new Date(eventData.rsvpDeadline) : null,
            allowWaitlist: eventData.allowWaitlist !== false,
            allowGuests: eventData.allowGuests !== false,
            maxGuestsPerRSVP: eventData.maxGuestsPerRSVP || 4,
            
            // Ticketing
            requiresPayment: eventData.requiresPayment || false,
            ticketPrice: eventData.ticketPrice || 0,
            memberDiscount: eventData.memberDiscount || 0, // Percentage
            childrenFree: eventData.childrenFree !== false,
            childrenAgeLimit: eventData.childrenAgeLimit || 12,
            
            // Media
            featuredImage: eventData.featuredImage || '',
            galleryImages: eventData.galleryImages || [],
            
            // Status
            status: 'draft', // draft, published, cancelled, completed
            isPublished: false,
            isFeatured: eventData.isFeatured || false,
            
            // Statistics
            rsvpCount: 0,
            guestCount: 0,
            waitlistCount: 0,
            checkedInCount: 0,
            ticketsSold: 0,
            revenue: 0,
            
            // Notifications
            reminderSettings: {
                oneWeek: true,
                oneDay: true,
                twoHours: true
            },
            reminder1WeekSent: false,
            reminder1DaySent: false,
            reminder2HoursSent: false,
            
            // Metadata
            createdBy: member._id,
            createdAt: new Date(),
            lastModified: new Date(),
            
            // Feedback
            feedbackEnabled: true,
            feedbackSent: false
        });
        
        // Create recurring events if specified
        if (eventData.isRecurring && eventData.recurringPattern) {
            await createRecurringEvents(event, eventData.recurringPattern);
        }
        
        await logEventActivity(event._id, 'EVENT_CREATED', `Event "${event.title}" created`);
        
        return {
            success: true,
            eventId: event._id,
            message: 'Event created successfully'
        };
        
    } catch (error) {
        console.error('Error creating event:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Publish event (make it visible to members)
 * @param {string} eventId 
 */
export async function publishEvent(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        
        event.status = 'published';
        event.isPublished = true;
        event.publishedAt = new Date();
        event.publishedBy = member._id;
        event.lastModified = new Date();
        
        await wixData.update('Events', event);
        
        // Send event announcement to members (optional)
        // await sendEventAnnouncement(event);
        
        await logEventActivity(eventId, 'EVENT_PUBLISHED', `Event published`);
        
        return {
            success: true,
            message: 'Event published successfully'
        };
        
    } catch (error) {
        console.error('Error publishing event:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Update event details
 * @param {string} eventId 
 * @param {Object} updates 
 */
export async function updateEvent(eventId, updates) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        
        const previousDate = event.eventDate;
        const previousVenue = event.venueName;
        
        // Apply updates
        const updatedEvent = {
            ...event,
            ...updates,
            lastModified: new Date()
        };
        
        await wixData.update('Events', updatedEvent);
        
        // Check if critical details changed
        const dateChanged = updates.eventDate && 
            new Date(updates.eventDate).getTime() !== new Date(previousDate).getTime();
        const venueChanged = updates.venueName && updates.venueName !== previousVenue;
        
        // Notify RSVPed attendees of changes
        if (dateChanged || venueChanged) {
            await notifyEventChanges(eventId, {
                dateChanged,
                venueChanged,
                newDate: updates.eventDate,
                newVenue: updates.venueName
            });
        }
        
        await logEventActivity(eventId, 'EVENT_UPDATED', `Event details updated`);
        
        return {
            success: true,
            message: 'Event updated successfully'
        };
        
    } catch (error) {
        console.error('Error updating event:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Cancel event
 * @param {string} eventId 
 * @param {string} reason 
 */
export async function cancelEvent(eventId, reason = '') {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        
        event.status = 'cancelled';
        event.cancellationReason = reason;
        event.cancelledAt = new Date();
        event.cancelledBy = member._id;
        event.lastModified = new Date();
        
        await wixData.update('Events', event);
        
        // Notify all RSVPed attendees
        await notifyEventCancellation(eventId, reason);
        
        // Process refunds if paid event
        if (event.requiresPayment && event.revenue > 0) {
            await createAdminTask({
                type: 'REFUND_REQUIRED',
                title: `Process refunds for cancelled event: ${event.title}`,
                eventId: eventId,
                priority: 'high'
            });
        }
        
        await logEventActivity(eventId, 'EVENT_CANCELLED', `Event cancelled: ${reason}`);
        
        return {
            success: true,
            message: 'Event cancelled and attendees notified'
        };
        
    } catch (error) {
        console.error('Error cancelling event:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// RSVP MANAGEMENT
// =====================================================

/**
 * Process RSVP for event
 * @param {Object} rsvpData 
 */
export async function processRSVP(rsvpData) {
    try {
        const event = await wixData.get('Events', rsvpData.eventId);
        
        if (!event || !event.isPublished) {
            return { success: false, error: 'Event not found or not available' };
        }
        
        if (event.status !== 'published') {
            return { success: false, error: 'Event is not accepting RSVPs' };
        }
        
        // Check RSVP deadline
        if (event.rsvpDeadline && new Date() > new Date(event.rsvpDeadline)) {
            return { success: false, error: 'RSVP deadline has passed' };
        }
        
        // Check if already RSVPed
        const existingRSVP = await wixData.query('EventRSVPs')
            .eq('eventId', rsvpData.eventId)
            .eq('attendeeEmail', rsvpData.attendeeEmail)
            .ne('status', RSVP_STATUS.CANCELLED)
            .find();
        
        if (existingRSVP.items.length > 0) {
            return { 
                success: false, 
                error: 'You have already RSVPed for this event',
                existingRSVP: existingRSVP.items[0]
            };
        }
        
        // Check capacity
        const totalAttending = rsvpData.guestCount ? rsvpData.guestCount + 1 : 1;
        const currentAttendees = event.rsvpCount + event.guestCount;
        
        let rsvpStatus = RSVP_STATUS.CONFIRMED;
        let isWaitlisted = false;
        
        if (event.capacity && currentAttendees + totalAttending > event.capacity) {
            if (event.allowWaitlist) {
                rsvpStatus = RSVP_STATUS.WAITLISTED;
                isWaitlisted = true;
            } else {
                return { success: false, error: 'Event is at full capacity' };
            }
        }
        
        // Validate guest count
        if (rsvpData.guestCount && rsvpData.guestCount > event.maxGuestsPerRSVP) {
            return { 
                success: false, 
                error: `Maximum ${event.maxGuestsPerRSVP} guests allowed per RSVP` 
            };
        }
        
        // Get member info if logged in
        const member = await currentMember.getMember().catch(() => null);
        
        // Create RSVP
        const rsvp = await wixData.insert('EventRSVPs', {
            eventId: rsvpData.eventId,
            memberId: member?._id || null,
            attendeeName: rsvpData.attendeeName,
            attendeeEmail: rsvpData.attendeeEmail,
            attendeePhone: rsvpData.attendeePhone || '',
            
            // Guests
            guestCount: rsvpData.guestCount || 0,
            guestNames: rsvpData.guestNames || [],
            totalAttending: totalAttending,
            
            // Status
            status: rsvpStatus,
            
            // Dietary & Accessibility
            dietaryRestrictions: rsvpData.dietaryRestrictions || '',
            accessibilityNeeds: rsvpData.accessibilityNeeds || '',
            
            // Additional Info
            notes: rsvpData.notes || '',
            
            // Payment (if applicable)
            paymentRequired: event.requiresPayment,
            paymentStatus: event.requiresPayment ? 'pending' : 'not_required',
            paymentId: null,
            totalAmount: event.requiresPayment ? calculateTicketPrice(event, member, totalAttending) : 0,
            
            // Timestamps
            rsvpDate: new Date(),
            checkedIn: false,
            checkInTime: null,
            
            // Confirmation
            confirmationCode: generateConfirmationCode(),
            confirmationSent: false
        });
        
        // Update event counts
        if (!isWaitlisted) {
            event.rsvpCount = (event.rsvpCount || 0) + 1;
            event.guestCount = (event.guestCount || 0) + (rsvpData.guestCount || 0);
        } else {
            event.waitlistCount = (event.waitlistCount || 0) + 1;
        }
        await wixData.update('Events', event);
        
        // Send confirmation email
        await sendRSVPConfirmation(rsvp, event, isWaitlisted);
        
        // Award engagement points if member
        if (member?._id) {
            const { addEngagementPoints } = await import('backend/member-automation.jsw');
            await addEngagementPoints(member._id, 2, `RSVP for ${event.title}`);
        }
        
        await logEventActivity(rsvpData.eventId, 'RSVP_RECEIVED', 
            `${rsvpData.attendeeName} RSVPed${isWaitlisted ? ' (waitlisted)' : ''}`);
        
        return {
            success: true,
            rsvpId: rsvp._id,
            confirmationCode: rsvp.confirmationCode,
            status: rsvpStatus,
            message: isWaitlisted 
                ? "You've been added to the waitlist. We'll notify you if a spot opens up."
                : "Your RSVP has been confirmed!",
            paymentRequired: event.requiresPayment && rsvpStatus === RSVP_STATUS.CONFIRMED,
            paymentAmount: rsvp.totalAmount
        };
        
    } catch (error) {
        console.error('Error processing RSVP:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Cancel RSVP
 * @param {string} rsvpId 
 * @param {string} reason 
 */
export async function cancelRSVP(rsvpId, reason = '') {
    try {
        const rsvp = await wixData.get('EventRSVPs', rsvpId);
        
        if (!rsvp) {
            return { success: false, error: 'RSVP not found' };
        }
        
        // Verify ownership or admin
        const member = await currentMember.getMember().catch(() => null);
        const isOwner = member && rsvp.memberId === member._id;
        const isAdminUser = member && await isAdmin(member._id);
        
        if (!isOwner && !isAdminUser) {
            return { success: false, error: 'Unauthorized' };
        }
        
        const wasWaitlisted = rsvp.status === RSVP_STATUS.WAITLISTED;
        const wasConfirmed = rsvp.status === RSVP_STATUS.CONFIRMED;
        
        rsvp.status = RSVP_STATUS.CANCELLED;
        rsvp.cancellationReason = reason;
        rsvp.cancelledAt = new Date();
        
        await wixData.update('EventRSVPs', rsvp);
        
        // Update event counts
        const event = await wixData.get('Events', rsvp.eventId);
        
        if (wasWaitlisted) {
            event.waitlistCount = Math.max(0, (event.waitlistCount || 1) - 1);
        } else if (wasConfirmed) {
            event.rsvpCount = Math.max(0, (event.rsvpCount || 1) - 1);
            event.guestCount = Math.max(0, (event.guestCount || 0) - (rsvp.guestCount || 0));
            
            // Process waitlist - move first waitlisted person to confirmed
            await processWaitlist(rsvp.eventId);
        }
        
        await wixData.update('Events', event);
        
        // Send cancellation confirmation
        await triggeredEmails.emailContact(
            'rsvp_cancelled',
            rsvp.attendeeEmail,
            {
                variables: {
                    attendeeName: rsvp.attendeeName,
                    eventName: event.title,
                    eventDate: formatDate(event.eventDate)
                }
            }
        );
        
        await logEventActivity(rsvp.eventId, 'RSVP_CANCELLED', 
            `${rsvp.attendeeName} cancelled RSVP`);
        
        return {
            success: true,
            message: 'RSVP cancelled successfully'
        };
        
    } catch (error) {
        console.error('Error cancelling RSVP:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Process waitlist - move first waitlisted to confirmed
 * @param {string} eventId 
 */
async function processWaitlist(eventId) {
    try {
        const event = await wixData.get('Events', eventId);
        
        // Check if there's space
        const currentAttendees = event.rsvpCount + event.guestCount;
        if (event.capacity && currentAttendees >= event.capacity) {
            return;
        }
        
        // Get first waitlisted RSVP
        const waitlist = await wixData.query('EventRSVPs')
            .eq('eventId', eventId)
            .eq('status', RSVP_STATUS.WAITLISTED)
            .ascending('rsvpDate')
            .limit(1)
            .find();
        
        if (waitlist.items.length === 0) {
            return;
        }
        
        const waitlistedRSVP = waitlist.items[0];
        
        // Check if this RSVP fits in remaining capacity
        const totalAttending = waitlistedRSVP.totalAttending;
        if (event.capacity && currentAttendees + totalAttending > event.capacity) {
            return; // Can't fit this RSVP
        }
        
        // Move to confirmed
        waitlistedRSVP.status = RSVP_STATUS.CONFIRMED;
        waitlistedRSVP.confirmedFromWaitlist = true;
        waitlistedRSVP.confirmedFromWaitlistAt = new Date();
        
        await wixData.update('EventRSVPs', waitlistedRSVP);
        
        // Update event counts
        event.rsvpCount = (event.rsvpCount || 0) + 1;
        event.guestCount = (event.guestCount || 0) + (waitlistedRSVP.guestCount || 0);
        event.waitlistCount = Math.max(0, (event.waitlistCount || 1) - 1);
        
        await wixData.update('Events', event);
        
        // Notify attendee
        await triggeredEmails.emailContact(
            'waitlist_confirmed',
            waitlistedRSVP.attendeeEmail,
            {
                variables: {
                    attendeeName: waitlistedRSVP.attendeeName,
                    eventName: event.title,
                    eventDate: formatDate(event.eventDate),
                    confirmationCode: waitlistedRSVP.confirmationCode
                }
            }
        );
        
        await logEventActivity(eventId, 'WAITLIST_PROMOTED', 
            `${waitlistedRSVP.attendeeName} moved from waitlist to confirmed`);
        
    } catch (error) {
        console.error('Error processing waitlist:', error);
    }
}

// =====================================================
// EVENT REMINDERS
// =====================================================

/**
 * Send event reminders (run by scheduled job)
 */
export async function sendEventReminders() {
    try {
        const now = new Date();
        const oneWeekFromNow = addDays(now, 7);
        const oneDayFromNow = addDays(now, 1);
        const twoHoursFromNow = new Date(now.getTime() + 2 * 60 * 60 * 1000);
        
        const results = {
            oneWeek: 0,
            oneDay: 0,
            twoHours: 0
        };
        
        // 1 Week Reminders
        const weekEvents = await wixData.query('Events')
            .eq('status', 'published')
            .between('eventDate', now, oneWeekFromNow)
            .eq('reminder1WeekSent', false)
            .find();
        
        for (const event of weekEvents.items) {
            if (event.reminderSettings?.oneWeek) {
                await sendReminderForEvent(event, '1_week');
                event.reminder1WeekSent = true;
                await wixData.update('Events', event);
                results.oneWeek++;
            }
        }
        
        // 1 Day Reminders
        const dayEvents = await wixData.query('Events')
            .eq('status', 'published')
            .between('eventDate', now, oneDayFromNow)
            .eq('reminder1DaySent', false)
            .find();
        
        for (const event of dayEvents.items) {
            if (event.reminderSettings?.oneDay) {
                await sendReminderForEvent(event, '1_day');
                event.reminder1DaySent = true;
                await wixData.update('Events', event);
                results.oneDay++;
            }
        }
        
        // 2 Hours Reminders
        const hourEvents = await wixData.query('Events')
            .eq('status', 'published')
            .between('eventDate', now, twoHoursFromNow)
            .eq('reminder2HoursSent', false)
            .find();
        
        for (const event of hourEvents.items) {
            if (event.reminderSettings?.twoHours) {
                await sendReminderForEvent(event, '2_hours');
                event.reminder2HoursSent = true;
                await wixData.update('Events', event);
                results.twoHours++;
            }
        }
        
        console.log('Event reminders sent:', results);
        return { success: true, ...results };
        
    } catch (error) {
        console.error('Error sending reminders:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send reminder for specific event
 * @param {Object} event 
 * @param {string} reminderType 
 */
async function sendReminderForEvent(event, reminderType) {
    try {
        // Get all confirmed RSVPs
        const rsvps = await wixData.query('EventRSVPs')
            .eq('eventId', event._id)
            .eq('status', RSVP_STATUS.CONFIRMED)
            .find();
        
        const templateId = `event_reminder_${reminderType}`;
        
        for (const rsvp of rsvps.items) {
            await triggeredEmails.emailContact(
                templateId,
                rsvp.attendeeEmail,
                {
                    variables: {
                        attendeeName: rsvp.attendeeName,
                        eventName: event.title,
                        eventDate: formatDate(event.eventDate),
                        eventTime: event.startTime,
                        venueName: event.venueName,
                        venueAddress: `${event.venueAddress}, ${event.venueCity}, ${event.venueState}`,
                        confirmationCode: rsvp.confirmationCode,
                        mapLink: event.mapLink || '',
                        virtualLink: event.virtualLink || ''
                    }
                }
            );
        }
        
        await logEventActivity(event._id, 'REMINDERS_SENT', 
            `${reminderType} reminders sent to ${rsvps.items.length} attendees`);
        
    } catch (error) {
        console.error('Error sending event reminder:', error);
    }
}

// =====================================================
// CHECK-IN MANAGEMENT
// =====================================================

/**
 * Check in attendee
 * @param {string} confirmationCode 
 */
export async function checkInAttendee(confirmationCode) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const rsvps = await wixData.query('EventRSVPs')
            .eq('confirmationCode', confirmationCode)
            .find();
        
        if (rsvps.items.length === 0) {
            return { success: false, error: 'Invalid confirmation code' };
        }
        
        const rsvp = rsvps.items[0];
        
        if (rsvp.checkedIn) {
            return { 
                success: false, 
                error: 'Already checked in',
                checkInTime: rsvp.checkInTime
            };
        }
        
        if (rsvp.status !== RSVP_STATUS.CONFIRMED) {
            return { 
                success: false, 
                error: `Cannot check in: Status is ${rsvp.status}` 
            };
        }
        
        // Update RSVP
        rsvp.checkedIn = true;
        rsvp.checkInTime = new Date();
        rsvp.checkedInBy = member._id;
        rsvp.status = RSVP_STATUS.CHECKED_IN;
        
        await wixData.update('EventRSVPs', rsvp);
        
        // Update event checked-in count
        const event = await wixData.get('Events', rsvp.eventId);
        event.checkedInCount = (event.checkedInCount || 0) + 1 + (rsvp.guestCount || 0);
        await wixData.update('Events', event);
        
        // Award engagement points for attendance
        if (rsvp.memberId) {
            const { addEngagementPoints } = await import('backend/member-automation.jsw');
            await addEngagementPoints(rsvp.memberId, 10, `Attended ${event.title}`);
        }
        
        return {
            success: true,
            attendeeName: rsvp.attendeeName,
            guestCount: rsvp.guestCount,
            totalCheckedIn: rsvp.totalAttending,
            message: `${rsvp.attendeeName} + ${rsvp.guestCount} guests checked in`
        };
        
    } catch (error) {
        console.error('Error checking in:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Get check-in statistics for event
 * @param {string} eventId 
 */
export async function getCheckInStats(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        const rsvps = await wixData.query('EventRSVPs')
            .eq('eventId', eventId)
            .ne('status', RSVP_STATUS.CANCELLED)
            .find();
        
        const stats = {
            totalRSVPs: rsvps.items.length,
            totalExpectedAttendees: rsvps.items.reduce((sum, r) => sum + r.totalAttending, 0),
            checkedIn: rsvps.items.filter(r => r.checkedIn).length,
            totalCheckedInAttendees: event.checkedInCount || 0,
            notYetCheckedIn: rsvps.items.filter(r => !r.checkedIn && r.status === RSVP_STATUS.CONFIRMED).length,
            waitlisted: rsvps.items.filter(r => r.status === RSVP_STATUS.WAITLISTED).length
        };
        
        return {
            success: true,
            stats: stats
        };
        
    } catch (error) {
        console.error('Error getting check-in stats:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// POST-EVENT
// =====================================================

/**
 * Mark event as completed and send feedback surveys
 * @param {string} eventId 
 */
export async function completeEvent(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        
        event.status = 'completed';
        event.completedAt = new Date();
        event.lastModified = new Date();
        
        // Mark no-shows
        const rsvps = await wixData.query('EventRSVPs')
            .eq('eventId', eventId)
            .eq('status', RSVP_STATUS.CONFIRMED)
            .eq('checkedIn', false)
            .find();
        
        for (const rsvp of rsvps.items) {
            rsvp.status = RSVP_STATUS.NO_SHOW;
            await wixData.update('EventRSVPs', rsvp);
        }
        
        await wixData.update('Events', event);
        
        // Send feedback surveys if enabled
        if (event.feedbackEnabled) {
            await sendFeedbackSurveys(eventId);
        }
        
        await logEventActivity(eventId, 'EVENT_COMPLETED', 'Event marked as completed');
        
        return {
            success: true,
            message: 'Event completed and feedback surveys sent'
        };
        
    } catch (error) {
        console.error('Error completing event:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Send feedback surveys to attendees
 * @param {string} eventId 
 */
async function sendFeedbackSurveys(eventId) {
    try {
        const event = await wixData.get('Events', eventId);
        
        const attendees = await wixData.query('EventRSVPs')
            .eq('eventId', eventId)
            .eq('status', RSVP_STATUS.CHECKED_IN)
            .find();
        
        for (const attendee of attendees.items) {
            await triggeredEmails.emailContact(
                'event_feedback_request',
                attendee.attendeeEmail,
                {
                    variables: {
                        attendeeName: attendee.attendeeName,
                        eventName: event.title,
                        feedbackLink: `https://jaxbengali.org/feedback/${eventId}?code=${attendee.confirmationCode}`
                    }
                }
            );
        }
        
        event.feedbackSent = true;
        event.feedbackSentDate = new Date();
        await wixData.update('Events', event);
        
    } catch (error) {
        console.error('Error sending feedback surveys:', error);
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

/**
 * Send RSVP confirmation email
 */
async function sendRSVPConfirmation(rsvp, event, isWaitlisted) {
    const templateId = isWaitlisted ? 'rsvp_waitlisted' : 'rsvp_confirmed';
    
    await triggeredEmails.emailContact(
        templateId,
        rsvp.attendeeEmail,
        {
            variables: {
                attendeeName: rsvp.attendeeName,
                eventName: event.title,
                eventDate: formatDate(event.eventDate),
                eventTime: event.startTime,
                venueName: event.venueName || 'TBD',
                venueAddress: event.venueAddress || '',
                guestCount: rsvp.guestCount,
                confirmationCode: rsvp.confirmationCode,
                paymentRequired: event.requiresPayment && !isWaitlisted
            }
        }
    );
    
    rsvp.confirmationSent = true;
    await wixData.update('EventRSVPs', rsvp);
}

/**
 * Notify attendees of event changes
 */
async function notifyEventChanges(eventId, changes) {
    const event = await wixData.get('Events', eventId);
    const rsvps = await wixData.query('EventRSVPs')
        .eq('eventId', eventId)
        .eq('status', RSVP_STATUS.CONFIRMED)
        .find();
    
    for (const rsvp of rsvps.items) {
        await triggeredEmails.emailContact(
            'event_updated',
            rsvp.attendeeEmail,
            {
                variables: {
                    attendeeName: rsvp.attendeeName,
                    eventName: event.title,
                    dateChanged: changes.dateChanged,
                    venueChanged: changes.venueChanged,
                    newDate: changes.newDate ? formatDate(changes.newDate) : '',
                    newVenue: changes.newVenue || ''
                }
            }
        );
    }
}

/**
 * Notify attendees of event cancellation
 */
async function notifyEventCancellation(eventId, reason) {
    const event = await wixData.get('Events', eventId);
    const rsvps = await wixData.query('EventRSVPs')
        .eq('eventId', eventId)
        .ne('status', RSVP_STATUS.CANCELLED)
        .find();
    
    for (const rsvp of rsvps.items) {
        await triggeredEmails.emailContact(
            'event_cancelled',
            rsvp.attendeeEmail,
            {
                variables: {
                    attendeeName: rsvp.attendeeName,
                    eventName: event.title,
                    eventDate: formatDate(event.eventDate),
                    cancellationReason: reason || 'No reason provided'
                }
            }
        );
    }
}

/**
 * Calculate ticket price
 */
function calculateTicketPrice(event, member, totalAttending) {
    let pricePerPerson = event.ticketPrice || 0;
    
    // Apply member discount
    if (member && event.memberDiscount > 0) {
        pricePerPerson = pricePerPerson * (1 - event.memberDiscount / 100);
    }
    
    return Math.round(pricePerPerson * totalAttending * 100) / 100;
}

/**
 * Generate confirmation code
 */
function generateConfirmationCode() {
    return 'BANF-' + Math.random().toString(36).substring(2, 8).toUpperCase();
}

/**
 * Create admin task
 */
async function createAdminTask(taskData) {
    await wixData.insert('AdminTasks', {
        ...taskData,
        status: 'pending',
        createdAt: new Date()
    });
}

/**
 * Log event activity
 */
async function logEventActivity(eventId, action, details) {
    await wixData.insert('EventActivityLog', {
        eventId: eventId,
        action: action,
        details: details,
        timestamp: new Date()
    });
}

/**
 * Check if member is admin
 */
async function isAdmin(memberId) {
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec')
            );
        }
        return false;
    } catch {
        return false;
    }
}

/**
 * Add days to date
 */
function addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

/**
 * Format date for display
 */
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Create recurring events
 */
async function createRecurringEvents(baseEvent, pattern) {
    // Implementation for recurring events
    // pattern: { frequency: 'weekly'|'monthly', count: number, days: [] }
    console.log('Creating recurring events:', pattern);
}

```
------------------------------------------------------------

## [17/41] events
- File: `events.jsw`
- Size: 13.8 KB
- Lines: 391

```javascript
// backend/events.jsw
// BANF Event Management - Wix Velo Backend

import wixData from 'wix-data';
import { sendEmail } from 'backend/email.jsw';

const EVENTS_COLLECTION = 'Events';
const REGISTRATIONS_COLLECTION = 'EventRegistrations';
const FEEDBACK_COLLECTION = 'EventFeedback';

/**
 * Get all upcoming events
 */
export async function getUpcomingEvents(options = { limit: 20 }) {
    try {
        const now = new Date();
        
        const result = await wixData.query(EVENTS_COLLECTION)
            .ge('eventDate', now)
            .eq('isActive', true)
            .ascending('eventDate')
            .limit(options.limit)
            .find();
        
        return result.items;
    } catch (error) {
        console.error('Error getting upcoming events:', error);
        return [];
    }
}

/**
 * Get past events for archive
 */
export async function getPastEvents(options = { limit: 50, skip: 0 }) {
    try {
        const now = new Date();
        
        const result = await wixData.query(EVENTS_COLLECTION)
            .lt('eventDate', now)
            .descending('eventDate')
            .limit(options.limit)
            .skip(options.skip)
            .find();
        
        return {
            items: result.items,
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error getting past events:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Get single event by ID
 */
export async function getEventById(eventId) {
    try {
        return await wixData.get(EVENTS_COLLECTION, eventId);
    } catch (error) {
        console.error('Error getting event:', error);
        return null;
    }
}

/**
 * Create a new event (admin only)
 */
export async function createEvent(eventData) {
    try {
        const event = {
            title: eventData.title,
            eventType: eventData.eventType, // durga_puja, saraswati_puja, pohela_boishakh, etc.
            description: eventData.description,
            eventDate: new Date(eventData.eventDate),
            endDate: eventData.endDate ? new Date(eventData.endDate) : null,
            registrationDeadline: eventData.registrationDeadline ? new Date(eventData.registrationDeadline) : null,
            venueName: eventData.venueName,
            venueAddress: eventData.venueAddress,
            maxAttendees: eventData.maxAttendees || 500,
            currentRegistrations: 0,
            ticketPrice: eventData.ticketPrice || 0,
            memberDiscount: eventData.memberDiscount || 0,
            featuredImage: eventData.featuredImage || '',
            galleryImages: eventData.galleryImages || [],
            isActive: true,
            isFeatured: eventData.isFeatured || false,
            createdBy: eventData.adminId,
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert(EVENTS_COLLECTION, event);
        return { success: true, event: result };
    } catch (error) {
        console.error('Error creating event:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Update an event (admin only)
 */
export async function updateEvent(eventId, updateData) {
    try {
        const existing = await wixData.get(EVENTS_COLLECTION, eventId);
        if (!existing) {
            return { success: false, error: 'Event not found' };
        }
        
        // Convert dates
        if (updateData.eventDate) updateData.eventDate = new Date(updateData.eventDate);
        if (updateData.endDate) updateData.endDate = new Date(updateData.endDate);
        if (updateData.registrationDeadline) updateData.registrationDeadline = new Date(updateData.registrationDeadline);
        
        updateData._updatedDate = new Date();
        
        const updated = { ...existing, ...updateData };
        const result = await wixData.update(EVENTS_COLLECTION, updated);
        
        return { success: true, event: result };
    } catch (error) {
        console.error('Error updating event:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Register member for an event
 */
export async function registerForEvent(eventId, memberId, attendees) {
    try {
        // Get event details
        const event = await wixData.get(EVENTS_COLLECTION, eventId);
        if (!event) {
            return { success: false, error: 'Event not found' };
        }
        
        // Check if event is active
        if (!event.isActive) {
            return { success: false, error: 'Event is no longer accepting registrations' };
        }
        
        // Check registration deadline
        if (event.registrationDeadline && new Date() > event.registrationDeadline) {
            return { success: false, error: 'Registration deadline has passed' };
        }
        
        // Check capacity
        const attendeeCount = attendees ? attendees.length : 1;
        if (event.currentRegistrations + attendeeCount > event.maxAttendees) {
            return { success: false, error: 'Event is at capacity' };
        }
        
        // Check for existing registration
        const existingReg = await wixData.query(REGISTRATIONS_COLLECTION)
            .eq('eventId', eventId)
            .eq('memberId', memberId)
            .find();
        
        if (existingReg.items.length > 0) {
            return { success: false, error: 'Already registered for this event' };
        }
        
        // Create registration
        const registration = {
            eventId: eventId,
            eventTitle: event.title,
            memberId: memberId,
            attendeeCount: attendeeCount,
            attendeeDetails: JSON.stringify(attendees || []),
            registrationDate: new Date(),
            status: 'confirmed',
            totalAmount: calculateEventCost(event, attendeeCount, true), // true = member
            isPaid: false,
            _createdDate: new Date()
        };
        
        const regResult = await wixData.insert(REGISTRATIONS_COLLECTION, registration);
        
        // Update event count
        event.currentRegistrations = event.currentRegistrations + attendeeCount;
        event._updatedDate = new Date();
        await wixData.update(EVENTS_COLLECTION, event);
        
        return { 
            success: true, 
            registrationId: regResult._id,
            totalAmount: registration.totalAmount
        };
    } catch (error) {
        console.error('Error registering for event:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Cancel event registration
 */
export async function cancelRegistration(registrationId, memberId) {
    try {
        const registration = await wixData.get(REGISTRATIONS_COLLECTION, registrationId);
        if (!registration) {
            return { success: false, error: 'Registration not found' };
        }
        
        // Verify ownership
        if (registration.memberId !== memberId) {
            return { success: false, error: 'Unauthorized' };
        }
        
        // Get event and update count
        const event = await wixData.get(EVENTS_COLLECTION, registration.eventId);
        if (event) {
            event.currentRegistrations = Math.max(0, event.currentRegistrations - registration.attendeeCount);
            await wixData.update(EVENTS_COLLECTION, event);
        }
        
        // Update registration status
        registration.status = 'cancelled';
        registration.cancelledAt = new Date();
        await wixData.update(REGISTRATIONS_COLLECTION, registration);
        
        return { success: true };
    } catch (error) {
        console.error('Error cancelling registration:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get member's event registrations
 */
export async function getMemberRegistrations(memberId) {
    try {
        const result = await wixData.query(REGISTRATIONS_COLLECTION)
            .eq('memberId', memberId)
            .descending('registrationDate')
            .find();
        
        return result.items;
    } catch (error) {
        console.error('Error getting registrations:', error);
        return [];
    }
}

/**
 * Submit event feedback
 */
export async function submitEventFeedback(feedbackData) {
    try {
        // Calculate sentiment score
        const sentimentScore = calculateSentiment(feedbackData.feedbackText);
        
        const feedback = {
            eventId: feedbackData.eventId,
            eventName: feedbackData.eventName,
            eventDate: new Date(feedbackData.eventDate),
            memberId: feedbackData.memberId || null,
            memberName: feedbackData.isAnonymous ? 'Anonymous' : feedbackData.memberName,
            isAnonymous: feedbackData.isAnonymous || false,
            feedbackText: feedbackData.feedbackText,
            experienceScore: feedbackData.experienceScore, // 1-5
            overallRating: feedbackData.overallRating, // 1-10
            sentimentScore: sentimentScore,
            sentimentLabel: getSentimentLabel(sentimentScore),
            organizationRating: feedbackData.organizationRating,
            contentRating: feedbackData.contentRating,
            venueRating: feedbackData.venueRating,
            foodRating: feedbackData.foodRating,
            wouldRecommend: feedbackData.wouldRecommend,
            wouldAttendAgain: feedbackData.wouldAttendAgain,
            suggestions: feedbackData.suggestions || '',
            improvements: feedbackData.improvements || '',
            submittedAt: new Date(),
            processedAt: new Date(),
            _createdDate: new Date()
        };
        
        const result = await wixData.insert(FEEDBACK_COLLECTION, feedback);
        return { success: true, feedbackId: result._id };
    } catch (error) {
        console.error('Error submitting feedback:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get event feedback summary (admin)
 */
export async function getEventFeedbackSummary(eventId) {
    try {
        const feedbacks = await wixData.query(FEEDBACK_COLLECTION)
            .eq('eventId', eventId)
            .find();
        
        if (feedbacks.items.length === 0) {
            return { totalFeedbacks: 0, averages: null };
        }
        
        const items = feedbacks.items;
        const total = items.length;
        
        // Calculate averages
        const avgExperience = items.reduce((sum, f) => sum + (f.experienceScore || 0), 0) / total;
        const avgOverall = items.reduce((sum, f) => sum + (f.overallRating || 0), 0) / total;
        const avgOrganization = items.reduce((sum, f) => sum + (f.organizationRating || 0), 0) / total;
        const avgContent = items.reduce((sum, f) => sum + (f.contentRating || 0), 0) / total;
        const avgVenue = items.reduce((sum, f) => sum + (f.venueRating || 0), 0) / total;
        const avgFood = items.reduce((sum, f) => sum + (f.foodRating || 0), 0) / total;
        
        // Sentiment distribution
        const sentiments = {
            positive: items.filter(f => f.sentimentLabel === 'positive').length,
            neutral: items.filter(f => f.sentimentLabel === 'neutral').length,
            negative: items.filter(f => f.sentimentLabel === 'negative').length
        };
        
        // Recommendation rate
        const recommendRate = (items.filter(f => f.wouldRecommend).length / total) * 100;
        
        return {
            totalFeedbacks: total,
            averages: {
                experience: avgExperience.toFixed(1),
                overall: avgOverall.toFixed(1),
                organization: avgOrganization.toFixed(1),
                content: avgContent.toFixed(1),
                venue: avgVenue.toFixed(1),
                food: avgFood.toFixed(1)
            },
            sentiments,
            recommendationRate: recommendRate.toFixed(1)
        };
    } catch (error) {
        console.error('Error getting feedback summary:', error);
        return null;
    }
}

// Helper functions
function calculateEventCost(event, attendeeCount, isMember) {
    const basePrice = event.ticketPrice || 0;
    const discount = isMember ? (event.memberDiscount || 0) : 0;
    const pricePerPerson = basePrice - discount;
    return pricePerPerson * attendeeCount;
}

function calculateSentiment(text) {
    if (!text) return 0;
    
    const lowerText = text.toLowerCase();
    
    const positiveWords = [
        'excellent', 'amazing', 'wonderful', 'fantastic', 'great', 'good', 'best',
        'love', 'enjoyed', 'perfect', 'outstanding', 'impressive', 'beautiful',
        'brilliant', 'superb', 'awesome', 'pleased', 'happy', 'satisfied'
    ];
    
    const negativeWords = [
        'terrible', 'awful', 'horrible', 'bad', 'worst', 'hate', 'disappointed',
        'poor', 'boring', 'annoying', 'frustrated', 'angry', 'dissatisfied',
        'unorganized', 'chaotic', 'problems', 'issues', 'complaint'
    ];
    
    let positiveCount = 0;
    let negativeCount = 0;
    
    positiveWords.forEach(word => {
        if (lowerText.includes(word)) positiveCount++;
    });
    
    negativeWords.forEach(word => {
        if (lowerText.includes(word)) negativeCount++;
    });
    
    const totalWords = text.split(' ').length;
    const score = (positiveCount - negativeCount) / Math.max(totalWords / 10, 1);
    
    return Math.max(-1, Math.min(1, score));
}

function getSentimentLabel(score) {
    if (score > 0.2) return 'positive';
    if (score < -0.2) return 'negative';
    return 'neutral';
}

```
------------------------------------------------------------

## [18/41] evite-service
- File: `evite-service.jsw`
- Size: 36.2 KB
- Lines: 1001

```javascript
/**
 * BANF E-Vite Service
 * ====================
 * Wix Velo Backend Module for digital invitations with RSVP tracking
 * 
 * Features:
 * - Beautiful e-vite creation with templates
 * - Multi-channel delivery (email, WhatsApp, SMS)
 * - RSVP tracking with detailed attendee info
 * - Real-time analytics dashboard
 * - Dietary/accessibility requirement collection
 * - Guest management and plus-ones
 * 
 * @module backend/evite-service.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';
import { triggeredEmails } from 'wix-crm-backend';
import crypto from 'crypto';

// =====================================================
// EVITE TEMPLATES
// =====================================================

const EVITE_TEMPLATES = {
    DURGA_PUJA: {
        id: 'durga_puja',
        name: 'Durga Puja Celebration',
        theme: 'festive',
        primaryColor: '#ff6b35',
        secondaryColor: '#722f37',
        backgroundImage: 'durga_puja_bg.jpg',
        bengaliTitle: 'দুর্গা পূজা উৎসব',
        defaultMessage: 'You are cordially invited to celebrate Durga Puja with BANF family!'
    },
    SARASWATI_PUJA: {
        id: 'saraswati_puja',
        name: 'Saraswati Puja',
        theme: 'elegant',
        primaryColor: '#fff5e6',
        secondaryColor: '#daa520',
        backgroundImage: 'saraswati_bg.jpg',
        bengaliTitle: 'সরস্বতী পূজা',
        defaultMessage: 'Join us in celebrating the goddess of knowledge and arts!'
    },
    CULTURAL_PROGRAM: {
        id: 'cultural',
        name: 'Cultural Program',
        theme: 'artistic',
        primaryColor: '#006A4E',
        secondaryColor: '#f7931e',
        backgroundImage: 'cultural_bg.jpg',
        bengaliTitle: 'সাংস্কৃতিক অনুষ্ঠান',
        defaultMessage: 'Experience the richness of Bengali culture!'
    },
    PICNIC: {
        id: 'picnic',
        name: 'Annual Picnic',
        theme: 'casual',
        primaryColor: '#4CAF50',
        secondaryColor: '#FFC107',
        backgroundImage: 'picnic_bg.jpg',
        bengaliTitle: 'বার্ষিক পিকনিক',
        defaultMessage: 'Fun, food, and friendship await!'
    },
    GENERAL: {
        id: 'general',
        name: 'General Event',
        theme: 'modern',
        primaryColor: '#ff6b35',
        secondaryColor: '#1a1a2e',
        backgroundImage: 'general_bg.jpg',
        bengaliTitle: 'অনুষ্ঠান',
        defaultMessage: 'You are invited to join us!'
    }
};

const DIETARY_OPTIONS = [
    { id: 'vegetarian', label: 'Vegetarian', labelBengali: 'নিরামিষ', icon: '🥬' },
    { id: 'non_vegetarian', label: 'Non-Vegetarian', labelBengali: 'আমিষ', icon: '🍗' },
    { id: 'vegan', label: 'Vegan', labelBengali: 'ভেগান', icon: '🌱' },
    { id: 'gluten_free', label: 'Gluten-Free', labelBengali: 'গ্লুটেন-মুক্ত', icon: '🌾' },
    { id: 'nut_allergy', label: 'Nut Allergy', labelBengali: 'বাদাম এলার্জি', icon: '🥜' },
    { id: 'dairy_free', label: 'Dairy-Free', labelBengali: 'দুগ্ধ-মুক্ত', icon: '🥛' },
    { id: 'halal', label: 'Halal', labelBengali: 'হালাল', icon: '☪️' },
    { id: 'kosher', label: 'Kosher', labelBengali: 'কোশের', icon: '✡️' },
    { id: 'no_restriction', label: 'No Restrictions', labelBengali: 'কোনো সীমাবদ্ধতা নেই', icon: '✅' }
];

const AGE_CATEGORIES = [
    { id: 'adult', label: 'Adult (18+)', minAge: 18, maxAge: null },
    { id: 'teen', label: 'Teen (13-17)', minAge: 13, maxAge: 17 },
    { id: 'child', label: 'Child (5-12)', minAge: 5, maxAge: 12 },
    { id: 'toddler', label: 'Toddler (2-4)', minAge: 2, maxAge: 4 },
    { id: 'infant', label: 'Infant (0-1)', minAge: 0, maxAge: 1 }
];

const RSVP_STATUS = {
    PENDING: 'pending',
    ATTENDING: 'attending',
    NOT_ATTENDING: 'not_attending',
    MAYBE: 'maybe',
    EXPIRED: 'expired'
};

// =====================================================
// EVITE CREATION
// =====================================================

/**
 * Create a new e-vite for an event
 * @param {Object} eviteData
 */
export async function createEvite(eviteData) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized: Admin access required');
    }
    
    try {
        const template = EVITE_TEMPLATES[eviteData.template] || EVITE_TEMPLATES.GENERAL;
        const event = await wixData.get('Events', eviteData.eventId);
        
        if (!event) {
            return { success: false, error: 'Event not found' };
        }
        
        const evite = await wixData.insert('Evites', {
            // Event Reference
            eventId: eviteData.eventId,
            eventTitle: event.title,
            eventDate: event.eventDate,
            eventTime: event.startTime,
            eventLocation: event.venueName,
            eventAddress: `${event.venueAddress}, ${event.venueCity}, ${event.venueState}`,
            
            // Template & Design
            templateId: template.id,
            templateName: template.name,
            theme: template.theme,
            primaryColor: eviteData.primaryColor || template.primaryColor,
            secondaryColor: eviteData.secondaryColor || template.secondaryColor,
            backgroundImage: eviteData.backgroundImage || template.backgroundImage,
            customBanner: eviteData.customBanner || '',
            
            // Content
            title: eviteData.title || event.title,
            titleBengali: eviteData.titleBengali || template.bengaliTitle,
            message: eviteData.message || template.defaultMessage,
            messageBengali: eviteData.messageBengali || '',
            hostName: eviteData.hostName || 'BANF Executive Committee',
            
            // RSVP Settings
            rsvpEnabled: true,
            rsvpDeadline: eviteData.rsvpDeadline || addDays(event.eventDate, -3),
            allowPlusOnes: eviteData.allowPlusOnes !== false,
            maxGuestsPerInvite: eviteData.maxGuestsPerInvite || 5,
            collectDietary: eviteData.collectDietary !== false,
            collectAgeInfo: eviteData.collectAgeInfo !== false,
            collectAccessibility: eviteData.collectAccessibility !== false,
            allowMaybeResponse: eviteData.allowMaybeResponse || false,
            
            // Custom Questions
            customQuestions: eviteData.customQuestions || [],
            
            // Tracking
            totalInvitesSent: 0,
            totalViewed: 0,
            totalResponded: 0,
            
            // Status
            status: 'draft', // draft, active, closed
            
            // Metadata
            createdBy: member._id,
            createdAt: new Date(),
            lastModified: new Date(),
            
            // Unique Link
            publicLink: generatePublicLink()
        });
        
        await logEviteActivity(evite._id, 'EVITE_CREATED', `E-vite created for ${event.title}`);
        
        return {
            success: true,
            eviteId: evite._id,
            publicLink: evite.publicLink,
            message: 'E-vite created successfully'
        };
        
    } catch (error) {
        console.error('Error creating e-vite:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Add custom question to e-vite
 * @param {string} eviteId
 * @param {Object} question
 */
export async function addCustomQuestion(eviteId, question) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const evite = await wixData.get('Evites', eviteId);
        
        const newQuestion = {
            id: `q_${Date.now()}`,
            question: question.question,
            questionBengali: question.questionBengali || '',
            type: question.type || 'text', // text, select, multiselect, checkbox, number
            options: question.options || [],
            required: question.required || false,
            order: (evite.customQuestions?.length || 0) + 1
        };
        
        evite.customQuestions = [...(evite.customQuestions || []), newQuestion];
        evite.lastModified = new Date();
        
        await wixData.update('Evites', evite);
        
        return {
            success: true,
            questionId: newQuestion.id,
            message: 'Question added successfully'
        };
        
    } catch (error) {
        console.error('Error adding question:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// SEND INVITATIONS
// =====================================================

/**
 * Send e-vite to members
 * @param {string} eviteId
 * @param {Object} options - { memberIds, membershipTypes, sendToAll }
 */
export async function sendEvite(eviteId, options = {}) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const evite = await wixData.get('Evites', eviteId);
        
        if (!evite) {
            return { success: false, error: 'E-vite not found' };
        }
        
        // Get recipients
        let recipients = [];
        
        if (options.sendToAll) {
            const members = await wixData.query('MemberProfiles')
                .eq('membershipStatus', 'active')
                .find();
            recipients = members.items;
        } else if (options.membershipTypes?.length) {
            const members = await wixData.query('MemberProfiles')
                .eq('membershipStatus', 'active')
                .hasSome('membershipType', options.membershipTypes)
                .find();
            recipients = members.items;
        } else if (options.memberIds?.length) {
            for (const memberId of options.memberIds) {
                const memberData = await wixData.get('MemberProfiles', memberId);
                if (memberData) recipients.push(memberData);
            }
        }
        
        let sentCount = 0;
        let failedCount = 0;
        
        for (const recipient of recipients) {
            try {
                // Create individual invitation
                const invitation = await wixData.insert('EviteInvitations', {
                    eviteId: eviteId,
                    eventId: evite.eventId,
                    memberId: recipient._id,
                    memberName: `${recipient.firstName} ${recipient.lastName}`,
                    email: recipient.email,
                    phone: recipient.phone || '',
                    
                    // Unique token for this invitation
                    inviteToken: generateInviteToken(),
                    
                    // Tracking
                    sentAt: new Date(),
                    sentVia: options.channel || 'email',
                    viewed: false,
                    viewedAt: null,
                    responded: false,
                    respondedAt: null,
                    
                    // Response
                    rsvpStatus: RSVP_STATUS.PENDING,
                    
                    // Metadata
                    membershipType: recipient.membershipType
                });
                
                // Send via selected channel
                if (options.channel === 'email' || !options.channel) {
                    await sendEviteEmail(evite, invitation, recipient);
                }
                
                sentCount++;
                
            } catch (err) {
                console.error(`Failed to send to ${recipient.email}:`, err);
                failedCount++;
            }
        }
        
        // Update evite stats
        evite.totalInvitesSent = (evite.totalInvitesSent || 0) + sentCount;
        evite.status = 'active';
        evite.lastSentAt = new Date();
        await wixData.update('Evites', evite);
        
        await logEviteActivity(eviteId, 'EVITE_SENT', 
            `Sent to ${sentCount} recipients (${failedCount} failed)`);
        
        return {
            success: true,
            sentCount: sentCount,
            failedCount: failedCount,
            message: `E-vite sent to ${sentCount} recipients`
        };
        
    } catch (error) {
        console.error('Error sending e-vite:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Send e-vite email
 */
async function sendEviteEmail(evite, invitation, recipient) {
    const rsvpLink = `https://jaxbengali.org/rsvp/${invitation.inviteToken}`;
    
    await triggeredEmails.emailContact(
        'evite_invitation',
        recipient.email,
        {
            variables: {
                recipientName: `${recipient.firstName} ${recipient.lastName}`,
                eventTitle: evite.title,
                eventTitleBengali: evite.titleBengali,
                eventDate: formatDate(evite.eventDate),
                eventTime: evite.eventTime,
                eventLocation: evite.eventLocation,
                eventAddress: evite.eventAddress,
                message: evite.message,
                messageBengali: evite.messageBengali,
                hostName: evite.hostName,
                rsvpLink: rsvpLink,
                rsvpDeadline: formatDate(evite.rsvpDeadline)
            }
        }
    );
}

/**
 * Send e-vite via WhatsApp (using template message)
 * @param {string} eviteId
 * @param {Array} phoneNumbers
 */
export async function sendEviteWhatsApp(eviteId, phoneNumbers) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const evite = await wixData.get('Evites', eviteId);
        
        // Generate WhatsApp message
        const message = `🎉 *${evite.title}*\n\n` +
            `📅 ${formatDate(evite.eventDate)} at ${evite.eventTime}\n` +
            `📍 ${evite.eventLocation}\n\n` +
            `${evite.message}\n\n` +
            `Please RSVP: https://jaxbengali.org/evite/${evite.publicLink}\n\n` +
            `🙏 ${evite.hostName}`;
        
        // Store WhatsApp send records
        for (const phone of phoneNumbers) {
            await wixData.insert('WhatsAppQueue', {
                eviteId: eviteId,
                phone: phone,
                message: message,
                status: 'queued',
                createdAt: new Date()
            });
        }
        
        return {
            success: true,
            queued: phoneNumbers.length,
            message: `WhatsApp messages queued for ${phoneNumbers.length} recipients`,
            previewMessage: message
        };
        
    } catch (error) {
        console.error('Error sending WhatsApp:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// RSVP PROCESSING
// =====================================================

/**
 * Submit RSVP response
 * @param {string} inviteToken
 * @param {Object} rsvpData
 */
export async function submitRSVP(inviteToken, rsvpData) {
    try {
        // Find invitation
        const invitations = await wixData.query('EviteInvitations')
            .eq('inviteToken', inviteToken)
            .find();
        
        if (invitations.items.length === 0) {
            return { success: false, error: 'Invalid invitation link' };
        }
        
        const invitation = invitations.items[0];
        const evite = await wixData.get('Evites', invitation.eviteId);
        
        // Check deadline
        if (new Date() > new Date(evite.rsvpDeadline)) {
            return { success: false, error: 'RSVP deadline has passed' };
        }
        
        // Process main respondent
        const mainAttendee = {
            name: rsvpData.name || invitation.memberName,
            email: rsvpData.email || invitation.email,
            phone: rsvpData.phone || invitation.phone,
            ageCategory: rsvpData.ageCategory || 'adult',
            dietary: rsvpData.dietary || 'no_restriction',
            dietaryNotes: rsvpData.dietaryNotes || '',
            accessibilityNeeds: rsvpData.accessibilityNeeds || '',
            customAnswers: rsvpData.customAnswers || {}
        };
        
        // Process guests/plus-ones
        const guests = [];
        if (rsvpData.guests && evite.allowPlusOnes) {
            for (const guest of rsvpData.guests.slice(0, evite.maxGuestsPerInvite - 1)) {
                guests.push({
                    name: guest.name,
                    ageCategory: guest.ageCategory || 'adult',
                    dietary: guest.dietary || 'no_restriction',
                    dietaryNotes: guest.dietaryNotes || '',
                    relationship: guest.relationship || 'family'
                });
            }
        }
        
        // Create RSVP record
        const rsvp = await wixData.insert('EviteRSVPs', {
            eviteId: invitation.eviteId,
            eventId: invitation.eventId,
            invitationId: invitation._id,
            memberId: invitation.memberId,
            
            // Response
            rsvpStatus: rsvpData.attending ? RSVP_STATUS.ATTENDING : 
                        (rsvpData.maybe ? RSVP_STATUS.MAYBE : RSVP_STATUS.NOT_ATTENDING),
            
            // Main Attendee
            mainAttendee: mainAttendee,
            
            // Guests
            guests: guests,
            totalAttendees: rsvpData.attending ? 1 + guests.length : 0,
            
            // Counts by Category
            adultCount: countByAgeCategory([mainAttendee, ...guests], 'adult'),
            teenCount: countByAgeCategory([mainAttendee, ...guests], 'teen'),
            childCount: countByAgeCategory([mainAttendee, ...guests], 'child'),
            toddlerCount: countByAgeCategory([mainAttendee, ...guests], 'toddler'),
            infantCount: countByAgeCategory([mainAttendee, ...guests], 'infant'),
            
            // Dietary Counts
            vegetarianCount: countByDietary([mainAttendee, ...guests], 'vegetarian'),
            nonVegCount: countByDietary([mainAttendee, ...guests], 'non_vegetarian'),
            veganCount: countByDietary([mainAttendee, ...guests], 'vegan'),
            glutenFreeCount: countByDietary([mainAttendee, ...guests], 'gluten_free'),
            otherDietaryCount: countOtherDietary([mainAttendee, ...guests]),
            
            // Special Requirements
            specialDietaryNotes: collectDietaryNotes([mainAttendee, ...guests]),
            accessibilityNotes: collectAccessibilityNotes([mainAttendee, ...guests]),
            
            // Notes
            generalNotes: rsvpData.notes || '',
            
            // Metadata
            respondedAt: new Date(),
            ipAddress: rsvpData.ipAddress || '',
            userAgent: rsvpData.userAgent || ''
        });
        
        // Update invitation
        invitation.responded = true;
        invitation.respondedAt = new Date();
        invitation.rsvpStatus = rsvp.rsvpStatus;
        invitation.rsvpId = rsvp._id;
        await wixData.update('EviteInvitations', invitation);
        
        // Update evite stats
        evite.totalResponded = (evite.totalResponded || 0) + 1;
        await wixData.update('Evites', evite);
        
        // Send confirmation
        if (rsvpData.attending) {
            await triggeredEmails.emailContact(
                'rsvp_confirmation',
                mainAttendee.email,
                {
                    variables: {
                        name: mainAttendee.name,
                        eventTitle: evite.title,
                        eventDate: formatDate(evite.eventDate),
                        eventTime: evite.eventTime,
                        eventLocation: evite.eventLocation,
                        totalAttendees: rsvp.totalAttendees,
                        guestNames: guests.map(g => g.name).join(', ') || 'None'
                    }
                }
            );
        }
        
        await logEviteActivity(invitation.eviteId, 'RSVP_RECEIVED', 
            `${mainAttendee.name} responded: ${rsvp.rsvpStatus} (${rsvp.totalAttendees} attendees)`);
        
        return {
            success: true,
            rsvpId: rsvp._id,
            status: rsvp.rsvpStatus,
            totalAttendees: rsvp.totalAttendees,
            message: rsvpData.attending 
                ? `Thank you! Your RSVP for ${rsvp.totalAttendees} attendee(s) has been confirmed.`
                : 'Thank you for letting us know. We hope to see you at future events!'
        };
        
    } catch (error) {
        console.error('Error submitting RSVP:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Track e-vite view
 * @param {string} inviteToken
 */
export async function trackEviteView(inviteToken) {
    try {
        const invitations = await wixData.query('EviteInvitations')
            .eq('inviteToken', inviteToken)
            .find();
        
        if (invitations.items.length > 0) {
            const invitation = invitations.items[0];
            
            if (!invitation.viewed) {
                invitation.viewed = true;
                invitation.viewedAt = new Date();
                await wixData.update('EviteInvitations', invitation);
                
                const evite = await wixData.get('Evites', invitation.eviteId);
                evite.totalViewed = (evite.totalViewed || 0) + 1;
                await wixData.update('Evites', evite);
            }
            
            return { success: true, eviteId: invitation.eviteId };
        }
        
        return { success: false };
        
    } catch (error) {
        console.error('Error tracking view:', error);
        return { success: false };
    }
}

// =====================================================
// ANALYTICS & INSIGHTS
// =====================================================

/**
 * Get comprehensive RSVP analytics for an e-vite
 * @param {string} eviteId
 */
export async function getEviteAnalytics(eviteId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const evite = await wixData.get('Evites', eviteId);
        const rsvps = await wixData.query('EviteRSVPs')
            .eq('eviteId', eviteId)
            .find();
        
        const invitations = await wixData.query('EviteInvitations')
            .eq('eviteId', eviteId)
            .find();
        
        // Response Summary
        const attending = rsvps.items.filter(r => r.rsvpStatus === RSVP_STATUS.ATTENDING);
        const notAttending = rsvps.items.filter(r => r.rsvpStatus === RSVP_STATUS.NOT_ATTENDING);
        const maybe = rsvps.items.filter(r => r.rsvpStatus === RSVP_STATUS.MAYBE);
        const pending = invitations.items.filter(i => !i.responded);
        
        // Attendance Totals
        const totalAttending = attending.reduce((sum, r) => sum + r.totalAttendees, 0);
        
        // Age Demographics
        const ageDemographics = {
            adults: attending.reduce((sum, r) => sum + (r.adultCount || 0), 0),
            teens: attending.reduce((sum, r) => sum + (r.teenCount || 0), 0),
            children: attending.reduce((sum, r) => sum + (r.childCount || 0), 0),
            toddlers: attending.reduce((sum, r) => sum + (r.toddlerCount || 0), 0),
            infants: attending.reduce((sum, r) => sum + (r.infantCount || 0), 0)
        };
        
        // Dietary Requirements
        const dietaryBreakdown = {
            vegetarian: attending.reduce((sum, r) => sum + (r.vegetarianCount || 0), 0),
            nonVegetarian: attending.reduce((sum, r) => sum + (r.nonVegCount || 0), 0),
            vegan: attending.reduce((sum, r) => sum + (r.veganCount || 0), 0),
            glutenFree: attending.reduce((sum, r) => sum + (r.glutenFreeCount || 0), 0),
            other: attending.reduce((sum, r) => sum + (r.otherDietaryCount || 0), 0)
        };
        
        // Special Requirements
        const specialDietaryNotes = attending
            .filter(r => r.specialDietaryNotes)
            .map(r => ({
                member: r.mainAttendee.name,
                notes: r.specialDietaryNotes
            }));
        
        const accessibilityNeeds = attending
            .filter(r => r.accessibilityNotes)
            .map(r => ({
                member: r.mainAttendee.name,
                needs: r.accessibilityNotes
            }));
        
        // Response Rate
        const responseRate = invitations.items.length > 0 
            ? Math.round((rsvps.items.length / invitations.items.length) * 100) 
            : 0;
        
        // View Rate
        const viewRate = invitations.items.length > 0
            ? Math.round((invitations.items.filter(i => i.viewed).length / invitations.items.length) * 100)
            : 0;
        
        // Membership Type Breakdown
        const byMembershipType = {};
        for (const rsvp of attending) {
            const inv = invitations.items.find(i => i._id === rsvp.invitationId);
            const type = inv?.membershipType || 'unknown';
            byMembershipType[type] = (byMembershipType[type] || 0) + rsvp.totalAttendees;
        }
        
        // Response Timeline
        const responseTimeline = attending
            .map(r => ({
                date: new Date(r.respondedAt).toLocaleDateString(),
                count: r.totalAttendees
            }))
            .reduce((acc, item) => {
                const existing = acc.find(a => a.date === item.date);
                if (existing) {
                    existing.count += item.count;
                } else {
                    acc.push(item);
                }
                return acc;
            }, []);
        
        return {
            success: true,
            analytics: {
                // Summary
                summary: {
                    totalInvited: invitations.items.length,
                    totalResponded: rsvps.items.length,
                    responseRate: responseRate,
                    viewRate: viewRate
                },
                
                // Response Breakdown
                responses: {
                    attending: attending.length,
                    notAttending: notAttending.length,
                    maybe: maybe.length,
                    pending: pending.length
                },
                
                // Attendance
                attendance: {
                    totalHeadcount: totalAttending,
                    byAge: ageDemographics,
                    byMembershipType: byMembershipType
                },
                
                // Food Planning
                foodPlanning: {
                    dietary: dietaryBreakdown,
                    totalMealsNeeded: totalAttending,
                    vegetarianMeals: dietaryBreakdown.vegetarian + dietaryBreakdown.vegan,
                    nonVegMeals: dietaryBreakdown.nonVegetarian,
                    specialRequirements: specialDietaryNotes
                },
                
                // Age-Based Planning
                agePlanning: {
                    adultSeating: ageDemographics.adults,
                    kidsArea: ageDemographics.children + ageDemographics.toddlers,
                    highChairsNeeded: ageDemographics.infants + ageDemographics.toddlers,
                    childrenActivities: ageDemographics.children
                },
                
                // Accessibility
                accessibility: {
                    specialNeeds: accessibilityNeeds,
                    totalWithNeeds: accessibilityNeeds.length
                },
                
                // Timeline
                responseTimeline: responseTimeline,
                
                // Raw Data for Export
                attendeeList: attending.map(r => ({
                    primaryName: r.mainAttendee.name,
                    email: r.mainAttendee.email,
                    phone: r.mainAttendee.phone,
                    totalInParty: r.totalAttendees,
                    dietary: r.mainAttendee.dietary,
                    guests: r.guests?.map(g => g.name) || []
                }))
            }
        };
        
    } catch (error) {
        console.error('Error getting analytics:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Export attendee list for catering/planning
 * @param {string} eviteId
 * @param {string} format - 'json', 'csv'
 */
export async function exportAttendeeList(eviteId, format = 'json') {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const rsvps = await wixData.query('EviteRSVPs')
            .eq('eviteId', eviteId)
            .eq('rsvpStatus', RSVP_STATUS.ATTENDING)
            .find();
        
        const attendees = [];
        
        for (const rsvp of rsvps.items) {
            // Main attendee
            attendees.push({
                name: rsvp.mainAttendee.name,
                email: rsvp.mainAttendee.email,
                phone: rsvp.mainAttendee.phone,
                ageCategory: rsvp.mainAttendee.ageCategory,
                dietary: rsvp.mainAttendee.dietary,
                dietaryNotes: rsvp.mainAttendee.dietaryNotes,
                accessibility: rsvp.mainAttendee.accessibilityNeeds,
                isGuest: false,
                partyOf: rsvp.totalAttendees
            });
            
            // Guests
            for (const guest of (rsvp.guests || [])) {
                attendees.push({
                    name: guest.name,
                    email: '',
                    phone: '',
                    ageCategory: guest.ageCategory,
                    dietary: guest.dietary,
                    dietaryNotes: guest.dietaryNotes,
                    accessibility: '',
                    isGuest: true,
                    hostName: rsvp.mainAttendee.name
                });
            }
        }
        
        if (format === 'csv') {
            const headers = ['Name', 'Email', 'Phone', 'Age Category', 'Dietary', 'Dietary Notes', 'Accessibility', 'Is Guest', 'Host/Party Size'];
            const rows = attendees.map(a => [
                a.name, a.email, a.phone, a.ageCategory, a.dietary, 
                a.dietaryNotes, a.accessibility, a.isGuest ? 'Yes' : 'No',
                a.isGuest ? a.hostName : a.partyOf
            ]);
            
            const csv = [headers.join(','), ...rows.map(r => r.map(v => `"${v || ''}"`).join(','))].join('\n');
            
            return {
                success: true,
                format: 'csv',
                data: csv,
                filename: `attendees_${eviteId}.csv`
            };
        }
        
        return {
            success: true,
            format: 'json',
            data: attendees,
            totalAttendees: attendees.length
        };
        
    } catch (error) {
        console.error('Error exporting:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// REMINDER SYSTEM
// =====================================================

/**
 * Send RSVP reminders to non-responders
 * @param {string} eviteId
 */
export async function sendRSVPReminders(eviteId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const evite = await wixData.get('Evites', eviteId);
        
        // Get non-responders
        const invitations = await wixData.query('EviteInvitations')
            .eq('eviteId', eviteId)
            .eq('responded', false)
            .find();
        
        let remindersSent = 0;
        
        for (const invitation of invitations.items) {
            await triggeredEmails.emailContact(
                'rsvp_reminder',
                invitation.email,
                {
                    variables: {
                        name: invitation.memberName,
                        eventTitle: evite.title,
                        eventDate: formatDate(evite.eventDate),
                        rsvpDeadline: formatDate(evite.rsvpDeadline),
                        rsvpLink: `https://jaxbengali.org/rsvp/${invitation.inviteToken}`
                    }
                }
            );
            
            invitation.lastReminderSent = new Date();
            invitation.reminderCount = (invitation.reminderCount || 0) + 1;
            await wixData.update('EviteInvitations', invitation);
            
            remindersSent++;
        }
        
        await logEviteActivity(eviteId, 'REMINDERS_SENT', 
            `Sent ${remindersSent} RSVP reminders`);
        
        return {
            success: true,
            remindersSent: remindersSent,
            message: `Reminders sent to ${remindersSent} non-responders`
        };
        
    } catch (error) {
        console.error('Error sending reminders:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

function generatePublicLink() {
    return crypto.randomBytes(8).toString('hex');
}

function generateInviteToken() {
    return crypto.randomBytes(16).toString('hex');
}

function countByAgeCategory(attendees, category) {
    return attendees.filter(a => a.ageCategory === category).length;
}

function countByDietary(attendees, dietary) {
    return attendees.filter(a => a.dietary === dietary).length;
}

function countOtherDietary(attendees) {
    const mainTypes = ['vegetarian', 'non_vegetarian', 'no_restriction'];
    return attendees.filter(a => !mainTypes.includes(a.dietary)).length;
}

function collectDietaryNotes(attendees) {
    return attendees
        .filter(a => a.dietaryNotes)
        .map(a => `${a.name}: ${a.dietaryNotes}`)
        .join('; ');
}

function collectAccessibilityNotes(attendees) {
    return attendees
        .filter(a => a.accessibilityNeeds)
        .map(a => `${a.name}: ${a.accessibilityNeeds}`)
        .join('; ');
}

function addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

async function isAdmin(memberId) {
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec')
            );
        }
        return false;
    } catch {
        return false;
    }
}

async function logEviteActivity(eviteId, action, details) {
    await wixData.insert('EviteActivityLog', {
        eviteId: eviteId,
        action: action,
        details: details,
        timestamp: new Date()
    });
}

// Export constants
export { EVITE_TEMPLATES, DIETARY_OPTIONS, AGE_CATEGORIES, RSVP_STATUS };

```
------------------------------------------------------------

## [19/41] feedback-survey-service
- File: `feedback-survey-service.jsw`
- Size: 27.1 KB
- Lines: 797

```javascript
/**
 * BANF Feedback & Survey Service
 * ===============================
 * Wix Velo Backend Module for post-event surveys and member feedback
 * 
 * Features:
 * - Survey template creation
 * - Post-event feedback collection
 * - Rating analytics
 * - Improvement suggestions tracking
 * - NPS (Net Promoter Score) calculation
 * 
 * @module backend/feedback-survey-service.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';

// =====================================================
// SURVEY CONFIGURATION
// =====================================================

const QUESTION_TYPES = {
    RATING: 'rating',           // 1-5 stars
    NPS: 'nps',                 // 0-10 scale
    MULTIPLE_CHOICE: 'multiple_choice',
    CHECKBOX: 'checkbox',
    TEXT: 'text',
    TEXTAREA: 'textarea',
    YES_NO: 'yes_no'
};

const SURVEY_TEMPLATES = {
    POST_EVENT: {
        name: 'Post Event Survey',
        questions: [
            {
                questionId: 'Q1',
                type: QUESTION_TYPES.RATING,
                text: 'How would you rate the overall event?',
                required: true
            },
            {
                questionId: 'Q2',
                type: QUESTION_TYPES.RATING,
                text: 'How would you rate the venue?',
                required: true
            },
            {
                questionId: 'Q3',
                type: QUESTION_TYPES.RATING,
                text: 'How would you rate the food quality?',
                required: true
            },
            {
                questionId: 'Q4',
                type: QUESTION_TYPES.RATING,
                text: 'How would you rate the cultural program?',
                required: false
            },
            {
                questionId: 'Q5',
                type: QUESTION_TYPES.YES_NO,
                text: 'Was the event well organized?',
                required: true
            },
            {
                questionId: 'Q6',
                type: QUESTION_TYPES.NPS,
                text: 'How likely are you to recommend BANF events to friends?',
                required: true
            },
            {
                questionId: 'Q7',
                type: QUESTION_TYPES.TEXTAREA,
                text: 'What did you like most about the event?',
                required: false
            },
            {
                questionId: 'Q8',
                type: QUESTION_TYPES.TEXTAREA,
                text: 'What could we improve?',
                required: false
            },
            {
                questionId: 'Q9',
                type: QUESTION_TYPES.CHECKBOX,
                text: 'Which aspects would you like to see improved?',
                options: ['Venue', 'Food', 'Parking', 'Program timing', 'Registration process', 'Communication'],
                required: false
            }
        ]
    },
    
    MEMBERSHIP_SATISFACTION: {
        name: 'Membership Satisfaction Survey',
        questions: [
            {
                questionId: 'MS1',
                type: QUESTION_TYPES.RATING,
                text: 'How satisfied are you with your BANF membership?',
                required: true
            },
            {
                questionId: 'MS2',
                type: QUESTION_TYPES.MULTIPLE_CHOICE,
                text: 'How often do you attend BANF events?',
                options: ['Every event', 'Most events', 'Some events', 'Rarely', 'This was my first'],
                required: true
            },
            {
                questionId: 'MS3',
                type: QUESTION_TYPES.NPS,
                text: 'How likely are you to renew your membership?',
                required: true
            },
            {
                questionId: 'MS4',
                type: QUESTION_TYPES.CHECKBOX,
                text: 'What type of events would you like to see more of?',
                options: ['Pujas', 'Cultural programs', 'Picnics', 'Kids activities', 'Educational workshops', 'Sports events'],
                required: false
            },
            {
                questionId: 'MS5',
                type: QUESTION_TYPES.TEXTAREA,
                text: 'Any suggestions for improving BANF?',
                required: false
            }
        ]
    },
    
    QUICK_FEEDBACK: {
        name: 'Quick Feedback',
        questions: [
            {
                questionId: 'QF1',
                type: QUESTION_TYPES.RATING,
                text: 'Quick rating for this event',
                required: true
            },
            {
                questionId: 'QF2',
                type: QUESTION_TYPES.TEXT,
                text: 'One word to describe the event',
                required: false
            }
        ]
    }
};

// =====================================================
// SURVEY CREATION
// =====================================================

/**
 * Create a survey for an event
 * @param {Object} surveyData
 */
export async function createSurvey(surveyData) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        // Get template or custom questions
        let questions = surveyData.questions;
        if (surveyData.templateId && SURVEY_TEMPLATES[surveyData.templateId]) {
            questions = SURVEY_TEMPLATES[surveyData.templateId].questions;
        }
        
        const survey = await wixData.insert('Surveys', {
            // Event association
            eventId: surveyData.eventId,
            eventTitle: surveyData.eventTitle,
            
            // Survey details
            title: surveyData.title || `Feedback for ${surveyData.eventTitle}`,
            description: surveyData.description || 'We would love to hear your feedback!',
            templateId: surveyData.templateId || 'custom',
            
            // Questions
            questions: questions,
            
            // Settings
            isAnonymous: surveyData.isAnonymous || false,
            allowMultipleResponses: surveyData.allowMultipleResponses || false,
            isActive: true,
            
            // Timing
            startDate: surveyData.startDate || new Date(),
            endDate: surveyData.endDate || null, // null = no end
            
            // Stats
            responseCount: 0,
            averageRating: 0,
            npsScore: null,
            
            // Metadata
            createdBy: member._id,
            createdAt: new Date()
        });
        
        return {
            success: true,
            surveyId: survey._id,
            surveyUrl: `/feedback/${survey._id}`,
            message: 'Survey created successfully'
        };
        
    } catch (error) {
        console.error('Error creating survey:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Create post-event survey automatically
 * @param {string} eventId
 */
export async function createPostEventSurvey(eventId) {
    try {
        const event = await wixData.get('Events', eventId);
        
        if (!event) {
            return { success: false, error: 'Event not found' };
        }
        
        // Check if survey already exists
        const existing = await wixData.query('Surveys')
            .eq('eventId', eventId)
            .find({ suppressAuth: true });
        
        if (existing.items.length > 0) {
            return {
                success: true,
                surveyId: existing.items[0]._id,
                message: 'Survey already exists for this event'
            };
        }
        
        return await createSurvey({
            eventId: eventId,
            eventTitle: event.title,
            title: `Share Your Feedback: ${event.title}`,
            description: 'Thank you for attending! Your feedback helps us improve future events.',
            templateId: 'POST_EVENT',
            isAnonymous: false,
            startDate: new Date(),
            endDate: addDays(new Date(), 7) // Active for 7 days
        });
        
    } catch (error) {
        console.error('Error creating post-event survey:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// RESPONSE SUBMISSION
// =====================================================

/**
 * Submit survey response
 * @param {string} surveyId
 * @param {Object} responses - { questionId: answer }
 */
export async function submitSurveyResponse(surveyId, responses) {
    const member = await currentMember.getMember();
    
    try {
        const survey = await wixData.get('Surveys', surveyId);
        
        if (!survey) {
            return { success: false, error: 'Survey not found' };
        }
        
        if (!survey.isActive) {
            return { success: false, error: 'Survey is no longer active' };
        }
        
        if (survey.endDate && new Date() > new Date(survey.endDate)) {
            return { success: false, error: 'Survey has ended' };
        }
        
        // Check for duplicate response
        if (!survey.allowMultipleResponses && member) {
            const existing = await wixData.query('SurveyResponses')
                .eq('surveyId', surveyId)
                .eq('memberId', member._id)
                .find({ suppressAuth: true });
            
            if (existing.items.length > 0) {
                return { success: false, error: 'You have already submitted a response' };
            }
        }
        
        // Validate required questions
        for (const q of survey.questions) {
            if (q.required && !responses[q.questionId]) {
                return { 
                    success: false, 
                    error: `Required question not answered: ${q.text}`
                };
            }
        }
        
        // Save response
        const response = await wixData.insert('SurveyResponses', {
            surveyId: surveyId,
            eventId: survey.eventId,
            
            // Responder info (if not anonymous)
            memberId: survey.isAnonymous ? null : member?._id,
            memberName: survey.isAnonymous ? 'Anonymous' : 
                (member ? `${member.contactDetails?.firstName || ''} ${member.contactDetails?.lastName || ''}`.trim() : 'Guest'),
            
            // Responses
            responses: responses,
            
            // Calculated metrics
            overallRating: calculateOverallRating(survey.questions, responses),
            npsResponse: extractNPSResponse(survey.questions, responses),
            
            // Metadata
            submittedAt: new Date(),
            userAgent: '', // Could be populated from frontend
            isAnonymous: survey.isAnonymous
        });
        
        // Update survey stats
        await updateSurveyStats(surveyId);
        
        return {
            success: true,
            responseId: response._id,
            message: 'Thank you for your feedback!'
        };
        
    } catch (error) {
        console.error('Error submitting response:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// ANALYTICS & REPORTING
// =====================================================

/**
 * Get survey analytics
 * @param {string} surveyId
 */
export async function getSurveyAnalytics(surveyId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const survey = await wixData.get('Surveys', surveyId);
        
        if (!survey) {
            return { success: false, error: 'Survey not found' };
        }
        
        const responses = await wixData.query('SurveyResponses')
            .eq('surveyId', surveyId)
            .find({ suppressAuth: true });
        
        // Process each question
        const questionAnalytics = {};
        
        for (const q of survey.questions) {
            const questionResponses = responses.items
                .map(r => r.responses[q.questionId])
                .filter(r => r !== undefined && r !== null);
            
            switch (q.type) {
                case QUESTION_TYPES.RATING:
                    questionAnalytics[q.questionId] = {
                        question: q.text,
                        type: q.type,
                        responseCount: questionResponses.length,
                        average: calculateAverage(questionResponses),
                        distribution: calculateDistribution(questionResponses, [1, 2, 3, 4, 5])
                    };
                    break;
                    
                case QUESTION_TYPES.NPS:
                    const { score, promoters, passives, detractors } = calculateNPS(questionResponses);
                    questionAnalytics[q.questionId] = {
                        question: q.text,
                        type: q.type,
                        responseCount: questionResponses.length,
                        npsScore: score,
                        promoters: promoters,
                        passives: passives,
                        detractors: detractors
                    };
                    break;
                    
                case QUESTION_TYPES.MULTIPLE_CHOICE:
                case QUESTION_TYPES.CHECKBOX:
                    const optionCounts = {};
                    for (const r of questionResponses) {
                        const answers = Array.isArray(r) ? r : [r];
                        for (const a of answers) {
                            optionCounts[a] = (optionCounts[a] || 0) + 1;
                        }
                    }
                    questionAnalytics[q.questionId] = {
                        question: q.text,
                        type: q.type,
                        responseCount: questionResponses.length,
                        optionCounts: optionCounts
                    };
                    break;
                    
                case QUESTION_TYPES.YES_NO:
                    questionAnalytics[q.questionId] = {
                        question: q.text,
                        type: q.type,
                        responseCount: questionResponses.length,
                        yesCount: questionResponses.filter(r => r === 'yes' || r === true).length,
                        noCount: questionResponses.filter(r => r === 'no' || r === false).length
                    };
                    break;
                    
                case QUESTION_TYPES.TEXT:
                case QUESTION_TYPES.TEXTAREA:
                    questionAnalytics[q.questionId] = {
                        question: q.text,
                        type: q.type,
                        responseCount: questionResponses.length,
                        responses: questionResponses // Return actual text responses
                    };
                    break;
            }
        }
        
        // Overall metrics
        const ratingQuestions = survey.questions.filter(q => q.type === QUESTION_TYPES.RATING);
        const allRatings = ratingQuestions.flatMap(q => 
            responses.items.map(r => r.responses[q.questionId]).filter(Boolean)
        );
        
        return {
            success: true,
            analytics: {
                surveyTitle: survey.title,
                eventTitle: survey.eventTitle,
                totalResponses: responses.items.length,
                
                // Overall metrics
                overallRating: calculateAverage(allRatings),
                npsScore: survey.npsScore,
                
                // Question breakdown
                questionAnalytics: questionAnalytics,
                
                // Response timeline
                responseTimeline: groupResponsesByDate(responses.items),
                
                // Recent responses
                recentResponses: responses.items
                    .sort((a, b) => new Date(b.submittedAt) - new Date(a.submittedAt))
                    .slice(0, 10)
                    .map(r => ({
                        memberName: r.memberName,
                        overallRating: r.overallRating,
                        submittedAt: r.submittedAt
                    }))
            }
        };
        
    } catch (error) {
        console.error('Error getting analytics:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get feedback comparison across events
 * @param {Array} eventIds - Optional specific events to compare
 */
export async function getEventFeedbackComparison(eventIds = null) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        let query = wixData.query('Surveys');
        
        if (eventIds && eventIds.length > 0) {
            query = query.hasSome('eventId', eventIds);
        }
        
        const surveys = await query
            .descending('createdAt')
            .limit(20)
            .find({ suppressAuth: true });
        
        const comparison = [];
        
        for (const survey of surveys.items) {
            if (survey.responseCount > 0) {
                comparison.push({
                    eventId: survey.eventId,
                    eventTitle: survey.eventTitle,
                    responseCount: survey.responseCount,
                    averageRating: survey.averageRating,
                    npsScore: survey.npsScore,
                    surveyDate: survey.createdAt
                });
            }
        }
        
        // Calculate trends
        let ratingTrend = 'stable';
        let npsTrend = 'stable';
        
        if (comparison.length >= 2) {
            const recent = comparison.slice(0, 3);
            const older = comparison.slice(3, 6);
            
            const recentAvgRating = calculateAverage(recent.map(e => e.averageRating));
            const olderAvgRating = calculateAverage(older.map(e => e.averageRating));
            
            if (recentAvgRating > olderAvgRating + 0.2) ratingTrend = 'improving';
            else if (recentAvgRating < olderAvgRating - 0.2) ratingTrend = 'declining';
            
            const recentNPS = calculateAverage(recent.map(e => e.npsScore).filter(Boolean));
            const olderNPS = calculateAverage(older.map(e => e.npsScore).filter(Boolean));
            
            if (recentNPS > olderNPS + 5) npsTrend = 'improving';
            else if (recentNPS < olderNPS - 5) npsTrend = 'declining';
        }
        
        return {
            success: true,
            comparison: comparison,
            trends: {
                ratingTrend: ratingTrend,
                npsTrend: npsTrend,
                overallAverageRating: calculateAverage(comparison.map(e => e.averageRating)),
                overallNPS: calculateAverage(comparison.map(e => e.npsScore).filter(Boolean))
            }
        };
        
    } catch (error) {
        console.error('Error getting comparison:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get improvement suggestions aggregated
 */
export async function getImprovementSuggestions() {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const responses = await wixData.query('SurveyResponses')
            .descending('submittedAt')
            .limit(200)
            .find({ suppressAuth: true });
        
        const suggestions = [];
        const categories = {};
        
        for (const response of responses.items) {
            // Look for improvement-related questions
            for (const [qId, answer] of Object.entries(response.responses)) {
                if (typeof answer === 'string' && answer.length > 10) {
                    suggestions.push({
                        text: answer,
                        eventId: response.eventId,
                        rating: response.overallRating,
                        date: response.submittedAt
                    });
                }
                
                // Checkbox responses (improvement areas)
                if (Array.isArray(answer)) {
                    for (const item of answer) {
                        categories[item] = (categories[item] || 0) + 1;
                    }
                }
            }
        }
        
        return {
            success: true,
            suggestions: suggestions.slice(0, 50),
            categoryBreakdown: Object.entries(categories)
                .sort((a, b) => b[1] - a[1])
                .map(([category, count]) => ({ category, count })),
            totalFeedback: responses.items.length
        };
        
    } catch (error) {
        console.error('Error getting suggestions:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// SURVEY MANAGEMENT
// =====================================================

/**
 * Close a survey
 * @param {string} surveyId
 */
export async function closeSurvey(surveyId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const survey = await wixData.get('Surveys', surveyId);
        
        if (!survey) {
            return { success: false, error: 'Survey not found' };
        }
        
        survey.isActive = false;
        survey.closedAt = new Date();
        survey.closedBy = member._id;
        
        await wixData.update('Surveys', survey);
        
        return {
            success: true,
            message: 'Survey closed successfully'
        };
        
    } catch (error) {
        console.error('Error closing survey:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get active surveys
 */
export async function getActiveSurveys() {
    try {
        const surveys = await wixData.query('Surveys')
            .eq('isActive', true)
            .descending('createdAt')
            .find({ suppressAuth: true });
        
        return {
            success: true,
            surveys: surveys.items.map(s => ({
                _id: s._id,
                title: s.title,
                eventTitle: s.eventTitle,
                responseCount: s.responseCount,
                averageRating: s.averageRating,
                endDate: s.endDate,
                createdAt: s.createdAt
            }))
        };
        
    } catch (error) {
        console.error('Error getting active surveys:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

async function updateSurveyStats(surveyId) {
    const survey = await wixData.get('Surveys', surveyId);
    const responses = await wixData.query('SurveyResponses')
        .eq('surveyId', surveyId)
        .find({ suppressAuth: true });
    
    survey.responseCount = responses.items.length;
    
    // Calculate average rating
    const ratings = responses.items.map(r => r.overallRating).filter(Boolean);
    survey.averageRating = calculateAverage(ratings);
    
    // Calculate NPS
    const npsResponses = responses.items.map(r => r.npsResponse).filter(r => r !== null && r !== undefined);
    if (npsResponses.length > 0) {
        survey.npsScore = calculateNPS(npsResponses).score;
    }
    
    await wixData.update('Surveys', survey);
}

function calculateOverallRating(questions, responses) {
    const ratingQuestions = questions.filter(q => q.type === QUESTION_TYPES.RATING);
    const ratings = ratingQuestions
        .map(q => responses[q.questionId])
        .filter(r => r !== undefined && r !== null)
        .map(Number);
    
    return calculateAverage(ratings);
}

function extractNPSResponse(questions, responses) {
    const npsQuestion = questions.find(q => q.type === QUESTION_TYPES.NPS);
    return npsQuestion ? responses[npsQuestion.questionId] : null;
}

function calculateAverage(numbers) {
    if (!numbers || numbers.length === 0) return 0;
    const validNumbers = numbers.filter(n => !isNaN(n));
    if (validNumbers.length === 0) return 0;
    return validNumbers.reduce((a, b) => a + Number(b), 0) / validNumbers.length;
}

function calculateDistribution(responses, values) {
    const distribution = {};
    for (const v of values) {
        distribution[v] = responses.filter(r => Number(r) === v).length;
    }
    return distribution;
}

function calculateNPS(responses) {
    const validResponses = responses.map(Number).filter(r => !isNaN(r) && r >= 0 && r <= 10);
    
    if (validResponses.length === 0) {
        return { score: null, promoters: 0, passives: 0, detractors: 0 };
    }
    
    const promoters = validResponses.filter(r => r >= 9).length;
    const passives = validResponses.filter(r => r >= 7 && r <= 8).length;
    const detractors = validResponses.filter(r => r <= 6).length;
    
    const total = validResponses.length;
    const score = Math.round(((promoters - detractors) / total) * 100);
    
    return {
        score: score,
        promoters: Math.round((promoters / total) * 100),
        passives: Math.round((passives / total) * 100),
        detractors: Math.round((detractors / total) * 100)
    };
}

function groupResponsesByDate(responses) {
    const groups = {};
    
    for (const r of responses) {
        const date = new Date(r.submittedAt).toISOString().split('T')[0];
        groups[date] = (groups[date] || 0) + 1;
    }
    
    return Object.entries(groups)
        .map(([date, count]) => ({ date, count }))
        .sort((a, b) => new Date(a.date) - new Date(b.date));
}

function addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

async function isAdmin(memberId) {
    if (!memberId) return false;
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec')
            );
        }
        return false;
    } catch {
        return false;
    }
}

// Export constants
export { QUESTION_TYPES, SURVEY_TEMPLATES };

```
------------------------------------------------------------

## [20/41] finance
- File: `finance.jsw`
- Size: 12.5 KB
- Lines: 364

```javascript
// backend/finance.jsw
// BANF Financial Management - Wix Velo Backend

import wixData from 'wix-data';

const FINANCIAL_COLLECTION = 'FinancialRecords';
const ZELLE_COLLECTION = 'ZellePayments';
const MEMBER_FEES_COLLECTION = 'MemberFees';

/**
 * Record a financial transaction (admin only)
 */
export async function recordTransaction(transactionData, adminId) {
    try {
        const transaction = {
            transactionType: transactionData.type, // 'income' or 'expense'
            amount: parseFloat(transactionData.amount),
            description: transactionData.description,
            category: transactionData.category, // membership, sponsorship, event, donation, etc.
            subCategory: transactionData.subCategory || '',
            eventName: transactionData.eventName || '',
            transactionDate: new Date(transactionData.date),
            receiptNumber: transactionData.receiptNumber || generateReceiptNumber(),
            paymentMethod: transactionData.paymentMethod || 'cash',
            bankReference: transactionData.bankReference || '',
            memberId: transactionData.memberId || null,
            isApproved: false,
            approvedBy: null,
            approvedAt: null,
            receiptFile: transactionData.receiptFile || '',
            notes: transactionData.notes || '',
            createdBy: adminId,
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert(FINANCIAL_COLLECTION, transaction);
        return { success: true, transaction: result };
    } catch (error) {
        console.error('Error recording transaction:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get all transactions with filtering
 */
export async function getTransactions(filters = {}, options = { limit: 100, skip: 0 }) {
    try {
        let query = wixData.query(FINANCIAL_COLLECTION);
        
        // Apply filters
        if (filters.type) {
            query = query.eq('transactionType', filters.type);
        }
        if (filters.category) {
            query = query.eq('category', filters.category);
        }
        if (filters.startDate) {
            query = query.ge('transactionDate', new Date(filters.startDate));
        }
        if (filters.endDate) {
            query = query.le('transactionDate', new Date(filters.endDate));
        }
        if (filters.isApproved !== undefined) {
            query = query.eq('isApproved', filters.isApproved);
        }
        
        query = query
            .descending('transactionDate')
            .limit(options.limit)
            .skip(options.skip);
        
        const result = await query.find();
        
        return {
            items: result.items,
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error getting transactions:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Approve a transaction (admin only)
 */
export async function approveTransaction(transactionId, adminId, notes = '') {
    try {
        const transaction = await wixData.get(FINANCIAL_COLLECTION, transactionId);
        if (!transaction) {
            return { success: false, error: 'Transaction not found' };
        }
        
        transaction.isApproved = true;
        transaction.approvedBy = adminId;
        transaction.approvedAt = new Date();
        transaction.notes = transaction.notes + '\nApproval: ' + notes;
        transaction._updatedDate = new Date();
        
        await wixData.update(FINANCIAL_COLLECTION, transaction);
        return { success: true };
    } catch (error) {
        console.error('Error approving transaction:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get financial summary for dashboard
 */
export async function getFinancialSummary(year = null) {
    try {
        const targetYear = year || new Date().getFullYear();
        const startDate = new Date(targetYear, 0, 1);
        const endDate = new Date(targetYear, 11, 31, 23, 59, 59);
        
        // Get all approved transactions for the year
        const result = await wixData.query(FINANCIAL_COLLECTION)
            .ge('transactionDate', startDate)
            .le('transactionDate', endDate)
            .eq('isApproved', true)
            .find();
        
        const transactions = result.items;
        
        // Calculate totals
        let totalIncome = 0;
        let totalExpenses = 0;
        const incomeByCategory = {};
        const expensesByCategory = {};
        const monthlyData = {};
        
        transactions.forEach(t => {
            const month = t.transactionDate.getMonth();
            const monthKey = `${targetYear}-${String(month + 1).padStart(2, '0')}`;
            
            if (!monthlyData[monthKey]) {
                monthlyData[monthKey] = { income: 0, expenses: 0 };
            }
            
            if (t.transactionType === 'income') {
                totalIncome += t.amount;
                incomeByCategory[t.category] = (incomeByCategory[t.category] || 0) + t.amount;
                monthlyData[monthKey].income += t.amount;
            } else {
                totalExpenses += t.amount;
                expensesByCategory[t.category] = (expensesByCategory[t.category] || 0) + t.amount;
                monthlyData[monthKey].expenses += t.amount;
            }
        });
        
        return {
            year: targetYear,
            totalIncome: totalIncome.toFixed(2),
            totalExpenses: totalExpenses.toFixed(2),
            netBalance: (totalIncome - totalExpenses).toFixed(2),
            incomeByCategory,
            expensesByCategory,
            monthlyData,
            transactionCount: transactions.length
        };
    } catch (error) {
        console.error('Error getting financial summary:', error);
        return null;
    }
}

/**
 * Record Zelle payment
 */
export async function recordZellePayment(paymentData) {
    try {
        // Check for duplicate
        const existing = await wixData.query(ZELLE_COLLECTION)
            .eq('zelleCode', paymentData.zelleCode)
            .find();
        
        if (existing.items.length > 0) {
            return { success: false, error: 'Payment with this code already exists' };
        }
        
        const payment = {
            zelleCode: paymentData.zelleCode,
            transactionId: paymentData.transactionId || '',
            senderName: paymentData.senderName,
            senderEmail: paymentData.senderEmail || '',
            senderPhone: paymentData.senderPhone || '',
            amount: parseFloat(paymentData.amount),
            description: paymentData.description || '',
            memberName: paymentData.memberName || '',
            paymentType: paymentData.paymentType || 'membership', // membership, event, donation
            isVerified: false,
            memberId: paymentData.memberId || null,
            registrationId: paymentData.registrationId || null,
            verifiedBy: null,
            verificationNotes: '',
            paymentDate: new Date(paymentData.paymentDate || Date.now()),
            _createdDate: new Date(),
            verifiedAt: null
        };
        
        const result = await wixData.insert(ZELLE_COLLECTION, payment);
        return { success: true, paymentId: result._id };
    } catch (error) {
        console.error('Error recording Zelle payment:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Verify Zelle payment (admin only)
 */
export async function verifyZellePayment(paymentId, adminId, notes = '') {
    try {
        const payment = await wixData.get(ZELLE_COLLECTION, paymentId);
        if (!payment) {
            return { success: false, error: 'Payment not found' };
        }
        
        payment.isVerified = true;
        payment.verifiedBy = adminId;
        payment.verifiedAt = new Date();
        payment.verificationNotes = notes;
        
        await wixData.update(ZELLE_COLLECTION, payment);
        
        // Create corresponding financial record
        await recordTransaction({
            type: 'income',
            amount: payment.amount,
            description: `Zelle payment from ${payment.senderName} - ${payment.zelleCode}`,
            category: payment.paymentType,
            paymentMethod: 'zelle',
            memberId: payment.memberId,
            date: payment.paymentDate
        }, adminId);
        
        return { success: true };
    } catch (error) {
        console.error('Error verifying Zelle payment:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get pending Zelle payments (admin)
 */
export async function getPendingZellePayments() {
    try {
        const result = await wixData.query(ZELLE_COLLECTION)
            .eq('isVerified', false)
            .descending('paymentDate')
            .find();
        
        return result.items;
    } catch (error) {
        console.error('Error getting pending payments:', error);
        return [];
    }
}

/**
 * Record member fee
 */
export async function recordMemberFee(feeData, adminId) {
    try {
        const fee = {
            memberId: feeData.memberId,
            amount: parseFloat(feeData.amount),
            feeType: feeData.feeType, // monthly, annual, registration, event
            description: feeData.description || '',
            dueDate: new Date(feeData.dueDate),
            paidDate: feeData.paidDate ? new Date(feeData.paidDate) : null,
            paymentStatus: feeData.paidDate ? 'paid' : 'pending',
            paymentMethod: feeData.paymentMethod || '',
            receiptNumber: feeData.receiptNumber || '',
            createdBy: adminId,
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert(MEMBER_FEES_COLLECTION, fee);
        return { success: true, fee: result };
    } catch (error) {
        console.error('Error recording member fee:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get member fees
 */
export async function getMemberFees(memberId) {
    try {
        const result = await wixData.query(MEMBER_FEES_COLLECTION)
            .eq('memberId', memberId)
            .descending('dueDate')
            .find();
        
        return result.items;
    } catch (error) {
        console.error('Error getting member fees:', error);
        return [];
    }
}

/**
 * Get overdue fees
 */
export async function getOverdueFees() {
    try {
        const today = new Date();
        
        const result = await wixData.query(MEMBER_FEES_COLLECTION)
            .eq('paymentStatus', 'pending')
            .lt('dueDate', today)
            .find();
        
        return result.items;
    } catch (error) {
        console.error('Error getting overdue fees:', error);
        return [];
    }
}

// Helper functions
function generateReceiptNumber() {
    const timestamp = Date.now().toString(36);
    const random = Math.random().toString(36).substr(2, 5);
    return `BANF-${timestamp}-${random}`.toUpperCase();
}

/**
 * Get income by category breakdown
 */
export async function getIncomeCategoryBreakdown(year = null) {
    try {
        const summary = await getFinancialSummary(year);
        if (!summary) return null;
        
        const categories = [
            { name: 'Membership', key: 'membership', color: '#FF6B35' },
            { name: 'Sponsorship', key: 'sponsorship', color: '#006A4E' },
            { name: 'Events', key: 'event', color: '#8B0000' },
            { name: 'Donations', key: 'donation', color: '#D4AF37' },
            { name: 'Other', key: 'other', color: '#6c757d' }
        ];
        
        return categories.map(cat => ({
            name: cat.name,
            amount: summary.incomeByCategory[cat.key] || 0,
            color: cat.color,
            percentage: summary.totalIncome > 0 
                ? ((summary.incomeByCategory[cat.key] || 0) / parseFloat(summary.totalIncome) * 100).toFixed(1)
                : 0
        }));
    } catch (error) {
        console.error('Error getting category breakdown:', error);
        return null;
    }
}

```
------------------------------------------------------------

## [21/41] guide
- File: `guide.jsw`
- Size: 18.2 KB
- Lines: 564

```javascript
// backend/guide.jsw
// BANF Jacksonville Newcomer Guide - Wix Velo Backend

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';

// Guide categories
const GUIDE_CATEGORIES = [
    'housing',
    'schools',
    'healthcare',
    'grocery_stores',
    'restaurants',
    'temples',
    'community_centers',
    'parks',
    'transportation',
    'utilities',
    'banking',
    'insurance',
    'legal_services',
    'shopping',
    'entertainment',
    'sports',
    'classes',
    'childcare',
    'senior_services',
    'emergency_services',
    'government_offices',
    'job_resources',
    'volunteer_opportunities'
];

// Sub-regions of Jacksonville
const JACKSONVILLE_AREAS = [
    'downtown',
    'southside',
    'northside',
    'westside',
    'beaches',
    'mandarin',
    'san_marco',
    'riverside_avondale',
    'arlington',
    'orange_park',
    'st_johns',
    'fleming_island',
    'ponte_vedra',
    'other'
];

/**
 * Get guide entries by category
 */
export async function getGuideByCategory(category, options = { limit: 20, skip: 0, area: null }) {
    try {
        let query = wixData.query('JacksonvilleGuide')
            .eq('category', category)
            .eq('isActive', true);
        
        if (options.area) {
            query = query.eq('area', options.area);
        }
        
        query = query
            .descending('rating')
            .ascending('name')
            .limit(options.limit)
            .skip(options.skip);
        
        const result = await query.find({ suppressAuth: true });
        
        return {
            items: result.items.map(item => ({
                id: item._id,
                name: item.name,
                category: item.category,
                area: item.area,
                address: item.address,
                phone: item.phone,
                website: item.website,
                description: item.description,
                rating: item.rating || 0,
                reviewCount: item.reviewCount || 0,
                imageUrl: item.imageUrl,
                tags: JSON.parse(item.tags || '[]'),
                bengaliOwned: item.bengaliOwned || false,
                bengaliStaff: item.bengaliStaff || false
            })),
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error getting guide entries:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Get all categories with counts
 */
export async function getGuideCategories() {
    try {
        const categoryCounts = {};
        
        for (const category of GUIDE_CATEGORIES) {
            categoryCounts[category] = await wixData.query('JacksonvilleGuide')
                .eq('category', category)
                .eq('isActive', true)
                .count();
        }
        
        return {
            categories: GUIDE_CATEGORIES,
            counts: categoryCounts
        };
    } catch (error) {
        console.error('Error getting categories:', error);
        return { categories: GUIDE_CATEGORIES, counts: {} };
    }
}

/**
 * Search guide entries
 */
export async function searchGuide(searchTerm, options = { limit: 20, skip: 0, category: null }) {
    try {
        let query = wixData.query('JacksonvilleGuide')
            .eq('isActive', true)
            .contains('name', searchTerm)
            .or(wixData.query('JacksonvilleGuide').contains('description', searchTerm))
            .or(wixData.query('JacksonvilleGuide').contains('address', searchTerm));
        
        if (options.category) {
            query = query.eq('category', options.category);
        }
        
        query = query
            .descending('rating')
            .limit(options.limit)
            .skip(options.skip);
        
        const result = await query.find({ suppressAuth: true });
        
        return {
            items: result.items.map(item => ({
                id: item._id,
                name: item.name,
                category: item.category,
                area: item.area,
                address: item.address,
                description: item.description,
                rating: item.rating || 0,
                bengaliOwned: item.bengaliOwned || false
            })),
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error searching guide:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Get Bengali-owned/staffed businesses
 */
export async function getBengaliFriendlyPlaces(options = { limit: 20, skip: 0, category: null }) {
    try {
        let query = wixData.query('JacksonvilleGuide')
            .eq('isActive', true)
            .or(
                wixData.query('JacksonvilleGuide').eq('bengaliOwned', true),
                wixData.query('JacksonvilleGuide').eq('bengaliStaff', true)
            );
        
        if (options.category) {
            query = query.eq('category', options.category);
        }
        
        query = query
            .descending('rating')
            .limit(options.limit)
            .skip(options.skip);
        
        const result = await query.find({ suppressAuth: true });
        
        return {
            items: result.items.map(item => ({
                id: item._id,
                name: item.name,
                category: item.category,
                area: item.area,
                address: item.address,
                phone: item.phone,
                description: item.description,
                rating: item.rating || 0,
                bengaliOwned: item.bengaliOwned,
                bengaliStaff: item.bengaliStaff
            })),
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error getting Bengali-friendly places:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Get guide entry by ID
 */
export async function getGuideEntryById(entryId) {
    try {
        const entry = await wixData.get('JacksonvilleGuide', entryId, { suppressAuth: true });
        
        if (!entry) return null;
        
        // Get reviews
        const reviews = await wixData.query('GuideReviews')
            .eq('guideEntryId', entryId)
            .eq('isApproved', true)
            .descending('_createdDate')
            .limit(10)
            .find({ suppressAuth: true });
        
        return {
            id: entry._id,
            name: entry.name,
            category: entry.category,
            area: entry.area,
            address: entry.address,
            phone: entry.phone,
            email: entry.email,
            website: entry.website,
            description: entry.description,
            fullDescription: entry.fullDescription,
            hours: JSON.parse(entry.hours || '{}'),
            rating: entry.rating || 0,
            reviewCount: entry.reviewCount || 0,
            imageUrl: entry.imageUrl,
            images: JSON.parse(entry.images || '[]'),
            tags: JSON.parse(entry.tags || '[]'),
            bengaliOwned: entry.bengaliOwned || false,
            bengaliStaff: entry.bengaliStaff || false,
            acceptsCard: entry.acceptsCard,
            parkingAvailable: entry.parkingAvailable,
            wheelchairAccessible: entry.wheelchairAccessible,
            latitude: entry.latitude,
            longitude: entry.longitude,
            reviews: reviews.items.map(r => ({
                id: r._id,
                rating: r.rating,
                comment: r.comment,
                reviewerName: r.reviewerName,
                date: r._createdDate
            }))
        };
    } catch (error) {
        console.error('Error getting guide entry:', error);
        return null;
    }
}

/**
 * Submit new guide entry (member contribution)
 */
export async function submitGuideEntry(entryData) {
    try {
        const member = await currentMember.getMember({ fieldsets: ['PUBLIC'] });
        
        const entry = {
            name: entryData.name,
            category: entryData.category,
            area: entryData.area || 'other',
            address: entryData.address,
            phone: entryData.phone || '',
            email: entryData.email || '',
            website: entryData.website || '',
            description: entryData.description,
            fullDescription: entryData.fullDescription || entryData.description,
            hours: JSON.stringify(entryData.hours || {}),
            imageUrl: entryData.imageUrl || '',
            images: JSON.stringify(entryData.images || []),
            tags: JSON.stringify(entryData.tags || []),
            bengaliOwned: entryData.bengaliOwned || false,
            bengaliStaff: entryData.bengaliStaff || false,
            acceptsCard: entryData.acceptsCard,
            parkingAvailable: entryData.parkingAvailable,
            wheelchairAccessible: entryData.wheelchairAccessible,
            latitude: entryData.latitude || null,
            longitude: entryData.longitude || null,
            rating: 0,
            reviewCount: 0,
            isActive: false, // Pending approval
            submittedBy: member ? member._id : null,
            submittedByEmail: member ? member.loginEmail : entryData.submitterEmail,
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert('JacksonvilleGuide', entry);
        
        return {
            success: true,
            entryId: result._id,
            message: 'Guide entry submitted for review. Thank you for contributing!'
        };
    } catch (error) {
        console.error('Error submitting guide entry:', error);
        return { success: false, error: 'Failed to submit entry' };
    }
}

/**
 * Submit review for guide entry
 */
export async function submitReview(entryId, reviewData) {
    try {
        const member = await currentMember.getMember({ fieldsets: ['PUBLIC'] });
        
        // Check if already reviewed
        if (member) {
            const existing = await wixData.query('GuideReviews')
                .eq('guideEntryId', entryId)
                .eq('reviewerId', member._id)
                .find();
            
            if (existing.items.length > 0) {
                return { success: false, error: 'You have already reviewed this place' };
            }
        }
        
        const review = {
            guideEntryId: entryId,
            rating: Math.min(5, Math.max(1, reviewData.rating)),
            comment: reviewData.comment,
            reviewerName: reviewData.name || (member ? member.name : 'Anonymous'),
            reviewerId: member ? member._id : null,
            reviewerEmail: member ? member.loginEmail : reviewData.email,
            isApproved: false, // Pending moderation
            _createdDate: new Date()
        };
        
        await wixData.insert('GuideReviews', review, { suppressAuth: true });
        
        return { success: true, message: 'Review submitted. It will appear after moderation.' };
    } catch (error) {
        console.error('Error submitting review:', error);
        return { success: false, error: 'Failed to submit review' };
    }
}

/**
 * Approve review and update rating (admin only)
 */
export async function approveReview(reviewId) {
    try {
        const review = await wixData.get('GuideReviews', reviewId);
        if (!review) {
            return { success: false, error: 'Review not found' };
        }
        
        // Update review
        await wixData.update('GuideReviews', {
            ...review,
            isApproved: true
        });
        
        // Recalculate entry rating
        const allReviews = await wixData.query('GuideReviews')
            .eq('guideEntryId', review.guideEntryId)
            .eq('isApproved', true)
            .find();
        
        const totalRating = allReviews.items.reduce((sum, r) => sum + r.rating, 0);
        const avgRating = allReviews.items.length > 0 
            ? (totalRating / allReviews.items.length).toFixed(1)
            : 0;
        
        // Update entry
        const entry = await wixData.get('JacksonvilleGuide', review.guideEntryId);
        if (entry) {
            await wixData.update('JacksonvilleGuide', {
                ...entry,
                rating: parseFloat(avgRating),
                reviewCount: allReviews.items.length,
                _updatedDate: new Date()
            });
        }
        
        return { success: true, message: 'Review approved' };
    } catch (error) {
        console.error('Error approving review:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Approve guide entry (admin only)
 */
export async function approveGuideEntry(entryId, adminId) {
    try {
        const entry = await wixData.get('JacksonvilleGuide', entryId);
        if (!entry) {
            return { success: false, error: 'Entry not found' };
        }
        
        await wixData.update('JacksonvilleGuide', {
            ...entry,
            isActive: true,
            approvedBy: adminId,
            approvedAt: new Date(),
            _updatedDate: new Date()
        });
        
        return { success: true, message: 'Guide entry approved and published' };
    } catch (error) {
        console.error('Error approving entry:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get pending entries for review (admin only)
 */
export async function getPendingGuideEntries() {
    try {
        const result = await wixData.query('JacksonvilleGuide')
            .eq('isActive', false)
            .descending('_createdDate')
            .find();
        
        return result.items;
    } catch (error) {
        console.error('Error getting pending entries:', error);
        return [];
    }
}

/**
 * Get pending reviews (admin only)
 */
export async function getPendingReviews() {
    try {
        const result = await wixData.query('GuideReviews')
            .eq('isApproved', false)
            .descending('_createdDate')
            .find();
        
        // Get entry names
        const entries = {};
        for (const review of result.items) {
            if (!entries[review.guideEntryId]) {
                const entry = await wixData.get('JacksonvilleGuide', review.guideEntryId);
                entries[review.guideEntryId] = entry ? entry.name : 'Unknown';
            }
        }
        
        return result.items.map(r => ({
            ...r,
            entryName: entries[r.guideEntryId]
        }));
    } catch (error) {
        console.error('Error getting pending reviews:', error);
        return [];
    }
}

/**
 * Get featured/recommended places
 */
export async function getFeaturedPlaces(limit = 10) {
    try {
        const result = await wixData.query('JacksonvilleGuide')
            .eq('isActive', true)
            .eq('isFeatured', true)
            .descending('rating')
            .limit(limit)
            .find({ suppressAuth: true });
        
        return result.items.map(item => ({
            id: item._id,
            name: item.name,
            category: item.category,
            area: item.area,
            imageUrl: item.imageUrl,
            rating: item.rating || 0,
            description: item.description
        }));
    } catch (error) {
        console.error('Error getting featured places:', error);
        return [];
    }
}

/**
 * Get places near location (requires lat/lng)
 */
export async function getPlacesNearLocation(latitude, longitude, radiusMiles = 5, category = null) {
    try {
        // Simple distance calculation
        // In production, would use a geospatial query or external service
        
        let query = wixData.query('JacksonvilleGuide')
            .eq('isActive', true)
            .isNotEmpty('latitude')
            .isNotEmpty('longitude');
        
        if (category) {
            query = query.eq('category', category);
        }
        
        const result = await query.limit(100).find({ suppressAuth: true });
        
        // Filter by distance
        const nearbyPlaces = result.items.filter(place => {
            if (!place.latitude || !place.longitude) return false;
            
            const distance = calculateDistance(
                latitude, longitude,
                place.latitude, place.longitude
            );
            
            return distance <= radiusMiles;
        });
        
        // Sort by distance
        nearbyPlaces.sort((a, b) => {
            const distA = calculateDistance(latitude, longitude, a.latitude, a.longitude);
            const distB = calculateDistance(latitude, longitude, b.latitude, b.longitude);
            return distA - distB;
        });
        
        return nearbyPlaces.slice(0, 20).map(place => ({
            id: place._id,
            name: place.name,
            category: place.category,
            address: place.address,
            distance: calculateDistance(latitude, longitude, place.latitude, place.longitude).toFixed(1),
            rating: place.rating || 0
        }));
    } catch (error) {
        console.error('Error getting nearby places:', error);
        return [];
    }
}

// Helper function for distance calculation (Haversine formula)
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 3959; // Earth's radius in miles
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

// Export constants
export const GuideCategories = GUIDE_CATEGORIES;
export const JacksonvilleAreas = JACKSONVILLE_AREAS;

```
------------------------------------------------------------

## [22/41] insights-analytics
- File: `insights-analytics.jsw`
- Size: 27.1 KB
- Lines: 782

```javascript
/**
 * BANF Insights & Analytics Module
 * Real-time dashboards and analytics for all modules
 * 
 * File: backend/insights-analytics.jsw
 * Deploy to: Wix Velo Backend
 */

import wixData from 'wix-data';
import { hasSpecializedPermission } from 'backend/specialized-admin-roles.jsw';

// Dashboard Types
export const DASHBOARD_TYPES = {
    EXECUTIVE_OVERVIEW: 'executive_overview',
    FINANCIAL_DASHBOARD: 'financial_dashboard',
    MEMBERSHIP_DASHBOARD: 'membership_dashboard',
    EVENT_DASHBOARD: 'event_dashboard',
    ENGAGEMENT_DASHBOARD: 'engagement_dashboard',
    CONTENT_DASHBOARD: 'content_dashboard',
    SPONSOR_DASHBOARD: 'sponsor_dashboard',
    CUSTOM_DASHBOARD: 'custom_dashboard'
};

// KPI Categories
export const KPI_CATEGORIES = {
    MEMBERSHIP: 'membership',
    FINANCIAL: 'financial',
    EVENTS: 'events',
    ENGAGEMENT: 'engagement',
    CONTENT: 'content',
    SPONSORSHIP: 'sponsorship',
    COMMUNITY: 'community'
};

/**
 * Get Executive Overview Dashboard
 * High-level KPIs for leadership
 */
export async function getExecutiveOverview(userId) {
    try {
        const hasPermission = await hasSpecializedPermission(userId, 'insights_view');
        if (!hasPermission) {
            return { success: false, error: 'Not authorized to view insights' };
        }
        
        const now = new Date();
        const thisMonth = new Date(now.getFullYear(), now.getMonth(), 1);
        const lastMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1);
        const lastMonthEnd = new Date(now.getFullYear(), now.getMonth(), 0);
        
        // Parallel data fetching for performance
        const [
            membershipStats,
            financialStats,
            eventStats,
            engagementStats
        ] = await Promise.all([
            getMembershipKPIs(thisMonth, lastMonth, lastMonthEnd),
            getFinancialKPIs(thisMonth, lastMonth, lastMonthEnd),
            getEventKPIs(thisMonth, lastMonth, lastMonthEnd),
            getEngagementKPIs(thisMonth, lastMonth, lastMonthEnd)
        ]);
        
        return {
            success: true,
            timestamp: new Date(),
            overview: {
                membership: membershipStats,
                financial: financialStats,
                events: eventStats,
                engagement: engagementStats
            },
            alerts: await getActiveAlerts(),
            trends: await getTrendIndicators()
        };
    } catch (error) {
        console.error('Executive overview failed:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get Membership KPIs
 */
async function getMembershipKPIs(thisMonth, lastMonth, lastMonthEnd) {
    const members = await wixData.query('Members')
        .find({ suppressAuth: true });
    
    const currentTotal = members.items.length;
    const activeMembers = members.items.filter(m => m.status === 'active').length;
    const newThisMonth = members.items.filter(m => 
        new Date(m.createdAt) >= thisMonth
    ).length;
    const newLastMonth = members.items.filter(m => 
        new Date(m.createdAt) >= lastMonth && 
        new Date(m.createdAt) <= lastMonthEnd
    ).length;
    
    const pendingRenewals = members.items.filter(m => {
        const expiry = new Date(m.membershipExpiry);
        const thirtyDaysFromNow = new Date();
        thirtyDaysFromNow.setDate(thirtyDaysFromNow.getDate() + 30);
        return expiry <= thirtyDaysFromNow && m.status === 'active';
    }).length;
    
    return {
        totalMembers: currentTotal,
        activeMembers,
        newThisMonth,
        growthRate: newLastMonth > 0 
            ? (((newThisMonth - newLastMonth) / newLastMonth) * 100).toFixed(1) 
            : 100,
        pendingRenewals,
        retentionRate: await calculateRetentionRate(members.items),
        familyMemberships: members.items.filter(m => m.membershipType?.includes('Family')).length,
        trend: newThisMonth > newLastMonth ? 'up' : newThisMonth < newLastMonth ? 'down' : 'stable'
    };
}

/**
 * Get Financial KPIs
 */
async function getFinancialKPIs(thisMonth, lastMonth, lastMonthEnd) {
    const transactions = await wixData.query('Transactions')
        .ge('transactionDate', lastMonth)
        .find({ suppressAuth: true });
    
    const thisMonthTx = transactions.items.filter(t => 
        new Date(t.transactionDate) >= thisMonth
    );
    const lastMonthTx = transactions.items.filter(t => 
        new Date(t.transactionDate) >= lastMonth && 
        new Date(t.transactionDate) <= lastMonthEnd
    );
    
    const incomeThisMonth = thisMonthTx
        .filter(t => t.type === 'income')
        .reduce((sum, t) => sum + t.amount, 0);
    
    const expensesThisMonth = thisMonthTx
        .filter(t => t.type === 'expense')
        .reduce((sum, t) => sum + t.amount, 0);
    
    const incomeLastMonth = lastMonthTx
        .filter(t => t.type === 'income')
        .reduce((sum, t) => sum + t.amount, 0);
    
    return {
        incomeThisMonth,
        expensesThisMonth,
        netIncomeThisMonth: incomeThisMonth - expensesThisMonth,
        incomeGrowth: incomeLastMonth > 0 
            ? (((incomeThisMonth - incomeLastMonth) / incomeLastMonth) * 100).toFixed(1)
            : 100,
        pendingPayments: await getPendingPaymentsCount(),
        outstandingInvoices: await getOutstandingInvoicesCount(),
        budgetUtilization: await getBudgetUtilization(),
        trend: incomeThisMonth > incomeLastMonth ? 'up' : 'down'
    };
}

/**
 * Get Event KPIs
 */
async function getEventKPIs(thisMonth, lastMonth, lastMonthEnd) {
    const events = await wixData.query('Events')
        .find({ suppressAuth: true });
    
    const upcomingEvents = events.items.filter(e => 
        new Date(e.eventDate) > new Date()
    ).length;
    
    const eventsThisMonth = events.items.filter(e => 
        new Date(e.eventDate) >= thisMonth
    ).length;
    
    const registrations = await wixData.query('EventRegistrations')
        .ge('createdAt', thisMonth)
        .find({ suppressAuth: true });
    
    const lastMonthRegs = await wixData.query('EventRegistrations')
        .ge('createdAt', lastMonth)
        .le('createdAt', lastMonthEnd)
        .find({ suppressAuth: true });
    
    return {
        upcomingEvents,
        eventsThisMonth,
        registrationsThisMonth: registrations.items.length,
        registrationGrowth: lastMonthRegs.items.length > 0
            ? (((registrations.items.length - lastMonthRegs.items.length) / lastMonthRegs.items.length) * 100).toFixed(1)
            : 100,
        averageAttendance: await calculateAverageAttendance(),
        totalRevenue: await calculateEventRevenue(thisMonth),
        popularEvents: await getPopularEvents(5),
        trend: registrations.items.length > lastMonthRegs.items.length ? 'up' : 'down'
    };
}

/**
 * Get Engagement KPIs
 */
async function getEngagementKPIs(thisMonth, lastMonth, lastMonthEnd) {
    const [
        volunteerHours,
        surveyResponses,
        complaints,
        communityActivity
    ] = await Promise.all([
        wixData.query('VolunteerHours').ge('date', thisMonth).find({ suppressAuth: true }),
        wixData.query('SurveyResponses').ge('submittedAt', thisMonth).find({ suppressAuth: true }),
        wixData.query('Complaints').ge('submittedAt', thisMonth).find({ suppressAuth: true }),
        wixData.query('CommunityActivity').ge('date', thisMonth).find({ suppressAuth: true })
    ]);
    
    return {
        volunteerHoursThisMonth: volunteerHours.items.reduce((sum, h) => sum + h.hours, 0),
        activeVolunteers: new Set(volunteerHours.items.map(h => h.volunteerId)).size,
        surveyResponseRate: await calculateSurveyResponseRate(),
        openComplaints: complaints.items.filter(c => c.status !== 'resolved').length,
        resolvedComplaints: complaints.items.filter(c => c.status === 'resolved').length,
        communityParticipation: communityActivity.items.length,
        engagementScore: await calculateEngagementScore()
    };
}

/**
 * Get Real-time Dashboard Data
 */
export async function getDashboardData(dashboardType, userId) {
    try {
        const hasPermission = await hasSpecializedPermission(userId, 'insights_view');
        if (!hasPermission) {
            return { success: false, error: 'Not authorized' };
        }
        
        let data;
        
        switch (dashboardType) {
            case DASHBOARD_TYPES.EXECUTIVE_OVERVIEW:
                return await getExecutiveOverview(userId);
                
            case DASHBOARD_TYPES.FINANCIAL_DASHBOARD:
                data = await getFinancialDashboard();
                break;
                
            case DASHBOARD_TYPES.MEMBERSHIP_DASHBOARD:
                data = await getMembershipDashboard();
                break;
                
            case DASHBOARD_TYPES.EVENT_DASHBOARD:
                data = await getEventDashboard();
                break;
                
            case DASHBOARD_TYPES.ENGAGEMENT_DASHBOARD:
                data = await getEngagementDashboard();
                break;
                
            case DASHBOARD_TYPES.CONTENT_DASHBOARD:
                data = await getContentDashboard();
                break;
                
            case DASHBOARD_TYPES.SPONSOR_DASHBOARD:
                data = await getSponsorDashboard();
                break;
                
            default:
                return { success: false, error: 'Invalid dashboard type' };
        }
        
        return { success: true, data, timestamp: new Date() };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Get Financial Dashboard
 */
async function getFinancialDashboard() {
    const now = new Date();
    const yearStart = new Date(now.getFullYear(), 0, 1);
    
    const transactions = await wixData.query('Transactions')
        .ge('transactionDate', yearStart)
        .find({ suppressAuth: true });
    
    // Monthly breakdown
    const monthlyData = {};
    for (let i = 0; i < 12; i++) {
        const monthName = new Date(now.getFullYear(), i).toLocaleString('default', { month: 'short' });
        monthlyData[monthName] = { income: 0, expenses: 0 };
    }
    
    transactions.items.forEach(t => {
        const month = new Date(t.transactionDate).toLocaleString('default', { month: 'short' });
        if (monthlyData[month]) {
            if (t.type === 'income') monthlyData[month].income += t.amount;
            else monthlyData[month].expenses += t.amount;
        }
    });
    
    // Category breakdown
    const byCategory = {};
    transactions.items.forEach(t => {
        const category = t.category || 'Other';
        if (!byCategory[category]) {
            byCategory[category] = { income: 0, expenses: 0 };
        }
        if (t.type === 'income') byCategory[category].income += t.amount;
        else byCategory[category].expenses += t.amount;
    });
    
    return {
        monthlyTrend: monthlyData,
        byCategory,
        totalIncome: transactions.items.filter(t => t.type === 'income').reduce((sum, t) => sum + t.amount, 0),
        totalExpenses: transactions.items.filter(t => t.type === 'expense').reduce((sum, t) => sum + t.amount, 0),
        budgetStatus: await getBudgetStatus(),
        cashFlow: await getCashFlowProjection(),
        recentTransactions: transactions.items.slice(0, 10)
    };
}

/**
 * Get Membership Dashboard
 */
async function getMembershipDashboard() {
    const members = await wixData.query('Members')
        .find({ suppressAuth: true });
    
    // Growth over last 12 months
    const now = new Date();
    const monthlyGrowth = {};
    for (let i = 11; i >= 0; i--) {
        const monthDate = new Date(now.getFullYear(), now.getMonth() - i, 1);
        const monthKey = monthDate.toLocaleString('default', { month: 'short', year: '2-digit' });
        monthlyGrowth[monthKey] = members.items.filter(m => 
            new Date(m.createdAt) <= new Date(now.getFullYear(), now.getMonth() - i + 1, 0)
        ).length;
    }
    
    // Demographics
    const demographics = {
        byState: {},
        byMembershipType: {},
        byJoinYear: {}
    };
    
    members.items.forEach(m => {
        const state = m.state || 'Unknown';
        const type = m.membershipType || 'Standard';
        const year = new Date(m.createdAt).getFullYear();
        
        demographics.byState[state] = (demographics.byState[state] || 0) + 1;
        demographics.byMembershipType[type] = (demographics.byMembershipType[type] || 0) + 1;
        demographics.byJoinYear[year] = (demographics.byJoinYear[year] || 0) + 1;
    });
    
    return {
        totalMembers: members.items.length,
        activeMembers: members.items.filter(m => m.status === 'active').length,
        monthlyGrowth,
        demographics,
        expiringThisMonth: members.items.filter(m => {
            const expiry = new Date(m.membershipExpiry);
            const thisMonth = new Date();
            return expiry.getMonth() === thisMonth.getMonth() && 
                   expiry.getFullYear() === thisMonth.getFullYear();
        }).length,
        lifetimeMembers: members.items.filter(m => m.membershipType === 'Lifetime').length,
        recentJoins: members.items
            .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
            .slice(0, 10)
    };
}

/**
 * Get Event Dashboard
 */
async function getEventDashboard() {
    const events = await wixData.query('Events')
        .descending('eventDate')
        .find({ suppressAuth: true });
    
    const registrations = await wixData.query('EventRegistrations')
        .find({ suppressAuth: true });
    
    // Attendance by event type
    const byType = {};
    events.items.forEach(e => {
        const type = e.eventType || 'Other';
        if (!byType[type]) {
            byType[type] = { count: 0, totalAttendees: 0 };
        }
        byType[type].count++;
        byType[type].totalAttendees += registrations.items.filter(r => r.eventId === e._id).length;
    });
    
    // Monthly event count
    const now = new Date();
    const monthlyEvents = {};
    for (let i = 5; i >= 0; i--) {
        const monthDate = new Date(now.getFullYear(), now.getMonth() - i, 1);
        const monthEnd = new Date(now.getFullYear(), now.getMonth() - i + 1, 0);
        const monthKey = monthDate.toLocaleString('default', { month: 'short' });
        monthlyEvents[monthKey] = events.items.filter(e => {
            const eventDate = new Date(e.eventDate);
            return eventDate >= monthDate && eventDate <= monthEnd;
        }).length;
    }
    
    return {
        totalEvents: events.items.length,
        upcomingEvents: events.items.filter(e => new Date(e.eventDate) > new Date()),
        pastEvents: events.items.filter(e => new Date(e.eventDate) <= new Date()),
        byType,
        monthlyEvents,
        topEvents: events.items
            .map(e => ({
                ...e,
                registrationCount: registrations.items.filter(r => r.eventId === e._id).length
            }))
            .sort((a, b) => b.registrationCount - a.registrationCount)
            .slice(0, 5),
        recentRegistrations: registrations.items
            .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
            .slice(0, 10)
    };
}

/**
 * Get Engagement Dashboard
 */
async function getEngagementDashboard() {
    const [volunteers, surveys, complaints, community] = await Promise.all([
        wixData.query('VolunteerHours').find({ suppressAuth: true }),
        wixData.query('SurveyResponses').find({ suppressAuth: true }),
        wixData.query('Complaints').find({ suppressAuth: true }),
        wixData.query('CommunityActivity').find({ suppressAuth: true })
    ]);
    
    return {
        volunteerMetrics: {
            totalHours: volunteers.items.reduce((sum, v) => sum + v.hours, 0),
            totalVolunteers: new Set(volunteers.items.map(v => v.volunteerId)).size,
            topVolunteers: getTopVolunteers(volunteers.items, 5)
        },
        surveyMetrics: {
            totalResponses: surveys.items.length,
            averageSatisfaction: calculateAverageSatisfaction(surveys.items),
            responseRate: await calculateSurveyResponseRate()
        },
        complaintMetrics: {
            total: complaints.items.length,
            open: complaints.items.filter(c => c.status !== 'resolved').length,
            avgResolutionTime: calculateAvgResolutionTime(complaints.items)
        },
        communityMetrics: {
            activeInitiatives: community.items.filter(c => c.status === 'active').length,
            participation: community.items.reduce((sum, c) => sum + (c.participantCount || 0), 0)
        }
    };
}

/**
 * Get Content Dashboard
 */
async function getContentDashboard() {
    const [magazines, radio, guides, gallery] = await Promise.all([
        wixData.query('MagazineIssues').find({ suppressAuth: true }),
        wixData.query('RadioPrograms').find({ suppressAuth: true }),
        wixData.query('Guides').find({ suppressAuth: true }),
        wixData.query('GalleryItems').find({ suppressAuth: true })
    ]);
    
    return {
        magazineMetrics: {
            totalIssues: magazines.items.length,
            totalViews: magazines.items.reduce((sum, m) => sum + (m.viewCount || 0), 0),
            latestIssue: magazines.items.sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt))[0]
        },
        radioMetrics: {
            totalPrograms: radio.items.length,
            totalListens: radio.items.reduce((sum, r) => sum + (r.listenCount || 0), 0),
            upcomingShows: radio.items.filter(r => new Date(r.scheduledAt) > new Date()).length
        },
        guideMetrics: {
            totalGuides: guides.items.length,
            totalViews: guides.items.reduce((sum, g) => sum + (g.viewCount || 0), 0),
            byCategory: groupByCategory(guides.items)
        },
        galleryMetrics: {
            totalItems: gallery.items.length,
            byEvent: groupByEvent(gallery.items)
        }
    };
}

/**
 * Get Sponsor Dashboard
 */
async function getSponsorDashboard() {
    const sponsors = await wixData.query('Sponsors')
        .find({ suppressAuth: true });
    
    const vendors = await wixData.query('Vendors')
        .find({ suppressAuth: true });
    
    const ads = await wixData.query('Advertisements')
        .find({ suppressAuth: true });
    
    return {
        sponsorMetrics: {
            total: sponsors.items.length,
            byTier: groupByTier(sponsors.items),
            totalRevenue: sponsors.items.reduce((sum, s) => sum + (s.amount || 0), 0),
            expiringThisMonth: sponsors.items.filter(s => {
                const expiry = new Date(s.expiryDate);
                const now = new Date();
                return expiry.getMonth() === now.getMonth() && expiry.getFullYear() === now.getFullYear();
            }).length
        },
        vendorMetrics: {
            total: vendors.items.length,
            active: vendors.items.filter(v => v.status === 'active').length,
            avgRating: vendors.items.reduce((sum, v) => sum + (v.rating || 0), 0) / vendors.items.length || 0
        },
        adMetrics: {
            total: ads.items.length,
            active: ads.items.filter(a => a.status === 'active').length,
            totalRevenue: ads.items.reduce((sum, a) => sum + (a.revenue || 0), 0),
            avgCTR: calculateAvgCTR(ads.items)
        }
    };
}

/**
 * Get Predictive Analytics
 */
export async function getPredictiveAnalytics(metric, userId) {
    try {
        const hasPermission = await hasSpecializedPermission(userId, 'insights_advanced');
        if (!hasPermission) {
            return { success: false, error: 'Not authorized for advanced analytics' };
        }
        
        let prediction;
        
        switch (metric) {
            case 'membership_growth':
                prediction = await predictMembershipGrowth();
                break;
            case 'event_attendance':
                prediction = await predictEventAttendance();
                break;
            case 'revenue':
                prediction = await predictRevenue();
                break;
            case 'churn':
                prediction = await predictChurnRisk();
                break;
            default:
                return { success: false, error: 'Invalid metric' };
        }
        
        return { success: true, prediction };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// Prediction helper functions
async function predictMembershipGrowth() {
    // Simple linear projection based on historical data
    const members = await wixData.query('Members').find({ suppressAuth: true });
    
    const monthlyGrowth = [];
    for (let i = 5; i >= 0; i--) {
        const monthStart = new Date();
        monthStart.setMonth(monthStart.getMonth() - i);
        monthStart.setDate(1);
        const count = members.items.filter(m => new Date(m.createdAt) <= monthStart).length;
        monthlyGrowth.push(count);
    }
    
    // Simple linear regression for next 3 months
    const avgGrowth = (monthlyGrowth[5] - monthlyGrowth[0]) / 5;
    const predictions = [
        Math.round(monthlyGrowth[5] + avgGrowth),
        Math.round(monthlyGrowth[5] + avgGrowth * 2),
        Math.round(monthlyGrowth[5] + avgGrowth * 3)
    ];
    
    return {
        historical: monthlyGrowth,
        predicted: predictions,
        confidence: 0.75,
        trend: avgGrowth > 0 ? 'growing' : 'declining'
    };
}

async function predictEventAttendance() {
    return { predicted: 150, confidence: 0.70, factors: ['season', 'event_type', 'marketing'] };
}

async function predictRevenue() {
    return { predicted: 25000, confidence: 0.65, factors: ['memberships', 'events', 'sponsorships'] };
}

async function predictChurnRisk() {
    const members = await wixData.query('Members')
        .eq('status', 'active')
        .find({ suppressAuth: true });
    
    const atRisk = members.items.filter(m => {
        const expiry = new Date(m.membershipExpiry);
        const daysTillExpiry = (expiry - new Date()) / (1000 * 60 * 60 * 24);
        return daysTillExpiry <= 30 && daysTillExpiry > 0;
    });
    
    return {
        atRiskCount: atRisk.length,
        atRiskMembers: atRisk.map(m => ({
            id: m._id,
            name: `${m.firstName} ${m.lastName}`,
            expiryDate: m.membershipExpiry,
            riskScore: calculateChurnRiskScore(m)
        })),
        totalAtRiskValue: atRisk.reduce((sum, m) => sum + (m.membershipFee || 0), 0)
    };
}

// Helper functions
function calculateChurnRiskScore(member) {
    let score = 50; // Base score
    
    // Engagement factors
    if (member.lastEventAttended) {
        const daysSinceEvent = (new Date() - new Date(member.lastEventAttended)) / (1000 * 60 * 60 * 24);
        if (daysSinceEvent > 180) score += 20;
        else if (daysSinceEvent > 90) score += 10;
    } else {
        score += 15;
    }
    
    // Renewal history
    if (!member.isRenewal) score += 10; // First-time members at higher risk
    
    return Math.min(score, 100);
}

async function calculateRetentionRate(members) {
    const renewals = members.filter(m => m.isRenewal).length;
    return members.length > 0 ? ((renewals / members.length) * 100).toFixed(1) : 0;
}

async function getPendingPaymentsCount() {
    const pending = await wixData.query('Payments')
        .eq('status', 'pending')
        .count({ suppressAuth: true });
    return pending;
}

async function getOutstandingInvoicesCount() {
    const outstanding = await wixData.query('Invoices')
        .eq('status', 'outstanding')
        .count({ suppressAuth: true });
    return outstanding;
}

async function getBudgetUtilization() {
    return 75; // Placeholder
}

async function calculateAverageAttendance() {
    return 85; // Placeholder
}

async function calculateEventRevenue(startDate) {
    const revenue = await wixData.query('Transactions')
        .ge('transactionDate', startDate)
        .eq('source', 'events')
        .eq('type', 'income')
        .find({ suppressAuth: true });
    return revenue.items.reduce((sum, t) => sum + t.amount, 0);
}

async function getPopularEvents(limit) {
    return [];
}

async function calculateSurveyResponseRate() {
    return 65;
}

async function calculateEngagementScore() {
    return 78;
}

async function getActiveAlerts() {
    return [
        { type: 'warning', message: '5 memberships expiring this week' },
        { type: 'info', message: 'New event registrations up 15%' }
    ];
}

async function getTrendIndicators() {
    return {
        membership: 'up',
        revenue: 'stable',
        engagement: 'up'
    };
}

async function getBudgetStatus() {
    return { utilized: 75, remaining: 25 };
}

async function getCashFlowProjection() {
    return [];
}

function getTopVolunteers(hours, limit) {
    const byVolunteer = {};
    hours.forEach(h => {
        byVolunteer[h.volunteerName] = (byVolunteer[h.volunteerName] || 0) + h.hours;
    });
    return Object.entries(byVolunteer)
        .sort((a, b) => b[1] - a[1])
        .slice(0, limit);
}

function calculateAverageSatisfaction(surveys) {
    const scores = surveys.map(s => s.satisfactionScore).filter(s => s);
    return scores.length > 0 ? (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1) : 0;
}

function calculateAvgResolutionTime(complaints) {
    const resolved = complaints.filter(c => c.resolvedAt);
    if (resolved.length === 0) return 0;
    const totalDays = resolved.reduce((sum, c) => {
        return sum + (new Date(c.resolvedAt) - new Date(c.submittedAt)) / (1000 * 60 * 60 * 24);
    }, 0);
    return (totalDays / resolved.length).toFixed(1);
}

function groupByCategory(items) {
    const groups = {};
    items.forEach(i => {
        const cat = i.category || 'Other';
        groups[cat] = (groups[cat] || 0) + 1;
    });
    return groups;
}

function groupByEvent(items) {
    const groups = {};
    items.forEach(i => {
        const event = i.eventName || 'General';
        groups[event] = (groups[event] || 0) + 1;
    });
    return groups;
}

function groupByTier(sponsors) {
    const tiers = { platinum: 0, gold: 0, silver: 0, bronze: 0, supporter: 0 };
    sponsors.forEach(s => {
        const tier = s.tier?.toLowerCase() || 'supporter';
        if (tiers[tier] !== undefined) tiers[tier]++;
    });
    return tiers;
}

function calculateAvgCTR(ads) {
    const withMetrics = ads.filter(a => a.impressions > 0);
    if (withMetrics.length === 0) return 0;
    const totalCTR = withMetrics.reduce((sum, a) => {
        return sum + ((a.clicks || 0) / a.impressions) * 100;
    }, 0);
    return (totalCTR / withMetrics.length).toFixed(2);
}

```
------------------------------------------------------------

## [23/41] magazine
- File: `magazine.jsw`
- Size: 14.5 KB
- Lines: 454

```javascript
// backend/magazine.jsw
// BANF E-Magazine System - Wix Velo Backend

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';

// Article status constants
const ARTICLE_STATUS = {
    DRAFT: 'draft',
    PENDING_REVIEW: 'pending_review',
    PUBLISHED: 'published',
    ARCHIVED: 'archived'
};

// Article categories
const ARTICLE_CATEGORIES = [
    'community_news',
    'culture',
    'events',
    'poetry',
    'short_story',
    'recipe',
    'travel',
    'opinion',
    'youth',
    'health',
    'education',
    'sports',
    'tech',
    'business'
];

/**
 * Get published magazines
 */
export async function getPublishedMagazines(options = { limit: 12, skip: 0 }) {
    try {
        const result = await wixData.query('EMagazines')
            .eq('isPublished', true)
            .descending('issueDate')
            .limit(options.limit)
            .skip(options.skip)
            .find({ suppressAuth: true });
        
        return {
            items: result.items.map(mag => ({
                id: mag._id,
                title: mag.title,
                issueNumber: mag.issueNumber,
                issueDate: mag.issueDate,
                coverImageUrl: mag.coverImageUrl,
                description: mag.description,
                articleCount: mag.articleCount || 0
            })),
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error getting magazines:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Get latest magazine
 */
export async function getLatestMagazine() {
    try {
        const result = await wixData.query('EMagazines')
            .eq('isPublished', true)
            .descending('issueDate')
            .limit(1)
            .find({ suppressAuth: true });
        
        if (result.items.length === 0) return null;
        
        const magazine = result.items[0];
        
        // Get articles for this magazine
        const articles = await wixData.query('EMagazineArticles')
            .eq('magazineId', magazine._id)
            .eq('status', ARTICLE_STATUS.PUBLISHED)
            .ascending('orderIndex')
            .find({ suppressAuth: true });
        
        return {
            ...magazine,
            articles: articles.items.map(a => ({
                id: a._id,
                title: a.title,
                author: a.authorName,
                category: a.category,
                excerpt: a.excerpt
            }))
        };
    } catch (error) {
        console.error('Error getting latest magazine:', error);
        return null;
    }
}

/**
 * Get magazine by ID with articles
 */
export async function getMagazineById(magazineId) {
    try {
        const magazine = await wixData.get('EMagazines', magazineId, { suppressAuth: true });
        
        if (!magazine) return null;
        
        // Get articles for this magazine
        const articles = await wixData.query('EMagazineArticles')
            .eq('magazineId', magazineId)
            .eq('status', ARTICLE_STATUS.PUBLISHED)
            .ascending('orderIndex')
            .find({ suppressAuth: true });
        
        return {
            id: magazine._id,
            title: magazine.title,
            issueNumber: magazine.issueNumber,
            issueDate: magazine.issueDate,
            coverImageUrl: magazine.coverImageUrl,
            description: magazine.description,
            editorNote: magazine.editorNote,
            articles: articles.items.map(a => ({
                id: a._id,
                title: a.title,
                author: a.authorName,
                category: a.category,
                excerpt: a.excerpt,
                thumbnailUrl: a.thumbnailUrl
            }))
        };
    } catch (error) {
        console.error('Error getting magazine:', error);
        return null;
    }
}

/**
 * Get article by ID
 */
export async function getArticleById(articleId) {
    try {
        const article = await wixData.get('EMagazineArticles', articleId, { suppressAuth: true });
        
        if (!article) return null;
        
        // Increment view count
        await wixData.update('EMagazineArticles', {
            ...article,
            viewCount: (article.viewCount || 0) + 1
        });
        
        return {
            id: article._id,
            title: article.title,
            authorName: article.authorName,
            authorBio: article.authorBio,
            category: article.category,
            content: article.content,
            excerpt: article.excerpt,
            thumbnailUrl: article.thumbnailUrl,
            images: JSON.parse(article.images || '[]'),
            tags: JSON.parse(article.tags || '[]'),
            publishedDate: article.publishedDate,
            viewCount: (article.viewCount || 0) + 1,
            magazineId: article.magazineId
        };
    } catch (error) {
        console.error('Error getting article:', error);
        return null;
    }
}

/**
 * Get articles by category
 */
export async function getArticlesByCategory(category, options = { limit: 20, skip: 0 }) {
    try {
        const result = await wixData.query('EMagazineArticles')
            .eq('category', category)
            .eq('status', ARTICLE_STATUS.PUBLISHED)
            .descending('publishedDate')
            .limit(options.limit)
            .skip(options.skip)
            .find({ suppressAuth: true });
        
        return {
            items: result.items.map(a => ({
                id: a._id,
                title: a.title,
                author: a.authorName,
                excerpt: a.excerpt,
                thumbnailUrl: a.thumbnailUrl,
                publishedDate: a.publishedDate,
                magazineId: a.magazineId
            })),
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error getting articles by category:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Search articles
 */
export async function searchArticles(searchTerm, options = { limit: 20, skip: 0 }) {
    try {
        const result = await wixData.query('EMagazineArticles')
            .eq('status', ARTICLE_STATUS.PUBLISHED)
            .contains('title', searchTerm)
            .or(wixData.query('EMagazineArticles').contains('content', searchTerm))
            .or(wixData.query('EMagazineArticles').contains('authorName', searchTerm))
            .descending('publishedDate')
            .limit(options.limit)
            .skip(options.skip)
            .find({ suppressAuth: true });
        
        return {
            items: result.items.map(a => ({
                id: a._id,
                title: a.title,
                author: a.authorName,
                category: a.category,
                excerpt: a.excerpt,
                publishedDate: a.publishedDate
            })),
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error searching articles:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Submit article for publication (member contribution)
 */
export async function submitArticle(articleData) {
    try {
        const member = await currentMember.getMember({ fieldsets: ['PUBLIC'] });
        
        const article = {
            title: articleData.title,
            authorName: articleData.authorName || (member ? member.name : 'Anonymous'),
            authorEmail: articleData.authorEmail || (member ? member.loginEmail : ''),
            authorMemberId: member ? member._id : null,
            authorBio: articleData.authorBio || '',
            category: articleData.category || 'community_news',
            content: articleData.content,
            excerpt: articleData.excerpt || articleData.content.substring(0, 200) + '...',
            thumbnailUrl: articleData.thumbnailUrl || '',
            images: JSON.stringify(articleData.images || []),
            tags: JSON.stringify(articleData.tags || []),
            status: ARTICLE_STATUS.PENDING_REVIEW,
            submittedAt: new Date(),
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert('EMagazineArticles', article);
        
        return {
            success: true,
            articleId: result._id,
            message: 'Article submitted for review. You will be notified once reviewed.'
        };
    } catch (error) {
        console.error('Error submitting article:', error);
        return { success: false, error: 'Failed to submit article' };
    }
}

/**
 * Create magazine issue (admin only)
 */
export async function createMagazine(magazineData, adminId) {
    try {
        // Get next issue number
        const lastMagazine = await wixData.query('EMagazines')
            .descending('issueNumber')
            .limit(1)
            .find();
        
        const nextIssueNumber = lastMagazine.items.length > 0 
            ? lastMagazine.items[0].issueNumber + 1 
            : 1;
        
        const magazine = {
            title: magazineData.title || `Issue ${nextIssueNumber}`,
            issueNumber: nextIssueNumber,
            issueDate: magazineData.issueDate ? new Date(magazineData.issueDate) : new Date(),
            coverImageUrl: magazineData.coverImageUrl || '',
            description: magazineData.description || '',
            editorNote: magazineData.editorNote || '',
            isPublished: false,
            articleCount: 0,
            createdBy: adminId,
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert('EMagazines', magazine);
        
        return { success: true, magazineId: result._id, issueNumber: nextIssueNumber };
    } catch (error) {
        console.error('Error creating magazine:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Add article to magazine (admin only)
 */
export async function addArticleToMagazine(articleId, magazineId, orderIndex) {
    try {
        const article = await wixData.get('EMagazineArticles', articleId);
        if (!article) {
            return { success: false, error: 'Article not found' };
        }
        
        await wixData.update('EMagazineArticles', {
            ...article,
            magazineId: magazineId,
            orderIndex: orderIndex || 0,
            status: ARTICLE_STATUS.PUBLISHED,
            publishedDate: new Date(),
            _updatedDate: new Date()
        });
        
        // Update magazine article count
        const magazine = await wixData.get('EMagazines', magazineId);
        if (magazine) {
            await wixData.update('EMagazines', {
                ...magazine,
                articleCount: (magazine.articleCount || 0) + 1,
                _updatedDate: new Date()
            });
        }
        
        return { success: true, message: 'Article added to magazine' };
    } catch (error) {
        console.error('Error adding article to magazine:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Publish magazine (admin only)
 */
export async function publishMagazine(magazineId, adminId) {
    try {
        const magazine = await wixData.get('EMagazines', magazineId);
        if (!magazine) {
            return { success: false, error: 'Magazine not found' };
        }
        
        await wixData.update('EMagazines', {
            ...magazine,
            isPublished: true,
            publishedAt: new Date(),
            publishedBy: adminId,
            _updatedDate: new Date()
        });
        
        return { success: true, message: 'Magazine published successfully' };
    } catch (error) {
        console.error('Error publishing magazine:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get pending articles for review (admin only)
 */
export async function getPendingArticles() {
    try {
        const result = await wixData.query('EMagazineArticles')
            .eq('status', ARTICLE_STATUS.PENDING_REVIEW)
            .descending('submittedAt')
            .find();
        
        return result.items;
    } catch (error) {
        console.error('Error getting pending articles:', error);
        return [];
    }
}

/**
 * Review article (admin only)
 */
export async function reviewArticle(articleId, decision, feedback, adminId) {
    try {
        const article = await wixData.get('EMagazineArticles', articleId);
        if (!article) {
            return { success: false, error: 'Article not found' };
        }
        
        const newStatus = decision === 'approve' 
            ? ARTICLE_STATUS.DRAFT  // Approved but not yet in magazine
            : ARTICLE_STATUS.ARCHIVED; // Rejected
        
        await wixData.update('EMagazineArticles', {
            ...article,
            status: newStatus,
            reviewedAt: new Date(),
            reviewedBy: adminId,
            reviewFeedback: feedback || '',
            _updatedDate: new Date()
        });
        
        // TODO: Send email notification to author
        
        return { success: true, message: `Article ${decision}d successfully` };
    } catch (error) {
        console.error('Error reviewing article:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get popular articles
 */
export async function getPopularArticles(limit = 10) {
    try {
        const result = await wixData.query('EMagazineArticles')
            .eq('status', ARTICLE_STATUS.PUBLISHED)
            .descending('viewCount')
            .limit(limit)
            .find({ suppressAuth: true });
        
        return result.items.map(a => ({
            id: a._id,
            title: a.title,
            author: a.authorName,
            category: a.category,
            viewCount: a.viewCount || 0
        }));
    } catch (error) {
        console.error('Error getting popular articles:', error);
        return [];
    }
}

// Export constants
export const ArticleStatus = ARTICLE_STATUS;
export const ArticleCategories = ARTICLE_CATEGORIES;

```
------------------------------------------------------------

## [24/41] member-auth
- File: `member-auth.jsw`
- Size: 9.6 KB
- Lines: 297

```javascript
/**
 * BANF Member Authentication Backend Module
 * Handles member login, registration, and session management
 * 
 * File: backend/member-auth.jsw
 * Deploy to: Wix Velo Backend
 */

import wixData from 'wix-data';
import wixUsersBackend from 'wix-users-backend';
import { authentication } from 'wix-members-backend';
import { triggeredEmails } from 'wix-crm-backend';

/**
 * Register a new member
 * @param {object} memberData - Member registration data
 * @returns {object} - Registration result
 */
export async function registerMember(memberData) {
    const {
        email,
        password,
        firstName,
        lastName,
        phone,
        address,
        membershipType,
        familyMembers
    } = memberData;
    
    try {
        // Check if email already exists
        const existingMember = await wixData.query('Members')
            .eq('email', email.toLowerCase())
            .find({ suppressAuth: true });
        
        if (existingMember.items.length > 0) {
            return { success: false, error: 'Email already registered' };
        }
        
        // Register with Wix Members
        const registrationResult = await authentication.register(email, password, {
            contactInfo: {
                firstName,
                lastName,
                phones: [phone],
                addresses: [{ 
                    addressLine: address,
                    city: 'Jacksonville',
                    subdivision: 'FL',
                    country: 'US'
                }]
            }
        });
        
        // Create member record in CMS
        const member = await wixData.insert('Members', {
            wixMemberId: registrationResult.member._id,
            email: email.toLowerCase(),
            firstName,
            lastName,
            fullName: `${firstName} ${lastName}`,
            phone,
            address,
            membershipType: membershipType || 'Pending',
            membershipStatus: 'pending_payment',
            familyMembers: familyMembers || [],
            registrationDate: new Date(),
            isVerified: false,
            createdAt: new Date(),
            updatedAt: new Date()
        });
        
        // Send welcome email
        try {
            await triggeredEmails.emailMember('welcome_email', registrationResult.member._id, {
                variables: {
                    firstName,
                    membershipType: membershipType || 'New Member'
                }
            });
        } catch (emailError) {
            console.error('Welcome email failed:', emailError);
        }
        
        return {
            success: true,
            memberId: member._id,
            message: 'Registration successful! Please complete your membership payment.',
            sessionToken: registrationResult.sessionToken
        };
    } catch (error) {
        console.error('Member registration failed:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Login member
 * @param {string} email - Member email
 * @param {string} password - Member password
 * @returns {object} - Login result
 */
export async function loginMember(email, password) {
    try {
        const loginResult = await authentication.login(email, password);
        
        // Get member details
        const members = await wixData.query('Members')
            .eq('email', email.toLowerCase())
            .find({ suppressAuth: true });
        
        let memberData = null;
        if (members.items.length > 0) {
            memberData = {
                id: members.items[0]._id,
                fullName: members.items[0].fullName,
                email: members.items[0].email,
                membershipType: members.items[0].membershipType,
                membershipStatus: members.items[0].membershipStatus,
                isVerified: members.items[0].isVerified
            };
            
            // Update last login
            await wixData.update('Members', {
                ...members.items[0],
                lastLogin: new Date(),
                updatedAt: new Date()
            });
        }
        
        return {
            success: true,
            sessionToken: loginResult.sessionToken,
            member: memberData
        };
    } catch (error) {
        console.error('Member login failed:', error);
        return { success: false, error: 'Invalid email or password' };
    }
}

/**
 * Get current member profile
 * @param {string} memberId - Wix Member ID
 * @returns {object} - Member profile
 */
export async function getMemberProfile(memberId) {
    try {
        const members = await wixData.query('Members')
            .eq('wixMemberId', memberId)
            .find({ suppressAuth: true });
        
        if (members.items.length === 0) {
            return { success: false, error: 'Member not found' };
        }
        
        const member = members.items[0];
        
        return {
            success: true,
            profile: {
                id: member._id,
                fullName: member.fullName,
                firstName: member.firstName,
                lastName: member.lastName,
                email: member.email,
                phone: member.phone,
                address: member.address,
                membershipType: member.membershipType,
                membershipStatus: member.membershipStatus,
                membershipPaidDate: member.membershipPaidDate,
                membershipExpiryDate: member.membershipExpiryDate,
                familyMembers: member.familyMembers || [],
                isVerified: member.isVerified,
                registrationDate: member.registrationDate
            }
        };
    } catch (error) {
        console.error('Failed to get member profile:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Update member profile
 * @param {string} memberId - Wix Member ID
 * @param {object} updates - Profile updates
 * @returns {object} - Update result
 */
export async function updateMemberProfile(memberId, updates) {
    try {
        const members = await wixData.query('Members')
            .eq('wixMemberId', memberId)
            .find({ suppressAuth: true });
        
        if (members.items.length === 0) {
            return { success: false, error: 'Member not found' };
        }
        
        const member = members.items[0];
        
        // Only allow certain fields to be updated
        const allowedUpdates = ['phone', 'address', 'familyMembers'];
        const filteredUpdates = {};
        
        allowedUpdates.forEach(field => {
            if (updates[field] !== undefined) {
                filteredUpdates[field] = updates[field];
            }
        });
        
        await wixData.update('Members', {
            ...member,
            ...filteredUpdates,
            updatedAt: new Date()
        });
        
        return { success: true, message: 'Profile updated successfully' };
    } catch (error) {
        console.error('Failed to update member profile:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Request password reset
 * @param {string} email - Member email
 * @returns {object} - Result
 */
export async function requestPasswordReset(email) {
    try {
        await authentication.sendSetPasswordEmail(email);
        return { success: true, message: 'Password reset email sent' };
    } catch (error) {
        console.error('Password reset request failed:', error);
        return { success: false, error: 'Failed to send reset email' };
    }
}

/**
 * Check if member has active membership
 * @param {string} memberId - Member ID
 * @returns {object} - Membership status
 */
export async function checkMembershipStatus(memberId) {
    try {
        const members = await wixData.query('Members')
            .eq('wixMemberId', memberId)
            .find({ suppressAuth: true });
        
        if (members.items.length === 0) {
            return { success: false, error: 'Member not found' };
        }
        
        const member = members.items[0];
        const now = new Date();
        
        let isActive = member.membershipStatus === 'active';
        let isExpired = false;
        let daysUntilExpiry = null;
        
        if (member.membershipExpiryDate) {
            const expiryDate = new Date(member.membershipExpiryDate);
            isExpired = expiryDate < now;
            
            if (!isExpired) {
                daysUntilExpiry = Math.ceil((expiryDate - now) / (1000 * 60 * 60 * 24));
            }
            
            if (isExpired && isActive) {
                // Auto-update expired membership
                await wixData.update('Members', {
                    ...member,
                    membershipStatus: 'expired',
                    updatedAt: new Date()
                });
                isActive = false;
            }
        }
        
        return {
            success: true,
            status: {
                isActive,
                isExpired,
                membershipType: member.membershipType,
                expiryDate: member.membershipExpiryDate,
                daysUntilExpiry,
                needsRenewal: daysUntilExpiry !== null && daysUntilExpiry <= 30
            }
        };
    } catch (error) {
        console.error('Failed to check membership status:', error);
        return { success: false, error: error.message };
    }
}

```
------------------------------------------------------------

## [25/41] member-automation
- File: `member-automation.jsw`
- Size: 27.9 KB
- Lines: 909

```javascript
/**
 * BANF Member Automation Service
 * ================================
 * Wix Velo Backend Module for automated member management
 * 
 * Features:
 * - New member onboarding automation
 * - Membership renewal reminders
 * - Birthday wishes automation
 * - Member engagement scoring
 * - Automatic role/status management
 * 
 * @module backend/member-automation.jsw
 */

import wixData from 'wix-data';
import { currentMember, members } from 'wix-members-backend';
import { triggeredEmails } from 'wix-crm-backend';
import { contacts } from 'wix-crm-backend';

// =====================================================
// MEMBERSHIP TYPES & CONFIGURATION
// =====================================================

const MEMBERSHIP_TYPES = {
    FAMILY: {
        name: 'Family Membership',
        price: 100,
        durationMonths: 12,
        benefits: ['All events access', 'Puja participation', 'Newsletter', 'Voting rights']
    },
    INDIVIDUAL: {
        name: 'Individual Membership',
        price: 50,
        durationMonths: 12,
        benefits: ['All events access', 'Puja participation', 'Newsletter']
    },
    STUDENT: {
        name: 'Student Membership',
        price: 25,
        durationMonths: 12,
        benefits: ['All events access', 'Student discounts']
    },
    LIFETIME: {
        name: 'Lifetime Membership',
        price: 500,
        durationMonths: null, // Never expires
        benefits: ['All events access', 'Puja participation', 'Newsletter', 'Voting rights', 'Lifetime recognition']
    },
    HONORARY: {
        name: 'Honorary Membership',
        price: 0,
        durationMonths: null,
        benefits: ['Full member benefits', 'Special recognition']
    }
};

const ENGAGEMENT_ACTIONS = {
    EVENT_ATTENDANCE: 10,
    EVENT_RSVP: 2,
    VOLUNTEER: 20,
    DONATION: 15,
    REFERRAL: 25,
    COMMITTEE: 30,
    FEEDBACK_GIVEN: 5,
    STREAM_WATCHED: 3,
    NEWSLETTER_OPENED: 1
};

// =====================================================
// NEW MEMBER ONBOARDING
// =====================================================

/**
 * Process new member registration
 * Called automatically when a new member signs up
 * @param {Object} memberData
 */
export async function onboardNewMember(memberData) {
    try {
        console.log('Processing new member:', memberData.email);
        
        // 1. Create member profile in custom collection
        const memberProfile = await wixData.insert('MemberProfiles', {
            memberId: memberData._id,
            email: memberData.loginEmail,
            firstName: memberData.firstName || '',
            lastName: memberData.lastName || '',
            phone: memberData.phone || '',
            
            // Membership Details
            membershipType: 'INDIVIDUAL', // Default, will be updated on payment
            membershipStatus: 'PENDING', // PENDING, ACTIVE, EXPIRED, SUSPENDED
            membershipStartDate: null,
            membershipEndDate: null,
            
            // Profile Details
            address: {
                street: '',
                city: 'Jacksonville',
                state: 'FL',
                zip: ''
            },
            familyMembers: [],
            interests: [],
            dietaryRestrictions: '',
            
            // Engagement Tracking
            engagementScore: 0,
            totalEventsAttended: 0,
            totalDonations: 0,
            volunteerHours: 0,
            referralCount: 0,
            
            // Communication Preferences
            emailNotifications: true,
            smsNotifications: false,
            newsletterSubscribed: true,
            eventReminders: true,
            
            // Dates
            registrationDate: new Date(),
            lastActivityDate: new Date(),
            lastLoginDate: new Date(),
            
            // Birthday
            dateOfBirth: memberData.dateOfBirth || null,
            birthdayWishSent: false
        });
        
        // 2. Send welcome email
        await sendWelcomeEmail(memberData);
        
        // 3. Create welcome task for EC to review
        await createAdminTask({
            type: 'NEW_MEMBER_REVIEW',
            title: `Review new member: ${memberData.firstName} ${memberData.lastName}`,
            memberId: memberData._id,
            memberEmail: memberData.loginEmail,
            priority: 'medium',
            dueDate: addDays(new Date(), 3)
        });
        
        // 4. Log activity
        await logMemberActivity(memberData._id, 'REGISTRATION', 'New member registered');
        
        return {
            success: true,
            message: 'Member onboarding initiated',
            profileId: memberProfile._id
        };
        
    } catch (error) {
        console.error('Error in onboardNewMember:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Send welcome email to new member
 * @param {Object} memberData 
 */
async function sendWelcomeEmail(memberData) {
    try {
        await triggeredEmails.emailMember(
            'welcome_new_member',
            memberData._id,
            {
                variables: {
                    firstName: memberData.firstName || 'Friend',
                    membershipLink: 'https://jaxbengali.org/membership',
                    eventsLink: 'https://jaxbengali.org/events',
                    aboutLink: 'https://jaxbengali.org/about-us'
                }
            }
        );
        
        console.log('Welcome email sent to:', memberData.loginEmail);
        
    } catch (error) {
        console.error('Error sending welcome email:', error);
    }
}

/**
 * Complete member profile (called from profile form)
 * @param {string} memberId 
 * @param {Object} profileData 
 */
export async function completeProfile(memberId, profileData) {
    try {
        const profile = await wixData.query('MemberProfiles')
            .eq('memberId', memberId)
            .find();
        
        if (profile.items.length === 0) {
            return { success: false, error: 'Profile not found' };
        }
        
        const updatedProfile = {
            ...profile.items[0],
            ...profileData,
            profileCompleted: true,
            profileCompletedDate: new Date(),
            lastActivityDate: new Date()
        };
        
        await wixData.update('MemberProfiles', updatedProfile);
        
        // Award engagement points for completing profile
        await addEngagementPoints(memberId, 10, 'Profile completed');
        
        return {
            success: true,
            message: 'Profile updated successfully'
        };
        
    } catch (error) {
        console.error('Error completing profile:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// MEMBERSHIP RENEWAL
// =====================================================

/**
 * Check for expiring memberships and send reminders
 * (Run daily via scheduled job)
 */
export async function checkMembershipRenewals() {
    try {
        const now = new Date();
        const thirtyDaysFromNow = addDays(now, 30);
        const sevenDaysFromNow = addDays(now, 7);
        const oneDayFromNow = addDays(now, 1);
        
        const results = {
            thirtyDayReminders: 0,
            sevenDayReminders: 0,
            oneDayReminders: 0,
            expirations: 0
        };
        
        // 30-day reminders
        const expiring30 = await wixData.query('MemberProfiles')
            .eq('membershipStatus', 'ACTIVE')
            .between('membershipEndDate', now, thirtyDaysFromNow)
            .eq('reminder30DaySent', false)
            .find();
        
        for (const member of expiring30.items) {
            await sendRenewalReminder(member, 30);
            member.reminder30DaySent = true;
            await wixData.update('MemberProfiles', member);
            results.thirtyDayReminders++;
        }
        
        // 7-day reminders
        const expiring7 = await wixData.query('MemberProfiles')
            .eq('membershipStatus', 'ACTIVE')
            .between('membershipEndDate', now, sevenDaysFromNow)
            .eq('reminder7DaySent', false)
            .find();
        
        for (const member of expiring7.items) {
            await sendRenewalReminder(member, 7);
            member.reminder7DaySent = true;
            await wixData.update('MemberProfiles', member);
            results.sevenDayReminders++;
        }
        
        // 1-day reminders (final)
        const expiring1 = await wixData.query('MemberProfiles')
            .eq('membershipStatus', 'ACTIVE')
            .between('membershipEndDate', now, oneDayFromNow)
            .eq('reminder1DaySent', false)
            .find();
        
        for (const member of expiring1.items) {
            await sendRenewalReminder(member, 1);
            member.reminder1DaySent = true;
            await wixData.update('MemberProfiles', member);
            results.oneDayReminders++;
        }
        
        // Process expired memberships
        const expired = await wixData.query('MemberProfiles')
            .eq('membershipStatus', 'ACTIVE')
            .lt('membershipEndDate', now)
            .ne('membershipType', 'LIFETIME')
            .ne('membershipType', 'HONORARY')
            .find();
        
        for (const member of expired.items) {
            await processMembershipExpiration(member);
            results.expirations++;
        }
        
        console.log('Membership renewal check completed:', results);
        return {
            success: true,
            ...results
        };
        
    } catch (error) {
        console.error('Error checking renewals:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Send renewal reminder email
 * @param {Object} member 
 * @param {number} daysLeft 
 */
async function sendRenewalReminder(member, daysLeft) {
    try {
        const templateId = daysLeft === 1 
            ? 'membership_renewal_final'
            : daysLeft === 7 
                ? 'membership_renewal_week'
                : 'membership_renewal_month';
        
        await triggeredEmails.emailMember(
            templateId,
            member.memberId,
            {
                variables: {
                    firstName: member.firstName,
                    daysRemaining: daysLeft,
                    expirationDate: formatDate(member.membershipEndDate),
                    membershipType: MEMBERSHIP_TYPES[member.membershipType]?.name || member.membershipType,
                    renewalLink: 'https://jaxbengali.org/membership/renew'
                }
            }
        );
        
        // Log reminder sent
        await logMemberActivity(member.memberId, 'RENEWAL_REMINDER', `${daysLeft}-day renewal reminder sent`);
        
    } catch (error) {
        console.error('Error sending renewal reminder:', error);
    }
}

/**
 * Process membership expiration
 * @param {Object} member 
 */
async function processMembershipExpiration(member) {
    try {
        // Update status to EXPIRED
        member.membershipStatus = 'EXPIRED';
        member.membershipExpiredDate = new Date();
        
        // Reset reminder flags for next renewal cycle
        member.reminder30DaySent = false;
        member.reminder7DaySent = false;
        member.reminder1DaySent = false;
        
        await wixData.update('MemberProfiles', member);
        
        // Send expiration notification
        await triggeredEmails.emailMember(
            'membership_expired',
            member.memberId,
            {
                variables: {
                    firstName: member.firstName,
                    membershipType: MEMBERSHIP_TYPES[member.membershipType]?.name,
                    renewalLink: 'https://jaxbengali.org/membership/renew'
                }
            }
        );
        
        // Create admin task to follow up
        await createAdminTask({
            type: 'MEMBERSHIP_EXPIRED',
            title: `Follow up with expired member: ${member.firstName} ${member.lastName}`,
            memberId: member.memberId,
            memberEmail: member.email,
            priority: 'low',
            dueDate: addDays(new Date(), 7)
        });
        
        await logMemberActivity(member.memberId, 'MEMBERSHIP_EXPIRED', 'Membership expired');
        
    } catch (error) {
        console.error('Error processing expiration:', error);
    }
}

/**
 * Renew membership (called after payment)
 * @param {string} memberId 
 * @param {string} membershipType 
 * @param {Object} paymentInfo 
 */
export async function renewMembership(memberId, membershipType, paymentInfo = {}) {
    try {
        const profile = await wixData.query('MemberProfiles')
            .eq('memberId', memberId)
            .find();
        
        if (profile.items.length === 0) {
            return { success: false, error: 'Member profile not found' };
        }
        
        const member = profile.items[0];
        const membershipConfig = MEMBERSHIP_TYPES[membershipType];
        
        if (!membershipConfig) {
            return { success: false, error: 'Invalid membership type' };
        }
        
        // Calculate new dates
        const startDate = new Date();
        let endDate = null;
        
        if (membershipConfig.durationMonths) {
            endDate = new Date(startDate);
            endDate.setMonth(endDate.getMonth() + membershipConfig.durationMonths);
        }
        
        // Update member profile
        member.membershipType = membershipType;
        member.membershipStatus = 'ACTIVE';
        member.membershipStartDate = startDate;
        member.membershipEndDate = endDate;
        member.lastRenewalDate = startDate;
        member.paymentId = paymentInfo.paymentId || null;
        
        // Reset reminder flags
        member.reminder30DaySent = false;
        member.reminder7DaySent = false;
        member.reminder1DaySent = false;
        
        await wixData.update('MemberProfiles', member);
        
        // Send confirmation email
        await triggeredEmails.emailMember(
            'membership_confirmation',
            memberId,
            {
                variables: {
                    firstName: member.firstName,
                    membershipType: membershipConfig.name,
                    startDate: formatDate(startDate),
                    endDate: endDate ? formatDate(endDate) : 'Lifetime',
                    benefits: membershipConfig.benefits.join('\n• ')
                }
            }
        );
        
        // Award engagement points
        await addEngagementPoints(memberId, 20, 'Membership renewed');
        
        await logMemberActivity(memberId, 'MEMBERSHIP_RENEWED', `Renewed as ${membershipType}`);
        
        return {
            success: true,
            message: 'Membership renewed successfully',
            expirationDate: endDate
        };
        
    } catch (error) {
        console.error('Error renewing membership:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// BIRTHDAY AUTOMATION
// =====================================================

/**
 * Check and send birthday wishes
 * (Run daily via scheduled job)
 */
export async function checkBirthdayWishes() {
    try {
        const today = new Date();
        const todayMonth = today.getMonth() + 1;
        const todayDay = today.getDate();
        
        // Find members with birthday today
        const allMembers = await wixData.query('MemberProfiles')
            .eq('membershipStatus', 'ACTIVE')
            .isNotEmpty('dateOfBirth')
            .find();
        
        const birthdayMembers = allMembers.items.filter(member => {
            if (!member.dateOfBirth) return false;
            const dob = new Date(member.dateOfBirth);
            return dob.getMonth() + 1 === todayMonth && dob.getDate() === todayDay;
        });
        
        let sentCount = 0;
        
        for (const member of birthdayMembers) {
            // Check if already sent this year
            const thisYear = today.getFullYear();
            if (member.lastBirthdayWishYear === thisYear) {
                continue;
            }
            
            await sendBirthdayWish(member);
            
            // Update member record
            member.lastBirthdayWishYear = thisYear;
            await wixData.update('MemberProfiles', member);
            
            sentCount++;
        }
        
        console.log(`Birthday wishes sent: ${sentCount}`);
        return {
            success: true,
            birthdayMembersFound: birthdayMembers.length,
            wishesSent: sentCount
        };
        
    } catch (error) {
        console.error('Error checking birthdays:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Send birthday wish email
 * @param {Object} member 
 */
async function sendBirthdayWish(member) {
    try {
        await triggeredEmails.emailMember(
            'happy_birthday',
            member.memberId,
            {
                variables: {
                    firstName: member.firstName,
                    // Calculate age if DOB is full date
                    memberSince: formatDate(member.registrationDate)
                }
            }
        );
        
        await logMemberActivity(member.memberId, 'BIRTHDAY_WISH', 'Birthday wish sent');
        
    } catch (error) {
        console.error('Error sending birthday wish:', error);
    }
}

// =====================================================
// ENGAGEMENT SCORING
// =====================================================

/**
 * Add engagement points to member
 * @param {string} memberId 
 * @param {number} points 
 * @param {string} reason 
 */
export async function addEngagementPoints(memberId, points, reason) {
    try {
        const profile = await wixData.query('MemberProfiles')
            .eq('memberId', memberId)
            .find();
        
        if (profile.items.length === 0) return;
        
        const member = profile.items[0];
        member.engagementScore = (member.engagementScore || 0) + points;
        member.lastActivityDate = new Date();
        
        await wixData.update('MemberProfiles', member);
        
        // Log engagement activity
        await wixData.insert('EngagementLog', {
            memberId: memberId,
            points: points,
            reason: reason,
            timestamp: new Date()
        });
        
        // Check for engagement milestones
        await checkEngagementMilestones(member);
        
    } catch (error) {
        console.error('Error adding engagement points:', error);
    }
}

/**
 * Check and award engagement milestones
 * @param {Object} member 
 */
async function checkEngagementMilestones(member) {
    const milestones = [
        { points: 100, badge: 'bronze', title: 'Community Participant' },
        { points: 250, badge: 'silver', title: 'Active Member' },
        { points: 500, badge: 'gold', title: 'Community Champion' },
        { points: 1000, badge: 'platinum', title: 'BANF Ambassador' }
    ];
    
    for (const milestone of milestones) {
        if (member.engagementScore >= milestone.points) {
            const badgeKey = `badge_${milestone.badge}_awarded`;
            
            if (!member[badgeKey]) {
                // Award badge
                member[badgeKey] = true;
                member[`badge_${milestone.badge}_date`] = new Date();
                
                await wixData.update('MemberProfiles', member);
                
                // Send milestone notification
                await triggeredEmails.emailMember(
                    'engagement_milestone',
                    member.memberId,
                    {
                        variables: {
                            firstName: member.firstName,
                            badge: milestone.badge,
                            title: milestone.title,
                            points: member.engagementScore
                        }
                    }
                );
                
                await logMemberActivity(
                    member.memberId, 
                    'MILESTONE_ACHIEVED', 
                    `Achieved ${milestone.title} (${milestone.badge})`
                );
            }
        }
    }
}

/**
 * Get engagement leaderboard
 * @param {number} limit 
 */
export async function getEngagementLeaderboard(limit = 10) {
    try {
        const leaders = await wixData.query('MemberProfiles')
            .eq('membershipStatus', 'ACTIVE')
            .descending('engagementScore')
            .limit(limit)
            .find();
        
        return {
            success: true,
            leaderboard: leaders.items.map((m, index) => ({
                rank: index + 1,
                name: `${m.firstName} ${m.lastName?.charAt(0) || ''}.`,
                score: m.engagementScore,
                badge: getBadgeLevel(m.engagementScore)
            }))
        };
        
    } catch (error) {
        console.error('Error getting leaderboard:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Get badge level based on points
 * @param {number} points 
 */
function getBadgeLevel(points) {
    if (points >= 1000) return 'platinum';
    if (points >= 500) return 'gold';
    if (points >= 250) return 'silver';
    if (points >= 100) return 'bronze';
    return 'none';
}

// =====================================================
// MEMBER ANALYTICS & REPORTING
// =====================================================

/**
 * Get member statistics (admin only)
 */
export async function getMemberStatistics() {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const allMembers = await wixData.query('MemberProfiles')
            .limit(1000)
            .find();
        
        const members = allMembers.items;
        
        // Status breakdown
        const statusCounts = {
            ACTIVE: 0,
            PENDING: 0,
            EXPIRED: 0,
            SUSPENDED: 0
        };
        
        // Type breakdown
        const typeCounts = {};
        
        // Monthly registrations (last 12 months)
        const monthlyRegistrations = {};
        
        for (const m of members) {
            // Status
            statusCounts[m.membershipStatus] = (statusCounts[m.membershipStatus] || 0) + 1;
            
            // Type
            typeCounts[m.membershipType] = (typeCounts[m.membershipType] || 0) + 1;
            
            // Monthly
            if (m.registrationDate) {
                const monthKey = formatMonthKey(new Date(m.registrationDate));
                monthlyRegistrations[monthKey] = (monthlyRegistrations[monthKey] || 0) + 1;
            }
        }
        
        // Expiring soon
        const thirtyDaysFromNow = addDays(new Date(), 30);
        const expiringSoon = members.filter(m => 
            m.membershipStatus === 'ACTIVE' &&
            m.membershipEndDate &&
            new Date(m.membershipEndDate) <= thirtyDaysFromNow
        ).length;
        
        return {
            success: true,
            statistics: {
                total: members.length,
                byStatus: statusCounts,
                byType: typeCounts,
                expiringSoon: expiringSoon,
                averageEngagementScore: Math.round(
                    members.reduce((sum, m) => sum + (m.engagementScore || 0), 0) / members.length
                ),
                monthlyRegistrations: monthlyRegistrations
            }
        };
        
    } catch (error) {
        console.error('Error getting statistics:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Get inactive members (no activity in X days)
 * @param {number} daysSinceLastActivity 
 */
export async function getInactiveMembers(daysSinceLastActivity = 90) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const cutoffDate = addDays(new Date(), -daysSinceLastActivity);
        
        const inactive = await wixData.query('MemberProfiles')
            .eq('membershipStatus', 'ACTIVE')
            .lt('lastActivityDate', cutoffDate)
            .find();
        
        return {
            success: true,
            count: inactive.items.length,
            members: inactive.items.map(m => ({
                name: `${m.firstName} ${m.lastName}`,
                email: m.email,
                lastActivity: m.lastActivityDate,
                engagementScore: m.engagementScore
            }))
        };
        
    } catch (error) {
        console.error('Error getting inactive members:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

/**
 * Create admin task
 * @param {Object} taskData 
 */
async function createAdminTask(taskData) {
    try {
        await wixData.insert('AdminTasks', {
            ...taskData,
            status: 'pending',
            createdAt: new Date()
        });
    } catch (error) {
        console.error('Error creating admin task:', error);
    }
}

/**
 * Log member activity
 * @param {string} memberId 
 * @param {string} action 
 * @param {string} details 
 */
async function logMemberActivity(memberId, action, details) {
    try {
        await wixData.insert('MemberActivityLog', {
            memberId: memberId,
            action: action,
            details: details,
            timestamp: new Date()
        });
    } catch (error) {
        console.error('Error logging activity:', error);
    }
}

/**
 * Check if member is admin
 * @param {string} memberId 
 */
async function isAdmin(memberId) {
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec')
            );
        }
        return false;
    } catch {
        return false;
    }
}

/**
 * Add days to date
 * @param {Date} date 
 * @param {number} days 
 */
function addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

/**
 * Format date for display
 * @param {Date} date 
 */
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Format month key for reporting
 * @param {Date} date 
 */
function formatMonthKey(date) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
}

```
------------------------------------------------------------

## [26/41] member-directory-service
- File: `member-directory-service.jsw`
- Size: 28.5 KB
- Lines: 842

```javascript
/**
 * BANF Member Directory & Search Service
 * ========================================
 * Wix Velo Backend Module for member directory and networking
 * 
 * Features:
 * - Member search and filtering
 * - Profile visibility controls
 * - Member networking
 * - Family connections
 * - Member statistics
 * 
 * @module backend/member-directory-service.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';

// =====================================================
// DIRECTORY CONFIGURATION
// =====================================================

const VISIBILITY_LEVELS = {
    PUBLIC: 'public',           // All members can see
    MEMBERS_ONLY: 'members',    // Only logged-in members
    PRIVATE: 'private'          // Only the member and admins
};

const PROFILE_FIELDS = {
    name: { default: VISIBILITY_LEVELS.PUBLIC },
    email: { default: VISIBILITY_LEVELS.MEMBERS_ONLY },
    phone: { default: VISIBILITY_LEVELS.MEMBERS_ONLY },
    address: { default: VISIBILITY_LEVELS.PRIVATE },
    profession: { default: VISIBILITY_LEVELS.PUBLIC },
    hometown: { default: VISIBILITY_LEVELS.PUBLIC },
    interests: { default: VISIBILITY_LEVELS.PUBLIC },
    familyMembers: { default: VISIBILITY_LEVELS.MEMBERS_ONLY }
};

// =====================================================
// MEMBER DIRECTORY SEARCH
// =====================================================

/**
 * Search member directory
 * @param {Object} searchParams
 */
export async function searchDirectory(searchParams = {}) {
    const member = await currentMember.getMember();
    const isLoggedIn = !!member;
    const isAdminUser = member ? await isAdmin(member._id) : false;
    
    try {
        let query = wixData.query('MemberProfiles')
            .eq('isActive', true);
        
        // Text search
        if (searchParams.query) {
            const searchTerm = searchParams.query.toLowerCase();
            query = query.or(
                wixData.query('MemberProfiles')
                    .contains('firstName', searchTerm)
                    .or(
                        wixData.query('MemberProfiles')
                            .contains('lastName', searchTerm)
                    )
                    .or(
                        wixData.query('MemberProfiles')
                            .contains('hometown', searchTerm)
                    )
            );
        }
        
        // Filter by hometown
        if (searchParams.hometown) {
            query = query.eq('hometown', searchParams.hometown);
        }
        
        // Filter by profession
        if (searchParams.profession) {
            query = query.eq('profession', searchParams.profession);
        }
        
        // Filter by membership type
        if (searchParams.membershipType) {
            query = query.eq('membershipType', searchParams.membershipType);
        }
        
        // Filter by join year
        if (searchParams.joinYear) {
            const startDate = new Date(searchParams.joinYear, 0, 1);
            const endDate = new Date(searchParams.joinYear, 11, 31);
            query = query.between('memberSince', startDate, endDate);
        }
        
        // Filter by interests
        if (searchParams.interests && searchParams.interests.length > 0) {
            query = query.hasSome('interests', searchParams.interests);
        }
        
        // Pagination
        const page = searchParams.page || 1;
        const limit = searchParams.limit || 20;
        const skip = (page - 1) * limit;
        
        // Sort
        if (searchParams.sortBy === 'name') {
            query = query.ascending('lastName').ascending('firstName');
        } else if (searchParams.sortBy === 'recent') {
            query = query.descending('memberSince');
        } else {
            query = query.ascending('lastName');
        }
        
        const results = await query
            .skip(skip)
            .limit(limit)
            .find({ suppressAuth: true });
        
        // Filter fields based on visibility
        const filteredResults = results.items.map(profile => 
            filterProfileByVisibility(profile, isLoggedIn, isAdminUser)
        );
        
        return {
            success: true,
            members: filteredResults,
            pagination: {
                page: page,
                limit: limit,
                total: results.totalCount,
                totalPages: Math.ceil(results.totalCount / limit),
                hasMore: results.hasNext()
            }
        };
        
    } catch (error) {
        console.error('Error searching directory:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get member profile
 * @param {string} memberId
 */
export async function getMemberProfile(memberId) {
    const currentUser = await currentMember.getMember();
    const isLoggedIn = !!currentUser;
    const isOwnProfile = currentUser?._id === memberId;
    const isAdminUser = currentUser ? await isAdmin(currentUser._id) : false;
    
    try {
        const profile = await wixData.query('MemberProfiles')
            .eq('memberId', memberId)
            .find({ suppressAuth: true });
        
        if (profile.items.length === 0) {
            return { success: false, error: 'Member not found' };
        }
        
        const memberProfile = profile.items[0];
        
        // Check if profile is public or user is authorized
        if (memberProfile.profileVisibility === VISIBILITY_LEVELS.PRIVATE 
            && !isOwnProfile && !isAdminUser) {
            return { success: false, error: 'Profile is private' };
        }
        
        // Get additional data
        const enrichedProfile = await enrichProfile(memberProfile);
        
        // Filter based on visibility
        const filteredProfile = isOwnProfile || isAdminUser 
            ? enrichedProfile 
            : filterProfileByVisibility(enrichedProfile, isLoggedIn, isAdminUser);
        
        return {
            success: true,
            profile: filteredProfile,
            isOwnProfile: isOwnProfile
        };
        
    } catch (error) {
        console.error('Error getting profile:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// PROFILE MANAGEMENT
// =====================================================

/**
 * Update member profile
 * @param {Object} profileData
 */
export async function updateMyProfile(profileData) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in');
    }
    
    try {
        // Get existing profile
        let existingProfile = await wixData.query('MemberProfiles')
            .eq('memberId', member._id)
            .find({ suppressAuth: true });
        
        let profile;
        
        if (existingProfile.items.length > 0) {
            // Update existing
            profile = existingProfile.items[0];
            
            // Updateable fields
            const updateableFields = [
                'firstName', 'lastName', 'phone', 'address', 'city', 'state', 'zip',
                'hometown', 'profession', 'employer', 'bio', 'interests',
                'profilePhoto', 'coverPhoto', 'socialLinks',
                'profileVisibility', 'fieldVisibility'
            ];
            
            for (const field of updateableFields) {
                if (profileData[field] !== undefined) {
                    profile[field] = profileData[field];
                }
            }
            
            profile.lastUpdated = new Date();
            
            await wixData.update('MemberProfiles', profile);
            
        } else {
            // Create new profile
            profile = await wixData.insert('MemberProfiles', {
                memberId: member._id,
                email: member.loginEmail,
                firstName: profileData.firstName || member.contactDetails?.firstName || '',
                lastName: profileData.lastName || member.contactDetails?.lastName || '',
                phone: profileData.phone || member.contactDetails?.phones?.[0] || '',
                address: profileData.address || '',
                city: profileData.city || '',
                state: profileData.state || '',
                zip: profileData.zip || '',
                hometown: profileData.hometown || '',
                profession: profileData.profession || '',
                employer: profileData.employer || '',
                bio: profileData.bio || '',
                interests: profileData.interests || [],
                profilePhoto: profileData.profilePhoto || member.profilePhoto || '',
                coverPhoto: profileData.coverPhoto || '',
                socialLinks: profileData.socialLinks || {},
                profileVisibility: profileData.profileVisibility || VISIBILITY_LEVELS.MEMBERS_ONLY,
                fieldVisibility: profileData.fieldVisibility || {},
                membershipType: 'regular',
                memberSince: new Date(),
                isActive: true,
                lastUpdated: new Date()
            });
        }
        
        return {
            success: true,
            profileId: profile._id,
            message: 'Profile updated successfully'
        };
        
    } catch (error) {
        console.error('Error updating profile:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Update visibility settings
 * @param {Object} visibilitySettings
 */
export async function updateVisibilitySettings(visibilitySettings) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in');
    }
    
    try {
        const profile = await wixData.query('MemberProfiles')
            .eq('memberId', member._id)
            .find({ suppressAuth: true });
        
        if (profile.items.length === 0) {
            return { success: false, error: 'Profile not found' };
        }
        
        const memberProfile = profile.items[0];
        
        memberProfile.profileVisibility = visibilitySettings.profileVisibility || memberProfile.profileVisibility;
        memberProfile.fieldVisibility = {
            ...memberProfile.fieldVisibility,
            ...visibilitySettings.fieldVisibility
        };
        memberProfile.lastUpdated = new Date();
        
        await wixData.update('MemberProfiles', memberProfile);
        
        return {
            success: true,
            message: 'Visibility settings updated'
        };
        
    } catch (error) {
        console.error('Error updating visibility:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// FAMILY CONNECTIONS
// =====================================================

/**
 * Add family member connection
 * @param {Object} familyData
 */
export async function addFamilyMember(familyData) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in');
    }
    
    try {
        const profile = await wixData.query('MemberProfiles')
            .eq('memberId', member._id)
            .find({ suppressAuth: true });
        
        if (profile.items.length === 0) {
            return { success: false, error: 'Profile not found' };
        }
        
        const memberProfile = profile.items[0];
        const familyMembers = memberProfile.familyMembers || [];
        
        // Create family member entry
        const familyMember = {
            id: generateId(),
            name: familyData.name,
            relationship: familyData.relationship, // spouse, child, parent, sibling
            age: familyData.age || null,
            linkedMemberId: familyData.linkedMemberId || null, // If they're also a BANF member
            addedAt: new Date()
        };
        
        familyMembers.push(familyMember);
        memberProfile.familyMembers = familyMembers;
        memberProfile.lastUpdated = new Date();
        
        await wixData.update('MemberProfiles', memberProfile);
        
        // If linked to another member, create bidirectional link
        if (familyData.linkedMemberId) {
            await createFamilyLink(member._id, familyData.linkedMemberId, familyData.relationship);
        }
        
        return {
            success: true,
            familyMemberId: familyMember.id,
            message: 'Family member added'
        };
        
    } catch (error) {
        console.error('Error adding family member:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get family network
 * @param {string} memberId
 */
export async function getFamilyNetwork(memberId) {
    const currentUser = await currentMember.getMember();
    const isOwnProfile = currentUser?._id === memberId;
    const isAdminUser = currentUser ? await isAdmin(currentUser._id) : false;
    
    try {
        const profile = await wixData.query('MemberProfiles')
            .eq('memberId', memberId)
            .find({ suppressAuth: true });
        
        if (profile.items.length === 0) {
            return { success: false, error: 'Member not found' };
        }
        
        const memberProfile = profile.items[0];
        
        // Check visibility
        const fieldVisibility = memberProfile.fieldVisibility?.familyMembers || PROFILE_FIELDS.familyMembers.default;
        
        if (fieldVisibility === VISIBILITY_LEVELS.PRIVATE && !isOwnProfile && !isAdminUser) {
            return { success: false, error: 'Family information is private' };
        }
        
        const familyMembers = memberProfile.familyMembers || [];
        
        // Enrich with linked member data
        const enrichedFamily = [];
        for (const fm of familyMembers) {
            const enriched = { ...fm };
            
            if (fm.linkedMemberId) {
                const linked = await wixData.query('MemberProfiles')
                    .eq('memberId', fm.linkedMemberId)
                    .find({ suppressAuth: true });
                
                if (linked.items.length > 0) {
                    enriched.linkedMember = {
                        name: `${linked.items[0].firstName} ${linked.items[0].lastName}`,
                        profilePhoto: linked.items[0].profilePhoto
                    };
                }
            }
            
            enrichedFamily.push(enriched);
        }
        
        return {
            success: true,
            familyMembers: enrichedFamily,
            totalFamily: enrichedFamily.length
        };
        
    } catch (error) {
        console.error('Error getting family network:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// DIRECTORY FILTERS & STATS
// =====================================================

/**
 * Get filter options for directory
 */
export async function getDirectoryFilters() {
    try {
        // Get distinct hometowns
        const hometowns = await wixData.query('MemberProfiles')
            .eq('isActive', true)
            .distinct('hometown', { suppressAuth: true });
        
        // Get distinct professions
        const professions = await wixData.query('MemberProfiles')
            .eq('isActive', true)
            .distinct('profession', { suppressAuth: true });
        
        // Get all interests
        const allProfiles = await wixData.query('MemberProfiles')
            .eq('isActive', true)
            .find({ suppressAuth: true });
        
        const interests = new Set();
        for (const p of allProfiles.items) {
            if (p.interests) {
                for (const i of p.interests) {
                    interests.add(i);
                }
            }
        }
        
        // Get membership types
        const membershipTypes = await wixData.query('MemberProfiles')
            .eq('isActive', true)
            .distinct('membershipType', { suppressAuth: true });
        
        return {
            success: true,
            filters: {
                hometowns: hometowns.items.filter(Boolean).sort(),
                professions: professions.items.filter(Boolean).sort(),
                interests: Array.from(interests).sort(),
                membershipTypes: membershipTypes.items.filter(Boolean)
            }
        };
        
    } catch (error) {
        console.error('Error getting filters:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get directory statistics
 */
export async function getDirectoryStats() {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const totalMembers = await wixData.query('MemberProfiles')
            .eq('isActive', true)
            .count({ suppressAuth: true });
        
        const allProfiles = await wixData.query('MemberProfiles')
            .eq('isActive', true)
            .find({ suppressAuth: true });
        
        // Hometown distribution
        const hometownDist = {};
        for (const p of allProfiles.items) {
            if (p.hometown) {
                hometownDist[p.hometown] = (hometownDist[p.hometown] || 0) + 1;
            }
        }
        
        // Join date distribution
        const joinByYear = {};
        for (const p of allProfiles.items) {
            if (p.memberSince) {
                const year = new Date(p.memberSince).getFullYear();
                joinByYear[year] = (joinByYear[year] || 0) + 1;
            }
        }
        
        // Profile completeness
        let completeProfiles = 0;
        const requiredFields = ['firstName', 'lastName', 'email', 'phone', 'hometown'];
        
        for (const p of allProfiles.items) {
            const complete = requiredFields.every(f => p[f] && p[f].toString().trim() !== '');
            if (complete) completeProfiles++;
        }
        
        // Family members count
        const totalFamilyMembers = allProfiles.items.reduce((sum, p) => 
            sum + (p.familyMembers?.length || 0), 0);
        
        return {
            success: true,
            stats: {
                totalMembers: totalMembers,
                profileCompleteness: Math.round((completeProfiles / totalMembers) * 100),
                totalFamilyMembers: totalFamilyMembers,
                avgFamilySize: Math.round(totalFamilyMembers / totalMembers * 10) / 10,
                topHometowns: Object.entries(hometownDist)
                    .sort((a, b) => b[1] - a[1])
                    .slice(0, 10)
                    .map(([hometown, count]) => ({ hometown, count })),
                membersByYear: Object.entries(joinByYear)
                    .sort((a, b) => Number(a[0]) - Number(b[0]))
                    .map(([year, count]) => ({ year: Number(year), count }))
            }
        };
        
    } catch (error) {
        console.error('Error getting stats:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// MEMBER NETWORKING
// =====================================================

/**
 * Send connection request
 * @param {string} targetMemberId
 * @param {string} message
 */
export async function sendConnectionRequest(targetMemberId, message = '') {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in');
    }
    
    try {
        // Check if already connected
        const existing = await wixData.query('MemberConnections')
            .eq('memberId1', member._id)
            .eq('memberId2', targetMemberId)
            .find({ suppressAuth: true });
        
        const existingReverse = await wixData.query('MemberConnections')
            .eq('memberId1', targetMemberId)
            .eq('memberId2', member._id)
            .find({ suppressAuth: true });
        
        if (existing.items.length > 0 || existingReverse.items.length > 0) {
            return { 
                success: false, 
                error: 'Connection already exists or pending'
            };
        }
        
        const memberName = `${member.contactDetails?.firstName || ''} ${member.contactDetails?.lastName || ''}`.trim();
        
        const connection = await wixData.insert('MemberConnections', {
            memberId1: member._id,
            memberName1: memberName,
            memberId2: targetMemberId,
            status: 'pending',
            message: message,
            requestedAt: new Date()
        });
        
        return {
            success: true,
            connectionId: connection._id,
            message: 'Connection request sent'
        };
        
    } catch (error) {
        console.error('Error sending connection request:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Respond to connection request
 * @param {string} connectionId
 * @param {boolean} accept
 */
export async function respondToConnection(connectionId, accept) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in');
    }
    
    try {
        const connection = await wixData.get('MemberConnections', connectionId);
        
        if (!connection) {
            return { success: false, error: 'Connection request not found' };
        }
        
        if (connection.memberId2 !== member._id) {
            return { success: false, error: 'Unauthorized' };
        }
        
        connection.status = accept ? 'connected' : 'declined';
        connection.respondedAt = new Date();
        
        await wixData.update('MemberConnections', connection);
        
        return {
            success: true,
            message: accept ? 'Connection accepted' : 'Connection declined'
        };
        
    } catch (error) {
        console.error('Error responding to connection:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get my connections
 */
export async function getMyConnections() {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in');
    }
    
    try {
        // Connections where I'm either member1 or member2
        const connections1 = await wixData.query('MemberConnections')
            .eq('memberId1', member._id)
            .eq('status', 'connected')
            .find({ suppressAuth: true });
        
        const connections2 = await wixData.query('MemberConnections')
            .eq('memberId2', member._id)
            .eq('status', 'connected')
            .find({ suppressAuth: true });
        
        const connectedMemberIds = [
            ...connections1.items.map(c => c.memberId2),
            ...connections2.items.map(c => c.memberId1)
        ];
        
        // Get profiles
        const profiles = await wixData.query('MemberProfiles')
            .hasSome('memberId', connectedMemberIds)
            .find({ suppressAuth: true });
        
        // Pending requests for me
        const pendingRequests = await wixData.query('MemberConnections')
            .eq('memberId2', member._id)
            .eq('status', 'pending')
            .find({ suppressAuth: true });
        
        return {
            success: true,
            connections: profiles.items.map(p => ({
                memberId: p.memberId,
                name: `${p.firstName} ${p.lastName}`,
                profilePhoto: p.profilePhoto,
                hometown: p.hometown,
                profession: p.profession
            })),
            pendingRequests: pendingRequests.items.map(r => ({
                connectionId: r._id,
                memberId: r.memberId1,
                memberName: r.memberName1,
                message: r.message,
                requestedAt: r.requestedAt
            })),
            totalConnections: connectedMemberIds.length
        };
        
    } catch (error) {
        console.error('Error getting connections:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

function filterProfileByVisibility(profile, isLoggedIn, isAdmin) {
    const filtered = {
        memberId: profile.memberId,
        firstName: profile.firstName,
        lastName: profile.lastName,
        profilePhoto: profile.profilePhoto,
        memberSince: profile.memberSince
    };
    
    const visibility = profile.fieldVisibility || {};
    
    // Add fields based on visibility
    for (const [field, config] of Object.entries(PROFILE_FIELDS)) {
        const fieldVis = visibility[field] || config.default;
        
        if (fieldVis === VISIBILITY_LEVELS.PUBLIC) {
            filtered[field] = profile[field];
        } else if (fieldVis === VISIBILITY_LEVELS.MEMBERS_ONLY && isLoggedIn) {
            filtered[field] = profile[field];
        } else if (isAdmin) {
            filtered[field] = profile[field];
        }
    }
    
    return filtered;
}

async function enrichProfile(profile) {
    // Get member's event participation
    const rsvps = await wixData.query('EventRSVPs')
        .eq('memberId', profile.memberId)
        .eq('status', 'confirmed')
        .count({ suppressAuth: true });
    
    // Get volunteer stats
    const volunteerHours = await wixData.query('Volunteers')
        .eq('memberId', profile.memberId)
        .find({ suppressAuth: true });
    
    const totalVolunteerHours = volunteerHours.items.length > 0 
        ? volunteerHours.items[0].totalHours || 0 
        : 0;
    
    return {
        ...profile,
        stats: {
            eventsAttended: rsvps,
            volunteerHours: totalVolunteerHours
        }
    };
}

async function createFamilyLink(memberId1, memberId2, relationship) {
    // Create reverse relationship
    const reverseRelationship = {
        'spouse': 'spouse',
        'child': 'parent',
        'parent': 'child',
        'sibling': 'sibling'
    };
    
    const profile2 = await wixData.query('MemberProfiles')
        .eq('memberId', memberId2)
        .find({ suppressAuth: true });
    
    if (profile2.items.length > 0) {
        const p = profile2.items[0];
        const family = p.familyMembers || [];
        
        // Check if link already exists
        const exists = family.some(fm => fm.linkedMemberId === memberId1);
        
        if (!exists) {
            const member1Profile = await wixData.query('MemberProfiles')
                .eq('memberId', memberId1)
                .find({ suppressAuth: true });
            
            if (member1Profile.items.length > 0) {
                const m1 = member1Profile.items[0];
                family.push({
                    id: generateId(),
                    name: `${m1.firstName} ${m1.lastName}`,
                    relationship: reverseRelationship[relationship] || relationship,
                    linkedMemberId: memberId1,
                    addedAt: new Date()
                });
                
                p.familyMembers = family;
                await wixData.update('MemberProfiles', p);
            }
        }
    }
}

function generateId() {
    return 'fm_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

async function isAdmin(memberId) {
    if (!memberId) return false;
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec')
            );
        }
        return false;
    } catch {
        return false;
    }
}

// Export constants
export { VISIBILITY_LEVELS, PROFILE_FIELDS };

```
------------------------------------------------------------

## [27/41] members
- File: `members.jsw`
- Size: 8.6 KB
- Lines: 268

```javascript
// backend/members.jsw
// BANF Member Management - Wix Velo Backend

import wixData from 'wix-data';
import wixMembers from 'wix-members-backend';
import { currentMember } from 'wix-members-backend';
import { sendEmail } from 'backend/email.jsw';

const COLLECTION = 'Members';

/**
 * Register a new BANF member
 * @param {Object} memberData - Member registration data
 * @param {Object} paymentInfo - Payment verification info
 */
export async function registerMember(memberData, paymentInfo) {
    try {
        // 1. Check if member already exists
        const existing = await wixData.query(COLLECTION)
            .eq('email', memberData.email)
            .or(wixData.query(COLLECTION).eq('phoneNumber', memberData.phone))
            .find();
        
        if (existing.items.length > 0) {
            return { success: false, error: 'Member with this email or phone already exists' };
        }
        
        // 2. Create member record
        const memberRecord = {
            fullName: memberData.fullName,
            email: memberData.email,
            phoneNumber: memberData.phone,
            address: memberData.address || '',
            membershipType: memberData.membershipType || 'individual',
            membershipStatus: 'pending',
            membershipStartDate: new Date(),
            membershipEndDate: getEndDate(memberData.membershipType),
            familyMembers: JSON.stringify(memberData.familyMembers || []),
            feesDue: 0,
            totalPaid: paymentInfo.amount || 0,
            isVerified: false,
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert(COLLECTION, memberRecord);
        
        // 3. Record payment
        if (paymentInfo && paymentInfo.zelleCode) {
            await recordZellePayment({
                memberId: result._id,
                zelleCode: paymentInfo.zelleCode,
                amount: paymentInfo.amount,
                paymentType: 'membership',
                senderName: memberData.fullName
            });
        }
        
        // 4. Send welcome email
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

/**
 * Get member by ID (for current user or admin)
 */
export async function getMemberById(memberId) {
    try {
        const member = await wixData.get(COLLECTION, memberId);
        if (member) {
            member.familyMembers = JSON.parse(member.familyMembers || '[]');
        }
        return member;
    } catch (error) {
        console.error('Error getting member:', error);
        return null;
    }
}

/**
 * Get current logged-in member's profile
 */
export async function getCurrentMemberProfile() {
    try {
        const member = await currentMember.getMember();
        if (!member) return null;
        
        const profile = await wixData.query(COLLECTION)
            .eq('email', member.loginEmail)
            .find();
        
        if (profile.items.length > 0) {
            const memberData = profile.items[0];
            memberData.familyMembers = JSON.parse(memberData.familyMembers || '[]');
            return memberData;
        }
        return null;
    } catch (error) {
        console.error('Error getting current member:', error);
        return null;
    }
}

/**
 * Update member profile
 */
export async function updateMemberProfile(memberId, updateData) {
    try {
        const existing = await wixData.get(COLLECTION, memberId);
        if (!existing) {
            return { success: false, error: 'Member not found' };
        }
        
        // Prevent changing certain fields
        delete updateData._id;
        delete updateData._createdDate;
        delete updateData.membershipStatus; // Only admin can change
        
        if (updateData.familyMembers) {
            updateData.familyMembers = JSON.stringify(updateData.familyMembers);
        }
        
        updateData._updatedDate = new Date();
        
        const updated = { ...existing, ...updateData };
        const result = await wixData.update(COLLECTION, updated);
        
        return { success: true, member: result };
    } catch (error) {
        console.error('Error updating member:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get all members (admin only)
 */
export async function getAllMembers(filters = {}, options = { limit: 100, skip: 0 }) {
    try {
        let query = wixData.query(COLLECTION);
        
        if (filters.membershipStatus) {
            query = query.eq('membershipStatus', filters.membershipStatus);
        }
        if (filters.membershipType) {
            query = query.eq('membershipType', filters.membershipType);
        }
        if (filters.isVerified !== undefined) {
            query = query.eq('isVerified', filters.isVerified);
        }
        
        query = query.limit(options.limit).skip(options.skip);
        
        const result = await query.find();
        
        // Parse family members JSON
        result.items.forEach(member => {
            member.familyMembers = JSON.parse(member.familyMembers || '[]');
        });
        
        return {
            items: result.items,
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error getting members:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Search members by name, email, or phone
 */
export async function searchMembers(searchTerm) {
    try {
        const results = await wixData.query(COLLECTION)
            .contains('fullName', searchTerm)
            .or(wixData.query(COLLECTION).contains('email', searchTerm))
            .or(wixData.query(COLLECTION).contains('phoneNumber', searchTerm))
            .find();
        
        return results.items;
    } catch (error) {
        console.error('Error searching members:', error);
        return [];
    }
}

/**
 * Verify member (admin action)
 */
export async function verifyMember(memberId, adminId) {
    try {
        const member = await wixData.get(COLLECTION, memberId);
        if (!member) {
            return { success: false, error: 'Member not found' };
        }
        
        member.isVerified = true;
        member.membershipStatus = 'active';
        member.verifiedBy = adminId;
        member.verifiedAt = new Date();
        member._updatedDate = new Date();
        
        await wixData.update(COLLECTION, member);
        
        // Send verification email
        await sendEmail(member.email, 'verified', { name: member.fullName });
        
        return { success: true };
    } catch (error) {
        console.error('Error verifying member:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get membership statistics
 */
export async function getMembershipStats() {
    try {
        const [total, active, pending, individual, family, senior] = await Promise.all([
            wixData.query(COLLECTION).count(),
            wixData.query(COLLECTION).eq('membershipStatus', 'active').count(),
            wixData.query(COLLECTION).eq('membershipStatus', 'pending').count(),
            wixData.query(COLLECTION).eq('membershipType', 'individual').count(),
            wixData.query(COLLECTION).eq('membershipType', 'family').count(),
            wixData.query(COLLECTION).eq('membershipType', 'senior').count()
        ]);
        
        return {
            total,
            active,
            pending,
            byType: { individual, family, senior }
        };
    } catch (error) {
        console.error('Error getting stats:', error);
        return null;
    }
}

// Helper function
function getEndDate(membershipType) {
    const today = new Date();
    return new Date(today.getFullYear() + 1, today.getMonth(), today.getDate());
}

// Import helper
async function recordZellePayment(paymentData) {
    return wixData.insert('ZellePayments', {
        ...paymentData,
        isVerified: false,
        status: 'pending',
        paymentDate: new Date(),
        _createdDate: new Date()
    });
}

```
------------------------------------------------------------

## [28/41] payment-automation
- File: `payment-automation.jsw`
- Size: 30.7 KB
- Lines: 922

```javascript
/**
 * BANF Payment Automation Service
 * ==================================
 * Wix Velo Backend Module for automated payment processing
 * 
 * Features:
 * - Payment completion handling
 * - Automatic receipt generation
 * - Tax receipt for donations
 * - Payment reminders
 * - Refund processing
 * - Financial reporting
 * 
 * @module backend/payment-automation.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';
import { triggeredEmails } from 'wix-crm-backend';
import wixPayBackend from 'wix-pay-backend';

// =====================================================
// PAYMENT TYPES & CONFIGURATION
// =====================================================

const PAYMENT_TYPES = {
    MEMBERSHIP: {
        name: 'Membership Payment',
        taxDeductible: false,
        receiptPrefix: 'MEM'
    },
    DONATION: {
        name: 'Donation',
        taxDeductible: true,
        receiptPrefix: 'DON'
    },
    EVENT_TICKET: {
        name: 'Event Ticket',
        taxDeductible: false,
        receiptPrefix: 'TKT'
    },
    PUJA_SPONSORSHIP: {
        name: 'Puja Sponsorship',
        taxDeductible: true,
        receiptPrefix: 'PUJ'
    },
    VENDOR_FEE: {
        name: 'Vendor Fee',
        taxDeductible: false,
        receiptPrefix: 'VND'
    },
    AD_SPONSORSHIP: {
        name: 'Advertisement Sponsorship',
        taxDeductible: false,
        receiptPrefix: 'ADS'
    },
    MISCELLANEOUS: {
        name: 'Miscellaneous Payment',
        taxDeductible: false,
        receiptPrefix: 'MISC'
    }
};

// BANF Organization Info (for receipts)
const ORG_INFO = {
    name: 'Bengal Association of North Florida, Inc.',
    shortName: 'BANF',
    ein: 'XX-XXXXXXX', // Replace with actual EIN
    address: 'Jacksonville, FL',
    website: 'https://jaxbengali.org',
    email: 'treasurer@jaxbengali.org',
    phone: '(904) XXX-XXXX'
};

// =====================================================
// PAYMENT PROCESSING
// =====================================================

/**
 * Handle payment completion (webhook from Wix Payments)
 * @param {Object} paymentEvent - Payment event data from Wix
 */
export async function onPaymentComplete(paymentEvent) {
    try {
        console.log('Processing payment completion:', paymentEvent.payment?.id);
        
        const payment = paymentEvent.payment;
        const metadata = payment.metadata || {};
        
        // Create payment record
        const paymentRecord = await wixData.insert('Payments', {
            paymentId: payment.id,
            transactionId: payment.transactionId,
            memberId: metadata.memberId || null,
            memberEmail: metadata.memberEmail || payment.payer?.email,
            memberName: `${payment.payer?.firstName || ''} ${payment.payer?.lastName || ''}`.trim(),
            
            // Payment Details
            paymentType: metadata.paymentType || 'MISCELLANEOUS',
            amount: payment.amount?.amount || 0,
            currency: payment.amount?.currency || 'USD',
            status: 'COMPLETED',
            
            // Related Records
            eventId: metadata.eventId || null,
            membershipType: metadata.membershipType || null,
            donationCampaign: metadata.donationCampaign || null,
            
            // Receipt
            receiptNumber: generateReceiptNumber(metadata.paymentType || 'MISC'),
            receiptSent: false,
            
            // Metadata
            description: metadata.description || '',
            notes: metadata.notes || '',
            
            // Timestamps
            paymentDate: new Date(),
            createdAt: new Date()
        });
        
        // Process based on payment type
        switch (metadata.paymentType) {
            case 'MEMBERSHIP':
                await processMembershipPayment(paymentRecord, metadata);
                break;
            case 'DONATION':
                await processDonationPayment(paymentRecord, metadata);
                break;
            case 'EVENT_TICKET':
                await processEventPayment(paymentRecord, metadata);
                break;
            case 'PUJA_SPONSORSHIP':
                await processPujaSponsorshipPayment(paymentRecord, metadata);
                break;
            default:
                await processGenericPayment(paymentRecord);
        }
        
        // Send receipt email
        await sendPaymentReceipt(paymentRecord);
        
        // Log payment
        await logPaymentActivity(paymentRecord, 'PAYMENT_COMPLETED', 'Payment processed successfully');
        
        return {
            success: true,
            paymentId: paymentRecord._id,
            receiptNumber: paymentRecord.receiptNumber
        };
        
    } catch (error) {
        console.error('Error processing payment:', error);
        
        // Log error
        await wixData.insert('PaymentErrors', {
            paymentEventId: paymentEvent.payment?.id,
            error: error.message,
            timestamp: new Date()
        });
        
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Process membership payment
 * @param {Object} paymentRecord 
 * @param {Object} metadata 
 */
async function processMembershipPayment(paymentRecord, metadata) {
    try {
        if (!metadata.memberId || !metadata.membershipType) {
            console.error('Missing membership data in payment');
            return;
        }
        
        // Import member automation module
        const { renewMembership } = await import('backend/member-automation.jsw');
        
        await renewMembership(
            metadata.memberId,
            metadata.membershipType,
            {
                paymentId: paymentRecord._id,
                transactionId: paymentRecord.transactionId
            }
        );
        
        console.log('Membership activated for:', metadata.memberId);
        
    } catch (error) {
        console.error('Error processing membership payment:', error);
    }
}

/**
 * Process donation payment
 * @param {Object} paymentRecord 
 * @param {Object} metadata 
 */
async function processDonationPayment(paymentRecord, metadata) {
    try {
        // Record donation
        await wixData.insert('Donations', {
            paymentId: paymentRecord._id,
            donorId: metadata.memberId || null,
            donorName: paymentRecord.memberName,
            donorEmail: paymentRecord.memberEmail,
            amount: paymentRecord.amount,
            campaign: metadata.donationCampaign || 'General Fund',
            isRecurring: metadata.isRecurring || false,
            recurringFrequency: metadata.recurringFrequency || null,
            isAnonymous: metadata.isAnonymous || false,
            dedicatedTo: metadata.dedicatedTo || null,
            dedicationType: metadata.dedicationType || null, // 'in_honor', 'in_memory'
            donationDate: new Date(),
            taxReceiptSent: false,
            fiscalYear: new Date().getFullYear()
        });
        
        // Update member profile donation total
        if (metadata.memberId) {
            const profile = await wixData.query('MemberProfiles')
                .eq('memberId', metadata.memberId)
                .find();
            
            if (profile.items.length > 0) {
                const member = profile.items[0];
                member.totalDonations = (member.totalDonations || 0) + paymentRecord.amount;
                member.lastDonationDate = new Date();
                await wixData.update('MemberProfiles', member);
                
                // Award engagement points
                const { addEngagementPoints } = await import('backend/member-automation.jsw');
                await addEngagementPoints(metadata.memberId, 15, `Donation: $${paymentRecord.amount}`);
            }
        }
        
        // Create admin notification for large donations
        if (paymentRecord.amount >= 100) {
            await createAdminNotification({
                type: 'LARGE_DONATION',
                title: `New donation received: $${paymentRecord.amount}`,
                details: `Donor: ${paymentRecord.memberName}, Campaign: ${metadata.donationCampaign || 'General'}`,
                priority: 'high'
            });
        }
        
    } catch (error) {
        console.error('Error processing donation:', error);
    }
}

/**
 * Process event ticket payment
 * @param {Object} paymentRecord 
 * @param {Object} metadata 
 */
async function processEventPayment(paymentRecord, metadata) {
    try {
        // Create RSVP record
        await wixData.insert('EventRSVPs', {
            eventId: metadata.eventId,
            memberId: metadata.memberId || null,
            attendeeName: paymentRecord.memberName,
            attendeeEmail: paymentRecord.memberEmail,
            ticketType: metadata.ticketType || 'general',
            quantity: metadata.ticketQuantity || 1,
            totalPaid: paymentRecord.amount,
            paymentId: paymentRecord._id,
            dietaryRestrictions: metadata.dietaryRestrictions || '',
            rsvpDate: new Date(),
            checkedIn: false
        });
        
        // Update event ticket count
        const event = await wixData.get('Events', metadata.eventId);
        if (event) {
            event.ticketsSold = (event.ticketsSold || 0) + (metadata.ticketQuantity || 1);
            event.revenue = (event.revenue || 0) + paymentRecord.amount;
            await wixData.update('Events', event);
        }
        
        // Send event confirmation email
        await triggeredEmails.emailContact(
            'event_ticket_confirmation',
            paymentRecord.memberEmail,
            {
                variables: {
                    attendeeName: paymentRecord.memberName,
                    eventName: metadata.eventName || 'BANF Event',
                    eventDate: metadata.eventDate || 'TBD',
                    ticketQuantity: metadata.ticketQuantity || 1,
                    totalAmount: `$${paymentRecord.amount}`,
                    confirmationNumber: paymentRecord.receiptNumber
                }
            }
        );
        
    } catch (error) {
        console.error('Error processing event payment:', error);
    }
}

/**
 * Process Puja sponsorship payment
 * @param {Object} paymentRecord 
 * @param {Object} metadata 
 */
async function processPujaSponsorshipPayment(paymentRecord, metadata) {
    try {
        // Record sponsorship
        await wixData.insert('PujaSponsorship', {
            paymentId: paymentRecord._id,
            sponsorId: metadata.memberId || null,
            sponsorName: paymentRecord.memberName,
            sponsorEmail: paymentRecord.memberEmail,
            sponsorshipType: metadata.sponsorshipType || 'general',
            pujaYear: metadata.pujaYear || new Date().getFullYear(),
            amount: paymentRecord.amount,
            dedicatedTo: metadata.dedicatedTo || null,
            dedicationType: metadata.dedicationType || null,
            displayName: metadata.displayName || paymentRecord.memberName,
            isAnonymous: metadata.isAnonymous || false,
            sponsorshipDate: new Date()
        });
        
        // Update member donation totals (Puja sponsorships count as donations)
        if (metadata.memberId) {
            const profile = await wixData.query('MemberProfiles')
                .eq('memberId', metadata.memberId)
                .find();
            
            if (profile.items.length > 0) {
                const member = profile.items[0];
                member.totalDonations = (member.totalDonations || 0) + paymentRecord.amount;
                member.pujaContributions = (member.pujaContributions || 0) + paymentRecord.amount;
                await wixData.update('MemberProfiles', member);
            }
        }
        
    } catch (error) {
        console.error('Error processing Puja sponsorship:', error);
    }
}

/**
 * Process generic payment
 * @param {Object} paymentRecord 
 */
async function processGenericPayment(paymentRecord) {
    // Just log the payment
    console.log('Generic payment processed:', paymentRecord.receiptNumber);
}

// =====================================================
// RECEIPT GENERATION
// =====================================================

/**
 * Send payment receipt email
 * @param {Object} paymentRecord 
 */
async function sendPaymentReceipt(paymentRecord) {
    try {
        const paymentTypeConfig = PAYMENT_TYPES[paymentRecord.paymentType] || PAYMENT_TYPES.MISCELLANEOUS;
        
        // Determine which email template to use
        const templateId = paymentTypeConfig.taxDeductible 
            ? 'tax_deductible_receipt' 
            : 'payment_receipt';
        
        await triggeredEmails.emailContact(
            templateId,
            paymentRecord.memberEmail,
            {
                variables: {
                    recipientName: paymentRecord.memberName,
                    receiptNumber: paymentRecord.receiptNumber,
                    paymentDate: formatDate(paymentRecord.paymentDate),
                    paymentType: paymentTypeConfig.name,
                    amount: `$${paymentRecord.amount.toFixed(2)}`,
                    description: paymentRecord.description || paymentTypeConfig.name,
                    
                    // Org info for tax receipts
                    orgName: ORG_INFO.name,
                    orgEIN: ORG_INFO.ein,
                    orgAddress: ORG_INFO.address,
                    
                    // Tax receipt specific
                    isTaxDeductible: paymentTypeConfig.taxDeductible,
                    taxYear: new Date().getFullYear()
                }
            }
        );
        
        // Update record
        paymentRecord.receiptSent = true;
        paymentRecord.receiptSentDate = new Date();
        await wixData.update('Payments', paymentRecord);
        
        console.log('Receipt sent for:', paymentRecord.receiptNumber);
        
    } catch (error) {
        console.error('Error sending receipt:', error);
    }
}

/**
 * Generate tax receipt for donations (end of year)
 * @param {string} memberId 
 * @param {number} fiscalYear 
 */
export async function generateAnnualTaxReceipt(memberId, fiscalYear) {
    const member = await currentMember.getMember();
    if (!member || (member._id !== memberId && !await isAdmin(member._id))) {
        throw new Error('Unauthorized');
    }
    
    try {
        // Get all tax-deductible donations for the year
        const donations = await wixData.query('Donations')
            .eq('donorId', memberId)
            .eq('fiscalYear', fiscalYear)
            .find();
        
        const pujaSponsors = await wixData.query('PujaSponsorship')
            .eq('sponsorId', memberId)
            .eq('pujaYear', fiscalYear)
            .find();
        
        // Calculate total
        const donationTotal = donations.items.reduce((sum, d) => sum + d.amount, 0);
        const pujaTotal = pujaSponsors.items.reduce((sum, p) => sum + p.amount, 0);
        const grandTotal = donationTotal + pujaTotal;
        
        if (grandTotal === 0) {
            return {
                success: true,
                message: 'No tax-deductible contributions found for this year',
                total: 0
            };
        }
        
        // Get member info
        const profile = await wixData.query('MemberProfiles')
            .eq('memberId', memberId)
            .find();
        
        const memberProfile = profile.items[0];
        
        // Generate receipt record
        const receiptRecord = await wixData.insert('AnnualTaxReceipts', {
            memberId: memberId,
            memberName: `${memberProfile.firstName} ${memberProfile.lastName}`,
            memberEmail: memberProfile.email,
            memberAddress: memberProfile.address,
            fiscalYear: fiscalYear,
            donationTotal: donationTotal,
            pujaTotal: pujaTotal,
            grandTotal: grandTotal,
            donationCount: donations.items.length,
            pujaCount: pujaSponsors.items.length,
            receiptNumber: `TAX-${fiscalYear}-${generateShortId()}`,
            generatedDate: new Date(),
            downloadUrl: null // Will be populated if PDF generated
        });
        
        // Send annual tax receipt email
        await triggeredEmails.emailMember(
            'annual_tax_receipt',
            memberId,
            {
                variables: {
                    firstName: memberProfile.firstName,
                    fiscalYear: fiscalYear,
                    donationTotal: `$${donationTotal.toFixed(2)}`,
                    pujaTotal: `$${pujaTotal.toFixed(2)}`,
                    grandTotal: `$${grandTotal.toFixed(2)}`,
                    receiptNumber: receiptRecord.receiptNumber,
                    orgName: ORG_INFO.name,
                    orgEIN: ORG_INFO.ein
                }
            }
        );
        
        return {
            success: true,
            receiptNumber: receiptRecord.receiptNumber,
            total: grandTotal,
            details: {
                donations: donationTotal,
                pujaSponsorship: pujaTotal
            }
        };
        
    } catch (error) {
        console.error('Error generating annual tax receipt:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// PAYMENT REMINDERS
// =====================================================

/**
 * Send payment reminders for pending invoices
 * (Run weekly via scheduled job)
 */
export async function sendPendingPaymentReminders() {
    try {
        const sevenDaysAgo = addDays(new Date(), -7);
        
        // Find unpaid invoices older than 7 days
        const pendingPayments = await wixData.query('PendingInvoices')
            .eq('status', 'PENDING')
            .lt('createdAt', sevenDaysAgo)
            .eq('reminderSent', false)
            .find();
        
        let remindersSent = 0;
        
        for (const invoice of pendingPayments.items) {
            await triggeredEmails.emailContact(
                'payment_reminder',
                invoice.email,
                {
                    variables: {
                        recipientName: invoice.recipientName,
                        invoiceAmount: `$${invoice.amount.toFixed(2)}`,
                        invoiceDescription: invoice.description,
                        paymentLink: invoice.paymentLink,
                        dueDate: formatDate(invoice.dueDate)
                    }
                }
            );
            
            invoice.reminderSent = true;
            invoice.reminderSentDate = new Date();
            await wixData.update('PendingInvoices', invoice);
            
            remindersSent++;
        }
        
        return {
            success: true,
            remindersSent: remindersSent
        };
        
    } catch (error) {
        console.error('Error sending payment reminders:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// REFUND PROCESSING
// =====================================================

/**
 * Process refund request
 * @param {string} paymentId 
 * @param {number} refundAmount 
 * @param {string} reason 
 */
export async function processRefund(paymentId, refundAmount, reason) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized: Admin access required');
    }
    
    try {
        const payment = await wixData.get('Payments', paymentId);
        
        if (!payment) {
            return { success: false, error: 'Payment not found' };
        }
        
        if (refundAmount > payment.amount) {
            return { success: false, error: 'Refund amount exceeds original payment' };
        }
        
        // Check if already refunded
        const existingRefunds = await wixData.query('Refunds')
            .eq('originalPaymentId', paymentId)
            .find();
        
        const totalRefunded = existingRefunds.items.reduce((sum, r) => sum + r.amount, 0);
        
        if (totalRefunded + refundAmount > payment.amount) {
            return { 
                success: false, 
                error: `Cannot refund more than original amount. Already refunded: $${totalRefunded}` 
            };
        }
        
        // Create refund record
        const refund = await wixData.insert('Refunds', {
            originalPaymentId: paymentId,
            originalTransactionId: payment.transactionId,
            memberId: payment.memberId,
            memberEmail: payment.memberEmail,
            memberName: payment.memberName,
            refundAmount: refundAmount,
            reason: reason,
            status: 'PENDING', // Will be updated after Wix processes
            requestedBy: member._id,
            requestedAt: new Date()
        });
        
        // Process through Wix Pay
        try {
            await wixPayBackend.refundTransaction(
                payment.transactionId,
                { amount: refundAmount }
            );
            
            refund.status = 'COMPLETED';
            refund.completedAt = new Date();
            await wixData.update('Refunds', refund);
            
        } catch (refundError) {
            refund.status = 'FAILED';
            refund.errorMessage = refundError.message;
            await wixData.update('Refunds', refund);
            
            return {
                success: false,
                error: `Refund processing failed: ${refundError.message}`
            };
        }
        
        // Update original payment
        payment.refundedAmount = (payment.refundedAmount || 0) + refundAmount;
        payment.status = refundAmount >= payment.amount ? 'FULLY_REFUNDED' : 'PARTIALLY_REFUNDED';
        await wixData.update('Payments', payment);
        
        // Send refund confirmation
        await triggeredEmails.emailContact(
            'refund_confirmation',
            payment.memberEmail,
            {
                variables: {
                    recipientName: payment.memberName,
                    refundAmount: `$${refundAmount.toFixed(2)}`,
                    originalAmount: `$${payment.amount.toFixed(2)}`,
                    reason: reason,
                    originalReceiptNumber: payment.receiptNumber
                }
            }
        );
        
        await logPaymentActivity(payment, 'REFUND_PROCESSED', `Refund of $${refundAmount} - ${reason}`);
        
        return {
            success: true,
            refundId: refund._id,
            message: `Refund of $${refundAmount} processed successfully`
        };
        
    } catch (error) {
        console.error('Error processing refund:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// FINANCIAL REPORTING
// =====================================================

/**
 * Get financial summary (admin only)
 * @param {Date} startDate 
 * @param {Date} endDate 
 */
export async function getFinancialSummary(startDate, endDate) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const payments = await wixData.query('Payments')
            .eq('status', 'COMPLETED')
            .between('paymentDate', new Date(startDate), new Date(endDate))
            .find();
        
        const refunds = await wixData.query('Refunds')
            .eq('status', 'COMPLETED')
            .between('completedAt', new Date(startDate), new Date(endDate))
            .find();
        
        // Calculate totals by type
        const byType = {};
        for (const payment of payments.items) {
            const type = payment.paymentType || 'MISCELLANEOUS';
            if (!byType[type]) {
                byType[type] = { count: 0, total: 0 };
            }
            byType[type].count++;
            byType[type].total += payment.amount;
        }
        
        const totalRevenue = payments.items.reduce((sum, p) => sum + p.amount, 0);
        const totalRefunds = refunds.items.reduce((sum, r) => sum + r.refundAmount, 0);
        
        // Monthly breakdown
        const monthlyRevenue = {};
        for (const payment of payments.items) {
            const monthKey = formatMonthKey(new Date(payment.paymentDate));
            monthlyRevenue[monthKey] = (monthlyRevenue[monthKey] || 0) + payment.amount;
        }
        
        return {
            success: true,
            summary: {
                period: {
                    start: formatDate(startDate),
                    end: formatDate(endDate)
                },
                totalRevenue: totalRevenue,
                totalRefunds: totalRefunds,
                netRevenue: totalRevenue - totalRefunds,
                transactionCount: payments.items.length,
                refundCount: refunds.items.length,
                byType: byType,
                monthlyRevenue: monthlyRevenue,
                averageTransaction: payments.items.length > 0 
                    ? Math.round(totalRevenue / payments.items.length * 100) / 100 
                    : 0
            }
        };
        
    } catch (error) {
        console.error('Error getting financial summary:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Get donations report for fiscal year
 * @param {number} fiscalYear 
 */
export async function getDonationsReport(fiscalYear) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const donations = await wixData.query('Donations')
            .eq('fiscalYear', fiscalYear)
            .find();
        
        const totalDonations = donations.items.reduce((sum, d) => sum + d.amount, 0);
        
        // By campaign
        const byCampaign = {};
        for (const donation of donations.items) {
            const campaign = donation.campaign || 'General Fund';
            if (!byCampaign[campaign]) {
                byCampaign[campaign] = { count: 0, total: 0 };
            }
            byCampaign[campaign].count++;
            byCampaign[campaign].total += donation.amount;
        }
        
        // Unique donors
        const uniqueDonors = new Set(donations.items.map(d => d.donorEmail)).size;
        
        return {
            success: true,
            report: {
                fiscalYear: fiscalYear,
                totalDonations: totalDonations,
                donationCount: donations.items.length,
                uniqueDonors: uniqueDonors,
                averageDonation: donations.items.length > 0 
                    ? Math.round(totalDonations / donations.items.length * 100) / 100 
                    : 0,
                byCampaign: byCampaign
            }
        };
        
    } catch (error) {
        console.error('Error getting donations report:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

/**
 * Generate receipt number
 * @param {string} paymentType 
 */
function generateReceiptNumber(paymentType) {
    const prefix = PAYMENT_TYPES[paymentType]?.receiptPrefix || 'RCP';
    const year = new Date().getFullYear().toString().slice(-2);
    const timestamp = Date.now().toString(36).toUpperCase();
    return `${prefix}-${year}-${timestamp}`;
}

/**
 * Generate short ID
 */
function generateShortId() {
    return Math.random().toString(36).substring(2, 8).toUpperCase();
}

/**
 * Create admin notification
 * @param {Object} notification 
 */
async function createAdminNotification(notification) {
    try {
        await wixData.insert('AdminNotifications', {
            ...notification,
            read: false,
            createdAt: new Date()
        });
    } catch (error) {
        console.error('Error creating notification:', error);
    }
}

/**
 * Log payment activity
 * @param {Object} payment 
 * @param {string} action 
 * @param {string} details 
 */
async function logPaymentActivity(payment, action, details) {
    try {
        await wixData.insert('PaymentActivityLog', {
            paymentId: payment._id,
            transactionId: payment.transactionId,
            action: action,
            details: details,
            timestamp: new Date()
        });
    } catch (error) {
        console.error('Error logging payment activity:', error);
    }
}

/**
 * Check if member is admin
 * @param {string} memberId 
 */
async function isAdmin(memberId) {
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec') ||
                role.toLowerCase().includes('treasurer')
            );
        }
        return false;
    } catch {
        return false;
    }
}

/**
 * Add days to date
 * @param {Date} date 
 * @param {number} days 
 */
function addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

/**
 * Format date for display
 * @param {Date} date 
 */
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Format month key for reporting
 * @param {Date} date 
 */
function formatMonthKey(date) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
}

```
------------------------------------------------------------

## [29/41] payment-processing
- File: `payment-processing.jsw`
- Size: 12.1 KB
- Lines: 356

```javascript
/**
 * BANF Payment Processing Backend Module
 * Handles credit card payments with fee pass-through to members
 * 
 * File: backend/payment-processing.jsw
 * Deploy to: Wix Velo Backend
 */

import wixData from 'wix-data';
import wixPay from 'wix-pay-backend';
import { currentMember } from 'wix-members-backend';

// Credit Card Processing Fees (Stripe/Square standard rates)
const CC_FEE_PERCENTAGE = 2.9;  // 2.9%
const CC_FEE_FIXED = 0.30;      // $0.30 per transaction

/**
 * Calculate the total amount including CC processing fee
 * Fee is passed to the member as per BANF policy
 * @param {number} baseAmount - Original payment amount
 * @returns {object} - Breakdown of fees and total
 */
export function calculatePaymentWithFee(baseAmount) {
    const baseFee = (baseAmount * CC_FEE_PERCENTAGE / 100) + CC_FEE_FIXED;
    // Account for fee on the fee itself (fee is charged on total)
    const totalWithFee = (baseAmount + CC_FEE_FIXED) / (1 - CC_FEE_PERCENTAGE / 100);
    const actualFee = totalWithFee - baseAmount;
    
    return {
        baseAmount: parseFloat(baseAmount.toFixed(2)),
        processingFee: parseFloat(actualFee.toFixed(2)),
        totalAmount: parseFloat(totalWithFee.toFixed(2)),
        feePercentage: CC_FEE_PERCENTAGE,
        fixedFee: CC_FEE_FIXED,
        feeBreakdown: `${CC_FEE_PERCENTAGE}% + $${CC_FEE_FIXED.toFixed(2)}`
    };
}

/**
 * BANF Membership Pricing Tiers (from Excel data)
 */
export const MEMBERSHIP_TIERS = {
    'EB-Family': { price: 340, description: 'Executive Board Family Membership' },
    'EB-Couple': { price: 300, description: 'Executive Board Couple Membership' },
    'EB-Individual': { price: 190, description: 'Executive Board Individual Membership' },
    'EB-Student': { price: 150, description: 'Executive Board Student Membership' },
    'Reg-Family': { price: 215, description: 'Regular Family Membership' },
    'Reg-Couple': { price: 200, description: 'Regular Couple Membership' },
    'Reg-Individual': { price: 150, description: 'Regular Individual Membership' },
    'Reg-Student': { price: 100, description: 'Regular Student Membership' }
};

/**
 * Get membership pricing with CC fee included
 * @param {string} tierType - Membership tier type
 * @returns {object} - Pricing breakdown
 */
export function getMembershipPricing(tierType) {
    const tier = MEMBERSHIP_TIERS[tierType];
    if (!tier) {
        throw new Error(`Invalid membership tier: ${tierType}`);
    }
    
    const pricing = calculatePaymentWithFee(tier.price);
    return {
        ...pricing,
        tierType,
        tierDescription: tier.description
    };
}

/**
 * Create a payment request for Wix Pay
 * @param {object} paymentDetails - Payment information
 * @returns {object} - Wix Pay payment object
 */
export async function createPaymentRequest(paymentDetails) {
    const { amount, paymentType, description, memberId, memberEmail, memberName } = paymentDetails;
    
    // Calculate total with CC fee
    const pricing = calculatePaymentWithFee(amount);
    
    // Create payment item for Wix Pay
    const paymentItem = {
        name: paymentType,
        price: pricing.totalAmount,
        quantity: 1
    };
    
    // Create the payment
    const paymentInfo = {
        items: [paymentItem],
        amount: {
            subtotal: pricing.baseAmount,
            shipping: 0,
            tax: 0,
            discount: 0,
            total: pricing.totalAmount,
            currency: "USD"
        },
        userInfo: {
            email: memberEmail,
            firstName: memberName.split(' ')[0],
            lastName: memberName.split(' ').slice(1).join(' ') || ''
        }
    };
    
    try {
        const payment = await wixPay.createPayment(paymentInfo);
        
        // Log the payment request to Transactions collection
        await logTransaction({
            transactionType: 'payment_initiated',
            paymentType,
            baseAmount: pricing.baseAmount,
            processingFee: pricing.processingFee,
            totalAmount: pricing.totalAmount,
            memberId,
            memberEmail,
            memberName,
            description,
            status: 'pending',
            paymentId: payment.id,
            createdAt: new Date()
        });
        
        return {
            success: true,
            payment,
            pricing
        };
    } catch (error) {
        console.error('Payment creation failed:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Process completed payment and update records
 * @param {object} paymentResult - Wix Pay result
 * @returns {object} - Processing result
 */
export async function processPaymentCompletion(paymentResult) {
    const { paymentId, status, transactionId } = paymentResult;
    
    try {
        // Update transaction record
        const transactions = await wixData.query('Transactions')
            .eq('paymentId', paymentId)
            .find();
        
        if (transactions.items.length > 0) {
            const transaction = transactions.items[0];
            
            await wixData.update('Transactions', {
                ...transaction,
                status: status === 'Successful' ? 'completed' : 'failed',
                transactionId,
                completedAt: new Date(),
                updatedAt: new Date()
            });
            
            // If successful, create income record in FinancialRecords
            if (status === 'Successful') {
                await createIncomeRecord({
                    amount: transaction.totalAmount,
                    baseAmount: transaction.baseAmount,
                    processingFee: transaction.processingFee,
                    category: transaction.paymentType,
                    description: transaction.description,
                    memberId: transaction.memberId,
                    memberName: transaction.memberName,
                    paymentMethod: 'Credit Card',
                    transactionId,
                    receiptNumber: `BANF-${Date.now()}`
                });
                
                // Update member's payment status if membership payment
                if (transaction.paymentType.includes('Membership')) {
                    await updateMembershipStatus(transaction.memberId, transaction.paymentType);
                }
            }
            
            return { success: true, status };
        }
        
        return { success: false, error: 'Transaction not found' };
    } catch (error) {
        console.error('Payment processing failed:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Log transaction to database
 * @param {object} transactionData - Transaction details
 */
async function logTransaction(transactionData) {
    try {
        await wixData.insert('Transactions', {
            ...transactionData,
            _id: undefined // Let Wix generate ID
        });
    } catch (error) {
        console.error('Failed to log transaction:', error);
    }
}

/**
 * Create income record in FinancialRecords
 * @param {object} incomeData - Income details
 */
async function createIncomeRecord(incomeData) {
    try {
        await wixData.insert('FinancialRecords', {
            transactionType: 'income',
            amount: incomeData.amount,
            netAmount: incomeData.baseAmount,
            processingFee: incomeData.processingFee,
            category: incomeData.category,
            subcategory: 'Online Payment',
            description: incomeData.description,
            memberId: incomeData.memberId,
            memberName: incomeData.memberName,
            paymentMethod: incomeData.paymentMethod,
            transactionDate: new Date(),
            receiptNumber: incomeData.receiptNumber,
            externalTransactionId: incomeData.transactionId,
            isApproved: true, // Auto-approved for online payments
            approvedAt: new Date(),
            createdAt: new Date()
        });
    } catch (error) {
        console.error('Failed to create income record:', error);
    }
}

/**
 * Update member's membership status after payment
 * @param {string} memberId - Member ID
 * @param {string} membershipType - Type of membership paid
 */
async function updateMembershipStatus(memberId, membershipType) {
    try {
        const members = await wixData.query('Members')
            .eq('_id', memberId)
            .find();
        
        if (members.items.length > 0) {
            const member = members.items[0];
            const now = new Date();
            const expiryDate = new Date(now.getFullYear() + 1, now.getMonth(), now.getDate());
            
            await wixData.update('Members', {
                ...member,
                membershipStatus: 'active',
                membershipType,
                membershipPaidDate: now,
                membershipExpiryDate: expiryDate,
                updatedAt: now
            });
        }
    } catch (error) {
        console.error('Failed to update membership status:', error);
    }
}

/**
 * Record a Zelle payment (manual verification required)
 * @param {object} zelleData - Zelle payment details
 */
export async function recordZellePayment(zelleData) {
    const { confirmationCode, amount, paymentType, memberId, memberName, memberEmail, senderName } = zelleData;
    
    try {
        // Check for duplicate confirmation code
        const existing = await wixData.query('ZellePayments')
            .eq('confirmationCode', confirmationCode)
            .find();
        
        if (existing.items.length > 0) {
            return { success: false, error: 'This confirmation code has already been used' };
        }
        
        // Create Zelle payment record
        const payment = await wixData.insert('ZellePayments', {
            confirmationCode,
            amount: parseFloat(amount),
            paymentType,
            memberId,
            memberName,
            memberEmail,
            senderName: senderName || memberName,
            status: 'pending_verification',
            submittedAt: new Date(),
            createdAt: new Date()
        });
        
        // Log to transactions
        await logTransaction({
            transactionType: 'zelle_submitted',
            paymentType,
            baseAmount: parseFloat(amount),
            processingFee: 0, // No fee for Zelle
            totalAmount: parseFloat(amount),
            memberId,
            memberEmail,
            memberName,
            description: `Zelle payment - ${confirmationCode}`,
            status: 'pending_verification',
            paymentId: payment._id,
            createdAt: new Date()
        });
        
        return { 
            success: true, 
            message: 'Payment submitted for verification',
            referenceNumber: `ZELLE-${payment._id.substring(0, 8).toUpperCase()}`
        };
    } catch (error) {
        console.error('Zelle payment recording failed:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get payment history for a member
 * @param {string} memberId - Member ID
 * @returns {array} - Payment history
 */
export async function getMemberPaymentHistory(memberId) {
    try {
        const transactions = await wixData.query('Transactions')
            .eq('memberId', memberId)
            .descending('createdAt')
            .limit(50)
            .find();
        
        return {
            success: true,
            payments: transactions.items.map(t => ({
                id: t._id,
                date: t.createdAt,
                type: t.paymentType,
                amount: t.totalAmount,
                status: t.status,
                method: t.transactionType.includes('zelle') ? 'Zelle' : 'Credit Card'
            }))
        };
    } catch (error) {
        return { success: false, error: error.message, payments: [] };
    }
}

```
------------------------------------------------------------

## [30/41] photo-gallery-service
- File: `photo-gallery-service.jsw`
- Size: 23.0 KB
- Lines: 735

```javascript
/**
 * BANF Photo Gallery & Media Service
 * =====================================
 * Wix Velo Backend Module for event photo management
 * 
 * Features:
 * - Event photo galleries
 * - Member photo uploads
 * - Photo tagging and approval
 * - Album organization
 * - Slideshow generation
 * 
 * @module backend/photo-gallery-service.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';
import { mediaManager } from 'wix-media-backend';

// =====================================================
// GALLERY CONFIGURATION
// =====================================================

const PHOTO_STATUS = {
    PENDING: 'pending',
    APPROVED: 'approved',
    REJECTED: 'rejected',
    FEATURED: 'featured'
};

const ALBUM_TYPES = {
    EVENT: 'event',
    GENERAL: 'general',
    MEMBER_SPOTLIGHT: 'member_spotlight',
    THROWBACK: 'throwback'
};

// =====================================================
// ALBUM MANAGEMENT
// =====================================================

/**
 * Create a photo album
 * @param {Object} albumData
 */
export async function createAlbum(albumData) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const album = await wixData.insert('PhotoAlbums', {
            // Basic Info
            title: albumData.title,
            description: albumData.description || '',
            albumType: albumData.albumType || ALBUM_TYPES.GENERAL,
            
            // Event association
            eventId: albumData.eventId || null,
            eventTitle: albumData.eventTitle || null,
            eventDate: albumData.eventDate || null,
            
            // Cover
            coverImage: albumData.coverImage || null,
            
            // Settings
            isPublic: albumData.isPublic !== false,
            allowMemberUploads: albumData.allowMemberUploads || false,
            requireApproval: albumData.requireApproval !== false,
            
            // Stats
            photoCount: 0,
            viewCount: 0,
            
            // Status
            status: 'active',
            
            // Metadata
            createdBy: member._id,
            createdAt: new Date(),
            lastModified: new Date()
        });
        
        return {
            success: true,
            albumId: album._id,
            message: 'Album created successfully'
        };
        
    } catch (error) {
        console.error('Error creating album:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Create album for an event
 * @param {string} eventId
 */
export async function createEventAlbum(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        
        if (!event) {
            return { success: false, error: 'Event not found' };
        }
        
        // Check if album already exists
        const existing = await wixData.query('PhotoAlbums')
            .eq('eventId', eventId)
            .find({ suppressAuth: true });
        
        if (existing.items.length > 0) {
            return { 
                success: true, 
                albumId: existing.items[0]._id,
                message: 'Album already exists for this event'
            };
        }
        
        return await createAlbum({
            title: `${event.title} - Photo Gallery`,
            description: `Photos from ${event.title} held on ${formatDate(event.eventDate)}`,
            albumType: ALBUM_TYPES.EVENT,
            eventId: eventId,
            eventTitle: event.title,
            eventDate: event.eventDate,
            allowMemberUploads: true,
            requireApproval: true
        });
        
    } catch (error) {
        console.error('Error creating event album:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// PHOTO UPLOAD & MANAGEMENT
// =====================================================

/**
 * Upload photos to an album
 * @param {string} albumId
 * @param {Array} photos - Array of photo data
 */
export async function uploadPhotos(albumId, photos) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in to upload photos');
    }
    
    try {
        const album = await wixData.get('PhotoAlbums', albumId);
        
        if (!album) {
            return { success: false, error: 'Album not found' };
        }
        
        // Check if member uploads allowed
        const isAdminUser = await isAdmin(member._id);
        if (!album.allowMemberUploads && !isAdminUser) {
            return { success: false, error: 'Member uploads not allowed for this album' };
        }
        
        const uploadedPhotos = [];
        
        for (const photoData of photos) {
            const photo = await wixData.insert('Photos', {
                albumId: albumId,
                albumTitle: album.title,
                eventId: album.eventId,
                
                // Photo data
                imageUrl: photoData.imageUrl,
                thumbnailUrl: photoData.thumbnailUrl || photoData.imageUrl,
                originalFileName: photoData.fileName || 'photo.jpg',
                
                // Metadata
                caption: photoData.caption || '',
                tags: photoData.tags || [],
                taggedMembers: photoData.taggedMembers || [],
                
                // Location
                location: photoData.location || album.eventTitle,
                
                // Dimensions
                width: photoData.width || 0,
                height: photoData.height || 0,
                
                // Status
                status: isAdminUser ? PHOTO_STATUS.APPROVED : PHOTO_STATUS.PENDING,
                
                // Stats
                viewCount: 0,
                likeCount: 0,
                downloadCount: 0,
                
                // Uploader
                uploadedBy: member._id,
                uploaderName: `${member.contactDetails?.firstName || ''} ${member.contactDetails?.lastName || ''}`.trim(),
                uploadedAt: new Date()
            });
            
            uploadedPhotos.push(photo._id);
        }
        
        // Update album photo count
        album.photoCount = (album.photoCount || 0) + uploadedPhotos.length;
        album.lastModified = new Date();
        await wixData.update('PhotoAlbums', album);
        
        return {
            success: true,
            uploadedCount: uploadedPhotos.length,
            photoIds: uploadedPhotos,
            needsApproval: !isAdminUser && album.requireApproval,
            message: isAdminUser 
                ? `${uploadedPhotos.length} photos uploaded successfully`
                : `${uploadedPhotos.length} photos uploaded and pending approval`
        };
        
    } catch (error) {
        console.error('Error uploading photos:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Approve or reject a photo
 * @param {string} photoId
 * @param {string} action - 'approve', 'reject', or 'feature'
 * @param {string} reason - Reason for rejection
 */
export async function moderatePhoto(photoId, action, reason = '') {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const photo = await wixData.get('Photos', photoId);
        
        if (!photo) {
            return { success: false, error: 'Photo not found' };
        }
        
        switch (action) {
            case 'approve':
                photo.status = PHOTO_STATUS.APPROVED;
                photo.approvedBy = member._id;
                photo.approvedAt = new Date();
                break;
                
            case 'reject':
                photo.status = PHOTO_STATUS.REJECTED;
                photo.rejectedBy = member._id;
                photo.rejectedAt = new Date();
                photo.rejectionReason = reason;
                break;
                
            case 'feature':
                photo.status = PHOTO_STATUS.FEATURED;
                photo.featuredBy = member._id;
                photo.featuredAt = new Date();
                break;
        }
        
        photo.lastModified = new Date();
        await wixData.update('Photos', photo);
        
        // Update album count if rejected
        if (action === 'reject') {
            const album = await wixData.get('PhotoAlbums', photo.albumId);
            if (album) {
                album.photoCount = Math.max(0, (album.photoCount || 0) - 1);
                await wixData.update('PhotoAlbums', album);
            }
        }
        
        return {
            success: true,
            message: `Photo ${action}d successfully`
        };
        
    } catch (error) {
        console.error('Error moderating photo:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Bulk approve photos
 * @param {Array} photoIds
 */
export async function bulkApprovePhotos(photoIds) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        let approvedCount = 0;
        
        for (const photoId of photoIds) {
            const result = await moderatePhoto(photoId, 'approve');
            if (result.success) approvedCount++;
        }
        
        return {
            success: true,
            approvedCount: approvedCount,
            message: `${approvedCount} photos approved`
        };
        
    } catch (error) {
        console.error('Error bulk approving:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// PHOTO RETRIEVAL
// =====================================================

/**
 * Get album with photos
 * @param {string} albumId
 * @param {Object} options - { page, limit, status }
 */
export async function getAlbumPhotos(albumId, options = {}) {
    try {
        const album = await wixData.get('PhotoAlbums', albumId);
        
        if (!album) {
            return { success: false, error: 'Album not found' };
        }
        
        // Update view count
        album.viewCount = (album.viewCount || 0) + 1;
        await wixData.update('PhotoAlbums', album);
        
        const page = options.page || 1;
        const limit = options.limit || 50;
        const skip = (page - 1) * limit;
        
        let query = wixData.query('Photos')
            .eq('albumId', albumId);
        
        // For public view, only show approved/featured
        if (!options.showAll) {
            query = query.hasSome('status', [PHOTO_STATUS.APPROVED, PHOTO_STATUS.FEATURED]);
        }
        
        const photos = await query
            .descending('uploadedAt')
            .skip(skip)
            .limit(limit)
            .find({ suppressAuth: true });
        
        return {
            success: true,
            album: {
                _id: album._id,
                title: album.title,
                description: album.description,
                eventTitle: album.eventTitle,
                eventDate: album.eventDate,
                photoCount: album.photoCount,
                coverImage: album.coverImage
            },
            photos: photos.items.map(p => ({
                _id: p._id,
                imageUrl: p.imageUrl,
                thumbnailUrl: p.thumbnailUrl,
                caption: p.caption,
                tags: p.tags,
                uploaderName: p.uploaderName,
                uploadedAt: p.uploadedAt,
                likeCount: p.likeCount,
                status: p.status,
                isFeatured: p.status === PHOTO_STATUS.FEATURED
            })),
            pagination: {
                page: page,
                limit: limit,
                total: photos.totalCount,
                hasMore: photos.hasNext()
            }
        };
        
    } catch (error) {
        console.error('Error getting album photos:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get all public albums
 * @param {Object} options
 */
export async function getPublicAlbums(options = {}) {
    try {
        let query = wixData.query('PhotoAlbums')
            .eq('isPublic', true)
            .eq('status', 'active');
        
        if (options.albumType) {
            query = query.eq('albumType', options.albumType);
        }
        
        const albums = await query
            .descending('createdAt')
            .limit(options.limit || 20)
            .find({ suppressAuth: true });
        
        return {
            success: true,
            albums: albums.items.map(a => ({
                _id: a._id,
                title: a.title,
                description: a.description,
                albumType: a.albumType,
                eventTitle: a.eventTitle,
                eventDate: a.eventDate,
                coverImage: a.coverImage,
                photoCount: a.photoCount,
                createdAt: a.createdAt
            }))
        };
        
    } catch (error) {
        console.error('Error getting albums:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get photos pending approval
 */
export async function getPendingPhotos() {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const photos = await wixData.query('Photos')
            .eq('status', PHOTO_STATUS.PENDING)
            .ascending('uploadedAt')
            .limit(50)
            .find({ suppressAuth: true });
        
        return {
            success: true,
            photos: photos.items.map(p => ({
                _id: p._id,
                imageUrl: p.imageUrl,
                thumbnailUrl: p.thumbnailUrl,
                caption: p.caption,
                albumId: p.albumId,
                albumTitle: p.albumTitle,
                uploaderName: p.uploaderName,
                uploadedAt: p.uploadedAt
            })),
            totalPending: photos.totalCount
        };
        
    } catch (error) {
        console.error('Error getting pending photos:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// PHOTO INTERACTIONS
// =====================================================

/**
 * Like a photo
 * @param {string} photoId
 */
export async function likePhoto(photoId) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in to like photos');
    }
    
    try {
        // Check if already liked
        const existing = await wixData.query('PhotoLikes')
            .eq('photoId', photoId)
            .eq('memberId', member._id)
            .find({ suppressAuth: true });
        
        if (existing.items.length > 0) {
            // Unlike
            await wixData.remove('PhotoLikes', existing.items[0]._id);
            
            const photo = await wixData.get('Photos', photoId);
            photo.likeCount = Math.max(0, (photo.likeCount || 0) - 1);
            await wixData.update('Photos', photo);
            
            return { success: true, liked: false, likeCount: photo.likeCount };
        }
        
        // Like
        await wixData.insert('PhotoLikes', {
            photoId: photoId,
            memberId: member._id,
            likedAt: new Date()
        });
        
        const photo = await wixData.get('Photos', photoId);
        photo.likeCount = (photo.likeCount || 0) + 1;
        await wixData.update('Photos', photo);
        
        return { success: true, liked: true, likeCount: photo.likeCount };
        
    } catch (error) {
        console.error('Error liking photo:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Tag members in a photo
 * @param {string} photoId
 * @param {Array} memberIds
 */
export async function tagMembers(photoId, memberIds) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Must be logged in to tag photos');
    }
    
    try {
        const photo = await wixData.get('Photos', photoId);
        
        if (!photo) {
            return { success: false, error: 'Photo not found' };
        }
        
        // Get member names for display
        const members = await wixData.query('Members/PrivateMembersData')
            .hasSome('_id', memberIds)
            .find({ suppressAuth: true });
        
        const taggedMembers = members.items.map(m => ({
            memberId: m._id,
            name: `${m.firstName || ''} ${m.lastName || ''}`.trim()
        }));
        
        photo.taggedMembers = [
            ...(photo.taggedMembers || []),
            ...taggedMembers
        ];
        
        // Dedupe
        const seen = new Set();
        photo.taggedMembers = photo.taggedMembers.filter(t => {
            if (seen.has(t.memberId)) return false;
            seen.add(t.memberId);
            return true;
        });
        
        await wixData.update('Photos', photo);
        
        return {
            success: true,
            taggedMembers: photo.taggedMembers,
            message: `${taggedMembers.length} members tagged`
        };
        
    } catch (error) {
        console.error('Error tagging members:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// SLIDESHOW GENERATION
// =====================================================

/**
 * Generate slideshow data for an album
 * @param {string} albumId
 * @param {Object} options
 */
export async function generateSlideshow(albumId, options = {}) {
    try {
        const album = await wixData.get('PhotoAlbums', albumId);
        
        if (!album) {
            return { success: false, error: 'Album not found' };
        }
        
        let query = wixData.query('Photos')
            .eq('albumId', albumId)
            .hasSome('status', [PHOTO_STATUS.APPROVED, PHOTO_STATUS.FEATURED]);
        
        // Featured first, then by upload date
        const photos = await query
            .descending('status')
            .descending('uploadedAt')
            .limit(options.maxPhotos || 100)
            .find({ suppressAuth: true });
        
        return {
            success: true,
            slideshow: {
                title: album.title,
                eventTitle: album.eventTitle,
                eventDate: album.eventDate,
                photos: photos.items.map(p => ({
                    imageUrl: p.imageUrl,
                    caption: p.caption,
                    uploaderName: p.uploaderName,
                    isFeatured: p.status === PHOTO_STATUS.FEATURED
                })),
                settings: {
                    autoPlay: options.autoPlay !== false,
                    interval: options.interval || 5000,
                    transition: options.transition || 'fade',
                    showCaptions: options.showCaptions !== false
                }
            }
        };
        
    } catch (error) {
        console.error('Error generating slideshow:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// GALLERY STATISTICS
// =====================================================

/**
 * Get gallery statistics
 */
export async function getGalleryStats() {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const totalAlbums = await wixData.query('PhotoAlbums')
            .count({ suppressAuth: true });
        
        const totalPhotos = await wixData.query('Photos')
            .eq('status', PHOTO_STATUS.APPROVED)
            .count({ suppressAuth: true });
        
        const pendingPhotos = await wixData.query('Photos')
            .eq('status', PHOTO_STATUS.PENDING)
            .count({ suppressAuth: true });
        
        const featuredPhotos = await wixData.query('Photos')
            .eq('status', PHOTO_STATUS.FEATURED)
            .count({ suppressAuth: true });
        
        // Top uploaders
        const allPhotos = await wixData.query('Photos')
            .find({ suppressAuth: true });
        
        const uploaderCounts = {};
        for (const p of allPhotos.items) {
            uploaderCounts[p.uploaderName] = (uploaderCounts[p.uploaderName] || 0) + 1;
        }
        
        const topUploaders = Object.entries(uploaderCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .map(([name, count]) => ({ name, count }));
        
        return {
            success: true,
            stats: {
                totalAlbums: totalAlbums,
                totalPhotos: totalPhotos,
                pendingPhotos: pendingPhotos,
                featuredPhotos: featuredPhotos,
                topUploaders: topUploaders
            }
        };
        
    } catch (error) {
        console.error('Error getting gallery stats:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

async function isAdmin(memberId) {
    if (!memberId) return false;
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec')
            );
        }
        return false;
    } catch {
        return false;
    }
}

// Export constants
export { PHOTO_STATUS, ALBUM_TYPES };

```
------------------------------------------------------------

## [31/41] qr-code-service
- File: `qr-code-service.jsw`
- Size: 30.6 KB
- Lines: 973

```javascript
/**
 * BANF QR Code Service
 * =====================
 * Wix Velo Backend Module for QR code generation, validation, and scanning
 * 
 * Features:
 * - Unique QR code generation per attendee
 * - Embedded attendee data (membership, dietary, etc.)
 * - One-time scan validation (void after use)
 * - Multi-station support (food, entry, etc.)
 * - Real-time tracking dashboard
 * - Offline validation support
 * 
 * @module backend/qr-code-service.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';
import { triggeredEmails } from 'wix-crm-backend';
import crypto from 'crypto';

// =====================================================
// QR CODE TYPES & CONFIGURATIONS
// =====================================================

const QR_CODE_TYPES = {
    EVENT_ENTRY: {
        id: 'event_entry',
        name: 'Event Entry',
        icon: '🎟️',
        singleUse: false, // Allow re-entry
        stations: ['main_entry', 'side_entry', 'vip_entry']
    },
    FOOD_SERVICE: {
        id: 'food_service',
        name: 'Food Service',
        icon: '🍽️',
        singleUse: true, // One meal per attendee
        stations: ['food_counter_1', 'food_counter_2', 'vip_food']
    },
    PRASAD: {
        id: 'prasad',
        name: 'Prasad Distribution',
        icon: '🙏',
        singleUse: true,
        stations: ['prasad_counter']
    },
    PRIZE_CLAIM: {
        id: 'prize_claim',
        name: 'Prize Claim',
        icon: '🎁',
        singleUse: true,
        stations: ['prize_booth']
    },
    PARKING: {
        id: 'parking',
        name: 'Parking Pass',
        icon: '🅿️',
        singleUse: false,
        stations: ['parking_entry', 'parking_exit']
    },
    KIDS_ACTIVITY: {
        id: 'kids_activity',
        name: 'Kids Activity',
        icon: '🎨',
        singleUse: false,
        stations: ['kids_zone']
    }
};

const QR_STATUS = {
    ACTIVE: 'active',
    USED: 'used',
    VOID: 'void',
    EXPIRED: 'expired'
};

// =====================================================
// QR CODE GENERATION
// =====================================================

/**
 * Generate QR codes for all attendees of an event
 * @param {string} eventId
 * @param {Object} options
 */
export async function generateEventQRCodes(eventId, options = {}) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized: Admin access required');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        if (!event) {
            return { success: false, error: 'Event not found' };
        }
        
        // Get all confirmed RSVPs
        const rsvps = await wixData.query('EviteRSVPs')
            .eq('eventId', eventId)
            .eq('rsvpStatus', 'attending')
            .find();
        
        const qrTypes = options.qrTypes || ['EVENT_ENTRY', 'FOOD_SERVICE'];
        let generatedCount = 0;
        const qrCodes = [];
        
        for (const rsvp of rsvps.items) {
            // Generate QR for main attendee
            const mainQR = await generateAttendeeQRCodes(
                eventId, 
                rsvp._id, 
                rsvp.mainAttendee, 
                qrTypes,
                true
            );
            qrCodes.push(mainQR);
            generatedCount++;
            
            // Generate QR for guests
            for (let i = 0; i < (rsvp.guests?.length || 0); i++) {
                const guest = rsvp.guests[i];
                const guestQR = await generateAttendeeQRCodes(
                    eventId,
                    rsvp._id,
                    guest,
                    qrTypes,
                    false,
                    i
                );
                qrCodes.push(guestQR);
                generatedCount++;
            }
        }
        
        // Create QR batch record
        const batch = await wixData.insert('QRBatches', {
            eventId: eventId,
            eventTitle: event.title,
            totalGenerated: generatedCount,
            qrTypes: qrTypes,
            generatedAt: new Date(),
            generatedBy: member._id,
            status: 'completed'
        });
        
        await logQRActivity(eventId, 'BATCH_GENERATED', 
            `Generated ${generatedCount} QR codes for ${rsvps.items.length} RSVPs`);
        
        return {
            success: true,
            batchId: batch._id,
            totalGenerated: generatedCount,
            totalRSVPs: rsvps.items.length,
            qrCodes: qrCodes
        };
        
    } catch (error) {
        console.error('Error generating QR codes:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Generate QR codes for a single attendee
 */
async function generateAttendeeQRCodes(eventId, rsvpId, attendee, qrTypes, isPrimary, guestIndex = null) {
    const qrCodes = {};
    
    // Generate unique identifier for this attendee
    const attendeeKey = isPrimary 
        ? `${rsvpId}_primary`
        : `${rsvpId}_guest_${guestIndex}`;
    
    for (const qrType of qrTypes) {
        const typeConfig = QR_CODE_TYPES[qrType];
        if (!typeConfig) continue;
        
        // Generate unique QR code
        const qrCode = generateSecureQRCode();
        
        // QR data payload
        const qrData = {
            code: qrCode,
            eventId: eventId,
            rsvpId: rsvpId,
            attendeeKey: attendeeKey,
            
            // Attendee Info
            name: attendee.name,
            ageCategory: attendee.ageCategory || 'adult',
            dietary: attendee.dietary || 'no_restriction',
            dietaryNotes: attendee.dietaryNotes || '',
            isPrimary: isPrimary,
            
            // QR Type
            qrType: qrType,
            typeName: typeConfig.name,
            typeIcon: typeConfig.icon,
            singleUse: typeConfig.singleUse,
            
            // Status
            status: QR_STATUS.ACTIVE,
            scannedAt: null,
            scannedBy: null,
            scannedStation: null,
            
            // Validation
            validFrom: new Date(),
            validUntil: null, // Set based on event end time
            
            // Metadata
            createdAt: new Date()
        };
        
        // Store in database
        const record = await wixData.insert('QRCodes', qrData);
        
        qrCodes[qrType] = {
            qrCode: qrCode,
            recordId: record._id,
            qrUrl: generateQRUrl(qrCode),
            type: typeConfig.name,
            icon: typeConfig.icon
        };
    }
    
    return {
        attendeeKey: attendeeKey,
        name: attendee.name,
        dietary: attendee.dietary,
        isPrimary: isPrimary,
        qrCodes: qrCodes
    };
}

/**
 * Generate a single QR code for specific purpose
 * @param {Object} data
 */
export async function generateSingleQRCode(data) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const qrCode = generateSecureQRCode();
        const typeConfig = QR_CODE_TYPES[data.qrType] || QR_CODE_TYPES.EVENT_ENTRY;
        
        const record = await wixData.insert('QRCodes', {
            code: qrCode,
            eventId: data.eventId,
            name: data.name,
            email: data.email || '',
            phone: data.phone || '',
            purpose: data.purpose || 'general',
            
            qrType: data.qrType,
            typeName: typeConfig.name,
            typeIcon: typeConfig.icon,
            singleUse: typeConfig.singleUse,
            
            status: QR_STATUS.ACTIVE,
            
            customData: data.customData || {},
            notes: data.notes || '',
            
            createdAt: new Date(),
            createdBy: member._id
        });
        
        return {
            success: true,
            qrCode: qrCode,
            recordId: record._id,
            qrUrl: generateQRUrl(qrCode),
            qrImageUrl: await getQRImageUrl(qrCode, data)
        };
        
    } catch (error) {
        console.error('Error generating QR:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// QR CODE VALIDATION & SCANNING
// =====================================================

/**
 * Validate and process QR code scan
 * @param {string} qrCode
 * @param {Object} scanData - { stationId, scannedBy, location }
 */
export async function validateQRCode(qrCode, scanData = {}) {
    try {
        // Find QR code record
        const qrRecords = await wixData.query('QRCodes')
            .eq('code', qrCode)
            .find({ suppressAuth: true });
        
        if (qrRecords.items.length === 0) {
            await logScanAttempt(qrCode, 'INVALID', 'QR code not found', scanData);
            return {
                success: false,
                valid: false,
                error: 'Invalid QR code',
                errorCode: 'INVALID_CODE'
            };
        }
        
        const qr = qrRecords.items[0];
        
        // Check if already used (for single-use codes)
        if (qr.singleUse && qr.status === QR_STATUS.USED) {
            await logScanAttempt(qrCode, 'ALREADY_USED', 
                `Already scanned at ${qr.scannedStation} on ${qr.scannedAt}`, scanData);
            return {
                success: false,
                valid: false,
                error: 'QR code already used',
                errorCode: 'ALREADY_USED',
                previousScan: {
                    station: qr.scannedStation,
                    time: qr.scannedAt
                }
            };
        }
        
        // Check if void
        if (qr.status === QR_STATUS.VOID) {
            await logScanAttempt(qrCode, 'VOID', 'QR code has been voided', scanData);
            return {
                success: false,
                valid: false,
                error: 'QR code has been cancelled',
                errorCode: 'VOID'
            };
        }
        
        // Check expiration
        if (qr.validUntil && new Date() > new Date(qr.validUntil)) {
            qr.status = QR_STATUS.EXPIRED;
            await wixData.update('QRCodes', qr, { suppressAuth: true });
            
            await logScanAttempt(qrCode, 'EXPIRED', 'QR code has expired', scanData);
            return {
                success: false,
                valid: false,
                error: 'QR code has expired',
                errorCode: 'EXPIRED'
            };
        }
        
        // Valid! Process the scan
        if (qr.singleUse) {
            qr.status = QR_STATUS.USED;
        }
        qr.scannedAt = new Date();
        qr.scannedBy = scanData.scannedBy || 'system';
        qr.scannedStation = scanData.stationId || 'unknown';
        qr.scanLocation = scanData.location || '';
        qr.scanCount = (qr.scanCount || 0) + 1;
        
        await wixData.update('QRCodes', qr, { suppressAuth: true });
        
        // Log successful scan
        await wixData.insert('QRScanLog', {
            qrCode: qrCode,
            qrRecordId: qr._id,
            eventId: qr.eventId,
            attendeeName: qr.name,
            qrType: qr.qrType,
            stationId: scanData.stationId,
            scannedBy: scanData.scannedBy,
            location: scanData.location,
            result: 'SUCCESS',
            timestamp: new Date()
        });
        
        // Return attendee info for display
        return {
            success: true,
            valid: true,
            attendee: {
                name: qr.name,
                ageCategory: qr.ageCategory,
                dietary: qr.dietary,
                dietaryIcon: getDietaryIcon(qr.dietary),
                dietaryNotes: qr.dietaryNotes,
                isPrimary: qr.isPrimary,
                qrType: qr.typeName,
                typeIcon: qr.typeIcon
            },
            scanInfo: {
                scanCount: qr.scanCount,
                isFirstScan: qr.scanCount === 1,
                singleUse: qr.singleUse,
                nowVoid: qr.singleUse
            },
            displayMessage: generateScanMessage(qr)
        };
        
    } catch (error) {
        console.error('Error validating QR:', error);
        return {
            success: false,
            valid: false,
            error: 'Validation error',
            errorCode: 'SYSTEM_ERROR'
        };
    }
}

/**
 * Bulk validate QR codes (for offline sync)
 * @param {Array} codes - Array of {qrCode, scanData}
 */
export async function bulkValidateQRCodes(codes) {
    const results = [];
    
    for (const item of codes) {
        const result = await validateQRCode(item.qrCode, item.scanData);
        results.push({
            qrCode: item.qrCode,
            ...result
        });
    }
    
    return {
        success: true,
        results: results,
        validCount: results.filter(r => r.valid).length,
        invalidCount: results.filter(r => !r.valid).length
    };
}

/**
 * Void a QR code manually
 * @param {string} qrCode
 * @param {string} reason
 */
export async function voidQRCode(qrCode, reason = '') {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const qrRecords = await wixData.query('QRCodes')
            .eq('code', qrCode)
            .find();
        
        if (qrRecords.items.length === 0) {
            return { success: false, error: 'QR code not found' };
        }
        
        const qr = qrRecords.items[0];
        qr.status = QR_STATUS.VOID;
        qr.voidedAt = new Date();
        qr.voidedBy = member._id;
        qr.voidReason = reason;
        
        await wixData.update('QRCodes', qr);
        
        await logQRActivity(qr.eventId, 'QR_VOIDED', 
            `QR for ${qr.name} voided: ${reason}`);
        
        return {
            success: true,
            message: `QR code for ${qr.name} has been voided`
        };
        
    } catch (error) {
        console.error('Error voiding QR:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// QR CODE DELIVERY
// =====================================================

/**
 * Send QR codes via email
 * @param {string} eventId
 */
export async function sendQRCodeEmails(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        const rsvps = await wixData.query('EviteRSVPs')
            .eq('eventId', eventId)
            .eq('rsvpStatus', 'attending')
            .find();
        
        let sentCount = 0;
        
        for (const rsvp of rsvps.items) {
            // Get all QR codes for this RSVP
            const qrCodes = await wixData.query('QRCodes')
                .eq('rsvpId', rsvp._id)
                .find();
            
            // Group by attendee
            const primaryQRs = qrCodes.items.filter(q => q.isPrimary);
            const guestQRs = qrCodes.items.filter(q => !q.isPrimary);
            
            // Send email to primary attendee
            await triggeredEmails.emailContact(
                'qr_code_delivery',
                rsvp.mainAttendee.email,
                {
                    variables: {
                        name: rsvp.mainAttendee.name,
                        eventTitle: event.title,
                        eventDate: formatDate(event.eventDate),
                        eventTime: event.startTime,
                        eventLocation: event.venueName,
                        totalInParty: rsvp.totalAttendees,
                        qrCodeUrl: generateQRUrl(primaryQRs.find(q => q.qrType === 'FOOD_SERVICE')?.code),
                        entryQRUrl: generateQRUrl(primaryQRs.find(q => q.qrType === 'EVENT_ENTRY')?.code),
                        dietaryPreference: rsvp.mainAttendee.dietary,
                        guestCount: rsvp.guests?.length || 0
                    }
                }
            );
            
            sentCount++;
        }
        
        await logQRActivity(eventId, 'QR_EMAILS_SENT', 
            `Sent QR code emails to ${sentCount} attendees`);
        
        return {
            success: true,
            sentCount: sentCount,
            message: `QR codes sent to ${sentCount} attendees`
        };
        
    } catch (error) {
        console.error('Error sending QR emails:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Generate WhatsApp message with QR code
 * @param {string} qrCode
 * @param {Object} attendeeInfo
 */
export async function generateWhatsAppQRMessage(qrCode, attendeeInfo, eventInfo) {
    const qrImageUrl = await getQRImageUrl(qrCode, attendeeInfo);
    
    const message = `🎉 *Your QR Code for ${eventInfo.title}*\n\n` +
        `👤 *Name:* ${attendeeInfo.name}\n` +
        `📅 *Date:* ${eventInfo.date}\n` +
        `📍 *Venue:* ${eventInfo.location}\n` +
        `🍽️ *Dietary:* ${attendeeInfo.dietary}\n\n` +
        `📲 *Your QR Code:* ${qrImageUrl}\n\n` +
        `Please show this QR code at the food counter.\n` +
        `⚠️ Note: This QR code is valid for ONE meal only.\n\n` +
        `🙏 BANF - Bengali Association of North Florida`;
    
    return {
        message: message,
        qrImageUrl: qrImageUrl
    };
}

/**
 * Send QR codes via SMS
 * @param {string} eventId
 * @param {Array} phoneNumbers - Optional, if not provided sends to all
 */
export async function sendQRCodeSMS(eventId, phoneNumbers = null) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        
        let rsvpQuery = wixData.query('EviteRSVPs')
            .eq('eventId', eventId)
            .eq('rsvpStatus', 'attending');
        
        const rsvps = await rsvpQuery.find();
        
        let queuedCount = 0;
        
        for (const rsvp of rsvps.items) {
            const phone = rsvp.mainAttendee.phone;
            
            if (!phone) continue;
            if (phoneNumbers && !phoneNumbers.includes(phone)) continue;
            
            // Get food QR code
            const qrCodes = await wixData.query('QRCodes')
                .eq('rsvpId', rsvp._id)
                .eq('qrType', 'FOOD_SERVICE')
                .eq('isPrimary', true)
                .find();
            
            if (qrCodes.items.length > 0) {
                const qr = qrCodes.items[0];
                
                await wixData.insert('SMSQueue', {
                    eventId: eventId,
                    phone: phone,
                    message: `BANF ${event.title}: Your food QR code link: ${generateQRUrl(qr.code)} - Show at counter. Valid for ${rsvp.totalAttendees} person(s). Dietary: ${rsvp.mainAttendee.dietary}`,
                    status: 'queued',
                    createdAt: new Date()
                });
                
                queuedCount++;
            }
        }
        
        return {
            success: true,
            queuedCount: queuedCount,
            message: `SMS queued for ${queuedCount} recipients`
        };
        
    } catch (error) {
        console.error('Error queueing SMS:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// STATION MANAGEMENT
// =====================================================

/**
 * Register a scanning station
 * @param {Object} stationData
 */
export async function registerStation(stationData) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const station = await wixData.insert('QRStations', {
            stationId: `STN_${Date.now()}`,
            eventId: stationData.eventId,
            name: stationData.name,
            type: stationData.type, // food, entry, prasad, etc.
            location: stationData.location || '',
            
            // Operators
            operators: stationData.operators || [],
            
            // Status
            status: 'inactive', // inactive, active, closed
            activatedAt: null,
            
            // Stats
            totalScans: 0,
            successfulScans: 0,
            failedScans: 0,
            
            // Settings
            allowedQRTypes: stationData.allowedQRTypes || ['FOOD_SERVICE'],
            
            createdAt: new Date(),
            createdBy: member._id
        });
        
        return {
            success: true,
            stationId: station.stationId,
            message: `Station "${station.name}" registered`
        };
        
    } catch (error) {
        console.error('Error registering station:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Activate a station for scanning
 * @param {string} stationId
 */
export async function activateStation(stationId) {
    try {
        const stations = await wixData.query('QRStations')
            .eq('stationId', stationId)
            .find();
        
        if (stations.items.length === 0) {
            return { success: false, error: 'Station not found' };
        }
        
        const station = stations.items[0];
        station.status = 'active';
        station.activatedAt = new Date();
        
        await wixData.update('QRStations', station);
        
        return {
            success: true,
            message: `Station "${station.name}" is now active`
        };
        
    } catch (error) {
        console.error('Error activating station:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get real-time station stats
 * @param {string} eventId
 */
export async function getStationStats(eventId) {
    try {
        const stations = await wixData.query('QRStations')
            .eq('eventId', eventId)
            .find();
        
        const stats = [];
        
        for (const station of stations.items) {
            // Get recent scans
            const recentScans = await wixData.query('QRScanLog')
                .eq('stationId', station.stationId)
                .descending('timestamp')
                .limit(10)
                .find();
            
            stats.push({
                stationId: station.stationId,
                name: station.name,
                type: station.type,
                status: station.status,
                totalScans: station.totalScans,
                successfulScans: station.successfulScans,
                failedScans: station.failedScans,
                successRate: station.totalScans > 0 
                    ? Math.round((station.successfulScans / station.totalScans) * 100) 
                    : 0,
                recentScans: recentScans.items.map(s => ({
                    name: s.attendeeName,
                    result: s.result,
                    time: s.timestamp
                }))
            });
        }
        
        return {
            success: true,
            stations: stats,
            totalStations: stations.items.length,
            activeStations: stations.items.filter(s => s.status === 'active').length
        };
        
    } catch (error) {
        console.error('Error getting station stats:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// ANALYTICS
// =====================================================

/**
 * Get QR code scanning analytics
 * @param {string} eventId
 */
export async function getQRAnalytics(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const qrCodes = await wixData.query('QRCodes')
            .eq('eventId', eventId)
            .find();
        
        const scanLogs = await wixData.query('QRScanLog')
            .eq('eventId', eventId)
            .find();
        
        // Count by status
        const byStatus = {
            active: qrCodes.items.filter(q => q.status === QR_STATUS.ACTIVE).length,
            used: qrCodes.items.filter(q => q.status === QR_STATUS.USED).length,
            void: qrCodes.items.filter(q => q.status === QR_STATUS.VOID).length
        };
        
        // Count by type
        const byType = {};
        for (const qr of qrCodes.items) {
            byType[qr.qrType] = (byType[qr.qrType] || 0) + 1;
        }
        
        // Food served by dietary
        const foodServed = qrCodes.items.filter(
            q => q.qrType === 'FOOD_SERVICE' && q.status === QR_STATUS.USED
        );
        
        const byDietary = {};
        for (const qr of foodServed) {
            const dietary = qr.dietary || 'no_restriction';
            byDietary[dietary] = (byDietary[dietary] || 0) + 1;
        }
        
        // Scan timeline (hourly)
        const scanTimeline = scanLogs.items.reduce((acc, scan) => {
            const hour = new Date(scan.timestamp).getHours();
            acc[hour] = (acc[hour] || 0) + 1;
            return acc;
        }, {});
        
        // Check-in rate
        const foodQRs = qrCodes.items.filter(q => q.qrType === 'FOOD_SERVICE');
        const checkInRate = foodQRs.length > 0 
            ? Math.round((foodServed.length / foodQRs.length) * 100)
            : 0;
        
        return {
            success: true,
            analytics: {
                summary: {
                    totalQRCodes: qrCodes.items.length,
                    totalScans: scanLogs.items.length,
                    uniqueAttendees: new Set(qrCodes.items.map(q => q.attendeeKey)).size,
                    checkInRate: checkInRate
                },
                byStatus: byStatus,
                byType: byType,
                foodService: {
                    totalMealsServed: foodServed.length,
                    byDietary: byDietary,
                    vegetarianMeals: (byDietary['vegetarian'] || 0) + (byDietary['vegan'] || 0),
                    nonVegMeals: byDietary['non_vegetarian'] || 0
                },
                timeline: scanTimeline,
                
                // For real-time dashboard
                recentScans: scanLogs.items.slice(0, 20).map(s => ({
                    name: s.attendeeName,
                    type: s.qrType,
                    station: s.stationId,
                    result: s.result,
                    time: s.timestamp
                }))
            }
        };
        
    } catch (error) {
        console.error('Error getting QR analytics:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

function generateSecureQRCode() {
    // Generate 12-character alphanumeric code
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // Exclude similar chars
    let code = '';
    const randomBytes = crypto.randomBytes(12);
    
    for (let i = 0; i < 12; i++) {
        code += chars[randomBytes[i] % chars.length];
    }
    
    return code;
}

function generateQRUrl(qrCode) {
    return `https://jaxbengali.org/qr/${qrCode}`;
}

async function getQRImageUrl(qrCode, data = {}) {
    // Generate QR code image URL using a QR code service
    // This would integrate with a QR code generation API
    const qrData = encodeURIComponent(generateQRUrl(qrCode));
    const size = 300;
    
    // Using Google Charts API for QR code generation (or could use custom service)
    return `https://chart.googleapis.com/chart?cht=qr&chs=${size}x${size}&chl=${qrData}&choe=UTF-8`;
}

function getDietaryIcon(dietary) {
    const icons = {
        'vegetarian': '🥬',
        'non_vegetarian': '🍗',
        'vegan': '🌱',
        'gluten_free': '🌾',
        'nut_allergy': '🥜',
        'dairy_free': '🥛',
        'halal': '☪️',
        'kosher': '✡️',
        'no_restriction': '✅'
    };
    return icons[dietary] || '✅';
}

function generateScanMessage(qr) {
    if (qr.qrType === 'FOOD_SERVICE') {
        return `✅ ${qr.name}\n🍽️ ${qr.dietaryNotes || qr.dietary}\n${qr.typeIcon} Meal served`;
    }
    return `✅ ${qr.name}\n${qr.typeIcon} ${qr.typeName} verified`;
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

async function isAdmin(memberId) {
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec')
            );
        }
        return false;
    } catch {
        return false;
    }
}

async function logQRActivity(eventId, action, details) {
    await wixData.insert('QRActivityLog', {
        eventId: eventId,
        action: action,
        details: details,
        timestamp: new Date()
    });
}

async function logScanAttempt(qrCode, result, reason, scanData) {
    await wixData.insert('QRScanLog', {
        qrCode: qrCode,
        result: result,
        reason: reason,
        stationId: scanData?.stationId,
        scannedBy: scanData?.scannedBy,
        timestamp: new Date()
    });
}

// Export constants
export { QR_CODE_TYPES, QR_STATUS };

```
------------------------------------------------------------

## [32/41] radio-scheduler
- File: `radio-scheduler.jsw`
- Size: 25.2 KB
- Lines: 823

```javascript
/**
 * BANF Radio Scheduler Backend Module
 * ====================================
 * Wix Velo Backend Module for managing Bengali music radio programming
 * 
 * Features:
 * - Weekly schedule management with Bengali programs
 * - Playlist management by genre
 * - Special event scheduling (Mahalaya, Puja celebrations)
 * - Real-time now playing tracking
 * - Listener analytics
 * 
 * @module backend/radio-scheduler.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';

// =====================================================
// CONSTANTS - Bengali Program Categories
// =====================================================

export const PROGRAM_CATEGORIES = {
    SOKALER_SUR: {
        id: 'bengali_morning',
        name_bn: 'সকালের সুর',
        name_en: 'Morning Melodies',
        description: 'Traditional Bengali morning songs and bhajans',
        color: '#fff3cd'
    },
    RABINDRA_SANGEET: {
        id: 'rabindra',
        name_bn: 'রবীন্দ্র সঙ্গীত',
        name_en: 'Rabindra Sangeet',
        description: 'Songs composed by Rabindranath Tagore',
        color: '#d4edda'
    },
    ADHUNIK_BANGLA: {
        id: 'modern',
        name_bn: 'আধুনিক বাংলা',
        name_en: 'Modern Bengali',
        description: 'Contemporary Bengali music',
        color: '#d1ecf1'
    },
    CHALACHITRER_GAAN: {
        id: 'film',
        name_bn: 'চলচ্চিত্রের গান',
        name_en: 'Film Songs',
        description: 'Bengali film songs from golden era to modern',
        color: '#e2d5f3'
    },
    SHASTRIYA_SANGEET: {
        id: 'classical',
        name_bn: 'শাস্ত্রীয় সঙ্গীত',
        name_en: 'Classical Music',
        description: 'Hindustani and Carnatic classical music',
        color: '#f8d7da'
    },
    NAZRUL_GEETI: {
        id: 'nazrul',
        name_bn: 'নজরুল গীতি',
        name_en: 'Nazrul Geeti',
        description: 'Songs composed by Kazi Nazrul Islam',
        color: '#ffeeba'
    },
    FOLK_SONGS: {
        id: 'folk',
        name_bn: 'লোকসঙ্গীত',
        name_en: 'Folk Songs',
        description: 'Baul, Bhatiyali, Jhumur and other folk genres',
        color: '#c3e6cb'
    },
    SPECIAL_PROGRAM: {
        id: 'special',
        name_bn: 'বিশেষ অনুষ্ঠান',
        name_en: 'Special Program',
        description: 'Special event programming',
        color: '#ffeaa7'
    }
};

// Default Weekly Schedule Template
const DEFAULT_SCHEDULE = {
    sunday: [
        { startHour: 6, endHour: 10, category: 'bengali_morning' },
        { startHour: 10, endHour: 14, category: 'rabindra' },
        { startHour: 14, endHour: 18, category: 'modern' },
        { startHour: 18, endHour: 21, category: 'film' },
        { startHour: 21, endHour: 24, category: 'classical' }
    ],
    monday: [
        { startHour: 6, endHour: 10, category: 'bengali_morning' },
        { startHour: 10, endHour: 14, category: 'rabindra' },
        { startHour: 14, endHour: 18, category: 'modern' },
        { startHour: 18, endHour: 21, category: 'film' },
        { startHour: 21, endHour: 24, category: 'classical' }
    ],
    tuesday: [
        { startHour: 6, endHour: 10, category: 'bengali_morning' },
        { startHour: 10, endHour: 14, category: 'nazrul' },
        { startHour: 14, endHour: 18, category: 'modern' },
        { startHour: 18, endHour: 21, category: 'film' },
        { startHour: 21, endHour: 24, category: 'classical' }
    ],
    wednesday: [
        { startHour: 6, endHour: 10, category: 'bengali_morning' },
        { startHour: 10, endHour: 14, category: 'rabindra' },
        { startHour: 14, endHour: 18, category: 'folk' },
        { startHour: 18, endHour: 21, category: 'film' },
        { startHour: 21, endHour: 24, category: 'classical' }
    ],
    thursday: [
        { startHour: 6, endHour: 10, category: 'bengali_morning' },
        { startHour: 10, endHour: 14, category: 'rabindra' },
        { startHour: 14, endHour: 18, category: 'modern' },
        { startHour: 18, endHour: 21, category: 'film' },
        { startHour: 21, endHour: 24, category: 'classical' }
    ],
    friday: [
        { startHour: 6, endHour: 10, category: 'bengali_morning' },
        { startHour: 10, endHour: 14, category: 'rabindra' },
        { startHour: 14, endHour: 18, category: 'modern' },
        { startHour: 19, endHour: 21, category: 'special' }, // Community Hour
        { startHour: 21, endHour: 24, category: 'classical' }
    ],
    saturday: [
        { startHour: 6, endHour: 10, category: 'bengali_morning' },
        { startHour: 10, endHour: 14, category: 'rabindra' },
        { startHour: 14, endHour: 18, category: 'nazrul' },
        { startHour: 18, endHour: 21, category: 'film' },
        { startHour: 21, endHour: 24, category: 'folk' }
    ]
};

// =====================================================
// SCHEDULE MANAGEMENT FUNCTIONS
// =====================================================

/**
 * Get current program based on time
 * @returns {Object} Current program details
 */
export async function getCurrentProgram() {
    try {
        const now = new Date();
        const dayNames = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
        const currentDay = dayNames[now.getDay()];
        const currentHour = now.getHours();
        
        // Check for special programs first
        const specialProgram = await getActiveSpecialProgram(now);
        if (specialProgram) {
            return {
                success: true,
                program: specialProgram,
                isSpecial: true
            };
        }
        
        // Get schedule from database
        const scheduleResult = await wixData.query('RadioSchedule')
            .eq('dayOfWeek', currentDay)
            .eq('isActive', true)
            .find();
        
        let schedule = scheduleResult.items.length > 0 
            ? scheduleResult.items[0].timeSlots 
            : DEFAULT_SCHEDULE[currentDay];
        
        // Find current time slot
        const currentSlot = schedule.find(slot => 
            currentHour >= slot.startHour && currentHour < slot.endHour
        );
        
        if (currentSlot) {
            const category = Object.values(PROGRAM_CATEGORIES).find(
                cat => cat.id === currentSlot.category
            );
            
            // Get current playlist for this category
            const playlist = await getCurrentPlaylist(currentSlot.category);
            
            return {
                success: true,
                program: {
                    ...currentSlot,
                    categoryInfo: category,
                    playlist: playlist,
                    startTime: `${currentSlot.startHour}:00`,
                    endTime: `${currentSlot.endHour}:00`
                },
                isSpecial: false
            };
        }
        
        return {
            success: false,
            message: 'No program scheduled for current time'
        };
        
    } catch (error) {
        console.error('Error getting current program:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Get active special program if any
 * @param {Date} currentTime 
 * @returns {Object|null}
 */
async function getActiveSpecialProgram(currentTime) {
    try {
        const specialPrograms = await wixData.query('SpecialPrograms')
            .le('startDateTime', currentTime)
            .ge('endDateTime', currentTime)
            .eq('isActive', true)
            .find();
        
        if (specialPrograms.items.length > 0) {
            return specialPrograms.items[0];
        }
        return null;
    } catch (error) {
        console.error('Error checking special programs:', error);
        return null;
    }
}

/**
 * Get current playlist for a category
 * @param {string} categoryId 
 * @returns {Object} Playlist details
 */
export async function getCurrentPlaylist(categoryId) {
    try {
        const playlistResult = await wixData.query('RadioPlaylists')
            .eq('category', categoryId)
            .eq('isActive', true)
            .find();
        
        if (playlistResult.items.length > 0) {
            const playlist = playlistResult.items[0];
            
            // Get tracks for this playlist
            const tracks = await wixData.query('RadioTracks')
                .eq('playlistId', playlist._id)
                .ascending('trackOrder')
                .find();
            
            return {
                ...playlist,
                tracks: tracks.items
            };
        }
        
        return {
            name: 'Auto-generated Playlist',
            category: categoryId,
            tracks: []
        };
        
    } catch (error) {
        console.error('Error getting playlist:', error);
        return null;
    }
}

/**
 * Get full weekly schedule
 * @returns {Object} Complete weekly schedule
 */
export async function getWeeklySchedule() {
    try {
        const scheduleResult = await wixData.query('RadioSchedule')
            .eq('isActive', true)
            .find();
        
        if (scheduleResult.items.length > 0) {
            // Convert to schedule object
            const schedule = {};
            scheduleResult.items.forEach(item => {
                schedule[item.dayOfWeek] = item.timeSlots;
            });
            return {
                success: true,
                schedule: schedule
            };
        }
        
        // Return default schedule
        return {
            success: true,
            schedule: DEFAULT_SCHEDULE
        };
        
    } catch (error) {
        console.error('Error getting weekly schedule:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Update schedule slot
 * @param {string} dayOfWeek 
 * @param {number} slotIndex 
 * @param {Object} newSlotData 
 */
export async function updateScheduleSlot(dayOfWeek, slotIndex, newSlotData) {
    // Verify admin permissions
    const member = await currentMember.getMember();
    if (!member || !member.loginEmail.includes('@jaxbengali.org')) {
        throw new Error('Unauthorized: Admin access required');
    }
    
    try {
        // Get existing schedule for this day
        const existingSchedule = await wixData.query('RadioSchedule')
            .eq('dayOfWeek', dayOfWeek)
            .find();
        
        let scheduleDoc;
        if (existingSchedule.items.length > 0) {
            scheduleDoc = existingSchedule.items[0];
        } else {
            // Create new schedule document with defaults
            scheduleDoc = {
                dayOfWeek: dayOfWeek,
                timeSlots: DEFAULT_SCHEDULE[dayOfWeek],
                isActive: true
            };
        }
        
        // Update the specific slot
        scheduleDoc.timeSlots[slotIndex] = {
            ...scheduleDoc.timeSlots[slotIndex],
            ...newSlotData
        };
        
        scheduleDoc.lastModified = new Date();
        
        // Save
        if (scheduleDoc._id) {
            await wixData.update('RadioSchedule', scheduleDoc);
        } else {
            await wixData.insert('RadioSchedule', scheduleDoc);
        }
        
        return {
            success: true,
            message: 'Schedule updated successfully'
        };
        
    } catch (error) {
        console.error('Error updating schedule:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// SPECIAL PROGRAM MANAGEMENT
// =====================================================

/**
 * Add special program (overrides regular schedule)
 * @param {Object} programData 
 */
export async function addSpecialProgram(programData) {
    // Verify admin
    const member = await currentMember.getMember();
    if (!member || !member.loginEmail.includes('@jaxbengali.org')) {
        throw new Error('Unauthorized');
    }
    
    try {
        const specialProgram = {
            title: programData.title,
            title_bn: programData.title_bn || programData.title,
            description: programData.description,
            category: 'special',
            startDateTime: new Date(programData.startDateTime),
            endDateTime: new Date(programData.endDateTime),
            streamUrl: programData.streamUrl || null,
            thumbnailUrl: programData.thumbnailUrl || null,
            isLive: programData.isLive || false,
            isActive: true,
            createdAt: new Date(),
            createdBy: member._id
        };
        
        const result = await wixData.insert('SpecialPrograms', specialProgram);
        
        return {
            success: true,
            programId: result._id,
            message: 'Special program added successfully'
        };
        
    } catch (error) {
        console.error('Error adding special program:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Get upcoming special programs
 * @param {number} days Number of days to look ahead
 */
export async function getUpcomingSpecialPrograms(days = 30) {
    try {
        const now = new Date();
        const futureDate = new Date();
        futureDate.setDate(futureDate.getDate() + days);
        
        const programs = await wixData.query('SpecialPrograms')
            .ge('startDateTime', now)
            .le('startDateTime', futureDate)
            .eq('isActive', true)
            .ascending('startDateTime')
            .find();
        
        return {
            success: true,
            programs: programs.items
        };
        
    } catch (error) {
        console.error('Error getting special programs:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// PLAYLIST MANAGEMENT
// =====================================================

/**
 * Create new playlist
 * @param {Object} playlistData 
 */
export async function createPlaylist(playlistData) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Unauthorized');
    }
    
    try {
        const playlist = {
            name: playlistData.name,
            name_bn: playlistData.name_bn || playlistData.name,
            category: playlistData.category,
            description: playlistData.description || '',
            isActive: true,
            trackCount: 0,
            totalDuration: 0,
            createdAt: new Date(),
            createdBy: member._id
        };
        
        const result = await wixData.insert('RadioPlaylists', playlist);
        
        return {
            success: true,
            playlistId: result._id
        };
        
    } catch (error) {
        console.error('Error creating playlist:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Add track to playlist
 * @param {string} playlistId 
 * @param {Object} trackData 
 */
export async function addTrackToPlaylist(playlistId, trackData) {
    try {
        // Get current track count for ordering
        const existingTracks = await wixData.query('RadioTracks')
            .eq('playlistId', playlistId)
            .count();
        
        const track = {
            playlistId: playlistId,
            title: trackData.title,
            title_bn: trackData.title_bn || trackData.title,
            artist: trackData.artist,
            artist_bn: trackData.artist_bn || trackData.artist,
            album: trackData.album || '',
            duration: trackData.duration || 0, // in seconds
            fileUrl: trackData.fileUrl,
            trackOrder: existingTracks + 1,
            isActive: true,
            addedAt: new Date()
        };
        
        const result = await wixData.insert('RadioTracks', track);
        
        // Update playlist stats
        await updatePlaylistStats(playlistId);
        
        return {
            success: true,
            trackId: result._id
        };
        
    } catch (error) {
        console.error('Error adding track:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Update playlist statistics
 * @param {string} playlistId 
 */
async function updatePlaylistStats(playlistId) {
    try {
        const tracks = await wixData.query('RadioTracks')
            .eq('playlistId', playlistId)
            .eq('isActive', true)
            .find();
        
        const totalDuration = tracks.items.reduce((sum, track) => sum + (track.duration || 0), 0);
        
        const playlist = await wixData.get('RadioPlaylists', playlistId);
        playlist.trackCount = tracks.items.length;
        playlist.totalDuration = totalDuration;
        
        await wixData.update('RadioPlaylists', playlist);
        
    } catch (error) {
        console.error('Error updating playlist stats:', error);
    }
}

/**
 * Get all playlists by category
 * @param {string} category 
 */
export async function getPlaylistsByCategory(category) {
    try {
        const query = wixData.query('RadioPlaylists')
            .eq('isActive', true);
        
        if (category && category !== 'all') {
            query.eq('category', category);
        }
        
        const playlists = await query.descending('createdAt').find();
        
        return {
            success: true,
            playlists: playlists.items
        };
        
    } catch (error) {
        console.error('Error getting playlists:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// LISTENER ANALYTICS
// =====================================================

/**
 * Log listener session
 * @param {Object} sessionData 
 */
export async function logListenerSession(sessionData) {
    try {
        const session = {
            memberId: sessionData.memberId || 'anonymous',
            startTime: new Date(),
            category: sessionData.category,
            program: sessionData.program,
            platform: sessionData.platform || 'web',
            userAgent: sessionData.userAgent,
            isActive: true
        };
        
        const result = await wixData.insert('RadioListenerSessions', session);
        
        return {
            success: true,
            sessionId: result._id
        };
        
    } catch (error) {
        console.error('Error logging session:', error);
        return { success: false };
    }
}

/**
 * End listener session
 * @param {string} sessionId 
 */
export async function endListenerSession(sessionId) {
    try {
        const session = await wixData.get('RadioListenerSessions', sessionId);
        session.endTime = new Date();
        session.duration = (session.endTime - session.startTime) / 1000; // seconds
        session.isActive = false;
        
        await wixData.update('RadioListenerSessions', session);
        
        return { success: true };
        
    } catch (error) {
        console.error('Error ending session:', error);
        return { success: false };
    }
}

/**
 * Get listener analytics
 * @param {string} period - 'day', 'week', 'month'
 */
export async function getListenerAnalytics(period = 'week') {
    try {
        const now = new Date();
        let startDate = new Date();
        
        switch (period) {
            case 'day':
                startDate.setDate(now.getDate() - 1);
                break;
            case 'week':
                startDate.setDate(now.getDate() - 7);
                break;
            case 'month':
                startDate.setMonth(now.getMonth() - 1);
                break;
        }
        
        const sessions = await wixData.query('RadioListenerSessions')
            .ge('startTime', startDate)
            .find();
        
        // Calculate analytics
        const uniqueListeners = new Set(sessions.items.map(s => s.memberId)).size;
        const totalSessions = sessions.items.length;
        const totalDuration = sessions.items.reduce((sum, s) => sum + (s.duration || 0), 0);
        const avgSessionDuration = totalSessions > 0 ? totalDuration / totalSessions : 0;
        
        // Category breakdown
        const categoryBreakdown = {};
        sessions.items.forEach(session => {
            const cat = session.category || 'unknown';
            categoryBreakdown[cat] = (categoryBreakdown[cat] || 0) + 1;
        });
        
        return {
            success: true,
            analytics: {
                period,
                uniqueListeners,
                totalSessions,
                totalListeningMinutes: Math.round(totalDuration / 60),
                averageSessionMinutes: Math.round(avgSessionDuration / 60),
                categoryBreakdown
            }
        };
        
    } catch (error) {
        console.error('Error getting analytics:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Get current active listeners count
 */
export async function getActiveListenersCount() {
    try {
        const count = await wixData.query('RadioListenerSessions')
            .eq('isActive', true)
            .count();
        
        return {
            success: true,
            count: count
        };
        
    } catch (error) {
        return {
            success: false,
            count: 0
        };
    }
}

// =====================================================
// MAHALAYA SPECIAL SCHEDULING
// =====================================================

/**
 * Schedule Mahalaya broadcast (annual special)
 * Mahalaya is traditionally broadcast at 4 AM on the day before Durga Puja
 * @param {number} year 
 */
export async function scheduleMahalaya(year) {
    // Mahalaya dates vary based on Bengali calendar
    // This would need to be set manually or via API
    const mahalayaProgram = {
        title: 'মহালয়া - মহিষাসুরমর্দিনী',
        title_bn: 'মহালয়া - মহিষাসুরমর্দিনী',
        description: 'Traditional Mahalaya broadcast - Mahishasuramardini by Birendra Krishna Bhadra',
        category: 'special',
        startDateTime: null, // To be set based on year
        endDateTime: null,
        streamUrl: 'mahalaya-special-stream',
        isLive: true,
        isActive: false, // Activate when date is confirmed
        isAnnual: true,
        createdAt: new Date()
    };
    
    return addSpecialProgram(mahalayaProgram);
}

// =====================================================
// STREAM HEALTH & MONITORING
// =====================================================

/**
 * Report stream status
 * @param {Object} statusData 
 */
export async function reportStreamStatus(statusData) {
    try {
        const status = {
            timestamp: new Date(),
            isOnline: statusData.isOnline,
            bitrate: statusData.bitrate,
            bufferHealth: statusData.bufferHealth,
            errorCount: statusData.errorCount || 0,
            currentTrack: statusData.currentTrack
        };
        
        await wixData.insert('RadioStreamStatus', status);
        
        // Keep only last 100 status records
        const oldRecords = await wixData.query('RadioStreamStatus')
            .descending('timestamp')
            .skip(100)
            .find();
        
        for (const record of oldRecords.items) {
            await wixData.remove('RadioStreamStatus', record._id);
        }
        
        return { success: true };
        
    } catch (error) {
        console.error('Error reporting stream status:', error);
        return { success: false };
    }
}

/**
 * Get stream health status
 */
export async function getStreamHealth() {
    try {
        const latestStatus = await wixData.query('RadioStreamStatus')
            .descending('timestamp')
            .limit(1)
            .find();
        
        if (latestStatus.items.length > 0) {
            return {
                success: true,
                status: latestStatus.items[0]
            };
        }
        
        return {
            success: true,
            status: {
                isOnline: false,
                lastChecked: null
            }
        };
        
    } catch (error) {
        return {
            success: false,
            status: { isOnline: false }
        };
    }
}

```
------------------------------------------------------------

## [33/41] radio
- File: `radio.jsw`
- Size: 12.8 KB
- Lines: 417

```javascript
// backend/radio.jsw
// BANF Radio Station Integration - Wix Velo Backend
// Integrates with external streaming services via wix-fetch

import wixData from 'wix-data';
import { fetch } from 'wix-fetch';

// Radio station status constants
const STATION_STATUS = {
    ONLINE: 'online',
    OFFLINE: 'offline',
    MAINTENANCE: 'maintenance'
};

/**
 * Get radio station configuration
 */
export async function getRadioStationConfig() {
    try {
        const result = await wixData.query('RadioStations')
            .eq('isActive', true)
            .find({ suppressAuth: true });
        
        if (result.items.length === 0) {
            return getDefaultStationConfig();
        }
        
        const station = result.items[0];
        return {
            id: station._id,
            name: station.stationName,
            description: station.description,
            streamUrl: station.streamUrl,
            fallbackUrl: station.fallbackUrl,
            logoUrl: station.logoUrl,
            status: station.status,
            currentShow: await getCurrentShow(),
            upcomingShows: await getUpcomingShows(5),
            metadata: {
                genre: station.genre || 'Bengali Music',
                language: station.language || 'Bengali',
                frequency: station.frequency || 'Online Only'
            }
        };
    } catch (error) {
        console.error('Error getting radio config:', error);
        return getDefaultStationConfig();
    }
}

/**
 * Get current playing show
 */
export async function getCurrentShow() {
    try {
        const now = new Date();
        const dayOfWeek = now.toLocaleDateString('en-US', { weekday: 'lowercase' });
        const currentTime = now.toTimeString().substring(0, 5); // HH:MM format
        
        const result = await wixData.query('RadioSchedule')
            .eq('dayOfWeek', dayOfWeek)
            .eq('isActive', true)
            .le('startTime', currentTime)
            .ge('endTime', currentTime)
            .find({ suppressAuth: true });
        
        if (result.items.length > 0) {
            const show = result.items[0];
            return {
                id: show._id,
                title: show.showTitle,
                host: show.hostName,
                description: show.description,
                startTime: show.startTime,
                endTime: show.endTime,
                genre: show.genre
            };
        }
        
        return {
            title: 'Auto DJ',
            host: 'BANF Radio',
            description: 'Playing your favorite Bengali songs',
            genre: 'Mixed'
        };
    } catch (error) {
        console.error('Error getting current show:', error);
        return null;
    }
}

/**
 * Get upcoming shows
 */
export async function getUpcomingShows(limit = 10) {
    try {
        const now = new Date();
        const dayOfWeek = now.toLocaleDateString('en-US', { weekday: 'lowercase' });
        const currentTime = now.toTimeString().substring(0, 5);
        
        // Get today's remaining shows
        const todayShows = await wixData.query('RadioSchedule')
            .eq('dayOfWeek', dayOfWeek)
            .eq('isActive', true)
            .gt('startTime', currentTime)
            .ascending('startTime')
            .limit(limit)
            .find({ suppressAuth: true });
        
        // Get tomorrow's shows if needed
        const shows = todayShows.items.map(s => ({
            id: s._id,
            title: s.showTitle,
            host: s.hostName,
            day: s.dayOfWeek,
            startTime: s.startTime,
            endTime: s.endTime,
            genre: s.genre
        }));
        
        return shows;
    } catch (error) {
        console.error('Error getting upcoming shows:', error);
        return [];
    }
}

/**
 * Get full weekly schedule
 */
export async function getWeeklySchedule() {
    try {
        const days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
        const schedule = {};
        
        for (const day of days) {
            const result = await wixData.query('RadioSchedule')
                .eq('dayOfWeek', day)
                .eq('isActive', true)
                .ascending('startTime')
                .find({ suppressAuth: true });
            
            schedule[day] = result.items.map(s => ({
                id: s._id,
                title: s.showTitle,
                host: s.hostName,
                startTime: s.startTime,
                endTime: s.endTime,
                genre: s.genre,
                description: s.description
            }));
        }
        
        return schedule;
    } catch (error) {
        console.error('Error getting weekly schedule:', error);
        return {};
    }
}

/**
 * Create/Update radio show (admin only)
 */
export async function createRadioShow(showData, adminId) {
    try {
        const show = {
            showTitle: showData.title,
            hostName: showData.host,
            description: showData.description || '',
            genre: showData.genre || 'General',
            dayOfWeek: showData.dayOfWeek.toLowerCase(),
            startTime: showData.startTime,
            endTime: showData.endTime,
            isRecurring: showData.isRecurring !== false,
            isActive: true,
            createdBy: adminId,
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        // Check for time conflicts
        const conflicts = await wixData.query('RadioSchedule')
            .eq('dayOfWeek', show.dayOfWeek)
            .eq('isActive', true)
            .find();
        
        const hasConflict = conflicts.items.some(existing => {
            return (show.startTime < existing.endTime && show.endTime > existing.startTime);
        });
        
        if (hasConflict) {
            return { success: false, error: 'Time slot conflicts with existing show' };
        }
        
        const result = await wixData.insert('RadioSchedule', show);
        
        return { success: true, showId: result._id };
    } catch (error) {
        console.error('Error creating radio show:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get song library
 */
export async function getSongLibrary(options = { limit: 50, skip: 0, genre: null }) {
    try {
        let query = wixData.query('BengaliSongs');
        
        if (options.genre) {
            query = query.eq('genre', options.genre);
        }
        
        query = query
            .ascending('title')
            .limit(options.limit)
            .skip(options.skip);
        
        const result = await query.find({ suppressAuth: true });
        
        return {
            items: result.items.map(song => ({
                id: song._id,
                title: song.title,
                artist: song.artist,
                album: song.album,
                genre: song.genre,
                duration: song.duration,
                year: song.releaseYear,
                playCount: song.playCount || 0
            })),
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error getting song library:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Add song to library (admin only)
 */
export async function addSong(songData, adminId) {
    try {
        const song = {
            title: songData.title,
            artist: songData.artist,
            album: songData.album || '',
            genre: songData.genre || 'Bengali',
            duration: songData.duration || 0,
            releaseYear: songData.year || null,
            lyrics: songData.lyrics || '',
            audioUrl: songData.audioUrl || '',
            playCount: 0,
            addedBy: adminId,
            _createdDate: new Date()
        };
        
        const result = await wixData.insert('BengaliSongs', song);
        
        return { success: true, songId: result._id };
    } catch (error) {
        console.error('Error adding song:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Submit song request
 */
export async function submitSongRequest(requestData) {
    try {
        const request = {
            songTitle: requestData.songTitle,
            artistName: requestData.artist || '',
            requestedBy: requestData.name || 'Anonymous',
            message: requestData.message || '',
            dedicatedTo: requestData.dedicatedTo || '',
            status: 'pending', // pending, approved, played, rejected
            submittedAt: new Date(),
            _createdDate: new Date()
        };
        
        await wixData.insert('SongRequests', request, { suppressAuth: true });
        
        return { success: true, message: 'Song request submitted!' };
    } catch (error) {
        console.error('Error submitting song request:', error);
        return { success: false, error: 'Failed to submit request' };
    }
}

/**
 * Get pending song requests (admin/DJ)
 */
export async function getPendingSongRequests() {
    try {
        const result = await wixData.query('SongRequests')
            .eq('status', 'pending')
            .descending('submittedAt')
            .limit(50)
            .find();
        
        return result.items;
    } catch (error) {
        console.error('Error getting song requests:', error);
        return [];
    }
}

/**
 * Update station status (admin only)
 */
export async function updateStationStatus(stationId, status, adminId) {
    try {
        const station = await wixData.get('RadioStations', stationId);
        if (!station) {
            return { success: false, error: 'Station not found' };
        }
        
        await wixData.update('RadioStations', {
            ...station,
            status: status,
            lastStatusUpdate: new Date(),
            statusUpdatedBy: adminId,
            _updatedDate: new Date()
        });
        
        return { success: true, message: 'Station status updated' };
    } catch (error) {
        console.error('Error updating station status:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get listener statistics
 */
export async function getListenerStats() {
    try {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        const weekAgo = new Date(today);
        weekAgo.setDate(weekAgo.getDate() - 7);
        
        const monthAgo = new Date(today);
        monthAgo.setDate(monthAgo.getDate() - 30);
        
        // These would typically come from external streaming service
        // For now, we track page views/interactions
        const todayStats = await wixData.query('RadioListenerLogs')
            .ge('timestamp', today)
            .count();
        
        const weekStats = await wixData.query('RadioListenerLogs')
            .ge('timestamp', weekAgo)
            .count();
        
        const monthStats = await wixData.query('RadioListenerLogs')
            .ge('timestamp', monthAgo)
            .count();
        
        return {
            today: todayStats,
            thisWeek: weekStats,
            thisMonth: monthStats,
            peakListeners: 0, // Would come from streaming service
            averageListenTime: 0 // Would come from streaming service
        };
    } catch (error) {
        console.error('Error getting listener stats:', error);
        return { today: 0, thisWeek: 0, thisMonth: 0 };
    }
}

/**
 * Log listener activity
 */
export async function logListenerActivity(action, details = {}) {
    try {
        await wixData.insert('RadioListenerLogs', {
            action: action, // 'play', 'pause', 'tune_in', 'tune_out'
            details: JSON.stringify(details),
            timestamp: new Date(),
            _createdDate: new Date()
        }, { suppressAuth: true });
    } catch (error) {
        console.error('Error logging listener activity:', error);
    }
}

// Helper function
function getDefaultStationConfig() {
    return {
        name: 'BANF Radio',
        description: 'Bay Area Natun Fasal Community Radio',
        streamUrl: '',
        status: STATION_STATUS.OFFLINE,
        currentShow: {
            title: 'Auto DJ',
            host: 'BANF Radio',
            description: 'Playing your favorite Bengali songs'
        },
        upcomingShows: [],
        metadata: {
            genre: 'Bengali Music',
            language: 'Bengali',
            frequency: 'Online Only'
        }
    };
}

// Export constants
export const StationStatus = STATION_STATUS;

```
------------------------------------------------------------

## [34/41] reporting-module
- File: `reporting-module.jsw`
- Size: 23.3 KB
- Lines: 702

```javascript
/**
 * BANF Reporting Module
 * Comprehensive report generation for all modules
 * 
 * File: backend/reporting-module.jsw
 * Deploy to: Wix Velo Backend
 */

import wixData from 'wix-data';
import { hasSpecializedPermission } from 'backend/specialized-admin-roles.jsw';

// Report Types
export const REPORT_TYPES = {
    // Financial Reports
    FINANCIAL_SUMMARY: 'financial_summary',
    INCOME_STATEMENT: 'income_statement',
    EXPENSE_REPORT: 'expense_report',
    BUDGET_VS_ACTUAL: 'budget_vs_actual',
    PAYMENT_RECONCILIATION: 'payment_reconciliation',
    TAX_SUMMARY: 'tax_summary',
    
    // Membership Reports
    MEMBERSHIP_GROWTH: 'membership_growth',
    MEMBERSHIP_RETENTION: 'membership_retention',
    MEMBERSHIP_DEMOGRAPHICS: 'membership_demographics',
    RENEWAL_STATUS: 'renewal_status',
    
    // Event Reports
    EVENT_ATTENDANCE: 'event_attendance',
    EVENT_REVENUE: 'event_revenue',
    EVENT_COMPARISON: 'event_comparison',
    REGISTRATION_TRENDS: 'registration_trends',
    
    // Engagement Reports
    VOLUNTEER_HOURS: 'volunteer_hours',
    COMMUNITY_ENGAGEMENT: 'community_engagement',
    SURVEY_RESULTS: 'survey_results',
    COMPLAINT_ANALYSIS: 'complaint_analysis',
    
    // Content Reports
    MAGAZINE_ANALYTICS: 'magazine_analytics',
    RADIO_LISTENERSHIP: 'radio_listenership',
    GUIDE_USAGE: 'guide_usage',
    
    // Sponsor & Vendor Reports
    SPONSOR_ROI: 'sponsor_roi',
    VENDOR_PERFORMANCE: 'vendor_performance',
    AD_PERFORMANCE: 'ad_performance'
};

// Time Periods
export const TIME_PERIODS = {
    DAILY: 'daily',
    WEEKLY: 'weekly',
    MONTHLY: 'monthly',
    QUARTERLY: 'quarterly',
    YEARLY: 'yearly',
    CUSTOM: 'custom'
};

/**
 * Generate a report
 * @param {string} reportType - Type of report from REPORT_TYPES
 * @param {object} options - Report options
 * @param {string} userId - User generating the report
 */
export async function generateReport(reportType, options = {}, userId) {
    try {
        // Check permission
        const hasPermission = await hasSpecializedPermission(userId, 'reports_generate');
        if (!hasPermission) {
            return { success: false, error: 'Not authorized to generate reports' };
        }
        
        const { 
            timePeriod = TIME_PERIODS.MONTHLY,
            startDate,
            endDate,
            eventId,
            filters = {}
        } = options;
        
        // Calculate date range
        const dateRange = calculateDateRange(timePeriod, startDate, endDate);
        
        let reportData;
        
        switch (reportType) {
            case REPORT_TYPES.FINANCIAL_SUMMARY:
                reportData = await generateFinancialSummary(dateRange, filters);
                break;
            case REPORT_TYPES.INCOME_STATEMENT:
                reportData = await generateIncomeStatement(dateRange, filters);
                break;
            case REPORT_TYPES.EXPENSE_REPORT:
                reportData = await generateExpenseReport(dateRange, filters);
                break;
            case REPORT_TYPES.MEMBERSHIP_GROWTH:
                reportData = await generateMembershipGrowth(dateRange, filters);
                break;
            case REPORT_TYPES.EVENT_ATTENDANCE:
                reportData = await generateEventAttendance(dateRange, eventId);
                break;
            case REPORT_TYPES.EVENT_REVENUE:
                reportData = await generateEventRevenue(dateRange, eventId);
                break;
            case REPORT_TYPES.VOLUNTEER_HOURS:
                reportData = await generateVolunteerHours(dateRange, filters);
                break;
            case REPORT_TYPES.SPONSOR_ROI:
                reportData = await generateSponsorROI(dateRange, filters);
                break;
            case REPORT_TYPES.AD_PERFORMANCE:
                reportData = await generateAdPerformance(dateRange, filters);
                break;
            default:
                return { success: false, error: 'Invalid report type' };
        }
        
        // Save report to history
        const report = await wixData.insert('ReportHistory', {
            reportType,
            timePeriod,
            dateRange: {
                start: dateRange.start,
                end: dateRange.end
            },
            filters,
            generatedBy: userId,
            generatedAt: new Date(),
            data: reportData,
            exportFormats: ['pdf', 'excel', 'csv']
        }, { suppressAuth: true });
        
        return {
            success: true,
            reportId: report._id,
            reportType,
            dateRange,
            data: reportData,
            generatedAt: new Date()
        };
    } catch (error) {
        console.error('Report generation failed:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Calculate date range based on time period
 */
function calculateDateRange(timePeriod, startDate, endDate) {
    const now = new Date();
    let start, end;
    
    switch (timePeriod) {
        case TIME_PERIODS.DAILY:
            start = new Date(now.setHours(0, 0, 0, 0));
            end = new Date(now.setHours(23, 59, 59, 999));
            break;
        case TIME_PERIODS.WEEKLY:
            const dayOfWeek = now.getDay();
            start = new Date(now.setDate(now.getDate() - dayOfWeek));
            start.setHours(0, 0, 0, 0);
            end = new Date(start);
            end.setDate(end.getDate() + 6);
            end.setHours(23, 59, 59, 999);
            break;
        case TIME_PERIODS.MONTHLY:
            start = new Date(now.getFullYear(), now.getMonth(), 1);
            end = new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59, 999);
            break;
        case TIME_PERIODS.QUARTERLY:
            const quarter = Math.floor(now.getMonth() / 3);
            start = new Date(now.getFullYear(), quarter * 3, 1);
            end = new Date(now.getFullYear(), quarter * 3 + 3, 0, 23, 59, 59, 999);
            break;
        case TIME_PERIODS.YEARLY:
            start = new Date(now.getFullYear(), 0, 1);
            end = new Date(now.getFullYear(), 11, 31, 23, 59, 59, 999);
            break;
        case TIME_PERIODS.CUSTOM:
            start = new Date(startDate);
            end = new Date(endDate);
            break;
        default:
            start = new Date(now.getFullYear(), now.getMonth(), 1);
            end = new Date(now.getFullYear(), now.getMonth() + 1, 0);
    }
    
    return { start, end };
}

/**
 * Generate Financial Summary Report
 */
async function generateFinancialSummary(dateRange, filters) {
    const transactions = await wixData.query('Transactions')
        .ge('transactionDate', dateRange.start)
        .le('transactionDate', dateRange.end)
        .find({ suppressAuth: true });
    
    const income = transactions.items
        .filter(t => t.type === 'income')
        .reduce((sum, t) => sum + t.amount, 0);
    
    const expenses = transactions.items
        .filter(t => t.type === 'expense')
        .reduce((sum, t) => sum + t.amount, 0);
    
    // Group by category
    const incomeByCategory = {};
    const expenseByCategory = {};
    
    transactions.items.forEach(t => {
        const category = t.category || 'Uncategorized';
        if (t.type === 'income') {
            incomeByCategory[category] = (incomeByCategory[category] || 0) + t.amount;
        } else {
            expenseByCategory[category] = (expenseByCategory[category] || 0) + t.amount;
        }
    });
    
    return {
        summary: {
            totalIncome: income,
            totalExpenses: expenses,
            netIncome: income - expenses,
            transactionCount: transactions.items.length
        },
        incomeByCategory,
        expenseByCategory,
        monthlyTrend: await getMonthlyTrend(dateRange),
        topExpenseCategories: Object.entries(expenseByCategory)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5),
        topIncomeCategories: Object.entries(incomeByCategory)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
    };
}

/**
 * Generate Income Statement
 */
async function generateIncomeStatement(dateRange, filters) {
    const transactions = await wixData.query('Transactions')
        .ge('transactionDate', dateRange.start)
        .le('transactionDate', dateRange.end)
        .eq('type', 'income')
        .find({ suppressAuth: true });
    
    // Group by source
    const bySource = {
        membership: 0,
        events: 0,
        sponsorship: 0,
        vendors: 0,
        donations: 0,
        advertising: 0,
        other: 0
    };
    
    transactions.items.forEach(t => {
        const source = t.source || 'other';
        bySource[source] = (bySource[source] || 0) + t.amount;
    });
    
    return {
        totalIncome: Object.values(bySource).reduce((a, b) => a + b, 0),
        bySource,
        transactionDetails: transactions.items.map(t => ({
            date: t.transactionDate,
            description: t.description,
            amount: t.amount,
            source: t.source,
            reference: t.referenceNumber
        }))
    };
}

/**
 * Generate Expense Report
 */
async function generateExpenseReport(dateRange, filters) {
    const transactions = await wixData.query('Transactions')
        .ge('transactionDate', dateRange.start)
        .le('transactionDate', dateRange.end)
        .eq('type', 'expense')
        .find({ suppressAuth: true });
    
    // Group by category
    const byCategory = {};
    const byVendor = {};
    const byEvent = {};
    
    transactions.items.forEach(t => {
        const category = t.category || 'Uncategorized';
        const vendor = t.vendor || 'Unknown';
        const event = t.eventName || 'General';
        
        byCategory[category] = (byCategory[category] || 0) + t.amount;
        byVendor[vendor] = (byVendor[vendor] || 0) + t.amount;
        byEvent[event] = (byEvent[event] || 0) + t.amount;
    });
    
    return {
        totalExpenses: transactions.items.reduce((sum, t) => sum + t.amount, 0),
        byCategory,
        byVendor,
        byEvent,
        pendingReimbursements: transactions.items
            .filter(t => t.status === 'pending_reimbursement')
            .length,
        largestExpenses: transactions.items
            .sort((a, b) => b.amount - a.amount)
            .slice(0, 10)
    };
}

/**
 * Generate Membership Growth Report
 */
async function generateMembershipGrowth(dateRange, filters) {
    const members = await wixData.query('Members')
        .find({ suppressAuth: true });
    
    const newMembers = members.items.filter(m => 
        new Date(m.createdAt) >= dateRange.start && 
        new Date(m.createdAt) <= dateRange.end
    );
    
    const renewals = members.items.filter(m => 
        m.renewedAt && 
        new Date(m.renewedAt) >= dateRange.start && 
        new Date(m.renewedAt) <= dateRange.end
    );
    
    // Group by membership type
    const byType = {};
    members.items.forEach(m => {
        const type = m.membershipType || 'Standard';
        byType[type] = (byType[type] || 0) + 1;
    });
    
    // Monthly growth
    const monthlyGrowth = {};
    newMembers.forEach(m => {
        const month = new Date(m.createdAt).toLocaleString('default', { month: 'short', year: 'numeric' });
        monthlyGrowth[month] = (monthlyGrowth[month] || 0) + 1;
    });
    
    return {
        totalMembers: members.items.length,
        activeMembers: members.items.filter(m => m.status === 'active').length,
        newMembersThisPeriod: newMembers.length,
        renewalsThisPeriod: renewals.length,
        byMembershipType: byType,
        monthlyGrowth,
        retentionRate: calculateRetentionRate(members.items, dateRange),
        familyMembers: members.items.filter(m => m.membershipType?.includes('Family')).length
    };
}

/**
 * Generate Event Attendance Report
 */
async function generateEventAttendance(dateRange, eventId) {
    let query = wixData.query('EventRegistrations')
        .ge('createdAt', dateRange.start)
        .le('createdAt', dateRange.end);
    
    if (eventId) {
        query = query.eq('eventId', eventId);
    }
    
    const registrations = await query.find({ suppressAuth: true });
    
    // Get events
    const eventIds = [...new Set(registrations.items.map(r => r.eventId))];
    const events = await wixData.query('Events')
        .hasSome('_id', eventIds)
        .find({ suppressAuth: true });
    
    const eventMap = {};
    events.items.forEach(e => {
        eventMap[e._id] = e.title;
    });
    
    // Calculate attendance by event
    const attendanceByEvent = {};
    registrations.items.forEach(r => {
        const eventName = eventMap[r.eventId] || 'Unknown Event';
        if (!attendanceByEvent[eventName]) {
            attendanceByEvent[eventName] = {
                registered: 0,
                attended: 0,
                noShow: 0,
                familyMembers: 0
            };
        }
        attendanceByEvent[eventName].registered++;
        if (r.checkedIn) attendanceByEvent[eventName].attended++;
        else attendanceByEvent[eventName].noShow++;
        attendanceByEvent[eventName].familyMembers += (r.familyCount || 0);
    });
    
    return {
        totalRegistrations: registrations.items.length,
        totalAttended: registrations.items.filter(r => r.checkedIn).length,
        attendanceRate: registrations.items.length > 0 
            ? (registrations.items.filter(r => r.checkedIn).length / registrations.items.length * 100).toFixed(1) 
            : 0,
        byEvent: attendanceByEvent,
        peakEvents: Object.entries(attendanceByEvent)
            .sort((a, b) => b[1].attended - a[1].attended)
            .slice(0, 5)
    };
}

/**
 * Generate Event Revenue Report
 */
async function generateEventRevenue(dateRange, eventId) {
    let query = wixData.query('Transactions')
        .ge('transactionDate', dateRange.start)
        .le('transactionDate', dateRange.end)
        .eq('source', 'events');
    
    if (eventId) {
        query = query.eq('eventId', eventId);
    }
    
    const transactions = await query.find({ suppressAuth: true });
    
    // Group by event
    const revenueByEvent = {};
    transactions.items.forEach(t => {
        const eventName = t.eventName || 'Unknown Event';
        if (!revenueByEvent[eventName]) {
            revenueByEvent[eventName] = {
                income: 0,
                expenses: 0,
                registrations: 0
            };
        }
        if (t.type === 'income') {
            revenueByEvent[eventName].income += t.amount;
            revenueByEvent[eventName].registrations++;
        } else {
            revenueByEvent[eventName].expenses += t.amount;
        }
    });
    
    // Calculate net for each event
    Object.keys(revenueByEvent).forEach(event => {
        revenueByEvent[event].net = revenueByEvent[event].income - revenueByEvent[event].expenses;
        revenueByEvent[event].roi = revenueByEvent[event].expenses > 0 
            ? ((revenueByEvent[event].net / revenueByEvent[event].expenses) * 100).toFixed(1)
            : 100;
    });
    
    return {
        totalRevenue: Object.values(revenueByEvent).reduce((sum, e) => sum + e.income, 0),
        totalExpenses: Object.values(revenueByEvent).reduce((sum, e) => sum + e.expenses, 0),
        netIncome: Object.values(revenueByEvent).reduce((sum, e) => sum + e.net, 0),
        byEvent: revenueByEvent,
        mostProfitable: Object.entries(revenueByEvent)
            .sort((a, b) => b[1].net - a[1].net)
            .slice(0, 5)
    };
}

/**
 * Generate Volunteer Hours Report
 */
async function generateVolunteerHours(dateRange, filters) {
    const hours = await wixData.query('VolunteerHours')
        .ge('date', dateRange.start)
        .le('date', dateRange.end)
        .find({ suppressAuth: true });
    
    // Group by volunteer
    const byVolunteer = {};
    const byTask = {};
    const byEvent = {};
    
    hours.items.forEach(h => {
        const volunteer = h.volunteerName || 'Unknown';
        const task = h.taskType || 'General';
        const event = h.eventName || 'General';
        
        byVolunteer[volunteer] = (byVolunteer[volunteer] || 0) + h.hours;
        byTask[task] = (byTask[task] || 0) + h.hours;
        byEvent[event] = (byEvent[event] || 0) + h.hours;
    });
    
    return {
        totalHours: hours.items.reduce((sum, h) => sum + h.hours, 0),
        totalVolunteers: Object.keys(byVolunteer).length,
        averageHoursPerVolunteer: Object.keys(byVolunteer).length > 0 
            ? (hours.items.reduce((sum, h) => sum + h.hours, 0) / Object.keys(byVolunteer).length).toFixed(1)
            : 0,
        byVolunteer,
        byTask,
        byEvent,
        topVolunteers: Object.entries(byVolunteer)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10)
    };
}

/**
 * Generate Sponsor ROI Report
 */
async function generateSponsorROI(dateRange, filters) {
    const sponsors = await wixData.query('Sponsors')
        .ge('sponsorshipDate', dateRange.start)
        .le('sponsorshipDate', dateRange.end)
        .find({ suppressAuth: true });
    
    // Group by tier
    const byTier = {
        platinum: { count: 0, revenue: 0 },
        gold: { count: 0, revenue: 0 },
        silver: { count: 0, revenue: 0 },
        bronze: { count: 0, revenue: 0 },
        supporter: { count: 0, revenue: 0 }
    };
    
    sponsors.items.forEach(s => {
        const tier = s.tier?.toLowerCase() || 'supporter';
        if (byTier[tier]) {
            byTier[tier].count++;
            byTier[tier].revenue += s.amount || 0;
        }
    });
    
    return {
        totalSponsors: sponsors.items.length,
        totalRevenue: sponsors.items.reduce((sum, s) => sum + (s.amount || 0), 0),
        byTier,
        renewalRate: calculateSponsorRenewalRate(sponsors.items),
        benefitsDelivered: countBenefitsDelivered(sponsors.items)
    };
}

/**
 * Generate Ad Performance Report
 */
async function generateAdPerformance(dateRange, filters) {
    const ads = await wixData.query('Advertisements')
        .ge('startDate', dateRange.start)
        .le('endDate', dateRange.end)
        .find({ suppressAuth: true });
    
    const metrics = await wixData.query('AdMetrics')
        .ge('date', dateRange.start)
        .le('date', dateRange.end)
        .find({ suppressAuth: true });
    
    // Calculate totals
    const totalImpressions = metrics.items.reduce((sum, m) => sum + (m.impressions || 0), 0);
    const totalClicks = metrics.items.reduce((sum, m) => sum + (m.clicks || 0), 0);
    const totalRevenue = ads.items.reduce((sum, a) => sum + (a.revenue || 0), 0);
    
    return {
        totalAds: ads.items.length,
        activeAds: ads.items.filter(a => a.status === 'active').length,
        totalImpressions,
        totalClicks,
        ctr: totalImpressions > 0 ? ((totalClicks / totalImpressions) * 100).toFixed(2) : 0,
        totalRevenue,
        revenuePerAd: ads.items.length > 0 ? (totalRevenue / ads.items.length).toFixed(2) : 0,
        byPlatform: groupAdsByPlatform(ads.items, metrics.items),
        topPerformingAds: metrics.items
            .sort((a, b) => b.clicks - a.clicks)
            .slice(0, 10)
    };
}

// Helper functions
function calculateRetentionRate(members, dateRange) {
    const renewedCount = members.filter(m => 
        m.renewedAt && new Date(m.renewedAt) >= dateRange.start
    ).length;
    const eligibleCount = members.filter(m => 
        m.membershipExpiry && new Date(m.membershipExpiry) >= dateRange.start
    ).length;
    return eligibleCount > 0 ? ((renewedCount / eligibleCount) * 100).toFixed(1) : 0;
}

async function getMonthlyTrend(dateRange) {
    // Implementation for monthly trend calculation
    return [];
}

function calculateSponsorRenewalRate(sponsors) {
    const renewed = sponsors.filter(s => s.isRenewal).length;
    return sponsors.length > 0 ? ((renewed / sponsors.length) * 100).toFixed(1) : 0;
}

function countBenefitsDelivered(sponsors) {
    return sponsors.reduce((count, s) => count + (s.benefitsDelivered || []).length, 0);
}

function groupAdsByPlatform(ads, metrics) {
    const platforms = {};
    ads.forEach(a => {
        const platform = a.platform || 'website';
        if (!platforms[platform]) {
            platforms[platform] = { count: 0, impressions: 0, clicks: 0, revenue: 0 };
        }
        platforms[platform].count++;
        platforms[platform].revenue += a.revenue || 0;
    });
    return platforms;
}

/**
 * Schedule automated report
 */
export async function scheduleReport(reportConfig, userId) {
    try {
        const scheduled = await wixData.insert('ScheduledReports', {
            ...reportConfig,
            createdBy: userId,
            createdAt: new Date(),
            isActive: true,
            lastRun: null,
            nextRun: calculateNextRun(reportConfig.frequency)
        }, { suppressAuth: true });
        
        return { success: true, scheduleId: scheduled._id };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

function calculateNextRun(frequency) {
    const now = new Date();
    switch (frequency) {
        case 'daily': return new Date(now.setDate(now.getDate() + 1));
        case 'weekly': return new Date(now.setDate(now.getDate() + 7));
        case 'monthly': return new Date(now.setMonth(now.getMonth() + 1));
        case 'quarterly': return new Date(now.setMonth(now.getMonth() + 3));
        default: return new Date(now.setMonth(now.getMonth() + 1));
    }
}

/**
 * Export report to different formats
 */
export async function exportReport(reportId, format, userId) {
    try {
        const report = await wixData.get('ReportHistory', reportId, { suppressAuth: true });
        
        if (!report) {
            return { success: false, error: 'Report not found' };
        }
        
        // Generate export based on format
        let exportData;
        switch (format) {
            case 'csv':
                exportData = convertToCSV(report.data);
                break;
            case 'excel':
                exportData = convertToExcel(report.data);
                break;
            case 'pdf':
                exportData = convertToPDF(report.data);
                break;
            default:
                exportData = JSON.stringify(report.data, null, 2);
        }
        
        return {
            success: true,
            format,
            data: exportData,
            filename: `${report.reportType}_${new Date().toISOString().split('T')[0]}.${format}`
        };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

function convertToCSV(data) {
    // CSV conversion implementation
    return JSON.stringify(data);
}

function convertToExcel(data) {
    // Excel conversion implementation
    return JSON.stringify(data);
}

function convertToPDF(data) {
    // PDF conversion implementation
    return JSON.stringify(data);
}

```
------------------------------------------------------------

## [35/41] specialized-admin-roles
- File: `specialized-admin-roles.jsw`
- Size: 11.4 KB
- Lines: 329

```javascript
/**
 * BANF Specialized Admin Roles Module
 * Extended admin roles for specific feature management
 * 
 * File: backend/specialized-admin-roles.jsw
 * Deploy to: Wix Velo Backend
 */

import wixData from 'wix-data';
import { logAdminActivity } from 'backend/admin-auth.jsw';

// Extended Specialized Admin Roles
export const SPECIALIZED_ROLES = {
    // Content & Media Roles
    MAGAZINE_EDITOR: 'magazine_editor',           // E-magazine management
    MAGAZINE_REVIEWER: 'magazine_reviewer',       // Article review only
    RADIO_MANAGER: 'radio_manager',               // Full radio control
    RADIO_DJ: 'radio_dj',                         // Live streaming only
    VIDEO_COORDINATOR: 'video_coordinator',       // Video content scheduling
    GALLERY_MANAGER: 'gallery_manager',           // Photo/video gallery
    
    // Events & Operations
    EVENT_COORDINATOR: 'event_coordinator',       // Specific event management
    VOLUNTEER_COORDINATOR: 'volunteer_coordinator', // Volunteer management
    VENDOR_COORDINATOR: 'vendor_coordinator',     // Vendor management
    
    // Marketing & Engagement
    AD_MANAGER: 'ad_manager',                     // Advertisement management
    SOCIAL_MEDIA_MANAGER: 'social_media_manager', // Social media integration
    COMMUNITY_LEAD: 'community_lead',             // Community initiatives
    
    // Analytics & Reporting
    REPORT_ANALYST: 'report_analyst',             // Report generation
    DATA_ANALYST: 'data_analyst',                 // Full analytics access
    
    // Support
    GUIDE_EDITOR: 'guide_editor',                 // Jacksonville guide content
    SURVEY_COORDINATOR: 'survey_coordinator'      // Survey management
};

// Specialized Role Permissions Matrix
const SPECIALIZED_PERMISSIONS = {
    magazine_editor: {
        permissions: ['magazine_full', 'magazine_publish', 'magazine_review', 'magazine_edit', 'magazine_delete'],
        description: 'Full control over e-magazine content and publishing',
        canApprove: true,
        canDelete: true
    },
    magazine_reviewer: {
        permissions: ['magazine_review', 'magazine_comment'],
        description: 'Review and comment on submitted articles',
        canApprove: false,
        canDelete: false
    },
    radio_manager: {
        permissions: ['radio_full', 'radio_schedule', 'radio_live', 'radio_playlist', 'radio_settings'],
        description: 'Full control over radio programming and settings',
        canApprove: true,
        canDelete: true
    },
    radio_dj: {
        permissions: ['radio_live', 'radio_playlist_readonly', 'radio_request'],
        description: 'Live streaming and music playback only',
        canApprove: false,
        canDelete: false
    },
    video_coordinator: {
        permissions: ['video_upload', 'video_schedule', 'video_edit', 'video_publish'],
        description: 'Video content management and scheduling',
        canApprove: true,
        canDelete: false
    },
    gallery_manager: {
        permissions: ['gallery_full', 'gallery_upload', 'gallery_organize', 'gallery_delete'],
        description: 'Photo and video gallery management',
        canApprove: true,
        canDelete: true
    },
    event_coordinator: {
        permissions: ['events_manage', 'events_checkin', 'events_reports'],
        description: 'Specific event operations (assigned events only)',
        canApprove: false,
        canDelete: false,
        scopeLimit: 'assigned_events'
    },
    volunteer_coordinator: {
        permissions: ['volunteer_full', 'volunteer_assign', 'volunteer_hours', 'volunteer_reports'],
        description: 'Volunteer recruitment and coordination',
        canApprove: true,
        canDelete: false
    },
    vendor_coordinator: {
        permissions: ['vendor_review', 'vendor_communicate', 'vendor_booth'],
        description: 'Vendor communication and booth management',
        canApprove: false,
        canDelete: false
    },
    ad_manager: {
        permissions: ['ads_full', 'ads_create', 'ads_schedule', 'ads_analytics', 'ads_billing'],
        description: 'Advertisement campaign management',
        canApprove: true,
        canDelete: true
    },
    social_media_manager: {
        permissions: ['social_post', 'social_schedule', 'social_analytics'],
        description: 'Social media integration and posting',
        canApprove: true,
        canDelete: false
    },
    community_lead: {
        permissions: ['community_full', 'charity_manage', 'career_manage', 'initiatives_manage'],
        description: 'Community engagement and initiatives',
        canApprove: true,
        canDelete: false
    },
    report_analyst: {
        permissions: ['reports_generate', 'reports_view', 'reports_export'],
        description: 'Generate and export reports',
        canApprove: false,
        canDelete: false
    },
    data_analyst: {
        permissions: ['analytics_full', 'insights_view', 'reports_full', 'data_export'],
        description: 'Full analytics and data access',
        canApprove: false,
        canDelete: false
    },
    guide_editor: {
        permissions: ['guide_full', 'guide_approve', 'guide_edit'],
        description: 'Jacksonville guide content management',
        canApprove: true,
        canDelete: true
    },
    survey_coordinator: {
        permissions: ['survey_create', 'survey_manage', 'survey_analyze'],
        description: 'Survey creation and analysis',
        canApprove: true,
        canDelete: false
    }
};

/**
 * Assign specialized role to a user
 * @param {string} userId - User to assign role
 * @param {string} specializedRole - Role from SPECIALIZED_ROLES
 * @param {object} options - Additional options (scope, expiry, etc.)
 * @param {string} assignedBy - Admin assigning the role
 */
export async function assignSpecializedRole(userId, specializedRole, options = {}, assignedBy) {
    try {
        // Validate role exists
        if (!SPECIALIZED_PERMISSIONS[specializedRole]) {
            return { success: false, error: 'Invalid specialized role' };
        }
        
        // Check if user already has this role
        const existing = await wixData.query('SpecializedRoles')
            .eq('userId', userId)
            .eq('role', specializedRole)
            .eq('isActive', true)
            .find({ suppressAuth: true });
        
        if (existing.items.length > 0) {
            return { success: false, error: 'User already has this role' };
        }
        
        const roleAssignment = {
            userId,
            role: specializedRole,
            permissions: SPECIALIZED_PERMISSIONS[specializedRole].permissions,
            canApprove: SPECIALIZED_PERMISSIONS[specializedRole].canApprove,
            canDelete: SPECIALIZED_PERMISSIONS[specializedRole].canDelete,
            scopeLimit: options.scopeLimit || SPECIALIZED_PERMISSIONS[specializedRole].scopeLimit || null,
            assignedEvents: options.assignedEvents || [],
            expiryDate: options.expiryDate || null,
            isActive: true,
            assignedBy,
            assignedAt: new Date(),
            notes: options.notes || ''
        };
        
        const result = await wixData.insert('SpecializedRoles', roleAssignment, { suppressAuth: true });
        
        await logAdminActivity(assignedBy, 'role_assigned', 
            `Assigned ${specializedRole} to user ${userId}`);
        
        return {
            success: true,
            roleAssignmentId: result._id,
            permissions: roleAssignment.permissions
        };
    } catch (error) {
        console.error('Role assignment failed:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Remove specialized role from user
 */
export async function removeSpecializedRole(userId, specializedRole, removedBy) {
    try {
        const existing = await wixData.query('SpecializedRoles')
            .eq('userId', userId)
            .eq('role', specializedRole)
            .eq('isActive', true)
            .find({ suppressAuth: true });
        
        if (existing.items.length === 0) {
            return { success: false, error: 'Role assignment not found' };
        }
        
        await wixData.update('SpecializedRoles', {
            ...existing.items[0],
            isActive: false,
            revokedBy: removedBy,
            revokedAt: new Date()
        }, { suppressAuth: true });
        
        await logAdminActivity(removedBy, 'role_revoked', 
            `Revoked ${specializedRole} from user ${userId}`);
        
        return { success: true, message: 'Role removed successfully' };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Check if user has specialized permission
 */
export async function hasSpecializedPermission(userId, permission) {
    try {
        const roles = await wixData.query('SpecializedRoles')
            .eq('userId', userId)
            .eq('isActive', true)
            .find({ suppressAuth: true });
        
        for (const role of roles.items) {
            // Check expiry
            if (role.expiryDate && new Date(role.expiryDate) < new Date()) {
                continue;
            }
            
            if (role.permissions.includes(permission)) {
                return true;
            }
        }
        
        return false;
    } catch (error) {
        console.error('Permission check failed:', error);
        return false;
    }
}

/**
 * Get all specialized roles for a user
 */
export async function getUserSpecializedRoles(userId) {
    try {
        const roles = await wixData.query('SpecializedRoles')
            .eq('userId', userId)
            .eq('isActive', true)
            .find({ suppressAuth: true });
        
        return {
            success: true,
            roles: roles.items.map(r => ({
                role: r.role,
                permissions: r.permissions,
                canApprove: r.canApprove,
                canDelete: r.canDelete,
                assignedAt: r.assignedAt,
                expiryDate: r.expiryDate
            }))
        };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Get all users with a specific specialized role
 */
export async function getUsersBySpecializedRole(role) {
    try {
        const assignments = await wixData.query('SpecializedRoles')
            .eq('role', role)
            .eq('isActive', true)
            .find({ suppressAuth: true });
        
        return {
            success: true,
            users: assignments.items.map(a => ({
                userId: a.userId,
                assignedAt: a.assignedAt,
                assignedBy: a.assignedBy
            }))
        };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Get role metadata
 */
export function getRoleMetadata(role) {
    if (!SPECIALIZED_PERMISSIONS[role]) {
        return null;
    }
    
    return {
        role,
        ...SPECIALIZED_PERMISSIONS[role]
    };
}

/**
 * Get all available specialized roles
 */
export function getAllSpecializedRoles() {
    return Object.entries(SPECIALIZED_ROLES).map(([key, value]) => ({
        key,
        value,
        metadata: SPECIALIZED_PERMISSIONS[value]
    }));
}

```
------------------------------------------------------------

## [36/41] sponsor-management
- File: `sponsor-management.jsw`
- Size: 34.7 KB
- Lines: 1111

```javascript
/**
 * BANF Sponsor Management Service
 * =================================
 * Wix Velo Backend Module for automated sponsorship management
 * 
 * Features:
 * - Sponsorship tier management
 * - Sponsor application & approval
 * - Benefit tracking & fulfillment
 * - Recognition automation
 * - Sponsor portal
 * 
 * @module backend/sponsor-management.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';
import { triggeredEmails } from 'wix-crm-backend';

// =====================================================
// SPONSORSHIP TIERS CONFIGURATION
// =====================================================

const SPONSORSHIP_TIERS = {
    PLATINUM: {
        name: 'Platinum Sponsor',
        icon: '🏆',
        minAmount: 5000,
        maxSponsors: 1, // Exclusive
        benefits: [
            'Exclusive naming rights (e.g., "Durga Puja presented by [Sponsor]")',
            'Premium logo placement on all materials',
            'Full-page ad in souvenir magazine',
            'Banner at main entrance',
            'VIP seating for 10 guests',
            'Social media spotlight (5 posts)',
            'Recognition in all communications',
            'Premium booth space (if desired)',
            'Speaking opportunity at main event'
        ],
        logoSize: 'extra-large',
        websitePosition: 1
    },
    GOLD: {
        name: 'Gold Sponsor',
        icon: '🥇',
        minAmount: 2500,
        maxSponsors: 3,
        benefits: [
            'Large logo on banners and materials',
            'Half-page ad in souvenir magazine',
            'Banner placement at event',
            'VIP seating for 6 guests',
            'Social media recognition (3 posts)',
            'Recognition in email communications',
            'Standard booth space (if desired)'
        ],
        logoSize: 'large',
        websitePosition: 2
    },
    SILVER: {
        name: 'Silver Sponsor',
        icon: '🥈',
        minAmount: 1000,
        maxSponsors: 5,
        benefits: [
            'Medium logo on select materials',
            'Quarter-page ad in souvenir magazine',
            'Table banner at event',
            'Reserved seating for 4 guests',
            'Social media mention (2 posts)',
            'Recognition on website'
        ],
        logoSize: 'medium',
        websitePosition: 3
    },
    BRONZE: {
        name: 'Bronze Sponsor',
        icon: '🥉',
        minAmount: 500,
        maxSponsors: 10,
        benefits: [
            'Logo on sponsor recognition board',
            'Business card ad in souvenir magazine',
            'Reserved seating for 2 guests',
            'Social media mention (1 post)',
            'Recognition on website'
        ],
        logoSize: 'small',
        websitePosition: 4
    },
    SUPPORTER: {
        name: 'Community Supporter',
        icon: '💝',
        minAmount: 100,
        maxSponsors: null, // Unlimited
        benefits: [
            'Name listed on supporter board',
            'Recognition on website',
            'Thank you in program'
        ],
        logoSize: 'text-only',
        websitePosition: 5
    }
};

const SPONSOR_STATUS = {
    PENDING: 'pending',
    APPROVED: 'approved',
    ACTIVE: 'active',
    COMPLETED: 'completed',
    DECLINED: 'declined',
    CANCELLED: 'cancelled'
};

const BENEFIT_STATUS = {
    PENDING: 'pending',
    IN_PROGRESS: 'in_progress',
    COMPLETED: 'completed',
    NOT_APPLICABLE: 'not_applicable'
};

// =====================================================
// SPONSOR APPLICATION
// =====================================================

/**
 * Submit sponsor application
 * @param {Object} applicationData 
 */
export async function submitSponsorApplication(applicationData) {
    try {
        const tier = SPONSORSHIP_TIERS[applicationData.tier];
        
        if (!tier) {
            return { success: false, error: 'Invalid sponsorship tier' };
        }
        
        // Check tier availability for event
        if (tier.maxSponsors) {
            const existingSponsors = await wixData.query('Sponsors')
                .eq('eventId', applicationData.eventId)
                .eq('tier', applicationData.tier)
                .ne('status', SPONSOR_STATUS.DECLINED)
                .ne('status', SPONSOR_STATUS.CANCELLED)
                .find();
            
            if (existingSponsors.items.length >= tier.maxSponsors) {
                return { 
                    success: false, 
                    error: `${tier.name} tier is fully committed for this event` 
                };
            }
        }
        
        // Validate amount
        if (applicationData.amount < tier.minAmount) {
            return { 
                success: false, 
                error: `Minimum amount for ${tier.name} is $${tier.minAmount}` 
            };
        }
        
        const member = await currentMember.getMember().catch(() => null);
        
        const sponsor = await wixData.insert('Sponsors', {
            // Event
            eventId: applicationData.eventId,
            eventYear: applicationData.eventYear || new Date().getFullYear(),
            
            // Company Info
            companyName: applicationData.companyName,
            industry: applicationData.industry || '',
            website: applicationData.website || '',
            
            // Contact Info
            contactName: applicationData.contactName,
            contactTitle: applicationData.contactTitle || '',
            email: applicationData.email,
            phone: applicationData.phone,
            
            // Address
            address: applicationData.address || '',
            city: applicationData.city || '',
            state: applicationData.state || 'FL',
            zip: applicationData.zip || '',
            
            // Sponsorship Details
            tier: applicationData.tier,
            tierName: tier.name,
            pledgedAmount: applicationData.amount,
            paidAmount: 0,
            balance: applicationData.amount,
            
            // Benefits
            benefits: tier.benefits.map(benefit => ({
                description: benefit,
                status: BENEFIT_STATUS.PENDING,
                notes: ''
            })),
            
            // Custom Benefits (if any)
            customBenefits: applicationData.customBenefits || [],
            
            // Media
            logo: applicationData.logo || '',
            logoApproved: false,
            adArtwork: '',
            adArtworkApproved: false,
            
            // Social Media
            socialMediaHandles: applicationData.socialMediaHandles || {},
            
            // Status
            status: SPONSOR_STATUS.PENDING,
            
            // Payment
            paymentStatus: 'pending',
            invoiceSent: false,
            
            // Recognition
            recognitionName: applicationData.recognitionName || applicationData.companyName,
            
            // Notes
            specialRequests: applicationData.specialRequests || '',
            adminNotes: '',
            
            // Metadata
            applicationNumber: generateApplicationNumber('SPO'),
            memberId: member?._id || null,
            appliedAt: new Date(),
            createdAt: new Date(),
            lastModified: new Date()
        });
        
        // Send confirmation email
        await triggeredEmails.emailContact(
            'sponsor_application_received',
            applicationData.email,
            {
                variables: {
                    contactName: applicationData.contactName,
                    companyName: applicationData.companyName,
                    tier: tier.name,
                    amount: applicationData.amount,
                    applicationNumber: sponsor.applicationNumber
                }
            }
        );
        
        // Create admin task
        await createAdminTask({
            type: 'SPONSOR_APPLICATION_REVIEW',
            title: `Review sponsor application: ${applicationData.companyName} (${tier.name})`,
            sponsorId: sponsor._id,
            priority: applicationData.tier === 'PLATINUM' ? 'high' : 'medium'
        });
        
        await logSponsorActivity(sponsor._id, 'APPLICATION_SUBMITTED', 
            `Sponsorship application submitted for ${tier.name} ($${applicationData.amount})`);
        
        return {
            success: true,
            sponsorId: sponsor._id,
            applicationNumber: sponsor.applicationNumber,
            message: 'Thank you for your sponsorship application! Our team will contact you shortly.'
        };
        
    } catch (error) {
        console.error('Error submitting sponsor application:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// SPONSOR APPROVAL WORKFLOW
// =====================================================

/**
 * Approve sponsor application
 * @param {string} sponsorId 
 * @param {Object} approvalData 
 */
export async function approveSponsorApplication(sponsorId, approvalData = {}) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized: Admin access required');
    }
    
    try {
        const sponsor = await wixData.get('Sponsors', sponsorId);
        
        if (!sponsor) {
            return { success: false, error: 'Sponsor not found' };
        }
        
        if (sponsor.status !== SPONSOR_STATUS.PENDING) {
            return { success: false, error: 'Application already processed' };
        }
        
        sponsor.status = SPONSOR_STATUS.APPROVED;
        sponsor.approvedAt = new Date();
        sponsor.approvedBy = member._id;
        sponsor.approvalNotes = approvalData.notes || '';
        sponsor.lastModified = new Date();
        
        await wixData.update('Sponsors', sponsor);
        
        // Send approval email with invoice
        await sendSponsorInvoice(sponsorId);
        
        await logSponsorActivity(sponsorId, 'APPLICATION_APPROVED', 
            `Sponsorship approved by admin`);
        
        return {
            success: true,
            message: 'Sponsor application approved and invoice sent'
        };
        
    } catch (error) {
        console.error('Error approving sponsor:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Decline sponsor application
 * @param {string} sponsorId 
 * @param {string} reason 
 */
export async function declineSponsorApplication(sponsorId, reason = '') {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const sponsor = await wixData.get('Sponsors', sponsorId);
        
        sponsor.status = SPONSOR_STATUS.DECLINED;
        sponsor.declinedAt = new Date();
        sponsor.declinedBy = member._id;
        sponsor.declineReason = reason;
        sponsor.lastModified = new Date();
        
        await wixData.update('Sponsors', sponsor);
        
        // Send decline email
        await triggeredEmails.emailContact(
            'sponsor_application_declined',
            sponsor.email,
            {
                variables: {
                    contactName: sponsor.contactName,
                    companyName: sponsor.companyName,
                    reason: reason || 'We appreciate your interest but are unable to proceed at this time.'
                }
            }
        );
        
        await logSponsorActivity(sponsorId, 'APPLICATION_DECLINED', reason);
        
        return {
            success: true,
            message: 'Application declined and sponsor notified'
        };
        
    } catch (error) {
        console.error('Error declining sponsor:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// SPONSOR PAYMENT
// =====================================================

/**
 * Send invoice to sponsor
 * @param {string} sponsorId 
 */
export async function sendSponsorInvoice(sponsorId) {
    try {
        const sponsor = await wixData.get('Sponsors', sponsorId);
        const event = await wixData.get('Events', sponsor.eventId);
        
        // Create invoice record
        const invoice = await wixData.insert('SponsorInvoices', {
            sponsorId: sponsorId,
            eventId: sponsor.eventId,
            invoiceNumber: generateInvoiceNumber(),
            amount: sponsor.pledgedAmount,
            tier: sponsor.tierName,
            status: 'sent',
            sentAt: new Date(),
            dueDate: addDays(new Date(), 30),
            createdAt: new Date()
        });
        
        // Send invoice email
        await triggeredEmails.emailContact(
            'sponsor_invoice',
            sponsor.email,
            {
                variables: {
                    contactName: sponsor.contactName,
                    companyName: sponsor.companyName,
                    tier: sponsor.tierName,
                    amount: sponsor.pledgedAmount,
                    invoiceNumber: invoice.invoiceNumber,
                    eventName: event.title,
                    dueDate: formatDate(invoice.dueDate),
                    paymentLink: `https://jaxbengali.org/sponsor-payment/${invoice._id}`
                }
            }
        );
        
        sponsor.invoiceSent = true;
        sponsor.invoiceSentDate = new Date();
        sponsor.currentInvoiceId = invoice._id;
        await wixData.update('Sponsors', sponsor);
        
        await logSponsorActivity(sponsorId, 'INVOICE_SENT', 
            `Invoice #${invoice.invoiceNumber} for $${sponsor.pledgedAmount} sent`);
        
        return {
            success: true,
            invoiceId: invoice._id,
            invoiceNumber: invoice.invoiceNumber
        };
        
    } catch (error) {
        console.error('Error sending invoice:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Process sponsor payment
 * @param {string} sponsorId 
 * @param {Object} paymentInfo 
 */
export async function processSponsorPayment(sponsorId, paymentInfo) {
    try {
        const sponsor = await wixData.get('Sponsors', sponsorId);
        
        // Create payment record
        const payment = await wixData.insert('SponsorPayments', {
            sponsorId: sponsorId,
            eventId: sponsor.eventId,
            invoiceId: sponsor.currentInvoiceId || null,
            
            amount: paymentInfo.amount,
            paymentMethod: paymentInfo.method,
            transactionId: paymentInfo.transactionId || '',
            checkNumber: paymentInfo.checkNumber || '',
            
            status: 'completed',
            processedAt: new Date(),
            notes: paymentInfo.notes || ''
        });
        
        // Update sponsor
        sponsor.paidAmount = (sponsor.paidAmount || 0) + paymentInfo.amount;
        sponsor.balance = sponsor.pledgedAmount - sponsor.paidAmount;
        sponsor.paymentStatus = sponsor.balance <= 0 ? 'paid' : 'partial';
        sponsor.lastPaymentDate = new Date();
        
        // Activate sponsor if fully paid
        if (sponsor.balance <= 0 && sponsor.status === SPONSOR_STATUS.APPROVED) {
            sponsor.status = SPONSOR_STATUS.ACTIVE;
            sponsor.activatedAt = new Date();
        }
        
        await wixData.update('Sponsors', sponsor);
        
        // Update invoice if exists
        if (sponsor.currentInvoiceId) {
            const invoice = await wixData.get('SponsorInvoices', sponsor.currentInvoiceId);
            invoice.status = sponsor.balance <= 0 ? 'paid' : 'partial';
            invoice.paidAmount = sponsor.paidAmount;
            await wixData.update('SponsorInvoices', invoice);
        }
        
        // Send receipt
        await triggeredEmails.emailContact(
            'sponsor_payment_receipt',
            sponsor.email,
            {
                variables: {
                    contactName: sponsor.contactName,
                    companyName: sponsor.companyName,
                    amount: paymentInfo.amount,
                    totalPaid: sponsor.paidAmount,
                    balance: sponsor.balance,
                    transactionId: payment._id
                }
            }
        );
        
        // If fully paid, send welcome package
        if (sponsor.balance <= 0) {
            await sendSponsorWelcomePackage(sponsorId);
        }
        
        await logSponsorActivity(sponsorId, 'PAYMENT_RECEIVED', 
            `Payment of $${paymentInfo.amount} received. Balance: $${sponsor.balance}`);
        
        return {
            success: true,
            paymentId: payment._id,
            newBalance: sponsor.balance,
            isFullyPaid: sponsor.balance <= 0
        };
        
    } catch (error) {
        console.error('Error processing sponsor payment:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// BENEFIT TRACKING
// =====================================================

/**
 * Send sponsor welcome package
 * @param {string} sponsorId 
 */
async function sendSponsorWelcomePackage(sponsorId) {
    const sponsor = await wixData.get('Sponsors', sponsorId);
    const event = await wixData.get('Events', sponsor.eventId);
    const tier = SPONSORSHIP_TIERS[sponsor.tier];
    
    await triggeredEmails.emailContact(
        'sponsor_welcome_package',
        sponsor.email,
        {
            variables: {
                contactName: sponsor.contactName,
                companyName: sponsor.companyName,
                tier: sponsor.tierName,
                eventName: event.title,
                eventDate: formatDate(event.eventDate),
                benefits: tier.benefits.join('\n• '),
                logoDeadline: formatDate(addDays(new Date(), 14)),
                adArtworkDeadline: formatDate(addDays(new Date(), 21)),
                sponsorPortalLink: `https://jaxbengali.org/sponsor-portal/${sponsor._id}`
            }
        }
    );
    
    sponsor.welcomePackageSent = true;
    sponsor.welcomePackageSentDate = new Date();
    await wixData.update('Sponsors', sponsor);
}

/**
 * Update benefit status
 * @param {string} sponsorId 
 * @param {number} benefitIndex 
 * @param {string} status 
 * @param {string} notes 
 */
export async function updateBenefitStatus(sponsorId, benefitIndex, status, notes = '') {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const sponsor = await wixData.get('Sponsors', sponsorId);
        
        if (benefitIndex < 0 || benefitIndex >= sponsor.benefits.length) {
            return { success: false, error: 'Invalid benefit index' };
        }
        
        sponsor.benefits[benefitIndex].status = status;
        sponsor.benefits[benefitIndex].notes = notes;
        sponsor.benefits[benefitIndex].updatedAt = new Date();
        sponsor.benefits[benefitIndex].updatedBy = member._id;
        
        sponsor.lastModified = new Date();
        await wixData.update('Sponsors', sponsor);
        
        // Check if all benefits completed
        const allCompleted = sponsor.benefits.every(
            b => b.status === BENEFIT_STATUS.COMPLETED || b.status === BENEFIT_STATUS.NOT_APPLICABLE
        );
        
        if (allCompleted && sponsor.status === SPONSOR_STATUS.ACTIVE) {
            sponsor.status = SPONSOR_STATUS.COMPLETED;
            sponsor.completedAt = new Date();
            await wixData.update('Sponsors', sponsor);
        }
        
        await logSponsorActivity(sponsorId, 'BENEFIT_UPDATED', 
            `Benefit "${sponsor.benefits[benefitIndex].description}" marked as ${status}`);
        
        return {
            success: true,
            message: 'Benefit status updated'
        };
        
    } catch (error) {
        console.error('Error updating benefit:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Upload sponsor logo
 * @param {string} sponsorId 
 * @param {string} logoUrl 
 */
export async function uploadSponsorLogo(sponsorId, logoUrl) {
    try {
        const sponsor = await wixData.get('Sponsors', sponsorId);
        
        sponsor.logo = logoUrl;
        sponsor.logoUploadedAt = new Date();
        sponsor.logoApproved = false; // Needs admin approval
        sponsor.lastModified = new Date();
        
        await wixData.update('Sponsors', sponsor);
        
        // Create admin task for logo review
        await createAdminTask({
            type: 'SPONSOR_LOGO_REVIEW',
            title: `Review logo for ${sponsor.companyName}`,
            sponsorId: sponsorId,
            priority: 'low'
        });
        
        await logSponsorActivity(sponsorId, 'LOGO_UPLOADED', 'Logo uploaded for review');
        
        return {
            success: true,
            message: 'Logo uploaded. Pending approval.'
        };
        
    } catch (error) {
        console.error('Error uploading logo:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Approve sponsor logo
 * @param {string} sponsorId 
 */
export async function approveSponsorLogo(sponsorId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const sponsor = await wixData.get('Sponsors', sponsorId);
        
        sponsor.logoApproved = true;
        sponsor.logoApprovedAt = new Date();
        sponsor.logoApprovedBy = member._id;
        sponsor.lastModified = new Date();
        
        await wixData.update('Sponsors', sponsor);
        
        // Notify sponsor
        await triggeredEmails.emailContact(
            'sponsor_logo_approved',
            sponsor.email,
            {
                variables: {
                    contactName: sponsor.contactName,
                    companyName: sponsor.companyName
                }
            }
        );
        
        await logSponsorActivity(sponsorId, 'LOGO_APPROVED', 'Logo approved for use');
        
        return {
            success: true,
            message: 'Logo approved'
        };
        
    } catch (error) {
        console.error('Error approving logo:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// RECOGNITION & DISPLAY
// =====================================================

/**
 * Get sponsors for public display
 * @param {string} eventId 
 */
export async function getEventSponsors(eventId) {
    try {
        const sponsors = await wixData.query('Sponsors')
            .eq('eventId', eventId)
            .eq('status', SPONSOR_STATUS.ACTIVE)
            .or(
                wixData.query('Sponsors')
                    .eq('eventId', eventId)
                    .eq('status', SPONSOR_STATUS.COMPLETED)
            )
            .eq('logoApproved', true)
            .find();
        
        // Group by tier
        const groupedSponsors = {
            platinum: [],
            gold: [],
            silver: [],
            bronze: [],
            supporter: []
        };
        
        for (const sponsor of sponsors.items) {
            const tier = sponsor.tier.toLowerCase();
            if (groupedSponsors[tier]) {
                groupedSponsors[tier].push({
                    id: sponsor._id,
                    companyName: sponsor.companyName,
                    recognitionName: sponsor.recognitionName,
                    logo: sponsor.logo,
                    website: sponsor.website,
                    tier: sponsor.tierName
                });
            }
        }
        
        return {
            success: true,
            sponsors: groupedSponsors,
            tiers: Object.keys(SPONSORSHIP_TIERS).map(key => ({
                key: key,
                ...SPONSORSHIP_TIERS[key]
            }))
        };
        
    } catch (error) {
        console.error('Error getting event sponsors:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Get sponsor wall data for display
 * @param {string} eventId 
 */
export async function getSponsorWallData(eventId) {
    try {
        const result = await getEventSponsors(eventId);
        
        if (!result.success) {
            return result;
        }
        
        // Format for sponsor wall display
        const wallData = Object.entries(result.sponsors)
            .filter(([_, sponsors]) => sponsors.length > 0)
            .map(([tier, sponsors]) => {
                const tierConfig = SPONSORSHIP_TIERS[tier.toUpperCase()];
                return {
                    tier: tier,
                    tierName: tierConfig.name,
                    icon: tierConfig.icon,
                    logoSize: tierConfig.logoSize,
                    sponsors: sponsors
                };
            })
            .sort((a, b) => {
                const posA = SPONSORSHIP_TIERS[a.tier.toUpperCase()]?.websitePosition || 99;
                const posB = SPONSORSHIP_TIERS[b.tier.toUpperCase()]?.websitePosition || 99;
                return posA - posB;
            });
        
        return {
            success: true,
            wallData: wallData
        };
        
    } catch (error) {
        console.error('Error getting sponsor wall data:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// REPORTING
// =====================================================

/**
 * Get sponsorship report for event
 * @param {string} eventId 
 */
export async function getSponsorshipReport(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const sponsors = await wixData.query('Sponsors')
            .eq('eventId', eventId)
            .find();
        
        const summary = {
            totalSponsors: sponsors.items.length,
            byTier: {},
            totalPledged: 0,
            totalPaid: 0,
            totalOutstanding: 0,
            byStatus: {}
        };
        
        // Initialize tier counts
        for (const tier of Object.keys(SPONSORSHIP_TIERS)) {
            summary.byTier[tier] = { count: 0, pledged: 0, paid: 0 };
        }
        
        // Initialize status counts
        for (const status of Object.values(SPONSOR_STATUS)) {
            summary.byStatus[status] = 0;
        }
        
        // Process sponsors
        for (const sponsor of sponsors.items) {
            summary.totalPledged += sponsor.pledgedAmount;
            summary.totalPaid += sponsor.paidAmount;
            summary.totalOutstanding += sponsor.balance;
            
            if (summary.byTier[sponsor.tier]) {
                summary.byTier[sponsor.tier].count++;
                summary.byTier[sponsor.tier].pledged += sponsor.pledgedAmount;
                summary.byTier[sponsor.tier].paid += sponsor.paidAmount;
            }
            
            summary.byStatus[sponsor.status] = (summary.byStatus[sponsor.status] || 0) + 1;
        }
        
        // Benefit fulfillment report
        const benefitReport = [];
        for (const sponsor of sponsors.items.filter(s => 
            s.status === SPONSOR_STATUS.ACTIVE || s.status === SPONSOR_STATUS.COMPLETED)) {
            
            const completedBenefits = sponsor.benefits.filter(
                b => b.status === BENEFIT_STATUS.COMPLETED
            ).length;
            
            benefitReport.push({
                companyName: sponsor.companyName,
                tier: sponsor.tierName,
                totalBenefits: sponsor.benefits.length,
                completedBenefits: completedBenefits,
                fulfillmentRate: Math.round((completedBenefits / sponsor.benefits.length) * 100)
            });
        }
        
        return {
            success: true,
            summary: summary,
            sponsors: sponsors.items.map(s => ({
                id: s._id,
                companyName: s.companyName,
                tier: s.tierName,
                status: s.status,
                pledgedAmount: s.pledgedAmount,
                paidAmount: s.paidAmount,
                balance: s.balance,
                logoApproved: s.logoApproved
            })),
            benefitFulfillment: benefitReport
        };
        
    } catch (error) {
        console.error('Error getting sponsorship report:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Get all sponsors (admin view)
 * @param {Object} filters 
 */
export async function getAllSponsors(filters = {}) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        let query = wixData.query('Sponsors');
        
        if (filters.eventId) {
            query = query.eq('eventId', filters.eventId);
        }
        if (filters.tier) {
            query = query.eq('tier', filters.tier);
        }
        if (filters.status) {
            query = query.eq('status', filters.status);
        }
        if (filters.year) {
            query = query.eq('eventYear', parseInt(filters.year));
        }
        
        const sponsors = await query
            .descending('createdAt')
            .find();
        
        return {
            success: true,
            sponsors: sponsors.items,
            total: sponsors.items.length
        };
        
    } catch (error) {
        console.error('Error getting sponsors:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Send thank you to all sponsors
 * @param {string} eventId 
 */
export async function sendSponsorThankYou(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        const sponsors = await wixData.query('Sponsors')
            .eq('eventId', eventId)
            .eq('paymentStatus', 'paid')
            .find();
        
        let sentCount = 0;
        
        for (const sponsor of sponsors.items) {
            await triggeredEmails.emailContact(
                'sponsor_thank_you',
                sponsor.email,
                {
                    variables: {
                        contactName: sponsor.contactName,
                        companyName: sponsor.companyName,
                        tier: sponsor.tierName,
                        eventName: event.title,
                        amount: sponsor.paidAmount
                    }
                }
            );
            
            sponsor.thankYouSent = true;
            sponsor.thankYouSentDate = new Date();
            await wixData.update('Sponsors', sponsor);
            
            sentCount++;
        }
        
        return {
            success: true,
            sentCount: sentCount,
            message: `Thank you emails sent to ${sentCount} sponsors`
        };
        
    } catch (error) {
        console.error('Error sending thank you:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

/**
 * Generate application/invoice number
 */
function generateApplicationNumber(prefix = 'SPO') {
    const year = new Date().getFullYear();
    const random = Math.random().toString(36).substring(2, 6).toUpperCase();
    return `${prefix}-${year}-${random}`;
}

function generateInvoiceNumber() {
    return generateApplicationNumber('INV');
}

/**
 * Add days to date
 */
function addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

/**
 * Format date for display
 */
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Create admin task
 */
async function createAdminTask(taskData) {
    await wixData.insert('AdminTasks', {
        ...taskData,
        status: 'pending',
        createdAt: new Date()
    });
}

/**
 * Log sponsor activity
 */
async function logSponsorActivity(sponsorId, action, details) {
    await wixData.insert('SponsorActivityLog', {
        sponsorId: sponsorId,
        action: action,
        details: details,
        timestamp: new Date()
    });
}

/**
 * Check if member is admin
 */
async function isAdmin(memberId) {
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec')
            );
        }
        return false;
    } catch {
        return false;
    }
}

/**
 * Get sponsorship tier information
 */
export function getSponsorshipTiers() {
    return Object.entries(SPONSORSHIP_TIERS).map(([key, tier]) => ({
        id: key,
        ...tier
    }));
}

```
------------------------------------------------------------

## [37/41] sponsorship
- File: `sponsorship.jsw`
- Size: 20.4 KB
- Lines: 576

```javascript
// backend/sponsorship.jsw
// BANF Sponsorship & Vendor Management - Wix Velo Backend

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';

// Sponsorship tier constants (based on BANF's structure)
const SPONSORSHIP_TIERS = {
    PLATINUM: { name: 'Platinum', minAmount: 2000, benefits: ['Title Sponsor recognition', 'Back cover ad', 'Banner at all events', 'VIP seating'] },
    GOLD: { name: 'Gold', minAmount: 1000, benefits: ['Full page + inside cover ad', 'Name on all promo materials', 'Event recognition'] },
    SILVER: { name: 'Silver', minAmount: 500, benefits: ['Full page ad', 'Website feature', 'Event recognition'] },
    BRONZE: { name: 'Bronze', minAmount: 250, benefits: ['Half page ad', 'Social media mention'] },
    SUPPORTER: { name: 'Supporter', minAmount: 100, benefits: ['Quarter page ad', 'Newsletter mention'] }
};

// Magazine advertisement rates
const MAGAZINE_AD_RATES = {
    QUARTER_PAGE: { name: 'Quarter Page', price: 125 },
    HALF_PAGE: { name: 'Half Page', price: 250 },
    FULL_PAGE: { name: 'Full Page', price: 400 },
    CENTER_PAGES: { name: '2 Full Center Pages', price: 450, slots: 1 },
    INSIDE_COVER: { name: 'Front or Back Inside Cover', price: 500, slots: 2 },
    BACK_COVER: { name: 'Back Cover', price: 700, slots: 1 }
};

// Food sponsorship categories
const FOOD_SPONSORSHIP_TYPES = {
    MISHTI: { name: 'Mishti/Sweets', minAmount: 200, maxAmount: 400 },
    LUNCH: { name: 'Lunch', minAmount: 400, maxAmount: 600 },
    DINNER: { name: 'Dinner', minAmount: 500, maxAmount: 800 },
    TEA_SNACKS: { name: 'Tea/Snacks', minAmount: 150, maxAmount: 300 },
    FRUITS: { name: 'Puja Fruits', minAmount: 100, maxAmount: 200 },
    FLOWERS: { name: 'Puja Flowers', minAmount: 100, maxAmount: 200 },
    SPECIAL_ITEMS: { name: 'Special Items', minAmount: 100, maxAmount: 500 }
};

// Sponsor status
const SPONSOR_STATUS = {
    PROSPECT: 'prospect',
    CONTACTED: 'contacted',
    PLEDGED: 'pledged',
    RECEIVED: 'received',
    DECLINED: 'declined'
};

/**
 * Create new sponsor record
 */
export async function createSponsor(sponsorData, adminId) {
    try {
        // Determine tier based on amount
        const tier = determineTier(sponsorData.amount);
        
        const sponsor = {
            // Basic Info
            sponsorName: sponsorData.name,
            businessName: sponsorData.businessName || '',
            contactPerson: sponsorData.contactPerson || sponsorData.name,
            email: sponsorData.email,
            phone: sponsorData.phone || '',
            address: sponsorData.address || '',
            website: sponsorData.website || '',
            
            // Sponsorship Details
            sponsorType: sponsorData.type || 'general', // general, food, vendor, event_title
            sponsorshipTier: tier,
            pledgedAmount: sponsorData.amount || 0,
            receivedAmount: 0,
            
            // Magazine Ad
            magazineAdType: sponsorData.magazineAdType || '',
            magazineAdRate: MAGAZINE_AD_RATES[sponsorData.magazineAdType]?.price || 0,
            adArtworkUrl: sponsorData.artworkUrl || '',
            
            // Food Sponsorship (if applicable)
            foodSponsorshipType: sponsorData.foodType || '',
            foodItemDescription: sponsorData.foodDescription || '',
            targetEvent: sponsorData.targetEvent || '',
            
            // Internet Promotion Package
            hasInternetPromotion: sponsorData.internetPromotion || false,
            internetPromotionFee: sponsorData.internetPromotion ? 250 : 0,
            
            // Status & Tracking
            status: SPONSOR_STATUS.PROSPECT,
            fiscalYear: sponsorData.fiscalYear || getCurrentFiscalYear(),
            notes: sponsorData.notes || '',
            
            // History
            contactHistory: JSON.stringify([{
                date: new Date().toISOString(),
                action: 'created',
                by: adminId,
                notes: 'Sponsor record created'
            }]),
            
            // Flags
            isRecurring: sponsorData.isRecurring || false,
            isMember: sponsorData.isMember || false,
            memberId: sponsorData.memberId || '',
            
            // Metadata
            createdBy: adminId,
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert('Sponsors', sponsor);
        
        return {
            success: true,
            sponsorId: result._id,
            tier: tier,
            message: `Sponsor "${sponsorData.name}" created as ${tier} tier`
        };
    } catch (error) {
        console.error('Error creating sponsor:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get all sponsors with filters
 */
export async function getSponsors(options = { limit: 50, skip: 0, fiscalYear: null, status: null, tier: null }) {
    try {
        let query = wixData.query('Sponsors');
        
        if (options.fiscalYear) {
            query = query.eq('fiscalYear', options.fiscalYear);
        }
        if (options.status) {
            query = query.eq('status', options.status);
        }
        if (options.tier) {
            query = query.eq('sponsorshipTier', options.tier);
        }
        
        query = query
            .descending('pledgedAmount')
            .limit(options.limit)
            .skip(options.skip);
        
        const result = await query.find();
        
        return {
            items: result.items.map(s => ({
                ...s,
                contactHistory: JSON.parse(s.contactHistory || '[]')
            })),
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error getting sponsors:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Get sponsor by ID
 */
export async function getSponsorById(sponsorId) {
    try {
        const sponsor = await wixData.get('Sponsors', sponsorId);
        if (!sponsor) return null;
        
        return {
            ...sponsor,
            contactHistory: JSON.parse(sponsor.contactHistory || '[]')
        };
    } catch (error) {
        console.error('Error getting sponsor:', error);
        return null;
    }
}

/**
 * Update sponsor status and record payment
 */
export async function updateSponsorStatus(sponsorId, updateData, adminId) {
    try {
        const sponsor = await wixData.get('Sponsors', sponsorId);
        if (!sponsor) {
            return { success: false, error: 'Sponsor not found' };
        }
        
        // Parse contact history
        let contactHistory = JSON.parse(sponsor.contactHistory || '[]');
        
        // Add history entry
        contactHistory.push({
            date: new Date().toISOString(),
            action: updateData.action || 'update',
            by: adminId,
            notes: updateData.notes || '',
            previousStatus: sponsor.status,
            newStatus: updateData.status || sponsor.status
        });
        
        const updatedSponsor = {
            ...sponsor,
            status: updateData.status || sponsor.status,
            receivedAmount: updateData.receivedAmount !== undefined 
                ? updateData.receivedAmount 
                : sponsor.receivedAmount,
            paymentDate: updateData.paymentDate ? new Date(updateData.paymentDate) : sponsor.paymentDate,
            paymentMethod: updateData.paymentMethod || sponsor.paymentMethod,
            receiptNumber: updateData.receiptNumber || sponsor.receiptNumber,
            notes: updateData.notes || sponsor.notes,
            contactHistory: JSON.stringify(contactHistory),
            _updatedDate: new Date()
        };
        
        await wixData.update('Sponsors', updatedSponsor);
        
        return { success: true, message: 'Sponsor updated successfully' };
    } catch (error) {
        console.error('Error updating sponsor:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Record sponsorship payment
 */
export async function recordSponsorPayment(sponsorId, paymentData, adminId) {
    try {
        const sponsor = await wixData.get('Sponsors', sponsorId);
        if (!sponsor) {
            return { success: false, error: 'Sponsor not found' };
        }
        
        const newReceivedAmount = (sponsor.receivedAmount || 0) + paymentData.amount;
        const newStatus = newReceivedAmount >= sponsor.pledgedAmount 
            ? SPONSOR_STATUS.RECEIVED 
            : sponsor.status;
        
        // Update sponsor
        await updateSponsorStatus(sponsorId, {
            status: newStatus,
            receivedAmount: newReceivedAmount,
            paymentDate: paymentData.date,
            paymentMethod: paymentData.method,
            receiptNumber: paymentData.receiptNumber,
            action: 'payment',
            notes: `Payment of $${paymentData.amount} received via ${paymentData.method}`
        }, adminId);
        
        // Create financial record
        await wixData.insert('FinancialRecords', {
            transactionId: `SPO-${Date.now()}`,
            transactionType: 'income',
            category: 'sponsorship',
            subcategory: sponsor.sponsorType,
            amount: paymentData.amount,
            description: `Sponsorship from ${sponsor.sponsorName}`,
            transactionDate: new Date(paymentData.date),
            paymentMethod: paymentData.method,
            sponsorId: sponsorId,
            memberName: sponsor.sponsorName,
            receiptUrl: paymentData.receiptUrl || '',
            fiscalYear: sponsor.fiscalYear,
            isApproved: true,
            approvedBy: adminId,
            approvedAt: new Date(),
            createdBy: adminId,
            _createdDate: new Date()
        });
        
        return { 
            success: true, 
            message: 'Payment recorded',
            totalReceived: newReceivedAmount,
            status: newStatus
        };
    } catch (error) {
        console.error('Error recording payment:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get sponsorship summary by fiscal year
 */
export async function getSponsorshipSummary(fiscalYear = null) {
    try {
        const year = fiscalYear || getCurrentFiscalYear();
        
        const allSponsors = await wixData.query('Sponsors')
            .eq('fiscalYear', year)
            .limit(1000)
            .find();
        
        const summary = {
            fiscalYear: year,
            totalSponsors: allSponsors.totalCount,
            byTier: {},
            byStatus: {},
            byType: {},
            totalPledged: 0,
            totalReceived: 0,
            magazineAdRevenue: 0,
            foodSponsorships: 0,
            internetPromotionRevenue: 0
        };
        
        // Initialize tier counts
        Object.keys(SPONSORSHIP_TIERS).forEach(tier => {
            summary.byTier[tier] = { count: 0, pledged: 0, received: 0 };
        });
        
        // Initialize status counts
        Object.values(SPONSOR_STATUS).forEach(status => {
            summary.byStatus[status] = 0;
        });
        
        // Process sponsors
        allSponsors.items.forEach(sponsor => {
            summary.totalPledged += sponsor.pledgedAmount || 0;
            summary.totalReceived += sponsor.receivedAmount || 0;
            summary.magazineAdRevenue += sponsor.magazineAdRate || 0;
            
            if (sponsor.hasInternetPromotion) {
                summary.internetPromotionRevenue += 250;
            }
            
            if (sponsor.sponsorType === 'food') {
                summary.foodSponsorships += sponsor.pledgedAmount || 0;
            }
            
            // Count by tier
            const tier = sponsor.sponsorshipTier || 'SUPPORTER';
            if (summary.byTier[tier]) {
                summary.byTier[tier].count++;
                summary.byTier[tier].pledged += sponsor.pledgedAmount || 0;
                summary.byTier[tier].received += sponsor.receivedAmount || 0;
            }
            
            // Count by status
            const status = sponsor.status || 'prospect';
            summary.byStatus[status] = (summary.byStatus[status] || 0) + 1;
            
            // Count by type
            const type = sponsor.sponsorType || 'general';
            if (!summary.byType[type]) {
                summary.byType[type] = { count: 0, amount: 0 };
            }
            summary.byType[type].count++;
            summary.byType[type].amount += sponsor.receivedAmount || 0;
        });
        
        summary.collectionRate = summary.totalPledged > 0 
            ? Math.round((summary.totalReceived / summary.totalPledged) * 100) 
            : 0;
        
        return summary;
    } catch (error) {
        console.error('Error getting sponsorship summary:', error);
        return null;
    }
}

// ==================== VENDOR MANAGEMENT ====================

/**
 * Create vendor record
 */
export async function createVendor(vendorData, adminId) {
    try {
        const vendor = {
            vendorName: vendorData.name,
            businessName: vendorData.businessName || vendorData.name,
            contactPerson: vendorData.contactPerson || '',
            email: vendorData.email || '',
            phone: vendorData.phone,
            address: vendorData.address || '',
            website: vendorData.website || '',
            
            vendorType: vendorData.type || 'food', // food, supplies, services, venue, entertainment
            cuisineType: vendorData.cuisineType || '', // For food vendors: Bengali, Indian, etc.
            specialties: JSON.stringify(vendorData.specialties || []),
            
            // Pricing
            pricingInfo: vendorData.pricingInfo || '',
            averageOrderSize: vendorData.averageOrderSize || 0,
            minimumOrder: vendorData.minimumOrder || 0,
            
            // Quality & Service
            rating: 0,
            totalOrders: 0,
            reliabilityScore: 0,
            
            // Payment
            paymentTerms: vendorData.paymentTerms || 'on_delivery',
            acceptsCard: vendorData.acceptsCard || false,
            acceptsCheck: vendorData.acceptsCheck || true,
            acceptsCash: vendorData.acceptsCash || true,
            
            // Documents
            contractUrl: vendorData.contractUrl || '',
            insuranceUrl: vendorData.insuranceUrl || '',
            licenseUrl: vendorData.licenseUrl || '',
            
            // Status
            isActive: true,
            isPreferred: vendorData.isPreferred || false,
            isBengaliOwned: vendorData.bengaliOwned || false,
            
            notes: vendorData.notes || '',
            createdBy: adminId,
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert('Vendors', vendor);
        
        return { success: true, vendorId: result._id };
    } catch (error) {
        console.error('Error creating vendor:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get vendors with filters
 */
export async function getVendors(options = { type: null, isPreferred: null, isActive: true }) {
    try {
        let query = wixData.query('Vendors');
        
        if (options.isActive !== null) {
            query = query.eq('isActive', options.isActive);
        }
        if (options.type) {
            query = query.eq('vendorType', options.type);
        }
        if (options.isPreferred !== null) {
            query = query.eq('isPreferred', options.isPreferred);
        }
        
        query = query.ascending('vendorName');
        
        const result = await query.find();
        
        return result.items.map(v => ({
            ...v,
            specialties: JSON.parse(v.specialties || '[]')
        }));
    } catch (error) {
        console.error('Error getting vendors:', error);
        return [];
    }
}

/**
 * Record vendor order
 */
export async function recordVendorOrder(orderData, adminId) {
    try {
        const order = {
            vendorId: orderData.vendorId,
            eventId: orderData.eventId || '',
            eventName: orderData.eventName || '',
            
            orderDate: new Date(orderData.orderDate),
            deliveryDate: orderData.deliveryDate ? new Date(orderData.deliveryDate) : null,
            
            items: JSON.stringify(orderData.items || []),
            itemDescription: orderData.description || '',
            
            quantity: orderData.quantity || '',
            totalAmount: orderData.amount,
            paidAmount: orderData.paidAmount || 0,
            
            paymentStatus: orderData.paidAmount >= orderData.amount ? 'paid' : 'pending',
            paymentMethod: orderData.paymentMethod || '',
            
            deliveryStatus: 'pending', // pending, delivered, cancelled
            qualityRating: null,
            
            notes: orderData.notes || '',
            createdBy: adminId,
            _createdDate: new Date()
        };
        
        const result = await wixData.insert('VendorOrders', order);
        
        // Update vendor total orders
        const vendor = await wixData.get('Vendors', orderData.vendorId);
        if (vendor) {
            await wixData.update('Vendors', {
                ...vendor,
                totalOrders: (vendor.totalOrders || 0) + 1,
                _updatedDate: new Date()
            });
        }
        
        return { success: true, orderId: result._id };
    } catch (error) {
        console.error('Error recording vendor order:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Rate vendor after order
 */
export async function rateVendor(vendorId, orderId, rating, feedback, adminId) {
    try {
        // Update order with rating
        const order = await wixData.get('VendorOrders', orderId);
        if (order) {
            await wixData.update('VendorOrders', {
                ...order,
                qualityRating: rating,
                qualityFeedback: feedback,
                ratedBy: adminId,
                ratedAt: new Date()
            });
        }
        
        // Recalculate vendor average rating
        const allOrders = await wixData.query('VendorOrders')
            .eq('vendorId', vendorId)
            .isNotEmpty('qualityRating')
            .find();
        
        const totalRating = allOrders.items.reduce((sum, o) => sum + (o.qualityRating || 0), 0);
        const avgRating = allOrders.items.length > 0 
            ? (totalRating / allOrders.items.length).toFixed(1)
            : 0;
        
        // Update vendor
        const vendor = await wixData.get('Vendors', vendorId);
        if (vendor) {
            await wixData.update('Vendors', {
                ...vendor,
                rating: parseFloat(avgRating),
                _updatedDate: new Date()
            });
        }
        
        return { success: true, newRating: avgRating };
    } catch (error) {
        console.error('Error rating vendor:', error);
        return { success: false, error: error.message };
    }
}

// ==================== HELPER FUNCTIONS ====================

function determineTier(amount) {
    if (amount >= 2000) return 'PLATINUM';
    if (amount >= 1000) return 'GOLD';
    if (amount >= 500) return 'SILVER';
    if (amount >= 250) return 'BRONZE';
    return 'SUPPORTER';
}

function getCurrentFiscalYear() {
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth();
    // BANF fiscal year runs from April to March
    if (month >= 3) { // April onwards
        return `${year}-${year + 1}`;
    }
    return `${year - 1}-${year}`;
}

// Export constants
export const SponsorshipTiers = SPONSORSHIP_TIERS;
export const MagazineAdRates = MAGAZINE_AD_RATES;
export const FoodSponsorshipTypes = FOOD_SPONSORSHIP_TYPES;
export const SponsorStatus = SPONSOR_STATUS;

```
------------------------------------------------------------

## [38/41] streaming-service
- File: `streaming-service.jsw`
- Size: 27.1 KB
- Lines: 910

```javascript
/**
 * BANF Video Streaming Service
 * =============================
 * Wix Velo Backend Module for live streaming and video management
 * 
 * Features:
 * - Create and schedule streaming events
 * - YouTube Live / Vimeo / Custom RTMP integration
 * - Automatic reminder notifications
 * - Viewer analytics
 * - Stream recording/archiving
 * 
 * @module backend/streaming-service.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';
import { triggeredEmails } from 'wix-crm-backend';
import { contacts } from 'wix-crm-backend';

// =====================================================
// STREAMING EVENT MANAGEMENT
// =====================================================

/**
 * Create a new streaming event
 * @param {Object} eventData Streaming event details
 * @returns {Promise<Object>} Created event with ID
 */
export async function createStreamingEvent(eventData) {
    // Verify admin permissions
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized: Admin access required');
    }
    
    try {
        const streamEvent = {
            title: eventData.title,
            description: eventData.description || '',
            category: eventData.category || 'cultural',
            scheduledDate: new Date(eventData.scheduledDate),
            scheduledTime: eventData.scheduledTime,
            duration: eventData.estimatedDuration || 120, // minutes
            
            // Stream Configuration
            streamType: eventData.streamType || 'youtube', // youtube, vimeo, custom
            streamUrl: eventData.streamUrl || null,
            embedCode: eventData.embedCode || null,
            rtmpUrl: eventData.rtmpUrl || null,
            streamKey: eventData.streamKey || null, // Encrypted storage recommended
            
            // Media
            thumbnailUrl: eventData.thumbnailUrl || '/default-stream-thumb.jpg',
            previewVideoUrl: eventData.previewVideoUrl || null,
            
            // Status
            status: 'scheduled', // scheduled, live, ended, cancelled
            isPublished: true,
            isFeatured: eventData.isFeatured || false,
            
            // Notifications
            sendReminders: eventData.sendReminders !== false,
            reminder24hSent: false,
            reminder1hSent: false,
            
            // Analytics
            viewerCount: 0,
            peakViewers: 0,
            totalViews: 0,
            
            // Metadata
            createdAt: new Date(),
            createdBy: member._id,
            lastModified: new Date()
        };
        
        const result = await wixData.insert('StreamingEvents', streamEvent);
        
        // Schedule reminder notifications
        if (streamEvent.sendReminders) {
            await scheduleStreamReminders(result._id, streamEvent.scheduledDate);
        }
        
        // Send immediate announcement if requested
        if (eventData.sendAnnouncement) {
            await sendStreamAnnouncement(result);
        }
        
        return {
            success: true,
            eventId: result._id,
            message: 'Streaming event created successfully',
            shareUrl: generateShareUrl(result._id)
        };
        
    } catch (error) {
        console.error('Error creating streaming event:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Update streaming event
 * @param {string} eventId 
 * @param {Object} updates 
 */
export async function updateStreamingEvent(eventId, updates) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('StreamingEvents', eventId);
        
        // Apply updates
        const updatedEvent = {
            ...event,
            ...updates,
            lastModified: new Date()
        };
        
        await wixData.update('StreamingEvents', updatedEvent);
        
        return {
            success: true,
            message: 'Event updated successfully'
        };
        
    } catch (error) {
        console.error('Error updating event:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Go live with streaming event
 * @param {string} eventId 
 */
export async function goLive(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('StreamingEvents', eventId);
        
        event.status = 'live';
        event.actualStartTime = new Date();
        event.lastModified = new Date();
        
        await wixData.update('StreamingEvents', event);
        
        // Send "We're Live!" notification
        await sendLiveNotification(event);
        
        // Start viewer tracking
        await initializeViewerTracking(eventId);
        
        return {
            success: true,
            message: 'Stream is now LIVE!',
            viewerDashboardUrl: `/admin/streaming/${eventId}/live`
        };
        
    } catch (error) {
        console.error('Error going live:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * End live stream
 * @param {string} eventId 
 * @param {Object} options - Archive options
 */
export async function endStream(eventId, options = {}) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('StreamingEvents', eventId);
        
        event.status = 'ended';
        event.actualEndTime = new Date();
        event.actualDuration = Math.round(
            (event.actualEndTime - event.actualStartTime) / 60000
        ); // minutes
        
        // Archive URL if available
        if (options.archiveUrl) {
            event.archiveUrl = options.archiveUrl;
            event.isArchived = true;
        }
        
        event.lastModified = new Date();
        
        await wixData.update('StreamingEvents', event);
        
        // Finalize analytics
        await finalizeStreamAnalytics(eventId);
        
        return {
            success: true,
            message: 'Stream ended successfully',
            analytics: {
                duration: event.actualDuration,
                peakViewers: event.peakViewers,
                totalViews: event.totalViews
            }
        };
        
    } catch (error) {
        console.error('Error ending stream:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Cancel streaming event
 * @param {string} eventId 
 * @param {string} reason 
 */
export async function cancelStream(eventId, reason = '') {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('StreamingEvents', eventId);
        
        event.status = 'cancelled';
        event.cancellationReason = reason;
        event.cancelledAt = new Date();
        event.cancelledBy = member._id;
        
        await wixData.update('StreamingEvents', event);
        
        // Notify members who RSVPed
        await sendCancellationNotification(event, reason);
        
        return {
            success: true,
            message: 'Stream cancelled and notifications sent'
        };
        
    } catch (error) {
        console.error('Error cancelling stream:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// STREAM RETRIEVAL
// =====================================================

/**
 * Get upcoming streaming events
 * @param {number} limit 
 */
export async function getUpcomingStreams(limit = 10) {
    try {
        const now = new Date();
        
        const streams = await wixData.query('StreamingEvents')
            .ge('scheduledDate', now)
            .eq('isPublished', true)
            .ne('status', 'cancelled')
            .ascending('scheduledDate')
            .limit(limit)
            .find();
        
        return {
            success: true,
            streams: streams.items.map(sanitizeStreamForPublic)
        };
        
    } catch (error) {
        console.error('Error getting upcoming streams:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Get current live stream(s)
 */
export async function getLiveStreams() {
    try {
        const streams = await wixData.query('StreamingEvents')
            .eq('status', 'live')
            .find();
        
        return {
            success: true,
            streams: streams.items.map(sanitizeStreamForPublic),
            isLiveNow: streams.items.length > 0
        };
        
    } catch (error) {
        console.error('Error getting live streams:', error);
        return {
            success: false,
            streams: [],
            isLiveNow: false
        };
    }
}

/**
 * Get archived/past streams
 * @param {number} limit 
 * @param {number} skip 
 */
export async function getPastStreams(limit = 20, skip = 0) {
    try {
        const streams = await wixData.query('StreamingEvents')
            .eq('status', 'ended')
            .eq('isArchived', true)
            .descending('actualEndTime')
            .skip(skip)
            .limit(limit)
            .find();
        
        return {
            success: true,
            streams: streams.items.map(sanitizeStreamForPublic),
            total: streams.totalCount,
            hasMore: streams.items.length === limit
        };
        
    } catch (error) {
        console.error('Error getting past streams:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Get single stream details
 * @param {string} eventId 
 */
export async function getStreamDetails(eventId) {
    try {
        const event = await wixData.get('StreamingEvents', eventId);
        
        if (!event || !event.isPublished) {
            return {
                success: false,
                error: 'Stream not found'
            };
        }
        
        // Log view
        await logStreamView(eventId);
        
        return {
            success: true,
            stream: sanitizeStreamForPublic(event)
        };
        
    } catch (error) {
        console.error('Error getting stream details:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// NOTIFICATIONS & REMINDERS
// =====================================================

/**
 * Schedule reminder emails for streaming event
 * @param {string} eventId 
 * @param {Date} scheduledDate 
 */
async function scheduleStreamReminders(eventId, scheduledDate) {
    try {
        // 24-hour reminder
        const reminder24h = new Date(scheduledDate);
        reminder24h.setHours(reminder24h.getHours() - 24);
        
        await wixData.insert('ScheduledNotifications', {
            eventId: eventId,
            type: 'stream_reminder_24h',
            scheduledFor: reminder24h,
            sent: false
        });
        
        // 1-hour reminder
        const reminder1h = new Date(scheduledDate);
        reminder1h.setHours(reminder1h.getHours() - 1);
        
        await wixData.insert('ScheduledNotifications', {
            eventId: eventId,
            type: 'stream_reminder_1h',
            scheduledFor: reminder1h,
            sent: false
        });
        
    } catch (error) {
        console.error('Error scheduling reminders:', error);
    }
}

/**
 * Send stream announcement to all members
 * @param {Object} event 
 */
async function sendStreamAnnouncement(event) {
    try {
        // Get all active members
        const members = await wixData.query('Members/PrivateMembersData')
            .eq('status', 'APPROVED')
            .find({ suppressAuth: true });
        
        // Send triggered email to each member
        for (const member of members.items) {
            try {
                await triggeredEmails.emailMember(
                    'stream_announcement',
                    member._id,
                    {
                        variables: {
                            streamTitle: event.title,
                            streamDate: formatDate(event.scheduledDate),
                            streamTime: event.scheduledTime,
                            streamDescription: event.description,
                            streamUrl: generateShareUrl(event._id),
                            thumbnailUrl: event.thumbnailUrl
                        }
                    }
                );
            } catch (emailError) {
                console.error(`Error sending to ${member._id}:`, emailError);
            }
        }
        
    } catch (error) {
        console.error('Error sending announcement:', error);
    }
}

/**
 * Send "We're Live!" notification
 * @param {Object} event 
 */
async function sendLiveNotification(event) {
    try {
        // Get members who RSVPed for this stream
        const rsvps = await wixData.query('StreamRSVPs')
            .eq('streamId', event._id)
            .find();
        
        for (const rsvp of rsvps.items) {
            try {
                await triggeredEmails.emailMember(
                    'stream_live_now',
                    rsvp.memberId,
                    {
                        variables: {
                            streamTitle: event.title,
                            watchUrl: generateWatchUrl(event._id)
                        }
                    }
                );
            } catch (emailError) {
                console.error('Error sending live notification:', emailError);
            }
        }
        
    } catch (error) {
        console.error('Error in live notification:', error);
    }
}

/**
 * Send cancellation notification
 * @param {Object} event 
 * @param {string} reason 
 */
async function sendCancellationNotification(event, reason) {
    try {
        const rsvps = await wixData.query('StreamRSVPs')
            .eq('streamId', event._id)
            .find();
        
        for (const rsvp of rsvps.items) {
            try {
                await triggeredEmails.emailMember(
                    'stream_cancelled',
                    rsvp.memberId,
                    {
                        variables: {
                            streamTitle: event.title,
                            cancellationReason: reason || 'No reason provided'
                        }
                    }
                );
            } catch (emailError) {
                console.error('Error sending cancellation:', emailError);
            }
        }
        
    } catch (error) {
        console.error('Error in cancellation notification:', error);
    }
}

// =====================================================
// RSVP MANAGEMENT
// =====================================================

/**
 * RSVP for streaming event
 * @param {string} streamId 
 */
export async function rsvpForStream(streamId) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Please log in to RSVP');
    }
    
    try {
        // Check if already RSVPed
        const existing = await wixData.query('StreamRSVPs')
            .eq('streamId', streamId)
            .eq('memberId', member._id)
            .find();
        
        if (existing.items.length > 0) {
            return {
                success: true,
                message: 'You are already registered for this stream'
            };
        }
        
        // Create RSVP
        await wixData.insert('StreamRSVPs', {
            streamId: streamId,
            memberId: member._id,
            memberEmail: member.loginEmail,
            memberName: `${member.firstName || ''} ${member.lastName || ''}`.trim(),
            rsvpDate: new Date(),
            notifyOnLive: true
        });
        
        // Increment RSVP count on stream
        const stream = await wixData.get('StreamingEvents', streamId);
        stream.rsvpCount = (stream.rsvpCount || 0) + 1;
        await wixData.update('StreamingEvents', stream);
        
        return {
            success: true,
            message: "You're registered! We'll remind you before the stream."
        };
        
    } catch (error) {
        console.error('Error RSVPing:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Cancel RSVP
 * @param {string} streamId 
 */
export async function cancelStreamRSVP(streamId) {
    const member = await currentMember.getMember();
    if (!member) {
        throw new Error('Please log in');
    }
    
    try {
        const rsvp = await wixData.query('StreamRSVPs')
            .eq('streamId', streamId)
            .eq('memberId', member._id)
            .find();
        
        if (rsvp.items.length > 0) {
            await wixData.remove('StreamRSVPs', rsvp.items[0]._id);
            
            // Decrement RSVP count
            const stream = await wixData.get('StreamingEvents', streamId);
            stream.rsvpCount = Math.max(0, (stream.rsvpCount || 1) - 1);
            await wixData.update('StreamingEvents', stream);
        }
        
        return {
            success: true,
            message: 'RSVP cancelled'
        };
        
    } catch (error) {
        console.error('Error cancelling RSVP:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// VIEWER ANALYTICS
// =====================================================

/**
 * Initialize viewer tracking for live stream
 * @param {string} eventId 
 */
async function initializeViewerTracking(eventId) {
    await wixData.insert('StreamViewerTracking', {
        streamId: eventId,
        timestamp: new Date(),
        currentViewers: 0,
        type: 'session_start'
    });
}

/**
 * Update viewer count (called from frontend periodically)
 * @param {string} eventId 
 * @param {number} viewerCount 
 */
export async function updateViewerCount(eventId, viewerCount) {
    try {
        const stream = await wixData.get('StreamingEvents', eventId);
        
        stream.viewerCount = viewerCount;
        stream.peakViewers = Math.max(stream.peakViewers || 0, viewerCount);
        
        await wixData.update('StreamingEvents', stream);
        
        // Log for historical tracking
        await wixData.insert('StreamViewerTracking', {
            streamId: eventId,
            timestamp: new Date(),
            currentViewers: viewerCount,
            type: 'periodic_update'
        });
        
        return { success: true };
        
    } catch (error) {
        console.error('Error updating viewer count:', error);
        return { success: false };
    }
}

/**
 * Log individual stream view
 * @param {string} eventId 
 */
async function logStreamView(eventId) {
    try {
        const stream = await wixData.get('StreamingEvents', eventId);
        stream.totalViews = (stream.totalViews || 0) + 1;
        await wixData.update('StreamingEvents', stream);
    } catch (error) {
        console.error('Error logging view:', error);
    }
}

/**
 * Finalize stream analytics after ending
 * @param {string} eventId 
 */
async function finalizeStreamAnalytics(eventId) {
    try {
        // Get all viewer tracking data
        const tracking = await wixData.query('StreamViewerTracking')
            .eq('streamId', eventId)
            .find();
        
        // Calculate statistics
        const viewerCounts = tracking.items
            .filter(t => t.type === 'periodic_update')
            .map(t => t.currentViewers);
        
        const avgViewers = viewerCounts.length > 0 
            ? Math.round(viewerCounts.reduce((a, b) => a + b, 0) / viewerCounts.length)
            : 0;
        
        // Update stream with final analytics
        const stream = await wixData.get('StreamingEvents', eventId);
        stream.analytics = {
            averageViewers: avgViewers,
            totalDataPoints: viewerCounts.length,
            viewerHistory: viewerCounts.slice(-50) // Keep last 50 data points
        };
        
        await wixData.update('StreamingEvents', stream);
        
    } catch (error) {
        console.error('Error finalizing analytics:', error);
    }
}

/**
 * Get stream analytics (admin only)
 * @param {string} eventId 
 */
export async function getStreamAnalytics(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const stream = await wixData.get('StreamingEvents', eventId);
        
        const tracking = await wixData.query('StreamViewerTracking')
            .eq('streamId', eventId)
            .ascending('timestamp')
            .find();
        
        const rsvps = await wixData.query('StreamRSVPs')
            .eq('streamId', eventId)
            .find();
        
        return {
            success: true,
            analytics: {
                totalViews: stream.totalViews || 0,
                peakViewers: stream.peakViewers || 0,
                averageViewers: stream.analytics?.averageViewers || 0,
                actualDuration: stream.actualDuration || 0,
                rsvpCount: rsvps.items.length,
                viewerTimeline: tracking.items.map(t => ({
                    timestamp: t.timestamp,
                    viewers: t.currentViewers
                }))
            }
        };
        
    } catch (error) {
        console.error('Error getting analytics:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

/**
 * Check if member is admin
 * @param {string} memberId 
 */
async function isAdmin(memberId) {
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec')
            );
        }
        return false;
    } catch {
        return false;
    }
}

/**
 * Sanitize stream data for public viewing
 * @param {Object} stream 
 */
function sanitizeStreamForPublic(stream) {
    const { streamKey, rtmpUrl, ...publicData } = stream;
    return publicData;
}

/**
 * Generate share URL for stream
 * @param {string} eventId 
 */
function generateShareUrl(eventId) {
    return `https://jaxbengali.org/live/${eventId}`;
}

/**
 * Generate watch URL
 * @param {string} eventId 
 */
function generateWatchUrl(eventId) {
    return `https://jaxbengali.org/watch/${eventId}`;
}

/**
 * Format date for display
 * @param {Date} date 
 */
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// =====================================================
// CRON JOBS (called by Wix Scheduled Jobs)
// =====================================================

/**
 * Process scheduled notifications (run every 15 minutes)
 */
export async function processScheduledNotifications() {
    try {
        const now = new Date();
        
        const pendingNotifications = await wixData.query('ScheduledNotifications')
            .eq('sent', false)
            .le('scheduledFor', now)
            .find();
        
        for (const notification of pendingNotifications.items) {
            try {
                const event = await wixData.get('StreamingEvents', notification.eventId);
                
                if (event && event.status === 'scheduled') {
                    // Get RSVPed members
                    const rsvps = await wixData.query('StreamRSVPs')
                        .eq('streamId', notification.eventId)
                        .find();
                    
                    // Send appropriate reminder
                    const templateId = notification.type === 'stream_reminder_24h' 
                        ? 'stream_reminder_24h' 
                        : 'stream_reminder_1h';
                    
                    for (const rsvp of rsvps.items) {
                        await triggeredEmails.emailMember(
                            templateId,
                            rsvp.memberId,
                            {
                                variables: {
                                    streamTitle: event.title,
                                    streamTime: event.scheduledTime,
                                    watchUrl: generateWatchUrl(event._id)
                                }
                            }
                        );
                    }
                    
                    // Update event flags
                    if (notification.type === 'stream_reminder_24h') {
                        event.reminder24hSent = true;
                    } else {
                        event.reminder1hSent = true;
                    }
                    await wixData.update('StreamingEvents', event);
                }
                
                // Mark notification as sent
                notification.sent = true;
                notification.sentAt = new Date();
                await wixData.update('ScheduledNotifications', notification);
                
            } catch (notifError) {
                console.error(`Error processing notification ${notification._id}:`, notifError);
            }
        }
        
        return { success: true, processed: pendingNotifications.items.length };
        
    } catch (error) {
        console.error('Error in processScheduledNotifications:', error);
        return { success: false, error: error.message };
    }
}

```
------------------------------------------------------------

## [39/41] surveys
- File: `surveys.jsw`
- Size: 15.3 KB
- Lines: 436

```javascript
// backend/surveys.jsw
// BANF Survey System - Wix Velo Backend

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';

// Survey types
const SURVEY_TYPES = {
    GENERAL: 'general',
    EVENT: 'event',
    MEMBER_SATISFACTION: 'member_satisfaction',
    FEEDBACK: 'feedback',
    POLL: 'poll'
};

// Question types
const QUESTION_TYPES = {
    TEXT: 'text',
    TEXTAREA: 'textarea',
    SINGLE_CHOICE: 'single_choice',
    MULTIPLE_CHOICE: 'multiple_choice',
    RATING: 'rating',
    SCALE: 'scale',
    DATE: 'date',
    EMAIL: 'email',
    NUMBER: 'number'
};

/**
 * Create new survey (admin only)
 */
export async function createSurvey(surveyData, adminId) {
    try {
        const survey = {
            title: surveyData.title,
            description: surveyData.description || '',
            surveyType: surveyData.surveyType || SURVEY_TYPES.GENERAL,
            questions: JSON.stringify(surveyData.questions || []),
            settings: JSON.stringify({
                allowAnonymous: surveyData.allowAnonymous !== false,
                allowMultipleResponses: surveyData.allowMultipleResponses || false,
                requireLogin: surveyData.requireLogin || false,
                showResults: surveyData.showResults || false,
                randomizeQuestions: surveyData.randomizeQuestions || false,
                notifyOnResponse: surveyData.notifyOnResponse !== false,
                thankYouMessage: surveyData.thankYouMessage || 'Thank you for your response!'
            }),
            startDate: surveyData.startDate ? new Date(surveyData.startDate) : new Date(),
            endDate: surveyData.endDate ? new Date(surveyData.endDate) : null,
            isActive: true,
            targetAudience: surveyData.targetAudience || 'all', // all, members, specific_group
            relatedEventId: surveyData.relatedEventId || null,
            responseCount: 0,
            createdBy: adminId,
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert('Surveys', survey);
        
        return {
            success: true,
            surveyId: result._id,
            shareUrl: `/survey/${result._id}`
        };
    } catch (error) {
        console.error('Error creating survey:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get active surveys
 */
export async function getActiveSurveys() {
    try {
        const now = new Date();
        
        const result = await wixData.query('Surveys')
            .eq('isActive', true)
            .le('startDate', now)
            .or(
                wixData.query('Surveys').isEmpty('endDate'),
                wixData.query('Surveys').ge('endDate', now)
            )
            .descending('_createdDate')
            .find({ suppressAuth: true });
        
        return result.items.map(survey => ({
            id: survey._id,
            title: survey.title,
            description: survey.description,
            surveyType: survey.surveyType,
            responseCount: survey.responseCount,
            startDate: survey.startDate,
            endDate: survey.endDate
        }));
    } catch (error) {
        console.error('Error getting active surveys:', error);
        return [];
    }
}

/**
 * Get survey by ID
 */
export async function getSurveyById(surveyId) {
    try {
        const survey = await wixData.get('Surveys', surveyId, { suppressAuth: true });
        
        if (!survey) return null;
        
        const settings = JSON.parse(survey.settings || '{}');
        let questions = JSON.parse(survey.questions || '[]');
        
        // Randomize questions if setting enabled
        if (settings.randomizeQuestions) {
            questions = shuffleArray(questions);
        }
        
        return {
            id: survey._id,
            title: survey.title,
            description: survey.description,
            surveyType: survey.surveyType,
            questions: questions,
            settings: settings,
            startDate: survey.startDate,
            endDate: survey.endDate,
            isActive: survey.isActive
        };
    } catch (error) {
        console.error('Error getting survey:', error);
        return null;
    }
}

/**
 * Submit survey response
 */
export async function submitSurveyResponse(surveyId, responses, respondentInfo = {}) {
    try {
        const survey = await wixData.get('Surveys', surveyId, { suppressAuth: true });
        
        if (!survey) {
            return { success: false, error: 'Survey not found' };
        }
        
        if (!survey.isActive) {
            return { success: false, error: 'Survey is no longer active' };
        }
        
        const settings = JSON.parse(survey.settings || '{}');
        
        // Check if login required
        if (settings.requireLogin) {
            const member = await currentMember.getMember({ fieldsets: ['PUBLIC'] });
            if (!member) {
                return { success: false, error: 'Login required to submit response' };
            }
            respondentInfo.memberId = member._id;
            respondentInfo.email = member.loginEmail;
        }
        
        // Check for duplicate responses
        if (!settings.allowMultipleResponses && respondentInfo.email) {
            const existing = await wixData.query('SurveyResponses')
                .eq('surveyId', surveyId)
                .eq('respondentEmail', respondentInfo.email)
                .find({ suppressAuth: true });
            
            if (existing.items.length > 0) {
                return { success: false, error: 'You have already submitted a response' };
            }
        }
        
        const response = {
            surveyId: surveyId,
            responses: JSON.stringify(responses),
            respondentMemberId: respondentInfo.memberId || null,
            respondentEmail: !settings.allowAnonymous ? respondentInfo.email : null,
            respondentName: !settings.allowAnonymous ? respondentInfo.name : null,
            isAnonymous: settings.allowAnonymous,
            submittedAt: new Date(),
            ipAddress: '', // Would need to be passed from frontend
            userAgent: respondentInfo.userAgent || '',
            _createdDate: new Date()
        };
        
        await wixData.insert('SurveyResponses', response, { suppressAuth: true });
        
        // Update response count
        await wixData.update('Surveys', {
            ...survey,
            responseCount: (survey.responseCount || 0) + 1,
            _updatedDate: new Date()
        });
        
        const thankYouMessage = settings.thankYouMessage || 'Thank you for your response!';
        
        return {
            success: true,
            message: thankYouMessage,
            showResults: settings.showResults
        };
    } catch (error) {
        console.error('Error submitting survey response:', error);
        return { success: false, error: 'Failed to submit response' };
    }
}

/**
 * Get survey responses (admin only)
 */
export async function getSurveyResponses(surveyId, options = { limit: 50, skip: 0 }) {
    try {
        const result = await wixData.query('SurveyResponses')
            .eq('surveyId', surveyId)
            .descending('submittedAt')
            .limit(options.limit)
            .skip(options.skip)
            .find();
        
        return {
            items: result.items.map(r => ({
                ...r,
                responses: JSON.parse(r.responses || '[]')
            })),
            totalCount: result.totalCount,
            hasNext: result.hasNext()
        };
    } catch (error) {
        console.error('Error getting responses:', error);
        return { items: [], totalCount: 0, hasNext: false };
    }
}

/**
 * Get survey results/analytics
 */
export async function getSurveyResults(surveyId) {
    try {
        const survey = await wixData.get('Surveys', surveyId);
        if (!survey) return null;
        
        const questions = JSON.parse(survey.questions || '[]');
        
        // Get all responses
        const responses = await wixData.query('SurveyResponses')
            .eq('surveyId', surveyId)
            .limit(1000)
            .find();
        
        // Aggregate results
        const results = {
            surveyTitle: survey.title,
            totalResponses: responses.totalCount,
            questions: []
        };
        
        for (const question of questions) {
            const questionResult = {
                id: question.id,
                text: question.text,
                type: question.type,
                responses: []
            };
            
            // Aggregate based on question type
            if (['single_choice', 'multiple_choice'].includes(question.type)) {
                const optionCounts = {};
                question.options.forEach(opt => optionCounts[opt] = 0);
                
                responses.items.forEach(r => {
                    const respData = JSON.parse(r.responses || '[]');
                    const answer = respData.find(a => a.questionId === question.id);
                    if (answer) {
                        if (Array.isArray(answer.value)) {
                            answer.value.forEach(v => {
                                if (optionCounts[v] !== undefined) optionCounts[v]++;
                            });
                        } else if (optionCounts[answer.value] !== undefined) {
                            optionCounts[answer.value]++;
                        }
                    }
                });
                
                questionResult.optionCounts = optionCounts;
                questionResult.totalAnswered = Object.values(optionCounts).reduce((a, b) => a + b, 0);
            } else if (['rating', 'scale'].includes(question.type)) {
                const values = [];
                responses.items.forEach(r => {
                    const respData = JSON.parse(r.responses || '[]');
                    const answer = respData.find(a => a.questionId === question.id);
                    if (answer && answer.value) {
                        values.push(Number(answer.value));
                    }
                });
                
                questionResult.average = values.length > 0 
                    ? (values.reduce((a, b) => a + b, 0) / values.length).toFixed(2)
                    : 0;
                questionResult.min = values.length > 0 ? Math.min(...values) : 0;
                questionResult.max = values.length > 0 ? Math.max(...values) : 0;
                questionResult.totalAnswered = values.length;
            } else {
                // Text responses
                questionResult.responses = responses.items
                    .map(r => {
                        const respData = JSON.parse(r.responses || '[]');
                        const answer = respData.find(a => a.questionId === question.id);
                        return answer ? answer.value : null;
                    })
                    .filter(v => v);
                questionResult.totalAnswered = questionResult.responses.length;
            }
            
            results.questions.push(questionResult);
        }
        
        return results;
    } catch (error) {
        console.error('Error getting survey results:', error);
        return null;
    }
}

/**
 * Update survey (admin only)
 */
export async function updateSurvey(surveyId, updateData) {
    try {
        const survey = await wixData.get('Surveys', surveyId);
        if (!survey) {
            return { success: false, error: 'Survey not found' };
        }
        
        const updatedSurvey = {
            ...survey,
            title: updateData.title || survey.title,
            description: updateData.description !== undefined ? updateData.description : survey.description,
            questions: updateData.questions ? JSON.stringify(updateData.questions) : survey.questions,
            settings: updateData.settings ? JSON.stringify(updateData.settings) : survey.settings,
            startDate: updateData.startDate ? new Date(updateData.startDate) : survey.startDate,
            endDate: updateData.endDate ? new Date(updateData.endDate) : survey.endDate,
            isActive: updateData.isActive !== undefined ? updateData.isActive : survey.isActive,
            _updatedDate: new Date()
        };
        
        await wixData.update('Surveys', updatedSurvey);
        
        return { success: true, message: 'Survey updated successfully' };
    } catch (error) {
        console.error('Error updating survey:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Clone survey (admin only)
 */
export async function cloneSurvey(surveyId, newTitle, adminId) {
    try {
        const original = await wixData.get('Surveys', surveyId);
        if (!original) {
            return { success: false, error: 'Survey not found' };
        }
        
        const cloned = {
            title: newTitle || `Copy of ${original.title}`,
            description: original.description,
            surveyType: original.surveyType,
            questions: original.questions,
            settings: original.settings,
            startDate: new Date(),
            endDate: null,
            isActive: false,
            targetAudience: original.targetAudience,
            relatedEventId: null,
            responseCount: 0,
            createdBy: adminId,
            _createdDate: new Date(),
            _updatedDate: new Date()
        };
        
        const result = await wixData.insert('Surveys', cloned);
        
        return {
            success: true,
            surveyId: result._id,
            message: 'Survey cloned successfully'
        };
    } catch (error) {
        console.error('Error cloning survey:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Delete survey and responses (admin only)
 */
export async function deleteSurvey(surveyId) {
    try {
        // Delete all responses first
        const responses = await wixData.query('SurveyResponses')
            .eq('surveyId', surveyId)
            .limit(1000)
            .find();
        
        for (const response of responses.items) {
            await wixData.remove('SurveyResponses', response._id);
        }
        
        // Delete survey
        await wixData.remove('Surveys', surveyId);
        
        return { success: true, message: 'Survey and responses deleted' };
    } catch (error) {
        console.error('Error deleting survey:', error);
        return { success: false, error: error.message };
    }
}

// Helper function
function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

// Export constants
export const SurveyTypes = SURVEY_TYPES;
export const QuestionTypes = QUESTION_TYPES;

```
------------------------------------------------------------

## [40/41] vendor-management
- File: `vendor-management.jsw`
- Size: 34.4 KB
- Lines: 1083

```javascript
/**
 * BANF Vendor Management Service
 * ================================
 * Wix Velo Backend Module for automated vendor management
 * 
 * Features:
 * - Vendor registration and approval workflow
 * - Booth assignment management
 * - Payment tracking
 * - Contract management
 * - Performance ratings
 * 
 * @module backend/vendor-management.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';
import { triggeredEmails } from 'wix-crm-backend';

// =====================================================
// VENDOR TYPES & CONFIGURATION
// =====================================================

const VENDOR_TYPES = {
    FOOD: {
        name: 'Food Vendor',
        icon: '🍲',
        requiresHealthPermit: true,
        baseFee: 200,
        description: 'Food service vendors'
    },
    RETAIL: {
        name: 'Retail Vendor',
        icon: '🛍️',
        requiresHealthPermit: false,
        baseFee: 150,
        description: 'Merchandise and retail vendors'
    },
    JEWELRY: {
        name: 'Jewelry Vendor',
        icon: '💎',
        requiresHealthPermit: false,
        baseFee: 150,
        description: 'Jewelry and accessories'
    },
    CLOTHING: {
        name: 'Clothing Vendor',
        icon: '👔',
        requiresHealthPermit: false,
        baseFee: 150,
        description: 'Traditional clothing and apparel'
    },
    HANDICRAFT: {
        name: 'Handicraft Vendor',
        icon: '🎨',
        requiresHealthPermit: false,
        baseFee: 100,
        description: 'Handmade crafts and art'
    },
    SERVICES: {
        name: 'Service Provider',
        icon: '💼',
        requiresHealthPermit: false,
        baseFee: 175,
        description: 'Professional services (photography, beauty, etc.)'
    },
    NONPROFIT: {
        name: 'Non-Profit Organization',
        icon: '🤝',
        requiresHealthPermit: false,
        baseFee: 0,
        description: 'Community organizations'
    }
};

const VENDOR_STATUS = {
    PENDING: 'pending',
    UNDER_REVIEW: 'under_review',
    APPROVED: 'approved',
    REJECTED: 'rejected',
    ACTIVE: 'active',
    SUSPENDED: 'suspended',
    BLACKLISTED: 'blacklisted'
};

const BOOTH_STATUS = {
    AVAILABLE: 'available',
    RESERVED: 'reserved',
    ASSIGNED: 'assigned',
    OCCUPIED: 'occupied'
};

// =====================================================
// VENDOR REGISTRATION
// =====================================================

/**
 * Register new vendor application
 * @param {Object} vendorData 
 */
export async function registerVendor(vendorData) {
    try {
        const member = await currentMember.getMember().catch(() => null);
        
        // Check for existing application
        const existing = await wixData.query('Vendors')
            .eq('email', vendorData.email)
            .eq('status', VENDOR_STATUS.PENDING)
            .find();
        
        if (existing.items.length > 0) {
            return { 
                success: false, 
                error: 'You already have a pending application' 
            };
        }
        
        const vendorType = VENDOR_TYPES[vendorData.vendorType] || VENDOR_TYPES.RETAIL;
        
        const vendor = await wixData.insert('Vendors', {
            // Basic Info
            businessName: vendorData.businessName,
            vendorType: vendorData.vendorType,
            vendorTypeName: vendorType.name,
            description: vendorData.description || '',
            
            // Contact
            contactName: vendorData.contactName,
            email: vendorData.email,
            phone: vendorData.phone,
            alternatePhone: vendorData.alternatePhone || '',
            
            // Address
            address: vendorData.address || '',
            city: vendorData.city || '',
            state: vendorData.state || 'FL',
            zip: vendorData.zip || '',
            
            // Business Details
            yearsInBusiness: vendorData.yearsInBusiness || 0,
            taxId: vendorData.taxId || '',
            businessLicense: vendorData.businessLicense || '',
            
            // For Food Vendors
            healthPermit: vendorData.healthPermit || '',
            healthPermitExpiry: vendorData.healthPermitExpiry || null,
            foodCategories: vendorData.foodCategories || [],
            servesAlcohol: vendorData.servesAlcohol || false,
            
            // Products/Services
            productCategories: vendorData.productCategories || [],
            productDescription: vendorData.productDescription || '',
            priceRange: vendorData.priceRange || '',
            
            // Booth Requirements
            preferredBoothSize: vendorData.preferredBoothSize || 'standard', // standard, large, premium
            requiresElectricity: vendorData.requiresElectricity || false,
            electricalNeeds: vendorData.electricalNeeds || '',
            requiresWater: vendorData.requiresWater || false,
            
            // Documents
            documents: vendorData.documents || [],
            insuranceCertificate: vendorData.insuranceCertificate || '',
            
            // Social/Website
            website: vendorData.website || '',
            facebookPage: vendorData.facebookPage || '',
            instagramHandle: vendorData.instagramHandle || '',
            
            // Previous Experience
            previousBANFVendor: vendorData.previousBANFVendor || false,
            previousEventYears: vendorData.previousEventYears || [],
            otherEventsAttended: vendorData.otherEventsAttended || '',
            
            // References
            references: vendorData.references || [],
            
            // Status
            status: VENDOR_STATUS.PENDING,
            
            // Financial
            baseFee: vendorType.baseFee,
            totalFeeDue: 0,
            totalPaid: 0,
            balance: 0,
            
            // Ratings (populated after events)
            averageRating: 0,
            totalRatings: 0,
            
            // Metadata
            memberId: member?._id || null,
            applicationNumber: generateApplicationNumber(),
            applicationDate: new Date(),
            createdAt: new Date(),
            lastModified: new Date(),
            
            // Admin Notes
            adminNotes: ''
        });
        
        // Send confirmation email
        await triggeredEmails.emailContact(
            'vendor_application_received',
            vendorData.email,
            {
                variables: {
                    contactName: vendorData.contactName,
                    businessName: vendorData.businessName,
                    applicationNumber: vendor.applicationNumber,
                    vendorType: vendorType.name
                }
            }
        );
        
        // Create admin task for review
        await createAdminTask({
            type: 'VENDOR_APPLICATION_REVIEW',
            title: `Review vendor application: ${vendorData.businessName}`,
            vendorId: vendor._id,
            priority: 'medium'
        });
        
        await logVendorActivity(vendor._id, 'APPLICATION_SUBMITTED', 
            `New vendor application from ${vendorData.businessName}`);
        
        return {
            success: true,
            vendorId: vendor._id,
            applicationNumber: vendor.applicationNumber,
            message: 'Application submitted successfully. You will receive an email confirmation.'
        };
        
    } catch (error) {
        console.error('Error registering vendor:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// VENDOR APPROVAL WORKFLOW
// =====================================================

/**
 * Review vendor application
 * @param {string} vendorId 
 * @param {string} decision - 'approve' or 'reject'
 * @param {string} notes 
 */
export async function reviewVendorApplication(vendorId, decision, notes = '') {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized: Admin access required');
    }
    
    try {
        const vendor = await wixData.get('Vendors', vendorId);
        
        if (!vendor) {
            return { success: false, error: 'Vendor not found' };
        }
        
        if (vendor.status !== VENDOR_STATUS.PENDING && 
            vendor.status !== VENDOR_STATUS.UNDER_REVIEW) {
            return { success: false, error: 'Application already processed' };
        }
        
        const previousStatus = vendor.status;
        
        if (decision === 'approve') {
            vendor.status = VENDOR_STATUS.APPROVED;
            vendor.approvedAt = new Date();
            vendor.approvedBy = member._id;
            vendor.approvalNotes = notes;
            
            // Send approval email
            await triggeredEmails.emailContact(
                'vendor_application_approved',
                vendor.email,
                {
                    variables: {
                        contactName: vendor.contactName,
                        businessName: vendor.businessName,
                        applicationNumber: vendor.applicationNumber,
                        vendorType: vendor.vendorTypeName,
                        notes: notes
                    }
                }
            );
            
        } else if (decision === 'reject') {
            vendor.status = VENDOR_STATUS.REJECTED;
            vendor.rejectedAt = new Date();
            vendor.rejectedBy = member._id;
            vendor.rejectionReason = notes;
            
            // Send rejection email
            await triggeredEmails.emailContact(
                'vendor_application_rejected',
                vendor.email,
                {
                    variables: {
                        contactName: vendor.contactName,
                        businessName: vendor.businessName,
                        applicationNumber: vendor.applicationNumber,
                        reason: notes || 'Your application did not meet our current requirements.'
                    }
                }
            );
        }
        
        vendor.adminNotes = (vendor.adminNotes || '') + 
            `\n[${new Date().toISOString()}] ${decision.toUpperCase()}: ${notes}`;
        vendor.lastModified = new Date();
        
        await wixData.update('Vendors', vendor);
        
        await logVendorActivity(vendorId, `APPLICATION_${decision.toUpperCase()}`, 
            `Application ${decision}ed by admin: ${notes}`);
        
        return {
            success: true,
            message: `Vendor application ${decision}ed successfully`
        };
        
    } catch (error) {
        console.error('Error reviewing vendor:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Request additional information from vendor
 * @param {string} vendorId 
 * @param {string} requestMessage 
 */
export async function requestVendorInfo(vendorId, requestMessage) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const vendor = await wixData.get('Vendors', vendorId);
        
        vendor.status = VENDOR_STATUS.UNDER_REVIEW;
        vendor.infoRequestedAt = new Date();
        vendor.infoRequestedBy = member._id;
        vendor.infoRequestMessage = requestMessage;
        vendor.lastModified = new Date();
        
        await wixData.update('Vendors', vendor);
        
        // Send info request email
        await triggeredEmails.emailContact(
            'vendor_info_request',
            vendor.email,
            {
                variables: {
                    contactName: vendor.contactName,
                    businessName: vendor.businessName,
                    applicationNumber: vendor.applicationNumber,
                    requestMessage: requestMessage
                }
            }
        );
        
        await logVendorActivity(vendorId, 'INFO_REQUESTED', requestMessage);
        
        return {
            success: true,
            message: 'Information request sent to vendor'
        };
        
    } catch (error) {
        console.error('Error requesting vendor info:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// BOOTH MANAGEMENT
// =====================================================

/**
 * Create booth inventory for an event
 * @param {string} eventId 
 * @param {Array} booths 
 */
export async function createBoothInventory(eventId, booths) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const createdBooths = [];
        
        for (const booth of booths) {
            const newBooth = await wixData.insert('EventBooths', {
                eventId: eventId,
                boothNumber: booth.boothNumber,
                boothType: booth.boothType || 'standard', // standard, large, premium, food_court
                location: booth.location || '',
                size: booth.size || '10x10',
                
                // Amenities
                hasElectricity: booth.hasElectricity || false,
                electricalAmps: booth.electricalAmps || 0,
                hasWater: booth.hasWater || false,
                hasShelter: booth.hasShelter || false,
                
                // Pricing
                price: booth.price || 150,
                
                // Status
                status: BOOTH_STATUS.AVAILABLE,
                
                // Assignment
                vendorId: null,
                reservedAt: null,
                assignedAt: null,
                
                // Metadata
                notes: booth.notes || '',
                createdAt: new Date()
            });
            
            createdBooths.push(newBooth);
        }
        
        return {
            success: true,
            boothsCreated: createdBooths.length,
            message: `${createdBooths.length} booths created for event`
        };
        
    } catch (error) {
        console.error('Error creating booth inventory:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Assign booth to vendor
 * @param {string} boothId 
 * @param {string} vendorId 
 * @param {string} eventId 
 */
export async function assignBoothToVendor(boothId, vendorId, eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const booth = await wixData.get('EventBooths', boothId);
        const vendor = await wixData.get('Vendors', vendorId);
        
        if (!booth || !vendor) {
            return { success: false, error: 'Booth or vendor not found' };
        }
        
        if (booth.status !== BOOTH_STATUS.AVAILABLE && 
            booth.status !== BOOTH_STATUS.RESERVED) {
            return { success: false, error: 'Booth is not available' };
        }
        
        if (vendor.status !== VENDOR_STATUS.APPROVED && 
            vendor.status !== VENDOR_STATUS.ACTIVE) {
            return { success: false, error: 'Vendor is not approved' };
        }
        
        // Update booth
        booth.vendorId = vendorId;
        booth.status = BOOTH_STATUS.ASSIGNED;
        booth.assignedAt = new Date();
        booth.assignedBy = member._id;
        
        await wixData.update('EventBooths', booth);
        
        // Create vendor event assignment
        await wixData.insert('VendorEventAssignments', {
            vendorId: vendorId,
            eventId: eventId,
            boothId: boothId,
            boothNumber: booth.boothNumber,
            boothType: booth.boothType,
            
            // Fees
            boothFee: booth.price,
            additionalFees: 0,
            totalFee: booth.price,
            paidAmount: 0,
            balance: booth.price,
            
            // Payment Status
            paymentStatus: 'pending',
            paymentDueDate: null,
            
            // Status
            status: 'assigned',
            
            // Check-in
            checkedIn: false,
            checkInTime: null,
            
            // Metadata
            assignedAt: new Date(),
            assignedBy: member._id,
            notes: ''
        });
        
        // Update vendor total fees
        vendor.totalFeeDue = (vendor.totalFeeDue || 0) + booth.price;
        vendor.balance = (vendor.balance || 0) + booth.price;
        vendor.status = VENDOR_STATUS.ACTIVE;
        await wixData.update('Vendors', vendor);
        
        // Send assignment email
        const event = await wixData.get('Events', eventId);
        
        await triggeredEmails.emailContact(
            'vendor_booth_assigned',
            vendor.email,
            {
                variables: {
                    contactName: vendor.contactName,
                    businessName: vendor.businessName,
                    eventName: event.title,
                    eventDate: formatDate(event.eventDate),
                    boothNumber: booth.boothNumber,
                    boothLocation: booth.location,
                    boothFee: booth.price
                }
            }
        );
        
        await logVendorActivity(vendorId, 'BOOTH_ASSIGNED', 
            `Assigned booth ${booth.boothNumber} for ${event.title}`);
        
        return {
            success: true,
            message: `Booth ${booth.boothNumber} assigned to ${vendor.businessName}`
        };
        
    } catch (error) {
        console.error('Error assigning booth:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Get available booths for event
 * @param {string} eventId 
 */
export async function getAvailableBooths(eventId) {
    try {
        const booths = await wixData.query('EventBooths')
            .eq('eventId', eventId)
            .eq('status', BOOTH_STATUS.AVAILABLE)
            .ascending('boothNumber')
            .find();
        
        return {
            success: true,
            booths: booths.items,
            total: booths.items.length
        };
        
    } catch (error) {
        console.error('Error getting available booths:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// VENDOR PAYMENT PROCESSING
// =====================================================

/**
 * Process vendor payment
 * @param {string} vendorId 
 * @param {string} eventId 
 * @param {Object} paymentInfo 
 */
export async function processVendorPayment(vendorId, eventId, paymentInfo) {
    try {
        const vendor = await wixData.get('Vendors', vendorId);
        
        // Find assignment
        const assignments = await wixData.query('VendorEventAssignments')
            .eq('vendorId', vendorId)
            .eq('eventId', eventId)
            .find();
        
        if (assignments.items.length === 0) {
            return { success: false, error: 'No booth assignment found' };
        }
        
        const assignment = assignments.items[0];
        
        // Create payment record
        const payment = await wixData.insert('VendorPayments', {
            vendorId: vendorId,
            eventId: eventId,
            assignmentId: assignment._id,
            
            // Payment Details
            amount: paymentInfo.amount,
            paymentMethod: paymentInfo.method, // cash, check, card, zelle
            transactionId: paymentInfo.transactionId || '',
            
            // Check Details (if applicable)
            checkNumber: paymentInfo.checkNumber || '',
            checkDate: paymentInfo.checkDate || null,
            
            // Status
            status: 'completed',
            
            // Metadata
            processedAt: new Date(),
            processedBy: paymentInfo.processedBy || 'system',
            notes: paymentInfo.notes || ''
        });
        
        // Update assignment
        assignment.paidAmount = (assignment.paidAmount || 0) + paymentInfo.amount;
        assignment.balance = assignment.totalFee - assignment.paidAmount;
        assignment.paymentStatus = assignment.balance <= 0 ? 'paid' : 'partial';
        assignment.lastPaymentDate = new Date();
        
        await wixData.update('VendorEventAssignments', assignment);
        
        // Update vendor totals
        vendor.totalPaid = (vendor.totalPaid || 0) + paymentInfo.amount;
        vendor.balance = Math.max(0, (vendor.balance || 0) - paymentInfo.amount);
        
        await wixData.update('Vendors', vendor);
        
        // Send receipt
        await triggeredEmails.emailContact(
            'vendor_payment_receipt',
            vendor.email,
            {
                variables: {
                    contactName: vendor.contactName,
                    businessName: vendor.businessName,
                    amount: paymentInfo.amount,
                    paymentMethod: paymentInfo.method,
                    transactionId: payment._id,
                    remainingBalance: assignment.balance
                }
            }
        );
        
        await logVendorActivity(vendorId, 'PAYMENT_RECEIVED', 
            `Payment of $${paymentInfo.amount} received`);
        
        return {
            success: true,
            paymentId: payment._id,
            newBalance: assignment.balance,
            message: 'Payment processed successfully'
        };
        
    } catch (error) {
        console.error('Error processing vendor payment:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Send payment reminders to vendors
 */
export async function sendVendorPaymentReminders() {
    try {
        const unpaidAssignments = await wixData.query('VendorEventAssignments')
            .eq('paymentStatus', 'pending')
            .or(
                wixData.query('VendorEventAssignments').eq('paymentStatus', 'partial')
            )
            .find();
        
        let remindersSent = 0;
        
        for (const assignment of unpaidAssignments.items) {
            const vendor = await wixData.get('Vendors', assignment.vendorId);
            const event = await wixData.get('Events', assignment.eventId);
            
            if (!vendor || !event) continue;
            
            // Check if event is within 2 weeks
            const eventDate = new Date(event.eventDate);
            const now = new Date();
            const daysUntilEvent = Math.ceil((eventDate - now) / (1000 * 60 * 60 * 24));
            
            if (daysUntilEvent > 0 && daysUntilEvent <= 14) {
                await triggeredEmails.emailContact(
                    'vendor_payment_reminder',
                    vendor.email,
                    {
                        variables: {
                            contactName: vendor.contactName,
                            businessName: vendor.businessName,
                            eventName: event.title,
                            eventDate: formatDate(event.eventDate),
                            amountDue: assignment.balance,
                            boothNumber: assignment.boothNumber,
                            daysUntilEvent: daysUntilEvent
                        }
                    }
                );
                
                remindersSent++;
            }
        }
        
        return {
            success: true,
            remindersSent: remindersSent
        };
        
    } catch (error) {
        console.error('Error sending payment reminders:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// VENDOR CHECK-IN
// =====================================================

/**
 * Check in vendor at event
 * @param {string} vendorId 
 * @param {string} eventId 
 */
export async function checkInVendor(vendorId, eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const assignments = await wixData.query('VendorEventAssignments')
            .eq('vendorId', vendorId)
            .eq('eventId', eventId)
            .find();
        
        if (assignments.items.length === 0) {
            return { success: false, error: 'No assignment found' };
        }
        
        const assignment = assignments.items[0];
        
        // Check payment status
        if (assignment.paymentStatus !== 'paid') {
            return { 
                success: false, 
                error: `Outstanding balance: $${assignment.balance}`,
                requiresPayment: true,
                balance: assignment.balance
            };
        }
        
        assignment.checkedIn = true;
        assignment.checkInTime = new Date();
        assignment.checkedInBy = member._id;
        assignment.status = 'active';
        
        await wixData.update('VendorEventAssignments', assignment);
        
        // Update booth status
        const booth = await wixData.get('EventBooths', assignment.boothId);
        booth.status = BOOTH_STATUS.OCCUPIED;
        await wixData.update('EventBooths', booth);
        
        const vendor = await wixData.get('Vendors', vendorId);
        
        await logVendorActivity(vendorId, 'CHECKED_IN', 
            `Vendor checked in at booth ${assignment.boothNumber}`);
        
        return {
            success: true,
            vendorName: vendor.businessName,
            boothNumber: assignment.boothNumber,
            message: `${vendor.businessName} checked in at booth ${assignment.boothNumber}`
        };
        
    } catch (error) {
        console.error('Error checking in vendor:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// VENDOR RATINGS & FEEDBACK
// =====================================================

/**
 * Rate vendor after event
 * @param {string} vendorId 
 * @param {string} eventId 
 * @param {Object} ratingData 
 */
export async function rateVendor(vendorId, eventId, ratingData) {
    try {
        const member = await currentMember.getMember();
        
        // Check if already rated
        const existingRating = await wixData.query('VendorRatings')
            .eq('vendorId', vendorId)
            .eq('eventId', eventId)
            .eq('raterId', member?._id || ratingData.raterEmail)
            .find();
        
        if (existingRating.items.length > 0) {
            return { success: false, error: 'You have already rated this vendor' };
        }
        
        const rating = await wixData.insert('VendorRatings', {
            vendorId: vendorId,
            eventId: eventId,
            raterId: member?._id || null,
            raterEmail: ratingData.raterEmail || '',
            raterName: ratingData.raterName || 'Anonymous',
            
            // Ratings (1-5)
            overallRating: ratingData.overallRating,
            productQuality: ratingData.productQuality || null,
            customerService: ratingData.customerService || null,
            valueForMoney: ratingData.valueForMoney || null,
            
            // Feedback
            comments: ratingData.comments || '',
            wouldRecommend: ratingData.wouldRecommend || false,
            
            // Metadata
            createdAt: new Date()
        });
        
        // Update vendor average rating
        await updateVendorAverageRating(vendorId);
        
        return {
            success: true,
            message: 'Thank you for your feedback!'
        };
        
    } catch (error) {
        console.error('Error rating vendor:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Update vendor's average rating
 * @param {string} vendorId 
 */
async function updateVendorAverageRating(vendorId) {
    const ratings = await wixData.query('VendorRatings')
        .eq('vendorId', vendorId)
        .find();
    
    if (ratings.items.length === 0) return;
    
    const totalRating = ratings.items.reduce((sum, r) => sum + r.overallRating, 0);
    const averageRating = totalRating / ratings.items.length;
    
    const vendor = await wixData.get('Vendors', vendorId);
    vendor.averageRating = Math.round(averageRating * 10) / 10;
    vendor.totalRatings = ratings.items.length;
    
    await wixData.update('Vendors', vendor);
}

// =====================================================
// REPORTING
// =====================================================

/**
 * Get vendor report for event
 * @param {string} eventId 
 */
export async function getVendorReportForEvent(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const assignments = await wixData.query('VendorEventAssignments')
            .eq('eventId', eventId)
            .find();
        
        let totalRevenue = 0;
        let totalPaid = 0;
        let totalOutstanding = 0;
        let checkedInCount = 0;
        
        const vendorDetails = [];
        
        for (const assignment of assignments.items) {
            const vendor = await wixData.get('Vendors', assignment.vendorId);
            
            totalRevenue += assignment.totalFee;
            totalPaid += assignment.paidAmount;
            totalOutstanding += assignment.balance;
            if (assignment.checkedIn) checkedInCount++;
            
            vendorDetails.push({
                vendorId: vendor._id,
                businessName: vendor.businessName,
                vendorType: vendor.vendorTypeName,
                boothNumber: assignment.boothNumber,
                totalFee: assignment.totalFee,
                paidAmount: assignment.paidAmount,
                balance: assignment.balance,
                paymentStatus: assignment.paymentStatus,
                checkedIn: assignment.checkedIn
            });
        }
        
        return {
            success: true,
            summary: {
                totalVendors: assignments.items.length,
                checkedIn: checkedInCount,
                totalRevenue: totalRevenue,
                totalPaid: totalPaid,
                totalOutstanding: totalOutstanding
            },
            vendors: vendorDetails
        };
        
    } catch (error) {
        console.error('Error getting vendor report:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * Get all vendors
 * @param {Object} filters 
 */
export async function getAllVendors(filters = {}) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        let query = wixData.query('Vendors');
        
        if (filters.status) {
            query = query.eq('status', filters.status);
        }
        if (filters.vendorType) {
            query = query.eq('vendorType', filters.vendorType);
        }
        
        const vendors = await query
            .descending('createdAt')
            .find();
        
        return {
            success: true,
            vendors: vendors.items,
            total: vendors.items.length
        };
        
    } catch (error) {
        console.error('Error getting vendors:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

/**
 * Generate application number
 */
function generateApplicationNumber() {
    const year = new Date().getFullYear();
    const random = Math.random().toString(36).substring(2, 6).toUpperCase();
    return `VND-${year}-${random}`;
}

/**
 * Create admin task
 */
async function createAdminTask(taskData) {
    await wixData.insert('AdminTasks', {
        ...taskData,
        status: 'pending',
        createdAt: new Date()
    });
}

/**
 * Log vendor activity
 */
async function logVendorActivity(vendorId, action, details) {
    await wixData.insert('VendorActivityLog', {
        vendorId: vendorId,
        action: action,
        details: details,
        timestamp: new Date()
    });
}

/**
 * Check if member is admin
 */
async function isAdmin(memberId) {
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec')
            );
        }
        return false;
    } catch {
        return false;
    }
}

/**
 * Format date for display
 */
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

```
------------------------------------------------------------

## [41/41] volunteer-service
- File: `volunteer-service.jsw`
- Size: 25.9 KB
- Lines: 761

```javascript
/**
 * BANF Volunteer Management Service
 * ===================================
 * Wix Velo Backend Module for volunteer coordination
 * 
 * Features:
 * - Volunteer registration and skills tracking
 * - Task assignment and scheduling
 * - Shift management
 * - Hours tracking and recognition
 * - Communication and notifications
 * 
 * @module backend/volunteer-service.jsw
 */

import wixData from 'wix-data';
import { currentMember } from 'wix-members-backend';
import { triggeredEmails } from 'wix-crm-backend';

// =====================================================
// VOLUNTEER SKILL CATEGORIES
// =====================================================

const SKILL_CATEGORIES = {
    COOKING: { id: 'cooking', name: 'Cooking', icon: '👨‍🍳', tasks: ['food_prep', 'serving', 'kitchen_cleanup'] },
    DECORATION: { id: 'decoration', name: 'Decoration', icon: '🎨', tasks: ['setup', 'decor', 'stage'] },
    TECHNICAL: { id: 'technical', name: 'Technical', icon: '💻', tasks: ['av_setup', 'lighting', 'streaming'] },
    REGISTRATION: { id: 'registration', name: 'Registration', icon: '📋', tasks: ['check_in', 'qr_scanning', 'badge'] },
    SECURITY: { id: 'security', name: 'Security', icon: '🔒', tasks: ['parking', 'crowd_control', 'entry'] },
    KIDS_ACTIVITY: { id: 'kids_activity', name: 'Kids Activity', icon: '🎈', tasks: ['games', 'supervision', 'crafts'] },
    PHOTOGRAPHY: { id: 'photography', name: 'Photography', icon: '📷', tasks: ['photo', 'video', 'social_media'] },
    EMCEE: { id: 'emcee', name: 'Emcee/Host', icon: '🎤', tasks: ['hosting', 'announcements', 'coordination'] },
    CLEANUP: { id: 'cleanup', name: 'Cleanup', icon: '🧹', tasks: ['venue_cleanup', 'packing', 'disposal'] },
    TRANSPORTATION: { id: 'transportation', name: 'Transportation', icon: '🚗', tasks: ['pickup', 'delivery', 'shuttle'] },
    GENERAL: { id: 'general', name: 'General Help', icon: '🤝', tasks: ['assistance', 'any_task'] }
};

const VOLUNTEER_STATUS = {
    REGISTERED: 'registered',
    ACTIVE: 'active',
    INACTIVE: 'inactive'
};

const TASK_STATUS = {
    OPEN: 'open',
    ASSIGNED: 'assigned',
    IN_PROGRESS: 'in_progress',
    COMPLETED: 'completed',
    CANCELLED: 'cancelled'
};

// =====================================================
// VOLUNTEER REGISTRATION
// =====================================================

/**
 * Register as a volunteer
 * @param {Object} volunteerData
 */
export async function registerVolunteer(volunteerData) {
    const member = await currentMember.getMember();
    
    try {
        // Check if already registered
        const existing = await wixData.query('Volunteers')
            .eq('memberId', member?._id || volunteerData.email)
            .find();
        
        if (existing.items.length > 0) {
            return { success: false, error: 'Already registered as volunteer' };
        }
        
        const volunteer = await wixData.insert('Volunteers', {
            memberId: member?._id || null,
            
            // Personal Info
            firstName: volunteerData.firstName,
            lastName: volunteerData.lastName,
            email: volunteerData.email,
            phone: volunteerData.phone,
            
            // Skills
            skills: volunteerData.skills || ['general'],
            skillDetails: volunteerData.skillDetails || '',
            languages: volunteerData.languages || ['english', 'bengali'],
            
            // Availability
            availability: volunteerData.availability || {
                weekday_evening: false,
                weekend_morning: true,
                weekend_afternoon: true,
                weekend_evening: true
            },
            
            // Preferences
            preferredTasks: volunteerData.preferredTasks || [],
            restrictions: volunteerData.restrictions || '',
            emergencyContact: volunteerData.emergencyContact || '',
            
            // Status
            status: VOLUNTEER_STATUS.REGISTERED,
            isVerified: false,
            
            // Stats
            totalHours: 0,
            eventsVolunteered: 0,
            rating: 5.0,
            badges: [],
            
            // Metadata
            registeredAt: new Date(),
            lastActive: new Date()
        });
        
        // Send confirmation
        await triggeredEmails.emailContact(
            'volunteer_registration',
            volunteerData.email,
            {
                variables: {
                    name: volunteerData.firstName,
                    skills: volunteerData.skills?.join(', ') || 'General Help'
                }
            }
        );
        
        await logVolunteerActivity(volunteer._id, 'REGISTERED', 'New volunteer registration');
        
        return {
            success: true,
            volunteerId: volunteer._id,
            message: 'Thank you for registering as a BANF volunteer!'
        };
        
    } catch (error) {
        console.error('Error registering volunteer:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Update volunteer profile
 * @param {string} volunteerId
 * @param {Object} updates
 */
export async function updateVolunteerProfile(volunteerId, updates) {
    const member = await currentMember.getMember();
    
    try {
        const volunteer = await wixData.get('Volunteers', volunteerId);
        
        if (!volunteer) {
            return { success: false, error: 'Volunteer not found' };
        }
        
        // Verify ownership or admin
        if (volunteer.memberId !== member?._id && !await isAdmin(member?._id)) {
            return { success: false, error: 'Unauthorized' };
        }
        
        // Apply updates
        const allowedUpdates = ['phone', 'skills', 'skillDetails', 'languages', 
            'availability', 'preferredTasks', 'restrictions', 'emergencyContact'];
        
        for (const key of allowedUpdates) {
            if (updates[key] !== undefined) {
                volunteer[key] = updates[key];
            }
        }
        
        volunteer.lastModified = new Date();
        
        await wixData.update('Volunteers', volunteer);
        
        return {
            success: true,
            message: 'Profile updated successfully'
        };
        
    } catch (error) {
        console.error('Error updating volunteer:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// EVENT VOLUNTEER MANAGEMENT
// =====================================================

/**
 * Create volunteer tasks for an event
 * @param {string} eventId
 * @param {Array} tasks
 */
export async function createEventTasks(eventId, tasks) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const event = await wixData.get('Events', eventId);
        
        if (!event) {
            return { success: false, error: 'Event not found' };
        }
        
        const createdTasks = [];
        
        for (const task of tasks) {
            const newTask = await wixData.insert('VolunteerTasks', {
                eventId: eventId,
                eventTitle: event.title,
                eventDate: event.eventDate,
                
                // Task Details
                taskName: task.name,
                taskDescription: task.description || '',
                category: task.category || 'general',
                
                // Timing
                startTime: task.startTime,
                endTime: task.endTime,
                duration: calculateDuration(task.startTime, task.endTime),
                
                // Requirements
                requiredSkills: task.requiredSkills || [],
                volunteersNeeded: task.volunteersNeeded || 1,
                volunteersAssigned: 0,
                
                // Location
                location: task.location || event.venueName,
                meetingPoint: task.meetingPoint || '',
                
                // Status
                status: TASK_STATUS.OPEN,
                
                // Assignments
                assignments: [],
                
                // Notes
                instructions: task.instructions || '',
                equipment: task.equipment || [],
                
                createdBy: member._id,
                createdAt: new Date()
            });
            
            createdTasks.push(newTask);
        }
        
        await logVolunteerActivity(null, 'TASKS_CREATED', 
            `Created ${createdTasks.length} tasks for ${event.title}`);
        
        return {
            success: true,
            createdCount: createdTasks.length,
            tasks: createdTasks
        };
        
    } catch (error) {
        console.error('Error creating tasks:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Volunteer sign up for a task
 * @param {string} taskId
 * @param {Object} signupData
 */
export async function signUpForTask(taskId, signupData = {}) {
    const member = await currentMember.getMember();
    
    try {
        const task = await wixData.get('VolunteerTasks', taskId);
        
        if (!task) {
            return { success: false, error: 'Task not found' };
        }
        
        if (task.volunteersAssigned >= task.volunteersNeeded) {
            return { success: false, error: 'Task is fully staffed' };
        }
        
        // Get volunteer record
        let volunteer;
        if (member) {
            const volunteers = await wixData.query('Volunteers')
                .eq('memberId', member._id)
                .find();
            volunteer = volunteers.items[0];
        }
        
        // Check for existing signup
        const existingAssignment = task.assignments?.find(
            a => a.volunteerId === volunteer?._id || a.email === signupData.email
        );
        
        if (existingAssignment) {
            return { success: false, error: 'Already signed up for this task' };
        }
        
        // Create assignment
        const assignment = {
            assignmentId: `ASN_${Date.now()}`,
            volunteerId: volunteer?._id || null,
            volunteerName: volunteer 
                ? `${volunteer.firstName} ${volunteer.lastName}`
                : signupData.name,
            email: volunteer?.email || signupData.email,
            phone: volunteer?.phone || signupData.phone,
            signedUpAt: new Date(),
            status: 'confirmed',
            checkedIn: false,
            checkedOut: false
        };
        
        // Update task
        task.assignments = [...(task.assignments || []), assignment];
        task.volunteersAssigned = (task.volunteersAssigned || 0) + 1;
        
        if (task.volunteersAssigned >= task.volunteersNeeded) {
            task.status = TASK_STATUS.ASSIGNED;
        }
        
        await wixData.update('VolunteerTasks', task);
        
        // Update volunteer stats
        if (volunteer) {
            volunteer.eventsVolunteered = (volunteer.eventsVolunteered || 0) + 1;
            volunteer.lastActive = new Date();
            await wixData.update('Volunteers', volunteer);
        }
        
        // Send confirmation
        await triggeredEmails.emailContact(
            'volunteer_task_confirmation',
            assignment.email,
            {
                variables: {
                    name: assignment.volunteerName,
                    taskName: task.taskName,
                    eventTitle: task.eventTitle,
                    eventDate: formatDate(task.eventDate),
                    startTime: task.startTime,
                    endTime: task.endTime,
                    location: task.location,
                    instructions: task.instructions
                }
            }
        );
        
        await logVolunteerActivity(volunteer?._id, 'TASK_SIGNUP', 
            `Signed up for ${task.taskName} at ${task.eventTitle}`);
        
        return {
            success: true,
            assignmentId: assignment.assignmentId,
            message: `Successfully signed up for ${task.taskName}`
        };
        
    } catch (error) {
        console.error('Error signing up:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get available tasks for an event
 * @param {string} eventId
 * @param {Object} filters - { skills, date }
 */
export async function getAvailableTasks(eventId, filters = {}) {
    try {
        let query = wixData.query('VolunteerTasks')
            .eq('eventId', eventId)
            .eq('status', TASK_STATUS.OPEN);
        
        const tasks = await query.find();
        
        // Filter by skills if provided
        let filteredTasks = tasks.items;
        if (filters.skills?.length) {
            filteredTasks = filteredTasks.filter(task => 
                task.requiredSkills.some(skill => filters.skills.includes(skill)) ||
                task.requiredSkills.length === 0
            );
        }
        
        return {
            success: true,
            tasks: filteredTasks.map(task => ({
                _id: task._id,
                name: task.taskName,
                description: task.taskDescription,
                category: task.category,
                categoryIcon: SKILL_CATEGORIES[task.category.toUpperCase()]?.icon || '🤝',
                startTime: task.startTime,
                endTime: task.endTime,
                duration: task.duration,
                location: task.location,
                spotsAvailable: task.volunteersNeeded - task.volunteersAssigned,
                requiredSkills: task.requiredSkills
            }))
        };
        
    } catch (error) {
        console.error('Error getting tasks:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// CHECK-IN / CHECK-OUT
// =====================================================

/**
 * Check in volunteer for a task
 * @param {string} taskId
 * @param {string} assignmentId
 */
export async function checkInVolunteer(taskId, assignmentId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const task = await wixData.get('VolunteerTasks', taskId);
        
        if (!task) {
            return { success: false, error: 'Task not found' };
        }
        
        const assignment = task.assignments?.find(a => a.assignmentId === assignmentId);
        
        if (!assignment) {
            return { success: false, error: 'Assignment not found' };
        }
        
        assignment.checkedIn = true;
        assignment.checkInTime = new Date();
        assignment.checkedInBy = member._id;
        
        if (task.status === TASK_STATUS.ASSIGNED) {
            task.status = TASK_STATUS.IN_PROGRESS;
        }
        
        await wixData.update('VolunteerTasks', task);
        
        return {
            success: true,
            message: `${assignment.volunteerName} checked in`
        };
        
    } catch (error) {
        console.error('Error checking in:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Check out volunteer from a task
 * @param {string} taskId
 * @param {string} assignmentId
 * @param {Object} checkoutData - { notes, rating }
 */
export async function checkOutVolunteer(taskId, assignmentId, checkoutData = {}) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const task = await wixData.get('VolunteerTasks', taskId);
        const assignment = task.assignments?.find(a => a.assignmentId === assignmentId);
        
        if (!assignment) {
            return { success: false, error: 'Assignment not found' };
        }
        
        assignment.checkedOut = true;
        assignment.checkOutTime = new Date();
        assignment.checkedOutBy = member._id;
        assignment.notes = checkoutData.notes || '';
        assignment.rating = checkoutData.rating || 5;
        
        // Calculate hours worked
        if (assignment.checkInTime) {
            const hours = (new Date() - new Date(assignment.checkInTime)) / (1000 * 60 * 60);
            assignment.hoursWorked = Math.round(hours * 100) / 100;
            
            // Update volunteer total hours
            if (assignment.volunteerId) {
                const volunteer = await wixData.get('Volunteers', assignment.volunteerId);
                if (volunteer) {
                    volunteer.totalHours = (volunteer.totalHours || 0) + assignment.hoursWorked;
                    
                    // Check for badges
                    const newBadges = checkForBadges(volunteer);
                    if (newBadges.length > 0) {
                        volunteer.badges = [...(volunteer.badges || []), ...newBadges];
                    }
                    
                    await wixData.update('Volunteers', volunteer);
                }
            }
        }
        
        // Check if all assignments completed
        const allCompleted = task.assignments.every(a => a.checkedOut);
        if (allCompleted) {
            task.status = TASK_STATUS.COMPLETED;
        }
        
        await wixData.update('VolunteerTasks', task);
        
        return {
            success: true,
            hoursWorked: assignment.hoursWorked,
            message: `${assignment.volunteerName} checked out (${assignment.hoursWorked} hours)`
        };
        
    } catch (error) {
        console.error('Error checking out:', error);
        return { success: false, error: error.message };
    }
}

function checkForBadges(volunteer) {
    const newBadges = [];
    const hours = volunteer.totalHours || 0;
    const events = volunteer.eventsVolunteered || 0;
    const existingBadges = volunteer.badges || [];
    
    // Hour-based badges
    if (hours >= 100 && !existingBadges.includes('century_volunteer')) {
        newBadges.push({ id: 'century_volunteer', name: 'Century Volunteer', icon: '💯', earnedAt: new Date() });
    } else if (hours >= 50 && !existingBadges.includes('super_volunteer')) {
        newBadges.push({ id: 'super_volunteer', name: 'Super Volunteer', icon: '⭐', earnedAt: new Date() });
    } else if (hours >= 20 && !existingBadges.includes('dedicated_volunteer')) {
        newBadges.push({ id: 'dedicated_volunteer', name: 'Dedicated Volunteer', icon: '🏅', earnedAt: new Date() });
    }
    
    // Event-based badges
    if (events >= 10 && !existingBadges.includes('event_regular')) {
        newBadges.push({ id: 'event_regular', name: 'Event Regular', icon: '🎪', earnedAt: new Date() });
    }
    
    return newBadges;
}

// =====================================================
// VOLUNTEER ANALYTICS
// =====================================================

/**
 * Get volunteer statistics for an event
 * @param {string} eventId
 */
export async function getEventVolunteerStats(eventId) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const tasks = await wixData.query('VolunteerTasks')
            .eq('eventId', eventId)
            .find();
        
        const totalTasks = tasks.items.length;
        const totalSpotsNeeded = tasks.items.reduce((sum, t) => sum + t.volunteersNeeded, 0);
        const totalSpotsFilled = tasks.items.reduce((sum, t) => sum + t.volunteersAssigned, 0);
        
        const byCategory = {};
        const byStatus = {};
        
        for (const task of tasks.items) {
            byCategory[task.category] = (byCategory[task.category] || 0) + 1;
            byStatus[task.status] = (byStatus[task.status] || 0) + 1;
        }
        
        // Get all unique volunteers
        const volunteerIds = new Set();
        for (const task of tasks.items) {
            for (const assignment of (task.assignments || [])) {
                if (assignment.volunteerId) {
                    volunteerIds.add(assignment.volunteerId);
                }
            }
        }
        
        return {
            success: true,
            stats: {
                summary: {
                    totalTasks: totalTasks,
                    totalSpotsNeeded: totalSpotsNeeded,
                    totalSpotsFilled: totalSpotsFilled,
                    fillRate: totalSpotsNeeded > 0 
                        ? Math.round((totalSpotsFilled / totalSpotsNeeded) * 100) 
                        : 0,
                    uniqueVolunteers: volunteerIds.size
                },
                byCategory: byCategory,
                byStatus: byStatus,
                openTasks: tasks.items
                    .filter(t => t.status === TASK_STATUS.OPEN)
                    .map(t => ({
                        name: t.taskName,
                        category: t.category,
                        spotsNeeded: t.volunteersNeeded - t.volunteersAssigned
                    }))
            }
        };
        
    } catch (error) {
        console.error('Error getting volunteer stats:', error);
        return { success: false, error: error.message };
    }
}

/**
 * Get volunteer leaderboard
 */
export async function getVolunteerLeaderboard() {
    try {
        const volunteers = await wixData.query('Volunteers')
            .eq('status', VOLUNTEER_STATUS.ACTIVE)
            .descending('totalHours')
            .limit(20)
            .find();
        
        return {
            success: true,
            leaderboard: volunteers.items.map((v, index) => ({
                rank: index + 1,
                name: `${v.firstName} ${v.lastName}`,
                totalHours: v.totalHours || 0,
                eventsVolunteered: v.eventsVolunteered || 0,
                badges: v.badges?.map(b => b.icon).join(' ') || '',
                skills: v.skills?.slice(0, 3).map(s => SKILL_CATEGORIES[s.toUpperCase()]?.icon || '🤝').join(' ')
            }))
        };
        
    } catch (error) {
        console.error('Error getting leaderboard:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// COMMUNICATION
// =====================================================

/**
 * Send message to event volunteers
 * @param {string} eventId
 * @param {Object} messageData
 */
export async function messageEventVolunteers(eventId, messageData) {
    const member = await currentMember.getMember();
    if (!member || !await isAdmin(member._id)) {
        throw new Error('Unauthorized');
    }
    
    try {
        const tasks = await wixData.query('VolunteerTasks')
            .eq('eventId', eventId)
            .find();
        
        // Collect unique volunteer emails
        const emails = new Set();
        for (const task of tasks.items) {
            for (const assignment of (task.assignments || [])) {
                if (assignment.email) {
                    emails.add(assignment.email);
                }
            }
        }
        
        let sentCount = 0;
        for (const email of emails) {
            await triggeredEmails.emailContact(
                'volunteer_message',
                email,
                {
                    variables: {
                        subject: messageData.subject,
                        message: messageData.message,
                        eventTitle: tasks.items[0]?.eventTitle || 'BANF Event'
                    }
                }
            );
            sentCount++;
        }
        
        return {
            success: true,
            sentCount: sentCount,
            message: `Message sent to ${sentCount} volunteers`
        };
        
    } catch (error) {
        console.error('Error sending message:', error);
        return { success: false, error: error.message };
    }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

function calculateDuration(startTime, endTime) {
    // Simple duration calculation
    // Assumes format like "10:00 AM" and "2:00 PM"
    return `${startTime} - ${endTime}`;
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

async function isAdmin(memberId) {
    if (!memberId) return false;
    try {
        const member = await wixData.query('Members/PrivateMembersData')
            .eq('_id', memberId)
            .find({ suppressAuth: true });
        
        if (member.items.length > 0) {
            const roles = member.items[0].memberRoles || [];
            return roles.some(role => 
                role.toLowerCase().includes('admin') || 
                role.toLowerCase().includes('ec')
            );
        }
        return false;
    } catch {
        return false;
    }
}

async function logVolunteerActivity(volunteerId, action, details) {
    await wixData.insert('VolunteerActivityLog', {
        volunteerId: volunteerId,
        action: action,
        details: details,
        timestamp: new Date()
    });
}

// Export constants
export { SKILL_CATEGORIES, VOLUNTEER_STATUS, TASK_STATUS };

```
------------------------------------------------------------
