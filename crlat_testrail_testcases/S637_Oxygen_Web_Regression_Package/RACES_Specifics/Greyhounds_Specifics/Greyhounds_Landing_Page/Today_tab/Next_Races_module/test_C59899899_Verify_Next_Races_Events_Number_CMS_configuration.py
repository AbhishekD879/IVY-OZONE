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
class Test_C59899899_Verify_Next_Races_Events_Number_CMS_configuration(Common):
    """
    TR_ID: C59899899
    NAME: Verify 'Next Races' Events Number CMS configuration
    DESCRIPTION: This test case verifies Events number configuration in CMS within Next Races
    PRECONDITIONS: Below you may find a call from CMS with 'numberOfEvents' and Number of Selections values.
    PRECONDITIONS: Network->mobile-cms/desktop-cms ->systemConfiguration.GreyhoundNextRaces
    PRECONDITIONS: Request URL: https://cms-hl.ladbrokes.com/cms/api/ladbrokes/initial-data/mobile
    PRECONDITIONS: ![](index.php?/attachments/get/118935035)
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
        EXPECTED: GreyhoundNextRaces section is opened
        """
        pass

    def test_004_in__numberofevents_drop_down_choose_some_number_from_1_12__gt_press_submit(self):
        """
        DESCRIPTION: In '** numberOfEvents**' drop-down choose some number from 1-12 -&gt; Press 'Submit'
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_005_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: 
        """
        pass

    def test_006_tap_ltgreyhoundgt_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap &lt;Greyhound&gt; icon from the Sports Menu Ribbon
        EXPECTED: - &lt;Greyhound&gt; landing page is opened
        EXPECTED: - 'Next Races' module/carousel is displayed
        """
        pass

    def test_007_verify_next_races_events_number(self):
        """
        DESCRIPTION: Verify 'Next Races' Events number
        EXPECTED: - Appropriate events of selections (which was set in CMS) is displayed within Next Races module/carousel
        EXPECTED: - If number of events is less than was set in CMS -&gt; display the remaining selections
        EXPECTED: ![](index.php?/attachments/get/118935037)
        """
        pass

    def test_008_go_to_cms__gt_in_numberofevents_drop_down_choose_some_other_number_from_1_12__gt_press_submit(self):
        """
        DESCRIPTION: Go to CMS -&gt; In '**numberOfEvents**' drop-down choose some other number from 1-12 -&gt; Press 'Submit'
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_009_repeat_steps_5_7(self):
        """
        DESCRIPTION: Repeat steps #5-7
        EXPECTED: 
        """
        pass
