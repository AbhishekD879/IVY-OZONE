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
class Test_C874376_Verify_adding_and_displaying_new_Promotions(Common):
    """
    TR_ID: C874376
    NAME: Verify adding and displaying new Promotions
    DESCRIPTION: This test case verifies adding and displaying new Promotion
    DESCRIPTION: To ed
    DESCRIPTION: AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_order=asc&group_id=739507
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/promotions
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: **Following fields should not be populated** :
    PRECONDITIONS: 1) Show on Competitions
    PRECONDITIONS: 2) Promotion ID
    PRECONDITIONS: 3) OB promotion ID
    PRECONDITIONS: 4) Include VIP Levels(only if you want to see promo on all types of users)
    PRECONDITIONS: 5) Event-level flag
    PRECONDITIONS: 6) Market-level flag
    PRECONDITIONS: 7) Overlay BET NOW button url(only if it is not needed)
    """
    keep_browser_open = True

    def test_001_go_to_promotion_section_on_cms(self):
        """
        DESCRIPTION: Go to 'Promotion' section on CMS
        EXPECTED: 'Promotion' section is opened
        """
        pass

    def test_002_click_on_promotion(self):
        """
        DESCRIPTION: Click on 'Promotion'
        EXPECTED: 'Promotion' Page is opened
        """
        pass

    def test_003_click_plus_create_promotion_button(self):
        """
        DESCRIPTION: Click "+ Create Promotion" button
        EXPECTED: "Create Promotion" page is opened
        """
        pass

    def test_004_verify_the_content_of_create_promotion_page(self):
        """
        DESCRIPTION: Verify the content of "Create Promotion" page
        EXPECTED: The following elements are present on "Create Promotion" page:
        EXPECTED: * 'Title' text field;
        EXPECTED: * 'Promo Key' text field;
        EXPECTED: * 'Show on Competitions' text field;
        EXPECTED: * 'Short Description' text field;
        EXPECTED: * 'Description' text field;
        EXPECTED: * 'Targeted Promos' section with following elements:
        EXPECTED: - 'Promotion ID' text field;
        EXPECTED: - 'OB promotion ID' text field;
        EXPECTED: * 'Use uploaded image' radio button;
        EXPECTED: * 'Main image' autofill input;
        EXPECTED: * 'Change File' button;
        EXPECTED: * 'Remove File' button;
        EXPECTED: * 'Use image URL' radio button;
        EXPECTED: * 'Image URL' text field;
        EXPECTED: * 'Validity Period Start' and 'Validity Period End' date fields;
        EXPECTED: * 'Is Signposting Promotion' checkbox;
        EXPECTED: * 'Event-level flag' text field;
        EXPECTED: * 'Market-level flag' text field;
        EXPECTED: * 'Overlay BET NOW' text field;
        EXPECTED: * 'Include VIP levels' text field;
        EXPECTED: * 'Opt In Request ID' text field;
        EXPECTED: * 'Show To Customer' drop-down selector;
        EXPECTED: * 'Category' drop-down selector;
        EXPECTED: * 'T&C' text field;
        EXPECTED: * 'Popup Title' text field;
        EXPECTED: * 'Popup Text' text field;
        EXPECTED: * 'Create Promotion' button
        """
        pass

    def test_005_populate_all_fields_with_valid_data_and_click_the_create_promotion_button_apart_from_those_mentioned_in_pre_conditions(self):
        """
        DESCRIPTION: Populate all fields with valid data and click the "Create Promotion" button
        DESCRIPTION: (!) Apart from those, mentioned in pre-conditions.
        EXPECTED: * New Promotion <offer_name> created
        EXPECTED: * Success message appears
        EXPECTED: * Promotion edit page is opened
        """
        pass

    def test_006_verify_the_image_upload_fields(self):
        """
        DESCRIPTION: Verify the image upload fields
        EXPECTED: * 'Main Image' field is present(for new Promotion)/'File Name' (for editing Promotion)
        EXPECTED: * 'Use Image URL' checkbox is present for 'Image URL' option
        EXPECTED: * 'Use Image URL' checkbox is unchecked by default
        EXPECTED: * 'Image URL ' field is present
        """
        pass

    def test_007_upload_an_image_for_the_promotion_using_the_main_imagefile_name__field_and_click_on_on_save_button(self):
        """
        DESCRIPTION: Upload an image for the Promotion using the 'Main Image'/'File Name'  field and click on on "Save" button
        EXPECTED: * Image is uploaded
        EXPECTED: * Success message appears
        """
        pass

    def test_008_navigate_to_promotions_page_on_oxygen_app(self):
        """
        DESCRIPTION: Navigate to 'Promotions' page on Oxygen app
        EXPECTED: * 'Promotions' page is opened
        EXPECTED: * Just added Promotions is shown on 'Promotions' page
        EXPECTED: * Promotion is displayed within correct uploaded image
        EXPECTED: * All data is displayed according to CMS
        """
        pass

    def test_009_navigate_to_the_relevant_promotion_in_the_cms_and_check_use_image_url_checkbox(self):
        """
        DESCRIPTION: Navigate to the relevant Promotion in the CMS and check 'Use Image URL' checkbox
        EXPECTED: * Promotion edit page is opened
        EXPECTED: * 'Use Image URL' checkbox is checked
        """
        pass

    def test_010_upload_an_image_to_the_image_url__field_using_the_absolute_url_and_click_on_save_button(self):
        """
        DESCRIPTION: Upload an image to the 'Image URL ' field using the Absolute URL and click on 'Save' button
        EXPECTED: * Image is uploaded
        EXPECTED: * Success message appears
        """
        pass

    def test_011_repeat_step_7(self):
        """
        DESCRIPTION: Repeat step 7
        EXPECTED: 
        """
        pass
