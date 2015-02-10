import re
import unittest

from sprintly_commit_parser import CommitParser


class CommitParserTests(unittest.TestCase):

    messages_to_test = [
        ["Built teaser page with signup form that posts to the 'nubook' user's subscriber list. This closes #77 and #78 Ref #1", [{'close_ticket': 77}, {'close_ticket': 78}, {'reference_ticket': 1}]],
        ['Added blah to blah. See: #1.', [{'reference_ticket': 1}]],
        ['Added blah to blah. See: ticket:1.', [{'reference_ticket': 1}]],
        ['Added blah to blah. fixes ticket:1.', [{'close_ticket': 1}]],
        ['Added blah to blah. closes item:1.', [{'close_ticket': 1}]],
        ['Added blah to blah. closes defect:1.', [{'close_ticket': 1}]],
        ['Added blah to blah. Fixes #1.', [{'close_ticket': 1}]],
        ['Added blah to blah. Fixes Task #1.', [{'close_ticket': 1}]],
        ['Added blah to blah. Refs Task #1.', [{'reference_ticket': 1}]],
        ['References #1.', [{'reference_ticket': 1}]],
        ['Added blah to blah. Fixes #1 and #2', [{'close_ticket': 1},
            {'close_ticket': 2}]],
        ['Added blah to blah. Fixes #1, #4, and #2', [{'close_ticket': 1},
            {'close_ticket': 4}, {'close_ticket': 2}]],
        ['Added blah to blah. Fixed #1.', [{'close_ticket': 1}]],
        ['Added blah to blah. Fixed #1. Added 3 hours.', [{'close_ticket': 1},
            {'add_hours': 3.0}]],
        ['Added blah to blah. Fixed #1. Added 3 hours. See #2 and #1.', [
            {'close_ticket': 1}, {'reference_ticket': 2},
            {'reference_ticket': 1}, {'add_hours': 3.0}]],
        ['Added blah to blah. Fixed #1. Knocked off 3.5 hours.', [
            {'close_ticket': 1}, {'minus_hours': 3.5}]],
        ["Stubbed out some from a table's properties. Fixes #4 and #5.",
            [{'close_ticket': 4}, {'close_ticket': 5}]],
        ["Stubbed out some from a table's properties. Reopens #4 and #5.",
            [{'reopen_ticket': 4}, {'reopen_ticket': 5}]],
        ['Modified card popover to blockers when hovering a blocked card. Ref #123',
            [{'reference_ticket': 123}]],
        ['Modified card popover to blockers when hovering a blocked card. Refs #123',
            [{'reference_ticket': 123}]],
    ]

    def setUp(self):
        self.parse_commit = CommitParser()

    def test_messages(self):
        """Make sure various commit messages are parsed as expected."""
        for tests in CommitParserTests.messages_to_test:
            message = tests[0]
            expected = tests[1]
            commands = self.parse_commit(message)
            self.assertEquals(expected, commands)

    def test_invalid_item_command(self):
        """Make sure invalid commands are not returned."""
        message = 'Added a widget. Analyzes #33'
        commands = self.parse_commit(message)
        self.assertEquals([], commands)

    def test_invalid_hour_command(self):
        """Make sure unknown hour commands are ignored."""
        message = 'Added a widget. Multiply 7 hours.'
        commands = self.parse_commit(message)
        self.assertEquals([], commands)

    def test_unknown_command_in_regexp(self):
        """Make sure unknown command doesn't throw a KeyError."""
        hour_words = CommitParser._hour_words
        hour_words.append('multiply')
        hour_command = '(%s) ([0-9]+(\.[0-9]+)?) (hours|hrs|hr|hour)' % \
            '|'.join(hour_words)
        CommitParser._hours_re = re.compile(hour_command, re.I)
        message = 'Added a widget. Multiply 7 hours.'
        commands = self.parse_commit(message)
        self.assertEquals([], commands)


if __name__ == '__main__':
    unittest.main()
