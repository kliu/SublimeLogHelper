import sublime
import sublime_plugin
import subprocess
import functools

settings = sublime.load_settings('LogHelper.sublime-settings')

class FormatLogCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_path = self.view.file_name()
        if file_path and len(file_path) > 0 and settings.get('automatic_save_formated_file'):
            subprocess.call(['ruby', '-pi', '-e', 'gsub(/\\\\r\\\\n|\\\\n\\\\n|\\\\n/, "\n")', file_path])
            subprocess.call(['ruby', '-pi', '-e', 'gsub("\\\\s", "/")', file_path])
            subprocess.call(['ruby', '-pi', '-e', 'gsub("\\\\t", "    ")', file_path])
            sublime.set_timeout(functools.partial(self.view.run_command, 'revert'), 0)
        else:
            replacements = self.view.find_all(r"\\r\\n|\\n\\n|\\n")
            replacements.reverse()
            for replacement in replacements:
                self.view.replace(edit, replacement, "\n")

            replacements = self.view.find_all(r"\\s")
            replacements.reverse()
            for replacement in replacements:
                self.view.replace(edit, replacement, "/")

            replacements = self.view.find_all(r"\\t")
            replacements.reverse()
            for replacement in replacements:
                self.view.replace(edit, replacement, "    ")


class FilterLogCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        words = set()
        for selection in self.view.sel():
            if selection.size() != 0:
                words.add(self.view.substr(selection))
        region = sublime.Region(0, self.view.size())
        lines = self.view.split_by_newlines(region)
        lines.reverse()
        scratch = self.view.window().new_file()
        scratch.set_scratch(True)
        scratch_edit = scratch.begin_edit('file_temp')
        for line in lines:
            lineStr = self.view.substr(line)
            for word in words:
                if word in lineStr:
                    scratch.insert(scratch_edit, 0, lineStr + "\n")
        scratch.end_edit(scratch_edit)

    def is_enabled(self):
        for region in self.view.sel():
            if region.size() != 0:
                return True;
        return False;


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





