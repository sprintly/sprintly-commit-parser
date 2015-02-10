import re


TICKET_PREFIX = '(?:#|(?:ticket|issue|item|defect|bug)[: ]?)'
TICKET_RE = re.compile(TICKET_PREFIX + '([0-9]+)', re.I | re.UNICODE)


def items_mentioned(string):
    if string is None or string.strip() == "":
        return []
    return [int(x) for x in TICKET_RE.findall(string)]


class CommitParser(object):
    _ticket_reference = TICKET_PREFIX + '[0-9]+'
    _ticket_command = (r'(?P<action>[A-Za-z]*) ?(task|issue|defect|bug|item|ticket|:)?.?'
        '(?P<ticket>%s(?:(?:[, &]*|[ ,]+?and[ ]?)%s)*)' %
        (_ticket_reference, _ticket_reference))

    _command_re = re.compile(_ticket_command, re.I | re.UNICODE)
    _ticket_re = re.compile(TICKET_PREFIX + '([0-9]+)', re.I | re.UNICODE)

    _hour_words = ['added', 'knocked off', 'killed', 'completed', 'finished',
        'subtract', 'subtracted', 'subtracts', 'adds', 'add']
    _hour_command = '(%s) ([0-9]+(\.[0-9]+)?) (hours|hrs|hr|hour)' % \
        '|'.join(_hour_words)
    _hours_re = re.compile(_hour_command, re.I | re.UNICODE)

    _parsers = ['commands', 'hours']
    _item_cmds = {'close': 'close_ticket',
                  'closed': 'close_ticket',
                  'closes': 'close_ticket',
                  'finish': 'close_ticket',
                  'finished': 'close_ticket',
                  'finishes': 'close_ticket',
                  'fix': 'close_ticket',
                  'fixed': 'close_ticket',
                  'fixes': 'close_ticket',
                  'breaks': 'reopen_ticket',
                  'unfixes': 'reopen_ticket',
                  'reopen': 'reopen_ticket',
                  'reopens': 'reopen_ticket',
                  're-open': 'reopen_ticket',
                  're-opens': 'reopen_ticket',
                  'addresses': 'reference_ticket',
                  're': 'reference_ticket',
                  'ref': 'reference_ticket',
                  'references': 'reference_ticket',
                  'refs': 'reference_ticket',
                  'start': 'reference_ticket',
                  'starts': 'reference_ticket',
                  'see': 'reference_ticket'}

    _hour_cmds = {'added': 'add_hours',
                  'adds': 'add_hours',
                  'add': 'add_hours',
                  'knocked off': 'minus_hours',
                  'killed': 'minus_hours',
                  'completed': 'minus_hours',
                  'finished': 'minus_hours',
                  'subtract': 'minus_hours',
                  'subtracted': 'minus_hours',
                  'subtracts': 'minus_hours'}

    def __call__(self, message):
        # TODO(justinabrahms): Consider using a defaultdict(list) here, rather
        # than a list of dicts.
        commands = []
        for p in CommitParser._parsers:
            parser = getattr(self, '_parse_%s' % p)
            if parser:
                new_commands = parser(message)
                if new_commands and isinstance(new_commands, list):
                    commands += new_commands

        return commands

    def _parse_commands(self, message):
        cmd_groups = CommitParser._command_re.findall(message)

        commands = []
        for cmd, junk, tkts in cmd_groups:
            try:
                command = CommitParser._item_cmds[cmd.lower()]
                tickets = items_mentioned(tkts)
                for t in tickets:
                    commands.append({command: int(t)})
            except KeyError:
                pass

        return commands

    def _parse_hours(self, message):
        hrs_groups = CommitParser._hours_re.findall(message)
        commands = []
        for cmd, hrs, blah, suffix in hrs_groups:
            try:
                command = {CommitParser._hour_cmds[cmd.lower()]: float(hrs)}
                commands.append(command)
            except KeyError:
                pass

        return commands
