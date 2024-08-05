import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C76025_NOT_valid_after_OX982_Add_Delete_Mobile_Banner(Common):
    """
    TR_ID: C76025
    NAME: [NOT valid after OX98.2] Add/Delete Mobile Banner
    DESCRIPTION: This test case verifies adding and displaying of new Bet Receipt Banner on Mobile
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   [BMA-16377 (CMS: Player Bets banner on Bet Receipt)][1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-16377
    PRECONDITIONS: User is logged in to CMS:
    PRECONDITIONS: User is logged in to Oxygen application.
    PRECONDITIONS: User has enough funds to place a bet
    PRECONDITIONS: Leagues for Bet Receipt Banner are created
    """
    keep_browser_open = True

    def test_001_navigate_to_cms_page_with_player_bets_banners_for_bet_receipt_banners__bet_receipt_banners_mobile(self):
        """
        DESCRIPTION: Navigate to CMS page with Player Bets banners for bet receipt (Banners ->
        DESCRIPTION: Bet Receipt Banners Mobile)
        EXPECTED: *  Page with list of banners is opened
        EXPECTED: *  ' + Create Bet Receipt Banner Mobile' button is present
        """
        pass

    def test_002_add_new_banner_via_clicking_plus_create_bet_receipt_banner_mobile_button_enter_all_required_data_and_save_it(self):
        """
        DESCRIPTION: Add new banner via clicking '+ Create Bet Receipt Banner Mobile' button, enter all required data and save it
        EXPECTED: Banner appears in the banners list
        """
        pass

    def test_003_navigate_to_cms_page_with_leagues_select_any_league_without_banner(self):
        """
        DESCRIPTION: Navigate to CMS page with Leagues, select any league without banner
        EXPECTED: 'Select...' is shown in 'Banner' field
        """
        pass

    def test_004_tap_arrow_button_in_mobile_banner_field(self):
        """
        DESCRIPTION: Tap arrow button in 'Mobile Banner' field
        EXPECTED: Banner created in step #2 is shown in dropdown list
        """
        pass

    def test_005_select_banner_and_save_changes(self):
        """
        DESCRIPTION: Select banner and save changes
        EXPECTED: Banner is saved for league
        """
        pass

    def test_006_in_oxygen_application_place_a_bet_on_event_from_league_for_which_banner_was_added(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from league for which banner was added
        EXPECTED: Bet Receipt is shown with Player bets clickable banner
        """
        pass

    def test_007_navigate_to_cms_page_with_player_bets_banners_for_bet_receipt_banners__bet_receipt_banners_mobile(self):
        """
        DESCRIPTION: Navigate to CMS page with Player Bets banners for bet receipt (Banners ->
        DESCRIPTION: Bet Receipt Banners Mobile)
        EXPECTED: *  Page with list of banners is opened
        EXPECTED: *  'delete bet receipt banner' link is shown
        """
        pass

    def test_008_select_any_banner_and_click_delete_bet_receipt_banner_link(self):
        """
        DESCRIPTION: Select any banner and click 'delete bet receipt banner' link
        EXPECTED: Selected banner is removed from banner list
        """
        pass

    def test_009_navigate_to_cms_page_with_leagues_select_any_league_without_banner(self):
        """
        DESCRIPTION: Navigate to CMS page with Leagues, select any league without banner
        EXPECTED: 'Select...' is shown in 'Mobile Banner' field
        """
        pass

    def test_010_tap_arrow_button_in_mobile_banner_field(self):
        """
        DESCRIPTION: Tap arrow button in 'Mobile Banner' field
        EXPECTED: Banner removed in step #8 is NOT shown in dropdown list
        """
        pass
