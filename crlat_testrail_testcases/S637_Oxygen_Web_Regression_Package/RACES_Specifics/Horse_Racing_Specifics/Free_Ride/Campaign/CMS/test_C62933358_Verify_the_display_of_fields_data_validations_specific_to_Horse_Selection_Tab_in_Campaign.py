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
class Test_C62933358_Verify_the_display_of_fields_data_validations_specific_to_Horse_Selection_Tab_in_Campaign(Common):
    """
    TR_ID: C62933358
    NAME: Verify the display of fields & data validations specific to Horse Selection Tab in Campaign
    DESCRIPTION: This test case verifies display of fields & data validations specific to Horse Selection Tab in Campaign
    PRECONDITIONS: 1: Login to CMS with admin access
    PRECONDITIONS: 2: Campaign should be created successfully
    """
    keep_browser_open = True

    def test_001_verify_display_of_horse_selection_tab_in_the_campaign_page(self):
        """
        DESCRIPTION: Verify display of Horse Selection Tab in the Campaign page
        EXPECTED: Horse Selection Tab should be displayed in the Campaign page
        """
        pass

    def test_002_click_on_horse_selection_tab(self):
        """
        DESCRIPTION: Click on Horse selection Tab
        EXPECTED: Below fields should be displayed under Horse Selection Tab
        EXPECTED: * Fetch for classIds
        EXPECTED: * Fetch from
        EXPECTED: * HH MM SS
        EXPECTED: * Restrict to UK And IRE
        EXPECTED: * Refresh Events CTA
        """
        pass

    def test_003_verify_data_validations_for_fetch_for_class_id_field(self):
        """
        DESCRIPTION: Verify data validations for 'Fetch for Class ID' field
        EXPECTED: * 'Fetch for Class ID' field should be enabled
        EXPECTED: * Able to accept multiple class Ids separated by commas
        """
        pass

    def test_004_verify_data_validations_for_fetch_from_field(self):
        """
        DESCRIPTION: Verify data validations for 'Fetch from' field
        EXPECTED: * 'Fetch from' field should be disabled and by default current system date should be displayed
        EXPECTED: * User should be able to change the date using date picker
        """
        pass

    def test_005_verify_the_data_validations_for_hh_mm_ss_field(self):
        """
        DESCRIPTION: Verify the data validations for 'HH MM SS' field
        EXPECTED: * 'HH MM SS' field should be enabled
        EXPECTED: * User can update the values by entering or by using up and down arrows
        """
        pass

    def test_006_verify_the_data_validations_for_restrict_to_uk_and_ire(self):
        """
        DESCRIPTION: Verify the data validations for 'Restrict to UK And IRE'
        EXPECTED: * 'Restrict to UK And IRE' field should be checked by default
        EXPECTED: * User should able to check/uncheck the field
        """
        pass

    def test_007_verify_the_state_of_refresh_events_cta_button(self):
        """
        DESCRIPTION: Verify the state of 'Refresh Events CTA' button
        EXPECTED: 'Refresh Events CTA' button should be enabled
        """
        pass
