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
            if line.begin() == v.size():
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
        regions = v.find_by_selector("punctuation.section.function.begin.python")
        for i, region in enumerate(regions):
            start = v.text_point(v.rowcol(region.begin())[0] + 1, 0)
            end = self.get_lines_in_function(start)
            regions[i] = sublime.Region(start - 1, end)
        v.fold(regions)
 