# about: Goto lines of interest by a user list that may use style detection
# help: https://community.notepad-plus-plus.org/topic/23039/faq-desk-how-to-install-and-run-a-script-in-pythonscript
# name: UserListGotoLine
# src: https://github.com/mpheath/user-list-goto-line-for-notepad-plus-plus

from Npp import editor, notepad, \
                FINDOPTION, FOLDLEVEL, LANGTYPE, \
                MESSAGEBOXFLAGS, SCINTILLANOTIFICATION

import random, re


class UserListGL():
    def __init__(self, max_length=120):
        '''Initialize an instance.'''

        # Create user list ids.
        self.list_id = []

        while len(self.list_id) < 2:
            list_id = random.randint(1000, 9999)

            if list_id not in self.list_id:
                self.list_id.append(list_id)

        # Set text maximum length for user list.
        self.max_length = max_length

        # Define a timestamp pattern for .LOG in files if needed.
        self.timestamp_pattern = None

        # Title used by messageBox.
        self.title = 'UserListGotoLine'

    def callback(self, args):
        '''Receive message from the user list.'''

        if args['listType'] == self.list_id[0]:
            m = re.match(r'\d+', args['text'])

            if not m:
                return

            line = m.group()
            line = int(line)
            editor.ensureVisible(line - 1)
            editor.setFirstVisibleLine(line - 1)
            editor.gotoLine(line - 1)

        elif args['listType'] == self.list_id[1]:
            text = args['text']

            if text.startswith('any word style'):
                self.any_word()
            elif text == 'bookmarks':
                self.bookmarks()
            elif text == 'change history':
                self.change_history()
            elif text == 'change history modified':
                self.change_history('mode_modified')
            elif text == 'change history reverted to modified':
                self.change_history('mode_reverted_to_modified')
            elif text == 'change history reverted to origin':
                self.change_history('mode_reverted_to_origin')
            elif text == 'change history saved':
                self.change_history('mode_saved')
            elif text == 'codes':
                self.codes()
            elif text == 'codes extended':
                self.codes('mode_extended')
            elif text == 'codes uppercase':
                self.codes('mode_uppercase')
            elif text == 'comments':
                self.comments()
            elif text == 'comments block':
                self.comments('mode_block')
            elif text == 'comments doc':
                self.comments('mode_doc')
            elif text == 'comments docline':
                self.comments('mode_docline')
            elif text == 'comments nested':
                self.comments('mode_nested')
            elif text == 'comments reminder':
                self.comments('mode_reminder')
            elif text.startswith('current char style'):
                self.current_char('mode_style')
            elif text == 'current selection':
                self.current_selection()
            elif text.startswith('current selection style'):
                self.current_selection('mode_style')
            elif text == 'current word':
                self.current_word()
            elif text.startswith('current word style'):
                self.current_word('mode_style')
            elif text == 'folds':
                self.folds()
            elif text == 'log':
                self.log()
            elif text == 'log error':
                self.log('mode_error')
            elif text == 'log fatal':
                self.log('mode_fatal')
            elif text == 'log warn':
                self.log('mode_warn')
            elif text == 'log timestamp':
                self.log('mode_timestamp')

    def register(self):
        '''Add the callback for the user list.'''

        editor.callback(self.callback, [SCINTILLANOTIFICATION.USERLISTSELECTION])

    def unregister(self):
        '''Remove the callback for the user list.'''

        editor.clearCallbacks(self.callback)

    def main(self):
        '''Show the main user list.'''

        lang_type = notepad.getLangType()
        lang_name = notepad.getLanguageName(lang_type)
        lang_lexer = editor.getLexerLanguage()

        items = set()

        # Any word.
        if editor.getWord(editor.getCurrentPos(), True):
            style_at = editor.getStyleAt(editor.getCurrentPos())
            items.add('any word style {}'.format(style_at))

        # Bookmarks.
        items.add('bookmarks')

        # Change history.
        if editor.getChangeHistory():
            if editor.canUndo():
                items.add('change history')
                items.add('change history modified')
                items.add('change history reverted to modified')
                items.add('change history reverted to origin')
                items.add('change history saved')

        # Codes.
        if lang_type not in (LANGTYPE.TXT,
                             LANGTYPE.CSS,
                             LANGTYPE.DIFF,
                             LANGTYPE.JSON,
                             LANGTYPE.JSON5,
                             LANGTYPE.RC,
                             LANGTYPE.SQL,
                             LANGTYPE.TOML,
                             LANGTYPE.XML):
            items.add('codes')

            if 'codes' in items:
                if lang_lexer in ('mssql',):
                    items.remove('codes')

            if lang_type in (LANGTYPE.BATCH,
                             LANGTYPE.INNO,
                             LANGTYPE.LUA,
                             LANGTYPE.SWIFT):
                items.add('codes extended')

            if lang_type in (LANGTYPE.AU3,
                             LANGTYPE.BASH,
                             LANGTYPE.COFFEESCRIPT,
                             LANGTYPE.CS,
                             LANGTYPE.D,
                             LANGTYPE.GDSCRIPT,
                             LANGTYPE.GOLANG,
                             LANGTYPE.INNO,
                             LANGTYPE.JAVA,
                             LANGTYPE.JAVASCRIPT,
                             LANGTYPE.LUA,
                             LANGTYPE.MATLAB,
                             LANGTYPE.PERL,
                             LANGTYPE.PHP,
                             LANGTYPE.POWERSHELL,
                             LANGTYPE.PYTHON,
                             LANGTYPE.RAKU,
                             LANGTYPE.RUBY,
                             LANGTYPE.RUST,
                             LANGTYPE.SWIFT):
                items.add('codes uppercase')

            if lang_type == LANGTYPE.USER:
                if 'dBASEPlus' in lang_name:
                    items.add('codes extended')

        # Comments.
        if lang_type not in (LANGTYPE.TXT,
                             LANGTYPE.JSON):
            items.add('comments')

            if lang_type in (LANGTYPE.AU3,
                             LANGTYPE.C,
                             LANGTYPE.COFFEESCRIPT,
                             LANGTYPE.CPP,
                             LANGTYPE.CS,
                             LANGTYPE.D,
                             LANGTYPE.ESCRIPT,
                             LANGTYPE.FREEBASIC,
                             LANGTYPE.GDSCRIPT,
                             LANGTYPE.GOLANG,
                             LANGTYPE.JAVA,
                             LANGTYPE.JAVASCRIPT,
                             LANGTYPE.LUA,
                             LANGTYPE.PHP,
                             LANGTYPE.POWERSHELL,
                             LANGTYPE.PYTHON,
                             LANGTYPE.RAKU,
                             LANGTYPE.RUBY,
                             LANGTYPE.RUST,
                             LANGTYPE.SWIFT,
                             LANGTYPE.SQL):
                items.add('comments block')

            elif lang_lexer in ('mssql',):
                items.add('comments block')

            if lang_type in (LANGTYPE.C,
                             LANGTYPE.COBOL,
                             LANGTYPE.CPP,
                             LANGTYPE.CS,
                             LANGTYPE.D,
                             LANGTYPE.FREEBASIC,
                             LANGTYPE.GOLANG,
                             LANGTYPE.JAVA,
                             LANGTYPE.JAVASCRIPT,
                             LANGTYPE.RAKU,
                             LANGTYPE.RUST,
                             LANGTYPE.SWIFT,
                             LANGTYPE.SQL):
                items.add('comments doc')

            if lang_type in (LANGTYPE.D,):
                items.add('comments docline')
                items.add('comments nested')

            if lang_type == LANGTYPE.NIM:
                if str(lang_lexer) == 'nim':
                    items.add('comments block')
                    items.add('comments doc')
                    items.add('comments docline')

            if lang_type == LANGTYPE.USER:
                if 'dBASEPlus' in lang_name:
                    items.add('comments block')

            items.add('comments reminder')

        # Current word/selection.
        start = editor.getSelectionStart()
        end = editor.getSelectionEnd()

        if start != end:
            items.add('current selection')

            text = editor.getTextRangeFull(start, end)

            if re.match(r'^\w+$', text):
                style_at = editor.getStyleAt(start)
                items.add('current selection style {}'.format(style_at))

        elif editor.getWord(editor.getCurrentPos(), True):
            items.add('current word')

            if lang_type != LANGTYPE.TXT:
                style_at = editor.getStyleAt(editor.getCurrentPos())
                items.add('current word style {}'.format(style_at))
        else:
            if lang_type != LANGTYPE.TXT:
                style_at = editor.getStyleAt(editor.getCurrentPos())
                items.add('current char style {}'.format(style_at))

        # Fold.
        if lang_type != LANGTYPE.TXT:
            if editor.getProperty('fold') != '0':
                items.add('folds')

        # Log.
        file = notepad.getCurrentFilename()

        if file.endswith('.log'):
            items.add('log')
            items.add('log error')
            items.add('log fatal')
            items.add('log warn')

        if lang_type == LANGTYPE.TXT:
            text = editor.getTextRangeFull(0, 4)

            if text == '.LOG':
                items.add('log timestamp')

        items = sorted(items)

        self.user_list_show(self.list_id[1], items)

    def any_word(self):
        '''Show any word lines with style at caret.'''

        pattern = r'\w+'
        style = editor.getStyleAt(editor.getCurrentPos())
        self.search(pattern, [style], True)

    def bookmarks(self):
        '''Show bookmarked lines.'''

        bookmark = notepad.getBookMarkID()
        mask = 1 << bookmark
        items = []
        tab_size = editor.getTabWidth() or 4

        for line in range(editor.getLineCount()):
            if editor.markerGet(line) & mask != 0:
                text = editor.getLine(line).rstrip()
                text = text.replace('\t', ' ' * tab_size)

                item = '{:<4}  {}'.format(line + 1, text[:self.max_length])
                items.append(item)

        self.user_list_show(self.list_id[0], items)

    def change_history(self, mode=None):
        '''Show change history lines with multiple modes.'''

        SC_MARKNUM_HISTORY_REVERTED_TO_ORIGIN = 21
        SC_MARKNUM_HISTORY_SAVED = 22
        SC_MARKNUM_HISTORY_MODIFIED = 23
        SC_MARKNUM_HISTORY_REVERTED_TO_MODIFIED = 24

        if mode == 'mode_modified':
            mask = 1 << SC_MARKNUM_HISTORY_MODIFIED
        elif mode == 'mode_reverted_to_modified':
            mask = 1 << SC_MARKNUM_HISTORY_REVERTED_TO_MODIFIED
        elif mode == 'mode_reverted_to_origin':
            mask = 1 << SC_MARKNUM_HISTORY_REVERTED_TO_ORIGIN
        elif mode == 'mode_saved':
            mask = 1 << SC_MARKNUM_HISTORY_SAVED
        else:
            mask = (1 << SC_MARKNUM_HISTORY_REVERTED_TO_ORIGIN|
                    1 << SC_MARKNUM_HISTORY_SAVED|
                    1 << SC_MARKNUM_HISTORY_MODIFIED|
                    1 << SC_MARKNUM_HISTORY_REVERTED_TO_MODIFIED)

        items = []
        tab_size = editor.getTabWidth() or 4

        for line in range(editor.getLineCount()):
            if editor.markerGet(line) & mask != 0:
                text = editor.getLine(line).rstrip()
                text = text.replace('\t', ' ' * tab_size)

                item = '{:<4}  {}'.format(line + 1, text[:self.max_length])
                items.append(item)

        self.user_list_show(self.list_id[0], items)

    def codes(self, mode=None):
        '''Show code lines with style and with multiple modes.'''

        def lang_not_setup():
            notepad.messageBox('Language not setup.\n\n'
                               'Name: ' + repr(lang_name) + '\n'
                               'Lexer: ' + repr(lang_lexer) + '\n'
                               'Type: ' + repr(lang_type),
                               self.title, MESSAGEBOXFLAGS.ICONEXCLAMATION)

        lang_type = notepad.getLangType()
        lang_name = notepad.getLanguageName(lang_type)
        lang_lexer = editor.getLexerLanguage()
        style = None

        re_upper = r'\b\u[\u_\d]+\b'

        # Set regex pattern and styles to detect.
        if lang_type == LANGTYPE.ADA:
            pattern = r'^\h*\K(?:function|procedure)\b'
            style = [1]
        elif lang_type == LANGTYPE.ASM:
            pattern = r'^\h*\K[A-Za-z_$][\w$]*(?=:)'
            style = [5]
        elif lang_type == LANGTYPE.AU3:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [9]
            else:
                pattern = r'(?i)^(?:func|\h*#region)\b'
                style = [5, 12]
        elif lang_type == LANGTYPE.AVS:
            pattern = r'^\h*\Kfunction\b'
            style = [6]
        elif lang_type == LANGTYPE.BASH:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [8, 9]
            else:
                pattern = r'^\h*\K(?:function\b|^\w+\h*\(\h*\)\h*\{)'
                style = [4, 8]
        elif lang_type == LANGTYPE.BATCH:
            if mode == 'mode_extended':
                pattern = r'(?i)^:\w+|\b(?:call|goto|exit)\b'
                style = [2, 3]
            else:
                pattern = r'^:\w+'
                style = [3]
        elif lang_type == LANGTYPE.COBOL:
            pattern = r'^\h*\K.'
            style = [5]
        elif lang_type == LANGTYPE.COFFEESCRIPT:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [11, 25]
            else:
                pattern = r'^\h*\K\w+\h*=\h*(?:\(.*?\))?\h*->'
                style = [11]
        elif lang_type == LANGTYPE.CMAKE:
            pattern = r'^\h*\K\w+\h*\('
            style = [5]
        elif lang_type == LANGTYPE.CS:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [11]
            else:
                pattern = r'\bclass\b'
                style = [16]
        elif lang_type == LANGTYPE.D:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [14]
            else:
                pattern = r'^\h*\Kclass\b'
                style = [6]
        elif lang_type in (LANGTYPE.FORTRAN,
                           LANGTYPE.FORTRAN_77):
            pattern = r'(?i)^\h*\K(?:function|subroutine)\b'
            style = [8]
        elif lang_type == LANGTYPE.FREEBASIC:
            pattern = r'(?i)^\h*\K(?:function|sub)\b'
            style = [3]
        elif lang_type == LANGTYPE.GDSCRIPT:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [11]
            else:
                pattern = r'^\h*\K(?:class|func)\b'
                style = [5]
        elif lang_type == LANGTYPE.GOLANG:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [11]
            else:
                pattern = r'^\h*\Kfunc\b'
                style = [5]
        elif lang_type == LANGTYPE.HTML:
            pattern = r'(?i)^\h*\K<(?:head|body|style|title|h[1-6])\b'
            style = [1]
        elif lang_type == LANGTYPE.INI:
            pattern = r'^\h*\K\[.+?\]'
            style = [2]
        elif lang_type == LANGTYPE.INNO:
            if mode == 'mode_extended':
                pattern = r'^\[.+?\]|^\h*\K(?:function|procedure)\b'
                style = [4, 8]
            elif mode == 'mode_uppercase':
                pattern = re_upper
                style = [0]
            else:
                pattern = r'^\[.+?\]'
                style = [4]
        elif lang_type == LANGTYPE.JAVA:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [11]
            else:
                pattern = r'\bclass\b'
                style = [16]
        elif lang_type == LANGTYPE.JAVASCRIPT:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [11]
            else:
                pattern = r'\bfunction\b'
                style = [5]
        elif lang_type == LANGTYPE.LUA:
            if mode == 'mode_extended':
                pattern = r'^\h*\K(?:function|local function|if|elseif|else)\b'
            elif mode == 'mode_uppercase':
                pattern = re_upper
                style = [11]
            else:
                pattern = r'^\h*\K(?:function|local function)\b'
                style = [5]
        elif lang_type == LANGTYPE.MAKEFILE:
            pattern = r':(?:\h|$)'
            style = [4]
        elif lang_type == LANGTYPE.MATLAB:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [7]
            else:
                pattern = r'\b(?:classdef|function)\b'
                style = [4]
        elif lang_type == LANGTYPE.MMIXAL:
            pattern = r'^\w'
            style = [2]
        elif lang_type == LANGTYPE.NIM:
            pattern = r'\b(?:func|method|proc)\b'

            if str(lang_lexer) == 'nimrod':
                style = [5, 11]
            else:
                style = [8]
        elif lang_type == LANGTYPE.NSIS:
            pattern = r'^\h*\K(?:Function|PageEx|SectionGroup|Section)\b'
            style = [9, 15, 17]
        elif lang_type == LANGTYPE.PASCAL:
            pattern = r'^\h*\K(?:function|procedure|constructor|destructor)\b'
            style = [9]
        elif lang_type == LANGTYPE.PERL:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [11]
            else:
                pattern = r'^\h*\Ksub\b'
                style = [5]
        elif lang_type == LANGTYPE.PHP:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [123]
            else:
                pattern = r'^\h*\K(?:function|class)\b'
                style = [121]
        elif lang_type == LANGTYPE.POWERSHELL:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [5]
            else:
                pattern = r'^\h*\K(?:filter|function)\b'
                style = [8]
        elif lang_type == LANGTYPE.PROPS:
            pattern = r'^\h*\K.+?='
            style = [5]
        elif lang_type == LANGTYPE.PYTHON:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [11]
            else:
                pattern = r'^\h*\K(?:async\h){0,1}(?:class|def)\b'
                style = [5]
        elif lang_type == LANGTYPE.REGISTRY:
            pattern = r'^\h*\K\[.+?\]'
            style = [6, 7]
        elif lang_type == LANGTYPE.RAKU:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [23]
            else:
                pattern = r'^\h*\K(?:class|(?:multi\h+)?method|role|submethod|sub)\b'
                style = [19, 20]
        elif lang_type == LANGTYPE.RUBY:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [11]
            else:
                pattern = r'^\h*\K(?:class|def|module)\b'
                style = [5]
        elif lang_type == LANGTYPE.RUST:
            if mode == 'mode_uppercase':
                pattern = re_upper
                style = [17]
            else:
                pattern = r'\b(?:fn|impl)\b'
                style= [6]
        elif lang_type == LANGTYPE.SWIFT:
            if mode == 'mode_extended':
                pattern = (r'\b(?:class|enum|extension|func|'
                           r'(?<!self\.)(?:deinit|init)|'
                           r'protocol|struct|subscript)\b')

                style = [5]
            elif mode == 'mode_uppercase':
                pattern = re_upper
                style = [11]
            else:
                pattern = r'\b(?:class|func)\b'
                style = [5]
        elif lang_type == LANGTYPE.VB:
            pattern = r'(?i)(?<!end\h)(?<!exit\h)(?:class|function|module|sub)\b'
            style = [3]
        elif lang_type == LANGTYPE.USER:
            if 'dBASEPlus' in lang_name:
                if mode == 'mode_extended':
                    pattern = r'(?:^\h*\K(?:function|procedure|with)\b|\bclass\b)(?!\h*=)'
                else:
                    pattern = r'(?:^\h*\K(?:function|procedure)\b|\bclass\b)(?!\h*=)'

                style = [4, 14]
            elif 'NppExec' in lang_name:
                pattern = r'^\h*:{1,2}'
                style = [6, 7]
            elif 'Markdown' in lang_name:
                pattern = r'^(?:#{1,6}\h|\h*\K\[.+?\]:\h+(?:http|www))'
                style = [2, 16]
            else:
                lang_not_setup()
                return
        else:
            lang_not_setup()
            return

        self.search(pattern, style, pattern.endswith('.'))

    def comments(self, mode=None):
        '''Show comment lines with style and with multiple modes.'''

        def lang_not_setup():
            notepad.messageBox('Language not setup.\n\n'
                               'Name: ' + repr(lang_name) + '\n'
                               'Lexer: ' + repr(lang_lexer) + '\n'
                               'Type: ' + repr(lang_type),
                               self.title, MESSAGEBOXFLAGS.ICONEXCLAMATION)

        lang_type = notepad.getLangType()
        lang_name = notepad.getLanguageName(lang_type)
        lang_lexer = editor.getLexerLanguage()
        style = None

        # Set pattern for search.
        if mode == 'mode_reminder':
            pattern = r'\b(?:debug|reminder|todo):'
        else:
            pattern = r'^\h*\K.'

            if lang_type == LANGTYPE.BATCH:
                pattern = r'^\h*@?\K.'
            elif lang_type == LANGTYPE.RAKU:
                if mode == 'mode_doc':
                    pass
                elif mode == 'mode_block':
                    pattern = r'(?<=#`).|^.'
                else:
                    pattern = r'^\h*\K(?!#`)#'

        # Set styles to detect.
        if lang_type == LANGTYPE.ADA:
            style = [10]
        elif lang_type == LANGTYPE.ASM:
            style = [1, 15]
        elif lang_type == LANGTYPE.AU3:
            if mode == 'mode_block':
                style = [2]
            else:
                style = [1]
        elif lang_type == LANGTYPE.AVS:
            style = [3]
        elif lang_type == LANGTYPE.BASH:
            style = [2]
        elif lang_type == LANGTYPE.BATCH:
            style = [1]
        elif lang_type in (LANGTYPE.C,
                           LANGTYPE.CPP,
                           LANGTYPE.CS,
                           LANGTYPE.GOLANG,
                           LANGTYPE.JAVA,
                           LANGTYPE.JAVASCRIPT,
                           LANGTYPE.SWIFT):
            if mode == 'mode_block':
                style = [1]
            elif mode == 'mode_doc':
                style = [3]
            else:
                style = [2]
        elif lang_type == LANGTYPE.CMAKE:
            style = [1]
        elif lang_type == LANGTYPE.COBOL:
            if mode == 'mode_doc':
                style = [3]
            else:
                style = [2]
        elif lang_type == LANGTYPE.COFFEESCRIPT:
            if mode == 'mode_block':
                style = [22]
            else:
                style = [2]
        elif lang_type == LANGTYPE.CSS:
            style = [9]
        elif lang_type == LANGTYPE.D:
            if mode == 'mode_block':
                style = [1]
            elif mode == 'mode_doc':
                style = [3]
            elif mode == 'mode_docline':
                style = [15]
            elif mode == 'mode_nested':
                style = [4]
            else:
                style = [2]
        elif lang_type == LANGTYPE.DIFF:
            style = [1]
        elif lang_type == LANGTYPE.ESCRIPT:
            if mode == 'mode_block':
                style = [1]
            else:
                style = [2]
        elif lang_type == LANGTYPE.FREEBASIC:
            if mode == 'mode_block':
                style = [19]
            elif mode == 'mode_doc':
                style = [20]
            else:
                style = [1]
        elif lang_type in (LANGTYPE.FORTRAN,
                           LANGTYPE.FORTRAN_77):
            style = [1]
        elif lang_type == LANGTYPE.GDSCRIPT:
            if mode == 'mode_block':
                style = [12]
            else:
                style = [1]
        elif lang_type == LANGTYPE.HTML:
            style = [9, 20, 42, 43, 44, 58, 72, 82, 92, 107, 124, 125]
        elif lang_type in (LANGTYPE.INI,
                           LANGTYPE.PROPS):
            style = [1]
        elif lang_type == LANGTYPE.INNO:
            style = [1, 7]
        elif lang_type == LANGTYPE.JSON5:
            style = [6]
        elif lang_type == LANGTYPE.LUA:
            if mode == 'mode_block':
                style = [1]
            else:
                style = [2]
        elif lang_type == LANGTYPE.MAKEFILE:
            style = [1]
        elif lang_type == LANGTYPE.MATLAB:
            style = [1]
        elif lang_type == LANGTYPE.MMIXAL:
            style = [1]
        elif lang_type == LANGTYPE.NIM:
            if str(lang_lexer) == 'nimrod':
                style = [1]
            else:
                if mode == 'mode_block':
                    style = [1]
                elif mode == 'mode_doc':
                    style = [2]
                elif mode == 'mode_docline':
                    style = [4]
                else:
                    style = [3]
        elif lang_type == LANGTYPE.NSIS:
            style = [1, 18]
        elif lang_type == LANGTYPE.PASCAL:
            style = [2, 3, 4]
        elif lang_type == LANGTYPE.PERL:
            style = [2, 3]
        elif lang_type == LANGTYPE.PHP:
            if mode == 'mode_block':
                style = [124]
            else:
                style = [125]
        elif lang_type == LANGTYPE.POWERSHELL:
            if mode == 'mode_block':
                style = [13, 16]
            else:
                style = [1]
        elif lang_type == LANGTYPE.PYTHON:
            if mode == 'mode_block':
                style = [12]
            else:
                style = [1]
        elif lang_type == LANGTYPE.RAKU:
            if mode == 'mode_block':
                style = [3]
            elif mode == 'mode_doc':
                style = [4]
            else:
                style = [2]
        elif lang_type == LANGTYPE.RC:
            style = [2]
        elif lang_type == LANGTYPE.REGISTRY:
            style = [1]
        elif lang_type == LANGTYPE.RUBY:
            if mode == 'mode_block':
                style = [3]
            else:
                style = [2]
        elif lang_type == LANGTYPE.RUST:
            if mode == 'mode_block':
                style = [1]
            elif mode == 'mode_doc':
                style = [4]
            else:
                style = [2]
        elif lang_type == LANGTYPE.SQL:
            if mode == 'mode_block':
                style = [1]
            elif mode == 'mode_doc':
                style = [3]
            else:
                style = [2]
        elif lang_type == LANGTYPE.TOML:
            style = [1]
        elif lang_type == LANGTYPE.XML:
            style = [9]
        elif lang_lexer == 'mssql':
            if mode == 'mode_block':
                style = [1]
            else:
                style = [2]
        elif lang_type == LANGTYPE.VB:
            style = [1]
        elif lang_type == LANGTYPE.USER:
            if 'dBASEPlus' in lang_name:
                if mode == 'mode_block':
                    style = [1]
                else:
                    style = [2, 19]
            elif 'NppExec' in lang_name:
                style = [2]
            elif 'Markdown' in lang_name:
                style = [1]
            else:
                lang_not_setup()
                return
        else:
            lang_not_setup()
            return

        self.search(pattern, style, pattern.endswith('.'))

    def current_selection(self, mode=None):
        '''Show current selection lines with option of style mode if a word.'''

        start = editor.getSelectionStart()
        end = editor.getSelectionEnd()

        if start != end:
            pattern = editor.getTextRangeFull(start, end)

            if mode == 'mode_style':
                style_at = editor.getStyleAt(start)
                self.search(pattern, [style_at], True)
            else:
                pattern = r'\Q' + pattern + r'\E'
                self.search(pattern, None)

    def current_char(self, mode=None):
        '''Show current char lines with option of style mode.'''

        ch = editor.getCharAt(editor.getCurrentPos())

        if ch:
            if ch < 0 or ch > 0x10FFFF:
                notepad.messageBox('Char ' + repr(ch) + ' '
                                   'is out of range from 0 to 0x10FFFF.',
                                   self.title, MESSAGEBOXFLAGS.ICONEXCLAMATION)
                return

            char = chr(ch)

            pattern = r'\Q' + char + r'\E'

            if mode == 'mode_style':
                style = editor.getStyleAt(editor.getCurrentPos())
                self.search(pattern, [style], True)
            else:
                self.search(pattern, None)

    def current_word(self, mode=None):
        '''Show current word lines with option of style mode.'''

        pattern = editor.getWord(editor.getCurrentPos(), True)

        if pattern:
            pattern = r'\b' + pattern + r'\b'

            if mode == 'mode_style':
                style = editor.getStyleAt(editor.getCurrentPos())
                self.search(pattern, [style], True)
            else:
                self.search(pattern, None)

    def folds(self):
        '''Show fold lines.'''

        if editor.getEndStyled() != editor.getTextLength():
            msg = ('Doc detected as not fully styled.\n\n'
                   'Try to run this script again after '
                   'scrolling the doc to the end '
                   'to force styling.\n\n')

            notepad.messageBox(msg + 'Click OK to cancel the search.',
                               self.title, MESSAGEBOXFLAGS.ICONEXCLAMATION)
            return

        items = []
        prev_level = FOLDLEVEL.BASE
        tab_size = editor.getTabWidth() or 4

        for line in range(editor.getLineCount()):
            level = editor.getFoldLevel(line) & FOLDLEVEL.NUMBERMASK

            if level > prev_level:
                text = editor.getLine(line - 1).rstrip()
                text = text.replace('\t', ' ' * tab_size)

                item = '{:<4}  {}'.format(line, text[:self.max_length])
                items.append(item)

            prev_level = level

        self.user_list_show(self.list_id[0], items)

    def log(self, mode=None):
        '''Show log lines based on mode.'''

        if mode == 'mode_error':
            pattern = r'(?i)\berrors?\b'
        elif mode == 'mode_fatal':
            pattern = r'(?i)\bfatal\b'
        elif mode == 'mode_warn':
            pattern = r'(?i)\bwarn(?:ings?)?\b'
        elif mode == 'mode_timestamp':
            pattern = self.timestamp_pattern

            if not pattern:
                def get_timestamp_pattern():
                    '''Create re pattern for timestamp from the current buffer.'''

                    # Get the first line with text after the .LOG line.
                    for line in range(1, editor.getLineCount()):
                        text = editor.getLine(line).rstrip()

                        if text:
                            break
                    else:
                        return

                    pattern = []

                    for item in text.split():
                        if not item:
                            continue

                        # Trim possible comma at the end of item.
                        if item.endswith(','):
                            end = ','
                            item = item[:-1]
                        else:
                            end = ''

                        # Append matching item patterns.
                        for s in (

                            # Time: '1:00'
                            r'\d{1,2}:\d{2}',

                            # Digits: '2025' '01' '01'
                            r'\d+',

                            # Word: 'AM' 'January' 'PST'
                            r'\w+',

                            # Date: '2025-01-01'
                            r'\d{4}-\d{2}-\d{2}',

                            # Date: '2025/01/01' '1/1/25'
                            r'\d{1,4}/\d{1,4}/\d{1,4}'):

                            if re.match(s + '$', item):
                                pattern.append(s + end)
                                break

                    # Return timestamp pattern else None.
                    if pattern:
                        return '^' + ' '.join(pattern) + '$'

                pattern = get_timestamp_pattern()
        else:
            pattern = r'(?i)\b(?:errors?|fatal|warn(?:ings?)?)\b'

        self.search(pattern, None)

    def search(self, pattern, style, require_styled=False):
        '''Search with a pattern in the current buffer.'''

        if not pattern:
            notepad.messageBox('Pattern to search is empty.',
                               self.title, MESSAGEBOXFLAGS.ICONEXCLAMATION)
            return

        msg = ('Doc detected as not fully styled.\n\n'
               'Try to run this script again after '
               'scrolling the doc to the end '
               'to force styling.\n\n')

        # Require doc to be fully styled to the end.
        if require_styled:
            if editor.getEndStyled() != editor.getTextLength():
                notepad.messageBox(msg + 'Click OK to cancel the search.',
                                   self.title, MESSAGEBOXFLAGS.ICONEXCLAMATION)
                return

        # Alert user if not styled to the end.
        if style is not None and editor.getEndStyled() != editor.getTextLength():
            reply = notepad.messageBox(msg + 'Click OK to continue the search '
                                       'without style {} validation which may '
                                       'show an inaccurate list.'
                                       .format(str(style)), self.title,
                                       MESSAGEBOXFLAGS.OKCANCEL|
                                       MESSAGEBOXFLAGS.ICONINFORMATION|
                                       MESSAGEBOXFLAGS.DEFBUTTON2)

            if reply == MESSAGEBOXFLAGS.RESULTOK:
                style = None
            else:
                return

        # Search and show the user list.
        flags = FINDOPTION.REGEXP | FINDOPTION.POSIX | FINDOPTION.MATCHCASE
        editor.setSearchFlags(flags)
        editor.targetWholeDocument()
        length = editor.getTextLength()
        start = editor.searchInTarget(pattern)

        if start == -1:
            notepad.messageBox('No items found with the search.', self.title,
                               MESSAGEBOXFLAGS.ICONEXCLAMATION)
            return

        items = []
        prev_line = -1
        tab_size = editor.getTabWidth() or 4

        while start >= 0:
            end = editor.getTargetEnd()
            style_at = editor.getStyleAt(start)

            if style is None or style_at in style:
                line = editor.lineFromPosition(start)

                if prev_line != line:
                    text = editor.getLine(line).rstrip()
                    text = text.replace('\t', ' ' * tab_size)

                    item = '{:<4}  {}'.format(line + 1, text[:self.max_length])
                    items.append(item)

                prev_line = line

            editor.setTargetStart(end + 1)
            editor.setTargetEnd(length)

            start = editor.searchInTarget(pattern)

        self.user_list_show(self.list_id[0], items)

    def user_list_show(self, list_id, items):
        '''Show the matched lines in another user list.'''

        if not items:
            notepad.messageBox('No items in the list to show.', self.title,
                               MESSAGEBOXFLAGS.ICONEXCLAMATION)
            return

        # Save current separators.
        saved = {'item_sep': editor.autoCGetSeparator(),
                 'type_sep': editor.autoCGetTypeSeparator()}

        # Set new separators.
        editor.autoCSetTypeSeparator(0x10)
        editor.autoCSetSeparator(0x7F)

        # Show the list.
        editor.userListShow(list_id, chr(0x7F).join(items))

        # Restore old separators.
        editor.autoCSetSeparator(saved['item_sep'])
        editor.autoCSetTypeSeparator(saved['type_sep'])


if __name__ == '__main__':
    try:
        user_list_gl
    except NameError:
        user_list_gl = UserListGL()
        user_list_gl.register()
    finally:
        user_list_gl.main()
