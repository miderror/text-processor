import json


class FileManager:
    def __init__(self):
        self.file_name = None
        self.data = {"pages": []}

    def new_file(self):
        self.file_name = None
        self.data = {"pages": [""]}

    def load_file(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
        self.file_name = file_name

    def save_file(self, file_name):
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
        self.file_name = file_name

    def get_page_content(self, page_num):
        try:
            return self.data["pages"][page_num]
        except IndexError:
            return ""

    def set_page_content(self, page_num, content):
        if page_num < len(self.data["pages"]):
            self.data["pages"][page_num] = content
        else:
            self.data["pages"].append(content)

    def new_page(self):
        self.data["pages"].append("")

    @property
    def num_pages(self):
        return len(self.data["pages"])
