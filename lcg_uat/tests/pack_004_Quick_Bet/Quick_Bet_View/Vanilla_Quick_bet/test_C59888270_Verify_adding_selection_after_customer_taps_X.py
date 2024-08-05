import pytest
import voltron.environments.constants as vec
import tests
from random import choice
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.reg165_fix
@vtest
class Test_C59888270_Verify_adding_selection_after_customer_taps_X(BaseBetSlipTest, BaseRacing, BaseSportTest):
    """
    TR_ID: C59888270
    NAME: Verify adding selection after customer taps X
    DESCRIPTION: BMA-54870 Quickbet - Add selection if customer taps X
    DESCRIPTION: This Test case verifies that, after customer taps 'X' Button on Quick bet, Quick bet is closed and Selection is added to Betslip
    DESCRIPTION: Before the release of this feature, tapping on 'X' will close Quick bet, without adding selection to Betslip
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 1. App is loaded
    PRECONDITIONS: 2. User is logged in/logged out
    PRECONDITIONS: (Test for logged in and logged out user)
    """
    keep_browser_open = True

    def verify_betslip(self, selection_name=None):
        quick_bet = self.site.quick_bet_panel
        quick_bet.header.close_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
        self.verify_betslip_counter_change(expected_value=1)
        self.site.open_betslip()

        sections = self.get_betslip_sections().Singles
        self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
        self.assertIn(selection_name, sections,
                      msg=f'Added selection "{self.outcome_name}" is not present in Betslip sections "{sections}"')
        stake = list(sections.values())[0]
        stake_value = stake.amount_form.input.value
        self.assertEqual(float(stake_value), float(self.bet_amount),
                         msg='Current stake value: "%s" does not match with expected: "%s"'
                             % (float(stake_value), float(self.bet_amount)))
        self.clear_betslip()
        self.site.open_betslip()
        actual_message = self.get_betslip_content().no_selections_title
        self.assertEqual(actual_message, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'Actual title message "{actual_message}" != Expected "{vec.betslip.NO_SELECTIONS_TITLE}"')
        self.site.close_betslip()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        if tests.settings.backend_env != 'prod':
            event_params_1 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID_1 = event_params_1.event_id
            event_1 = event_params_1.ss_response
            self.__class__.selection_name = event_params_1.team1
            expected_market = normalize_name(self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
            self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=expected_market)

            event_params_2 = self.ob_config.add_UK_racing_event(number_of_runners=1, ew_terms=self.ew_terms)
            selection_ids = event_params_2.selection_ids
            self.__class__.eventID_2 = event_params_2.event_id
            self.__class__.outcome_name = list(selection_ids.keys())[0]
        else:
            event_1 = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID_1 = event_1['event']['id']
            self.__class__.expected_market_name =normalize_name(event_1['event']['children'][0].get('market').get('name'))
            self.__class__.selection_name = event_1['event']['children'][0]['market']['children'][0]['outcome']['name']

            hr_events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                            all_available_events=True,
                                                            expected_template_market='Win or Each Way')
            event_2 = choice(hr_events)
            self.__class__.eventID_2 = event_2['event']['id']
            market = next((market for market in event_2['event']['children']), None)
            outcomes_resp = market['market']['children']
            self.all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                                      for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}
            self.__class__.outcome_name = list(self.all_selection_ids.keys())[0]


    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add Selection to Quick Bet
        EXPECTED: Quick Bet appears at the bottom of the page
        """
        self.navigate_to_edp(event_id=self.eventID_1)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name,
                                                           selection_name=self.selection_name)
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')

    def test_002_tap_on_x_button(self):
        """
        DESCRIPTION: Tap on 'X' Button
        EXPECTED: * Quick Bet is closed automatically
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Betslip counter is increased by 1
        """
        quick_bet = self.site.quick_bet_panel
        quick_bet.header.close_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
        self.verify_betslip_counter_change(expected_value=1)

    def test_003_go_to_betslip_verify_added_selection(self):
        """
        DESCRIPTION: Go to Betslip. Verify added Selection
        EXPECTED: Selection is the same as was added by Quick bet
        """
        self.site.open_betslip()
        sections = self.get_betslip_sections().Singles
        self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
        self.assertIn(self.selection_name, sections,
                      msg=f'Added selection "{self.selection_name}" is not present in Betslip sections "{sections}"')

    def test_004_remove_all_selections_from_betslip(self):
        """
        DESCRIPTION: Remove all selections from Betslip
        EXPECTED: Betslip is empty
        """
        self.clear_betslip()
        self.site.open_betslip()
        actual_message = self.get_betslip_content().no_selections_title
        self.assertEqual(actual_message, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'Actual title message "{actual_message}" != Expected "{vec.betslip.NO_SELECTIONS_TITLE}"')

    def test_005_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add Selection to Quick Bet
        EXPECTED: Quick Bet appears at the bottom of the page
        """
        self.test_001_add_selection_to_quick_bet()

    def test_006_add_any_stake(self):
        """
        DESCRIPTION: Add any Stake
        EXPECTED: 'Stake' field contains added value
        """
        quick_bet = self.site.quick_bet_panel
        quick_bet.selection.content.amount_form.input.value = self.bet_amount
        self.assertEqual(float(quick_bet.selection.content.amount_form.input.value), float(self.bet_amount),
                         msg=f'Actual amount: "{quick_bet.selection.content.amount_form.input.value}" '
                             f'does not match expected: "{self.bet_amount}"')

    def test_007_tap_on_x_button(self):
        """
        DESCRIPTION: Tap on 'X' Button
        EXPECTED: * Quick Bet is closed automatically
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Betslip counter is increased by 1
        EXPECTED: * Selection is the same as was added by Quick bet
        EXPECTED: * 'Stake' field contains added value from Quick bet
        """
        self.verify_betslip(selection_name=self.selection_name)

    def test_008_tap_one_on_race_selection_with_each_way_option_available(self):
        """
        DESCRIPTION: Tap one on 'Race' selection with Each Way option available
        EXPECTED: Quick Bet appears at the bottom of the page
        """
        self.navigate_to_edp(event_id=self.eventID_2, sport_name='horse-racing')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        self.add_selection_to_quick_bet(outcome_name=self.outcome_name)

    def test_009_add_any_stake_and_check_ew_checkbox(self):
        """
        DESCRIPTION: Add any Stake and check 'E/W' checkbox
        EXPECTED: * 'Stake' field contains added value
        EXPECTED: * 'E/W' checkbox is selected
        """
        quick_bet = self.site.quick_bet_panel.selection.content
        quick_bet.amount_form.input.value = self.bet_amount
        quick_bet.each_way_checkbox.click()
        self.assertEqual(float(quick_bet.amount_form.input.value), float(self.bet_amount),
                         msg=f'Actual amount: "{quick_bet.amount_form.input.value}" '
                             f'does not match expected: "{self.bet_amount}"')
        self.assertTrue(quick_bet.each_way_checkbox.is_selected(), msg='Each Way is not selected')

    def test_010_tap_on_x_button(self):
        """
        DESCRIPTION: Tap on 'X' Button
        EXPECTED: * Quick Bet is closed automatically
        EXPECTED: * Selection is added
        EXPECTED: * Selection is the same as was added by Quick bet
        EXPECTED: * 'Stake' field contains added value from Quick bet
        EXPECTED: * 'E/W' checkbox is selected
        """
        self.verify_betslip(selection_name=self.outcome_name)
        self.site.login()
        self.test_001_add_selection_to_quick_bet()
        self.test_002_tap_on_x_button()
        self.test_003_go_to_betslip_verify_added_selection()
        self.test_004_remove_all_selections_from_betslip()
        self.test_005_add_selection_to_quick_bet()
        self.test_006_add_any_stake()
        self.test_007_tap_on_x_button()
        self.test_008_tap_one_on_race_selection_with_each_way_option_available()
        self.test_009_add_any_stake_and_check_ew_checkbox()
        self.verify_betslip(selection_name=self.outcome_name)
