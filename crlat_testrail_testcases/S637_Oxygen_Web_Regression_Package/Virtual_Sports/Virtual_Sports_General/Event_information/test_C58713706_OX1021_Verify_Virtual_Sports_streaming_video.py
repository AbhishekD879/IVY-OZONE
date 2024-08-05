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
class Test_C58713706_OX1021_Verify_Virtual_Sports_streaming_video(Common):
    """
    TR_ID: C58713706
    NAME: [OX102.1] Verify Virtual Sports streaming video
    DESCRIPTION: This test case verifies Verify Virtual Sports streaming video
    PRECONDITIONS: How to configure Stream URLs for Virtual Sports:
    PRECONDITIONS: 1. Open CMS > Virtual Sports > Sport > Child Sport
    PRECONDITIONS: 2. Put Url in 'Stream URL' field
    PRECONDITIONS: Test: https://player-test.igamemedia.com/vplayer?c=30473&s=football
    PRECONDITIONS: Prod Ladbrokes: https://player.igamemedia.com/vplayer?c=30473&s=football
    PRECONDITIONS: Prod Coral: https://player.igamemedia.com/vplayer?c=83127&s=football
    PRECONDITIONS: Where **football** is the key of current Virtual Sport
    PRECONDITIONS: Virtual Sports stream keys:
    PRECONDITIONS: 'virtual-horse-racing': 'horses',
    PRECONDITIONS: 'virtual-football': 'football',
    PRECONDITIONS: 'virtual-greyhounds': 'dogs',
    PRECONDITIONS: 'virtual-boxing': 'boxing',
    PRECONDITIONS: 'virtual-darts': 'darts',
    PRECONDITIONS: 'virtual-tennis': 'tennis',
    PRECONDITIONS: 'virtual-cycling': 'cycling',
    PRECONDITIONS: 'virtual-speedway': 'speedway',
    PRECONDITIONS: 'virtual-motorsports': 'cars',
    PRECONDITIONS: 'virtual-grand-national': 'grandnational',
    PRECONDITIONS: 'virtual-basketball': 'basketball',
    PRECONDITIONS: 'virtual-hr-jumps': 'horsesjumps',
    PRECONDITIONS: 'virtual-footballrush': 'footballrush2'
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_select_one_of_virtual_sports(self):
        """
        DESCRIPTION: Select one of Virtual sports
        EXPECTED: - The stream is successfully displayed for the current sport
        EXPECTED: - The stream corresponds to live event
        EXPECTED: - Stream corresponds the Stream URL from CMS with screen parameter
        EXPECTED: (e.g. https://player-test.igamemedia.com/vplayer?c=30473&s= **football**)
        """
        pass

    def test_002_return_back_to_virtual_sports_pageopen_another_type_of_virtual_sport(self):
        """
        DESCRIPTION: Return back to Virtual Sports Page
        DESCRIPTION: Open another type of Virtual sport
        EXPECTED: - The stream is successfully displayed for the current sport
        EXPECTED: - The stream corresponds to live event
        EXPECTED: - Stream corresponds the Stream URL from CMS with screen parameter
        EXPECTED: (e.g. https://player-test.igamemedia.com/vplayer?c=30473&s= **cycling**)
        """
        pass

    def test_003_repeat_this_test_case_for_the_following_virtual_sportscyclinghorse_racinggreyhoundsfootballmotorsportsspeedwaytennisdartsboxinggrand_nationalbasketballhorsesjumps(self):
        """
        DESCRIPTION: Repeat this test case for the following virtual sports:
        DESCRIPTION: Cycling,
        DESCRIPTION: Horse Racing,
        DESCRIPTION: Greyhounds,
        DESCRIPTION: Football,
        DESCRIPTION: Motorsports,
        DESCRIPTION: Speedway,
        DESCRIPTION: Tennis,
        DESCRIPTION: Darts,
        DESCRIPTION: Boxing,
        DESCRIPTION: Grand National,
        DESCRIPTION: Basketball,
        DESCRIPTION: Horsesjumps
        EXPECTED: 
        """
        pass

    def test_004_select_one_of_virtual_sports_where_stream_url_is_empty_on_cms(self):
        """
        DESCRIPTION: Select one of Virtual sports where Stream URL is empty on CMS
        EXPECTED: - The stream is NOT displayed for the current sport
        EXPECTED: - Error with the text 'Stream details were not found' displayed in Stream frame
        """
        pass
