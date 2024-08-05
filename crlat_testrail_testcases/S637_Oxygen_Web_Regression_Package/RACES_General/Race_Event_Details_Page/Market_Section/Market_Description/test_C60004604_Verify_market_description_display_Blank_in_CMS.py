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
class Test_C60004604_Verify_market_description_display_Blank_in_CMS(Common):
    """
    TR_ID: C60004604
    NAME: Verify market description display- Blank in CMS
    DESCRIPTION: Verify that description is not displayed below the Market tab when left blank in CMS -Horse racing/ Greyhounds market description table
    PRECONDITIONS: 1. Horse racing event should be available
    PRECONDITIONS: 2. User should have admin role for CMS
    PRECONDITIONS: 3: Market description table should have description blank for atleast one Market Template
    """
    keep_browser_open = True

    def test_001_login_to_cms(self):
        """
        DESCRIPTION: Login to CMS
        EXPECTED: User should be logged into CMS
        """
        pass

    def test_002_navigate_to_system_configuration__structure_and_enable_market_description_table(self):
        """
        DESCRIPTION: Navigate to System configuration > Structure and enable Market Description table
        EXPECTED: User should be able to disable Market Description table successfully
        """
        pass

    def test_003_navigate_to_racing_edp_template_and_leave_the_description_blank_for_one_of_the_market_template(self):
        """
        DESCRIPTION: Navigate to Racing EDP template and leave the description blank for one of the market template
        EXPECTED: User should be able to save the changes in CMS
        """
        pass

    def test_004_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral /Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_005_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: User should be navigated Horse racing landing page
        """
        pass

    def test_006_click_on_any_race_which_has_the_market_templates_available_for_which_description_is_left_blank_in_cms(self):
        """
        DESCRIPTION: Click on any race which has the Market templates available for which description is left blank in CMS
        EXPECTED: User should be navigated to EDP page
        """
        pass

    def test_007_validate_the_description_below_the_market_tab(self):
        """
        DESCRIPTION: Validate the description below the Market tab
        EXPECTED: User should not be displayed description
        """
        pass

    def test_008_navigate_to_grey_hounds_and_repeat_67_steps(self):
        """
        DESCRIPTION: Navigate to Grey Hounds and Repeat 6,7 steps
        EXPECTED: User should not be displayed description
        """
        pass

    def test_009_repeat_step_3_for_different_market_templates(self):
        """
        DESCRIPTION: Repeat Step 3 for different market templates
        EXPECTED: User should be able to save the changes in CMS
        """
        pass

    def test_010_repeat_67_steps_for_both_grey_hounds_and_horse_racing(self):
        """
        DESCRIPTION: Repeat 6,7 Steps for both Grey Hounds and Horse racing
        EXPECTED: 
        """
        pass
