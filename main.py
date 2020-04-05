from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
import re
import requests
import sys

def main():
    current_year = datetime.now().year
    year = input('select year (2010-{}): '.format(current_year))
    years = [str(possible_year) for possible_year in range(2010, current_year + 1)]

    if year not in years:
        print('year incorrect')
        sys.exit()

    month = input('select month (1-12): ')
    months_validation = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

    if month not in months_validation:
        print('month incorrect')
        sys.exit()

    resolutions_string = '320x480, 640x480, 800x480, 800x600, 1024x768, 1024x1024, 1152x864, 1280x720, 1280x800, 1280x960, 1280x1024, ' \
                         '1366x768, 1440x900, 1440x1050, 1600x1200, 1680x1050, 1680x1200, 1920x1080, 1920x1200, 1920x1440, 2560x1440'
    resolutions = re.split(r',\s*', resolutions_string)
    resolution = input('select resolution ({}): '.format(resolutions_string))

    if resolution not in resolutions:
        print('resolution incorrect')
        sys.exit()

    is_with_calendar = input('Wallpapers with calendar, Yes or No? print Y/N and press Enter: ').lower()
    is_with_calendar_validation = ['y','n']

    if is_with_calendar not in is_with_calendar_validation:
        print('walpapers type incorrect')
        sys.exit()

    wallpaper_type = 'with calendar' if is_with_calendar == 'y' else 'without calendar'
    publish_year = year if month != '1' else str(int(year) - 1)
    numbering_of_months = ['12', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    months = ['december', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
              'november', 'december']
    url = 'https://www.smashingmagazine.com/{0}/{1}/desktop-wallpaper-calendars-{2}-{3}/'.format(publish_year, numbering_of_months[int(month) - 1], months[int(month)], year)
    data = requests.get(url)

    if (data.status_code != 200):
        url = 'https://www.smashingmagazine.com/{0}/{1}/desktop-wallpaper-calendars-{2}-{3}/'.format(year, numbering_of_months[int(month)], months[int(month)], year)
        data = requests.get(url)
        if (data.status_code != 200):
            print('no wallpapers for the requested time period')
            sys.exit()

    folder = 'images\{0}\{1}.{2}_{3}'.format(wallpaper_type, month, year, resolution)
    is_desired_resolution_exist = False
    soup = bs(data.text, 'html.parser')
    li_tags = soup.findAll('li')

    for li_tag in li_tags:
        if (re.findall(r'^{}: '.format(wallpaper_type), li_tag.text)):
            li_soup = bs(str(li_tag), 'html.parser')
            links = li_soup.findAll('a')
            for link in links:
                if (link.text == resolution):
                    is_desired_resolution_exist = True
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                    wallpaper = requests.get(link.get('href'), stream=True)
                    file_name_arr = re.findall(r'[\w-]{1,}\.{1}\w{3,4}$', link.get('href'))
                    file_name = file_name_arr[0]
                    f = open('{0}\{1}'.format(folder, file_name), "wb")
                    for chunk in wallpaper:
                        f.write(chunk)
                    f.close()

    if not is_desired_resolution_exist:
        print('no wallpapers with desired resolution')
    else:
        print('wallpapers downloaded successfully')

if __name__ == '__main__':
    main()