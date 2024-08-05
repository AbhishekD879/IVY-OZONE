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
class Test_C66017377_Verify_Meetings_Overlay_and_Next_Races_EDP_Navigation_in_Horse_racing_EDP(Common):
    """
    TR_ID: C66017377
    NAME: Verify Meetings Overlay  and Next Races EDP Navigation in Horse racing EDP
    DESCRIPTION: This testcase verifies Meetings Overlay in Horse racing EDP
    PRECONDITIONS: 1.App is installed and launched.
    PRECONDITIONS: 2.User is logged in.
    PRECONDITIONS: 3.Should have horse Race events
    """
    keep_browser_open = True

    def test_000_launch_the__application(self):
        """
        DESCRIPTION: Launch the  application
        EXPECTED: User should be able to launch the app should be see the Homepage is loaded successfully.
        """
        pass

    def test_000_navigate_to_horse_race_pageclick_on_any_event_and_observe(self):
        """
        DESCRIPTION: Navigate to Horse Race page,Click on any event and observe
        EXPECTED: User should navigate to EDP for respective event
        """
        pass

    def test_000_click_on_the_meetings_drop_down(self):
        """
        DESCRIPTION: Click on the meetings drop down
        EXPECTED: Meetings overlay should open and display data.
        EXPECTED: The ordering of content in the overlay should follow the current hierarchy as on Horse Racing homepage.
        EXPECTED: The left and right arrows should be scrollable on the available content
        """
        pass

    def test_000_click__x_on_meeting_overlay(self):
        """
        DESCRIPTION: Click  'X' on meeting overlay
        EXPECTED: User should return back to the EDP page.
        """
        pass

    def test_000_verify__country_panel(self):
        """
        DESCRIPTION: Verify  country panel
        EXPECTED: Only first Country panel should be expanded by default
        EXPECTED: Display order in the  country panels should be same as Horse Racing homepage
        """
        pass

    def test_000_click_on_any_of_the_race_in_from_uk_and_irish_section(self):
        """
        DESCRIPTION: Click on any of the race in from UK and Irish section
        EXPECTED: Should navigate to respective HR EDP
        """
        pass

    def test_000_verify_default_tab_in_meeting_overlay(self):
        """
        DESCRIPTION: Verify default tab in Meeting Overlay
        EXPECTED: The meetings overlay will open with Today (selected by default),/ Tomorrow / Day 'X' tab
        EXPECTED: user should be able to switch from default to tomorrow/Day'X'
        """
        pass

    def test_000_verify_signposting_in_all_sections(self):
        """
        DESCRIPTION: Verify signposting in all sections
        EXPECTED: Signposting elements like Extra Place Race , BOG, Watch, Cash out should display for all sections
        """
        pass

    def test_000_navigate_to_future_tab(self):
        """
        DESCRIPTION: Navigate to Future tab
        EXPECTED: Meetings overlay should be opened with 3 different Tabs (Flat, National hunt and International)
        """
        pass
