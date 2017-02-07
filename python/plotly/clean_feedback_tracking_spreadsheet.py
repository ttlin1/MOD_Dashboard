# -*- coding: utf-8 -*-
"""
cleaning up the feedback tracking spreadsheet
"""
import os
from os.path import join
import re
import datetime
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar

# fb short for feedback here
pi_file_dir = r'\\gisstore\gis\PUBLIC\SteeleM\OTP\OTP_feedback_tracking'
raw_file = join(pi_file_dir, 'OTP_feedback_tracking.xlsx')
out_file = join(pi_file_dir, 'OTP_feedback_tracking_cleaned.xlsx')
dash_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
out_file_no_pi = join(dash_dir, 'xlsx/OTP_feedback_tracking_cleaned_no_pi.xlsx')


def get_holidays(x):
    cal = calendar()
    holidays = cal.holidays(start=x.min(), end=x.max(), return_name=True)
    holidays = cal.holidays(start='2015-01-01',
                            end='2016-12-31',
                            return_name=True)
    holidays = holidays[~holidays.isin(['Presidents Day',
                                        'Columbus Day',
                                        'Veterans Day'])]
    mlk_days = holidays[holidays == 'Dr. Martin Luther King Jr.']
    return holidays, mlk_days


def find_day_type(x):
    """ We have 5 different day type categories at TriMet. Weekdays,
    Sat, Sun, Holidays (same as Sundays) and MLK (its own beast)"""
    week_num = x.weekday()
    if week_num < 5:
        day_type = "Weekday"
    if week_num == 5:
        day_type = "Saturday"
    if week_num == 6:
        day_type = "Saturday"
    if x in (holidays):
        day_type = "Holiday"
    if x in (mlk_days):
        day_type = "MLK Jr. Day"
    return day_type


def extract_trip_url(x):
    # just keeping the last (earliest) trimet url in the email content
    if isinstance(x, (str, unicode)):
        urls = re.findall(('http[s]?://(?:[a-zA-Z]|[0-9]|[#$-_@.&+]|' +
                           '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'), x)
        trimet_urls = list(x for x in urls if "trimet" in x)
        if len(trimet_urls) > 0:
            # remove date/time parameters
            trip_url = re.sub("\&[hH]our=[0-9]+", '', urls[-1])
            trip_url = re.sub("\&[Mm]inute=[0-9]+", '', trip_url)
            trip_url = re.sub("\&[Aa]m[Pp]m=[amp]+", '', trip_url)
            trip_url = re.sub("\&[Dd]ay=[0-9]+", '', trip_url)
            trip_url = re.sub("\&[Mm]onth=[0-9]+", '', trip_url)
            trip_url = re.sub("\&[Yy]ear=[0-9]+", '', trip_url)
            # remove default parameters
            trip_url = re.sub("&mode=TRANSIT.*?WALK?", '', trip_url)
            for default_param in ['&optimize=QUICK',
                                  '&maxHours=6', '&min=QUICK']:
                trip_url = trip_url.replace(default_param, '')
            return trip_url
    return None


def get_trip_date_type(x):
    '''
    Desired logic: Only apply this function to rows that have trip URLS
    extract those first) AND that don't already have a date. (I will manually
    add some for ride.trimet.org trip URLS) extract trip date from email
    content. If there isn't a year, grab the year from the date recieved.
    If there isn't a date month and day either, then just use date received'
    '''
    # just keeping the last (earliest) trimet url in the email content
    trip_url = x[0]
    date_received = x[1]
    trip_date = ''
    trip_date_type = ''
    if isinstance(trip_url, (str, unicode)):
        urls = re.findall(('http[s]?://(?:[a-zA-Z]|[0-9]|[#$-_@.&+]|' +
                           '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'), trip_url)
        trimet_urls = list(x for x in urls if "trimet.org/#" in x)
        if len(trimet_urls) > 0:
            # print trimet_urls[-1]
            d = re.search("\&[Dd]ay=[0-9]+", trimet_urls[-1])
            if d is None:
                trip_date = date_received  # Use date received
            else:
                d = int(d.group(0).split('=')[-1])
                m = re.search("\&[Mm]onth=[0-9]+", trimet_urls[-1])
                m = int(m.group(0).split('=')[-1])
                y = re.search("\&[Yy]ear=[0-9]+", trimet_urls[-1])
                if y is None:
                    y = date_received.year  # Grab year from date recieved.
                else:
                    y = int(y.group(0).split('=')[-1])
                trip_date = datetime.datetime(year=y, month=m, day=d)

    if trip_date != '':
        trip_date_type = find_day_type(trip_date)
    return trip_date_type

fb_df = pd.read_excel(raw_file, "Sheet1")
dr = fb_df['Date Received']
holidays, mlk_days = get_holidays(fb_df['Date Received'])

# The extract_trip_url function only works for the text trip planner, and there
# are so few map trip planner urls that it was faster to just do them by hand
no_maptripplanner = fb_df[fb_df['Source of Feedback '] != 'maptripplanner@trimet.org']
fb_df['Trip URL (no date)'] = no_maptripplanner['Email Content'].apply(extract_trip_url)
fb_df['Trip date type'] = no_maptripplanner[["Email Content", 'Date Received']].apply(get_trip_date_type, axis=1)

# Write out the version with all data
writer = pd.ExcelWriter(out_file, engine='xlsxwriter',
                        datetime_format='mmm d yyyy',
                        options={'strings_to_urls': False, 'index': False})
fb_df.to_excel(writer)
worksheet = writer.sheets['Sheet1']
worksheet.set_column('A:A', 5)
worksheet.set_column('B:B', 40)
worksheet.set_column('C:G', 30)
worksheet.set_column('H:H', 60)
worksheet.set_column('I:N', 30)
worksheet.freeze_panes(1, 0)
writer.close()

# Write out the no Personal Information version
fb_df_no_pi = fb_df[[u'Date Received', u'Source of Feedback ',
                     u'Type of Feedback', u'Primary Concern or Request',
                     u'Underlying Issue', u'Location Outside District',
                     u'Trip URL (no date)', u'Trip date type']]
writer = pd.ExcelWriter(out_file_no_pi, engine='xlsxwriter',
                        datetime_format='mmm d yyyy',
                        options={'strings_to_urls': False, 'index': False})
fb_df_no_pi.to_excel(writer)
worksheet = writer.sheets['Sheet1']
worksheet.set_column('A:A', 5)
worksheet.set_column('B:B', 20)
worksheet.set_column('C:G', 30)
worksheet.set_column('H:H', 60)
worksheet.set_column('I:I', 30)
worksheet.freeze_panes(1, 0)

writer.close()
