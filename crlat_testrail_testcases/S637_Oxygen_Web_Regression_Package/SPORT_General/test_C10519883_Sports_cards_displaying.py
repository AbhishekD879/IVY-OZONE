import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C10519883_Sports_cards_displaying(Common):
    """
    TR_ID: C10519883
    NAME: <Sports> cards displaying
    DESCRIPTION: This test case verifies <sports> cards UI
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have sports cards with next configurations:
    PRECONDITIONS: 1) Prematch event
    PRECONDITIONS: 2) In-play prematch event (rawIsOffCode="-" or rawIsOffCode="N", drilldownTagNames="EVFLAG_BL")
    PRECONDITIONS: 3) In-play live event (rawIsOffCode="Y", drilldownTagNames="EVFLAG_BL")
    PRECONDITIONS: 4) Outright live event (eventSortCode:"TNMT", rawIsOffCode="Y", drilldownTagNames="EVFLAG_BL")
    PRECONDITIONS: - You should be on a <Sport> landing page > Matches tab in application
    """
    keep_browser_open = True

    def test_001_verify_prematch_cards_displaying(self):
        """
        DESCRIPTION: Verify prematch cards displaying
        EXPECTED: - 'Favorite' icon at the top left corner (shown if enabled in CMS > System Configuration > Structure > Favorites)
        EXPECTED: - 'WATCH' label at the top left corner after the 'Favorite' icon (shown if stream enabled)
        EXPECTED: - Event start time and day next to the 'Favorite' icon (or 'WATCH' if applicable) in format HH:MM dd mmm (e.g 21:15 05 Aug, only if event starts today 'dd mmm' is replaced with 'Today') next to the 'Favorite' or 'WATCH' label
        EXPECTED: - 'XX MORE >' markets link at the top right corner where XX - amount of all active markets-1 market that is displayed (if event has only 1 active market - link is not displayed)
        EXPECTED: - Teams names one under another are displayed at the bottom left corner
        EXPECTED: - ODDS buttons are displayed at the bottom right corner
        EXPECTED: NOTE: Favorite icon is applicable to Football only
        """
        pass

    def test_002_go_to_in_play_tab_and_verify_cards_displaying(self):
        """
        DESCRIPTION: Go to 'In-Play' tab and verify cards displaying
        EXPECTED: - 'Favorite' icon at the top left corner (shown if enabled in CMS > System Configuration > Structure > Favorites)
        EXPECTED: - 'WATCH' label at the top left corner next to the 'Favorite' icon (shown if stream enabled)
        EXPECTED: - 'LIVE' label at the top left corner next to the 'Favorite' icon (shown if event has started)
        EXPECTED: - 'WATCH LIVE' label at the top left corner next to the 'Favorite' icon (shown if event has started and has stream enabled)
        EXPECTED: - 'XX MORE >' markets link at the top right corner where XX - amount of all active markets-1 market that is displayed (if event has only 1 active market - link is not displayed)
        EXPECTED: - Teams names one under another are displayed at the bottom left corner
        EXPECTED: - ODDS buttons are displayed at the bottom right corner
        EXPECTED: NOTE: Favorite icon is applicable to Football only
        """
        pass

    def test_003_go_to_sport_landing_page__in_play_tab_with_outright_event_and_verify_card_displaying(self):
        """
        DESCRIPTION: Go to <Sport> landing page > In-Play tab with outright event and verify card displaying
        EXPECTED: - 'LIVE' label at the top left corner (shown if event has started)
        EXPECTED: - Event name is displayed below the 'LIVE' label (if event has not started - name is centered) with ">" arrow
        """
        pass
