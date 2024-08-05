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
class Test_C60005811_Verify_the_display_order_of_Markets_when_they_are_not_configured_in_CMS(Common):
    """
    TR_ID: C60005811
    NAME: Verify the display order of Markets when they are not configured in CMS
    DESCRIPTION: Verify the display order of Markets when they are not configured in CMS
    PRECONDITIONS: 1: Horse racing & Grey Hounds racing should be available
    PRECONDITIONS: 2: Markets should be available which are not configured in CMS
    PRECONDITIONS: 3: User should have CMS access
    """
    keep_browser_open = True

    def test_001_1launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: 1:Launch Coral/ Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_2_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: 2: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: Horse Racing Landing page should be displayed
        """
        pass

    def test_003_click_on_any_event_with_markets_available(self):
        """
        DESCRIPTION: Click on any event with Markets available
        EXPECTED: User should be navigated to EDP
        """
        pass

    def test_004_validate_the_display_order_of_markets_which_are_not_configured_in_cms(self):
        """
        DESCRIPTION: Validate the display order of Markets which are not Configured in CMS
        EXPECTED: 
        """
        pass

    def test_005_navigate_to_grey_hounds_and_validate_the_same(self):
        """
        DESCRIPTION: Navigate to Grey Hounds and Validate the same
        EXPECTED: 
        """
        pass
