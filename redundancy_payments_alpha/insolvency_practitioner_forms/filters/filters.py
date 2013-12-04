def datetime_string(date):
    date_string = None
    try:
        date_string = date.strftime('%H:%M - %d/%m/%Y')
    except AttributeError as e:
        pass
    return date_string


def setup_filters(app):
    app.jinja_env.filters['datetime_string'] = datetime_string

