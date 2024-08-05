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
class Test_C76619_NOT_valid_after_OX982Change_Delete_Mobile_and_Tablet_Banners_for_League(Common):
    """
    TR_ID: C76619
    NAME: [NOT valid after OX98.2]Change/Delete Mobile and Tablet Banners for League
    DESCRIPTION: This test case verifies changing and deleting of Mobile and Tablet Bet Receipt banners for league
    DESCRIPTION: Jira ticket:
    DESCRIPTION: BMA-16377 (CMS: Player Bets banner on Bet Receipt)
    DESCRIPTION: BMA-17456 (CMS: Add the ability to configure bet receipt banner for tablet with small resolution)
    PRECONDITIONS: User is logged in to Oxygen application.
    PRECONDITIONS: At least two Mobile and Tablet Bet Receipt banners with uploaded images are created
    PRECONDITIONS: User has enough funds to place a bet
    """
    keep_browser_open = True

    def test_001_navigate_to_cms_page_with_leagues(self):
        """
        DESCRIPTION: Navigate to CMS page with Leagues
        EXPECTED: Page with list of leagues is opened
        """
        pass

    def test_002_click_by_any_existing_league_name(self):
        """
        DESCRIPTION: Click by any existing league name
        EXPECTED: - Page with League details is opened
        EXPECTED: - Names of uploaded banners are shown in 'Mobile Banner' and 'Tablet Benner' fields
        """
        pass

    def test_003_select_another_mobile_banner_from_the_list_of_banners_save_changes(self):
        """
        DESCRIPTION: Select another Mobile banner from the list of banners. Save changes
        EXPECTED: Changes are saved w/o any errors
        """
        pass

    def test_004_load_oxygen_application_on_mobile_and_place_a_bet_on_event_from_league_with_changed_banner(self):
        """
        DESCRIPTION: Load Oxygen application on Mobile and place a bet on event from league with changed banner
        EXPECTED: Bet Receipt is shown with new Player bets clickable banner
        """
        pass

    def test_005_navigate_to_cms_page_with_mobile_bet_receipt_banners_banners__bet_receipt_banners_mobile(self):
        """
        DESCRIPTION: Navigate to CMS page with Mobile Bet Receipt Banners (Banners ->
        DESCRIPTION: Bet Receipt Banners Mobile)
        EXPECTED: Page with list of banners is opened
        """
        pass

    def test_006_delete_banner_selected_in_step_3(self):
        """
        DESCRIPTION: Delete banner selected in step #3
        EXPECTED: Banner is deleted
        """
        pass

    def test_007_load_oxygen_application_on_mobile_and_place_a_bet_on_event_from_the_same_league_with_deleted_banner(self):
        """
        DESCRIPTION: Load Oxygen application on Mobile and place a bet on event from the same league with deleted banner
        EXPECTED: Bet Receipt is shown without Player bets clickable banner
        """
        pass

    def test_008_front_end_part_is_not_implemented_yet_repeat_steps_1_7_for_tablet_banners(self):
        """
        DESCRIPTION: FRONT END PART IS NOT IMPLEMENTED YET: Repeat steps #1-7 for Tablet banners
        EXPECTED: 
        """
        pass
