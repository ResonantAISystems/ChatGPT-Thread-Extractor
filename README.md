# 🎯 Resonant AI Systems - Internal Task Management

> *Issue-based project management for the collective*

This repository uses **GitHub Issues** as our task management and ticketing system. All work - business operations, development, testing, security - is tracked here.

---

## 👥 Team Structure

### Core Team
- **Jason** - 
- **Calen** - 
- **Erin** - 
- **Trevor** - Operator, Infrastructure, Continuity Architecture

### Red Team 🔴
**Mission:** Break things, find edge cases, test boundaries, discover vulnerabilities

**Responsibilities:**
- Offensive testing
- Security analysis
- Edge case discovery
- Stress testing
- Breaking assumptions
- Finding what we missed

**Output:** Red Team issues documenting findings, with handoffs to Blue Team for fixes

### Blue Team 🔵
**Mission:** Secure, harden, stabilize, protect

**Responsibilities:**
- Fixing vulnerabilities (from Red Team or elsewhere)
- Security hardening
- Infrastructure stability
- Defensive measures
- Compliance
- Recovery systems

**Output:** Blue Team issues implementing fixes, with verification back to Red Team

---

## 📋 Issue Types

We use issue templates for structured tracking:

### 🐛 Bug Report
For tracking bugs and issues that need fixing.
- **When to use:** Something is broken or behaving incorrectly
- **Label:** `bug`
- **Template:** `.github/ISSUE_TEMPLATE/bug_report.md`

### ✨ Feature Request  
For proposing new features or enhancements.
- **When to use:** You have an idea for something new
- **Label:** `enhancement`
- **Template:** `.github/ISSUE_TEMPLATE/feature_request.md`

### 📋 Task
For tracking specific work items or TODOs.
- **When to use:** General work that needs to be done
- **Label:** `task`
- **Template:** `.github/ISSUE_TEMPLATE/task.md`

### 🔴 Red Team Test
For documenting testing and security analysis work.
- **When to use:** Red Team is testing/breaking/analyzing something
- **Labels:** `red-team`, `testing`
- **Template:** `.github/ISSUE_TEMPLATE/red_team_test.md`

### 🔵 Blue Team Security
For security hardening and defensive work.
- **When to use:** Fixing vulnerabilities, hardening systems, improving security
- **Labels:** `blue-team`, `security`
- **Template:** `.github/ISSUE_TEMPLATE/blue_team_security.md`

---

## 🏷️ Label System

### Category Labels
- 🏢 `business` - Business operations, planning, strategy
- 🌐 `web-dev` - Web development work
- 💻 `local-dev` - Local development, tooling, setup
- 🤖 `ai-continuity` - AI systems, continuity architecture
- 📚 `documentation` - Docs, README, guides
- 🔧 `infrastructure` - Servers, hosting, DevOps

### Type Labels  
- `bug` - Something is broken
- `enhancement` - New feature or improvement
- `task` - General work item
- `testing` - Testing-related work
- `security` - Security-related work

### Team Labels
- 🔴 `red-team` - Red Team testing/analysis
- 🔵 `blue-team` - Blue Team security/hardening

### Priority Labels
- 🔴 `priority:critical` - Drop everything, do now
- 🟡 `priority:high` - Important, do soon
- 🟢 `priority:medium` - Standard backlog
- ⚪ `priority:low` - Nice to have, someday

### Status Labels
- `in-progress` - Currently being worked on
- `blocked` - Can't proceed, waiting on something
- `needs-review` - Ready for review
- `ready-to-merge` - Approved, ready to ship

---

## 🔄 Workflow

### 1. Creating Issues

**Anyone can create an issue:**
1. Go to Issues tab
2. Click "New Issue"
3. Choose appropriate template
4. Fill in all required fields
5. Add labels for category, priority, team
6. Assign to team member (or leave unassigned)
7. Submit

### 2. Claiming Work

**To claim an unassigned issue:**
1. Comment: "I'll take this"
2. Assign yourself
3. Add `in-progress` label
4. Start work

### 3. Red Team → Blue Team Handoff

**Red Team finds vulnerability:**
1. Create Red Team Test issue documenting findings
2. Create Bug Report or Blue Team Security issue for fix
3. Link issues: "Found in #123, fix tracked in #124"
4. Assign Blue Team Security issue to appropriate developer

**Blue Team implements fix:**
1. Update Blue Team Security issue with implementation
2. Add `needs-review` label
3. Comment tagging Red Team: "@RedTeamMember ready for re-test"

