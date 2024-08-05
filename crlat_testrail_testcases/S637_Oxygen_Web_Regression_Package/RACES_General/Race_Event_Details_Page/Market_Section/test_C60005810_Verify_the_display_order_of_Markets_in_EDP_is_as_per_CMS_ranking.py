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
class Test_C60005810_Verify_the_display_order_of_Markets_in_EDP_is_as_per_CMS_ranking(Common):
    """
    TR_ID: C60005810
    NAME: Verify the display order of Markets in EDP is as per CMS ranking
    DESCRIPTION: Verify that display order of Markets tabs in EDP is as configured in CMS
    PRECONDITIONS: 1: Horse racing & Grey Hounds racing should be available
    PRECONDITIONS: 2: Markets should be available
    PRECONDITIONS: 3: User should have CMS access
    """
    keep_browser_open = True

    def test_001_login_to_cms(self):
        """
        DESCRIPTION: Login to CMS
        EXPECTED: CMS should be logged in
        """
        pass

    def test_002_navigate_to_racing_edp_in_cms_and_configure_the_markets__adding_the_markets_or_re_arranging_the_order_by_drag__drop(self):
        """
        DESCRIPTION: Navigate to Racing EDP in CMS and configure the Markets ( Adding the markets or re-arranging the order by drag & drop)
        EXPECTED: User should be able to save the changes successfully
        """
        pass

    def test_003_1launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: 1:Launch Coral/ Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_004_2_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: 2: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: Horse Racing Landing page should be displayed
        """
        pass

    def test_005_click_on_any_event_with_markets_available(self):
        """
        DESCRIPTION: Click on any event with Markets available
        EXPECTED: User should be navigated to EDP
        """
        pass

    def test_006_validate_the_display_order_of_markets(self):
        """
        DESCRIPTION: Validate the display order of Markets
        EXPECTED: 1: Market tabs should be displayed as per CMS ranking
        EXPECTED: 2: If any market is unavailable the next market should take it's position
        """
        pass

    def test_007_navigate_to_grey_hounds_and_validate_the_same(self):
        """
        DESCRIPTION: Navigate to Grey Hounds and Validate the same
        EXPECTED: 
        """
        pass
