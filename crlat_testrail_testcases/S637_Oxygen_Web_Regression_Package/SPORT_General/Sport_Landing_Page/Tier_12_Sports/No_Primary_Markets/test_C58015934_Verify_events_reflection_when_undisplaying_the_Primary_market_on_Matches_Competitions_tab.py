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
class Test_C58015934_Verify_events_reflection_when_undisplaying_the_Primary_market_on_Matches_Competitions_tab(Common):
    """
    TR_ID: C58015934
    NAME: Verify events reflection when undisplaying the  Primary market on 'Matches'/'Competitions' tab
    DESCRIPTION: This test case verifies events reflection when undisplaying the  Primary market on 'Matches'/'Competitions' tab.
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
    PRECONDITIONS: - Updates on 'Matches' and 'Competitions' tab are received via 'push'
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Sport Landing page
    PRECONDITIONS: 3. Choose the 'Matches' tab
    """
    keep_browser_open = True

    def test_001_verify_events_displaying_on_the_page(self):
        """
        DESCRIPTION: Verify events displaying on the page
        EXPECTED: - Events that have Primary Market with the following attributes and outcomes are displayed:
        EXPECTED: - "marketTemplateName" = |Match Betting|, |Money Line|, |Match Winner|, etc. depends on Sport
        EXPECTED: - "dispSortName"='MR' or dispSortName='HH'
        EXPECTED: - Selections from the Primary Market are displayed on the event card
        EXPECTED: - Event is received in <EventToOutcomeForClass> response from the SS
        EXPECTED: - Primary and NOT Primary markets are received in <EventToOutcomeForClass> response from the SS
        """
        pass

    def test_002__trigger_the_undisplaying_of_the_primary_market_for_event_that_contains_not_primary_market_as_well_dont_refresh_the_page_verify_the_event_reflection(self):
        """
        DESCRIPTION: * Trigger the undisplaying of the Primary Market for event that contains Not Primary Market as well.
        DESCRIPTION: * Don't refresh the page.
        DESCRIPTION: * Verify the event reflection.
        EXPECTED: - General Event card is replaced by Outright card that contains the following elements:
        EXPECTED: - Event Name
        EXPECTED: - Navigation arrow
        EXPECTED: - 'Odds Card' header disappears in case the primary market is undisplayed for the last event in a 'Type' accordion
        EXPECTED: - Updates for the market with the parameter 'displayed': "N" is received in 'push'
        """
        pass

    def test_003__navigate_to_the_competitions_tab_tier_2_only_repeat_the_steps_1_2(self):
        """
        DESCRIPTION: * Navigate to the 'Competitions' tab (Tier 2 only).
        DESCRIPTION: * Repeat the steps 1-2.
        EXPECTED: 
        """
        pass
