import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C44870404_Verify_user_can_navigate_to_in_play_sports_via_Homepage_and_Inplay_Tab(Common):
    """
    TR_ID: C44870404
    NAME: Verify user can navigate to in-play sports via Homepage and Inplay Tab
    DESCRIPTION: Verify user is able to navigate to all available in-play sports via the homepage and in-play tab sections.
    PRECONDITIONS: User is able to access in-play sports via the homepage and in-play tab sections in both logged out and logged in status
    """
    keep_browser_open = True

    def test_001_open_httpsbeta_sportscoralcouk_on_chrome_browser(self):
        """
        DESCRIPTION: Open https://beta-sports.coral.co.uk/ on Chrome browser.
        EXPECTED: https://beta-sports.coral.co.uk/ displayed on Chrome browser.
        """
        pass

    def test_002_verify_inplay_and_live_stream_section_is_visible_on_homepage_with_a_range_of_sports_with_correct_icons_and_signposting_badge_displaying_how_many_events_are_live(self):
        """
        DESCRIPTION: Verify Inplay and Live Stream section is visible on homepage with a range of sports with correct icons and signposting badge displaying how many events are live.
        EXPECTED: Inplay and Live Stream section is visible on homepage with a range of sports displaying correct icons and signposting badge displaying how many events are live.
        """
        pass

    def test_003_verify_navigation_through_each_sport_displayed(self):
        """
        DESCRIPTION: Verify navigation through each sport displayed.
        EXPECTED: User can navigate through each sport successfully.
        """
        pass

    def test_004_verify_correct_eventscompetitions_are_displayed_under_respective_sports_tabs_when_navigated(self):
        """
        DESCRIPTION: Verify correct events/competitions are displayed under respective sports tabs when navigated.
        EXPECTED: Correct events/competitions are displayed in respective sports tabs when navigated.
        """
        pass

    def test_005_click_on_in_play_via_header_sub_menu_links_displayed_under_the_sports_ribbon(self):
        """
        DESCRIPTION: Click on In-Play via header sub menu links (displayed under the sports ribbon)
        EXPECTED: In-play page displayed with carousel of sports, correct icons and signposting badge displaying how many events are live.
        """
        pass

    def test_006_verify_in_play_sports_are_visible_with_a_range_of_sports_with_correct_icons_and_signposting_badge_displaying_how_many_events_are_live(self):
        """
        DESCRIPTION: Verify In-play sports are visible with a range of sports with correct icons and signposting badge displaying how many events are live.
        EXPECTED: In-play sports are visible with a range of sports with correct icons and signposting badge displaying how many events are live.
        """
        pass

    def test_007_verify_navigation_through_each_sport_displayed(self):
        """
        DESCRIPTION: Verify navigation through each sport displayed.
        EXPECTED: User can navigate through each sport successfully.
        """
        pass

    def test_008_verify_correct_eventscompetitions_are_displayed_in_respective_sports(self):
        """
        DESCRIPTION: Verify correct events/competitions are displayed in respective sports.
        EXPECTED: Correct events/competitions are displayed in respective sports.
        """
        pass
