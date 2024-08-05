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
class Test_C76616_NOT_valid_after_OX982Uploading_images_for_Mobile_and_Tablet_Bet_Receipt_banners(Common):
    """
    TR_ID: C76616
    NAME: [NOT valid after OX98.2]Uploading images for Mobile and Tablet Bet Receipt banners
    DESCRIPTION: This test case verifies uploading and displaying images for Bet Receipt Banners
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   [BMA-16377 (CMS: Player Bets banner on Bet Receipt)][1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-16377
    DESCRIPTION: *   [BMA-17456 (CMS: Add the ability to configure bet receipt banner for tablet with small resolution
    PRECONDITIONS: At least one Mobile and Tablet Bet Receipt Banner without uploaded image are created
    PRECONDITIONS: User is logged in to Oxygen application.
    PRECONDITIONS: User has enough funds to place a bet
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_on_mobile_and_place_a_bet_on_event_from_league_with_mobile_banner_without_uploaded_image(self):
        """
        DESCRIPTION: Load Oxygen application on Mobile and place a bet on event from league with Mobile banner without uploaded image
        EXPECTED: Bet Receipt is shown without Player bets clickable banner
        """
        pass

    def test_002_navigate_to_cms_page_with_mobile_player_bets_banners_for_bet_receipt_banners___bet_receipt_banners_mobile(self):
        """
        DESCRIPTION: Navigate to CMS page with Mobile Player Bets banners for bet receipt (Banners -> Bet Receipt Banners Mobile)
        EXPECTED: *  Page with list of banners is opened
        EXPECTED: *   ' + Create Bet Receipt Banner Mobile' button is present
        """
        pass

    def test_003_open_settings_page_for_banner_without_uploaded_image_by_clicking_on_its_name(self):
        """
        DESCRIPTION: Open settings page for banner without uploaded image by clicking on its name
        EXPECTED: *  Settings page is opened
        """
        pass

    def test_004_verify_the_image_upload_fields(self):
        """
        DESCRIPTION: Verify the image upload fields
        EXPECTED: * 'Filename' field is present
        EXPECTED: * 'Use Image URL' checkbox is present for 'Image URL' option
        EXPECTED: * 'Use Image URL' checkbox is unchecked by default
        EXPECTED: *  'Image URL' field is present
        """
        pass

    def test_005_upload_an_image_for_the_mobile_player_bets_banners_using_the_filename_field(self):
        """
        DESCRIPTION: Upload an image for the Mobile Player Bets banners using the 'Filename' field
        EXPECTED: Image is uploaded
        """
        pass

    def test_006_click_on_save_button(self):
        """
        DESCRIPTION: Click on "Save" button
        EXPECTED: Success message appears
        """
        pass

    def test_007_load_oxygen_application_on_mobile_and_place_a_bet_on_event_from_league_with_uploaded_banner(self):
        """
        DESCRIPTION: Load Oxygen application on Mobile and place a bet on event from league with uploaded banner
        EXPECTED: Bet Receipt is shown with Player bets clickable banner in the footer
        """
        pass

    def test_008_in_cms_update_the_url_with_new_one_for_the_same_banner_save_changes(self):
        """
        DESCRIPTION: In CMS update the URL with new one for the same banner. Save changes
        EXPECTED: Changes are saved without any errors
        """
        pass

    def test_009_load_oxygen_application_on_mobile_and_place_a_bet_on_event_from_league_with_changed_banner(self):
        """
        DESCRIPTION: Load Oxygen application on Mobile and place a bet on event from league with changed banner
        EXPECTED: Bet Receipt is shown with new Player bets clickable banner
        """
        pass

    def test_010_navigate_to_the_relevant_mobile_player_bets_banner_in_the_cms(self):
        """
        DESCRIPTION: Navigate to the relevant Mobile Player Bets banner in the CMS
        EXPECTED: Mobile Player Bets banner edit page is opened
        """
        pass

    def test_011_check_the_use_image_url_checkbox(self):
        """
        DESCRIPTION: Check the 'Use Image URL' checkbox
        EXPECTED: 'Use Image URL' checkbox is checked
        """
        pass

    def test_012_upload_an_image_to_the_image_url_field_using_the_absolute_url(self):
        """
        DESCRIPTION: Upload an image to the 'Image URL' field using the Absolute URL
        EXPECTED: Image is uploaded
        """
        pass

    def test_013_click_on_save_button(self):
        """
        DESCRIPTION: Click on "Save" button
        EXPECTED: Success message appears
        """
        pass

    def test_014_load_oxygen_application_on_mobile_and_place_a_bet_on_event_from_league_with_uploaded_banner(self):
        """
        DESCRIPTION: Load Oxygen application on Mobile and place a bet on event from league with uploaded banner
        EXPECTED: * Bet Receipt is shown with new Player bets clickable banner
        EXPECTED: * All data is displayed according to CMS
        EXPECTED: * Player bets banner is displayed within image uploaded by using 'Image URL' field
        """
        pass

    def test_015_front_end_part_is_not_implemented_yet_repeat_steps_1_7_for_tablet_banners(self):
        """
        DESCRIPTION: FRONT END PART IS NOT IMPLEMENTED YET: Repeat steps #1-7 for Tablet banners
        EXPECTED: 
        """
        pass
