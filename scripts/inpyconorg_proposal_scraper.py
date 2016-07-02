""".."""

from bs4 import BeautifulSoup as Bs
import requests
import traceback


class Scrape:
    """.."""

    def __init__(self):
        """Intializing varibales."""
        self.proposal_url = "https://in.pycon.org/cfp/2016/proposals/"
        self.base_url = 'https://in.pycon.org'
        self.result = {}
        self.headers = {}

    def make_request(self, url):
        """Making request to get html page of given url.

        :params url
        Return
            BeautifulSoup object or None
        """
        try:
            self.headers['User-Agent'] = ("Mozilla/5.0 (Macintosh; Intel Mac"
                                          " OS X 10_11_5) AppleWebKit/537.36"
                                          "(KHTML, like Gecko) Chrome/51.0."
                                          "2704.103 Safari/537.36")
            print self.headers
            r = requests.get(url, headers=self.headers)
            if r.ok:
                return Bs(r.text)
        except:
            print traceback.format_exc()
        return None

    def start(self):
        """Call to start scraping in.pycon.org proposals.

        Return
            dict of proposals.
        """
        soup = self.make_request(self.proposal_url)
        if not soup:
            return
        soup_proposals = soup.findAll(
            'div', attrs={'class': 'row user-proposals'})
        for proposal in soup_proposals:
            p = proposal.find('h3', attrs={'class': 'proposal--title'})
            title, url = p.text, "".join([self.base_url,
                                          p.find('a').get('href', '')])
            soup = self.make_request(url)
            if not soup:
                continue
            soup_proposal = soup.findAll(
                'div', attrs={'class': 'proposal-writeup--section'})
            temp = {}
            for data in soup_proposal:
                try:
                    temp[data.find('h4').text] = "".join(
                        [ptag.text for ptag in data.findAll('p')])
                except:
                    print traceback.format_exc()
            self.result[title] = temp

        # from pprint import pprint
        # # Printing data
        # pprint(self.result)
        return self.result

if __name__ == '__main__':
    Scrape().start()
