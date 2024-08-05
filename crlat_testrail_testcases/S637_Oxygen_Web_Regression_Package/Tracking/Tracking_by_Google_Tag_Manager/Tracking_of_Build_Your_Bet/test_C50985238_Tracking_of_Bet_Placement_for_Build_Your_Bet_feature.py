import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.5_a_side
@vtest
class Test_C50985238_Tracking_of_Bet_Placement_for_Build_Your_Bet_feature(Common):
    """
    TR_ID: C50985238
    NAME: Tracking of Bet Placement for 'Build Your Bet'  feature
    DESCRIPTION: This test case verifies GA tracking during bet placement from 'BYB' QuickBet on Football EDP
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Log in the app
    PRECONDITIONS: 3. Navigate to the Football event details page that has 'Build Your Bet'/'Bet Builder' tab
    PRECONDITIONS: 4. Click/Tap on 'Build Your Bet'/'Bet Builder' tab
    PRECONDITIONS: 5. Add a selection(s) (bet) from any 'Build Your Bet' market accordion to the 'BYB' dashboard
    PRECONDITIONS: 6. Click/Tap on 'Odds/place Bet' button to add selection(s) to QuickBet
    PRECONDITIONS: 7. Browser console should be opened
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

    def test_001__add_the_stake_in_the_byb_quickbet_clicktap_on_the_place_bet_button(self):
        """
        DESCRIPTION: * Add the stake in the 'BYB' QuickBet.
        DESCRIPTION: * Click/Tap on the 'Place bet' button.
        EXPECTED: 'Bet receipt' is displayed
        """
        pass

    def test_002_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type **'dataLayer'** in browser's console and verify GA tracking record
        EXPECTED: The following record with corresponding parameters is present in data layer:
        EXPECTED: * event: "trackEvent"
        EXPECTED: * eventCategory: "quickbet"
        EXPECTED: * eventAction: "place bet"
        EXPECTED: * eventLabel: "success"
        EXPECTED: * betID: "O/XXXXX/XXXXX"
        EXPECTED: * betType: "Multiple"
        EXPECTED: * location: "yourcall"
        EXPECTED: * ecommerce.purchase.actionField:
        EXPECTED: * 'id': "O/XXXXX/XXXXX"
        EXPECTED: * 'revenue': "XX.XX" - **Potential Returns value**
        EXPECTED: * ecommerce.purchase.products:
        EXPECTED: * 'price': <<STAKE AMOUNT>>
        EXPECTED: * 'category': '<<EVENT CATEGORY>>'
        EXPECTED: * 'variant': '<<EVENT TYPE>>'
        EXPECTED: * 'brand': 'Bet builder'
        EXPECTED: * 'dimension60': '<<EVENT>>'
        EXPECTED: * 'dimension62': <<IN PLAY STATUS>> - **'1' for Live events, '0' for Pre-match**
        EXPECTED: * 'dimension63': <<CUSTOMER BUILT>> - **if it's YourCall Bet set '1' in other cases '0'**
        EXPECTED: * 'dimension66': <<BET LINES>>,
        EXPECTED: * 'dimension67': <<BET ODDS>>,
        EXPECTED: * 'dimension89': <<FORMATION TYPE>> - **undefined**
        EXPECTED: * 'dimension90': <<BET ID>>
        """
        pass
