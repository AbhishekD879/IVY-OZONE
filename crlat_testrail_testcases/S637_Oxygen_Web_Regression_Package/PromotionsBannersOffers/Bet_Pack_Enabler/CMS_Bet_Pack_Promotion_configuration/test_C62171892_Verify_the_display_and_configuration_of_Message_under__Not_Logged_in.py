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
class Test_C62171892_Verify_the_display_and_configuration_of_Message_under__Not_Logged_in(Common):
    """
    TR_ID: C62171892
    NAME: Verify the display and configuration of Message under  ' Not Logged in'
    DESCRIPTION: This test case verifies display and configuration of Message under 'Not Logged in' in Promotion page
    PRECONDITIONS: 1: User should have admin access and Login to CMS
    PRECONDITIONS: 2: Bet Pack Enabler Button should be created
    PRECONDITIONS: 3: 'Mark this promotion as Bet Pack Enabler' checkbox should be checked
    """
    keep_browser_open = True

    def test_001_verify_the_display_of_not_logged_in(self):
        """
        DESCRIPTION: Verify the display of 'Not Logged in'
        EXPECTED: 'Not Logged in' should be displayed below to 'Low funds' message field
        """
        pass

    def test_002_verify_the_display_of_message_text_field_in_not_logged_in(self):
        """
        DESCRIPTION: Verify the display of 'Message' text field in 'Not Logged in'
        EXPECTED: 'Message' text field should be displayed
        """
        pass

    def test_003_verify_data_validations_for_the_message_text_field(self):
        """
        DESCRIPTION: Verify data validations for the Message text field
        EXPECTED: Message text field should accept max 200 chars
        """
        pass