# Project Roadmap: Web-Based Document Translator

This document serves as a reference for the development process, following the "Vertical Slice" architecture and the Matt Pocock engineering flow.

## 🎯 Product Goal
A user can upload a document or paste text, choose a target language, and provide an email address. The translated result is delivered to that email.

**Core Priority:** Email delivery is the most critical feature. Prioritize it over UI polish.

---

## 🛠 Proposed Tech Stack (Free/Open Source)
- **Backend:** Python + FastAPI
- **Frontend:** Simple HTML/Jinja + HTMX (or minimal React)
- **Background Jobs:** Redis + Celery / RQ (for large documents)
- **Translation Engine:** Self-hosted open-source models (e.g., Argos Translate, LibreTranslate, or Opus-MT)
- **Email:** Mailpit (Dev) $\rightarrow$ Free SMTP tier (Production)
- **Parsing:** `pypdf`, `python-docx`

---

## 🚀 The Engineering Flow

### Phase 1: Sharpening & Validation
1. **`/grill-with-docs`**: Stress-test the "free only" stack. Resolve technical uncertainties.
   - *Output:* `CONTEXT.md` (Glossary), `docs/adr/` (Architectural decisions).
2. **`/prototype`**: Build a "technical spike" to prove the core loop (Translate $\rightarrow$ Email) works with free tools.
   - *Output:* Throwaway code in `prototype/` directory.

### Phase 2: Planning
3. **`/to-spec`**: Convert the agreed-upon thinking into a formal Technical Specification.
   - *Output:* `spec.md`.
4. **`/to-tickets`**: Split the spec into **Vertical Tracer-Bullet Tickets**.
   - *Output:* GitHub Issues.

### Phase 3: Execution (The Build)
5. **`/implement`**: Run for each ticket.
   - **Internal Process:** `/implement` $\rightarrow$ `/tdd` (Test-Driven Development) $\rightarrow$ `/code-review` (Standards & Spec check) $\rightarrow$ Commit.
   - *Requirement:* Every ticket must be demoable in the browser.

---

## 📏 Vertical Slice Sequence (The Tickets)

| Slice | Focus | End-to-End Flow | Ticket Reference |
| :--- | :--- | :--- | :--- |
| **1** | **Thinnest Slice** | Paste short text $\rightarrow$ Email $\rightarrow$ Language $\rightarrow$ Submit $\rightarrow$ Receive translated email. | `.scratch/translation/issues/001-thinnest-slice.md` |
| **2** | **Basic File Support** | Upload `.txt` file $\rightarrow$ Backend parse $\rightarrow$ Translation $\rightarrow$ Email. | `.scratch/translation/issues/002-txt-upload.md` |
| **3** | **Asynchronous Loop** | Submit $\rightarrow$ Background Job (Redis/Celery) $\rightarrow$ Confirmation Page $\rightarrow$ Email. | `.scratch/translation/issues/003-async-loop.md` |
| **4** | **Complex Formats** | Support `.docx` and `.pdf` $\rightarrow$ Parsing $\rightarrow$ Translation $\rightarrow$ Email. | `.scratch/translation/issues/004-complex-docs.md` |
| **5** | **Scalability** | Handle large documents via chunking $\rightarrow$ Progress tracking $\rightarrow$ Email. | `.scratch/translation/issues/005-large-docs.md` |
| **6** | **Hardening** | Validation $\rightarrow$ Rate limits $\rightarrow$ File size limits $\rightarrow$ Error emails. | `.scratch/translation/issues/006-hardening.md` |

---

## 📝 Reference: Skill Definitions
- **`/tdd`**: Writes a failing test $\rightarrow$ writes minimal code to pass $\rightarrow$ refactors.
- **`/code-review`**: Reviews code against the Spec and general coding standards.
- **`/prototype`**: Quick, throwaway code to answer a "will this work?" question.
