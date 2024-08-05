import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.navigation
@vtest
class Test_C1669288_Displaying_Super_Button_according_to_Page(Common):
    """
    TR_ID: C1669288
    NAME: Displaying Super Button according to Page
    DESCRIPTION: This test case verifies displaying Super Button according to Page
    DESCRIPTION: AUTOTEST: [C16396576]
    PRECONDITIONS: * Super Button should be added and enabled in CMS
    PRECONDITIONS: https://{domain}/sports-pages/homepage
    PRECONDITIONS: where domain may be
    PRECONDITIONS: coral-cms-dev1.symphony-solutions.eu - Local env
    PRECONDITIONS: coral-cms-dev0.symphony-solutions.eu - Develop
    PRECONDITIONS: cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/ - Beta
    """
    keep_browser_open = True

    def test_001_load_cms_and_log_in(self):
        """
        DESCRIPTION: Load CMS and log in
        EXPECTED: * CMS is loaded
        EXPECTED: * Content manager is logged in
        """
        pass

    def test_002_go_to_sports_pages___super_button___open_existing_super_button(self):
        """
        DESCRIPTION: Go to Sports Pages -> Super Button -> open existing Super Button
        EXPECTED: Super Button details page is opened
        """
        pass

    def test_003_select_one_of_the_available_tabs_from_show_on_home_tabs_drop_down_and_save_changeseg_featured_next_races_in_play_live_stream(self):
        """
        DESCRIPTION: Select one of the available Tabs from 'Show on Home Tabs' drop-down and save changes
        DESCRIPTION: e.g
        DESCRIPTION: * Featured
        DESCRIPTION: * Next Races
        DESCRIPTION: * in-Play
        DESCRIPTION: * Live Stream
        EXPECTED: * Super Button to particular Home Tab is selected
        EXPECTED: * Changes are saved successfully
        """
        pass

    def test_004_load_oxygen_app_and_verify_super_button_presence(self):
        """
        DESCRIPTION: Load Oxygen app and verify Super Button presence
        EXPECTED: * Super Button is present on the same Home Tab that was chosen on step#3
        EXPECTED: * Super Button is present below Module Ribbon Tabs and above of content of the tab
        EXPECTED: * Super Button is a yellow button
        """
        pass

    def test_005_go_back_to_the_same_super_button_unselect_tab_from_step3_in_show_on_home_tabs_drop_down_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same Super Button, unselect tab from step#3 in 'Show on Home Tabs' drop-down and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_006_load_oxygen_app_and_verify_super_button_presence(self):
        """
        DESCRIPTION: Load Oxygen app and verify Super Button presence
        EXPECTED: Super Button is NO more displayed on the chosen Home Tab
        """
        pass

    def test_007_repeat_steps_3_6_for_each_home_tab_from_the_list_above_step_3(self):
        """
        DESCRIPTION: Repeat steps 3-6 for each home tab from the list above (step 3)
        EXPECTED: Results are the same
        """
        pass

    def test_008_go_back_to_the_same_super_button_select_to_one_of_available_sport__race_in_show_on_sports_drop_down_and_save_changeseg_football_tennis_horse_racing_cricketnote_super_buttons_are_not_displayed_on_the_next_pages_lotto_yourcall_virtual_sports_international_tote(self):
        """
        DESCRIPTION: Go back to the same Super Button, select to one of available Sport / Race in 'Show on Sports' drop-down and save changes
        DESCRIPTION: e.g
        DESCRIPTION: * Football
        DESCRIPTION: * Tennis
        DESCRIPTION: * Horse Racing
        DESCRIPTION: * Cricket
        DESCRIPTION: **NOTE** Super Buttons are NOT displayed on the next pages
        DESCRIPTION: * Lotto
        DESCRIPTION: * Yourcall
        DESCRIPTION: * Virtual Sports
        DESCRIPTION: * International Tote
        EXPECTED: * Super Button for particular Sport/Race page is selected
        EXPECTED: * Changes are saved successfully
        """
        pass

    def test_009_load_oxygen_app_and_verify_super_button_presence_for_particular_sportrace(self):
        """
        DESCRIPTION: Load Oxygen app and verify Super Button presence for particular Sport/Race
        EXPECTED: * Super Button is present on the same Sport/Race page that was chosen on step#7
        EXPECTED: * Super Button is present between <Sport>/<Race> subtabs (e.g. In-Play) and page content
        """
        pass

    def test_010_go_back_to_the_same_super_button_unselect_sportrace_from_step7_in_show_on_sports_drop_down_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same Super Button, unselect Sport/Race from step#7 in 'Show on Sports' drop-down and save changes
        EXPECTED: * Super Button to particular Sport/Race is unselected
        EXPECTED: * Changes are saved successfully
        """
        pass

    def test_011_load_oxygen_app_and_verify_super_button_presence_for_particular_sportrace(self):
        """
        DESCRIPTION: Load Oxygen app and verify Super Button presence for particular Sport/Race
        EXPECTED: Super Button is NO more displayed on the chosen Sport/Race page
        """
        pass

    def test_012_repeat_steps_8_11_for_each_sportrace_from_the_list_above_step_8(self):
        """
        DESCRIPTION: Repeat steps 8-11 for each Sport/Race from the list above (step 8)
        EXPECTED: Results are the same
        """
        pass
