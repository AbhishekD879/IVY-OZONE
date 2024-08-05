import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C9621398_Greyhounds_displaying_Winning_Distances_and_Trap_Challenges_section(Common):
    """
    TR_ID: C9621398
    NAME: Greyhounds: displaying "Winning Distances" and "Trap Challenges" section
    DESCRIPTION: This test case verifies that "Winning Distances" and "Trap Challenges" section is not displayed on the GH landing page.
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have Greyhounds events with next configurations:
    PRECONDITIONS: **Event configuration for "Winning Distance" section**
    PRECONDITIONS: 1) Class "Greyhounds - Specials"
    PRECONDITIONS: 2) Type "Winning Distances"
    PRECONDITIONS: 3) Event is active, configured to be displayed today and not started
    PRECONDITIONS: 4) Event has active market with selections (try 'To Win' market template)
    PRECONDITIONS: **Event configuration for "Trap Challenges" section**
    PRECONDITIONS: 1) Class "Greyhounds - Specials"
    PRECONDITIONS: 2) Type "Trap Challenges"
    PRECONDITIONS: 3) Event is active, configured to be displayed today and not started
    PRECONDITIONS: 4) Event has active market with selections (try 'Other Markets' market template)
    PRECONDITIONS: - You should be on a Greyhounds landing page/Today tab (or other tabs - 'Next Races', 'Tomorrow' or 'Future').
    PRECONDITIONS: **The full request to check data:**
    PRECONDITIONS: **Ladbrokes**
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/198,201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T14:17:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: **Coral**
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-26T00:00:00.000Z&simpleFilter=event.startTime:lessThan:2020-08-27T00:00:00.000Z&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T13:35:30.000Z&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_verify_winning_distances_section(self):
        """
        DESCRIPTION: Verify "Winning Distances" section
        EXPECTED: "Winning Distances" section is not displayed
        """
        pass

    def test_002_verify_trap_challenges_section(self):
        """
        DESCRIPTION: Verify "Trap Challenges" section
        EXPECTED: "Trap Challenges" section is not displayed
        """
        pass
