# Technical Specification: Web-Based Document Translator

**Status:** `ready-for-agent`

## Problem Statement

Users need a way to translate documents or text into target languages without creating accounts or paying for expensive services, receiving the results conveniently via email.

## Solution

A web application where users provide text/files, an email address, and a target language. The system translates the content in the background and emails the result to the user.

## User Stories

1. As a user, I want to paste a short block of text into a form, so that I can translate it quickly.
2. As a user, I want to enter my email address, so that I can receive the translation without staying on the page.
3. As a user, I want to choose a target language from a list, so that the translation is in the language I need.
4. As a user, I want to submit the request and see a confirmation message, so that I know the system is processing my request.
5. As a user, I want to receive an email containing the translated text in the body for short translations, so that I can read it immediately.
6. As a user, I want to upload a .txt file, so that I can translate simple documents.
7. As a user, I want to upload a .docx file, so that I can translate professional documents.
8. As a user, I want to upload a .pdf file, so that I can translate portable documents.
9. As a user, I want the translation of large documents to run in the background, so that the web page doesn't freeze or timeout.
10. As a user, I want to receive the translated result as an email attachment for large documents, so that the formatting is preserved and the email is manageable.
11. As a user, I want to see a simple job status (e.g., 'Processing', 'Completed'), so that I know when to expect my email.
12. As a user, I want an error email if the translation fails, so that I am not left wondering why I didn't receive my result.
13. As a system administrator, I want to limit the file size of uploads, so that the server is not overwhelmed.
14. As a system administrator, I want to rate-limit requests per email address, so that the service is not abused.
15. As a system administrator, I want to validate the email address format, so that emails are not sent to invalid addresses.

## Implementation Decisions

### Architecture
- **Backend:** FastAPI for the REST API and request handling.
- **Frontend:** Simple HTML templates with HTMX for dynamic updates (e.g., status polling) without full page reloads.
- **Async Processing:** Celery with Redis as a broker to handle translation jobs outside the request-response cycle.
- **Translation:** Integration with an open-source translation engine (e.g., Argos Translate) accessed via a clean Translator interface.
- **Email:** An EmailProvider interface to handle dispatch, allowing switching between Mailpit (dev) and a free SMTP tier (prod).

### API Contracts
- `POST /translate`: Accepts email, target language, and either text or a file. Returns a `job_id`.
- `GET /status/{job_id}`: Returns the current status of the translation job.

### Data Flow
1. User submits form -> FastAPI validates input.
2. FastAPI creates a job in Redis -> returns `job_id` to user.
3. Celery worker picks up job -> extracts text from file/input -> calls Translator.
4. Translator returns translated text.
5. Celery worker calls EmailProvider to send result -> marks job as completed.

## Testing Decisions

- **External Behavior Focus:** Tests will verify that a request results in an email being 'sent' and the job status being updated.
- **Seams:**
    - **API Seam:** Use FastAPI TestClient for end-to-end flow verification.
    - **Email Seam:** Use a FakeEmailProvider to capture and assert on sent messages.
    - **Translation Seam:** Use a FakeTranslator to avoid resource-heavy model calls during logic tests.
- **TDD Approach:** Red-Green-Refactor cycle for every single user story.

## Out of Scope
- User accounts, authentication, or login.
- Payment processing.
- OCR for scanned PDFs or complex layout preservation.
- Dedicated mobile application.

## Further Notes
- Priority is strictly: Email Delivery -> Core Translation -> File Support -> UI Polish.
