import pytest
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_inplay_structure, get_inplay_sport_by_category
from voltron.utils.waiters import wait_for_result, wait_for_cms_reflection


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.cms
@pytest.mark.adhoc_suite
@pytest.mark.mobile_only
@pytest.mark.module_ribbon
@pytest.mark.timeout(1500)
@vtest
class Test_C65940561_MRT__verify_the_In_play_tablive_now_section_expanded_events_count_as_per_CMS_and_show_all_text_with_category_name(
    Common):
    """
    TR_ID: C65940561
    NAME: MRT - verify the In-play tab,live now section expanded events count as per CMS and show all text with category name
    DESCRIPTION: This test case is to verify the live now section expanded events count as per CMS and show all text with category name and count
    """
    enable_bs_performance_log = True
    # This flag keeps the browser open after the tests finish
    keep_browser_open = True

    # Configuration for the In-Play tab
    inplay_config = {
        'title': 'In-Play',
        'directive_name': 'InPlay',
        'visible': True,
        'internal_id': 'tab-in-play',
        'devices_android': True,
        'devices_ios': True,
        'devices_wp': True,
        'url': '/home/in-play',
        'show_tabs_on': 'both',
    }

    # Flag to track if we've reached step 9 condition
    reached_step_9_condition = False

    # A set to keep track of checked sport categories
    checked_sport = set()

    # Helper method to get in-play data by category
    def get_inplay_data_by_category(self, category_id, max_attempts=3):
        data = wait_for_result(lambda: get_inplay_sport_by_category(category_id=category_id), timeout=10)
        if not data and max_attempts > 0:
            return self.get_inplay_data(max_attempts=max_attempts - 1)
        else:
            return list(set(item['typeName'] for item in data.get('eventsByTypeName')))

    # Helper method to get in-play data
    def get_inplay_data(self, max_attempts=3, return_all=False, sport_name=None, max_event=False):
        sleep(2)
        data = wait_for_result(lambda: get_inplay_structure(), timeout=10).get("livenow", {}).get('eventsBySports', {})

        if not data and max_attempts > 0:
            return self.get_inplay_data(max_attempts=max_attempts - 1, return_all=return_all, sport_name=sport_name,
                                        max_event=max_event)
        elif sport_name:
            # Filter data for the specified sport name and directly return it
            normalized_sport_name = sport_name.strip().lower()
            filtered_data = [sport for sport in data if
                             sport.get('categoryName', '').strip().lower() == normalized_sport_name]
            if not filtered_data:
                raise ValueError(f"No data found for sport: {sport_name}")
            return filtered_data[0]
        else:
            if return_all:
                # Return all sport
                return data
            elif max_event:
                # Return the maximum event count
                max_event = max(data, key=lambda sport: sport.get('eventCount', 0))
                return max_event
            else:
                return data

    # Helper method to expand a sport category and check if the "Show More" button is available
    def expand_sport_and_check_show_more(self, sport_name=None, category_id=None):
        sport_item = self.site.home.tab_content.live_now.items_as_ordered_dict.get(sport_name.upper())
        if sport_item:
            sport_item.expand()
            sport_data = self.get_inplay_data_by_category(category_id=category_id)
            type_count = len(sport_data) if sport_data else 0
            if type_count > 0:
                return sport_item.has_show_more_leagues_button()
        return "SPORT NOT LIVE"

    # Test step for preconditions
    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User should have oxygen CMS access
        PRECONDITIONS: 2) Configuration for module ribbon tab in the cms
        PRECONDITIONS: 2a)  -click on module ribbon tab option from left menu in Main navigation
        PRECONDITIONS: 2b) Click on "+ Create Module ribbon tab" button to create new MRT.
        PRECONDITIONS: 2c) Enter All mandatory Fields and click on save button:
        PRECONDITIONS: -Module ribbon tab title as "In-Play"
        PRECONDITIONS: - Select Directive name of In-Play option from dropdown
        PRECONDITIONS: -id as "tab-in-play"
        PRECONDITIONS: -URL  as "/home/in-play"
        PRECONDITIONS: -Click on "Create" CTA button
        PRECONDITIONS: 2d)Check and select below required fields in module ribbon tab configuration:
        PRECONDITIONS: -Active
        PRECONDITIONS: -IOS
        PRECONDITIONS: -Android
        PRECONDITIONS: -Windows Phone
        PRECONDITIONS: -Select Show tab on option from dropdown like Both, Desktop ,Mobile/tablet
        PRECONDITIONS: -Select radiobutton either Universal or segment(s)           inclusion.
        PRECONDITIONS: -Click on "Save changes" button
        PRECONDITIONS: 3) configuration for event expanded count
        PRECONDITIONS: 3a) System configuration > structure >search in "serach for configuraion" box as "InPlayCompetitionsExpanded"
        PRECONDITIONS: 3b) Enter field value for competitioncount field.
        """
        all_mrt_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        self.__class__.inplay_tab = next(
            (mrt_tab for mrt_tab in all_mrt_tabs if
             mrt_tab['directiveName'].strip().upper() == 'InPlay'.upper() and
             mrt_tab['internalId'].strip().upper() == 'tab-in-play'.upper()), None)
        if not self.inplay_tab:
            self.cms_config.module_ribbon_tabs.create_tab(**self.inplay_config)
        else:
            if not self.inplay_tab.get('visible'):
                self.cms_config.module_ribbon_tabs.update_mrt_tab(tab_name=self.inplay_tab.get('title'), visible=True)
        self.cms_config.update_system_configuration_structure(config_item='InPlayCompetitionsExpanded',
                                                              field_name='competitionsCount',
                                                              field_value=int(3))

    # Test step to launch the application
    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home Page should be loaded successfully
        """
        self.site.wait_content_state(state_name="Homepage")

    # Test step to verify if the In-Play tab is present in MRT
    def test_002_verify_in_play_tab_present_in_mrt(self):
        """
        DESCRIPTION: verify In-Play tab present in MRT
        EXPECTED: In-Play tab should be present in MRT
        """
        # covered in step 3

    # Test step to click on the In-Play tab
    def test_003_click_on_in_play_tab(self):
        """
        DESCRIPTION: Click on In-play tab
        EXPECTED: user should be able to see In-play tab
        """
        inplay_tab_name = self.inplay_tab.get('title').upper()
        inplay_tab_fe = wait_for_result(lambda: self.site.home.tabs_menu.items_as_ordered_dict.get(inplay_tab_name),
                                        timeout=50, bypass_exceptions=VoltronException)
        self.assertTrue(inplay_tab_fe, msg=f"Inplay tab is not present in MRT {self.site.home.tabs_menu.items_names}")
        inplay_tab_fe.click()
        current_tab = wait_for_result(lambda: self.site.home.tabs_menu.current, bypass_exceptions=VoltronException)
        self.assertEqual(current_tab, inplay_tab_name, msg=f"Current tab {current_tab} but"
                                                           f"Expected {inplay_tab_name} after clicking on "
                                                           f"{inplay_tab_name}")

    # Test step to verify Live Now section display and "See All" text with count and chevron
    def test_004_verify_live_now_section_display_and_see_all_text_with_count_and_chevron(self):
        """
        DESCRIPTION: Verify Live now section display and "See all" text with count and chevron
        EXPECTED: Live now section,see all text with count and chevron should be displayed
        """
        live_now_label = self.site.home.tab_content.live_now.live_now_header.text_label
        self.assertEqual(live_now_label.upper(), "LIVE NOW", msg='Live Now Label Not Found')

        has_see_all_label = self.site.home.tab_content.live_now.live_now_header.has_see_all_button()
        self.assertTrue(has_see_all_label, msg="See All Label Not Found")

        events_count_label = self.site.home.tab_content.live_now.live_now_header.events_count_label
        self.assertTrue(events_count_label, msg="Events Count Label Not Found")

    # Test step to verify that the first sport category is expanded by default and the rest are in the collapse state
    def test_005_verify_first_sport_category_is_expanded_by_default_and_rest_all_in_collapse_state(self):
        """
        DESCRIPTION: Verify first sport category is expanded by default and rest all in collapse state
        EXPECTED: First sport category should be expanded by default and rest all should be in collapse state
        """
        live_now_accordions = list(self.site.home.tab_content.live_now.items_as_ordered_dict.items())
        first_accordion_name, first_accordion = live_now_accordions[0]
        self.assertTrue(wait_for_result(lambda: first_accordion.is_expanded(), timeout=3),
                        msg=f"First sport category {first_accordion_name} is not expanded by default")
        for accordion_name, accordion in live_now_accordions[1:]:
            self.assertFalse(wait_for_result(lambda: accordion.is_expanded(), expected_result=False, timeout=3),
                             msg=f"sport category {accordion_name} is  expanded by default")

    # Test step to verify In-play expanded competition count as per CMS config
    def test_006_verify_inplay_expanded_competition_count_as_per_cms_config(self, sport=None, sport_name=None):
        """
        DESCRIPTION: Verify Inplay expanded competition count as per CMS config
        EXPECTED: in-play expanded count should be displayed as per cms Config
        """
        if self.reached_step_9_condition and sport_name:

            is_league_less_than_equal_to_cms_inplay_count = wait_for_result(
                lambda: sport.count_of_items <= int(
                    self.cms_config.get_system_configuration_structure() \
                        .get('InPlayCompetitionsExpanded') \
                        .get('competitionsCount')))
            competitions_count = self.cms_config.get_system_configuration_structure() \
                .get('InPlayCompetitionsExpanded') \
                .get('competitionsCount')

            leauge_count = sport.count_of_items

            self.assertTrue(is_league_less_than_equal_to_cms_inplay_count,
                            msg=f"Leauge count for sport {sport_name} is {leauge_count} "
                                f"even though Inplay Competition Count is {competitions_count}")

    # Test step to verify the display of "show all" text with sport category name when in-play competition count in the
    # sport is less than configured competition count in CMS
    def test_007_verify_display_show_all_text_with_sport_category_name_when_inplay_competition_count_in_sport_is_less_than_configured_competition_count_in_cms(
            self, sport=None, sport_name=None, sport_category=None):
        """
        DESCRIPTION: Verify display "show all" text with sport category name when inplay competition count in sport is less than configured competition count in CMS
        EXPECTED: "show all" text with sport category name should not be displayed
        """
        # "IN_PLAY_SPORTS::34::LIVE_EVENT"
        if self.reached_step_9_condition and sport_name and sport_category:
            type_count = len(self.get_inplay_data_by_category(sport_category))
            self.cms_config.update_system_configuration_structure(config_item='InPlayCompetitionsExpanded',
                                                                  field_name='competitionsCount',
                                                                  field_value=int(type_count))

            competitions_count = wait_for_result(lambda: self.cms_config.get_system_configuration_structure() \
                                                 .get('InPlayCompetitionsExpanded') \
                                                 .get('competitionsCount') == type_count,
                                                 expected_result=True, timeout=60)
            self.assertTrue(competitions_count, msg=f"Competitions count is not updated to {type_count}")

            competitions_count = self.cms_config.get_system_configuration_structure() \
                .get('InPlayCompetitionsExpanded') \
                .get('competitionsCount')

            is_show_more_available = wait_for_cms_reflection(
                lambda: self.expand_sport_and_check_show_more(sport_name=sport_name,
                                                              category_id=sport_category),
                ref=self,
                refresh_count=5,
                timeout=3,
                expected_result=False)

            if is_show_more_available == "SPORT NOT LIVE":
                return
            self.assertFalse(is_show_more_available,
                             msg=f"Show more is still displayed for {sport_name} Even though league count is{type_count}"
                                 f" cms competitionsCount is {competitions_count}")

    # Test step to verify the display of "show all" text with sport category name when in-play competition count in the
    # sport is more than configured competition count in CMS
    def test_008_verify_display_show_all_text_with_sport_category_name_when_inplay_competition_count_in_sport_is_more_than_configured_competition_count_in_cms(
            self, sport_name=None, sport_category=None):
        """
        DESCRIPTION: Verify display "show all" text with sport category name when inplay competition count in sport is more than configured competition count in CMS
        EXPECTED: "show all" text with sport category name should be displayed
        """
        if self.reached_step_9_condition and sport_name and sport_category:
            type_count = len(self.get_inplay_data_by_category(sport_category))
            self.cms_config.update_system_configuration_structure(config_item='InPlayCompetitionsExpanded',
                                                                  field_name='competitionsCount',
                                                                  field_value=1)

            competitions_count = wait_for_result(lambda: self.cms_config.get_system_configuration_structure() \
                                                 .get('InPlayCompetitionsExpanded') \
                                                 .get('competitionsCount') == 1, timeout=60,
                                                 expected_result=True)

            self.assertTrue(competitions_count, msg=f"Competitions count is not updated to {type_count}")

            competitions_count = self.cms_config.get_system_configuration_structure() \
                .get('InPlayCompetitionsExpanded') \
                .get('competitionsCount')

            is_show_more_available = wait_for_cms_reflection(
                lambda: self.expand_sport_and_check_show_more(sport_name=sport_name, category_id=sport_category),
                ref=self,
                refresh_count=5,
                timeout=3,
                expected_result=True)

            if is_show_more_available == "SPORT NOT LIVE" or type_count == 1:
                return
            self.assertTrue(is_show_more_available,
                            msg=f"Show more is not displayed for {sport_name} Even though league count is {type_count}"
                                f" cms competitionsCount is {competitions_count}")

    # Test step to click on the next sport category
    def test_009_click_on_next_sport_category(self):
        """
        DESCRIPTION: Click on next sport category
        EXPECTED: Sport should be expanded
        """
        # Covered in step 10

    # Test step to repeat above steps from 6 to 8 for all in-play sports categories
    def test_010_repeat_above_steps_from_6_to_8_for_all_inplay_sports_category(self):
        """
        DESCRIPTION: Repeat above steps from 6 to 8 for all inplay sports category
        EXPECTED:
        """
        sport_list = self.get_inplay_data(return_all=True)
        self.__class__.reached_step_9_condition = True
        for inplay_sport in sport_list:
            if len(self.checked_sport) >= 3:
                break

            inplay_sport_name = inplay_sport.get('categoryName').upper()
            inplay_sport_category = inplay_sport.get('categoryId')

            if inplay_sport_name in self.checked_sport:
                continue
            sport = self.site.home.tab_content.live_now.items_as_ordered_dict.get(inplay_sport_name)
            if not sport:
                continue

            if not sport.is_expanded():
                sport.expand()

            self.test_006_verify_inplay_expanded_competition_count_as_per_cms_config(sport=sport, sport_name=inplay_sport_name)

            self.test_007_verify_display_show_all_text_with_sport_category_name_when_inplay_competition_count_in_sport_is_less_than_configured_competition_count_in_cms(
                sport=sport, sport_name=inplay_sport_name, sport_category=inplay_sport_category)

            self.test_008_verify_display_show_all_text_with_sport_category_name_when_inplay_competition_count_in_sport_is_more_than_configured_competition_count_in_cms(
                sport_name=inplay_sport_name, sport_category=inplay_sport_category)

            if sport.is_expanded():
                sport.collapse()
            self.checked_sport.add(inplay_sport_name)

    # Test step for bet placement for single, multiple, and complex bets
    def test_011_bet_placement_for_singlemultiple_and_complex_bet(self):
        """
        DESCRIPTION: bet placement for single, multiple and complex bet
        EXPECTED: Bet should be placed successfully
        """
        # Covered in C65904562
