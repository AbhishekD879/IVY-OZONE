import pytest
import tests
from tests.base_test import vtest
from json import JSONDecodeError
from tests.Common import Common
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot grant odds boost tokens on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C34792794_Verify_grouping_3_calls_private_markets_odds_boost_freebets_into_single_request_on_page_refresh(Common):
    """
    TR_ID: C34792794
    NAME: Verify grouping 3 calls (private markets, odds boost, freebets) into single request on page refresh.
    DESCRIPTION: This test case verifies receiving 3 calls (private markets, odds boost, freebets) in one request on page refresh.
    PRECONDITIONS: * You should have two users. The first one shouldn't have any active Free Bets, Odd Boost tokens or Private Markets. The second one should have active Free Bets, Odd Boost tokens or Private Markets.
    PRECONDITIONS: * User should be logged in.
    PRECONDITIONS: * User is on the homepage.
    PRECONDITIONS: Request to be checked:
    PRECONDITIONS: Devtools > Network > accountFreebets?channel=M&returnOffers=Y
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: accountFreebets?freebetTokenType=BETBOOST - odds boost
    PRECONDITIONS: accountFreebets?freebetTokenType=SPORTS&channel=M&returnOffers=Y - freebets
    PRECONDITIONS: accountFreebets?freebetTokenType=ACCESS - private markets
    PRECONDITIONS: are no longer used on page refresh (after implementation of ticket https://jira.egalacoral.com/browse/BMA-49190)
    """
    keep_browser_open = True
    valid_req = 'accountFreebets?channel=M'
    invalid_req = 'accountFreebets?freebetTokenType=BETBOOST'
    invalid_req2 = 'accountFreebets?freebetTokenType=SPORTS&channel=M&returnOffers=Y'
    invalid_req3 = 'accountFreebets?freebetTokenType=ACCESS'
    ss_url = 'accountFreebets?'

    def get_response_url(self, url):
        """
        :param url: SS or Commentary url
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def check_request(self):
        """
        :return: Complete url
        """
        sleep(10)  # Need time for SS requests to load
        sp_url = self.get_response_url(url=self.ss_url)
        self.assertIn(self.valid_req, sp_url, msg=f'Required "{self.valid_req}" parameter not found')
        self.assertNotIn(self.invalid_req, sp_url, msg=f'Required "{self.invalid_req}" parameter found')
        self.assertNotIn(self.invalid_req2, sp_url, msg=f'Required "{self.invalid_req2}" parameter found')
        self.assertNotIn(self.invalid_req3, sp_url, msg=f'Required "{self.invalid_req3}" parameter found')

    def test_001_log_in_with_the_first_user_from_preconditionsrefresh_the_pagecheck_accountfreebetschannelmreturnoffersy_request(self):
        """
        DESCRIPTION: Log in with the first user from preconditions.
        DESCRIPTION: Refresh the page.
        DESCRIPTION: Check 'accountFreebets?channel=M&returnOffers=Y' request.
        EXPECTED: * accountFreebets?freebetTokenType=BETBOOST
        EXPECTED: * accountFreebets?freebetTokenType=SPORTS&channel=M&returnOffers=Y
        EXPECTED: * accountFreebets?freebetTokenType=ACCESS
        EXPECTED: **are not received**
        EXPECTED: accountFreebets?channel=M&returnOffers=Y is received with all appropriate data from the requests above in the 'freebetToken' parameter.
        """
        self.site.login()
        self.site.wait_content_state("homepage")
        self.device.refresh_page()
        self.site.wait_content_state("homepage")
        self.check_request()

    def test_002_log_in_with_the_second_user_from_preconditionsrefresh_the_pagecheck_accountfreebetschannelmreturnoffersy_request(self):
        """
        DESCRIPTION: Log in with the second user from preconditions.
        DESCRIPTION: Refresh the page.
        DESCRIPTION: Check 'accountFreebets?channel=M&returnOffers=Y' request.
        EXPECTED: * accountFreebets?freebetTokenType=BETBOOST
        EXPECTED: * accountFreebets?freebetTokenType=SPORTS&channel=M&returnOffers=Y
        EXPECTED: * accountFreebets?freebetTokenType=ACCESS
        EXPECTED: **are not received**
        EXPECTED: accountFreebets?channel=M&returnOffers=Y is received with all appropriate data from the requests above in the 'freebetToken' parameter.
        """
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')
        user_name = tests.settings.freebet_user
        self.site.login(username=user_name)
        self.site.wait_content_state("homepage")
        self.ob_config.grant_odds_boost_token(username=user_name)
        self.device.refresh_page()
        self.site.wait_content_state("homepage")
        self.check_request()

    def test_003_go_to_the_gaming_and_go_back_check_accountfreebetschannelmreturnoffersy_request(self):
        """
        DESCRIPTION: Go to the Gaming and go back. Check 'accountFreebets?channel=M&returnOffers=Y' request.
        EXPECTED: * accountFreebets?freebetTokenType=BETBOOST
        EXPECTED: * accountFreebets?freebetTokenType=SPORTS&channel=M&returnOffers=Y
        EXPECTED: * accountFreebets?freebetTokenType=ACCESS
        EXPECTED: **are not received**
        EXPECTED: accountFreebets?channel=M&returnOffers=Y is received with all appropriate data from the requests above in the 'freebetToken' parameter.
        """
        self.navigate_to_page('en/games')
        self.site.wait_content_state_changed()
        self.device.go_back()
        self.site.wait_content_state("homepage")
        self.check_request()
