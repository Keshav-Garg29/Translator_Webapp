from abc import ABC, abstractmethod

class Translator(ABC):
    @abstractmethod
    def translate(self, text: str, target_lang: str) -> str:
        """Translates text to the target language."""
        pass

    @abstractmethod
    def translate_file(self, file_path: str, target_lang: str) -> str:
        """Translates a file and returns the path to the translated file."""
        pass

class FakeTranslator(Translator):
    def translate(self, text: str, target_lang: str) -> str:
        """A fake translation implementation for testing purposes."""
        return f"[FAKE TRANSLATION to {target_lang}]: {text}"

    def translate_file(self, file_path: str, target_lang: str) -> str:
        """Simulates translating a file by creating a translated version on disk."""
        import os
        import shutil

        # Get file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        # Handle text extraction simulation based on file type
        if ext == '.txt':
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception:
                content = "[Could not read text file content]"
        elif ext in ['.docx', '.pdf']:
            # In a real app, we'd use python-docx or PyPDF2 here.
            # For the FakeTranslator, we simulate extracted text.
            content = f"[Simulated extracted text from {ext} file content]"
        else:
            content = f"[Unsupported file format {ext}]"

        translated_content = self.translate(content, target_lang)

        # Create a translated file path
        base, _ = os.path.splitext(file_path)
        translated_path = f"{base}_translated{ext}"

        with open(translated_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        return translated_path
