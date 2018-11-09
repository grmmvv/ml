def get_base_fixer_url():
    return 'http://data.fixer.io/api'


class URL:
    main_search_url = 'https://go.mail.ru'
    fixer_base_api_url = get_base_fixer_url()
    latest_fixer_api_url = '{}/latest'.format(get_base_fixer_url())
    old_fixer_api_url = 'http://api.fixer.io/'

    @staticmethod
    def get_fixer_url_for_date(year, month, day):
        return '{}/{}-{}-{}'.format(get_base_fixer_url(), year, month, day)
