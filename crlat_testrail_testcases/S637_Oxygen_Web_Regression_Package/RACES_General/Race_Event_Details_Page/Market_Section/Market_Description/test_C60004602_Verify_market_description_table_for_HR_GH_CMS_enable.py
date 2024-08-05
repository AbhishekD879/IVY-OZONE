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
class Test_C60004602_Verify_market_description_table_for_HR_GH_CMS_enable(Common):
    """
    TR_ID: C60004602
    NAME: Verify market description table for HR/GH -CMS enable
    DESCRIPTION: Verify that market description is displayed in the EDP page below the Market tab when Horse racing/ Greyhounds market description table toggle is ON and Market description text is configured in CMS
    PRECONDITIONS: 1.  Horse racing & Grey Hound racing event should be available
    PRECONDITIONS: 2. User should have admin role for CMS
    PRECONDITIONS: 3: Market description table should have description added for the Market
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
        EXPECTED: User should be able to enable Market Description table successfully
        """
        pass

    def test_003_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral /Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_004_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: User should be navigated Horse racing landing page
        """
        pass

    def test_005_click_on_any_race_which_has_the_market_templates_available_for_which_description_is_configured_in_cms(self):
        """
        DESCRIPTION: Click on any race which has the Market templates available for which description is configured in CMS
        EXPECTED: User should be navigated to EDP page
        """
        pass

    def test_006_validate_the_description_below_the_market_tab(self):
        """
        DESCRIPTION: Validate the description below the Market tab
        EXPECTED: User should be able to view the description configured for that market template in CMS
        """
        pass

    def test_007_validate_the_description_for_different_market_templates_available(self):
        """
        DESCRIPTION: Validate the description for different market templates available
        EXPECTED: User should be able to view the description configured for that market template in CMS
        """
        pass

    def test_008_navigate_to_grey_hounds_and_repeat_567_steps(self):
        """
        DESCRIPTION: Navigate to Grey Hounds and Repeat 5,6,7 steps
        EXPECTED: 
        """
        pass
