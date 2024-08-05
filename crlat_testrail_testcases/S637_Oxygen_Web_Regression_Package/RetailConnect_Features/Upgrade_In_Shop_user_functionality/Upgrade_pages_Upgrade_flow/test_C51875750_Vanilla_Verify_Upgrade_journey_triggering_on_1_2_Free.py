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
class Test_C51875750_Vanilla_Verify_Upgrade_journey_triggering_on_1_2_Free(Common):
    """
    TR_ID: C51875750
    NAME: [Vanilla] Verify Upgrade journey triggering on 1-2-Free
    DESCRIPTION: This test case verified triggering on Upgrade journey within 1-2-Free feature
    PRECONDITIONS: - In-Shop user (card number and pin) are available
    PRECONDITIONS: - In-Shop user is logged in
    PRECONDITIONS: - 1-2-Free feature is configured and active in CMS https://{cms-api-ui}/one-two-free/games
    PRECONDITIONS: ---
    PRECONDITIONS: User type ('In-shop', 'Online', 'Multi-channel') received in https://{env}/en/api/clientconfig/partial?configNames=vnUser&configNames=vnClaims in
    PRECONDITIONS: "http://api.bwin.com/v3/user/accBusinessPhase:" attribute after login and stored in local storage > OX.USER > accountBusinessPhase attribute
    PRECONDITIONS: ![](index.php?/attachments/get/74407650) ![](index.php?/attachments/get/74407651)
    PRECONDITIONS: ---
    PRECONDITIONS: 'In-Shop' - user with card number and pin (The Grid - Ladbrokes; Connect - Coral).
    PRECONDITIONS: 'Online' - user with username and password.
    PRECONDITIONS: 'Multi-channel' - user who was 'In-Shop' and is upgraded to 'Online' (e.g. has both card#/pin and username/password)
    PRECONDITIONS: ---
    PRECONDITIONS: Contact Venugopal Rao Joshi in order to generate In-Shop users for Ladbrokes brand (currently no known flows to generate In-Shop users for Coral)
    """
    keep_browser_open = True

    def test_001_navigate_to_1_2_free_page(self):
        """
        DESCRIPTION: Navigate to /1-2-free page
        EXPECTED: - 1-2-free game page is displayed
        EXPECTED: - CTA button displays: "UPGRADE AND PLAY"
        """
        pass

    def test_002_click_on_upgrade_and_play_button(self):
        """
        DESCRIPTION: Click on "UPGRADE AND PLAY" button
        EXPECTED: User is redirected to Upgrade popup/page
        """
        pass
