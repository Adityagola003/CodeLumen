# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: analyze.spec.js >> uploads a sample file and renders analysis results
- Location: tests\e2e\analyze.spec.js:4:1

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('#explainResult .explain-summary')
Expected: visible
Timeout: 10000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 10000ms
  - waiting for locator('#explainResult .explain-summary')

```

```yaml
- navigation:
  - link "C CodeLumen AI":
    - /url: "#"
  - link "Workspace":
    - /url: "#workspace"
  - link "Analytics":
    - /url: "#analyticsDashboard"
  - link "History":
    - /url: "#historySection"
  - combobox "Select language":
    - option "English" [selected]
    - option "தமிழ் (Tamil)"
    - option "हिन्दी (Hindi)"
    - option "Français (French)"
  - button "Switch to dark mode" [pressed]
- text: Open Source · AI-Powered · Always Free
- heading "Spot Bugs. Learn Fast. Code with Confidence." [level=1]:
  - text: Spot Bugs. Learn Fast.
  - emphasis: Code with Confidence.
- paragraph: Drop in your code and get instant bug detection, plain-English explanations, and actionable improvement suggestions — no sign-up, no hassle.
- button "Start Analyzing":
  - img
  - text: Start Analyzing
- button "Try Sample Code":
  - img
  - text: Try Sample Code
- text: Analyses
- strong: "0"
- text: Avg. score
- strong: "--"
- text: Issues found
- strong: "0"
- text: Engine
- strong: Local + AI
- img
- paragraph: 40+ Bug Patterns
- paragraph: Python, JS, TS, Java, C++
- img
- paragraph: Code Explanation
- paragraph: Plain English breakdowns
- img
- paragraph: Smart Suggestions
- paragraph: Quality score + grade
- img
- paragraph: Dark / Light Mode
- paragraph: Persisted preference
- img
- paragraph: File Upload
- paragraph: .py .js .ts .java .cpp .kt .zip
- text: Code Editor
- group "Analysis provider":
  - button "AI" [pressed]
  - button "Local"
- button "Upload file"
- button "Clear"
- button "Copy code"
- group "Select Programming Language":
  - button "Python" [pressed]
  - button "JavaScript"
  - button "TypeScript"
  - button "Java"
  - button "C++"
- text: 1 2 3 4 5 6
- textbox "Code editor":
  - /placeholder: "# Paste your code here or click 'Try Sample Code' above…"
  - text: "def add(a, b): return a + b print(add(1, 2))"
- text: 51 chars · 6 lines · 3 non-blank
- group "Analysis action":
  - button "Analyze Code" [pressed]
  - button "AI Chat"
- text: Ctrl+Alt+1-2
- button "Analyze Code" [disabled]
- note "Keyboard shortcuts": / Focus editor Ctrl/⌘ + Enter Analyze Esc Leave editor
- text: Analysis Results
- tablist "Result Tabs":
  - tab "Explain" [selected]
  - tab "Debug"
  - tab "Improve"
  - tab "AI Chat"
- tabpanel "Explain"
- group: Analytics Dashboard ▶
- text: Query History
- button "Clear"
- button "Download history as JSON": Download JSON
- button "Download history as CSV": Download CSV
- textbox "Search history..."
- text: "Language:"
- combobox "Filter history by language":
  - option "All" [selected]
  - option "Python"
  - option "Java"
  - option "JavaScript"
  - option "TypeScript"
  - option "C++"
- text: "Issues:"
- combobox "Filter history by issue count":
  - option "Any" [selected]
  - option "0 Issues"
  - option "1-5 Issues"
  - option "5+ Issues"
- text: "Sort:"
- combobox "Sort history by":
  - option "Date" [selected]
  - option "Quality Score"
  - option "Bugs Scanned"
- text: "Order:"
- combobox "Sort order":
  - option "Desc" [selected]
  - option "Asc"
- text: No history yet. Run your first analysis.
- button "« Prev" [disabled]
- text: Page 1 of 1
- button "Next »" [disabled]
- text: Saved Favorites
- button "Clear"
- text: No favorites saved yet.
- contentinfo:
  - text: CodeLumen AI
  - paragraph: Local code analysis workspace
```