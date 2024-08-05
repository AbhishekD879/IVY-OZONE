from crlat_ob_client.freebet import Freebet
from crlat_ob_client.utils.helpers import do_request


class Offer(Freebet):

    def __init__(self, env, brand, *args, **kwargs):
        super(Offer, self).__init__(env, brand, '', '', *args, **kwargs)

    def give_offer(self, username, offer_id):
        """
        :param offer_id - id of the offer that will be given for user
        :param username - username
        """
        user_id = self.get_custid(username)
        params = (
            ('action', 'CM::cust::offer::do_claim'),
            ('cust_id', user_id),
            ('offer_id', offer_id)
        )
        url = self.site[:-2] + 'camp_mgr'
        r = do_request(url=url, params=params, cookies=self.site_cookies, load_response=False)
        return r
