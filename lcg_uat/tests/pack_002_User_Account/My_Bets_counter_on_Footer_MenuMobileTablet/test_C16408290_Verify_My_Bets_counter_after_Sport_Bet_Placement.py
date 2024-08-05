import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.login
@pytest.mark.my_bets
@pytest.mark.mobile_only
@pytest.mark.bet_history_open_bets
@pytest.mark.other
@vtest
class Test_C16408290_Verify_My_Bets_counter_after_Sport_Bet_Placement(BaseCashOutTest, BaseUserAccountTest):
    """
    TR_ID: C16408290
    VOL_ID: C58634254
    NAME: Verify My Bets counter after Sport Bet Placement
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after Sport Bet Placement
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: - Load Oxygen/Roxanne Application and login
        DESCRIPTION: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
        DESCRIPTION: - My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
        """
        self.check_my_bets_counter_enabled_in_cms()

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=2)
            outcomes_1 = next(((market['market'].get('children')) for market in events[0]['event'].get('children')), None)
            outcomes_2 = next(((market['market'].get('children')) for market in events[1]['event'].get('children')), None)
            if outcomes_1 is None or outcomes_2 is None:
                raise SiteServeException('There are no available outcomes')

            team1_1 = next((outcome['outcome']['name'] for outcome in outcomes_1 if
                            outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            team1_2 = next((outcome['outcome']['name'] for outcome in outcomes_2 if
                            outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not team1_1 or not team1_2:
                raise SiteServeException('No Home team present is SS response')
            self.__class__.selection_ids_1 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_1}.get(team1_1)
            self.__class__.selection_ids_2 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_2}.get(team1_2)
            self.__class__.selection_ids = [self.selection_ids_1, self.selection_ids_2]
        else:
            events_params = self.create_several_autotest_premier_league_football_events(
                number_of_events=2)
            self.__class__.selection_ids = [event_params.selection_ids[event_params.team1] for event_params in events_params]
            self.__class__.selection_ids_1 = self.selection_ids[0]

        self.site.login(username=tests.settings.betplacement_user)
        if '+' in self.get_my_bets_counter_value_from_footer():
            self.__class__.initial_my_bets_counter = int(self.get_my_bets_counter_value_from_footer().strip('+'))
        else:
            self.__class__.initial_my_bets_counter = int(self.get_my_bets_counter_value_from_footer())
        self.__class__.expected_counter = self.initial_my_bets_counter

    def test_001_add_sport_selection__eg_football_to_quickbetbetslip_and_place_bet(self):
        """
        DESCRIPTION: Add sport selection ( e.g. Football) to Quickbet/Betslip and place bet
        EXPECTED: Bets is placed successfully
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids_1)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_002_close_quickbetbetslip_verify_my_bets_counter_at_the_footer_panel(self):
        """
        DESCRIPTION: * Close Quickbet/Betslip
        DESCRIPTION: * Verify 'My Bets' counter at the Footer panel
        EXPECTED: My bets counter icon is increased by one
        """
        self.site.close_betreceipt()
        if '+' in self.get_my_bets_counter_value_from_footer():
            actual_counter = int(self.get_my_bets_counter_value_from_footer().strip('+'))
        else:
            self.__class__.expected_counter += 1
            actual_counter = int(self.get_my_bets_counter_value_from_footer())
        self.assertEqual(actual_counter, self.expected_counter,
                         msg=f'Actual My Bets counter: "{actual_counter}" '
                             f'is not as expected: "{self.expected_counter}"')

    def test_003_repeat_steps_1_4_for_multiples(self):
        """
        DESCRIPTION: Repeat steps #1-4 for multiples
        EXPECTED: Results are the same:
        EXPECTED: My bets counter icon is increased by one
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.test_002_close_quickbetbetslip_verify_my_bets_counter_at_the_footer_panel()
