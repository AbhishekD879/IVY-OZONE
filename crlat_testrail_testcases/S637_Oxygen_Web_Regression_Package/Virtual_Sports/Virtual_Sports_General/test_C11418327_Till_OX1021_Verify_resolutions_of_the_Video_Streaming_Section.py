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
class Test_C11418327_Till_OX1021_Verify_resolutions_of_the_Video_Streaming_Section(Common):
    """
    TR_ID: C11418327
    NAME: [Till OX102.1] Verify resolutions of the Video Streaming Section
    DESCRIPTION: This test case verifies size of the Video streaming section on the Virtual Sports event details page with different resolutions.
    PRECONDITIONS: DESIGNS:
    PRECONDITIONS: 1600px pre click:
    PRECONDITIONS: https://app.zeplin.io/project/59f0b3bf277e469f985e211d/screen/5b0676039af8b1243f4b2694
    PRECONDITIONS: https://app.zeplin.io/project/59f0b3bf277e469f985e211d/screen/5b0676083e6866d43a014f83
    PRECONDITIONS: 1600px after click:
    PRECONDITIONS: https://app.zeplin.io/project/59f0b3bf277e469f985e211d/screen/5b067603b17a27c252c792f4
    PRECONDITIONS: https://app.zeplin.io/project/59f0b3bf277e469f985e211d/screen/5b0676023d1806165dd63a5b
    PRECONDITIONS: 1280px:
    PRECONDITIONS: https://app.zeplin.io/project/59f0b3bf277e469f985e211d/screen/5b067602d2a8c986855f0c61
    PRECONDITIONS: 1025px:
    PRECONDITIONS: https://app.zeplin.io/project/59f0b3bf277e469f985e211d/screen/5b0676023b1452b60546a906
    PRECONDITIONS: 970px:
    PRECONDITIONS: https://app.zeplin.io/project/59f0b3bf277e469f985e211d/screen/5b067602e9672286526ca43a
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_change_pagescreen_resolution_to_1600pxverify_size_of_the_video_streaming_sections(self):
        """
        DESCRIPTION: Change page/screen resolution to 1600px
        DESCRIPTION: Verify size of the video streaming sections
        EXPECTED: * Virtuals video player positioned under the Event Header, Breadcrumbs and Sports Ribbon in the center
        EXPECTED: * Video streaming section size should be 640x360
        """
        pass

    def test_002_navigate_to_the_following_virtual_sportsvirtual_horseracingvirtual_footballvirtual_greyhoundsvirtual_tennisvirtual_cyclingvirtual_speedwayvirtual_motorsportsverify_the_size_of_the_video_streaming_sections(self):
        """
        DESCRIPTION: Navigate to the following Virtual Sports:
        DESCRIPTION: Virtual Horseracing
        DESCRIPTION: Virtual Football
        DESCRIPTION: Virtual Greyhounds
        DESCRIPTION: Virtual Tennis
        DESCRIPTION: Virtual Cycling
        DESCRIPTION: Virtual Speedway
        DESCRIPTION: Virtual Motorsports
        DESCRIPTION: Verify the size of the video streaming sections.
        EXPECTED: * Video streaming section size should be 640x360
        """
        pass

    def test_003_repeat_this_test_case_with_the_following_pagescreen_resolutions__1280_px__1025_px__970_pxverify_the_sizes_of_the_video_streaming_sections(self):
        """
        DESCRIPTION: Repeat this test case with the following page/screen resolutions:
        DESCRIPTION: - 1280 px
        DESCRIPTION: - 1025 px
        DESCRIPTION: - 970 px
        DESCRIPTION: Verify the sizes of the video streaming sections
        EXPECTED: Video streaming section size should be:
        EXPECTED: 1280px - 640x360
        EXPECTED: 1025px - 525x394
        EXPECTED: 970px - 460-345
        """
        pass
