# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin

class FoldPythonFunctions(sublime_plugin.TextCommand):

    def get_indentation(self, point):
        return self.view.indentation_level(point)

    def get_lines_in_function(self, start):
        v = self.view
        row = v.rowcol(start)[0]
        base_indentation = self.get_indentation(start)
        lines = []
        going = True
        while going:
            point = v.text_point(row, 0)
            line = v.line(point)
            if line.end() >= v.size():
                going = False
            if self.get_indentation(point) >= base_indentation or line.empty():
                row += 1
                lines.append(line)
            else:
                going = False

        # remove empty lines at the end
        for line in reversed(lines):
            if line.empty():
                row -= 1
            else:
                return v.text_point(row, 0) - 1

    def run(self, edit):
        v = self.view
        selection = v.sel()
        selection.clear()
        regions = v.find_by_selector("meta.function.python - punctuation.section.function.begin.python")
        for i, region in enumerate(regions):
            start = v.text_point(v.rowcol(region.begin())[0] + 1, 0)
            end = self.get_lines_in_function(start)
            regions[i] = sublime.Region(start - 1, end)
        v.fold(regions)

    def is_enabled(self):
        return 'source.python' in self.view.scope_name(0)
        

class FoldJavascriptFunctions(sublime_plugin.TextCommand):

    def moveTill(self, char_stop, pt, increment):
        char = self.view.substr(pt)
        size = self.view.size()
        while char != char_stop and 0 <= pt < size:
            pt += 1
            char = self.view.substr(pt)
        return pt

    def run(self, edit):
        v = self.view
        selection = v.sel()
        selection.clear()
        functions_name = v.find_by_selector("meta.function.declaration.js")
        for i, function_name in enumerate(functions_name):
            functions_name[i] = sublime.Region(self.moveTill('{', function_name.end(), 1) + 1)
        selection.add_all(functions_name)
        self.view.run_command('expand_selection', {'to': "brackets"})
        self.view.run_command('fold')
        selection.clear()

    def is_enabled(self):
        return 'source.js' in self.view.scope_name(0)