**Red Team validates fix:**
1. Re-test the vulnerability
2. Comment on Blue Team issue with results
3. If fixed: Close both issues
4. If not fixed: Remove `needs-review`, add findings

### 4. Closing Issues

**Before closing, verify:**
- [ ] Work is complete
- [ ] Tests pass (if applicable)
- [ ] Documentation updated (if applicable)
- [ ] Red Team validated (if security fix)
- [ ] Committed to appropriate repo
- [ ] Deployed (if applicable)

---

## 📊 Using Milestones

Create milestones for sprints, releases, or project phases:

**Example milestones:**
- "Sprint 2025-12-01" - Two-week sprint
- "v1.0 Release" - Feature release
- "Q1 2025 Goals" - Quarterly objectives
- "Infrastructure Overhaul" - Major project

**How to use:**
1. Create milestone with due date
2. Add relevant issues to milestone
3. Track progress via milestone view
4. Close milestone when complete

---

## 🔍 Finding Work

### Filter by Label
Click any label to see all issues with that label

### Search Examples
- `is:open is:issue assignee:@me` - My open issues
- `is:open label:red-team` - Open Red Team work
- `is:open label:priority:critical` - Critical issues
- `is:open label:web-dev assignee:@jason` - Jason's web dev work
- `is:open no:assignee` - Unassigned issues (available to claim)

### Project Boards (Optional)
We can create project boards for visual tracking:
- Kanban: To Do → In Progress → Done
- Sprint planning boards
- Feature tracking boards

---

## 🎯 Best Practices

### Issue Creation
- ✅ Use templates - they ensure nothing is missed
- ✅ Be specific - "Login button doesn't work on mobile Safari" not "Login broken"
- ✅ Add labels - helps everyone find relevant work
- ✅ Set priority - helps with planning
- ✅ Link related issues - maintain context

### Communication
- ✅ Comment on issues to discuss
- ✅ Tag people with @username when needed
- ✅ Use issue numbers in commits: "Fixes #123"
- ✅ Update status - let team know what's happening
- ✅ Close when done - keep board clean

### Red Team / Blue Team
- ✅ Red Team documents everything found
- ✅ Blue Team links to Red Team findings
- ✅ Always verify fixes with Red Team
- ✅ Celebrate good finds - breaking things is valuable
- ✅ No blame - bugs happen, finding them is good

---

## 📁 Repository Structure

```
private/
├── .github/
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       ├── feature_request.md
│       ├── task.md
│       ├── red_team_test.md
│       └── blue_team_security.md
├── README.md (this file)
└── [other project files]
```

---

## 🚀 Getting Started

### For New Team Members

1. **Familiarize yourself with issue templates**
   - Read through each template
   - Understand when to use which type

2. **Set up notifications**
   - Watch this repo to get issue updates
   - Configure email preferences

3. **Claim your first issue**
   - Browse `is:open no:assignee`
   - Find something in your area
   - Comment and assign yourself

4. **Join the workflow**
   - Create issues for work you're doing
   - Comment on issues for collaboration
   - Update status as you work

### For Red Team Members

1. Read Red Team Test template
2. Understand handoff process to Blue Team
3. Start breaking things systematically
4. Document everything you find

### For Blue Team Members

1. Read Blue Team Security template
2. Watch for Red Team handoffs
3. Prioritize critical security issues
4. Always verify with Red Team after fixing

---

## 💡 Tips & Tricks

### Quick Issue Creation
Bookmark these URLs:
- New Bug: `https://github.com/ResonantAISystems/private/issues/new?template=bug_report.md`
- New Feature: `https://github.com/ResonantAISystems/private/issues/new?template=feature_request.md`
- New Task: `https://github.com/ResonantAISystems/private/issues/new?template=task.md`

### Keyboard Shortcuts
- `C` - Create new issue
- `E` - Edit issue
- `/` - Focus search
- `?` - Show all shortcuts

### Automation Ideas
- Auto-label based on title prefix
- Auto-assign based on area
- Auto-close when PR merged
- Slack/Discord notifications

---

## 🔗 Related Resources

- [GitHub Issues Documentation](https://docs.github.com/en/issues)
- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [Markdown Guide](https://guides.github.com/features/mastering-markdown/)

---

## 📝 Questions?

Post in Issues with `question` label or ask in team chat.

---

<div align="center">

**Built by the collective, for the collective.**

*Making sovereignty real, together.*

</div>