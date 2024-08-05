import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2088614_Verify_in_shop_Multichannel_negative_upgrade_cases(Common):
    """
    TR_ID: C2088614
    NAME: Verify in-shop > Multichannel negative upgrade cases
    DESCRIPTION: 
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: 1. Load SportBook
    PRECONDITIONS: 2. Log in with InShop user
    PRECONDITIONS: 3. Select 'Connect' from header ribbon
    """
    keep_browser_open = True

    def test_001_select_upgrade_your_connect_account_to_bet_online(self):
        """
        DESCRIPTION: Select 'Upgrade your Connect account to bet online'
        EXPECTED: Upgrade page with dialog is opened
        """
        pass

    def test_002_tap_upgrade_button(self):
        """
        DESCRIPTION: Tap UPGRADE button
        EXPECTED: Upgrade page is opened (similar to registration page)
        """
        pass

    def test_003__populate_all_required_fields_into_email_field_enter_mail_that_belongs_to_already_upgraded_multi_channel_user(self):
        """
        DESCRIPTION: * Populate all required fields
        DESCRIPTION: * Into email field enter mail that belongs to already upgraded multi-channel user
        EXPECTED: Error message says "This email address is already registered to a Connect or Online account"
        """
        pass

    def test_004__into_email_field_enter_mail_that_belongs_to_only_online_account_not_multichannel(self):
        """
        DESCRIPTION: * Into email field enter mail that belongs to only online account (not multichannel)
        EXPECTED: Error message says "This email address is already registered to a Connect or Online account"
        """
        pass
