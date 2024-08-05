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
class Test_C57732104_Verify_view_of_Current_tab_Desktop__Tablet(Common):
    """
    TR_ID: C57732104
    NAME: Verify view of 'Current tab' [Desktop / Tablet]
    DESCRIPTION: This test case verifies view of 'Current tab' [Desktop]
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is NOT logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE' is available on Homepage / Football sports page
    PRECONDITIONS: 3. User Do NOT have a prediction yet
    """
    keep_browser_open = True

    def test_001_tap_on_play_1_2_free_quick_link_on_homepage__football_sports_page(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE' quick link on Homepage / Football sports page
        EXPECTED: User should see the Splash page
        EXPECTED: 'Current tab' is successfully opened and designed according to:
        EXPECTED: https://app.zeplin.io/project/5c471d82d6094838624e7232/dashboard?seid=5d11f9c15259df7049a86104
        EXPECTED: - Close button
        EXPECTED: - Expanded/Collapsed text from CMS (Static text-> **Splash page** -> Page Text)
        EXPECTED: - Submit (Static text-> Current page-> ctaText1)
        EXPECTED: - Events(CMS->Active game):
        EXPECTED: - Event number: *e.g. Match 1*
        EXPECTED: - Date of event: *e.g. 15:00 MON*
        EXPECTED: - Team name *Liverpool*
        EXPECTED: - Team kits
        EXPECTED: - Event TV icon *BBC*
        """
        pass

    def test_002_make_prediction_and_tap_on_submit_button(self):
        """
        DESCRIPTION: Make prediction and Tap on 'Submit' button
        EXPECTED: Prediction successfully made
        """
        pass

    def test_003_re_open_play_1_2_free(self):
        """
        DESCRIPTION: Re-open 'Play 1-2-FREE'
        EXPECTED: - Expanded/Collapsed text changed to 'You already entered...' from CMS (Static text-> **Сurrent week tab** -> Already played text)
        """
        pass
