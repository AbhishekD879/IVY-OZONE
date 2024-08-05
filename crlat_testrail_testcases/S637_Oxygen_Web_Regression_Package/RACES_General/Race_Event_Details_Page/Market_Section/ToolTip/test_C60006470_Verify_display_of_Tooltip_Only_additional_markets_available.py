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
class Test_C60006470_Verify_display_of_Tooltip_Only_additional_markets_available(Common):
    """
    TR_ID: C60006470
    NAME: Verify display of Tooltip: Only additional markets available
    DESCRIPTION: Verify that Tooltip is displayed only when additional markets are available
    PRECONDITIONS: 1: Tooltip should be enabled in CMS
    PRECONDITIONS: 2: HR/GH events should be available with additional markets that needs scrolling
    PRECONDITIONS: 3: Tooltip for the device is not shown previously
    """
    keep_browser_open = True

    def test_001_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral/ Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: Horse Racing Landing page should be displayed
        """
        pass

    def test_003_click_on_any_horse_racing_event_that_has_additional_markets_that_needs_scrolling(self):
        """
        DESCRIPTION: Click on any horse racing event that has additional markets that needs scrolling
        EXPECTED: User should be navigated to event details page (race card)
        """
        pass

    def test_004_validate_the_display_of_tooltipindexphpattachmentsget120878235indexphpattachmentsget120878237indexphpattachmentsget120878236indexphpattachmentsget120878238(self):
        """
        DESCRIPTION: Validate the display of Tooltip
        DESCRIPTION: ![](index.php?/attachments/get/120878235)
        DESCRIPTION: ![](index.php?/attachments/get/120878237)
        DESCRIPTION: ![](index.php?/attachments/get/120878236)
        DESCRIPTION: ![](index.php?/attachments/get/120878238)
        EXPECTED: User should be able to view the Tooltip "There are more markets for you to view below"
        EXPECTED: "Look below to find out what other markets are available"
        EXPECTED: (Text that is configured in CMS)
        """
        pass

    def test_005_repeat_step_2_to_step_4_and_validate_for_grey_hound_racing(self):
        """
        DESCRIPTION: Repeat Step 2 to Step 4 and Validate for Grey Hound racing
        EXPECTED: User should be able to view the Tooltip "There are more markets for you to view below"
        EXPECTED: "Look below to find out what other markets are available"
        EXPECTED: (Text that is configured in CMS)
        """
        pass
