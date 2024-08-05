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
class Test_C50155076_Tracking_of_adding_selection_to_QuickBet_from_5_A_Side_section(Common):
    """
    TR_ID: C50155076
    NAME: Tracking of adding selection to 'QuickBet'  from '5-A-Side' section
    DESCRIPTION: This test case verifies GA tracking during adding selection to 'QuickBet'  from '5-A-Side' section on Football EDP
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Log in the app
    PRECONDITIONS: 3. Navigate to the Football event details page that has '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap on '5-A-Side' tab
    PRECONDITIONS: 5. Click/Tap 'Build' button
    PRECONDITIONS: 6. Click/Tap on **+** button on '5-A-Side' overlay and select one specific player
    PRECONDITIONS: 7. Click/Tap on another available **+** button on '5-A-Side' overlay and select one specific player (which could combine with the previous one)
    PRECONDITIONS: 8. Browser console should be opened
    PRECONDITIONS: **5-A-Side configuration:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91091847
    """
    keep_browser_open = True

    def test_001_clicktap_place_bet_button_on_5_a_side_overlay(self):
        """
        DESCRIPTION: Click/Tap 'Place bet' button on '5-A-Side' overlay
        EXPECTED: '5-A-Side' QuickBet is initiated
        """
        pass

    def test_002_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type **'dataLayer'** in browser's console and verify GA tracking record
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: * event: "trackEvent"
        EXPECTED: * eventCategory: "quickbet"
        EXPECTED: * eventAction: "add to quickbet"
        EXPECTED: * eventLabel: "success"
        EXPECTED: * ecommerce.add.products:
        EXPECTED: * 'name': '<<EVENT NAME>>'
        EXPECTED: * 'category': '<<EVENT CATEGORY>>'
        EXPECTED: * 'variant': '<<EVENT TYPE>>'
        EXPECTED: * 'brand': "5-A-Side"
        EXPECTED: * 'dimension60': '<<EVENT>>'
        EXPECTED: * 'dimension62': <<IN PLAY STATUS>>
        EXPECTED: * 'dimension63': '<<CUSTOMER BUILT>>'
        EXPECTED: * 'dimension64': '<<LOCATION>>'
        EXPECTED: * 'dimension65': '<<MODULE>>'
        EXPECTED: * 'dimension86': '<<ODDSBOOST>>'
        EXPECTED: * 'dimension87': '<<STREAM ACTIVE>>'
        EXPECTED: * 'dimension89': '<<FORMATION TYPE>>'
        EXPECTED: * 'quantity': '1'
        EXPECTED: where **<FORMATION TYPE>** is the name of picked Formation configured in CMS (CMS > BYB > 5-A-Side > choose/add necessary formation)
        """
        pass
