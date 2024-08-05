import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.bet_history_open_bets
@vtest
class Test_C11508492_GA_Tracking_start_editing_the_acca(Common):
    """
    TR_ID: C11508492
    NAME: GA Tracking: start editing the acca
    DESCRIPTION: This test case verifies GA tracking of the start of editing the acca
    PRECONDITIONS: - Edit My Acca GA Tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=GA&title=Edit+my+acca
    PRECONDITIONS: - You should be logged in
    PRECONDITIONS: - You should have an acca bet made
    PRECONDITIONS: - You should be on 'Cash Out' or 'Open Bets' tab'
    """
    keep_browser_open = True

    def test_001___tap_edit_my_acca_button__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: - Tap 'EDIT MY ACCA' button
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: dataLayer.push{
        EXPECTED: 'betInPlay' : '<<IN PLAY STATUS>>',
        EXPECTED: 'betType' : '<<BET TYPE>>',
        EXPECTED: 'customerBuilt' : '<<CUSTOMER BUILT>>',
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventAction' : 'start',
        EXPECTED: 'eventCategory' : 'edit acca',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'location' : '<<LOCATION>>'
        EXPECTED: }
        """
        pass
