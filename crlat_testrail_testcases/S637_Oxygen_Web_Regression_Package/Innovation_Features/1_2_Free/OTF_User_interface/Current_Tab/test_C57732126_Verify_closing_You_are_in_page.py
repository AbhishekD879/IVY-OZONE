import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C57732126_Verify_closing_You_are_in_page(Common):
    """
    TR_ID: C57732126
    NAME: Verify closing 'You are in' page
    DESCRIPTION: This test case verifies closing 'You are in' page
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: for Qubit version (deprecated) https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: for Oxygen version: https://confluence.egalacoral.com/display/SPI/1-2-Free+configurations?preview=/106397589/106397584/1-2-Free%20CMS%20configurations.pdf
    PRECONDITIONS: 1. User is logged In
    """
    keep_browser_open = True

    def test_001_open_current_tab_and_submit_a_prediction(self):
        """
        DESCRIPTION: Open 'Current Tab' and submit a prediction
        EXPECTED: - Prediction is successfully saved
        EXPECTED: - 'You are in' page appear
        """
        pass

    def test_002_navigate_away_or_close_x_you_are_in_page(self):
        """
        DESCRIPTION: Navigate away or Close [x] 'You are in' page
        EXPECTED: - App closed
        """
        pass
