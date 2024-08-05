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
class Test_C57732009_Verify_UpSell_BTTS_displayed_based_on_prediction(Common):
    """
    TR_ID: C57732009
    NAME: Verify UpSell 'BTTS' displayed based on prediction
    DESCRIPTION: This test case verifies UpSell 'Both Teams To Score (BTTS)' displayed based on prediction
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. Market with name |Both Teams to Score| configured on Openbet https://tst2-backoffice-lcm.ladbrokes.com/ti
    PRECONDITIONS: 2. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 3. User on 'Current Tab'
    """
    keep_browser_open = True

    def test_001_set_scores_and_tap_on_submit_button_on_current_tab(self):
        """
        DESCRIPTION: Set scores and Tap on 'Submit' button on 'Current Tab'
        EXPECTED: 'You are in' page is successfully opened and designed according to:
        EXPECTED: https://app.zeplin.io/project/5c471d82d6094838624e7232/screen/5c5053d01a14267a73d1cb4f
        EXPECTED: Three UpSell 'Treble - Both Teams To Score (BTTS)' are displayed based on their prediction:
        EXPECTED: - 'No' - if any teems prediction **has** '0' scores
        EXPECTED: - 'Yes' - if both teems prediction **has** '>0' scores
        """
        pass
