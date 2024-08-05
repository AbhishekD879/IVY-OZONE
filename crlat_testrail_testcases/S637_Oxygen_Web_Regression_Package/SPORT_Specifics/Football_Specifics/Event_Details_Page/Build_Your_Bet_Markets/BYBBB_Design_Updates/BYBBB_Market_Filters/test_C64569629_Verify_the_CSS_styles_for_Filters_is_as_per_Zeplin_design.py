import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C64569629_Verify_the_CSS_styles_for_Filters_is_as_per_Zeplin_design(Common):
    """
    TR_ID: C64569629
    NAME: Verify the CSS styles for Filters is as per Zeplin design
    DESCRIPTION: Verify the CSS styles for Filters is as per Zeplin design
    PRECONDITIONS: Zeplin : https://app.zeplin.io/project/610ba4fa9f2dc2bf673ee8d5/dashboard?sid=61717295eb76ea9f87269469
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_football_edp(self):
        """
        DESCRIPTION: Navigate to Football EDP
        EXPECTED: EDP should be displayed with BYB/BB Markets
        """
        pass

    def test_003_click_on_bybbb(self):
        """
        DESCRIPTION: Click on BYB/BB
        EXPECTED: BYB/BB Markets should be displayed
        """
        pass

    def test_004_validate_css_styles_for_market_label_and_description(self):
        """
        DESCRIPTION: Validate CSS Styles for Market Label and Description
        EXPECTED: CSS styles should be as per Zeplin
        """
        pass

    def test_005_validate_css_styles_for_filtershttpsappzeplinioproject610ba4fa9f2dc2bf673ee8d5dashboardsid61717295eb76ea9f87269469(self):
        """
        DESCRIPTION: Validate CSS styles for Filters
        DESCRIPTION: https://app.zeplin.io/project/610ba4fa9f2dc2bf673ee8d5/dashboard?sid=61717295eb76ea9f87269469
        EXPECTED: CSS styles should be as per Zeplin
        """
        pass
