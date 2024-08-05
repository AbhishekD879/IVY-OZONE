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
class Test_C66133021_Verify_if_updated_record_is_displayed_still_under_Expired_Cards_Table(Common):
    """
    TR_ID: C66133021
    NAME: Verify if updated record is displayed still under 'Expired Cards Table'
    DESCRIPTION: Verify if updated record is displayed still under 'Expired Cards Table'
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

    def test_000_do_not_change_from_and_to_dates(self):
        """
        DESCRIPTION: Do not change From and To dates
        EXPECTED: From and To dates are unchanged
        """
        pass

    def test_000_click_save_icon(self):
        """
        DESCRIPTION: Click 'Save Icon'
        EXPECTED: Updated values should be saved successfully
        """
        pass

    def test_000_verify_if_updated_record_is_displayed_under_expired_markets_cards_table(self):
        """
        DESCRIPTION: Verify if updated record is displayed under 'Expired Markets Cards Table'
        EXPECTED: Record should be displayed under 'Expired Markets Cards Table'
        """
        pass
