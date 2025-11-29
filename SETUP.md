# GitHub Issue System - Setup Instructions

## 📦 Files Included

- `bug_report.md` - Bug report template
- `feature_request.md` - Feature request template
- `task.md` - General task template
- `red_team_test.md` - Red Team testing template
- `blue_team_security.md` - Blue Team security template
- `PRIVATE_README.md` - Main documentation for the system
- `labels.txt` - Label definitions for import
- `example_issues.md` - Example issues to demonstrate workflow

---

## 🚀 Installation Steps

### 1. Create Directory Structure

In your `private` repo:

```bash
mkdir -p .github/ISSUE_TEMPLATE
```

### 2. Install Templates

Copy the template files to the templates directory:

```bash
cp bug_report.md .github/ISSUE_TEMPLATE/
cp feature_request.md .github/ISSUE_TEMPLATE/
cp task.md .github/ISSUE_TEMPLATE/
cp red_team_test.md .github/ISSUE_TEMPLATE/
cp blue_team_security.md .github/ISSUE_TEMPLATE/
```

### 3. Install Main README

```bash
cp PRIVATE_README.md README.md
```

Or if you already have a README, add the contents to it.

### 4. Create Labels

**Option A: Manual Creation**
1. Go to `https://github.com/ResonantAISystems/private/labels`
2. Click "New label"
3. Create each label from `labels.txt` with name, color, and description

**Option B: Bulk Import (Easier)**
1. Install GitHub CLI: `gh auth login`
2. Use this script to import all labels:

```bash
# From labels.txt, create each label
# Format: name,color,description

gh label create "business" --color "E7F0FF" --description "Business operations and strategy" --repo ResonantAISystems/private
gh label create "web-dev" --color "1D76DB" --description "Web development work" --repo ResonantAISystems/private
gh label create "local-dev" --color "5319E7" --description "Local development and tooling" --repo ResonantAISystems/private
# ... repeat for all labels in labels.txt
```

Or create a quick script:

```bash
while IFS=, read -r name color desc; do
  gh label create "$name" --color "$color" --description "$desc" --repo ResonantAISystems/private
done < labels.txt
```

### 5. Commit and Push

```bash
git add .github/ISSUE_TEMPLATE/
git add README.md
git commit -m "Add GitHub issue-based task management system"
git push
```

### 6. Create Example Issues (Optional)

Use the examples in `example_issues.md` to populate the board and demonstrate workflow:

1. Go to Issues → New Issue
2. Select appropriate template
3. Copy content from example
4. Adjust as needed
5. Submit

Create all 7 examples to show:
- Red Team → Blue Team workflow
- Feature → Task breakdown
- Bug reports
- Business tasks

---

## ✅ Verification

After setup, verify:

1. **Templates visible:**
   - Go to Issues → New Issue
   - Should see 5 template options

2. **Labels created:**
   - Go to Labels tab
   - Should see all category, type, team, priority, and status labels

3. **README shows:**
   - Main page of repo should show documentation

4. **Test creating issue:**
   - Create a test issue using each template
   - Verify all fields work
   - Delete test issues after verification

---

## 🎯 Next Steps

1. **Share with team:**
   - Send everyone link to README
   - Walk through templates in team meeting
   - Explain Red/Blue Team workflow

2. **Create first real issues:**
   - Start with backlog items
   - Break down current projects into tasks
   - Assign to team members

3. **Set up notifications:**
   - Watch the repo (all team members)
   - Configure email preferences
   - Optional: Integrate with Slack/Discord

4. **Define milestones:**
   - Create milestone for current sprint
   - Create milestone for next release
   - Add issues to milestones

5. **Start using:**
   - Create issues for all new work
   - Comment on issues for discussion
   - Close issues as work completes

---

## 💡 Pro Tips

### Quick Access Bookmarks

Bookmark these for fast issue creation:

```
Bug: https://github.com/ResonantAISystems/private/issues/new?template=bug_report.md
Feature: https://github.com/ResonantAISystems/private/issues/new?template=feature_request.md
Task: https://github.com/ResonantAISystems/private/issues/new?template=task.md
Red Team: https://github.com/ResonantAISystems/private/issues/new?template=red_team_test.md
Blue Team: https://github.com/ResonantAISystems/private/issues/new?template=blue_team_security.md
```

### Useful Searches

Save these as bookmarks:

```
My open issues: https://github.com/ResonantAISystems/private/issues?q=is%3Aopen+is%3Aissue+assignee%3A%40me
Critical issues: https://github.com/ResonantAISystems/private/issues?q=is%3Aopen+label%3Apriority%3Acritical
Red Team work: https://github.com/ResonantAISystems/private/issues?q=is%3Aopen+label%3Ared-team
Available work: https://github.com/ResonantAISystems/private/issues?q=is%3Aopen+no%3Aassignee
```

---

## 🔧 Customization

### Adding Custom Templates

Create new template in `.github/ISSUE_TEMPLATE/`:

```markdown
---
name: Your Template Name
about: Description of when to use this
title: '[PREFIX] '
labels: your-labels
assignees: ''
---

Your template content here
```

### Adding Custom Labels

```bash
gh label create "your-label" --color "HEXCOLOR" --description "Description" --repo ResonantAISystems/private
```

### Modifying Templates

Edit files in `.github/ISSUE_TEMPLATE/` and commit changes.

---

## 📞 Support

Questions about the system? Create an issue with `question` label!

---

## ✅ Setup Complete!

Your issue-based task management system is ready to use.

Start creating issues and managing work! 🚀