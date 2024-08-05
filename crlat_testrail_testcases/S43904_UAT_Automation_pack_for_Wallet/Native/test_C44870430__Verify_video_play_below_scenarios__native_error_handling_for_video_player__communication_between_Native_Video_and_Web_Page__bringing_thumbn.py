import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C44870430__Verify_video_play_below_scenarios__native_error_handling_for_video_player__communication_between_Native_Video_and_Web_Page__bringing_thumbnail_video_back_into_standard_view__dragging_and_closing_video_while_in_thumbnail__video_thumbnail_contr(Common):
    """
    TR_ID: C44870430
    NAME: " Verify video play below scenarios,   native error handling for video player   communication between Native Video and Web Page   bringing thumbnail video back into standard view   dragging and closing video while in thumbnail   video thumbnail contr
    DESCRIPTION: " Verify video play below scenarios,
    DESCRIPTION: native error handling for video player
    DESCRIPTION: communication between Native Video and Web Page
    DESCRIPTION: bringing thumbnail video back into standard view
    DESCRIPTION: dragging and closing video while in thumbnail
    DESCRIPTION: video thumbnail controls"
    PRECONDITIONS: 
    """
    keep_browser_open = True
