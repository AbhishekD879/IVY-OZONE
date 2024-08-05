import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C26268029_Verify_that_redirection_from_Gaming_pages_back_to_a_website_under_maintenance_is_correct(Common):
    """
    TR_ID: C26268029
    NAME: Verify that redirection from Gaming pages back to a website under maintenance is correct
    DESCRIPTION: This test case verifies that user is redirected only to Maintenance page through any redirection link of Gaming pages once Maintenance mode is turned ON for the Oxygen App.
    PRECONDITIONS: 0) Maintenance Page should be created in CMS > Maintenance
    PRECONDITIONS: 1) Maintenance Page should have its Validity Period 'End' Date value set to a future date.
    PRECONDITIONS: 2) Maintenance Page should be disabled: enabled = false
    PRECONDITIONS: 3) Maintenance Page should have a '.png' image being set/uploaded through 'Filename' field
    PRECONDITIONS: 4) CMS > Maintenance Page > #PAGE_NAME should be opened (where #PAGE_NAME is the name of page created in step 0)
    PRECONDITIONS: *Test case should be run on PROD environment.*
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load 'Oxygen' application
        EXPECTED: 
        """
        pass

    def test_002_in_oxygen_application_clicktap_on_gaming_icon(self):
        """
        DESCRIPTION: In 'Oxygen' application, click/tap on 'Gaming' icon
        EXPECTED: User is redirected to 'https://gaming.coral.co.uk' page
        """
        pass

    def test_003_in_cms__maintenance_page__page_name_set_enabled__true_and_click_save_changes_with_additional_confirmation_through_yes_button_in_modal_window(self):
        """
        DESCRIPTION: In CMS > Maintenance Page > #PAGE_NAME, set enabled = true and click 'Save Changes' with additional confirmation through 'Yes' button in modal window
        EXPECTED: Notification about maintenance page changes being saved is shown
        """
        pass

    def test_004_on_httpsgamingcoralcouk_of_the_oxygen_application_desktop_click_on_in_play_link_label_under_the_quick_links_list_of_the_left_menumobiletablet_tap_on_sandwich_icon__sports__in_play_options(self):
        """
        DESCRIPTION: On 'https://gaming.coral.co.uk' of the Oxygen application:
        DESCRIPTION: -
        DESCRIPTION: Desktop: click on 'In-Play' link-label under the 'QUICK LINKS' list of the left menu
        DESCRIPTION: Mobile/Tablet: tap on 'Sandwich' icon > 'SPORTS' > 'IN-PLAY' options
        EXPECTED: Screen refresh/redirection is done
        EXPECTED: Splash image set through CMS is shown to user
        EXPECTED: User is redirected to 'maintenance' page.
        """
        pass
