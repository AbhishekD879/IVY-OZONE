from time import sleep

import pytest
import tests
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.environments import constants as vec


# @pytest.mark.tst2  Can not get BYB events in QA2
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@pytest.mark.desktop
@vtest
class Test_C28946288_Banach_URLs_of_BYB_pages(BaseBanachTest):
    """
    TR_ID: C28946288
    NAME: Banach. URLs of BYB pages
    DESCRIPTION: Test case verifies URLs of **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) pages
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Note:**
    PRECONDITIONS: **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) tab on Homepage/event details page is loaded
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    proxy = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find event with Banach markets
        """
        self.__class__.event_id = self.get_ob_event_with_byb_market()

        byb_leagues_presence = self.check_byb_leagues_presence()
        self.__class__.today_banach_leagues = byb_leagues_presence.today and bool(
            self.get_mapped_leagues(date_range='today'))
        self.__class__.upcoming_banach_leagues = byb_leagues_presence.upcoming and bool(
            self.get_mapped_leagues(date_range='upcoming'))

        if not any([self.today_banach_leagues, self.upcoming_banach_leagues]):
            raise SiteServeException('Neither Today nor Upcoming Banach events found')

        is_byb_configured_in_cms = next((tab for tab in self.cms_config.module_ribbon_tabs.visible_tabs_data
              if tab.get('directiveName') == 'BuildYourBet'), None)

        if is_byb_configured_in_cms:
            data = next((tab for tab in self.cms_config.module_ribbon_tabs.visible_tabs_data
                         if tab.get('directiveName') == 'BuildYourBet'), None)
            self.__class__.universal_segment = data['universalSegment']
            if not self.universal_segment and self.device_type == 'mobile':
                self.cms_config.module_ribbon_tabs.create_tab(directive_name='BuildYourBet',
                                                              internal_id='tab-bet-builder', title='BUILD YOUR BET',
                                                              inclusionList=[self.segment], universalSegment=False)

            if not self.universal_segment and self.device_type == 'desktop' and self.brand == 'ladbrokes':
                self.cms_config.module_ribbon_tabs.create_tab(directive_name='BuildYourBet',
                                                              internal_id='tab-build-your-bet',
                                                              title='BUILD YOUR BET')
                sleep(15)  # Newly created BYB will take some time to reflect
        if not is_byb_configured_in_cms:
            self.cms_config.module_ribbon_tabs.create_tab(directive_name='BuildYourBet',
                                                              internal_id='tab-build-your-bet', title='BUILD YOUR BET')

    def test_001_mobileclick_on_build_your_bet_for_coral_bet_builder_for_ladbrokes_tab_on_homepage(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Click on **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) tab on Homepage
        EXPECTED: **Mobile:**
        EXPECTED: * **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) tab of Homepage is opened
        EXPECTED: * URL has the following structure:
        EXPECTED: https://xxx/home/buildyourbet **Coral**
        EXPECTED: https://xxx/home/betbuilder **Ladbrokes**
        EXPECTED: where
        EXPECTED: **xxx** - Coral or Ladbrokes domain
        """
        self.site.wait_content_state("Homepage")
        if not self.universal_segment and self.device_type == 'mobile':
            self.site.login()
            self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
            self.device.refresh_page()
            self.site.wait_content_state(state_name='Homepage', timeout=20)
        if self.device_type == 'mobile':
            self.site.home.module_selection_ribbon.tab_menu.click_button(vec.siteserve.EXPECTED_MARKET_TABS.build_your_bet)
            self.assertEqual(self.site.home.module_selection_ribbon.tab_menu.current,
                             vec.siteserve.EXPECTED_MARKET_TABS.build_your_bet,
                             msg='"Build Your Bet/Bet Builder" tab is not selected')
            expected_url = "/home/betbuilder" if self.brand == 'ladbrokes' else "/home/buildyourbet"
            actual_url = self.device.get_current_url()
            self.assertIn(expected_url, actual_url,
                          msg=f'Expected url: "{expected_url}" is not in actual url: "{actual_url}"')

    def test_002_mobile__click_on_any_event_of_build_your_bet_for_coral_bet_builder_for_ladbrokes_pagedesktop__scroll_the_homepage_down_to_build_your_bet_for_coral_bet_builder_for_ladbrokes_block__click_on_any_event_of_this_block(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: - Click on any Event of **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) page
        DESCRIPTION: **Desktop:**
        DESCRIPTION: - Scroll the Homepage down to **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) block
        DESCRIPTION: - Click on any Event of this block
        EXPECTED: **Mobile/Desktop:**
        EXPECTED: * Event Details page: **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) tab is opened by default
        EXPECTED: * URL has the following structure:
        EXPECTED: https://xxx/event/football/class/type/yyy/zzz/build-your-bet **Coral**
        EXPECTED: https://xxx/event/football/class/type/yyy/zzz/bet-builder **Ladbrokes**
        EXPECTED: where
        EXPECTED: **xxx** - Coral or Ladbrokes domain
        EXPECTED: **yyy** - Event name
        EXPECTED: **zzz** - Event id
        """
        event_name = None
        if self.device_type == 'mobile':
            sections = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            events = list(sections.values())[0].items_as_ordered_dict
            list(events.values())[0].click()
            event_name = (list(events.keys())[0]).lower().replace(' ', '-')

        if self.device_type == 'desktop' and self.brand == 'ladbrokes':
            build_your_bet = self.get_ribbon_tab_name(
                self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.build_your_bet)
            self.__class__.byb_module = self.site.home.get_module_content(module_name=build_your_bet)
            sections = self.byb_module.accordions_list.items_as_ordered_dict
            events = list(sections.values())[0].items_as_ordered_dict
            list(events.values())[0].click()
            event_name = (list(events.keys())[0]).lower().replace(' ', '-')

        if (self.device_name == 'mobile') or (self.device_type == 'desktop' and self.brand == 'ladbrokes'):
            self.site.wait_content_state(state_name='EventDetails')
            actual_url = self.device.get_current_url()
            expected_url_part1 = ("https://" + tests.HOSTNAME + "/event/")
            expected_url_part2 = f"/{event_name}/"
            expected_url_part3 = "/bet-builder" if self.brand == 'ladbrokes' else "/build-your-bet"
            self.assertIn(expected_url_part1, actual_url,
                          msg=f'Expected url: "{expected_url_part1}" is not in actual url: "{actual_url}"')
            self.assertIn(expected_url_part2, actual_url,
                          msg=f'Expected url: "{expected_url_part2}" is not in actual url: "{actual_url}"')
            self.assertIn(expected_url_part3, actual_url,
                          msg=f'Expected url: "{expected_url_part3}" is not in actual url: "{actual_url}"')

    def test_003_mobiledesktop__navigate_to_the_football_page_competitions_tab__select_class_and_type_which_include_event_with_available_byb__click_on_event_with_mapped_byb_markets(self):
        """
        DESCRIPTION: **Mobile/Desktop:**
        DESCRIPTION: - Navigate to the Football page: Competitions tab
        DESCRIPTION: - Select Class and Type which include Event with available BYB
        DESCRIPTION: - Click on Event with mapped BYB Markets
        EXPECTED: **Mobile/Desktop:**
        EXPECTED: * Event Details page: **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) tab is opened
        EXPECTED: * URL has the following structure:
        EXPECTED: https://xxx/event/football/ccc/ttt/yyy/zzz/build-your-bet **Coral**
        EXPECTED: https://xxx/event/football/ccc/ttt/yyy/zzz/bet-builder **Ladbrokes**
        EXPECTED: where
        EXPECTED: **xxx** - Coral or Ladbrokes domain
        EXPECTED: **ccc** - Class name
        EXPECTED: **ttt** - Type name
        EXPECTED: **yyy** - Event name
        EXPECTED: **zzz** - Event id
        """
        self.navigate_to_edp(event_id=self.event_id, timeout=50)
        self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        actual_url = self.device.get_current_url()
        expected_url_part1 = ("https://" + tests.HOSTNAME + "/event/football/")
        expected_url_part2 = '/bet-builder' if self.brand == 'ladbrokes' else '/build-your-bet'
        self.assertIn(expected_url_part1, actual_url,
                      msg=f'Expected url: "{expected_url_part1}" is not in actual url: "{actual_url}"')
        self.assertIn(expected_url_part2, actual_url,
                      msg=f'Expected url: "{expected_url_part2}" is not in actual url: "{actual_url}"')
