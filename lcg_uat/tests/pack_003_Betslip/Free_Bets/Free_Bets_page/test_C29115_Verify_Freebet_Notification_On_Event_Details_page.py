import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


#@pytest.mark.crl_stg2
#@pytest.mark.crl_tst2
# @pytest.mark.crl_prod  # Coral only
# @pytest.mark.crl_hl  # can't grant freebets on prod
@pytest.mark.user_account
@pytest.mark.back_button
@pytest.mark.freebets
@pytest.mark.bet_placement
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.na
@vtest
class Test_C29115_Verify_Freebet_Notification_On_Event_Details_page(BaseUserAccountTest, BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C29115
    NAME: Verify Freebet Notification On Event Details page
    DESCRIPTION: This test case verifies freebets notifications on event details page
    """
    keep_browser_open = True
    username = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        EXPECTED: Created football test event
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID, self.__class__.selection_ids = event_params.event_id, event_params.selection_ids

    def test_001_login(self):
        """
        DESCRIPTION: Login
        EXPECTED: User is logged in successfully
        """
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(username=self.username, amount=tests.settings.min_deposit_amount)
        self.site.login(username=self.username)
        self.site.logout()
        self.site.login(username=self.username)

    def test_002_apply_freebet_offer_on_the_event_level(self):
        """
        DESCRIPTION: Apply Freebet offer on the event level
        EXPECTED: Freebet is added
        """
        self.ob_config.grant_freebet(username=self.username, level='event', id=self.eventID)

    def test_003_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Page is reloaded
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

    def test_004_navigate_to_the_relevant_event_details_page(self):
        """
        DESCRIPTION: Navigate to the relevant Event details page
        EXPECTED: 'Freebet' notification icon is displayed on the relevant Event details page
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.site.close_all_dialogs(async_close=False)
        self.assertTrue(self.site.sport_event_details.freebet_icon.is_displayed(), msg='Freebet icon is not displayed')

    def test_005_tap_on_freebet_notification_icon(self):
        """
        DESCRIPTION: Tap on 'Freebet' notification icon
        EXPECTED: 'My Freebets/Bonuses' page is opened
        """
        self.site.sport_event_details.freebet_icon.click()
        self.site.wait_content_state(state_name='Freebets')

    def test_006_tap_on_back_button(self):
        """
        DESCRIPTION: Tap on back button
        EXPECTED: User navigate to the previous page (Event details page)
        """
        self.site.freebets.back_button_click()
        self.site.wait_content_state(state_name='EventDetails')

    def test_007_place_a_bet_using_current_freebet_offer_event_level(self):
        """
        DESCRIPTION: Place a bet using current Freebet offer (event level)
        EXPECTED: 'Freebet' notification disappeared from the Event details page
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'])
        self.place_single_bet(freebet=True)
        self.check_bet_receipt_is_displayed()

        self.navigate_to_edp(event_id=self.eventID)
        self.assertFalse(self.site.sport_event_details.has_freebet_icon,
                         msg='Freebet icon is displayed after bet')
