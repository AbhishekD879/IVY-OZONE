import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.module_ribbon
@pytest.mark.adhoc_suite
@vtest
# This test case covers C65946730
class Test_C65940560_MRT__Verify_the_In_play_tab_display_live_now_section_with_price_and_score_updates(Common):
    """
    TR_ID: C65940560
    NAME: MRT - Verify the In-play tab display, live now section with price and score updates
    DESCRIPTION: This test case is to verify the live now section with price and score updates
    """
    keep_browser_open = True

    inplay_config = {
    'internalId': "tab-in-play",
    'title': "In-Play",
    'visible': True,
    'showTabOn': "both",
    'url': "/home/in-play",
    'directiveName': "InPlay",
    'devices_android': True,
    'devices_ios': True,
    'devices_wp': True
    }

    inplay_sports_list_to_check = ['TABLE TENNIS', 'VOLLEYBALL']

    def test_000_precondition(self):
        """
        TR_ID: C65940560
        NAME: MRT - Verify the In-play tab display, live now section with price and score updates
        DESCRIPTION: This test case is to verify the live now section with price and score updates
        PRECONDITIONS: 1) User should have oxygen CMS access
        PRECONDITIONS: 2) Configuration for module ribbon tab in the cms
        PRECONDITIONS: -click on module ribbon tab option from left menu in Main navigation
        PRECONDITIONS: 3) Click on "+ Create Module ribbon tab" button to create new MRT.
        PRECONDITIONS: 4) Enter All mandatory Fields and click on save button:
        PRECONDITIONS: -Module ribbon tab title as "In-Play"
        PRECONDITIONS: - Select Directive name of In-Play option from dropdown
        PRECONDITIONS: -id as "tab-in-play"
        PRECONDITIONS: -URL  as "/home/in-play"
        PRECONDITIONS: -Click on "Create" CTA button
        PRECONDITIONS: 5)Check and select below required fields in module ribbon tab configuration:
        PRECONDITIONS: -Active
        PRECONDITIONS: -IOS
        PRECONDITIONS: -Android
        PRECONDITIONS: -Windows Phone
        PRECONDITIONS: -Select Show tab on option from dropdown like Both, Desktop ,Mobile/tablet
        PRECONDITIONS: -Select radiobutton either Universal or segment(s) inclusion.
        PRECONDITIONS: -Click on "Save changes" button
        """
        # Get all the data from CMS 'module ribbon tabs'
        all_module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        self.__class__.inplay_tab =next(
            mrt_tab for mrt_tab in all_module_ribbon_tabs if
            mrt_tab ['directiveName'] == 'InPlay' and
            mrt_tab ['internalId'] == 'tab-in-play'
        )
        if not self.inplay_tab:
            self.cms_config.create_tab(*self.inplay_config)
        else:
            if not self.inplay_tab.get('visible'):
                self.cms_config.module_ribbon_tabs.update_mrt_tab(tab_name=self.inplay_tab.get('title'),visible=True)

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home Page should be loaded successfully
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_verify_in_play_tab_present_in_mrt(self):
        """
        DESCRIPTION: verify In-Play tab present in MRT
        EXPECTED: In-Play tab should be present in MRT
        """
        #covered in step 3

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
        wait_for_haul(5)
        current_tab = self.site.home.tabs_menu.current
        self.assertEqual(current_tab, inplay_tab_name, msg=f"Current tab {current_tab} but"
                                                           f"Expected {inplay_tab_name} after clicking on "
                                                           f"{inplay_tab_name}")

    def test_004_verify_live_now_section_display_and_see_all_text_with_count_and_chevron(self):
        """
        DESCRIPTION: verify Live now section display and see all text with count and chevron
        EXPECTED: Live now section,see all text with count and chevron should be displayed
        """
        live_now_label = self.site.home.tab_content.live_now.live_now_header.text_label
        self.assertEqual(live_now_label.upper(), "LIVE NOW", msg='Live Now Label Not Found')

        has_see_all_label = self.site.home.tab_content.live_now.live_now_header.has_see_all_button()
        self.assertTrue(has_see_all_label, msg="See All Label Not Found")

        events_count_label = self.site.home.tab_content.live_now.live_now_header.events_count_label
        self.assertTrue(events_count_label, msg="Events Count Label Not Found")

    def test_005_verify_score_and_price_updates(self):
        """
        DESCRIPTION: Verify score and price updates
        EXPECTED: score and price should be updated
        """
        # Retrieve the live sports list
        get_live_sports_list = list(self.site.home.tab_content.live_now.items_as_ordered_dict.items())

        #iterate over the live sports list to check whether expected sport is available inside the live sports list

        # Iterate over the live sports list and check if any sport is in the inplay_sports_list_to_check
        are_required_sport_available = False
        for live_sport_name, live_sport in get_live_sports_list:
            # Check if the current live sport is in the list of sports to check
            if live_sport_name in self.inplay_sports_list_to_check:
                are_required_sport_available=True
                if not live_sport.is_expanded():
                    live_sport.expand()

                # Maximum wait time in seconds
                max_wait_time = 120
                # Interval to check for changes in seconds
                check_interval = 5

                # Retrieve the odds before the change
                odds_before_change = list(list(live_sport.items_as_ordered_dict.items())[0][1].items_as_ordered_dict.items())[0][1].template.first_player_bet_button.name

                # Retrieve the score board keys before the change
                sgp_before_change = list(list(live_sport.items_as_ordered_dict.items())[0][1].items_as_ordered_dict.items())[0][1].template.score_table.items_as_ordered_dict.keys()

                odds_after_change = \
                list(list(live_sport.items_as_ordered_dict.items())[0][1].items_as_ordered_dict.items())[0][
                    1].template.first_player_bet_button.name
                sgp_after_change = \
                list(list(live_sport.items_as_ordered_dict.items())[0][1].items_as_ordered_dict.items())[0][
                    1].template.score_table.items_as_ordered_dict.keys()

                elapsed_time = 0
                while elapsed_time < max_wait_time:
                    # Simulate waiting for a short duration (5 seconds)
                    wait_for_haul(check_interval)
                    elapsed_time += check_interval

                    # Simulate retrieving the odds and score board keys after the change
                    odds_after_change = list(list(live_sport.items_as_ordered_dict.items())[0][1].items_as_ordered_dict.items())[0][1].template.first_player_bet_button.name
                    sgp_after_change = list(list(live_sport.items_as_ordered_dict.items())[0][1].items_as_ordered_dict.items())[0][1].template.score_table.items_as_ordered_dict.keys()

                    # Check if odds have changed
                    if odds_before_change != odds_after_change:
                        self._logger.info("Odds changed!")
                        break

                    # Check if score board keys have changed
                    if sgp_before_change != sgp_after_change:
                        self._logger.info("Score board keys changed!")
                        break

                # Check if odds have changed
                self.assertNotEqual(odds_before_change, odds_after_change,
                                msg='Odds did not change after waiting for few times')

                # Check if the score board keys have changed
                self.assertNotEqual(sgp_before_change, sgp_after_change,
                                msg='Score board did not changed after waiting for some times ')
        if not are_required_sport_available:
            raise VoltronException(f"Required Sports {self.inplay_sports_list_to_check} not Live"
                                   f"Available Sports {get_live_sports_list}")