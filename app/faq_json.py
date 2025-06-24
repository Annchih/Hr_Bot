import json
import os

class FAQManager:
    def __init__(self, file_path="faq.json"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _load(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def _save(self, faqs):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(faqs, f, indent=2, ensure_ascii=False)

    def get_all_faqs(self):
        return self._load()

    def add_faq(self, question, answer):
        faqs = self._load()
        new_id = max([faq["id"] for faq in faqs], default=0) + 1
        faqs.append({"id": new_id, "question": question, "answer": answer})
        self._save(faqs)

    def delete_faq(self, faq_id):
        faqs = [faq for faq in self._load() if faq["id"] != faq_id]
        self._save(faqs)

    def update_faq(self, faq_id, question=None, answer=None):
        faqs = self._load()
        for faq in faqs:
            if faq["id"] == faq_id:
                if question:
                    faq["question"] = question
                if answer:
                    faq["answer"] = answer
                break
        self._save(faqs)

    def get_faq_by_id(self, faq_id):
        faqs = self._load()
        for faq in faqs:
            if faq["id"] == faq_id:
                return faq["question"], faq["answer"]
        return "Вопрос не найден", "Ответ отсутствует"