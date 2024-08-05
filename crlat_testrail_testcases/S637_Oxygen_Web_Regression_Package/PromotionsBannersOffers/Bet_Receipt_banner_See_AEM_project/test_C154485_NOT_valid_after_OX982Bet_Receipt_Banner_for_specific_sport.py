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
class Test_C154485_NOT_valid_after_OX982Bet_Receipt_Banner_for_specific_sport(Common):
    """
    TR_ID: C154485
    NAME: [NOT valid after OX98.2]Bet Receipt Banner for specific sport
    DESCRIPTION: This test case verifies general Bet Receipt Banner for specific sport
    PRECONDITIONS: * User is logged in to CMS.
    PRECONDITIONS: * At least one banner with uploaded image is created.
    PRECONDITIONS: * User is logged in to Oxygen application.
    PRECONDITIONS: * User has enough funds to place a bet.
    PRECONDITIONS: Note: Verification of editing of Type ID and Redirection URL fields and deleting for league are covered in TC https://gci.testrail.com/index.php?/cases/view/76617
    PRECONDITIONS: [Guide for Bet Receipt banners in CMS] [1].
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/Guide+for+Bet+Receipt+banners+in+CMS
    """
    keep_browser_open = True

    def test_001_navigate_to_cms_page_with_leagues(self):
        """
        DESCRIPTION: Navigate to CMS page with Leagues
        EXPECTED: * Page with list of leagues is opened
        EXPECTED: * ' + Create League' button is present
        """
        pass

    def test_002_click_plus_create_league_button(self):
        """
        DESCRIPTION: Click '+ Create League' button.
        EXPECTED: 'Create a new League' window is opened
        """
        pass

    def test_003_enter_the_following_information_to_the_fields____enter_league_title____in_type_id__field_enter_0_value__in_category_id_field_enter_category_id_of_needed_sport_eg_16_for_football__select_prevously_created_needed_banner_from_dropdown_in_mobile_banner_field__in_redirection_url_field_enter_one_of_the_following__name_of_page_in_oxygen_application_e_g_promotions_that_will_be_shown_in_the_end_of_url_for_opened_page_after_redirection__external_link_eg_casino__link_to_the_specific_game_eg_roulette__leave_betbuilder_url_and_league_url_fields_emptysave_changes(self):
        """
        DESCRIPTION: Enter the following information to the fields:
        DESCRIPTION: *    enter league title;
        DESCRIPTION: *    in 'Type Id'  field enter '0' value;
        DESCRIPTION: - in 'Category Id' field enter category id of needed sport (e.g. 16 for football);
        DESCRIPTION: - select prevously created needed banner from dropdown in 'Mobile Banner' field;
        DESCRIPTION: - in 'Redirection URL' field enter one of the following:
        DESCRIPTION: - name of page in Oxygen application (e. g. promotions) that will be shown in the end of URL for opened page after redirection
        DESCRIPTION: - external link (e.g. Casino)
        DESCRIPTION: - link to the specific game (e.g. Roulette)
        DESCRIPTION: - leave 'BetBuilder URL' and 'League Url' fields empty.
        DESCRIPTION: Save changes.
        EXPECTED: * Changes are saved without any errors
        EXPECTED: * Created configuration is shown in 'Leagues' list
        """
        pass

    def test_004_click_by_league_title_of_created_in_step_3_league(self):
        """
        DESCRIPTION: Click by league title of created in step #3 league
        EXPECTED: League details page is opened
        """
        pass

    def test_005_enter_sport_code_eg_football_in_ss_category_code_fieldsave_changes(self):
        """
        DESCRIPTION: Enter sport code (e.g. 'FOOTBALL') in 'SS Category Code' field.
        DESCRIPTION: Save changes.
        EXPECTED: Changes are saved without any errors
        """
        pass

    def test_006_in_oxygen_application_place_a_bet_on_event_from_sport_with_the_same_category_id_as_for_sport_league_created_in_step_3(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from sport with the same category id as for sport league created in step #3
        EXPECTED: Bet Receipt is shown with clickable banner set for sport league created in step #3
        """
        pass

    def test_007_tap_banner(self):
        """
        DESCRIPTION: Tap banner
        EXPECTED: * Page from 'Redirection URL' field for created in step #3 sport league is opened
        EXPECTED: * In case of redirection to external Coral related page (not Oxygen application) user is logged in
        """
        pass

    def test_008_navigate_to_cms_page_with_leagues_select_sport_league_created_in_step_3_and_change_category_id_enter_id_of_any_other_sportsave_changes(self):
        """
        DESCRIPTION: Navigate to CMS page with Leagues, select sport league created in step #3 and change Category Id (enter id of any other sport).
        DESCRIPTION: Save changes
        EXPECTED: Changes are saved without any errors
        """
        pass

    def test_009_in_oxygen_application_place_a_bet_on_event_from_sport_with_the_same_category_id_as_for_sport_league_edited_in_step_8(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from sport with the same category id as for sport league edited in step #8
        EXPECTED: Bet Receipt is shown with the same clickable banner
        """
        pass

    def test_010_tap_banner(self):
        """
        DESCRIPTION: Tap banner
        EXPECTED: * Page from 'Redirection URL' field for created in step #3 sport league is opened
        EXPECTED: * In case of redirection to external Coral related page (not Oxygen application) user is logged in
        """
        pass

    def test_011_in_oxygen_application_place_a_bet_on_event_from_sport_with_the_old_category_id_that_was_set_for_league_in_step_2(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from sport with the old category id that was set for league in step #2
        EXPECTED: Bet Receipt is shown without clickable banner
        """
        pass
