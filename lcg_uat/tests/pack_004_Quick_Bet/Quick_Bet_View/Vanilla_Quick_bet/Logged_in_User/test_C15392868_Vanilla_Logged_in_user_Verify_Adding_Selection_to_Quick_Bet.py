import pytest
import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C15392868_Vanilla_Logged_in_user_Verify_Adding_Selection_to_Quick_Bet(BaseRacing, BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C15392868
    NAME: [Vanilla] [Logged in user] Verify Adding Selection to Quick Bet
    DESCRIPTION: This test case verifies adding Selection to Quick Bet
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * User should be Logged in and have a positive balance
    PRECONDITIONS: * Betslip counter should be 0
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        Create event or get the event data
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            outcomes = next(((market['market']['children']) for market in event['event']['children']
                             if market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_name = list(selection_ids.keys())[1]

        else:
            event = self.ob_config.add_UK_racing_event(number_of_runners=1, ew_terms=self.ew_terms)
            self.__class__.eventID = event.event_id
            self.__class__.selection_name = list(event.selection_ids.keys())[0]

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_tap_one_sportrace_selection(self):
        """
        DESCRIPTION: Tap one <Sport>/<Race> selection
        EXPECTED: * Selected price/odds are highlighted in green
        EXPECTED: * Betslip counter does NOT increase by one
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab('WIN OR E/W')
        self.add_selection_to_quick_bet(outcome_name=self.selection_name)
        self.verify_betslip_counter_change(expected_value=0)

    def test_003_verify_quick_bet(self):
        """
        DESCRIPTION: Verify Quick Bet
        EXPECTED: * Quick Bet appears at the bottom of the page
        EXPECTED: * All selection details are displayed within Quick Bet
        EXPECTED: * the Following view should be displayed for Logged in user
        EXPECTED: ![](index.php?/attachments/get/31341)
        """
        self.assertTrue(self.site.wait_for_quick_bet_panel(expected_result=True), msg='Quick Bet is not present')
        self.assertTrue(self.site.quick_bet_panel.selection.content.amount_form.input.is_displayed(),
                        msg='input place is not displayed')
        outcome_name = self.site.quick_bet_panel.selection.content.outcome_name
        self.assertEqual(outcome_name, self.selection_name,
                         msg=f'Outcome name displayed "{outcome_name}" is not same as expected name "{self.selection_name}"')
