import re


TICKET_PREFIX = '(?:#|(?:ticket|issue|item|defect|bug)[: ]?)'
TICKET_ID = '(([0-9]+:)?([0-9]+))'
TICKET_RE = re.compile(TICKET_PREFIX + TICKET_ID, re.I | re.UNICODE)


def items_mentioned(string):
    if string is None or string.strip() == "":
        return []

    items = []
    for _ in TICKET_RE.findall(string):
        x = _[0]
        if ':' in x:
            product_id, item_number = x.split(':')
            ticket_id = {
                'product_id': int(product_id),
                'item_number': int(item_number)
            }
        else:
            ticket_id = int(x)

        print 'x = {0} -> ticket_id = {1}'.format(x, ticket_id)

        items.append(ticket_id)

    return items
#    return [int(x) for x in TICKET_RE.findall(string)]


class CommitParser(object):
    _ticket_reference = TICKET_PREFIX + TICKET_ID
    _ticket_command = (r'(?P<action>[A-Za-z]*) ?(task|issue|defect|bug|item|ticket|:)?.?'
        '(?P<ticket>%s(?:(?:[, &]*|[ ,]+?and[ ]?)%s)*)' % (_ticket_reference, _ticket_reference))

    _command_re = re.compile(_ticket_command, re.I | re.UNICODE)
    _parsers = ['commands']
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

        print cmd_groups

        commands = []

        x = lambda bit: (bit and bit not in [':'])

        for group in cmd_groups:
            bits = filter(bool, group)
            cmd, tkts = (bits[0], bits[1])
            try:
                command = CommitParser._item_cmds[cmd.lower()]
                tickets = items_mentioned(tkts)
                for t in tickets:
                    commands.append({command: t})
            except KeyError:
                pass

        return commands
