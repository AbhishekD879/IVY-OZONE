import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C2552995_Displaying_Super_Button_on_Big_Competition(Common):
    """
    TR_ID: C2552995
    NAME: Displaying Super Button on Big Competition
    DESCRIPTION: This test case verifies displaying Super Button according to Page
    PRECONDITIONS: * Super Button should be added and enabled in CMS
    PRECONDITIONS: https://{domain}/sports-pages/homepage
    PRECONDITIONS: where domain may be
    PRECONDITIONS: coral-cms-dev1.symphony-solutions.eu - Local env
    PRECONDITIONS: coral-cms-dev0.symphony-solutions.eu - Develop
    PRECONDITIONS: * Big Competition should be added, set up in CMS
    """
    keep_browser_open = True

    def test_001_load_cms_and_log_in(self):
        """
        DESCRIPTION: Load CMS and log in
        EXPECTED: * CMS is loaded
        EXPECTED: * Content manager is logged in
        """
        pass

    def test_002_go_to_super_button___open_existing_super_button(self):
        """
        DESCRIPTION: Go to Super Button -> open existing Super Button
        EXPECTED: Super Button details page is opened
        """
        pass

    def test_003_select_to_one_of_the_available_competitions_from_show_on_big_competitions_drop_down_and_save_changes(self):
        """
        DESCRIPTION: Select to one of the available competitions from 'Show on Big Competitions' drop-down and save changes
        EXPECTED: * Super Button for particular Competition is selected
        EXPECTED: * Changes are saved successfully
        """
        pass

    def test_004_load_oxygen_app_and_verify_super_button_presence_for_particular_competition(self):
        """
        DESCRIPTION: Load Oxygen app and verify Super Button presence for particular Competition
        EXPECTED: Super Button is present on the same Competition page that was chosen on step#3
        """
        pass

    def test_005_go_back_to_the_same_super_button_unselect_competition_from_step3_in_show_on_big_competition_drop_down_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same Super Button, unselect Competition from step#3 in 'Show on Big Competition' drop-down and save changes
        EXPECTED: * Super Button for particular Competition is unselected
        EXPECTED: * Changes are saved successfully
        """
        pass

    def test_006_load_oxygen_app_and_verify_super_button_presence_for_particular_competition(self):
        """
        DESCRIPTION: Load Oxygen app and verify Super Button presence for particular Competition
        EXPECTED: Super Button is NO more displayed on chosen Competition page
        """
        pass
