import sublime
import sublime_plugin
import os

class FormatLogCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_path = self.view.file_name()
        if file_path and len(file_path) > 0:
            folder_name, file_name = os.path.split(self.view.file_name())
            self.view.window().run_command('exec', {'cmd': ['ruby', '-pi', '-e', 'gsub(/\\\\r\\\\n|\\\\n\\\\n/, "\n")', file_path], 'working_dir': folder_name})
            self.view.window().run_command('exec', {'cmd': ['ruby', '-pi', '-e', 'gsub("\\\\n", "")', file_path], 'working_dir': folder_name})
            self.view.window().run_command('exec', {'cmd': ['ruby', '-pi', '-e', 'gsub("\\\\s", "/")', file_path], 'working_dir': folder_name})
            self.view.window().run_command('exec', {'cmd': ['ruby', '-pi', '-e', 'gsub("\\\\t", "    ")', file_path], 'working_dir': folder_name})
        else:
            replacements = self.view.find_all("\\\\r\\\\n|\\\\n\\\\n")
            replacements.reverse()
            for replacement in replacements:
                self.view.replace(edit, replacement, "\n")

            replacements = self.view.find_all("\\\\n")
            replacements.reverse()
            for replacement in replacements:
                self.view.erase(edit, replacement)

            replacements = self.view.find_all("\\\\s")
            replacements.reverse()
            for replacement in replacements:
                self.view.replace(edit, replacement, "/")

            replacements = self.view.find_all("\\\\t")
            replacements.reverse()
            for replacement in replacements:
                self.view.replace(edit, replacement, "    ")


class FilterLogCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()[0]
        if len(selection) != 0:
            word = self.view.substr(selection)
        if word and len(word) > 0:
            region = sublime.Region(0, self.view.size())
            lines = self.view.split_by_newlines(region)
            scratch = self.view.window().new_file()
            scratch.set_scratch(True)
            scratch_edit = scratch.begin_edit('file_temp')
            for line in lines:
                lineStr = self.view.substr(line)
                if word in lineStr:
                    scratch.insert(scratch_edit, 0, lineStr + "\n")
            scratch.end_edit(scratch_edit)

    def is_enabled(self):
        return self.view.sel()[0] and len(self.view.sel()[0]) > 0

# def encode(text):
#     return base64.b64encode(text)

# class EncodeCommand(sublime_plugin.TextCommand):
#     def run(self, edit):
#         e = self.view.begin_edit('encode')
#         regions = [region for region in self.view.sel()]

#         def get_end(region):
#             return region.end()
#         regions.sort(key=get_end, reverse=True)

#         for region in regions:
#             if region.empty():
#                 continue
#             text = self.view.substr(region)
#             replacement = encode(text)
#             self.view.replace(edit, region, replacement)
#         self.view.end_edit(e)





