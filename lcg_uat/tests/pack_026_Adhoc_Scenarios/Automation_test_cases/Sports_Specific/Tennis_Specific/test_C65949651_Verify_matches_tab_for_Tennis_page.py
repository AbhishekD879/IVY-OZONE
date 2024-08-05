import pytest
from datetime import datetime
from tests.base_test import vtest
from tzlocal import get_localzone
from tests.Common import Common
import voltron.environments.constants as vec
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports_specific
@pytest.mark.tennis_specific
@pytest.mark.other
@pytest.mark.adhoc_suite
@vtest
class Test_C65949651_Verify_matches_tab_for_Tennis_page(BaseSportTest,Common):
    """
    TR_ID: C65949651
    NAME: Verify matches tab for Tennis page.
    DESCRIPTION: This testcase verifies matches tab for Tennis page.
    PRECONDITIONS: 1. User must be loggedin/logout.
    PRECONDITIONS: 2. Matches tab can be configured from CMS->
    PRECONDITIONS: sports menu->sportscategory->Tennis->matches tab->enable/disable.
    PRECONDITIONS: 3. Verify modules which are available in matches tab. Modules are cofigured from CMS.
    PRECONDITIONS: 4. Types of modules are: quicklinks, surface bets, highlight courosule, superbuttons.
    PRECONDITIONS: Signposting will be displayed on event cards.
    """
    keep_browser_open = True
    timezone = str(get_localzone())

    def valid_modules(self,modules):
        if self.timezone.upper() == "UTC":
            now = get_date_time_as_string(date_time_obj=datetime.now(),
                                          time_format='%Y-%m-%dT%H:%M:%S.%f',
                                          url_encode=False)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            now = get_date_time_as_string(date_time_obj=datetime.now(),
                                          time_format='%Y-%m-%dT%H:%M:%S.%f',
                                          url_encode=False, hours=-1)[:-3] + 'Z'
        else:
            now = get_date_time_as_string(date_time_obj=datetime.now(),
                                          time_format='%Y-%m-%dT%H:%M:%S.%f',
                                          url_encode=False, hours=-5.5)[:-3] + 'Z'
        valid_module = []
        if modules:
            for module in modules:
                  if (now <= module['displayTo']) and module['disabled'] is False:
                   valid_module.append(module['title'].upper().strip())
        else:
            return valid_module

    def verify_the_module_cms(self, mod_type):
        sport_id = self.ob_config.tennis_config.category_id
        self.__class__.enabled_quick_links = []
        self.__class__.enabled_hc = []
        self.__class__.enabled_sb = []
        self.__class__.enabled_super_button = []

        if mod_type == 'QUICK_LINKS':
            modules = self.cms_config.get_quick_links(sport_id=sport_id)
            self.enabled_quick_links = self.valid_modules(modules)

        if mod_type == 'HIGHLIGHTS_CAROUSEL':
            modules = self.cms_config.get_all_highlights_carousels(page_id=sport_id)
            self.enabled_hc = self.valid_modules(modules)

        if mod_type == 'SURFACE_BET':
            modules = self.cms_config.get_surface_bets_for_page(reference_id=sport_id)
            self.enabled_sb = self.valid_modules(modules)

        if mod_type == 'SUPER_BUTTON':
            modules = self.cms_config.get_mobile_super_buttons()
            self.enabled_super_button = self.valid_modules(modules)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. User must be loggedin/logout.
        PRECONDITIONS: 2. Matches tab can be configured from CMS->
        PRECONDITIONS: sports menu->sportscategory->Tennis->matches tab->enable/disable.
        PRECONDITIONS: 3. Verify modules which are available in matches tab. Modules are cofigured from CMS.
        PRECONDITIONS: 4. Types of modules are: quicklinks, surface bets, highlight courosule, superbuttons.
        PRECONDITIONS: Signposting will be displayed on event cards.
        """
        sport_id = self.ob_config.tennis_config.category_id
        tab_status = self.cms_config.get_sport_tab_status(sport_id=sport_id,
                                                      tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)
        if not tab_status:
            raise SiteServeException(f'{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches}" tab is not enabled in cms')

        modules = self.cms_config.get_sport_module(sport_id=sport_id, module_type=None)
        for module in modules:
            if not module['disabled']:
                mod_type = module['moduleType']
                self.verify_the_module_cms(mod_type)

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application.
        EXPECTED: User should be able to launch the application successfully.
        """
        self.site.wait_content_state('Homepage')

    def test_002_click_on_tennis_sport(self):
        """
        DESCRIPTION: Click on tennis sport.
        EXPECTED: User should be able to navigate tennis landing page.
        """
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.click_item(vec.siteserve.TENNIS_TAB)
        else:
            sport = self.site.header.sport_menu.items_as_ordered_dict[vec.siteserve.TENNIS_TAB.upper()]
            sport.click()
        self.site.wait_content_state(state_name='Tennis')

    def test_003_verify_tennis_landing_page(self):
        """
        DESCRIPTION: Verify tennis landing page.
        EXPECTED: User should be able to see tennis landing page.
        """
        # covered in step 002

    def test_004_desktop_verify_today_tomorrow_and_futuretab(self):
        """
        DESCRIPTION: Desktop: Verify today, tomorrow and future
        DESCRIPTION: tab.
        EXPECTED: User should be able to see today, tomorrow and future tab.
        """
        # Check if Matches Tab Is Selected By Default
        current_tab = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab.upper(), "Matches".upper(), msg=f"Current Active tab is {current_tab}, "
                                                                     f"Expected tab is Matches")
        if self.device_type != 'mobile':
            # verify today
            date_tabs = self.site.tennis.date_tab.items_as_ordered_dict
            for name,tab in date_tabs.items():
                self.assertTrue(tab.is_displayed(), msg=f'{name} is not displayed in tennis landing page')

    def test_005_verify_default_tab(self):
        """
        DESCRIPTION: Verify default tab.
        EXPECTED: User should be able to see today tab is selected by default
        EXPECTED: after launching the tennis page.
        """
        if self.device_type != 'mobile':
            current_date_tab = self.site.tennis.date_tab.current_date_tab
            self.assertEqual(current_date_tab, vec.sb.SPORT_DAY_TABS.today,
                             msg=f'"{vec.sb.SPORT_DAY_TABS.today}" is not active'
                                 f' date tab, active is "{current_date_tab}"')

    def test_006_(self):
        """
        DESCRIPTION: 
        EXPECTED: Mobile: After launching tennis page in matches tab today
        EXPECTED: and tomorrows events will be displayed.
        """
       # covered in step 11

    def test_007_verify_matches_tab(self):
        """
        DESCRIPTION: Verify matches tab.
        EXPECTED: User should be able to see matches tab.
        """
        # Covered in step 004

    def test_008_verify_modules_mentioned_in_preconditions(self):
        """
        DESCRIPTION: Verify modules mentioned in preconditions
        EXPECTED: Mobile: Quiclinks, Surfacebets, Highlights corousels, super buttons
        EXPECTED: should be displayed as per CMS config
        EXPECTED: Desktop: Surfacebets, Highlights corousels should be displayed
        """
        # Verify Highlight carousel
        if self.enabled_hc:
            hc_fe = self.site.home.desktop_modules.items_as_ordered_dict.get('FEATURED').tab_content.highlight_carousels
            self.assertTrue(hc_fe, msg=f'{self.enabled_hc} Highlight carousels are not displayed in tennis page')

        # Verify Surface Bet
        if self.enabled_sb:
            surface_bets = self.site.home.get_module_content(vec.SB.HOME_FEATURED_NAME).surface_bets
            self.assertTrue(surface_bets, msg=f'{self.enabled_sb} surface bets are not displayed in tennis page')

        if self.device_type == 'mobile':
            # Verify quick links
            if self.enabled_quick_links:
                quick_links = self.site.home.get_module_content(vec.SB.HOME_FEATURED_NAME).quick_links
                self.assertTrue(quick_links, msg=f'{self.enabled_quick_links} quick links are not displayed in tennis page')

            # Verify super button
            if self.enabled_super_button:
                super_button = self.site.tennis.super_button_section.super_button.button
                self.assertTrue(super_button, msg=f'{super_button} super button ')

    def test_009_verify_accordians_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordians are collapsable and expandable
        EXPECTED: accordians should be collapsable and expandable
        """
        # This step is covered in step 011


    def test_010_for_mobileverify_see_all_link_navigation_whichpresents_besides_type_name(self):
        """
        DESCRIPTION: For Mobile:
        DESCRIPTION: Verify SEE ALL Link navigation which
        DESCRIPTION: presents besides type name
        EXPECTED: On clicking SEE ALL link should navigate to
        EXPECTED: respective competitions details page
        """
        if self.device_type == 'mobile':
            leagues = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
            event = [item for name, item in leagues.items()][0]
            event.group_header.see_all_link.click()
            self.site.wait_content_state('CompetitionLeaguePage')
            self.site.back_button_click()
            self.site.wait_content_state(state_name='tennis')

    def test_011_verify_event_card_body(self):
        """
        DESCRIPTION: Verify Event Card body
        EXPECTED: Event Card body should show with
        EXPECTED: * fixture headers (home,draw,away)
        EXPECTED: * event1 v event 2
        EXPECTED: * Odd buttons
        EXPECTED: * Date and Time in upcoming section
        EXPECTED: * More markets link
        """
        leagues = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        league_name = list(leagues.keys())[0]
        header = leagues.get(league_name).fixture_header
        self.assertTrue(header.is_displayed(), msg= f'league fixture is not displayed')

        length = len(list(leagues.keys()))
        number_of_leagues = 2 if length > 3 else length
        for league in list(leagues.values())[:number_of_leagues]:
            if league.is_expanded():
                league.collapse()
                wait_for_haul(1)
                league.expand()
            else:
                league.expand()
            events = league.items_as_ordered_dict
            for event in list(events.values())[:1]:

                # Displayed event name
                event_name = event.template.event_name_we
                self.assertTrue(event_name.is_displayed(), msg=f'{event_name} Event name not displayed')

                # Displayed odds buttons
                odds = event.template.items_as_ordered_dict
                self.assertTrue(odds, msg=f'odds buttons is not displayed')

                # Displayed time and Day
                time_day = event.template.event_time
                self.assertTrue(time_day, msg=f'{time_day} time day is not displayed')

                # Displayed more link
                more_link = event.template.more_markets_link
                self.assertTrue(more_link.is_displayed(), msg='More market link is not displayed')

        # Displayed more link and event details page
        more_link.click()
        self.site.wait_content_state(state_name='EVENTDETAILS')

    def test_012_verify_more_links(self):
        """
        DESCRIPTION: Verify more links.
        EXPECTED: User should be able to see more link below the odds at rightside corner.
        """
        # Covered in step 011

    def test_013_click_on_more_link(self):
        """
        DESCRIPTION: Click on more link.
        EXPECTED: User should be able to navigate event details page.
        """
        # Covered in step 011