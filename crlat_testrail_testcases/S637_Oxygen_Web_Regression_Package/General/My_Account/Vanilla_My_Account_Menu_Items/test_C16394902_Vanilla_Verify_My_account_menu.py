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
class Test_C16394902_Vanilla_Verify_My_account_menu(Common):
    """
    TR_ID: C16394902
    NAME: [Vanilla] Verify "My account" menu
    DESCRIPTION: This TC verifies the "My account" menu
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Log in as a non VIP user
    """
    keep_browser_open = True

    def test_001_click_the_my_account_element_top_menu_bardesktop__tabletindexphpattachmentsget114837491mobileindexphpattachmentsget10014148(self):
        """
        DESCRIPTION: Click the "My account" element (top menu bar)
        DESCRIPTION: *Desktop / Tablet:*
        DESCRIPTION: ![](index.php?/attachments/get/114837491)
        DESCRIPTION: *Mobile:*
        DESCRIPTION: ![](index.php?/attachments/get/10014148)
        EXPECTED: 1. My account  menu opens
        EXPECTED: 2. Menu should contain options (options may differ - Portal config):
        EXPECTED: - Cashier
        EXPECTED: - Offers
        EXPECTED: - History
        EXPECTED: - Inbox
        EXPECTED: - Connect
        EXPECTED: - Settings
        EXPECTED: - Gambling Controls
        EXPECTED: - Help & Contact
        EXPECTED: - Log out
        EXPECTED: and green [DEPOSIT] button at the bottom.
        EXPECTED: *Desktop:*
        EXPECTED: ![](index.php?/attachments/get/36863)
        EXPECTED: *Tablet:*
        EXPECTED: ![](index.php?/attachments/get/36861)
        EXPECTED: *Mobile:*
        EXPECTED: ![](index.php?/attachments/get/36862)
        """
        pass
