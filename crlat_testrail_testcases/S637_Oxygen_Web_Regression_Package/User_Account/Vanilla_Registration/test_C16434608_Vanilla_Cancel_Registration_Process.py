import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C16434608_Vanilla_Cancel_Registration_Process(Common):
    """
    TR_ID: C16434608
    NAME: [Vanilla] Cancel Registration Process
    DESCRIPTION: This test case verifies canceling of registration process
    PRECONDITIONS: User is logged out.
    """
    keep_browser_open = True

    def test_001_load_vanilla_application(self):
        """
        DESCRIPTION: Load Vanilla application
        EXPECTED: 
        """
        pass

    def test_002_click_on_join_button(self):
        """
        DESCRIPTION: Click on 'Join' button
        EXPECTED: Registration page is opened
        """
        pass

    def test_003_enter_correct_data_to_all_required_fields_due_to_validation_rules_for_3_registration_pages(self):
        """
        DESCRIPTION: Enter correct data to all required fields due to validation rules for 3 registration pages
        EXPECTED: All mandatory fields are filled
        """
        pass

    def test_004_clicktap_on_x_button_at_the_top_right_corner(self):
        """
        DESCRIPTION: Click/Tap on 'X' button at the top right corner
        EXPECTED: - Registration process is canceled
        EXPECTED: - Homepage is shown
        """
        pass
