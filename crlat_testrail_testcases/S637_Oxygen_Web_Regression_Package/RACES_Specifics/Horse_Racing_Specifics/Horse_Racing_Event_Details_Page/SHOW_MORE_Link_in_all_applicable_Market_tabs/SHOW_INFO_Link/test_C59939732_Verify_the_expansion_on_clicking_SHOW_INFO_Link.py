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
class Test_C59939732_Verify_the_expansion_on_clicking_SHOW_INFO_Link(Common):
    """
    TR_ID: C59939732
    NAME: Verify the expansion on clicking "SHOW INFO" Link
    DESCRIPTION: This Test case describes  the expansion of panels for all the horses related information in that meeting point is displayed on clicking "SHOW INFO" Link
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

    def test_005_verify__expansion_of_panels_for_all_the_horses_related_information_in_that_meeting_point_is_displayed_on_clicking_show_info_link(self):
        """
        DESCRIPTION: Verify  expansion of panels for all the horses related information in that meeting point is displayed on clicking "SHOW INFO" Link
        EXPECTED: User should able to see the expansion of panels for all the horses related information.
        """
        pass
