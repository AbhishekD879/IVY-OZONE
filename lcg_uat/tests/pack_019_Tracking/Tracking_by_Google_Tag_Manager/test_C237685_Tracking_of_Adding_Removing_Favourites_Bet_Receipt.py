import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.google_analytics
@pytest.mark.favourites
@pytest.mark.bet_placement
@pytest.mark.low
@pytest.mark.other
@pytest.mark.login
@vtest
class Test_C237685_Tracking_Of_Adding_Removing_Favourites_Bet_Receipt(BaseBetSlipTest, BaseDataLayerTest):
    """
    TR_ID: C237685
    VOL_ID: C9690261
    NAME: Tracking of Adding/Removing Favourites on Bet Receipt
    """
    keep_browser_open = True

    def test_000_create_test_event(self):
        """
        DESCRIPTION: Create event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID, self.__class__.team1, self.__class__.selection_ids =\
            event_params.event_id, event_params.team1, event_params.selection_ids
        self.__class__.event_name = self.team1 + ' v ' + event_params.team2

    def test_001_login(self):
        """
        DESCRIPTION: Login to application
        EXPECTED: User is logged in
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_add_selection_to_betslip(self):
        """
        DESCRIPTION: Add selection to BetSlip
        EXPECTED: Selection is added, counter is 1
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_003_place_bet(self):
        """
        DESCRIPTION: Place bet on added selection
        EXPECTED: Bet is placed
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_004_add_event_to_favourites_from_bet_receipt(self):
        """
        DESCRIPTION: Click on 'star' icon on Bet Receipt
        EXPECTED: 'Star' icon is highlighted
        """
        self.site.bet_receipt.match_center.add_all_to_favourites_button.click()
        self.assertTrue(self.site.bet_receipt.match_center.add_all_to_favourites_button.is_selected(),
                        msg='"Add all to favourites" button is not selected')

    def test_005_check_data_layer_response_for_adding_to_favourites_on_bet_receipt(self):
        """
        DESCRIPTION: Check data layer response for adding to favourites on bet receipt
        EXPECTED: 'action' must be 'add', 'location' must be 'betslip receipt'
        """
        self.check_data_layer_favourites_response(object_key='eventAction', action='add', location='betslip receipt')

    def test_006_remove_event_from_favourites(self):
        """
        DESCRIPTION: Remove event from Favourites
        EXPECTED: Star icon is not highlighted
        """
        self.site.bet_receipt.match_center.add_all_to_favourites_button.click()
        self.assertFalse(self.site.bet_receipt.match_center.add_all_to_favourites_button.is_selected(expected_result=False),
                         msg='"Add all to favourites" button is still selected')

    def test_007_check_data_layer_response_for_removing_from_favourites_on_football_page(self):
        """
        DESCRIPTION: Check data layer response for removing from favourites on betreceipt
        EXPECTED: 'action' must be 'remove', 'location' must be 'betslip receipt'
        """
        self.check_data_layer_favourites_response(object_key='eventAction', action='remove', location='betslip receipt')
