import json
import os

class FAQManager:
    def __init__(self, file_path="faq.json"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            self._save([]) 

    def _load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save(self, faqs):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(faqs, f, indent=2, ensure_ascii=False)

    def get_all_faqs(self):
        return self._load()

    def add_faq(self, question, answer):
        faqs = self._load()
        new_id = max((faq["id"] for faq in faqs), default=0) + 1
        faqs.append({"id": new_id, "question": question, "answer": answer})
        self._save(faqs)
        return new_id

    def delete_faq(self, faq_id):
        faqs = [faq for faq in self._load() if faq["id"] != faq_id]
        self._save(faqs)

    def update_faq(self, faq_id, question=None, answer=None):
        faqs = self._load()
        updated = False
        for faq in faqs:
            if faq["id"] == faq_id:
                if question is not None:
                    faq["question"] = question
                if answer is not None:
                    faq["answer"] = answer
                updated = True
                break
        if updated:
            self._save(faqs)
        return updated

    def get_faq_by_id(self, faq_id):
        for faq in self._load():
            if faq["id"] == faq_id:
                return faq["question"], faq["answer"]
        return None, None

    def get_id_by_question(self, question):
        question_clean = question.strip().lower()
        for faq in self._load():
            if faq["question"].strip().lower() == question_clean:
                return faq["id"]
        return None
