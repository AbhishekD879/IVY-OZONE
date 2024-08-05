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
class Test_C57731990_Lads_only_Verify_getting_username_value_from_local_storage(Common):
    """
    TR_ID: C57731990
    NAME: [Lads only] Verify getting 'username' value from local storage
    DESCRIPTION: This test case verifies getting 'username' value from local storage
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE predictor and win £150' is available on Homepage or Football landing page
    """
    keep_browser_open = True

    def test_001_tap_on_play_1_2_free_predictor_and_win_150_quick_link(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE predictor and win £150' quick link
        EXPECTED: User successfully navigated to 1-2-Free
        """
        pass

    def test_002_open_browser_local_storage(self):
        """
        DESCRIPTION: Open browser Local Storage
        EXPECTED: 'lbruser' key present with 'username' according to login credentials
        """
        pass
