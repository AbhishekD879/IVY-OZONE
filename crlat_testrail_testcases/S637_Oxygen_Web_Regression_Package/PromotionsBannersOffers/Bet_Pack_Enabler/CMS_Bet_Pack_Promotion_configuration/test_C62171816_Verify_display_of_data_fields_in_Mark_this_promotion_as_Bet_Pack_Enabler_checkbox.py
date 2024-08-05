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
class Test_C62171816_Verify_display_of_data_fields_in_Mark_this_promotion_as_Bet_Pack_Enabler_checkbox(Common):
    """
    TR_ID: C62171816
    NAME: Verify display of data fields in  'Mark this promotion as Bet Pack Enabler' checkbox'
    DESCRIPTION: This test case verifies display of data fields in 'Mark this promotion as Bet Pack Enabler' checkbox when user select the 'Mark this promotion as Bet Pack Enabler' checkbox in promotions page
    PRECONDITIONS: 1: User should have admin access and Login to CMS
    PRECONDITIONS: 2: Bet Pack Enabler Button should be created
    PRECONDITIONS: 3:'Mark this promotion as Bet Pack Enabler' checkbox should be checked
    """
    keep_browser_open = True

    def test_001_verify__mark_this_promotion_as_bet_pack_enabler_checkbox(self):
        """
        DESCRIPTION: Verify ' 'Mark this promotion as Bet Pack Enabler' checkbox'
        EXPECTED: 'Mark this promotion as Bet Pack Enabler' checkbox should be checked
        """
        pass

    def test_002_verify_the_data_fields_in_mark_this_promotion_as_bet_pack_enabler_checkbox(self):
        """
        DESCRIPTION: Verify the data fields in 'Mark this promotion as Bet Pack Enabler' checkbox
        EXPECTED: Below fields should be displayed
        EXPECTED: * Text
        EXPECTED: * Congrats Message
        EXPECTED: * OB Promotion ID
        EXPECTED: * Trigger Ids
        EXPECTED: * Value
        EXPECTED: * Low funds
        EXPECTED: * Non Logged In
        EXPECTED: * Error message
        EXPECTED: * Message field below to (Low funds, Non Logged In and error message)
        """
        pass

    def test_003_verify_data_validations_for_the_data_fields(self):
        """
        DESCRIPTION: Verify data validations for the data fields
        EXPECTED: * Text: Allow to enter max 200 chars
        EXPECTED: * OB Promotion ID: Allow only Integers
        EXPECTED: * Trigger Ids: Allow only Integers
        EXPECTED: * Value: Allow only Integers
        """
        pass
