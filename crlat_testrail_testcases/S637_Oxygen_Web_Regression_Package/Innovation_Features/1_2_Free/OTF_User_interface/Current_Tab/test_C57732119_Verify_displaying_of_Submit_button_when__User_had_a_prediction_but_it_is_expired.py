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
class Test_C57732119_Verify_displaying_of_Submit_button_when__User_had_a_prediction_but_it_is_expired(Common):
    """
    TR_ID: C57732119
    NAME: Verify displaying of 'Submit' button when - User had a prediction but it is expired
    DESCRIPTION: This test case verifies displaying of 'Submit' button when - User had a prediction but it is expired
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: for Qubit version (deprecated) https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: for Oxygen version: https://confluence.egalacoral.com/display/SPI/1-2-Free+configurations?preview=/106397589/106397584/1-2-Free%20CMS%20configurations.pdf
    PRECONDITIONS: 1. User is logged In
    PRECONDITIONS: 2. User have prediction for Game #1
    PRECONDITIONS: 3. New Game #2 has started
    """
    keep_browser_open = True

    def test_001_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: - New Game #2 displayed
        EXPECTED: - 'Submit' button is **active**
        EXPECTED: - Arrows **displayed** on scores
        """
        pass