import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C13802092_Surface_Bets__renaming_in_CMS(Common):
    """
    TR_ID: C13802092
    NAME: Surface Bets - renaming in CMS
    DESCRIPTION: This test case verifies renaming of Surface Bets to include special characters.
    PRECONDITIONS: - To see what CMS and TI is in use, type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_go_to_the_cms_for_your_environment__sport_pages__homepage__surface_bet_module_and_click_create_surface_bet_button(self):
        """
        DESCRIPTION: Go to the: CMS (for your environment) > Sport Pages > Homepage > Surface Bet Module and click 'Create Surface Bet' button.
        EXPECTED: 'New Surface Bet' page is opened.
        """
        pass

    def test_002_type_a_title_for_the_new_surface_bet_including_someall_of_the_following_special_characters________plus_______(self):
        """
        DESCRIPTION: Type a Title for the new Surface Bet including some/all of the following special characters: ; : # @ & - + ( ) ! ? ' $ £
        EXPECTED: Entered text value is displayed in 'Title' text field.
        """
        pass

    def test_003_type_a_content_for_the_new_surface_bet_including_someall_of_the_following_special_characters________plus_______(self):
        """
        DESCRIPTION: Type a Content for the new Surface Bet including some/all of the following special characters: ; : # @ & - + ( ) ! ? ' $ £
        EXPECTED: Entered text value is displayed in 'Content' text field.
        """
        pass

    def test_004_fill_in_other_required_fields_set_valid_eventids_selectionid_make_sure_date_fields_are_valid_check_off_enabled_displayed_on_highlights_tab_display_on_edp_checkboxes_and_click_create_button(self):
        """
        DESCRIPTION: Fill in other required fields (set valid EventID(s), SelectionID, make sure date fields are valid), check off 'Enabled', 'Displayed on Highlights tab', 'Display on EDP' checkboxes and click 'Create' button.
        EXPECTED: The new Surface Bet was successfully created and it is displayed in Sport Pages > Homepage > Surface Bet Module under 'Active Surface Bets' section and with 'Enabled'/'Highlights Tab'/'EDP' checkboxes checked off.
        """
        pass

    def test_005_re_login_into_cms_and_go_to_the_sport_pages__homepage__surface_bet_module(self):
        """
        DESCRIPTION: Re-login into CMS and go to the: Sport Pages > Homepage > Surface Bet Module.
        EXPECTED: Just created Surface Bet module is still displayed with the correct title and all other fields, populated on the previous steps.
        """
        pass

    def test_006_click_on_just_created_surface_bet_module_and_change_the_title_and_content_fields_on_the_opened_page_click_save_changes_button_confirm_the_action(self):
        """
        DESCRIPTION: Click on just created Surface Bet module and change the Title and Content fields on the opened page. Click 'Save Changes' button. Confirm the action.
        EXPECTED: The changes were successfully saved.
        """
        pass

    def test_007_launch_coralladbrokes_application_on_mobile_and_tablet(self):
        """
        DESCRIPTION: Launch Coral/Ladbrokes application on Mobile and Tablet.
        EXPECTED: Surface Bet module created on the previous steps is displayed on the Home page/Highlights, EDP page with the correct name and it contains valid selection (based on SelectionID set on the step 4).
        """
        pass
