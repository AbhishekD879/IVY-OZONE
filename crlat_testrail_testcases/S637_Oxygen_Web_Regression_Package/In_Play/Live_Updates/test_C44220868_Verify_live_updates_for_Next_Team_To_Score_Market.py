import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44220868_Verify_live_updates_for_Next_Team_To_Score_Market(Common):
    """
    TR_ID: C44220868
    NAME: Verify live updates for Next Team To Score Market
    DESCRIPTION: This test case verifies that live updates are received only for Next Team To Score markets that are visible on UI
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose any Sport
    PRECONDITIONS: 3. Select Football sport on Sports Ribbon
    PRECONDITIONS: 4. Select 'Next Team to Score' in Market selector
    PRECONDITIONS: 4. Make sure that there is event with primary market and few markets created by template 'Next Team to Score',  attributes is_off = 'Y' and Bet In Running (event attribute isStarted)
    PRECONDITIONS: 5. Open Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket
    PRECONDITIONS: 6. Open OB TI tool
    PRECONDITIONS: Note:
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: OB TI:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    """
    keep_browser_open = True

    def test_001_in_timake_price_updatessuspension_for_selection_from_market_next_team_to_score_with_the_lowest_displayordernote_this_market_is_displayed_on_in_play_page(self):
        """
        DESCRIPTION: In TI:
        DESCRIPTION: Make price updates/suspension for selection from market 'Next Team to Score' with the lowest displayOrder
        DESCRIPTION: NOTE: this market is displayed on In Play page
        EXPECTED: Changes are saved
        """
        pass

    def test_002_in_appcheck_updates_are_received_in_web_sockets__gt_eio3transportwebsocket(self):
        """
        DESCRIPTION: In App:
        DESCRIPTION: Check Updates are received in Web Sockets -&gt; ?EIO=3&transport=websocket
        EXPECTED: Price updates/suspension are received
        """
        pass

    def test_003_verify_updates_are_displayed_for_event(self):
        """
        DESCRIPTION: Verify updates are displayed for event
        EXPECTED: * If price update was received, new price is displayed within Odds button
        EXPECTED: * If suspension was received, Odds button is disabled
        """
        pass

    def test_004_in_timake_price_updatessuspension_for_selection_from_market_next_team_to_score_with_the_highest_or_higher_displayordernote_this_market_is_not_displayed_on_in_play_page(self):
        """
        DESCRIPTION: In TI:
        DESCRIPTION: Make price updates/suspension for selection from market 'Next Team to Score' with the highest or higher displayOrder
        DESCRIPTION: NOTE: this market is not displayed on In Play page
        EXPECTED: Changes are saved
        """
        pass

    def test_005_in_appcheck_updates_are_not_received_in_web_sockets__gt_eio3transportwebsocket(self):
        """
        DESCRIPTION: In App:
        DESCRIPTION: Check Updates are not received in Web Sockets -&gt; ?EIO=3&transport=websocket
        EXPECTED: Price updates/suspension are NOT received
        """
        pass
