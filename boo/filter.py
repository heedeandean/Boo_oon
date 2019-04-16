from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from boo import app



@app.template_filter('simpledate')

def simpledate(dt):
    if not isinstance(dt, date):
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M')

    # if ( datetime.now() - dt) < timedelta(1):
    if (datetime.now() - dt).days < 1:
        fmt = "%H:%M"
    else:
        fmt = "%m/%d"

    return dt.strftime(fmt)


