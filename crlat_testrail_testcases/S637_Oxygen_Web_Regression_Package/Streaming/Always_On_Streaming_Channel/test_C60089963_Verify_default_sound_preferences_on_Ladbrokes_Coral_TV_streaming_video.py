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
class Test_C60089963_Verify_default_sound_preferences_on_Ladbrokes_Coral_TV_streaming_video(Common):
    """
    TR_ID: C60089963
    NAME: Verify default sound preferences on Ladbrokes/Coral TV streaming video
    DESCRIPTION: This case verifies default sound preferences on Ladbrokes/Coral TV streaming video
    PRECONDITIONS: **TO BE FINISHED AFTER IMPLEMENTATION OF BMA-56794**
    PRECONDITIONS: List of CMS endpoints: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: Static block for Always On Stream Channel is created in CMS
    PRECONDITIONS: Designs:
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5ba3a1f77d3b30391d93e665/dashboard?sid=5f748efe059ce64d59a70620
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5d24ab732fabd699077b9b8c/dashboard?sid=5f748e0c0bf7df38a687f767
    PRECONDITIONS: In CMS: System Configuration > Structure > %future streaming tv config name% -> set to enabled
    PRECONDITIONS: 1) Load app
    PRECONDITIONS: 2) User is logged in with balance >0 or placed bet during last 24 hours
    PRECONDITIONS: 3) Navigate to Greyhounds Landing page
    """
    keep_browser_open = True

    def test_001_press_on_watch_ladbrokescoral_tv_button(self):
        """
        DESCRIPTION: Press on 'Watch Ladbrokes/Coral TV' button
        EXPECTED: User is navigated to Ladbrokes/Coral TV meeting page
        """
        pass

    def test_002_press_play_button_on_video_streaming_player(self):
        """
        DESCRIPTION: Press Play button on video streaming player
        EXPECTED: * Stream is started, user is able to see the content
        EXPECTED: * Sound is muted by default
        EXPECTED: * Player controls and features are same as on regular event stream and depends on platform under test (web or native)
        """
        pass

    def test_003_unmute_sound_on_video_player(self):
        """
        DESCRIPTION: Unmute sound on video player
        EXPECTED: * User is able to see the content
        EXPECTED: * Sound is enabled on device
        """
        pass

    def test_004_mute_sound_again_on_video_player(self):
        """
        DESCRIPTION: Mute sound again on video player
        EXPECTED: * User is able to see the content
        EXPECTED: * Sound is muted on device
        """
        pass
