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
class Test_C75996_NOT_valid_after_OX982Enabled_Disabled_Mobile_and_Tablet_Banners(Common):
    """
    TR_ID: C75996
    NAME: [NOT valid after OX98.2]Enabled/Disabled Mobile and Tablet Banners
    DESCRIPTION: This test case verifies banner setting 'Disabled'
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   [BMA-16377 (CMS: Player Bets banner on Bet Receipt)][1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-16377
    DESCRIPTION: *   [BMA-17456 (CMS: Add the ability to configure bet receipt banner for tablet with small resolution)] [2]
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-17456
    PRECONDITIONS: At least one Mobile and Tablet Bet Receipt banners are created
    PRECONDITIONS: User is logged in to Oxygen application.
    PRECONDITIONS: User has enough funds to place a bet
    """
    keep_browser_open = True

    def test_001_navigate_to_cms_page_with_mobile_player_bets_banners_for_bet_receipt_banners___bet_receipt_banners(self):
        """
        DESCRIPTION: Navigate to CMS page with Mobile Player Bets banners for bet receipt (Banners -> Bet Receipt Banners)
        EXPECTED: Page with list of banners for mobile is opened
        """
        pass

    def test_002_open_settings_page_for_any_banner_by_clicking_on_its_name_e_g_for_football_england_premier_league_tick_disabled_checkbox_and_save_change(self):
        """
        DESCRIPTION: Open settings page for any banner by clicking on its name (e. g. for Football England Premier League), tick 'Disabled' checkbox and save change
        EXPECTED: Change is saved
        """
        pass

    def test_003_load_oxygen_application_on_mobile_and_place_a_bet_on_event_from_football_england_premier_league(self):
        """
        DESCRIPTION: Load Oxygen application on Mobile and place a bet on event from Football England Premier League
        EXPECTED: Bet Receipt is shown with Player bets clickable banner in the footer
        """
        pass

    def test_004_in_cms_navigate_to_settings_page_for_previously_changed_banner_untick_disabled_checkbox_and_save_change(self):
        """
        DESCRIPTION: In CMS navigate to settings page for previously changed banner, untick 'Disabled' checkbox and save change
        EXPECTED: Change is saved
        """
        pass

    def test_005_load_oxygen_application_on_mobile_and_place_a_bet_on_event_from_football_england_premier_league(self):
        """
        DESCRIPTION: Load Oxygen application on Mobile and place a bet on event from Football England Premier League
        EXPECTED: Bet Receipt is shown without Player bets clickable banner in the footer
        """
        pass

    def test_006_navigate_to_cms_page_with_tablet_player_bets_banners_for_bet_receipt_banners___bet_receipt_banners_tablet(self):
        """
        DESCRIPTION: Navigate to CMS page with Tablet Player Bets banners for bet receipt (Banners -> Bet Receipt Banners Tablet)
        EXPECTED: Page with list of banners for Tablet is opened
        """
        pass

    def test_007_front_end_part_is_not_implemented_yet_repeat_steps_2_5_for_tablet_banners(self):
        """
        DESCRIPTION: FRONT END PART IS NOT IMPLEMENTED YET: Repeat steps #2-5 for Tablet banners
        EXPECTED: 
        """
        pass
