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
class Test_C46540_Verify_CMS_configuration_of_Cookie_Notification_Banner(Common):
    """
    TR_ID: C46540
    NAME: Verify CMS configuration of Cookie Notification Banner
    DESCRIPTION: This test case verifies CMS configuration of Cookie Notification Banner
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-14778 Cookie Notifications On All Platforms
    DESCRIPTION: BMA-46701 Coral IOS app - please remove the cookie banner
    PRECONDITIONS: 1.To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/static-blocks
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: 2.Make sure that Cookie Banner is **NOT DISPLAYED** on Coral iOS wrapper v.5.1.1 build 1157 and higher regardless of the CMS configuration.
    PRECONDITIONS: ||: Hyperlink|: Link
    PRECONDITIONS: || cookie policy | https://coral-eng.custhelp.com/app/answers/detail/a_id/2132#cookies
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_verify_cookie_notification_banner(self):
        """
        DESCRIPTION: Verify Cookie Notification Banner
        EXPECTED: Make sure data is taken from 'Cookie banner' static block
        """
        pass

    def test_003_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_004_open_static_blocks_section(self):
        """
        DESCRIPTION: Open 'Static blocks' section
        EXPECTED: 'Static blocks' section is opened
        """
        pass

    def test_005_go_to_cookie_banner_static_block(self):
        """
        DESCRIPTION: Go to 'Cookie banner' static block
        EXPECTED: 
        """
        pass

    def test_006_make_some_changes_in_cookie_banner_static_block_and_save_changes(self):
        """
        DESCRIPTION: Make some changes in 'Cookie banner' static block and save changes
        EXPECTED: Changes are made and saved successfully
        """
        pass

    def test_007_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_008_verify_cookie_notification_banner(self):
        """
        DESCRIPTION: Verify Cookie Notification Banner
        EXPECTED: Changes made in CMS are displayed successfully
        """
        pass
