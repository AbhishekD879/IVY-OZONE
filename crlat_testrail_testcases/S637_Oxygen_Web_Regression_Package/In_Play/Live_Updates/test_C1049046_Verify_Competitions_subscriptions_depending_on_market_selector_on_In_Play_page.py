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
class Test_C1049046_Verify_Competitions_subscriptions_depending_on_market_selector_on_In_Play_page(Common):
    """
    TR_ID: C1049046
    NAME: Verify Competitions subscriptions depending on market selector on In Play page
    DESCRIPTION: Verify competitions subscribed/unsubscribed depending on market selected in Market Selector
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose Football tab > 'Live Now' section/switcher
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To check Live Serv notifications open Dev tools -> Network tab -> WS tab -> Frames section -> choose ?EIO=3&transport=websocket record
    """
    keep_browser_open = True

    def test_001_tap_football_icon_in_in_play_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon in In Play ribbon
        EXPECTED: * 'Football' page is opened
        EXPECTED: * 'Live Now' sorting type is chosen
        EXPECTED: * Market Selector set to Match betting by default
        EXPECTED: * 42["subscribe", "IN_PLAY_SPORT_COMPETITION_CHANGED::16::LIVE_EVENT"] record in WS (Market is not specified)
        """
        pass

    def test_002_select_any_other_market_in_market_selector_eg_total_goals_overunder_15_and_verify_eio3transportwebsocket_record(self):
        """
        DESCRIPTION: Select any other market in Market Selector (e.g 'Total Goals Over/Under 1.5') and verify ?EIO=3&transport=websocket record
        EXPECTED: Unsubscribe message sent:
        EXPECTED: ["unsubscribe",
        EXPECTED: "IN_PLAY_SPORT_COMPETITION_CHANGED::16::LIVE_EVENT"]
        EXPECTED: Subscription message sent:
        EXPECTED: ["subscribe", "IN_PLAY_SPORT_COMPETITION_CHANGED::16::LIVE_EVENT::Total Goals Over/Under 1.5"]
        """
        pass

    def test_003_select_different_market_in_market_selector_eg_both_teams_to_score(self):
        """
        DESCRIPTION: Select different Market in Market Selector (e.g: 'Both Teams To Score')
        EXPECTED: *Unsubscribe message sent for previous Market:
        EXPECTED: ["unsubscribe", "IN_PLAY_SPORT_COMPETITION_CHANGED::16::LIVE_EVENT::Total Goals Over/Under 1.5"]
        EXPECTED: *Subscribe message sent for newly selected Market:
        EXPECTED: ["subscribe", "IN_PLAY_SPORT_COMPETITION_CHANGED::16::LIVE_EVENT::Both Teams To Score"]
        """
        pass

    def test_004_repeat_steps_1_5_on_sport___inplay(self):
        """
        DESCRIPTION: Repeat Steps 1-5 on <Sport> - InPlay
        EXPECTED: 
        """
        pass
