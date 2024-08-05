import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.module_ribbon
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.next_races
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28942_Verify_PriceOdds_Buttons(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C28942
    NAME: Verify Price/Odds Buttons
    DESCRIPTION: This test case is for checking of odds for each event which is displayed in 'Next Races' module.
    PRECONDITIONS: 1) To retrieve information from Site Server use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYY?translationLang=LL
    PRECONDITIONS: Where,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *YYYYY - an event id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes:
    PRECONDITIONS: -  **'priceTypeCodes'** to specify a type of price / odds buttons
    PRECONDITIONS: - **'priceDen' **and** ****'priceNum'** to specify price/odds value
    PRECONDITIONS: 2) To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/structure
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: 3) In order to get a list of **Next 4 Races **events and check** priceTypeCodes**
    PRECONDITIONS: check Networks -> **NextNEventToOutcomeForClass** response
    PRECONDITIONS: 4) Price type could be set in CMS (SP or LP)
    """
    keep_browser_open = True
    prices_LP = {0: '1/5'}
    prices_LP_SP = {0: '1/2'}
    autotest_uk_name_pattern = None

    def check_price_correctness_for_event(self, event, event_name, event_id):
        """
        :param event: Event object
        :param event_name: Event name
        :param event_id: Appropriate Event id
        :return:
        """
        event.scroll_to()
        outcomes = event.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No outcomes found for "{event_name}"')
        for name, outcome in outcomes.items():
            bet_button = outcome.bet_button
            bet_button.scroll_to()
            price = bet_button.outcome_price_text
            self.assertRegexpMatches(price, self.fractional_pattern,
                                     msg=f'Odds value for current selections combination "{price}" '
                                     f'is not in correct format "{self.fractional_pattern}"')

            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id,
                                                                   query_builder=self.ss_query_builder)
            self.__class__.outcomes_resp = event_resp[0]['event']['children'][0]['market']['children']
            price_resp = next((i["outcome"]["children"][0]["price"] for i in self.outcomes_resp
                               if 'price' in i["outcome"]["children"][0].keys() and i["outcome"]['name'] == name), '')
            self._logger.debug(f'\nOutcome name: {name} \nOutcome response: {self.outcomes_resp} \nprice_resp {price_resp}')
            self.assertTrue(price_resp, msg=f'Price is not found in Siteserve response "{self.outcomes_resp}"')
            price_resp = f'{price_resp["priceNum"]}/{price_resp["priceDen"]}'
            self.assertEqual(price, price_resp,
                             msg=f'Price "{price}" is '
                             f'not the same as in response "{price_resp}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        self.setup_cms_next_races_number_of_events()
        type_id = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id
        self.check_and_setup_cms_next_races_for_type(type_id=type_id)

        self.__class__.next_races_tab_name = self.get_ribbon_tab_name(
            self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.next_races, raise_exceptions=False)

        self.assertTrue(self.next_races_tab_name,
                        msg=f'Tab name for "{self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.next_races}" '
                            f'internal id was not found')

        event_params_SP = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1,
                                                             time_to_start=3, sp=True, lp=False)
        event_off_time_SP = event_params_SP.event_off_time
        self.__class__.event_name_SP = f'{event_off_time_SP} {self.horseracing_autotest_uk_name_pattern}'
        if self.device_type != 'desktop' or self.brand != 'bma':
            self.__class__.event_name_SP = self.event_name_SP.upper()

        event_params_LP = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1,
                                                             time_to_start=5, sp=False, lp=True,
                                                             lp_prices=self.prices_LP)
        self.__class__.event_id_LP = event_params_LP.event_id
        event_off_time_LP = event_params_LP.event_off_time
        self.__class__.event_name_LP = f'{event_off_time_LP} {self.horseracing_autotest_uk_name_pattern}'

        event_params_LP_SP = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1,
                                                                time_to_start=10, sp=True, lp=True,
                                                                lp_prices=self.prices_LP_SP)
        self.__class__.event_id_LP_SP = event_params_LP_SP.event_id
        event_off_time_LP_SP = event_params_LP_SP.event_off_time
        self.__class__.event_name_LP_SP = \
            f'{event_off_time_LP_SP} {self.horseracing_autotest_uk_name_pattern}'

        event_params_LP_SP_negative = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1,
                                                                         time_to_start=20, sp=True, lp=True,
                                                                         lp_prices=None)
        self.__class__.event_id_LP_SP_neg = event_params_LP_SP_negative.event_id
        event_off_time_LP_SP_neg = event_params_LP_SP_negative.event_off_time
        self.__class__.event_name_LP_SP_neg = \
            f'{event_off_time_LP_SP_neg} {self.horseracing_autotest_uk_name_pattern}'

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        self.site.wait_content_state('Homepage')

    def test_002_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page
        EXPECTED: * 'Horse Racing' Landing page is opened
        EXPECTED: * 'Featured' tab is opened by default
        EXPECTED: * 'Next Races' module is displayed
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing')
        current_tab = self.site.horse_racing.tabs_menu.current
        self.softAssert(self.assertEqual, current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                        msg=f'Current tab "{current_tab}" is not the same as '
                        f'expected "{vec.racing.RACING_DEFAULT_TAB_NAME}"')

    def test_003_verify_next_races_module(self):
        """
        DESCRIPTION: Verify 'Next Races' module
        EXPECTED: The 'Next Races' available events are shown
        """
        next_races = self.get_next_races_section()
        self.softAssert(self.assertTrue, next_races.is_expanded(), msg='Next4 expected to be expanded by default')

    def test_004_from_the_site_server_find_event_where_price_type_codes_sp_and_check_price_odds_in_the_next_races_module(self):
        """
        DESCRIPTION: From the Site Server find event where:
        DESCRIPTION: *   '**priceTypeCodes'** = 'SP, '
        DESCRIPTION: and check price / odds in the 'Next Races' module
        EXPECTED: 'SP' price / odds buttons are displayed next to each selection
        """
        event = self.get_event_from_next_races_module(event_name=self.event_name_SP)
        outcomes = event.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No outcomes found for event {self.event_name_SP}')
        for outcome_name, outcome in outcomes.items():
            outcome.bet_button.scroll_to()
            self.softAssert(self.assertEqual, outcome.bet_button.outcome_price_text, 'SP',
                            msg=f'Outcome "{outcome_name}" does not have "SP" price')

    def test_005_from_the_site_server_find_event_where_pricetypecodes_lp_and_check_priceodd_in_the_next_races_module(self, expected_event_name=None, expected_event_id=None):
        """
        DESCRIPTION: From the Site Server find event where:
        DESCRIPTION: *    **'priceTypeCodes'** = 'LP, '
        DESCRIPTION: and check price/odd in the 'Next Races' module
        EXPECTED: The 'LP' price/odd button is displayed in decimal or fractional format (depends upon the users chosen odds display preference)
        EXPECTED: Prices correspond to the **'priceNum'** and** 'priceDen'** attributes from the Site Server
        """
        event_name, event_id = (expected_event_name, expected_event_id) \
            if expected_event_name and expected_event_id else (self.event_name_LP, self.event_id_LP)

        event_name = event_name if self.device_type == 'desktop' and self.brand == 'bma' else event_name.upper()
        event = self.get_event_from_next_races_module(event_name=event_name)
        self.check_price_correctness_for_event(event=event, event_id=event_id, event_name=event_name)

    def test_006_from_the_site_server_response_find_event_where_price_type_code_sp_lp_prices_are_availabe_for_outcomes_and_check_priceodds_in_the_next_races_module(self):
        """
        DESCRIPTION: From the Site Server response find event where:
        DESCRIPTION: *   **'priceTypeCode'**='SP, LP, '
        DESCRIPTION: *   Prices ARE available for outcomes
        DESCRIPTION: and check price/odds in the 'Next Races' module
        EXPECTED: 'LP' price / odd buttons are displayed in fractional / decimal format next to each selection
        EXPECTED: Prices correspond to the **'priceNum'** and** 'priceDen'** attributes from the Site Server
        """
        self.test_005_from_the_site_server_find_event_where_pricetypecodes_lp_and_check_priceodd_in_the_next_races_module(self.event_name_LP_SP, self.event_id_LP_SP)

    def test_007_from_the_site_server_response_find_event_where_pricetypecodesp_lp_prices_are_not_availabe_for_outcomesand_check_priceodds_in_the_next_races_module(self):
        """
        DESCRIPTION: From the Site Server response find event where:
        DESCRIPTION: *   **'priceTypeCode'**='SP, LP, '
        DESCRIPTION: *   Prices are NOT available for outcomes
        DESCRIPTION: and check price/odds in the 'Next Races' module
        EXPECTED: 'SP' price / odds buttons are shown next to each selection
        """
        event_name = self.event_name_LP_SP_neg if self.device_type == 'desktop' and self.brand == 'bma' \
            else self.event_name_LP_SP_neg.upper()
        event = self.get_event_from_next_races_module(event_name=event_name)
        outcomes = event.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No outcomes found for event "{event_name}"')
        for outcome_name, outcome in outcomes.items():
            outcome.bet_button.scroll_to_we()
            self.softAssert(self.assertEqual, outcome.bet_button.outcome_price_text, 'SP',
                            msg=f'Outcome "{outcome_name}" does not have "SP" price')

    def test_008_for_mobile_and_tablet_go_to_the_homepage_tap_next_races_tab_from_the_module_selector_ribbon(self):
        """
        DESCRIPTION: **For Mobile and Tablet:**
        DESCRIPTION: Go to the homepage -> tap 'Next Races' tab from the module selector ribbon
        EXPECTED: **For Mobile and Tablet:**
        EXPECTED: 'Next Races' module is shown
        """
        if self.device_type == 'mobile':
            self.site.go_to_home_page()
            self.site.home.get_module_content(module_name=self.next_races_tab_name)
            self.assertTrue(self.site.home.tab_content,
                            msg=f'{self.next_races_tab_name} module is not found')
            tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            self.softAssert(self.assertTrue, tabs[self.next_races_tab_name].is_selected(),
                            msg=f'{self.next_races_tab_name} is not selected after clicking on it')

    def test_009_for_mobile_and_tablet_repeat_steps_4_7(self):
        """
        DESCRIPTION: **For Mobile and Tablet:**
        DESCRIPTION: Repeat steps # 4 - 7
        EXPECTED:
        """
        if self.device_type == 'mobile':
            events = self.site.home.get_module_content(module_name=self.next_races_tab_name).accordions_list.items_as_ordered_dict
            self.assertTrue(events, msg='No one event was found in Next Races section')
            for event_name, event_id in {self.event_name_LP: self.event_id_LP,
                                         self.event_name_LP_SP: self.event_id_LP_SP}.items():
                event_name_by_brand = event_name.upper() if self.brand == 'ladbrokes' else event_name
                event = events.get(event_name_by_brand)
                self.assertTrue(event, msg=f'Event "{event_name_by_brand}" was not found in "{events.keys()}"')
                event.scroll_to()
                self.check_price_correctness_for_event(event=event, event_id=event_id, event_name=event_name_by_brand)

            event_name = self.event_name_LP_SP_neg.upper() if self.brand == 'ladbrokes' else self.event_name_LP_SP_neg
            event = events.get(event_name)
            self.assertTrue(event, msg=f'Event "{event_name}" was not found in "{events.keys()}"')
            event.scroll_to()
            outcomes = event.items_as_ordered_dict
            self.assertTrue(outcomes, msg=f'No outcomes found for event "{self.event_name_LP_SP_neg}"')
            for outcome_name, outcome in outcomes.items():
                outcome.bet_button.scroll_to_we()
                self.softAssert(self.assertEqual, outcome.bet_button.outcome_price_text, 'SP',
                                msg=f'Outcome "{outcome_name}" does not have "SP" price')

    def test_010_for_desktop_go_to_the_desktop_homepage_check_next_races_section_under_the_in_play_section(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Go to the desktop homepage -> check 'Next Races' section under the 'In-Play' section
        EXPECTED: **For Desktop:**
        EXPECTED: 'Next Races' section is shown
        """
        if self.device_type != 'mobile':
            self.site.go_to_home_page()
            home_page_modules = self.site.home.desktop_modules.items_as_ordered_dict
            self.assertTrue(home_page_modules, msg='Home page modules not found on Home Page')

            next_races_section = home_page_modules.get(self.next_races_tab_name)
            self.assertTrue(next_races_section.is_displayed(),
                            msg=f'"{self.next_races_tab_name}" section was not found in "{home_page_modules.keys()}"')

    def test_011_for_desktop_repeat_steps_4_7(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps # 4 - 7
        EXPECTED:
        """
        if self.device_type != 'mobile':
            events = self.site.home.get_module_content(module_name=self.next_races_tab_name).accordions_list.items_as_ordered_dict
            self.assertTrue(events, msg='No one event was found in Next Races section')
            for event_name, event_id in {self.event_name_LP: self.event_id_LP,
                                         self.event_name_LP_SP: self.event_id_LP_SP}.items():
                event_name_by_brand = event_name.upper() if self.brand == 'ladbrokes' else event_name
                event = events.get(event_name_by_brand)
                self.assertTrue(event, msg=f'Event "{event_name_by_brand}" was not found in "{events.keys()}"')
                event.scroll_to()
                self.check_price_correctness_for_event(event=event, event_id=event_id, event_name=event_name)

            event_name = self.event_name_LP_SP_neg.upper() if self.brand == 'ladbrokes' else self.event_name_LP_SP_neg
            event = events.get(event_name)
            self.assertTrue(event, msg=f'Event "{event_name}" was not found in "{events.keys()}"')
            event.scroll_to()
            outcomes = event.items_as_ordered_dict
            self.assertTrue(outcomes, msg=f'No outcomes found for event "{self.event_name_LP_SP_neg}"')
            for outcome_name, outcome in outcomes.items():
                outcome.bet_button.scroll_to_we()
                self.assertEqual(outcome.bet_button.outcome_price_text, 'SP',
                                 msg=f'Outcome "{outcome_name}" does not have "SP" price')
