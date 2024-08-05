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
class Test_C13802091_Highlights_Carousel__renaming_in_CMS(Common):
    """
    TR_ID: C13802091
    NAME: Highlights Carousel - renaming in CMS
    DESCRIPTION: This test case verifies renaming of Highlights Carousels to include special characters.
    PRECONDITIONS: - To see what CMS and TI is in use, type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_go_to_the_cms_for_your_environment__sport_pages__homepage__highlights_carousel_and_click_create_highlights_carousel_button(self):
        """
        DESCRIPTION: Go to the: CMS (for your environment) > Sport Pages > Homepage > Highlights Carousel and click 'Create Highlights Carousel' button.
        EXPECTED: 'New Highlights Carousel' page is opened.
        """
        pass

    def test_002_type_a_title_for_the_new_highlights_carousel_including_someall_of_the_following_special_characters________plus_______(self):
        """
        DESCRIPTION: Type a Title for the new Highlights Carousel including some/all of the following special characters: ; : # @ & - + ( ) ! ? ' $ £
        EXPECTED: Entered special characters are displayed in 'Title' text field.
        """
        pass

    def test_003_fill_in_other_required_fields_set_valid_typeid_or_eventids_make_sure_date_fields_are_valid_check_off_active_checkbox_and_click_create_button(self):
        """
        DESCRIPTION: Fill in other required fields (set valid TypeID or EventID(s), make sure date fields are valid), check off 'Active' checkbox and click 'Create' button.
        EXPECTED: The new Highlights Carousel was successfully created and it is displayed in Sport Pages > Homepage > Highlights Carousel with 'Enabled' checkbox checked off.
        """
        pass

    def test_004_re_login_into_cms_and_go_to_the_sport_pages__homepage__highlights_carousel(self):
        """
        DESCRIPTION: Re-login into CMS and go to the: Sport Pages > Homepage > Highlights Carousel.
        EXPECTED: Just created Highlights Carousel is still displayed with the correct title and all other fields, populated on the previous steps.
        """
        pass

    def test_005_click_on_just_created_highlights_carousel_and_change_the_title_field_on_the_opened_page_click_save_changes_button_and_confirm_the_action(self):
        """
        DESCRIPTION: Click on just created Highlights Carousel and change the Title field on the opened page. Click 'Save changes' button and confirm the action.
        EXPECTED: The changes were successfully saved.
        """
        pass

    def test_006_launch_coralladbrokes_application_on_mobile_and_tablet_and_go_to_the_home_page_that_is_opened_by_default(self):
        """
        DESCRIPTION: Launch Coral/Ladbrokes application on Mobile and Tablet and go to the Home page (that is opened by default).
        EXPECTED: Highlights Carousel created on the previous steps is displayed on the Home page with the correct name and it contains valid events (based on TypeID or EventID(s) set on step 3).
        """
        pass
