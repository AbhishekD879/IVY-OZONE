from time import sleep
import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Events cannot be created/suspend on prod & beta
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.mobile_only
@vtest
class Test_C2605968_Verify_suspended_event_market_selection_in_Quick_bet_for_boosted_bet(BaseSportTest,
                                                                                         BaseBetSlipTest):
    """
    TR_ID: C2605968
    NAME: Verify suspended event/market/selection in Quick bet for boosted bet
    DESCRIPTION: This test case verifies suspension of event/market/selection in Quick Bet for boosted bet and the behavior of related UI elements.
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: Enable Odds Boost in CMS
    PRECONDITIONS: Load Application
    PRECONDITIONS: Login into App by user with Odds boost token generated
    PRECONDITIONS: How to generate Odds Boost: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    """
    keep_browser_open = True

    def boost_button_and_suspend_verification(self):
        """
        This method verifies following points:
        - 'Your event/market/selection has been suspended' warning message
        - 'Boost' button disappears
        """
        self.__class__.quick_bet = self.site.quick_bet_panel
        result = wait_for_result(lambda: self.quick_bet.has_odds_boost_button(timeout=5),
                                 expected_result=False,
                                 timeout=5)
        self.assertFalse(result, msg='Odds boost button is displayed after suspending event')

        expected_message = vec.quickbet.BET_PLACEMENT_ERRORS.event_suspended
        message = self.site.quick_bet_panel.info_panels_text[0]
        self.assertEqual(message, expected_message,
                         msg=f'Actual message "{message}" does not match expected "{expected_message}"')

    def boost_button_warning_message_verification(self):
        """
        This method verifies following points:
        - Warning message disappears
        - Boost is again available for this bet ('Boost' button is shown again)
        """
        self.assertFalse(self.site.quick_bet_panel.wait_for_quick_bet_info_panel(expected_result=False),
                         msg='Quick Bet Info Panel is present')

        quick_bet = self.site.quick_bet_panel
        result = wait_for_result(lambda: quick_bet.has_odds_boost_button(timeout=5),
                                 expected_result=True,
                                 timeout=20)
        self.assertTrue(result, msg='Odds boost button is not displayed')

    def suspend_event(self, active=True):
        """
        This method verifies following points:
        - Suspend/Unsuspend of event
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=active)
        # After suspend/ unsuspend event, it is taking sometime to reflect on UI hence wait is added.
        sleep(30)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Quick Bet functionality should be enabled in CMS
        PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
        PRECONDITIONS: Enable Odds Boost in CMS
        PRECONDITIONS: Load Application
        PRECONDITIONS: Login into App by user with Odds boost token generated
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')
        quick_bet = self.get_initial_data_system_configuration().get('quickBet', {})
        if not quick_bet:
            quick_bet = self.cms_config.get_system_configuration_item('quickBet')
        if not quick_bet.get('EnableQuickBet'):
            raise CmsClientException('Quick Bet is disabled in CMS')
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='Login button is not displayed')

        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event_params.event_id
        self.__class__.all_selection_ids = list(event_params.selection_ids.values())
        self.__class__.marketID = event_params.default_market_id
        self.__class__.expected_market = event_params.ss_response['event']['children'][0]['market']['name']

        username = tests.settings.odds_boost_user
        offer_id = self.ob_config.backend.ob.odds_boost_offer_non_adhoc.general_offer.offer_id
        self.ob_config.grant_odds_boost_token(username=username, level='selection', offer_id=offer_id)
        self.site.login(username=username)

    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: Quick Bet appears at the bottom of the page
        EXPECTED: Boost is available for this bet ('Boost' button is present)
        """
        self.navigate_to_edp(event_id=self.eventID, timeout=40)
        sleep(40)
        self.site.wait_splash_to_hide(5)
        self.site.wait_content_state(state_name='EventDetails', timeout=60)
        if self.brand == 'ladbrokes' and self.site.root_app.has_timeline_overlay_tutorial(timeout=3,
                                                                                          expected_result=True):
            self.site.timeline_tutorial_overlay.close_icon.click()
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market)

        result = wait_for_result(lambda: self.site.quick_bet_panel.has_odds_boost_button(timeout=5),
                                 expected_result=True,
                                 timeout=20)
        self.assertTrue(result, msg='Odds boost button is not displayed')

    def test_002_make_eventmarketselection_suspended_for_the_selection_in_quickbet(self):
        """
        DESCRIPTION: Make event/market/selection suspended for the selection in QuickBet
        EXPECTED: 'Your event/market/selection has been suspended' warning message is displayed below Quick Bet (yellow) background for Coral; cyan background for Ladbrokes)
        EXPECTED: 'Boost' button disappears
        """
        self.suspend_event(active=False)
        self.boost_button_and_suspend_verification()

    def test_003_unsuspended_eventmarketselection_used_in_quickbet(self):
        """
        DESCRIPTION: Unsuspended event/market/selection used in QuickBet
        EXPECTED: Warning message disappears
        EXPECTED: Boost is again available for this bet ('Boost' button is shown again)
        """
        self.suspend_event(active=True)
        self.boost_button_warning_message_verification()

    def test_004_tap_on_boost_button(self):
        """
        DESCRIPTION: Tap on 'Boost' button
        EXPECTED: Button changes to 'Boosted'
        EXPECTED: Crossed out original price(its value) of the selection is shown near the 'boosted' value within the grey(Coral)/yellow(Ladbrokes) frame
        """
        self.quick_bet.odds_boost_button.click()
        result = wait_for_result(lambda: self.quick_bet.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')

        self.assertTrue(self.quick_bet.selection.content.is_original_odds_crossed,
                        msg='Original odds are not crossed out')

    def test_005_make_eventmarketselection_suspended_for_the_selection_in_quickbet(self):
        """
        DESCRIPTION: Make event/market/selection suspended for the selection in QuickBet
        EXPECTED: Your event/market/selection has been suspended' warning message is displayed below Quick Bet (yellow) background for Coral; cyan background for Ladbrokes)
        EXPECTED: 'Boost' button disappears
        EXPECTED: Crossed out original price and 'boosted' value disappear
        """
        self.suspend_event(active=False)
        self.boost_button_and_suspend_verification()
        self.assertFalse(self.site.quick_bet_panel.selection.content.is_original_odds_crossed,
                         msg='Original odds are crossed out')

    def test_006_unsuspended_eventmarketselection_used_in_quickbet(self):
        """
        DESCRIPTION: Unsuspended event/market/selection used in QuickBet
        EXPECTED: Warning message disappears
        EXPECTED: 'Boosted' button is shown again
        EXPECTED: Crossed out original price(its value) of the selection is shown near the 'boosted' value within the grey(Coral)/yellow(Ladbrokes) frame
        """
        self.suspend_event(active=True)
        self.boost_button_warning_message_verification()
        self.assertTrue(self.site.quick_bet_panel.selection.content.is_original_odds_crossed,
                        msg='Original odds are not crossed out')
