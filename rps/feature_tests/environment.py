import contextlib

from birmingham_cabinet.api import truncate_all_tables

def before_scenario(context, scenario):
    if 'nuke_db' in scenario.tags:
        truncate_all_tables()

def after_feature(context, feature):
    truncate_all_tables()

