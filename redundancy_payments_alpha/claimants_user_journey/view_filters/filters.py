def discrepancy_message(discrepancy):
    return 'The value you provided was %s but the insolvency ' \
           'practitioner handling this case ' \
           'suggested %s.' % (discrepancy[0], discrepancy[1])


def setup_filters(app):
    app.jinja_env.filters['discrepancy_message'] = discrepancy_message
