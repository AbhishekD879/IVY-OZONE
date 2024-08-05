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
class Test_C9770800_Verify_account_one_links_configurations_in_CMS(Common):
    """
    TR_ID: C9770800
    NAME: Verify account one links configurations in CMS
    DESCRIPTION: This test case verifies account one links configurations in CMS
    PRECONDITIONS: 1. CMS is loaded
    PRECONDITIONS: (Use link: https://confluence.egalacoral.com/display/SPI/Migration+CMS-API )
    PRECONDITIONS: where CMS_ENDPOINT e.g. DEV0 or DEV1 can be found using devlog
    PRECONDITIONS: 2. In CMS: Current brand 'Ladbrokes' is selected -> 'System Configuration' -> 'Structure' is opened
    PRECONDITIONS: 3. 'ExternalUrls' section with the following 'Field Name' fields related to AccountOne are present with appropriate links in 'Field Value':
    PRECONDITIONS: * change-password - https://accountone.ladbrokes.com/forgot-password
    PRECONDITIONS: * forgot-password - https://accountone.ladbrokes.com/forgot-password
    PRECONDITIONS: * forgot-username - https://accountone.ladbrokes.com/forgot-username
    PRECONDITIONS: * signup - https://accountone.ladbrokes.com/register
    PRECONDITIONS: * personal-details - https://accountone.ladbrokes.com/personal-details
    PRECONDITIONS: * deposit - https://accountone.ladbrokes.com/deposit
    PRECONDITIONS: * freebets - https://accountone.ladbrokes.com/free-bets
    PRECONDITIONS: * transfer - http://accountone.ladbrokes.com/transfer
    PRECONDITIONS: * withdraw - http://accountone.ladbrokes.com/withdraw
    PRECONDITIONS: * account-history - http://accountone.ladbrokes.com/gaming-and-account
    PRECONDITIONS: * transaction-history - http://accountone.ladbrokes.com/gaming-and-account
    PRECONDITIONS: * gaming-history - http://accountone.ladbrokes.com/gaming-and-account
    PRECONDITIONS: * view-balances - http://accountone.ladbrokes.com/view-balances
    PRECONDITIONS: * limits - https://accountone.ladbrokes.com/responsible-gambling
    PRECONDITIONS: * responsible-gambling - https://accountone.ladbrokes.com/responsible-gambling
    PRECONDITIONS: * marketing-preferences - https://accountone.ladbrokes.com/contact-preferences
    PRECONDITIONS: * kyc-entry-point - https://accountone.ladbrokes.com/entry-point
    """
    keep_browser_open = True
