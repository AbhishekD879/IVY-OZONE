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
class Test_C59939730_Verify_the_display_of_SHOW_INFO_Link(Common):
    """
    TR_ID: C59939730
    NAME: Verify the display of "SHOW INFO" Link
    DESCRIPTION: This test case describes that "SHOW INFO" Link is displayed in Horse racing meeting event detail page.
    PRECONDITIONS: 1. Horse racing meeting event, should be available
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
        EXPECTED: User should be able navigate to event detail page. (EDP)
        """
        pass

    def test_005_verify_show_info_link_is_displayed_above_the_first_horse_and_below_eachway__odds__label_in_the_same_line_where_sort_label_is_displayed_left_aligned(self):
        """
        DESCRIPTION: Verify "SHOW INFO" Link is displayed above the first horse and below "Eachway:- Odds " label, in the same line where "SORT" label is displayed. (left aligned)
        EXPECTED: User should able to see"SHOW INFO" Link
        """
        pass
