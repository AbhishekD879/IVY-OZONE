import pytest
import tests
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C15860060_from_OX99_Betslip_header_and_sub_headers_UI_for_Logged_in_User_on_TABLET_Desktop(BaseBetSlipTest):
    """
    TR_ID: C15860060
    NAME: [from OX99] Betslip: header and sub headers UI for Logged in User on TABLET/Desktop
    DESCRIPTION: This test case verifies betslip header and sub-headers UI for Logged in User
    PRECONDITIONS: User account with a positive balance
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify CashOut tab configuration in CMS
        PRECONDITIONS: Events creation and placing treble bet
        EXPECTED : Events created and treble bet is placed
        """
        system_config = self.get_initial_data_system_configuration()
        cashout_cms = system_config.get('CashOut', {})
        if not cashout_cms:
            cashout_cms = self.cms_config.get_system_configuration_item('CashOut')
        self.__class__.is_cashout_tab_enabled = cashout_cms.get('isCashOutTabEnabled')
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            market = next((market for market in event['event']['children'] if market['market'].get('children')), None)
            outcomes_resp = market['market']['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                                 for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}
            self.__class__.team1 = list(all_selection_ids.keys())[0]
            self.__class__.selection_id = all_selection_ids.get(self.team1)
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, selection_ids = event_params.team1, event_params.selection_ids
            self.__class__.selection_id = selection_ids[self.team1]

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_log_in_user_account__from_preconditions(self):
        """
        DESCRIPTION: Log in User account ( from Preconditions)
        EXPECTED: User is logged in
        """
        self.site.login()

    def test_003_verify_betslip_header_ui(self):
        """
        DESCRIPTION: Verify betslip header UI
        EXPECTED: Betslip header area is displayed and it includes:
        EXPECTED: * Betslip tab
        EXPECTED: * My Bets tab
        EXPECTED: Betslip tab is selected by default and "*Your betslip is empty* Please add one or more selections to place a bet" message is displayed below the betslip header
        EXPECTED: **[For Ladbrokes on Tablet]**: Button 'Go Betting' is present
        """
        actual_tab_menu = self.get_betslip_content().betslip_tabs.items_names
        for tab in self.required_bet_slip_tabs:
            self.assertTrue(tab in actual_tab_menu,
                            msg=f'"{tab}" tab was not found Betslip header')
        bet_slip_tab = self.required_bet_slip_tabs[0]
        actual_selected_tab = self.get_betslip_content().name
        self.assertEquals(bet_slip_tab, actual_selected_tab,
                          msg=f'"{bet_slip_tab}" tab is not selected by default, instead "{actual_selected_tab}" is')
        actual_message = self.get_betslip_content().no_selections_title
        self.assertEqual(actual_message, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'Actual title message "{actual_message}" != Expected "{vec.betslip.NO_SELECTIONS_TITLE}"')
        if self.brand != 'ladbrokes':
            actual_message = self.get_betslip_content().no_selections_message
            self.assertEqual(actual_message, vec.betslip.NO_SELECTIONS_MSG,
                             msg=f'Actual body message "{actual_message}" != Expected "{vec.betslip.NO_SELECTIONS_MSG}"')

    def test_004_navigate_to_my_bets_sub_tab(self):
        """
        DESCRIPTION: Navigate to 'My Bets' sub-tab
        EXPECTED: My Bets tab is displayed and sub-headers are displayed including:
        EXPECTED: Cash Out
        EXPECTED: Open Bets
        EXPECTED: Settled Bets
        EXPECTED: Shop Bets
        EXPECTED: Open Bets sub-tab is selected by default and List of available not resulted bets is present
        """
        self.site.open_my_bets()
        tabs = self.site.betslip.tabs_menu.items_names
        self.assertTrue(tabs, msg='Tabs are not found')
        expected_tabs = [vec.bet_history.CASH_OUT_TAB_NAME,
                         vec.bet_history.OPEN_BETS_TAB_NAME,
                         vec.bet_history.SETTLED_BETS_TAB_NAME,
                         vec.bet_history.IN_SHOP_BETS_TAB_NAME]
        for tab in tabs:
            self.assertIn(tab, expected_tabs,
                          msg=f'Tab "{tab}" is not found in "{expected_tabs}"')

        self.assertTrue(
                self.site.betslip.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).is_selected(),
                msg=f'Tab "{vec.bet_history.OPEN_BETS_TAB_NAME}" is not selected by default')

    def test_005_navigate_to_open_bets_sub_tab(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' sub-tab
        EXPECTED: Sub-tab is opened with filter 'Regular'
        """
        self.__class__.widget_tabs = self.site.betslip.tabs_menu.items_as_ordered_dict
        self.widget_tabs.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.assertTrue(
            self.site.betslip.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).is_selected(),
            msg=f'Tab "{vec.bet_history.OPEN_BETS_TAB_NAME}" is not selected opened')

    def test_006_navigate_to_settled_bets_sub_tab(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' sub-tab
        EXPECTED: Calendar icons 'From' and 'To' are present
        """
        self.widget_tabs.get(vec.bet_history.SETTLED_BETS_TAB_NAME).click()
        self.assertTrue(self.site.bet_history.tab_content.accordions_list.date_picker.date_from.is_displayed(timeout=10),
                        msg='From is not displayed')
        self.assertTrue(self.site.bet_history.tab_content.accordions_list.date_picker.date_to.is_displayed(timeout=10),
                        msg='To is not displayed')

    def test_007_add_some_selections_to_betslip_and_verify_betslip_tab(self):
        """
        DESCRIPTION: Add some selections to betslip and verify 'Betslip' tab
        EXPECTED: Added selection is displayed in the Betslip content area
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No items found in Betslip content area')
        self.assertEqual(len(singles_section), 1,
                         msg=f'Singles selection count "{self.get_betslip_content().selections_count}" is not the same as expected "1"')
        self.assertTrue(singles_section.get(self.team1), msg=f'Selection "{self.team1}" is not found')
