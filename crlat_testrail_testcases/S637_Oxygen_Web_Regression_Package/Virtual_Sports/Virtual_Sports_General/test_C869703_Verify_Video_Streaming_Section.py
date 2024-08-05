import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C869703_Verify_Video_Streaming_Section(Common):
    """
    TR_ID: C869703
    NAME: Verify Video Streaming Section
    DESCRIPTION: This test case verifies Video streaming section on the Virtual Sports event details page
    PRECONDITIONS: List of stream URLs:
    PRECONDITIONS: HORSES:
    PRECONDITIONS: Web	https://player.igamemedia.com/vplayer?c=83127&s=horses&q=web
    PRECONDITIONS: Mobile High	https://player.igamemedia.com/vplayer?c=83127&s=horses&q=mobhi
    PRECONDITIONS: Mobile Low	https://player.igamemedia.com/vplayer?c=83127&s=horses&q=moblo
    PRECONDITIONS: DOGS:
    PRECONDITIONS: Web	https://player.igamemedia.com/vplayer?c=83127&s=dogs&q=web
    PRECONDITIONS: Mobile High	https://player.igamemedia.com/vplayer?c=83127&s=dogs&q=mobhi
    PRECONDITIONS: Mobile Low	https://player.igamemedia.com/vplayer?c=83127&s=dogs&q=moblo
    PRECONDITIONS: CARS:
    PRECONDITIONS: Web	https://player.igamemedia.com/vplayer?c=83127&s=cars&q=web
    PRECONDITIONS: Mobile High	https://player.igamemedia.com/vplayer?c=83127&s=cars&q=mobhi
    PRECONDITIONS: Mobile Low	https://player.igamemedia.com/vplayer?c=83127&s=cars&q=moblo
    PRECONDITIONS: SPEEDWAY:
    PRECONDITIONS: Web	https://player.igamemedia.com/vplayer?c=83127&s=speedway&q=web
    PRECONDITIONS: Mobile High	https://player.igamemedia.com/vplayer?c=83127&s=speedway&q=mobhi
    PRECONDITIONS: Mobile Low	https://player.igamemedia.com/vplayer?c=83127&s=speedway&q=moblo
    PRECONDITIONS: CYCLING:
    PRECONDITIONS: Web	https://player.igamemedia.com/vplayer?c=83127&s=cycling&q=web
    PRECONDITIONS: Mobile High	https://player.igamemedia.com/vplayer?c=83127&s=cycling&q=mobhi
    PRECONDITIONS: Mobile Low	https://player.igamemedia.com/vplayer?c=83127&s=cycling&q=moblo
    PRECONDITIONS: TENNIS:
    PRECONDITIONS: Web	https://player.igamemedia.com/vplayer?c=83127&s=tennis&q=web
    PRECONDITIONS: Mobile High	https://player.igamemedia.com/vplayer?c=83127&s=tennis&q=mobhi
    PRECONDITIONS: Mobile Low	https://player.igamemedia.com/vplayer?c=83127&s=tennis&q=moblo
    PRECONDITIONS: FOOTBALL:
    PRECONDITIONS: Web	https://player.igamemedia.com/vplayer?c=83127&s=test1&q=web
    PRECONDITIONS: Mobile High	https://player.igamemedia.com/vplayer?c=83127&s=test1&q=mobhi
    PRECONDITIONS: Mobile Low	https://player.igamemedia.com/vplayer?c=83127&s=test1&q=moblo
    PRECONDITIONS: GRAND NATIONAL:
    PRECONDITIONS: TBD
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_verify_expanding_of_video_streaming_sections(self):
        """
        DESCRIPTION: Verify expanding of video streaming sections
        EXPECTED: * Video streaming section is expanded
        EXPECTED: * It is not possible to collapse the section
        """
        pass

    def test_002_verify_video_streaming_section1_use_play_button_for_non_applicable_devices2_auto_stream_activation_for_applicable_devices(self):
        """
        DESCRIPTION: Verify video streaming section:
        DESCRIPTION: 1. Use 'Play' button for non-applicable devices
        DESCRIPTION: 2. Auto-stream activation for applicable devices
        EXPECTED: * Black countdown timer overlay is NOT available
        EXPECTED: 1. It is possible to play video by clicking on 'Play' button.
        EXPECTED: 2. Video image, containing countdown timer is displayed
        EXPECTED: * Once event becomes live, corresponding video of an event is played
        """
        pass

    def test_003_switch_video_to_full_screen_and_back(self):
        """
        DESCRIPTION: Switch video to full screen and back
        EXPECTED: Video is opened in a full screen and back (only for applicable players)
        """
        pass

    def test_004_using_inspect_tool_from_the_dev_tools_verify_video_streaming_links(self):
        """
        DESCRIPTION: Using "Inspect" tool from the dev tools, verify video streaming links
        EXPECTED: For every virtual sport, video streaming links correspond to links, listed in Preconditions
        """
        pass

    def test_005_check_the_timer_on_sports_carousel_tab_for_current_sport(self):
        """
        DESCRIPTION: Check the timer on sports carousel tab for current sport
        EXPECTED: Countdown timer is replaced with 'Live' label
        """
        pass

    def test_006_repeat_this_test_case_for_the_following_virtual_sports_greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
        """
        DESCRIPTION: Repeat this test case for the following Virtual Sports:
        DESCRIPTION: * Greyhounds
        DESCRIPTION: * Football,
        DESCRIPTION: * Motorsports,
        DESCRIPTION: * Cycling,
        DESCRIPTION: * Speedway,
        DESCRIPTION: * Tennis
        DESCRIPTION: * Grand National
        EXPECTED: 
        """
        pass
