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
class Test_C50972777_Tracking_of_adding_selection_to_QuickBet_from_BYB_dashboard(Common):
    """
    TR_ID: C50972777
    NAME: Tracking of adding selection to 'QuickBet'  from 'BYB' dashboard
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of adding selection to 'QuickBet'  from 'BYB' dashboard
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Log in the app
    PRECONDITIONS: 3. Navigate to the Football event details page that has 'Build Your Bet'/'Bet Builder' tab
    PRECONDITIONS: 4. Click/Tap on 'Build Your Bet'/'Bet Builder' tab
    PRECONDITIONS: 5. Add a selection(s) (bet) from any 'Build Your Bet' market accordion to the 'BYB' dashboard
    PRECONDITIONS: 6. Browser console should be opened
    PRECONDITIONS: **Build Your Bet configuration:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> YourCallIconsAndTabs -> enableTab: True
    PRECONDITIONS: - Banach leagues are added and enabled for BYB in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for BYB’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response) (in case checking the tracking for 'Player Bets' markets)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91091847
    """
    keep_browser_open = True

    def test_001_clicktap_place_bet_button_on_byb_dashboard(self):
        """
        DESCRIPTION: Click/Tap 'Place bet' button on 'BYB' dashboard
        EXPECTED: 'BYB' QuickBet is initiated
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following record with corresponding parameters is present in data layer:
        EXPECTED: * event: "trackEvent"
        EXPECTED: * eventCategory: "quickbet"
        EXPECTED: * eventAction: "add to quickbet"
        EXPECTED: * eventLabel: "success"
        EXPECTED: * ecommerce.add.products:
        EXPECTED: * 'name': '<<EVENT NAME>>'
        EXPECTED: * 'category': '<<EVENT CATEGORY>>'
        EXPECTED: * 'variant': '<<EVENT TYPE>>'
        EXPECTED: * brand: "Bet builder"
        EXPECTED: * 'dimension60': '<<EVENT>>'
        EXPECTED: * 'dimension62': <<IN PLAY STATUS>> - **'1' for Live events, '0' for Pre-match**
        EXPECTED: * 'dimension63': <<CUSTOMER BUILT>>
        EXPECTED: * 'dimension64': '<<LOCATION>>' - **YourCall**
        EXPECTED: * 'dimension65': '<<MODULE>>' - **Bet Builder**
        EXPECTED: * 'dimension86': <<ODDSBOOST>>
        EXPECTED: * 'dimension87': <<STREAM ACTIVE>>
        EXPECTED: * 'dimension89': <<FORMATION TYPE>> - **undefined**
        EXPECTED: * 'quantity': 1
        """
        pass
