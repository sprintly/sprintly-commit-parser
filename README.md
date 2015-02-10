# Sprintly Commit Parser

Parse commits for Sprintly commands.

### Usage

```
>>> from sprintly_commit_parser import CommitParser
>>> parser = CommitParser()
>>> parser('closes #123 refs #456 #789')
[{'close_ticket': 123}, {'reference_ticket': 456}, {'reference_ticket': 789}]
```
