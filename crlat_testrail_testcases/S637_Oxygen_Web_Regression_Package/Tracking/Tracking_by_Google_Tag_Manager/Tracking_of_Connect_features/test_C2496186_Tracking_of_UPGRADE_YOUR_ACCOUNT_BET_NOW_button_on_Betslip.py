import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C2496186_Tracking_of_UPGRADE_YOUR_ACCOUNT_BET_NOW_button_on_Betslip(Common):
    """
    TR_ID: C2496186
    NAME: Tracking of 'UPGRADE YOUR ACCOUNT & BET NOW' button on Betslip
    DESCRIPTION: 
    PRECONDITIONS: 1. The in-shop user should be logged in
    PRECONDITIONS: 2. A few bets should be added to the betslip
    PRECONDITIONS: The following credentials can be used for testing:
    PRECONDITIONS: Card: 5000000000992086
    PRECONDITIONS: PIN: 1234
    """
    keep_browser_open = True

    def test_001_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: * Betslip contains added selections
        EXPECTED: * UPGRADE YOUR ACCOUNT & BET NOW' button is displayed at the bottom
        """
        pass

    def test_002_tap_upgrade_your_account__bet_now_button(self):
        """
        DESCRIPTION: Tap UPGRADE YOUR ACCOUNT & BET NOW' button
        EXPECTED: In browser console -> enter 'dataLayer' in Console -> last Object contains:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'cta',
        EXPECTED: 'eventAction' : 'upgrade account'
        EXPECTED: 'eventLabel' : 'yes - upgrade Account'
        EXPECTED: });
        """
        pass
