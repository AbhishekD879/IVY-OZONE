import pytest
from datetime import datetime, timedelta
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from random import uniform

from voltron.utils.exceptions.failure_exception import TestFailure


#@pytest.mark.crl_stg2  # Coral only
#@pytest.mark.crl_tst2
# @pytest.mark.crl_prod  # can't grant freebets on prod
# @pytest.mark.crl_hl
@pytest.mark.user_account
@pytest.mark.freebets
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.login
@pytest.mark.na
@vtest
@pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-3017')
class Test_C29116_Verify_Bet_Now_link_on_Freebet_Information_page(BaseUserAccountTest, BaseSportTest):
    """
    TR_ID: C29116
    NAME: Verify Bet Now link on Freebet Information page
    DESCRIPTION: This Test Case verifies 'Bet Now' link on 'Freebet Information' page.
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User have Free Bets available on their account
    """
    keep_browser_open = True
    username = None
    url = None
    free_bet_value = f'{uniform(10, 20):.2f}'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        EXPECTED: Created football test event
        """
        self.__class__.eventID = self.ob_config.add_football_event_to_italy_serie_a().event_id

    def test_001_login(self):
        """
        DESCRIPTION: Login
        EXPECTED: User successfully logged in
        """
        self.__class__.username = tests.settings.freebet_user
        self.site.login(username=self.username)

    def test_002_apply_freebet_offer_on_the_market_level(self):
        """
        DESCRIPTION: Apply Freebet offer on the event level
        EXPECTED: Applied grant_freebet for event level
        """
        future_date = datetime.utcnow() + timedelta(days=5)
        self.ob_config.grant_freebet(username=self.username, level='event', freebet_value=self.free_bet_value,
                                     id=self.eventID, expiration_date=future_date)

    def test_003_navigate_to_the_my_freebets_page(self):
        """
        DESCRIPTION: Navigate to the 'My Freebets/Bonuses' page
        EXPECTED: My Freebets page is opened
        """
        self.navigate_to_page(name='freebets')
        self.site.wait_content_state(state_name='Freebets')
        self.site.close_all_dialogs(async_close=False, timeout=3)

    def test_004_navigate_to_the_freebet_details_page_for_freebet_what_is_applied_on_the_selection_level(self):
        """
        DESCRIPTION: Navigate to the Freebet Details page for Freebet what is applied on the event level
        EXPECTED: 'Freebet Information' page is opened
        EXPECTED: Freebet description is present
        EXPECTED: 'Bet Now' link is present
        """
        freebet_items = self.site.freebets.freebets_content.items_as_ordered_dict
        self.assertTrue(freebet_items,
                        msg=f'No freebet offers found for username "{self.username}"')
        for _, freebet in freebet_items.items():
            if f'{freebet.freebet_value:.2f}' == self.free_bet_value and freebet.name == self.freebet_name_template:
                freebet.click()
                break
        else:
            raise TestFailure(f'No freebet found with value "{self.free_bet_value}" and name "{self.freebet_name_template}"')

        self.site.wait_content_state(state_name='FreeBetDetails')
        self.verify_freebet_details_page()

        self.__class__.url = self.site.freebet_details.bet_now.href
        self.assertIn(self.eventID, self.url,
                      msg='Event id "%s" is not present in url "%s"' % (self.eventID, self.url))

    def test_005_tap_on_bet_now_link(self):
        """
        DESCRIPTION: Tap on 'Bet Now' Link
        EXPECTED: User is redirected to the relevant <Sport> Event Details page
        """
        self.site.freebet_details.bet_now.click()
        self.site.wait_content_state(state_name='EventDetails')
        event_url = self.device.get_current_url()
        self.assertIn(self.url, event_url,
                      msg='Url from freebet page "%s" is not found in current url "%s"' % (self.url, event_url))
        self.assertIn(self.eventID, event_url,
                      msg='Event id "%s" is not found in current url "%s"' % (self.eventID, event_url))
