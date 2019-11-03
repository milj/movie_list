from expects.matchers import Matcher


class change(Matcher):
    '''A custom matcher to check if the result of 'expected' callable
    is changed by the call to 'subject' callable.

    The argument 'by' is expected to be a number.

    See https://expects.readthedocs.io/en/stable/custom-matchers.html
    '''
    def __init__(self, expected, by=None):
        self._expected = expected
        self._change_by = by

    def _match(self, subject):
        before = self._expected()
        subject()
        after = self._expected()

        if self._change_by is None:
            if before != after:
                return True, [
                    f'it changed (from {before} to {after})'
                ]
            return False, [
                f"it didn't change (was {before}, still is {after})"
            ]

        if (before + self._change_by) == after:
            return True, [
                f'it changed by {self._change_by} (from {before} to {after})'
            ]
        return False, [
            f"it didn't change by {self._change_by} (was {before}, still is {after})"
        ]
