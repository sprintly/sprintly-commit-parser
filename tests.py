import unittest

from sprintly_commit_parser import CommitParser


def make_test(message, expected):
    def run(self):
        result = self.parse_commit(message)
        self.assertEquals(expected, result)
    return run


class MessagesTester(type):
    def __new__(cls, name, bases, attrs):
        cases = attrs.get('cases', [])

        for doc, message, expected in cases:
            test = make_test(message, expected)
            test.__name__ = name
            test.__doc__ = doc
            test_name = 'test_commit_parser_%s' % doc.lower().replace(' ', '_')
            attrs[test_name] = test
        return super(MessagesTester, cls).__new__(cls, name, bases, attrs)


class CommitParserTests(unittest.TestCase):
    __metaclass__ = MessagesTester

    cases = [
        ['And', "Built teaser page with signup form that posts to the 'nubook' user's subscriber list. This closes #77 and #78 Ref #1",
            [{'close_ticket': 77}, {'close_ticket': 78}, {'reference_ticket': 1}]],
        ['See', 'Added blah to blah. See: #1.', [{'reference_ticket': 1}]],
        ['See alternate', 'Added blah to blah. See: ticket:1.', [{'reference_ticket': 1}]],
        ['Fixes alternate', 'Added blah to blah. fixes ticket:1.', [{'close_ticket': 1}]],
        ['Closes alternate', 'Added blah to blah. closes item:1.', [{'close_ticket': 1}]],
        ['Closes defect alternate', 'Added blah to blah. closes defect:1.', [{'close_ticket': 1}]],
        ['Fixes', 'Added blah to blah. Fixes #1.', [{'close_ticket': 1}]],
        ['Fixes task', 'Added blah to blah. Fixes Task #1.', [{'close_ticket': 1}]],
        ['Refs task', 'Added blah to blah. Refs Task #1.', [{'reference_ticket': 1}]],
        ['References', 'References #1.', [{'reference_ticket': 1}]],
        ['Fixes and', 'Added blah to blah. Fixes #1 and #2', [{'close_ticket': 1},
            {'close_ticket': 2}]],
        ['Fixes multiple and', 'Added blah to blah. Fixes #1, #4, and #2', [{'close_ticket': 1},
            {'close_ticket': 4}, {'close_ticket': 2}]],
        ['Fixed', 'Added blah to blah. Fixed #1.', [{'close_ticket': 1}]],
        ['Fixes and again', "Stubbed out some from a table's properties. Fixes #4 and #5.",
            [{'close_ticket': 4}, {'close_ticket': 5}]],
        ['Reopens and', "Stubbed out some from a table's properties. Reopens #4 and #5.",
            [{'reopen_ticket': 4}, {'reopen_ticket': 5}]],
        ['Ref', 'Modified card popover to blockers when hovering a blocked card. Ref #123',
            [{'reference_ticket': 123}]],
        ['Refs', 'Modified card popover to blockers when hovering a blocked card. Refs #123',
            [{'reference_ticket': 123}]],
    ]

    def setUp(self):
        self.parse_commit = CommitParser()

    def test_invalid_item_command(self):
        """Make sure invalid commands are not returned."""
        message = 'Added a widget. Analyzes #33'
        commands = self.parse_commit(message)
        self.assertEquals([], commands)

if __name__ == '__main__':
    unittest.main()
