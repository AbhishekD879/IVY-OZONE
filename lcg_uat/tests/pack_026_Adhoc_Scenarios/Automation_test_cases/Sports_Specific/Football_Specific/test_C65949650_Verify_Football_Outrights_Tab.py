import re
import pytest
import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.sports_specific
@pytest.mark.football_specific
@pytest.mark.desktop
@vtest
class Test_C65949650_Verify_Football_Outrights_Tab(BaseSportTest):
    """
    TR_ID: C65949650
    NAME: Verify Football Outrights Tab
    DESCRIPTION: This test case verifies football specials tab
    PRECONDITIONS: 1.Outright events should be configured in OB
    PRECONDITIONS: 2.Outrights tab should be enabled in CMS for
    PRECONDITIONS: football sport
    """
    keep_browser_open = True
    sport_name = vec.sb.FOOTBALL

    def extract_event_id_from_url(self):
        """
        Function to extract the last numbers(event id) from the URL
        """
        current_url = self.device.get_current_url()
        parts = current_url.split('/')
        for part in reversed(parts):
            if part.isnumeric():
                return part

    def test_000_preconditions(self):
        """
        Description : checking outrights tab is enable or disable in cms
        Description : if it is disabled making it enable in cms
        Description : getting all outright events
        """
        # checking whether outrights tab is enable or disable
        sport_id = self.ob_config.football_config.category_id
        response = self.cms_config.get_sports_tab_data(sport_id=sport_id, tab_name='outrights')
        # making outrights tab is enabled in cms if it is disable in cms
        if not response['enabled']:
            tab_id = self.cms_config.get_sport_tab_id(sport_id=sport_id,
                                                      tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights)
            self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="true",
                                                     sport_id=sport_id)

    def test_001_launch_application_and_navigate_to_football_page(self):
        """
        DESCRIPTION: Launch application and navigate to football page
        EXPECTED: By default matches tab should load
        """
        self.site.open_sport(name='FOOTBALL')
        current_tab_name = self.site.football.tabs_menu.current.upper()
        expected_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper()
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Default tab is not "{expected_tab_name}", it is "{current_tab_name}"')
        if self.device_type == 'desktop':
            actual_date_tab_name = self.site.football.date_tab.current_date_tab
            self.assertEqual(actual_date_tab_name, vec.sb.SPORT_DAY_TABS.today,
                             msg=f'Actual date tab is "{actual_date_tab_name}" not "{vec.sb.SPORT_DAY_TABS.today}"')

    def test_002_navigate_to_outrights_tab(self):
        """
        DESCRIPTION: Navigate to Outrights tab
        EXPECTED: Outrights tab should load with all available outright events
        """
        outright_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper()
        self.site.football.tabs_menu.click_button(outright_tab_name)

    def test_003_verify_outright_accordians(self):
        """
        DESCRIPTION: Verify Outright accordians
        EXPECTED: Outrights accordians should be collapsable and expandable
        """
        # getting accordions in outrights tab and checking whether each accordians is expanded and collapsed
        sections = list(self.site.contents.tab_content.accordions_list.get_items(number=4).values())
        self.assertTrue(sections, msg=f'no accordions are found')
        for section in sections:
            section.expand()
            self.assertTrue(section.is_expanded(), msg='section is not expanded')
            section.collapse()
            self.assertFalse(section.is_expanded(), msg='section is not collapse')

    def test_004_click_on_any_outright_event(self):
        """
        DESCRIPTION: Click on any outright event
        EXPECTED: Outright event details page should load with available markets
        """
        first_accordion = list(self.site.contents.tab_content.accordions_list.get_items(number=2).values())[0]
        first_accordion.expand()
        self.assertTrue(first_accordion.is_expanded(), msg='section is not expanded')
        events = list(first_accordion.items_as_ordered_dict.values())
        self.assertTrue(events, msg=f'Events not found')
        events[0].click()
        self.site.wait_content_state(state_name='EventDetails')

    def test_005_verify_out_right_event_details_page(self):
        """
        DESCRIPTION: Verify Outright event details page
        EXPECTED: Markets and selections should be displayed.
        EXPECTED: Markets should be expandable and collapsable.
        EXPECTED: If any market has more selections show all link should be displayed.
        """
        # verifying event details page in front end
        if self.device_type == "mobile":
            wait_for_haul(5)
            event_name_details_page = wait_for_result(lambda: self.site.sport_event_details.event_name.strip(), timeout=30)
            self.assertTrue(event_name_details_page, msg=f'event name is not displayed')
        else:
            event_name_details_page = wait_for_result(lambda: self.site.sport_event_details.event_title_bar.event_name, timeout=30)
            self.assertTrue(event_name_details_page, msg=f'event name is not displayed')
        self._logger.debug(f'*** Event name on event details page: "{event_name_details_page}"')
        result = re.match(tests.settings.football_event_name_pattern, event_name_details_page, re.U)
        self.assertTrue(result, msg=f'Item text "{event_name_details_page}" not matching pattern'
                                    f'"{tests.settings.football_event_name_pattern}"')

        # verifying markets are present or not and expandable and collapsable
        markets = self.site.sport_event_details.tab_content.accordions_list.get_items(number=4)
        self.assertTrue(markets, msg=f'markets are not available in event details page')
        self.__class__.event_response = \
            self.ss_req.ss_event_to_outcome_for_event(event_id=self.extract_event_id_from_url())[0].get('event')
        for market_name, market in markets.items():
            market.expand()
            self.assertTrue(market.is_expanded(), msg='section is not expanded')

            markets_cms = self.event_response.get('children')
            outcomes_length = len(next((market_cms['market']['children']) for market_cms in markets_cms if
                                       market_cms['market']['name'].strip('|').upper() == market_name.upper()))

            # verifying selections are present or not under accordions
            selections = market.outcomes.items_as_ordered_dict
            self.assertEqual(bool(outcomes_length), bool(selections), msg=f'selections are not available')

            # validating show all button if outcomes are more than six
            self.assertEqual(outcomes_length > 6, market.has_show_all_button,
                             msg=f'show all button is {"not displayed even outcomes have more than 6" if outcomes_length > 6 else "is displayed even outcomes less than 6"}')
            market.collapse()
            self.assertFalse(market.is_expanded(), msg='section is not collapse')

    def test_006_verify_signpostings(self):
        """
        DESCRIPTION: Verify Signpostings
        EXPECTED: Sign postings should be displayed (if available)
        EXPECTED: eg: cashout
        EXPECTED: Mobile:
        EXPECTED: Favourite (star) icon should be displayed
        """
        market_name,first_market = next(iter(self.site.sport_event_details.tab_content.accordions_list.get_items(number=2).items()))

        # verifying cash_out sign_post is displaying or not
        if self.event_response['cashoutAvail'] == 'Y':
            cashout_status_of_market = next(market_cms['market']['cashoutAvail'] == 'Y' for market_cms in self.event_response.get('children') if
                                            market_cms['market']['name'].strip('|').upper() == market_name.upper())
            actual_cashout_status = first_market.section_header.has_cash_out_mark()
            self.assertEqual(cashout_status_of_market, actual_cashout_status,
                             f'Actual Cashout Status : {actual_cashout_status} is not Expected Status : {cashout_status_of_market}')

        # verifying favourites icon is displaying or not in sport event details page
        # favourites icon is applicable for Coral mobile only
        if self.device_type == 'mobile' and self.brand == 'bma':
            self.assertTrue(self.site.sport_event_details.header_line.has_favourites_icon,
                            msg='Favourite icon is not displayed on Football Event Details page')
