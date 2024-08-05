import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C44870314_Verify_the_layout_and_the_controls_for_live_stream_of_virtual_sports(Common):
    """
    TR_ID: C44870314
    NAME: Verify the layout and the controls for live stream of virtual sports.
    DESCRIPTION: 
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def test_001_navigate_to_virtuals_and_verify_the_layout_of_the_live_stream_window(self):
        """
        DESCRIPTION: Navigate to Virtuals and verify the layout of the live stream window.
        EXPECTED: The following controls are displayed in the live stream window -
        EXPECTED: 1. The pause/play button (if the stream is playing then the pause button is displayed after tapping in the live stream window.
        EXPECTED: 2. The volume button
        EXPECTED: 3. LIVE label
        EXPECTED: 4. Settings
        EXPECTED: 5. Arrows to open the live stream in full screen mode.
        """
        pass

    def test_002_select_grand_nationals_if_not_selected_by_default_and_verify(self):
        """
        DESCRIPTION: Select Grand Nationals (if not selected by default) and verify.
        EXPECTED: The live stream starts playing automatically.
        """
        pass

    def test_003_pause_and_play_the_live_stream_verify(self):
        """
        DESCRIPTION: Pause and play the live stream. Verify.
        EXPECTED: The live stream is paused and then again resumes after clicking on Play.
        """
        pass

    def test_004_expand_the_live_stream_window_verify(self):
        """
        DESCRIPTION: Expand the live stream window. Verify.
        EXPECTED: The live stream window opens in full screen mode, i.e. occupies the entire width of the screen display.
        """
        pass

    def test_005_minimise_the_live_stream_window_verify(self):
        """
        DESCRIPTION: Minimise the live stream window. Verify.
        EXPECTED: The live stream window is minimised, i.e. occupies a small part of the screen as seen in step 1.
        """
        pass

    def test_006_pause_and_play_the_live_stream_verify(self):
        """
        DESCRIPTION: Pause and play the live stream. Verify.
        EXPECTED: The live stream is paused and then again resumes after clicking on Play.
        """
        pass

    def test_007_perform_steps_1_6_for_the_following_virtuals_live_stream_provided_by_inspire__1_horse_racing2_hr_jumps3_greyhounds4_football5_motorsports(self):
        """
        DESCRIPTION: Perform steps 1-6 for the following virtuals (live stream provided by Inspire) -
        DESCRIPTION: 1. Horse Racing
        DESCRIPTION: 2. HR Jumps
        DESCRIPTION: 3. Greyhounds
        DESCRIPTION: 4. Football
        DESCRIPTION: 5. Motorsports
        EXPECTED: The expected is same as mentioned in steps 1-6.
        """
        pass
