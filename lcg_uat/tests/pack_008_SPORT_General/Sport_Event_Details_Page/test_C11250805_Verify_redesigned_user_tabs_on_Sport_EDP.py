import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.crl_tst2  # Coral only, test case is not applicable for Ladbrokes has no "Markets","My Bets"  tabs
@pytest.mark.crl_stg2
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C11250805_Verify_redesigned_user_tabs_on_Sport_EDP(BaseBetSlipTest):
    """
    TR_ID: C11250805
    NAME: Verify redesigned user tabs on <Sport> EDP
    DESCRIPTION: This test case verifies the appearance of new redesigned user tabs "Markets", "My Bets" on <Sport> EDP when configured in CMS.
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: Note: User tabs like 'Markets'/'My Bets' are available for all sports. If configured in CMS, they appear on UI redesigned, if not, the old design of tabs is shown (2 buttons of yellow and blue colors)
    PRECONDITIONS: CMS configuration is described here: https://ladbrokescoral.testrail.com/index.php?/cases/view/10852269
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User has positive balance
    PRECONDITIONS: - User is on any <sport> EDP (and has NOT yet placed a bet for any of its selections)
    PRECONDITIONS: - New redesigned tabs are already configured in CMS
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        in_play_event=True)[0]
            self.__class__.eventID = event['event']['id']
            outcomes = next(((market['market'].get('children')) for market in event['event'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('No outcomes available')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id = list(selection_ids.values())[0]
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.__class__.eventID = event_params.event_id
            self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.site.login(username=tests.settings.betplacement_user)
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')

    def test_001_check_the_area_below_the_scoreboards(self):
        """
        DESCRIPTION: Check the area below the scoreboards
        EXPECTED: There are no tabs available like "Markets","My Bets" (on the area where 'watch' icon is placed)
        """
        has_markets_my_bets = self.site.sport_event_details.has_markets_my_bets_tab()
        self.assertFalse(has_markets_my_bets, msg='2 tabs "Markets","My Bets" appear below the scoreboards')

    def test_002_place_a_bet_for_any_selection_on_this_page(self):
        """
        DESCRIPTION: Place a bet for any selection on this page
        EXPECTED: Bet is successfully placed
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id, timeout=30)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()

    def test_003_refresh_the_page_and_check_if_tabs_appeared(self):
        """
        DESCRIPTION: Refresh the page and check if tabs appeared
        EXPECTED: - After page refresh 2 tabs "Markets","My Bets" appear below the scoreboards (along with 'watch' icon, if in-play event) with white text name on dark blue background
        EXPECTED: - User can switch between the tabs
        EXPECTED: - "My Bets" tab has counter of the bets placed
        EXPECTED: - The active tab looks underlined
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide(timeout=30)
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')
        has_markets_my_bets = self.site.sport_event_details.has_markets_my_bets_tab()
        self.assertTrue(has_markets_my_bets, msg='2 tabs "Markets","My Bets" not appear below the scoreboards')
        self.assertTrue(has_markets_my_bets)
