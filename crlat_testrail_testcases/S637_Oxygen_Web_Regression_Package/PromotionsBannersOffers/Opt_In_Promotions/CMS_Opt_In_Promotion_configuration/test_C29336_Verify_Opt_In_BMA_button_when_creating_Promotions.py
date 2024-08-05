import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29336_Verify_Opt_In_BMA_button_when_creating_Promotions(Common):
    """
    TR_ID: C29336
    NAME: Verify Opt In BMA button when creating Promotions
    DESCRIPTION: This test case verifies Opt In BMA button option to description within CMS when creating Promotions only
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ (check CMS_ENDPOINT via devlog function)
    PRECONDITIONS: NOTE: For caching needs Akamai service is used on TST2/ STG environment, so after saving changes in CMS there clould be delay up to 5-10 mins before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_go_to_promotions_tab(self):
        """
        DESCRIPTION: Go to 'Promotions' tab
        EXPECTED: 'Promotions' section is opened
        """
        pass

    def test_003_add_a_few_promotions(self):
        """
        DESCRIPTION: Add a few Promotions
        EXPECTED: Promotions are added successfully
        """
        pass

    def test_004_tap_on_create_bma_button_into_description_section(self):
        """
        DESCRIPTION: Tap on 'Create bma button' into Description section
        EXPECTED: 'Opt In Button' is added to 'Create bma button'
        """
        pass

    def test_005_click_on_opt_in_button(self):
        """
        DESCRIPTION: Click on 'Opt In Button'
        EXPECTED: Pop-up to create Opt In button appears
        EXPECTED: Follow fields: URL, 'Text to display', 'Traget' can remain blank when creating an Opt In button
        """
        pass

    def test_006_click_on_ok_button_on_the_creation_opt_in_button_pop_up(self):
        """
        DESCRIPTION: Click on 'OK' button on the creation Opt In button pop-up
        EXPECTED: Opt In button is inputted into description
        """
        pass

    def test_007_check_opt_in_request_id_field_when_creating_a_promotion(self):
        """
        DESCRIPTION: Check Opt In Request ID field when creating a Promotion
        EXPECTED: Opt In Request ID field is dispalyed in CMS when creating Promotions
        """
        pass

    def test_008_enter_request_id_into_opt_in_request_id_field(self):
        """
        DESCRIPTION: Enter Request ID into Opt In Request ID field
        EXPECTED: 
        """
        pass

    def test_009_tap_on_submit_button_to_save_changes(self):
        """
        DESCRIPTION: Tap on 'Submit' button to save changes
        EXPECTED: Changes are saved
        """
        pass
