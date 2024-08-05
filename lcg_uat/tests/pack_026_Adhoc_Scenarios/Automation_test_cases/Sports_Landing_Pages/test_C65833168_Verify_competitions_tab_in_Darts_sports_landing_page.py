import pytest
import random
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.timeout(900)
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.market_switcher
@pytest.mark.sports_specific
@pytest.mark.darts_union_specific
@vtest
class Test_C65833168_Verify_competitions_tab_in_Darts_sports_landing_page(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C65833168
    NAME: Verify "competitions tab" in Darts sports landing page
    DESCRIPTION: Verify "competitions tab" in Darts sports landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets "Market template name" which is in OB should be mentioned in Primary markets" section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: D) Markets which are configured in Primary markets should be added to Market Switcher Labels Table under Competitions Tab In CMS
    PRECONDITIONS: sports pages > sport category >  > Competitions Tab > Market Switcher Labels Table
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Darts Competition page -> 'competitions'  tab
     """
    keep_browser_open = True
    bet_amount = 0.2
    preplay_list = []
    inplay_list = []

    # Markets for Events created in OB(Stg/tst only)
    event_markets = [
        ('match_handicap', {}),
        ('total_180s_over_under', {}),
        ('most_180s', {})
    ]

    # CMS Markets Config for Created Market in OB(Stg/tst only)
    cms_markets_names = [
        {
            "templateMarketName": "Match Result",
            "title": "Match Result",
            "aggregated": False
        },
        {
            "templateMarketName": "Most 180s",
            "title": "Most 180s",
            "aggregated": False
        },
        {
            "templateMarketName": "Total 180s Over/Under",
            "title": "Total 180s",
            "aggregated": False
        },
        {
            "templateMarketName": "Match Handicap",
            "title": "Handicap",
            "aggregated": False
        }
    ]

    def verify_fixture_and_market(self, market, header1=None, header2=None, header3=None, bet_button_qty=None):
        # Check If market param is selected by default in the Market Selector drop-down
        market_dropdown_selector = self.site.darts.tab_content.dropdown_market_selector
        all_markets = market_dropdown_selector.available_options
        market_to_select = market
        self.assertIn(market_to_select,
                      all_markets,
                      msg=f'Actual markets: '
                          f'{all_markets} does not contain expected market: '
                          f'{market_to_select} ')
        if not self.site.darts.tab_content.dropdown_market_selector.is_expanded():
            self.site.darts.tab_content.dropdown_market_selector.expand()
        market_dropdown_selector.items_as_ordered_dict.get(market_to_select).click()
        if bet_button_qty == 3:
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3,
                                                              header1=header1,
                                                              header2=header2,
                                                              header3=header3)
        elif bet_button_qty == 2:
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2,
                                                              header1=header1,
                                                              header3=header3)
        else:
            raise ValueError(f'bet_button_qty: {bet_button_qty} is not valid')

    def place_bet_and_verify(self):
        darts_section = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        events = list(darts_section.items_as_ordered_dict.values())
        self.assertTrue(events, msg=f'Events is not found')
        if len(events) >= 2:
            event1, event2 = events[0], events[1]
            bet_buttons = event1.template.get_available_prices()
            self.assertTrue(bet_buttons, msg='No selections found')
            event2_bet_buttons = event2.template.get_available_prices()
            self.assertTrue(event2_bet_buttons, msg='No selections found')
        else:
            bet_buttons = events[0].template.get_available_prices()
            self.assertTrue(bet_buttons, msg='No selections found')
        # multiple
        try:
            if len(events) >= 2:
                bet_button = random.choice(list(bet_buttons.values()))
                self.site.wait_splash_to_hide(5)
                if self.drop_down.is_expanded():
                    self.drop_down.click()
                bet_button.click()
                if self.device_type == 'mobile':
                    sleep(3)
                    self.site.add_first_selection_from_quick_bet_to_betslip()
                bet_button = random.choice(list(event2_bet_buttons.values()))
                self.site.wait_splash_to_hide(5)
                if self.drop_down.is_expanded():
                    self.drop_down.click()
                bet_button.click()
                self.site.open_betslip()
                self.place_multiple_bet()
                self.check_bet_receipt_is_displayed()
                self.site.close_betreceipt()
        except VoltronException as e:
            self._logger.info('*** can not place a multiple bet as there is only one event present***')
            self.site.close_betslip()
        # single betplacement
        bet_button = random.choice(list(bet_buttons.values()))
        # self.site.wait_splash_to_hide(10)
        if self.drop_down.is_expanded():
            self.drop_down.click()
        bet_button.click()
        if self.device_type == 'mobile':
            sleep(3)
            self.site.add_first_selection_from_quick_bet_to_betslip()
        self.site.open_betslip()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

        # single betplacement through quick bet
        if self.device_type == 'mobile':
            bet_button = random.choice(list(bet_buttons.values()))
            # self.site.wait_splash_to_hide(10)
            if self.drop_down.is_expanded():
                self.drop_down.click()
            bet_button.click()
            sleep(3)
            quick_bet = self.site.quick_bet_panel
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            self.site.wait_content_state_changed()
            quick_bet.place_bet.click()
            bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            quick_bet.header.close_button.click()

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1=None, header3=None, header2=None):
        items = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        events = items.items_as_ordered_dict.values()
        self.assertTrue(events, msg='"Events" are not available')
        event = items.fixture_header
        self.assertEqual(event.header1, header1,
                         msg=f'Actual fixture header "{event.header1}" does not equal to'
                             f'Expected "{header1}"')
        if header2:
            self.assertEqual(event.header2, header2,
                             msg=f'Actual fixture header "{event.header2}" does not equal to'
                                 f'Expected "{header2}"')
        self.assertEqual(event.header3, header3,
                         msg=f'Actual fixture header "{event.header2}" does not equal to'
                             f'Expected "{header3}"')

        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.keys()))
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the darts Landing page -> 'Competitions' tab
        """

        # Lower Envs
        if tests.settings.backend_env != "prod":
            # Enabling market Selector if Disabled in CMS
            self.cms_config.verify_and_update_market_switcher_status(sport_name='darts', status=True)

            # verifying and updating the sport configuration(General Configurations) based on these arguments.
            self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.darts_config.category_id,
                                                           disp_sort_names='HH,MR,WH,HL',
                                                           primary_markets=f'|{"Match Betting"}|,|{"Most 180s"}|,|{"Total 180s Over/Under"}|,|{"Match Handicap"}|')

            # Adding Market Switcher Labels to Competitions tabs
            self.cms_config.update_sport_config(
                tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                enabled=True,
                sport_id=self.ob_config.darts_config.category_id,
                marketsNames=self.cms_markets_names)

            # Creating Three Events For Each markets
            for i in range(0, 3):
                self.ob_config.add_darts_event_to_darts_all_darts(markets=self.event_markets)
        else:
            # For beta And prod

            # Check if competitions tab is enabled for darts in CMS
            dart_competitions_tab_status: bool = self.cms_config.get_sport_tab_status(
                sport_id=self.ob_config.darts_config.category_id,
                tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions
            )

            # Check if market switcher is enabled for darts in CMS
            darts_market_switcher_status: bool = self.cms_config.get_initial_data() \
                ['systemConfiguration']['MarketSwitcher']['darts']

            if not darts_market_switcher_status:
                raise CmsClientException(f"CMS Configuration Are Not Correct:"
                                         f"Market Switcher Status for dart in CMS:{darts_market_switcher_status},"
                                         )

        # Getting Display name For Competitions tab
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.darts_config.category_id)

        # login and navigate to darts SLP
        self.site.login()
        self.navigate_to_page("sport/darts")
        self.site.wait_content_state('darts')

        # getting tabs name from front end
        tabs = self.site.contents.tabs_menu.items_as_ordered_dict
        tabs_names = [tab.upper() for tab in tabs]
        if not dart_competitions_tab_status and expected_tab_name.upper() not in tabs_names:
            raise CmsClientException(f' "{expected_tab_name}" tab is not enabled in CMS for Darts')
        self.assertTrue(tabs.get(expected_tab_name),
                        msg='competitions tab is not available.')
        # Click On expected tab name i.e (Competitions Tab)
        tabs.get(expected_tab_name).click()
        self.site.wait_content_state_changed()

        # Check If Current tab is Equal to Expected tab name
        current_tab_name = self.site.contents.tabs_menu.current
        if current_tab_name != expected_tab_name:
            tabs.get(expected_tab_name).click()
            current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected Tab: "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: &bull; &lsquo;Market Selector&rsquo; is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: &bull;'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: &bull; 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: &bull; 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: &bull; Chevron (pointing down) are shown next to 'Match Result' Ladbrokes
        EXPECTED: &bull; Up and down arrows are shown next to 'Match Result' in 'Market selector' Coral
        """

        # Checking if the Market Selector dropdown is displayed
        market_selector_dropdown = self.site.darts.tab_content.dropdown_market_selector
        self.assertTrue(market_selector_dropdown, msg=f"Market Selector Dropdown is Not Displayed")

        if self.device_type == "mobile":
            # Checking for Change button
            change_button = market_selector_dropdown.change_button
            self.assertTrue(change_button, msg=f"Change Button is Not Displayed Below Market Dropdown Selector")
            market_selector_dropdown.collapse()
            change_button.click()

            # Checking if Market Selector Is Expanded After Clicking On the Change Button
            expanded = market_selector_dropdown.is_expanded()
            self.assertTrue(expanded, msg=f"Market Selector is not Expanded After Clicking On Change button")

        # Check if current Date tab has market drop-down selector
        self.assertTrue(self.site.darts.tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on darts landing page')
        # Getting the first available Market in the Market Selector drop-down
        market_selector_first_market = market_selector_dropdown.available_options[0].title()

        # Getting the default Market in the Market Selector drop-down
        actual_default_market = market_selector_dropdown.selected_market_selector_item.title()

        # Checking if First available Market is selected by default
        self.assertEqual(actual_default_market, market_selector_first_market, msg=f"Market"
                                                                                  f"{market_selector_first_market}"
                                                                                  f"is not selected by default, instead"
                                                                                  f"{actual_default_market} "
                                                                                  f"is selected by default")

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: &bull; Match Result
        EXPECTED: &bull; Most 180s
        EXPECTED: &bull; Handicap
        EXPECTED: &bull; Total 180s
        EXPECTED: Note:
        EXPECTED: &bull; If any Market is not available then it is skipped in the Market selector drop down list*
        """
        # Get All Market in Market Selector drop-down
        self.__class__.available_markets = [market.title() for market in self.site.darts.tab_content.dropdown_market_selector.available_options]
        self.__class__.expected_markets_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default,
                                                vec.siteserve.EXPECTED_MARKETS_NAMES.most_180s,
                                                vec.siteserve.EXPECTED_MARKETS_NAMES.total_180s_over_under,
                                                vec.siteserve.EXPECTED_MARKETS_NAMES.handicap]
        if tests.settings.backend_env != "prod":
            # Checking if All Market Selector is available as per Created Events
            self.assertListEqual(self.expected_markets_list,
                                 self.available_markets,
                                 msg=f'Expected list: {self.expected_markets_list} '
                                     f'does not match Actual list: {self.available_markets}')
        else:
            # Checking if All Markets are available in FE as configured in the CMS
            expected_markets = self.cms_config \
                .get_sports_tab_data(sport_id=self.ob_config.darts_config.category_id, tab_name='competitions') \
                ['marketsNames']
            expected_markets = [market['title'].title() for market in expected_markets]

            # Verify Default Markets Selection From Cms

            # If Events are not available For any market then skip the validation
            for market in self.available_markets:
                self.softAssert(self.assertIn, market.title(), expected_markets,
                                msg=f'Actual market: {market} is not present in '
                                    f'the Expected list: {expected_markets}')

    def test_003_select_match_result_in_the_market_selector_dropdown_list(self):

        """
        DESCRIPTION: Select 'Match Result' in the 'Market Selector' dropdown list
        EXPECTED: &bull; The events for selected market are shown
        EXPECTED: &bull; Values on Fixture header are changed for each event according to selected market
        EXPECTED: &bull; Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        # covered in step 4

    def test_004_repeat_step_3_for_the_following_marketsbull_most_180sbull_handicapbull_total_180s(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: &bull; Most 180s
        DESCRIPTION: &bull; Handicap
        DESCRIPTION: &bull; Total 180s
        EXPECTED:
        """
        for market in self.available_markets:
            if market in self.expected_markets_list:
                self._logger.info(msg=f'Market: {market} is selected')
                # Match Result
                if market == vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default:
                    self.verify_fixture_and_market(
                        market=vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default,
                        header1="1", header2=None, header3="2", bet_button_qty=2)
                # Most 180s
                elif market == vec.siteserve.EXPECTED_MARKETS_NAMES.most_180s:
                    self.verify_fixture_and_market(
                        market=vec.siteserve.EXPECTED_MARKETS_NAMES.most_180s,
                        header1="1", header2="TIE", header3="2", bet_button_qty=3)
                # Total 180s
                elif market == vec.siteserve.EXPECTED_MARKETS_NAMES.total_180s_over_under:
                    self.verify_fixture_and_market(
                        market=vec.siteserve.EXPECTED_MARKETS_NAMES.total_180s_over_under,
                        bet_button_qty=2, header1=vec.sb.OVER.upper(),
                        header3=vec.sb.UNDER.upper())
                # Handicap
                elif market == vec.siteserve.EXPECTED_MARKETS_NAMES.handicap or market == vec.siteserve.EXPECTED_MARKETS_NAMES.handicap_2_way:
                    self.verify_fixture_and_market(
                        market=market,
                        header1="1", header3="2", bet_button_qty=2)

    def test_005_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_marketsbull_match_resultbull_most_180sbull_handicapbull_total_180s(
            self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: &bull; Match Result
        DESCRIPTION: &bull; Most 180s
        DESCRIPTION: &bull; Handicap
        DESCRIPTION: &bull; Total 180s
        EXPECTED: Bet should be placed successfully
        """
        market_dropdown_selector = self.site.darts.tab_content.dropdown_market_selector
        self.__class__.drop_down = market_dropdown_selector
        all_markets = market_dropdown_selector.available_options
        all_markets = all_markets[:3] if len(all_markets) >= 3 else all_markets
        for market in all_markets:
            market_dropdown_selector = self.site.darts.tab_content.dropdown_market_selector
            market_dropdown_selector.items_as_ordered_dict.get(market).click()
            self.place_bet_and_verify()
