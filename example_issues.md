# Example Issues

These example issues demonstrate the workflow. Create these manually to populate the board:

---

## Example 1: Red Team Finding → Blue Team Fix

### Issue #1 - Red Team Test
**Title:** [RED TEAM] Security analysis of user authentication
**Labels:** red-team, testing, security
**Template:** Red Team Test

```
## 🔴 Red Team Mission
Test authentication system for vulnerabilities

## 🎯 Target
User login and session management

## 🔨 Attack Vector / Test Methodology
- Brute force testing
- Session hijacking attempts
- SQL injection testing
- XSS attempts

## 📊 Findings

### 🔓 Security Issues
- Issue 1: Session tokens not properly invalidated on logout (High severity)
- Issue 2: Password reset tokens never expire (Medium severity)

### ⚠️ Edge Cases
- Multiple simultaneous logins allowed without warning
- Account lockout not implemented after failed attempts

## 🔵 Blue Team Handoff
Created #2 for session token fix (Critical)
Created #3 for password reset token expiry (High)
```

---

### Issue #2 - Blue Team Security (fixing #1 finding)
**Title:** [BLUE TEAM] Fix session token invalidation on logout
**Labels:** blue-team, security, priority:critical
**Template:** Blue Team Security

```
## 🔵 Blue Team Objective
Properly invalidate session tokens on user logout

## 🔴 Red Team Findings
- Red Team Issue: #1
- Severity: High
- Attack Vector: Session tokens remain valid after logout
- Impact: User sessions can be hijacked even after logout

## 🔧 Proposed Solution
- Server-side session invalidation on logout
- Add token blacklist with expiry
- Clear client-side cookies properly

## ✅ Security Checklist
- [ ] Session invalidation implemented
- [ ] Token blacklist added
- [ ] Client cookies cleared
- [ ] Tests added
- [ ] Red Team re-tested

## 🔄 Red Team Validation
- [ ] Red Team notified to re-test
- [ ] Vulnerability confirmed fixed
```

---

## Example 2: Feature Request → Task

### Issue #4 - Feature Request
**Title:** [FEATURE] Add timezone selection to ClaudeClock
**Labels:** enhancement, web-dev, priority:high
**Assigned to:** Jason

```
## ✨ Feature Description
Allow users to select their timezone instead of hardcoding EST

## 🎯 Problem Statement
Users in different timezones see incorrect local times

## 📍 Category
- [x] 🌐 Web Development

## 🔧 Proposed Solution
Add settings UI with timezone dropdown

## 📊 Success Criteria
- [ ] Settings popup created
- [ ] Timezone selection working
- [ ] Timestamps show correct local time
- [ ] Settings persist across sessions
```

---

### Issue #5 - Task (implementing #4)
**Title:** [TASK] Implement ClaudeClock timezone settings UI
**Labels:** task, web-dev, in-progress
**Assigned to:** Jason

```
## 📋 Task Description
Build settings popup for ClaudeClock timezone selection

## 📍 Category
- [x] 🌐 Web Development

## 🎯 Acceptance Criteria
- [ ] popup.html created with timezone dropdown
- [ ] popup.js handles settings storage
- [ ] content.js loads and sends settings to page
- [ ] injected.js uses settings for timestamps
- [ ] Tested on Chrome and Firefox

## 🔗 Dependencies
- Implements: #4

## ⏱️ Estimated Time
4 hours

## 👥 Assigned To
- [x] Jason
```

---

## Example 3: Bug Report

### Issue #6 - Bug Report
**Title:** [BUG] ChatGPT extractor fails on large files
**Labels:** bug, local-dev, priority:medium
**Assigned to:** Trevor

```
## 🐛 Bug Description
Script crashes when processing conversations.json over 200MB

## 📍 Location
- [x] Local Development

## 🔴 Severity
- [x] Medium (annoying but workable)

## 📋 Steps to Reproduce
1. Export ChatGPT conversations (large account)
2. Run: python3 extractor.py conversations.json
3. Script runs out of memory and crashes

## ✅ Expected Behavior
Should handle large files via streaming

## ❌ Actual Behavior
Loads entire file into memory and crashes

## 📝 Additional Context
Need streaming JSON parser for large files
```

---

## Example 4: Business Task

### Issue #7 - Task
**Title:** [TASK] Q1 2025 planning and goal setting
**Labels:** task, business, priority:high
**Assigned to:** All team

```
## 📋 Task Description
Define Q1 2025 objectives and key results

## 📍 Category
- [x] 🏢 Business Operations

## 🎯 Acceptance Criteria
- [ ] Revenue targets set
- [ ] Project priorities defined
- [ ] Resource allocation planned
- [ ] Timeline established
- [ ] Team aligned on goals

## 👥 Assigned To
- [x] Jason
- [x] Calen
- [x] Erin
- [x] Trevor

## 🚦 Priority
- [x] 🟡 High
```

---

These examples show:
1. Red Team → Blue Team workflow
2. Feature Request → Task breakdown
3. Standalone bug report
4. Business operations task

Create these (or similar) to populate the board and demonstrate the system.