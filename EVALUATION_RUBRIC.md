# Evaluation Rubric: Virtual Patient Data Platform

## Overview

This rubric provides detailed criteria for evaluating candidate submissions. Each section includes specific behaviors to look for and red flags to watch out for.

---

## 1. Data Synchronization Algorithm (25 points)

### Excellent (22-25 points)
- [ ] Correctly aligns data streams with different starting times
- [ ] Handles multiple timestamp formats (Unix ms, Unix seconds, ISO 8601 with timezones)
- [ ] Implements intelligent gap handling (interpolation, forward-fill, or explicit flagging)
- [ ] Preserves data integrity - no silent data loss
- [ ] Handles edge cases: empty files, single data points, overlapping timestamps
- [ ] Algorithm is efficient (O(n log n) or better for alignment)
- [ ] Provides multiple sync strategies (configurable)

### Good (17-21 points)
- [ ] Correctly handles most timestamp formats
- [ ] Basic gap handling implemented
- [ ] Works for the provided dataset without errors
- [ ] Some edge cases handled

### Adequate (12-16 points)
- [ ] Basic alignment works but may have precision issues
- [ ] Limited gap handling (e.g., just removes gaps)
- [ ] May fail on some edge cases

### Poor (0-11 points)
- [ ] Incorrect alignment or data corruption
- [ ] Crashes on edge cases
- [ ] No consideration for different timestamp formats

### Red Flags 🚩
- Silently dropping data points without user notification
- Loading entire dataset into memory without streaming consideration
- Hardcoded assumptions about timestamp formats
- No handling for sensor error values (-1, null, etc.)

---

## 2. Backend Architecture (20 points)

### Excellent (17-20 points)
- [ ] Clean separation of concerns (routes, services, data access)
- [ ] RESTful API design with consistent naming
- [ ] Proper error handling with meaningful messages
- [ ] Input validation on all endpoints
- [ ] Efficient data storage/retrieval approach
- [ ] Handles large file uploads gracefully (streaming)
- [ ] API versioning consideration

### Good (13-16 points)
- [ ] Reasonable project structure
- [ ] API works correctly for happy path
- [ ] Basic error handling
- [ ] Input validation present

### Adequate (8-12 points)
- [ ] Functional but monolithic structure
- [ ] Limited error handling
- [ ] Some validation gaps

### Poor (0-7 points)
- [ ] No clear structure
- [ ] Minimal error handling
- [ ] Security vulnerabilities (SQL injection, etc.)

### What to Look For
```
✓ Proper HTTP status codes (400 for bad input, 404 for not found, etc.)
✓ Consistent response format (JSON structure)
✓ Streaming for large file handling
✓ Database/storage abstraction layer
✓ Environment configuration (not hardcoded values)
```

---

## 3. Frontend UX (20 points)

### Excellent (17-20 points)
- [ ] Intuitive upload flow with drag-and-drop support
- [ ] Real-time feedback during upload/processing
- [ ] Clear visualization of data gaps and quality issues
- [ ] Responsive design works on different screen sizes
- [ ] Accessible (keyboard navigation, ARIA labels)
- [ ] Interactive timeline with smooth zoom/pan
- [ ] Tooltips showing exact values on hover
- [ ] Loading states and error feedback

### Good (13-16 points)
- [ ] Clean, usable interface
- [ ] Visualization shows all data streams
- [ ] Basic interactivity (zoom, selection)
- [ ] Good visual design

### Adequate (8-12 points)
- [ ] Functional but basic UI
- [ ] Data displays correctly
- [ ] Limited interactivity

### Poor (0-7 points)
- [ ] Confusing interface
- [ ] Data visualization unclear or incorrect
- [ ] No loading/error states

### Visualization Criteria
```
✓ Multi-stream timeline view (all 5 data types visible)
✓ Clear indication of data gaps (not just empty space)
✓ Visual differentiation between real and interpolated data
✓ Synchronized cursor across all streams
✓ Time range selector
✓ Zoom without performance degradation
```

