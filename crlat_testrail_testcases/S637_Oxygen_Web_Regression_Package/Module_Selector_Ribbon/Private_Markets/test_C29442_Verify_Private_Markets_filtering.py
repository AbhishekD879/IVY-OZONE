import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29442_Verify_Private_Markets_filtering(Common):
    """
    TR_ID: C29442
    NAME: Verify Private Markets filtering
    DESCRIPTION: This test case verifies Private Markets filtering to be displayed within 'Your Enhanced Multiples' tab/section
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1.  User should be logged in
    PRECONDITIONS: 2. **accountFreebets?freebetTokenType=ACCESS** request is used in order to get a private market for particular user after a page refresh or navigating to Homepage from any other page and **user** request is used to get private market after login(open Dev tools -> Network ->XHR tab)
    PRECONDITIONS: 3.  User should be eligible for one or more private enhanced market offers
    PRECONDITIONS: 4.  Private market offers should be active (not expired)
    PRECONDITIONS: 5.  Odds format is Fractional
    PRECONDITIONS: 6.  To view event information on SS use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?includeRestricted=true&translationLang=LL
    PRECONDITIONS: *   XXX - event ID (can be get from response - in Console XHR tab or from UAT)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: For setting private markets use the link:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+Setup+and+Use+Private+Markets?preview=/36604227/36604228/HowToSetupAndUsePrivateMarkets%20.pdf
    PRECONDITIONS: Place a bet on the configured event by any user with sufficient funds for bet placement and then verify Private Markets on the Homepage. Private Markets will be shown for all users which placed a bet on the configured event.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_verify_your_enhancedmarkets_tabsection(self):
        """
        DESCRIPTION: Verify 'Your Enhanced Markets' tab/section
        EXPECTED: *   'Your Enhanced Markets' tab is present and selected by default **for mobile/tablet**
        EXPECTED: *   'Your Enhanced Markets' section is present at the top of the page (below Hero Header) **for mobile/tablet**
        EXPECTED: *   All eligible private markets and associated selections are shown
        EXPECTED: *   All private market sections expanded by default
        """
        pass

    def test_003_verify_markets_list(self):
        """
        DESCRIPTION: Verify Markets list
        EXPECTED: *   Markets from pre-match events are shown
        EXPECTED: *   If market is from event that has **isStarted="true"** attribute it should contain **isMarketBetInRun="true"** attribute on market level to be shown
        EXPECTED: *   Markets without outcomes are hidden from the front-end
        """
        pass
