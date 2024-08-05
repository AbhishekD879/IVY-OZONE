import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66133019_Verify_if_user_is_able_to_update_all_the_values_in_the_record_and_Edit_Icon_changes_to_Save_Icon(Common):
    """
    TR_ID: C66133019
    NAME: Verify if user is able to update all the values in the record and 'Edit Icon' changes to 'Save Icon'
    DESCRIPTION: This test case is to verify if user is able to update all the values in the record once 'Edit Icon' is clicked and 'Edit Icon' changes to 'Save Icon'
    PRECONDITIONS: 1. BYB Widget sub section should be created under BYB main section
    PRECONDITIONS: 2. Navigation to go CMS -> BYB -> BYB Widget
    PRECONDITIONS: 3.CMS launch is successful
    PRECONDITIONS: 4.Expired records are available under 'Expired Market Cards Table'
    """
    keep_browser_open = True

    def test_000_verify_edit_icon_for_the_expired_records(self):
        """
        DESCRIPTION: Verify 'Edit Icon' for the expired records
        EXPECTED: Edit Icon' should be displayed for the expired records
        """
        pass

    def test_000_verify_if_user_is_able_to_update_all_the_values_in_the_record_once_edit_icon_is_clicked(self):
        """
        DESCRIPTION: Verify if user is able to update all the values in the record once 'Edit Icon' is clicked
        EXPECTED: User should be able to update the values
        """
        pass

    def test_000_verify_edit_icon_changes_to_save_icon(self):
        """
        DESCRIPTION: Verify 'Edit Icon' changes to 'Save Icon'
        EXPECTED: Edit Icon' should change to 'Save Icon'
        """
        pass

    def test_000_click_save_icon(self):
        """
        DESCRIPTION: Click 'Save Icon'
        EXPECTED: Updated values should be saved successfully
        """
        pass
