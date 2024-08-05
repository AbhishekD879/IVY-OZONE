import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C64569855_Verify_popups_like_oddboosts_freebets_timeline_after_launching_of_My_Bets_on_casino_game_overlay(Common):
    """
    TR_ID: C64569855
    NAME: Verify popups like oddboosts, freebets, timeline after launching of My Bets on casino game overlay.
    DESCRIPTION: Verify popups like oddboosts, freebets, timeline after launching of My Bets on casino game overlay.
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * User should be logged in Gaming Window.
    PRECONDITIONS: * User should have offers like oddboosts, freebets
    PRECONDITIONS: * Timeline/Coralpulse splash page is enabled in CMS
    PRECONDITIONS: Note: Applies to only Mobile Web
    """
    keep_browser_open = True

    def test_001_launch_any_casino_game(self):
        """
        DESCRIPTION: Launch any casino game
        EXPECTED: * User redirects to particular gaming page ex: Roulette page
        EXPECTED: * User able to see 'sports' icon on EZNav panel(header) in gaming page
        """
        pass

    def test_002_tap_sports_icon_from_eznav_panel(self):
        """
        DESCRIPTION: Tap 'sports' icon from ezNav panel
        EXPECTED: * User launches 'MyBets' overlay & displays below tabs:
        EXPECTED: Cashout (if available)
        EXPECTED: Openbets
        EXPECTED: Settledbets
        """
        pass

    def test_003_observe_whether_user_receiving_popups_related_to_offers_splash_pages(self):
        """
        DESCRIPTION: Observe whether user receiving popups related to offers, splash pages
        EXPECTED: * No popups received
        """
        pass
