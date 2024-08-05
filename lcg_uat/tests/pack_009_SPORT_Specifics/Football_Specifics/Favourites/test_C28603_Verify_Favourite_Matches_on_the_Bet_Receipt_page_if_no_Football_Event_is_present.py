import pytest

import tests
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
@pytest.mark.football
@pytest.mark.favourites
@pytest.mark.bet_receipt
@pytest.mark.bet_placement
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.login
@vtest
class Test_C28603_Verify_Favourite_Matches_on_the_Bet_Receipt_page_if_no_Football_Event_is_present(BaseBetSlipTest):
    """
    TR_ID: C28603
    NAME: Verify Favourite Matches on the Bet Receipt page if no Football Event is present
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Not Football Event
        """
        if self.cms_config.get_widgets(widget_type='favourites')[0]['disabled']:
            raise CmsClientException('"Favourites" widget is disabled in CMS')

        if tests.settings.backend_env == 'prod':
            self.__class__.selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.backend.ti.tennis.category_id)
            self._logger.info(f'*** Found Tennis event with selection ids "{self.selection_ids}"')
            self.__class__.team1 = list(self.selection_ids.keys())[0]
        else:
            event_params = self.ob_config.add_tennis_event_to_autotest_trophy()
            self.__class__.team1, self.__class__.selection_ids = event_params.team1, event_params.selection_ids

    def test_002_login(self):
        """
        DESCRIPTION: Login
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_003_add_selection_to_the_bet_slip_via_deeplink(self):
        """
        DESCRIPTION: Add selection to the Bet Slip
        EXPECTED: Selection is added
        EXPECTED: Bet Slip page is open
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_004_enter_stake_in_stake_field_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and tap 'Bet Now' button
        EXPECTED: Bet is placed successfully
        EXPECTED: Bet Receipt is shown
        EXPECTED: 'Favourite matches' functionality isn't included
        EXPECTED: 'Add all to favourites' button isn't included
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

        has_match_center = self.site.bet_receipt.has_match_center
        self.assertFalse(has_match_center, msg="'Add all to favourites' and match center section are displayed")
