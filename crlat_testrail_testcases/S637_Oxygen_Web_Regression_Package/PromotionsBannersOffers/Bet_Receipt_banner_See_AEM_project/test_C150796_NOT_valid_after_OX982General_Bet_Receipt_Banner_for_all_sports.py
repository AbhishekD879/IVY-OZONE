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
class Test_C150796_NOT_valid_after_OX982General_Bet_Receipt_Banner_for_all_sports(Common):
    """
    TR_ID: C150796
    NAME: [NOT valid after OX98.2]General Bet Receipt Banner for all sports
    DESCRIPTION: This test case verifies general Bet Receipt Banner for all sports
    PRECONDITIONS: * User is logged in to CMS.
    PRECONDITIONS: * At least one banner with uploaded image is created.
    PRECONDITIONS: * User is logged in to Oxygen application.
    PRECONDITIONS: * User has enough funds to place a bet.
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Verification of editing of Type ID and Redirection URL fields and deleting for league are covered in TC https://gci.testrail.com/index.php?/cases/view/76617
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

    def test_003_enter_the_following_information_to_the_fields__enter_league_title__in_type_id_and_category_id_fields_enter_0_value__select_previously_created_needed_banner_from_dropdown_in_mobile_banner_field__in_redirection_url_field_enter_one_of_the_following__name_of_page_in_oxygen_application_e_g_promotions_that_will_be_shown_in_the_end_of_url_for_opened_page_after_redirection__external_link_eg_casino__link_to_the_specific_game_eg_roulette__leave_betbuilder_url_and_league_url_fields_emptysave_changes(self):
        """
        DESCRIPTION: Enter the following information to the fields:
        DESCRIPTION: - enter league title;
        DESCRIPTION: - in 'Type Id' and 'Category Id' fields enter '0' value;
        DESCRIPTION: - select previously created needed banner from dropdown in 'Mobile Banner' field;
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

    def test_005_enter_general_in_ss_category_code_fieldsave_changes(self):
        """
        DESCRIPTION: Enter 'GENERAL' in 'SS Category Code' field.
        DESCRIPTION: Save changes.
        EXPECTED: Changes are saved without any errors
        """
        pass

    def test_006_in_oxygen_application_place_a_bet_on_event_from_sportleague_that_doesnt_have_specific_banner_configured(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from sport/league that doesn't have specific banner configured
        EXPECTED: Bet Receipt is shown with clickable banner
        """
        pass

    def test_007_tap_banner(self):
        """
        DESCRIPTION: Tap banner
        EXPECTED: * Page from 'Redirection URL' field for created in step #3 sport league is opened
        EXPECTED: * In case of redirection to external Coral related page (not Oxygen application) user is logged in
        """
        pass
