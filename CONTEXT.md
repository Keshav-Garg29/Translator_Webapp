# Project Context: Translator Web App

## Glossary

### Core Entities
- **Requestor**: The individual requesting a translation, identified solely by a mandatory email address. There is currently no formal account/authentication system.
- **Translation Request**: A persistent entity representing a single translation job. It tracks the lifecycle of the translation to ensure failures can be handled gracefully.
- **Translation Result**: The output of a Translation Request, hosted at a secure URL for the Requestor to access.

### Processes
- **Translation**: The act of converting text from a source language to a target language using a commercial API (e.g., DeepL or Google Translate) to ensure high accuracy and low local resource overhead.
- **Delivery**: The process of notifying a Requestor via email that their Translation Result is ready, providing a link to the result rather than attaching the file.
