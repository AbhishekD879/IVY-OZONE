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
class Test_C17752136_Vanilla_Automatically_reopen_one_product(Common):
    """
    TR_ID: C17752136
    NAME: [Vanilla] Automatically reopen one product
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User had one product closed (e.g. Sports) for a short period of time and that time has ended recently
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Management
    """
    keep_browser_open = True

    def test_001_select_i_want_to_close_someall_products_option_and_click_the_continue_button(self):
        """
        DESCRIPTION: Select 'I want to close some/all products' option and click the **Continue** button
        EXPECTED: Product closed before (e.g. Sports) has **Current status** set to **open**.
        EXPECTED: By that product is the **CLOSE** button.
        EXPECTED: 'Closed until' line is not present there.
        """
        pass
