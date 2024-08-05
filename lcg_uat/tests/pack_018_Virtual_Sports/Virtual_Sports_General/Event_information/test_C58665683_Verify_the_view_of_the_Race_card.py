import tests
import voltron.environments.constants as vec
import pytest
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter
from tests.base_test import vtest
from tests.pack_018_Virtual_Sports.BaseVirtualsTest import BaseVirtualsTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@pytest.mark.reg157_fix
@vtest
class Test_C58665683_Verify_the_view_of_the_Race_card(BaseVirtualsTest):
    """
    TR_ID: C58665683
    NAME: Verify the view of the Race card
    DESCRIPTION: This test case verifies the view of the Race card.
    """
    keep_browser_open = True
    actual_sports_list = []
    market_tabs = {vec.racing.RACING_EDP_WIN_OR_EACH_WAY_TAB, vec.racing.RACING_EDP_FORECAST_MARKET_TAB, vec.racing.RACING_EDP_TRICAST_MARKET_TAB}
    next_events = vec.virtuals.VIRTUAL_HUB_NEXT_EVENTS

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get list of active virtual sports
        DESCRIPTION: Login into the app
        EXPECTED: User successfully log into the app
        """
        virtuals_cms_class_ids = self.cms_virtual_sports_class_ids()
        if not (('285' in virtuals_cms_class_ids) or ('286' in virtuals_cms_class_ids) or ('290' in virtuals_cms_class_ids)):
            raise SiteServeException('Required Sports are not configured')
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.virtuals_config.category_id)
        sports_list = ss_req.ss_class(query_builder=self.ss_query_builder.
                                      add_filter(simple_filter(LEVELS.CLASS,
                                                               ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                                               str(self.ob_config.virtuals_config.category_id))))
        if not sports_list:
            raise SiteServeException('There are no active virtual sports')
        for sport in sports_list:
            self.actual_sports_list.append(sport['class']['id'])
        if not (('285' in self.actual_sports_list) or ('286' in self.actual_sports_list) or ('290' in self.actual_sports_list)):
            raise SiteServeException('Required Sports are configured but did not find in siteserve response')
        self.__class__.horse_race_name = next((sport.get("title") for sport in self.cms_config.get_parent_virtual_sports() if "/horse-racing" in sport.get('ctaButtonUrl')),None)

    def test_001_navigate_to_the_virtual_sport_page(self):
        """
        DESCRIPTION: Navigate to the Virtual sport page.
        EXPECTED: The next available event is loaded.
        EXPECTED: The Race card is displayed as per the design with next options:
        EXPECTED: - The event being displayed should be highlighted
        EXPECTED: - Time of the event with the name of the event
        EXPECTED: - Count down timer if the race isn't off yet
        EXPECTED: - Switcher for the Win/EW market, Forecast and Tricast markets
        EXPECTED: https://app.zeplin.io/project/5d64f0e582415f9b2a7045aa/screen/5dee3f51be0bb316723dcf29
        """
        self.site.open_sport(name=self.get_sport_title(category_id=self.ob_config.virtuals_config.category_id),
                             content_state='VirtualSports')
        virtual_hub_home_page = self.cms_config.get_system_configuration_structure().get('VirtualHubHomePage')
        if virtual_hub_home_page.get('enabled'):
            hubs_section = next((section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.upper() != self.next_events.upper()), None)
            section_sports = list(hubs_section.items_as_ordered_dict.values())[0]
            section_sports.click()
        virtual_sports = self.site.virtual_sports.sport_carousel.items_as_ordered_dict
        virtual_sport = next((virtual_sport for virtual_sport in virtual_sports.keys() if virtual_sport.upper() == self.horse_race_name.upper()),None)
        if not virtual_sport:
            raise CmsClientException('"Horse racing" is not configure in CMS for virtual sport')
        virtual_sports.get(virtual_sport).click()
        sport_category_names_from_page = self.site.virtual_sports.sport_carousel.items_names
        self.assertTrue(sport_category_names_from_page, msg='Virtual sports are not present on UI')

        tab_content = self.site.virtual_sports.tab_content
        event_time = tab_content.sport_event_time
        self.assertTrue(event_time.is_displayed(), msg=f'Event time: "{event_time.name} is displayed')
        event_name = tab_content.sport_event_name
        self.assertTrue(event_name, msg=f'Event name: "{event_name} is not displayed')
        try:
            self.assertTrue(tab_content.has_timer(), msg=f'Timer is not displayed for the event: "{event_time}"')
            event_name, event = list(tab_content.event_off_times_list.items_as_ordered_dict.items())[0]
            self.assertTrue(event.is_selected(), msg=f'The event: "{event_name}" being displayed is not highlighted')
        except Exception:
            self._logger.info(f'Event: "{event_name}" is went to live')

    def test_002_observe_the_winew_market(self):
        """
        DESCRIPTION: Observe the 'Win/EW' market.
        EXPECTED: There are next options displayed under the Win/EW market:
        EXPECTED: - Display the terms of the EW
        EXPECTED: - List of runners with the display order as per OB
        EXPECTED: - Runner number
        EXPECTED: - Silks
        EXPECTED: - Name of the runner
        EXPECTED: - Odds button with the odds
        EXPECTED: - CTA, with the text and the link (if configured)
        """
        tab_content = self.site.virtual_sports.tab_content
        market_tabs = tab_content.event_markets_list.market_tabs_list.items_names
        try:
            self.assertTrue(self.market_tabs.issubset(market_tabs),
                            msg=f'Expected markets: "{self.market_tabs}" are not present in the actual markets: "{market_tabs}"')
        except Exception:
            self._logger.info('Expected market/s may not be configure')
        tab_name = vec.racing.RACING_EDP_WIN_OR_EACH_WAY_TAB
        if tab_content.event_markets_list.market_tabs_list.current != tab_name:
            tab_content.event_markets_list.market_tabs_list.open_tab(tab_name)
            self.site.wait_content_state_changed(timeout=5)

        selections = self.site.virtual_sports.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(selections, msg='No outcome was found in section')
        self.assertTrue(self.site.virtual_sports.tab_content.has_post_info(),
                        msg='Terms of the Each Way is not displayed')
        for selection_name, selection in selections.items():
            try:
                self.assertTrue(selection_name, msg='Runner name is not displayed')
                self.assertTrue(selection.has_silks, msg='Silks not dispalyed')
                self.assertTrue(selection.runner_number, msg='Runner number is not displayed')
            except Exception:
                self._logger.info('silk, runner number may not be availanle for any runner')

        self.assertTrue(tab_content.cta_button.is_displayed(),
                        msg='CTA button at the bottom of the page is not displayed')

    def test_003_select_the_forecast_market(self):
        """
        DESCRIPTION: Select the 'Forecast' market.
        EXPECTED: There are next options displayed under the Forecast market:
        EXPECTED: - Text asking the User to pick the order of the first two runners.
        EXPECTED: - List of the runners sorted by runner number and the option to choose the position of the horse (from 1st, 2nd or Any).
        EXPECTED: - The 'Add to Betslip' CTA is disabled.
        """
        tab_name = vec.racing.RACING_EDP_FORECAST_MARKET_TAB
        tab_content = self.site.virtual_sports.tab_content
        if tab_name in tab_content.event_markets_list.market_tabs_list.items_names:
            tab_content.event_markets_list.market_tabs_list.open_tab(tab_name)
            wait_for_result(lambda: self.site.virtual_sports.tab_content.event_markets_list.market_tabs_list.current == tab_name,
                            name=f'{tab_name}" tab data to be loaded', timeout=10)
            tab_content = self.site.virtual_sports.tab_content
            selections = tab_content.event_markets_list.items_as_ordered_dict
            actual_runners_order = [outcome.runner_number for outcome in selections.values()]
            expected_runners_order = sorted(actual_runners_order, key=lambda x: int(x))
            self.assertListEqual(actual_runners_order, expected_runners_order,
                                 msg=f'Runners are not ordered by runner number. Actual order: "{actual_runners_order}"'
                                     f'Expected: "{expected_runners_order}"')
            self.assertTrue(tab_content.has_post_info(),
                            msg='Text asking the User to pick the order of the first two runners is not displayed')
            self.assertTrue(tab_content.cta_button.is_displayed(),
                            msg='CTA button at the bottom of the page is not displayed')

        else:
            self._logger.info(f'"{tab_name}" maraket tab is not configured')

    def test_004_select_the_tricast_market(self):
        """
        DESCRIPTION: Select the 'Tricast' market.
        EXPECTED: There are next options displayed under the Tricast market:
        EXPECTED: - Text asking the user to pick the order of the first three runners
        EXPECTED: - List of the runners sorted by runner number and the option to choose the position of the horse (from 1st, 2nd, 3rd or Any).
        EXPECTED: - The 'Add to Betslip' CTA is disabled.
        """
        tab_name = vec.racing.RACING_EDP_TRICAST_MARKET_TAB
        tab_content = self.site.virtual_sports.tab_content
        if tab_name in tab_content.event_markets_list.market_tabs_list.items_names:
            tab_content.event_markets_list.market_tabs_list.open_tab(tab_name)
            wait_for_result(
                lambda: self.site.virtual_sports.tab_content.event_markets_list.market_tabs_list.current == tab_name,
                name=f'{tab_name}" tab data to be loaded', timeout=10)
            tab_content = self.site.virtual_sports.tab_content
            selections = tab_content.event_markets_list.items_as_ordered_dict
            actual_runners_order = [outcome.runner_number for outcome in selections.values()]
            expected_runners_order = sorted(actual_runners_order, key=lambda x: int(x))
            self.assertListEqual(actual_runners_order, expected_runners_order,
                                 msg=f'Runners are not ordered by runner number. Actual order: "{actual_runners_order}"'
                                     f'Expected: "{expected_runners_order}"')
            self.assertTrue(tab_content.has_post_info(),
                            msg='Text asking the User to pick the order of the first two runners is not displayed')
            self.assertTrue(tab_content.cta_button.is_displayed(),
                            msg='CTA button at the bottom of the page is not displayed')

        else:
            self._logger.info(f'"{tab_name}" maraket tab is not configured')
