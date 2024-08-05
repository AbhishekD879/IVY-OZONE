import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.promotions_banners_offers
@vtest
class Test_C157254_NOT_valid_after_OX982Priority_of_Bet_Receipt_Bannerss_displaying(Common):
    """
    TR_ID: C157254
    NAME: [NOT valid after OX98.2]Priority of Bet Receipt Banners's displaying
    DESCRIPTION: This test case verifies priority of Bet Receipt Banners's displaying
    PRECONDITIONS: User is logged in to CMS.
    PRECONDITIONS: The following leagues are created in CMS->Leagues:
    PRECONDITIONS: * <General League>  with CategoryId:0, TypeId:0, SSCategoryCode:'General' and RedirectionUrl: e.g. 'promotions/betandgetclubweek12'
    PRECONDITIONS: * <Specific Sport> (e.g. Football) with CategoryId:16 , TypeId:0, SSCategoryCode:'FOOTBALL' and RedirectionUrl: e.g. 'football'
    PRECONDITIONS: * <Specific League in Sport> (e.g. Premier League for Football) with CategoryId:16 , TypeId:442, SSCategoryCode:'FOOTBALL' and RedirectionUrl: e.g. 'football/live'
    PRECONDITIONS: Each league uses banner with unique image.
    PRECONDITIONS: User is logged in to Oxygen application.
    PRECONDITIONS: User has enough funds to place a bet.
    """
    keep_browser_open = True

    def test_001_place_a_bet_on_event_from_not_configured_sportleague_in_cms_eg_basketball(self):
        """
        DESCRIPTION: Place a bet on event from not configured sport/league in CMS (e.g. basketball)
        EXPECTED: Bet Receipt is shown with clickable banner set for <General League>
        """
        pass

    def test_002_tap_banner(self):
        """
        DESCRIPTION: Tap banner
        EXPECTED: Page from 'Redirection URL' filed  for configured <General League> is opened
        """
        pass

    def test_003_place_a_bet_on_event_from_configured_sport_but_not_league_in_cms_eg_football_and_not_premier_league(self):
        """
        DESCRIPTION: Place a bet on event from configured sport, but not league in CMS (e.g. Football and not Premier League)
        EXPECTED: Bet Receipt is shown with clickable banner set for <Specific Sport>
        """
        pass

    def test_004_tap_banner(self):
        """
        DESCRIPTION: Tap banner
        EXPECTED: Page from 'Redirection URL' filed  for configured <Specific Sport> is opened
        """
        pass

    def test_005_place_a_bet_on_event_from_configured_sport_with_league_in_cms_eg_football_and_premier_league(self):
        """
        DESCRIPTION: Place a bet on event from configured sport with league in CMS (e.g. Football and Premier League)
        EXPECTED: Bet Receipt is shown with clickable banner set for <Specific League in Sport>
        """
        pass

    def test_006_tap_banner(self):
        """
        DESCRIPTION: Tap banner
        EXPECTED: Page from 'Redirection URL' filed  for configured <Specific League> is opened
        """
        pass
