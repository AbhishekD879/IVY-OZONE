import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C59899927_Verify_Next_Races_Runners_Number_CMS_configuration(Common):
    """
    TR_ID: C59899927
    NAME: Verify 'Next Races' Runners Number CMS configuration
    DESCRIPTION: This test case verifies Selections/runners number configuration in CMS within Next Races tab.
    PRECONDITIONS: 1. "Next Races" tab should be enabled in CMS (CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle-> nextRacesTabEnabled)
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Race events are available for the current day
    PRECONDITIONS: Below you may find a call from CMS with 'numberOfEvents' and Number of Selections values.
    PRECONDITIONS: Network->mobile-cms/desktop-cms ->systemConfiguration.GreyhoundNextRaces
    PRECONDITIONS: Request URL: https://cms-hl.ladbrokes.com/cms/api/ladbrokes/initial-data/mobile
    PRECONDITIONS: ![](index.php?/attachments/get/118934774)
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_tap_system_configuration_section(self):
        """
        DESCRIPTION: Tap 'System-configuration' section
        EXPECTED: 'System-configuration' section is opened
        """
        pass

    def test_003_go_to_greyhoundnextraces_section(self):
        """
        DESCRIPTION: Go to 'GreyhoundNextRaces' section
        EXPECTED: GreyhoundNextRaces section expanded
        """
        pass

    def test_004_in_numberofevents_for_greyhoundenter_some_number___press_submit(self):
        """
        DESCRIPTION: In '**numberOfEvents**' (for Greyhound)enter some number -> Press 'Submit'
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_005_in_number_of_selections_for_greyhoundenter_some_number___press_submit8_option_should_be_set_by_default(self):
        """
        DESCRIPTION: In '**Number of Selections**' (for Greyhound)enter some number -> Press 'Submit'
        DESCRIPTION: ('8' option should be set by default)
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_006_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: 
        """
        pass

    def test_007_tap_greyhound_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Greyhound> icon from the Sports Menu Ribbon
        EXPECTED: - <Greyhound> landing page is opened
        EXPECTED: - 'Next Races' tab is available
        """
        pass

    def test_008_open_next_races_tabverify__selectionsrunners_number(self):
        """
        DESCRIPTION: Open 'Next Races' tab.
        DESCRIPTION: Verify  Selections/runners number
        EXPECTED: -Appropriate number of selections (which was set in CMS) is displayed within Next Races module/carousel
        EXPECTED: - If number of selections is less than was set in CMS -> display the remaining selections
        EXPECTED: - 'Unnamed Favourite' runner shouldn't be shown on the 'Next Races' module
        EXPECTED: ![](index.php?/attachments/get/118934773)
        """
        pass

    def test_009_go_to_cms___in_number_of_selections_enter_some_other_number___press_submit1_option_should_be_set_by_default(self):
        """
        DESCRIPTION: Go to CMS -> In '**Number of Selections**' enter some other number -> Press 'Submit'
        DESCRIPTION: ('1' option should be set by default)
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_010_repeat_steps_5_7(self):
        """
        DESCRIPTION: Repeat steps #5-7
        EXPECTED: 
        """
        pass
