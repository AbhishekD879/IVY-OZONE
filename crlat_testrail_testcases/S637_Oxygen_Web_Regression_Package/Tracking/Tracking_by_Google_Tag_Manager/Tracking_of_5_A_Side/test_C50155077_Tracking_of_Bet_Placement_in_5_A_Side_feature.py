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
class Test_C50155077_Tracking_of_Bet_Placement_in_5_A_Side_feature(Common):
    """
    TR_ID: C50155077
    NAME: Tracking of Bet Placement in 5-A-Side feature
    DESCRIPTION: This test case verifies GA tracking during 5-A-Side bet placement from 5-A-Side Betslip on Football EDP
    PRECONDITIONS: **5-A-Side configuration:**
    PRECONDITIONS: 1. Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: 2. Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: 3. Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: 4. 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: 5. Event is prematch (not live)
    PRECONDITIONS: 1. Navigate to event details page that has '5-A-Side' tab
    PRECONDITIONS: 2. Click/Tap on '5-A-Side' tab
    PRECONDITIONS: 3. Click 'Build' button
    PRECONDITIONS: 4. Click on + button on Pitch overlay and select one specific player
    PRECONDITIONS: 5. Click on another available + button on Pitch overlay and select one specific player (which could combine with the previous one)
    PRECONDITIONS: 6. Press/tap on 'Place bet' button
    """
    keep_browser_open = True

    def test_001__add_the_stake_in_the_5_a_side_betslip_presstap_place_bet_button(self):
        """
        DESCRIPTION: * Add the stake in the 5-A-Side Betslip
        DESCRIPTION: * Press/tap 'Place bet' button
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
        EXPECTED: * 'brand': '5-A-Side'
        EXPECTED: * 'dimension60': '<<EVENT>>'
        EXPECTED: * 'dimension62': <<IN PLAY STATUS>> - **'1' for Live events, '0' for Pre-match**
        EXPECTED: * 'dimension63': <<CUSTOMER BUILT>> - **if it's YourCall Bet set '1' in other cases '0'**
        EXPECTED: * 'dimension66': <<BET LINES>>,
        EXPECTED: * 'dimension67': <<BET ODDS>>,
        EXPECTED: * 'dimension89': <<FORMATION TYPE>> - **is the name of picked Formation configured in CMS (CMS > BYB > 5-A-Side > choose/add necessary formation)**
        EXPECTED: * 'dimension90': <<BET ID>>
        """
        pass
