# from django.forms.widgets import FileInput


# class MultiFileInput(FileInput):
#     def __init__(self, attrs=None):
#         attrs = attrs or {}
#         attrs.update({'multiple': True})  # فعال کردن multiple
#         super().__init__(attrs)

#     def value_from_datadict(self, data, files, name):
#         # بازیابی چندین فایل از data dict
#         return files.getlist(name)