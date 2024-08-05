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
class Test_C60005055_Verify_the_display_of_header_for_selected_Market(Common):
    """
    TR_ID: C60005055
    NAME: Verify the display of header for selected Market
    DESCRIPTION: Verify the  header for selected market will be styled as per the new designs
    DESCRIPTION: 1: Bold text for selected market on light background
    DESCRIPTION: 2: Line underneath header to indicate
    PRECONDITIONS: 1: Horse Racing & Grey Hounds Racig events should be available
    PRECONDITIONS: 2: Markets should be available for the events
    """
    keep_browser_open = True

    def test_001_launch_coral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: User should be navigated Horse racing landing page
        """
        pass

    def test_003_click_on_any_horse_racing_event_which_has_markets_available(self):
        """
        DESCRIPTION: Click on any Horse racing event which has markets available
        EXPECTED: User should be navigated to the Event details page
        """
        pass

    def test_004_validate_the_market_headersindexphpattachmentsget120844527indexphpattachmentsget120844528(self):
        """
        DESCRIPTION: Validate the Market Headers
        DESCRIPTION: ![](index.php?/attachments/get/120844527)
        DESCRIPTION: ![](index.php?/attachments/get/120844528)
        EXPECTED: 1: By Default first Market Header should be selected
        EXPECTED: 2: Selected Market should be in Bold on light background
        EXPECTED: 3: Blue Line underneath header to indicate
        """
        pass

    def test_005_click_on_any_other_market_tab_in_the_edp(self):
        """
        DESCRIPTION: Click on any other Market tab in the EDP
        EXPECTED: 1: Selected Market should be in Bold on light background
        EXPECTED: 2: Blue Line underneath header to indicate
        """
        pass

    def test_006_repeat_the_same_for_grey_hound(self):
        """
        DESCRIPTION: Repeat the same for Grey Hound
        EXPECTED: 
        """
        pass
