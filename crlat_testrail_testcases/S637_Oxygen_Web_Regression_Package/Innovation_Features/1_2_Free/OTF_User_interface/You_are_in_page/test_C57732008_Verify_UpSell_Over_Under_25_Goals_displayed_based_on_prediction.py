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
class Test_C57732008_Verify_UpSell_Over_Under_25_Goals_displayed_based_on_prediction(Common):
    """
    TR_ID: C57732008
    NAME: Verify UpSell 'Over/Under 2.5 Goals' displayed based on prediction
    DESCRIPTION: This test case verifies 'You are in' page view
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. Market with name |Over/Under Total Goals| |2.5| configured on Openbet https://tst2-backoffice-lcm.ladbrokes.com/ti
    PRECONDITIONS: 2. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 3. User on 'Current Tab'
    """
    keep_browser_open = True

    def test_001_set_scores_and_tap_on_submit_button_on_current_tab(self):
        """
        DESCRIPTION: Set scores and Tap on 'Submit' button on 'Current Tab'
        EXPECTED: 'You are in' page is successfully opened and designed according to:
        EXPECTED: https://app.zeplin.io/project/5c471d82d6094838624e7232/screen/5c5053d01a14267a73d1ca9a
        EXPECTED: Three UpSell 'Treble - Over/Under 2.5 Goals' are displayed based on their prediction:
        EXPECTED: - 'Under 2.5' - if prediction has scores pairs [0, 0], [0, 1], [1, 0], [1, 1], [2, 0], [0, 2]
        EXPECTED: - 'Over 2.5' - if prediction has any other prediction outside scenario 1(i.e greater than 2.5)
        """
        pass
