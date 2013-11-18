from wtforms import TextField

class CurrencyField(TextField):
    """This is a subtype of the WTForm Text field which appends
    a pound-sign to the html.

    It does this as a monkey patch to the wtform.
    """
    def __call__(self, **kwargs):
        """See the depths of the __call__ method in Field
        to understand what is going on.
        """
        return "&pound; " + self.widget(self, **kwargs)
