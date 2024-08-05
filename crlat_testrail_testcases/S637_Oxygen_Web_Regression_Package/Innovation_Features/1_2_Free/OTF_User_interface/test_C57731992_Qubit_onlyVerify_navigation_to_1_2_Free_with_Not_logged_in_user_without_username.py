import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57731992_Qubit_onlyVerify_navigation_to_1_2_Free_with_Not_logged_in_user_without_username(Common):
    """
    TR_ID: C57731992
    NAME: [Qubit only]Verify navigation to 1-2-Free with Not logged in user (without 'username')
    DESCRIPTION: This test case navigation to 1-2-Free without 'username'
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is NOT logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE predictor and win £150' is available on Homepage or Football landing page
    """
    keep_browser_open = True

    def test_001_tap_on_play_1_2_free_predictor_and_win_150_quick_link(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE predictor and win £150' quick link
        EXPECTED: User NOT navigated to 1-2-Free
        EXPECTED: Pop-up with information that user should be logged in is shown
        """
        pass
