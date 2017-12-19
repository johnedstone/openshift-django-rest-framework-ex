class RandomPicker(object):
    def __init__(self, **kwargs):
        for field in (
                'start',
                'end',
                'status',
                'result',
                ):
            setattr(self, field, kwargs.get(field, None))

# vim: et ai ts=4 sw=4 sts=4 ru nu
