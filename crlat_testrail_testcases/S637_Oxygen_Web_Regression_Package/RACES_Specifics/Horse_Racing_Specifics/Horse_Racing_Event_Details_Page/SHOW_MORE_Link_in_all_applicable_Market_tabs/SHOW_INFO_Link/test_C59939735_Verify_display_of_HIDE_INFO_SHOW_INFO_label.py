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
class Test_C59939735_Verify_display_of_HIDE_INFO_SHOW_INFO_label(Common):
    """
    TR_ID: C59939735
    NAME: Verify display of "HIDE INFO"/"SHOW INFO" label
    DESCRIPTION: This test case describes the change   of "HIDE INFO" label  to "SHOW INFO" label on clicking for collapsing of all horses related information.
    PRECONDITIONS: 1. Horse racing meeting events, should be available
    """
    keep_browser_open = True

    def test_001_launch__coral_urlfor_coral_mobile_app_launch_app(self):
        """
        DESCRIPTION: Launch  Coral URL
        DESCRIPTION: For Coral Mobile App: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: Coral App should be opened
        """
        pass

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        pass

    def test_003_verify_any_country_panel_meeting_is_available(self):
        """
        DESCRIPTION: Verify any Country Panel meeting is available
        EXPECTED: The meetings in Country panel should be displayed
        """
        pass

    def test_004_click_on_the_any_horse_race_meeting_event(self):
        """
        DESCRIPTION: Click on the any horse race meeting event
        EXPECTED: User should be able to navigate to event detail page. (EDP)
        """
        pass

    def test_005_verify__hide_info_label_is_changed_to_show_info_label_on_clicking(self):
        """
        DESCRIPTION: Verify  "HIDE INFO" label is changed to "SHOW INFO" label on clicking
        EXPECTED: User should able to view "SHOW INFO" link  with collapsing all horse related information
        """
        pass
