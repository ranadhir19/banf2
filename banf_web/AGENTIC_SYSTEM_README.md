# BANF Website Agentic System

## Overview

This is a comprehensive agentic system for building and testing the BANF (Bengali Association of North Florida) landing page on Wix using automated browser interactions guided by an LLM.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MASTER ORCHESTRATOR                              │
│  - Goal decomposition & planning                                         │
│  - Agent coordination                                                    │
│  - State management & recovery                                           │
└───────────────────┬─────────────────┬───────────────────────────────────┘
                    │                 │
          ┌─────────▼─────────┐       │
          │   LLM CLIENT      │       │
          │  (Claude via      │       │
          │   Databricks)     │       │
          └───────────────────┘       │
                                      │
┌─────────────────────────────────────▼───────────────────────────────────┐
│                      COMPUTER USE AGENT                                  │
│  - Browser automation (Playwright)                                       │
│  - Screenshot capture & analysis                                         │
│  - Element detection & interaction                                       │
│  - Wix-specific navigation                                              │
└─────────────────────────────────────────────────────────────────────────┘
```

## Files Structure

```
banf_web/
├── agentic_system/
│   ├── __init__.py           # Package init
│   ├── config.py             # All configuration (Wix, LLM, Sections, Tests)
│   ├── orchestrator.py       # Master orchestrator with planning
│   └── computer_use_agent.py # Browser automation agent
├── run_agentic_system.py     # Full automated runner
└── run_step_by_step.py       # Interactive step-by-step runner
```

## Quick Start

### Option 1: Step-by-Step Mode (Recommended for first run)

```powershell
cd C:\projects\survey\banf_web
python run_step_by_step.py
```

This launches an interactive mode where you:
- See each step before execution
- Control pace with commands
- Manually login when prompted
- Review results at each stage

**Commands:**
- `n` - Execute next step
- `p` - Go back to previous step
- `j 5` - Jump to step 5
- `r` - Run all remaining steps
- `s` - Show detailed status
- `q` - Save and quit

### Option 2: Full Automated Mode

```powershell
cd C:\projects\survey\banf_web
python run_agentic_system.py
```

This will:
1. Create an AI-generated execution plan
2. Show plan summary
3. Ask for confirmation
4. Execute all steps automatically

## Execution Plan

### Phase 1: Setup (Steps 1-5)
1. **Launch Browser** - Start Chromium with Playwright
2. **Navigate to Dashboard** - Go to Wix dashboard for dev site
3. **Login** - Manual login to Wix account
4. **Open Editor** - Navigate to Wix Editor
5. **Enable Dev Mode** - Turn on Velo development mode

### Phase 2: Build Landing Page (Steps 6-14)
Build each section in priority order:
- Navigation Bar (priority 1)
- Hero Section (priority 1)
- Quick Access Bar (priority 2)
- Events Section (priority 2)
- Membership CTA (priority 3)
- Community Resources (priority 3)
- Radio Section (priority 4)
- Footer (priority 5)

### Phase 3: Deploy (Step 15)
- Publish site to dev environment

### Phase 4: Test (Steps 16-18)
- Test navigation links
- Test CTA buttons
- Test mobile responsiveness

## Configuration

All configuration is in `agentic_system/config.py`:

### Wix Site Details
```python
WIX_CONFIG = {
    "dev_site_id": "c13ae8c5-7053-4f2d-9a9a-371869be4395",
    "dev_site_url": "https://banfwix.wixsite.com/banf1",
    ...
}
```

### LLM Configuration
```python
DATABRICKS_CONFIG = {
    "url": "https://adb-7405619558164804.4.azuredatabricks.net",
    "model": "databricks-claude-sonnet-4-5",
    ...
}
```

### Landing Page Sections
Each section is defined with:
- Priority (1=highest)
- Elements to create
- Velo code requirements
- Status tracking

### Test Features
Each testable feature includes:
- Test steps
- Expected results
- Dependencies on other features

## Output

The system generates:
- **Screenshots** - `screenshots/agentic/` - Step-by-step visuals
- **Logs** - `agentic_logs/session_<id>/` - Detailed execution logs
- **Plans** - `agentic_system/plans/` - Generated execution plans
- **Session State** - JSON files tracking progress

## Error Handling

When a step fails:
1. Screenshot is captured
2. LLM is asked for recovery strategy
3. Recovery actions are attempted
4. If recovery fails, option to skip or retry

## Manual Steps Required

1. **Login** - You must manually enter Wix credentials in the browser
   - Email: Banfjax@gmail.com
   - Password: Banfec2022

2. **Complex UI Operations** - Some Wix Editor operations may need manual intervention

## Next Steps

After running the agentic system:

1. Review generated screenshots in `screenshots/agentic/`
2. Check session logs for any issues
3. Manually verify the landing page at: https://banfwix.wixsite.com/banf1
4. Run test features to validate functionality
5. Iterate on any sections that need refinement

## Troubleshooting

### Browser won't launch
```powershell
python -m playwright install chromium
```

### Login timeout
- Increase timeout in `computer_use_agent.py`
- Complete login faster
- Check credentials

### Element not found
- The LLM will suggest alternatives
- Screenshots help diagnose issues
- Check if Wix UI has changed
