import random

import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.module_ribbon
@pytest.mark.build_your_bet
@pytest.mark.banach
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.timeout(1200)
@pytest.mark.slow
@pytest.mark.safari
@pytest.mark.adhoc_suite
@vtest
class Test_C896761_BYB_Build_Your_Bet_icons_and_module_ribbon_tab(BaseBanachTest):
    """
    TR_ID: C896761
    NAME: BYB - Build Your Bet icons and module ribbon tab
    DESCRIPTION: This test case verifies display of Build Your Bet icons, and 'Build Your Bet' **CORAL**/'Bet Builder' **LADBROKES** ribbon tab
    PRECONDITIONS: In order to have Banach leagues, cms setup should be made and Banach provider should return data (to be requested if none)
    PRECONDITIONS: CMS guide on Banach setup
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Banach
    PRECONDITIONS: HL requests:
    PRECONDITIONS: Request for Banach leagues:  https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v1/selections?obEventId=xxxxx&marketIds=[ids]
    PRECONDITIONS: CMS config for 'Build Your Bet' **CORAL**/'Bet Builder' **LADBROKES** ribbon tab on the Home page: CMS->Module Ribbon Tabs
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: - 'BET BUILDER' tab name for **LADBROKES**, 'BUILD YOUR BET' tab name for **CORAL**
    PRECONDITIONS: - Build Your bet Promo Icons should **NOT** be displayed on **LADBROKES**
    """
    keep_browser_open = True
    sport_name = vec.sb.FOOTBALL.upper()
    byb_on_homepage = True
    proxy = None

    def verify_build_your_bet_icon(self, sections=None, featured=False, build_your_bet=False):
        """
        Verifies whether Build Your Bet icons are present on League level but not on event card level
        :param build_your_bet: desktop module to verify True or False
        :param featured: desktop module to verify True or False
        :param sections: accordions / leagues
        """
        ui_byb_sections, ui_byb_events = [], []

        for section_name, section in sections.items():
            section_byb_name = section_name.split(' - ')[-1]

            if section_byb_name in list(self.banach_leagues_data.keys()):
                ui_byb_sections.append(section_name)

        if len(ui_byb_sections) != 0:
            random_section = random.choice(ui_byb_sections)
            section = sections.get(random_section, None)
            self.assertTrue(section, msg=f'"{random_section}" league not found')

            result = wait_for_result(lambda: section.group_sport_header.has_byb_icon(expected_result=False),
                                     name="Build Your Bet icon not to be shown", timeout=3)
            self.assertFalse(result, msg=f'"{random_section}" league should not have Build Your Bet icon')

            section.expand()

            if self.device_type == 'desktop' and featured:
                module_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
                module_content = self.site.home.get_module_content(module_name=module_name)

                sections = module_content.accordions_list.items_as_ordered_dict
                self.assertTrue(sections, msg='No sections found')

            elif self.device_type == 'desktop' and build_your_bet:
                module_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.build_your_bet)
                module_content = self.site.home.get_module_content(module_name=module_name)

                sections = module_content.accordions_list.items_as_ordered_dict
                self.assertTrue(sections, msg='No sections found')
            else:
                sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
                self.assertTrue(sections, msg=f'No sections found')

            section = sections.get(random_section, None)
            self.assertTrue(section, msg=f'"{random_section}" league not found')

            events_ui_names = section.items_as_ordered_dict
            self.assertTrue(events_ui_names, msg=f'No events found in "{section_name}"')

            events_byb = self.get_events_for_league(self.banach_leagues_data.get(random_section))
            events_byb_names = [item['title'].replace('|', '').replace('vs', 'v') for item in events_byb]

            for event_name, event in events_ui_names.items():
                if event_name in events_byb_names:
                    ui_byb_events.append(event_name)

            if len(ui_byb_events) != 0:
                random_event = random.choice(ui_byb_events)
                event = events_ui_names.get(random_event, None)
                self.assertTrue(event, msg=f'"{random_event}" event not found')
                self.assertTrue(event.has_byb_icon(), msg=f'"{event_name}" event does not have Build Your Bet icon')
            else:
                self._logger.warning(f'*** Skipping verification as there are no Banach events found')
        else:
            self._logger.warning(f'*** Skipping verification as there are no Banach leagues found')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event; add Featured tab module
        """
        if tests.settings.backend_env != 'prod':
            self.__class__.eventID = self.create_ob_event_for_mock()

            self.__class__.proxy = None
            self.__class__.module = self.cms_config.add_featured_tab_module(
                select_event_by='Event', id=self.eventID)
            self._logger.info(f'*** Created BYB event with ID "{self.eventID}"')

    def test_001_navigate_to_several_pages_and_verify_build_your_bet_icon_where_banach_provider_is_available(self):
        """
        DESCRIPTION: **CORAL ONLY**
        DESCRIPTION: - Navigate to Football Landing Page, Competitions page, Accumulators page
        DESCRIPTION: - Verify Build Your Bet icon where Banach provider is available
        EXPECTED: - Build Your Bet icon is not present on League level (on accordion)
        EXPECTED: - Build Your Bet icon is present on event card level only
        """
        self.__class__.banach_leagues_data = self.get_banach_leagues()

        if self.brand != 'ladbrokes':
            self.site.open_sport(name=self.sport_name)

            expected_tab = self.expected_sport_tabs.matches
            current_tab = self.site.football.tabs_menu.current
            self.assertEqual(current_tab, expected_tab,
                             msg=f'Current tab: "{current_tab}" '
                                 f'is not as expected: "{expected_tab}"')

            sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg=f'No sections found on "{expected_tab}" tab for "{self.sport_name}"')

            self.verify_build_your_bet_icon(sections=sections)

    def test_002_navigate_to_featured_page_and_verify_the_icon(self):
        """
        DESCRIPTION: **CORAL ONLY**
        DESCRIPTION: - Navigate to Featured page and verify the icon
        EXPECTED: - Build Your Bet icon is not present on League level (on accordion)
        EXPECTED: - Build Your Bet icon is present on event card level only
        """
        if self.brand != 'ladbrokes':
            self.site.go_to_home_page()

            featured = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
            featured_module = self.site.home.get_module_content(module_name=featured)

            sections = featured_module.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found on Home Page')

            self.verify_build_your_bet_icon(sections=sections, featured=True)

    def test_003_navigate_to_build_your_bet_or_bet_builder_module_ribbon_tab(self):
        """
        DESCRIPTION: Navigate to 'Build Your Bet' **CORAL** / 'Bet Builder' **LADBROKES** module ribbon tab (takes leagues from Banach provider only)
        EXPECTED: 'Build Your Bet' **CORAL** / 'Bet Builder' **LADBROKES** tab is opened
        """
        self.site.go_to_home_page()

        build_your_bet = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.build_your_bet)
        self.__class__.byb_module = self.site.home.get_module_content(module_name=build_your_bet)

    def test_004_verify_today_upcoming_tabs_presence(self):
        """
        DESCRIPTION: Verify 'Today', 'Upcoming' tabs presence
        EXPECTED: - If no leagues returned from Banach - message "Sorry, no Build Your Bet **CORAL** / Bet Builder **LADBROKES** events are available at this time" and no 'Today', 'Upcoming' tabs
        EXPECTED: - If request returns leagues for today and next 5 days - there 2 tabs ('Today' and 'Upcoming')
        EXPECTED: - If request returns leagues either for today or next 5 days - only one corresponding tab is displayed
        """
        if not self.byb_module.has_no_events_label():
            self.check_byb_leagues_presence()

    def test_005_verify_accordions_within_build_your_bet_or_bet_builder_tab(self):
        """
        DESCRIPTION: Verify accordions within 'Build Your Bet' **CORAL** / 'Bet Builder' **LADBROKES** tab
        EXPECTED: - Each accordion within the tab corresponds to the Banach league
        EXPECTED: - The order of leagues which appear in BYB is defined by the order defined in CMS -> BYB -> Banach Leagues
        EXPECTED: - BYB icon is not present
        """
        grouping_buttons_section = self.byb_module.grouping_buttons
        grouping_buttons = grouping_buttons_section.items_as_ordered_dict
        self.assertTrue(grouping_buttons, msg='No switchers found')

        upcoming_tab = vec.yourcall.UPCOMING
        today_tab = vec.yourcall.TODAY

        self.assertTrue(any((grouping_buttons.get(upcoming_tab), grouping_buttons.get(today_tab))),
                        msg=f'Both "{today_tab}" and "{upcoming_tab}" tabs not present in {list(grouping_buttons.keys())}')

        for tab_name, tab in grouping_buttons.items():
            grouping_buttons_section.click_button(tab_name)

            sections = self.byb_module.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found on Home Page')

            self.verify_build_your_bet_icon(sections=sections, build_your_bet=True)
        self.__class__.sections = sections

    def test_006_open_event_from_build_your_bet_or_bet_builder_tab(self):
        """
        DESCRIPTION: Open event from 'Build Your Bet' **CORAL** / 'Bet Builder' **LADBROKES** tab
        EXPECTED: EDP is opened on 'Build Your Bet' **CORAL** / 'Bet Builder' **LADBROKES** tab
        """
        random_section = random.choice(list(self.sections.keys()))
        section = self.sections.get(random_section, None)
        self.assertTrue(section, msg=f'"{random_section}" league not found')

        section.expand()

        section_byb_name = random_section.split(' - ')[-1]
        events_byb = self.get_events_for_league(self.banach_leagues_data.get(section_byb_name))
        active_byb_events = [event['title'].replace('|', '') for event in events_byb if self.check_event_is_active(event_id=event['obEventId'])]

        if len(active_byb_events) != 0:
            events = section.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events found for "{random_section}"')

            random_event = random.choice(active_byb_events)
            event = events.get(random_event, None)
            self.assertTrue(event, msg=f'"{random_event}" event not found')

            event.click()
            self.site.wait_content_state(state_name='EventDetails')

            # replace is spike for tst env
            current_tab = self.site.sport_event_details.markets_tabs_list.current.replace('NEW\n', '')
            expected_tab = vec.siteserve.EXPECTED_MARKET_TABS.build_your_bet
            self.assertEqual(current_tab, expected_tab,
                             msg=f'Current tab: "{current_tab}" is not as expected: "{expected_tab}"')
        else:
            self._logger.warning(f'*** Skipping verification as there are no Banach events found')
