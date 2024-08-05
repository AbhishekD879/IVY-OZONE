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
class Test_C57732105_Verify_displaying_of_YAI_page_Desktop__Tablet(Common):
    """
    TR_ID: C57732105
    NAME: Verify displaying of YAI page [Desktop / Tablet]
    DESCRIPTION: This test case verifies displaying of YAI page [Desktop / Tablet]
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. User is logged In
    PRECONDITIONS: 2. User Do not have a prediction yet
    """
    keep_browser_open = True

    def test_001_make_prediction_and_tap_on_submit_button(self):
        """
        DESCRIPTION: Make prediction and Tap on 'Submit' button
        EXPECTED: YAI page successfully opened and designed according to:
        EXPECTED: https://app.zeplin.io/project/5c471d82d6094838624e7232/dashboard?seid=5d11f9c15259df7049a86104
        """
        pass

    def test_002_tap_on_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap on 'Add to Betslip' button
        EXPECTED: - Upsell selections successfully added to Betslip
        EXPECTED: - YAI should NOT close
        """
        pass

    def test_003_tap_on_add_to_betslip_button_again_for_previously_added_market(self):
        """
        DESCRIPTION: Tap on 'Add to Betslip' button again for previously added market
        EXPECTED: - Upsell selections should NOT duplicates
        EXPECTED: - YAI should NOT close
        """
        pass

    def test_004_tap_on_back_to_betting_button(self):
        """
        DESCRIPTION: Tap on 'Back to Betting' button
        EXPECTED: - User redirects to the previously opened page
        """
        pass
