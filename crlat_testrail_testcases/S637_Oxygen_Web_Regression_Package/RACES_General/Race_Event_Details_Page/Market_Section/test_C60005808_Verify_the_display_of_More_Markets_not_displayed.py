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
class Test_C60005808_Verify_the_display_of_More_Markets_not_displayed(Common):
    """
    TR_ID: C60005808
    NAME: Verify the display of More Markets- not displayed
    DESCRIPTION: Verify that 'More Markets' tab is no longer displayed in both HR/GH event display page and all the markets previously displayed under More markets tab- Insurance markets are displayed as individual tabs in EDP
    PRECONDITIONS: 1. Horse racing and Grey Hound racing events & markets should be available.
    """
    keep_browser_open = True

    def test_001_1launch_coral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: 1:Launch Coral URL
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

    def test_003_click_on_any_event_which_has_insurance_markets_available(self):
        """
        DESCRIPTION: Click on any event which has Insurance markets available
        EXPECTED: User should be navigated to EDP
        """
        pass

    def test_004_validate_more_markets_is_not_displayed(self):
        """
        DESCRIPTION: Validate More Markets is not displayed
        EXPECTED: 1: More Markets is not displayed
        EXPECTED: 2: All the Markets are displayed as per their ranking
        """
        pass

    def test_005_navigate_to_grey_hounds_and_validate_the_same(self):
        """
        DESCRIPTION: Navigate to Grey Hounds and Validate the same
        EXPECTED: 
        """
        pass
