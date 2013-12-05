def datetime_string(datetime):
    datetime_string = None
    try:
        datetime_string = datetime.strftime('%H:%M - %d/%m/%Y')
    except AttributeError as e:
        pass
    return datetime_string


def date_string(date):
    date_string = None
    try:
        date_string = date.strftime('%d/%m/%Y')
    except AttributeError as e:
        pass
    return date_string


def setup_filters(app):
    app.jinja_env.filters['datetime_string'] = datetime_string

