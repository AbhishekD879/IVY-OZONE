import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C58066845_Verify_events_reflection_when_undisplaying_the_Primary_market_on_In_Play_page_tab(Common):
    """
    TR_ID: C58066845
    NAME: Verify events reflection when undisplaying the  Primary market on 'In-Play' page/tab
    DESCRIPTION: This test case verifies events reflection when undisplaying the  Primary market on 'In-Play' page/tab.
    DESCRIPTION: **Note: Football is out of scope**
    PRECONDITIONS: **OB Configurations:**
    PRECONDITIONS: The event should contain the following settings:
    PRECONDITIONS: - Primary Market (|Match Betting|, |Money Line|, |Match Winner|, etc. depends on Sport) with **dispSortName="HH"** or **dispSortName="MR"**
    PRECONDITIONS: where
    PRECONDITIONS: HH = Head to Head
    PRECONDITIONS: MR = Match Result
    PRECONDITIONS: - Not Primary Market (|Handicap Match Result|) with **dispSortName="MH"** or **dispSortName="WH"**
    PRECONDITIONS: where
    PRECONDITIONS: MH = Match Handicap Result (3 way)
    PRECONDITIONS: WH = Match Handicap Result (2 Way)
    PRECONDITIONS: To configure the Primary market for Sport use the following link https://confluence.egalacoral.com/display/SPI/Primary+Markets+and+dispSortNames+for+Different+Sports
    PRECONDITIONS: **CMS Configurations:**
    PRECONDITIONS: To configure filters for the particular sport use the following instruction:
    PRECONDITIONS: * Navigate to CMS -> Sports Pages -> Sports Categories -> choose <Sport e.g. Cricket>
    PRECONDITIONS: * Put the values in 'Disp sort name' field (MR, HH for Primary markets and MH, WH for NOT Primary markets)
    PRECONDITIONS: * Put the values in 'Primary markets' field (|Match Betting|, |Money Line|, |Match Winner|, etc. depends on Sport and |Handicap Match Result|)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To trigger live updates use the OB system https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Updates on on 'In-Play' page/tab are received via WS:
    PRECONDITIONS: * 'featured-sports' for 'Featured' tab/section and 'In-Play' modules
    PRECONDITIONS: * 'inplay-publisher' for 'In-Play' tab/section
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the 'In-Play' tab on the Homepage
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_events_with_primary_and_not_primary_markets_on_the_page(self):
        """
        DESCRIPTION: Verify displaying of events with Primary and Not Primary markets on the page
        EXPECTED: - Events that have Primary Market with the following attributes and outcomes are displayed:
        EXPECTED: - "marketTemplateName" = |Match Betting|, |Money Line|, |Match Winner|, etc. depends on Sport
        EXPECTED: - "dispSortName"='MR' or dispSortName='HH'
        EXPECTED: - Selections from the Primary Market are displayed on the event card
        EXPECTED: - Event is received in WS
        EXPECTED: - Only Primary market is received in WS
        """
        pass

    def test_002__trigger_the_undisplaying_of_the_primary_market_for_an_event_that_contains_not_primary_market_as_well_verify_the_event_reflection(self):
        """
        DESCRIPTION: * Trigger the undisplaying of the Primary Market for an event that contains Not Primary Market as well.
        DESCRIPTION: * Verify the event reflection.
        EXPECTED: - Event disappears from the page
        EXPECTED: - 'EVMKT' update by the market is received in WS
        EXPECTED: - 'Odds Card' header disappears in case the primary market is undisplayed for the last event in a 'Type' accordion
        """
        pass

    def test_003__refresh_the_page_verify_the_event_reflection(self):
        """
        DESCRIPTION: * Refresh the page.
        DESCRIPTION: * Verify the event reflection.
        EXPECTED: General Event card is replaced by Outright card that contains the following elements:
        EXPECTED: * Event Name
        EXPECTED: * Navigation arrow
        """
        pass

    def test_004_repeat_the_steps_1___3_for_the_following_pages_in_play_page___sport_tab_sports_landing_page___in_play_tab_sports_landing_page___matches_tab___in_play_module_homepage___in_play_module(self):
        """
        DESCRIPTION: Repeat the steps 1 - 3 for the following pages:
        DESCRIPTION: * 'In-Play' page -> 'Sport' tab
        DESCRIPTION: * Sports Landing page -> 'In-Play' tab
        DESCRIPTION: * Sports Landing page -> 'Matches' tab -> 'In-Play' module
        DESCRIPTION: * Homepage -> 'In-Play' module
        EXPECTED: 
        """
        pass
