import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C17719842_Vanilla_Reopen_one_product(Common):
    """
    TR_ID: C17719842
    NAME: [Vanilla] Reopen one product
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in and have two or more products closed
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Management
    PRECONDITIONS: User selects 'I want to reopen some/all products' option and clicks the Continue button
    """
    keep_browser_open = True

    def test_001_click_the_open_button_on_selected_closed_productindexphpattachmentsget36528(self):
        """
        DESCRIPTION: Click the **Open** button on selected closed product
        DESCRIPTION: ![](index.php?/attachments/get/36528)
        EXPECTED: A confirmation message:
        EXPECTED: **'Successfully opened: <prod1>** is displayed on the **Account Reopening** page.
        EXPECTED: Under the confirmation there's the text:
        EXPECTED: ***Control which sections of your account should be accessible through the options below.***
        EXPECTED: The list of the remaining closed products is displayed under the text.
        EXPECTED: ![](index.php?/attachments/get/36529)
        EXPECTED: If there is more than one product on the list, the **REOPEN ALL** button is present under the list.
        EXPECTED: ![](index.php?/attachments/get/36530)
        """
        pass
