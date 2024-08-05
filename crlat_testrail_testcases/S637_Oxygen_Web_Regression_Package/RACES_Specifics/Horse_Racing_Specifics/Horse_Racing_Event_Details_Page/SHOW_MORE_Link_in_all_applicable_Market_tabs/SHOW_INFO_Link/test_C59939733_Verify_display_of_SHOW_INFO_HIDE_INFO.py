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
class Test_C59939733_Verify_display_of_SHOW_INFO_HIDE_INFO(Common):
    """
    TR_ID: C59939733
    NAME: Verify display of "SHOW INFO"/ "HIDE INFO"
    DESCRIPTION: This test case describes the change   of "SHOW INFO" label  to "HIDE INFO" label on clicking for expansion of all horses related information.
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

    def test_005_verify__show_info_label_is_changed_to_hide_info_label_on_clicking(self):
        """
        DESCRIPTION: Verify  "SHOW INFO" label is changed to "HIDE INFO" label on clicking
        EXPECTED: User should able to view "HIDE INFO" link
        """
        pass
