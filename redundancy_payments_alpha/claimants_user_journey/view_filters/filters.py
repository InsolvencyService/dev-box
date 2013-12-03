def discrepancy_message(discrepancy):
    return 'The value you provided was %s but the insolvency ' \
           'practitioner handling this case ' \
           'suggested %s.' % (discrepancy[0], discrepancy[1])


def date_summary(date_dict):
    return "%s/%s/%s" % (
        date_dict['day'],
        date_dict['month'],
        date_dict['year']
    )


def setup_filters(app):
    app.jinja_env.filters['discrepancy_message'] = discrepancy_message
    app.jinja_env.filters['date_summary'] = date_summary

