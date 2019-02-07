    # Cleanup the repo
    mock_repository.update(clean=True)

def test_analyze_patch():
    from static_analysis_bot.revisions import Revision
    from static_analysis_bot import Issue

    class MyIssue(Issue):
        def __init__(self, path, line):
            self.path = path
            self.line = line
            self.nb_lines = 1

        def as_dict():
            return {}

        def as_markdown():
            return ''

        def as_text():
            return ''

        def validates():
            return True

    issue_in_new_file = MyIssue('new.txt', 1)
    issue_in_existing_file_touched_line = MyIssue('modified.txt', 3)
    issue_in_existing_file_not_changed_line = MyIssue('modified.txt', 1)
    issue_in_existing_file_added_line = MyIssue('added.txt', 4)
    issue_in_not_changed_file = MyIssue('notexisting.txt', 1)

    rev = Revision()
    rev.patch = '''
diff --git a/new.txt b/new.txt
new file mode 100644
index 00000000..83db48f8
--- /dev/null
+++ b/new.txt
@@ -0,0 +1,3 @@
+line1
+line2
+line3
diff --git a/modified.txt b/modified.txt
index 84275f99..cbc9b72a 100644
--- a/modified.txt
+++ b/modified.txt
@@ -1,4 +1,4 @@
 line1
 line2
-line3
+line7
 line4
diff --git a/added.txt b/added.txt
index 83db48f8..84275f99 100644
--- a/added.txt
+++ b/added.txt
@@ -1,3 +1,4 @@
 line1
 line2
 line3
+line4
'''

    rev.analyze_patch()
    assert 'new.txt' in rev.lines
    assert rev.lines['new.txt'] == [1, 2, 3]
    assert 'modified.txt' in rev.lines
    assert rev.lines['modified.txt'] == [3]
    assert 'added.txt' in rev.lines
    assert rev.lines['added.txt'] == [4]
    assert 'new.txt' in rev.files
    assert 'modified.txt' in rev.files
    assert 'added.txt' in rev.files

    assert rev.contains(issue_in_new_file)
    assert rev.contains(issue_in_existing_file_touched_line)
    assert not rev.contains(issue_in_existing_file_not_changed_line)
    assert rev.contains(issue_in_existing_file_added_line)
    assert not rev.contains(issue_in_not_changed_file)