---

## 4. Code Quality (15 points)

### Excellent (13-15 points)
- [ ] Consistent code style throughout
- [ ] TypeScript with proper typing (no `any` abuse)
- [ ] Meaningful variable/function names
- [ ] Small, focused functions
- [ ] DRY - no significant code duplication
- [ ] Proper use of framework patterns (hooks, middleware, etc.)
- [ ] Error handling at appropriate layers

### Good (10-12 points)
- [ ] Generally clean code
- [ ] Typing mostly complete
- [ ] Reasonable organization

### Adequate (6-9 points)
- [ ] Code works but has some smell
- [ ] Inconsistent style
- [ ] Some large functions or files

### Poor (0-5 points)
- [ ] Difficult to read/understand
- [ ] No typing or excessive `any`
- [ ] Copy-paste code patterns

### Code Smell Checklist
```
🚩 Functions over 50 lines
🚩 Files over 500 lines
🚩 Deeply nested callbacks
🚩 Magic numbers without constants
🚩 Commented-out code
🚩 Console.log debugging left in
🚩 Any usage of `eval()`
```

---

## 5. Documentation (10 points)

### Excellent (9-10 points)
- [ ] README explains architecture decisions with reasoning
- [ ] Clear setup instructions that work first try
- [ ] API documentation (OpenAPI/Swagger preferred)
- [ ] Sync algorithm explained with examples
- [ ] Trade-offs discussed (what they would do differently with more time)

### Good (7-8 points)
- [ ] README covers how to run
- [ ] API endpoints documented
- [ ] Basic architecture overview

### Adequate (4-6 points)
- [ ] Minimal README
- [ ] Setup instructions present but incomplete
- [ ] Limited API documentation

### Poor (0-3 points)
- [ ] No README or unusable
- [ ] Cannot figure out how to run the project
- [ ] No API documentation

---

## 6. Bonus Features (10 points)

Award points for any of the following:

| Feature | Points |
|---------|--------|
| Export synced data to CSV/JSON | +1 |
| Anomaly detection with highlighting | +2 |
| Unit tests (meaningful coverage) | +2 |
| Integration/E2E tests | +1 |
| Docker compose setup | +1 |
| Real-time streaming simulation | +2 |
| Performance optimization for large datasets | +1 |
| Accessibility audit/fixes | +1 |
| Mobile-responsive design | +1 |

---

## Interview Follow-Up Questions

Use these during the review call:

### Architecture
1. "Walk me through how data flows from upload to visualization."
2. "What would you change if this needed to handle 100 patients with 10x the data?"
3. "How would you add real-time data streaming?"

### Data Handling
4. "Explain your sync algorithm. What's the time complexity?"
5. "How do you handle a gap in one stream but not others?"
6. "What happens if someone uploads the same file twice?"

### Trade-offs
7. "What would you do differently with more time?"
8. "What's the biggest technical debt in your solution?"
9. "How confident are you in the accuracy of the synchronized data?"

### Problem Solving
10. "The SpO2 sensor sometimes gives readings of 110%. How would you handle that?"
11. "A researcher wants to compare this patient to historical norms. How would you extend this?"

---

## Scoring Summary

| Category | Max Points | Score |
|----------|------------|-------|
| Data Synchronization | 25 | |
| Backend Architecture | 20 | |
| Frontend UX | 20 | |
| Code Quality | 15 | |
| Documentation | 10 | |
| Bonus Features | 10 | |
| **TOTAL** | **100** | |

### Score Interpretation

| Score | Recommendation |
|-------|---------------|
| 85+ | Strong hire - exceeds expectations |
| 70-84 | Hire - meets bar with some strengths |
| 55-69 | Maybe - discuss with team, may need mentoring |
| Below 55 | No hire - significant gaps |

---

## Notes Section

_Use this space for interviewer observations during code review:_

```
Candidate: ________________________
Date: ________________________

Strengths:



Areas for Growth:



Notable Decisions:



Red Flags:



Overall Impression:



```

