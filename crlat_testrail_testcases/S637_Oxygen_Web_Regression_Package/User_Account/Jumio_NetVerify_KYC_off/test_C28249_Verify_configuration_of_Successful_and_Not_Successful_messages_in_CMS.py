import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C28249_Verify_configuration_of_Successful_and_Not_Successful_messages_in_CMS(Common):
    """
    TR_ID: C28249
    NAME: Verify configuration of Successful and Not Successful messages in CMS
    DESCRIPTION: This test case verifies configuration of Successful and Not Successful messages in CMS.
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-4059 (Jumio/ NetVerify Integration)
    PRECONDITIONS: CMS: https://**CMS_ENDPOINT**/keystone
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_trigger_happy_path_of_netverify_transaction(self):
        """
        DESCRIPTION: Trigger happy path of Netverify transaction
        EXPECTED: Success page is opened
        """
        pass

    def test_003_verify_content_of_success_page(self):
        """
        DESCRIPTION: Verify content of Success page
        EXPECTED: Content of Success page corresponds to the html text set up in CMS->Static Blocks->Netverify Success EN
        """
        pass

    def test_004_verify_end_point_after_tapping_visit_coralcouk_button(self):
        """
        DESCRIPTION: Verify end point after tapping 'VISIT CORAL.CO.UK' button
        EXPECTED: User is redirected to the page defined in 'Insert/edit link' (homepage)
        """
        pass

    def test_005_open_cms_static_blocks_netverify_success(self):
        """
        DESCRIPTION: Open CMS->Static Blocks-> Netverify Success
        EXPECTED: Netverify Success configuration is opened
        """
        pass

    def test_006_make_any_changesconfigurations_and_save_them(self):
        """
        DESCRIPTION: Make any changes/configurations and save them
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_007_repeat_steps_1_2_and_verify_success_page(self):
        """
        DESCRIPTION: Repeat steps №1-2 and verify Success page
        EXPECTED: All changes are displayed correctly
        """
        pass

    def test_008_trigger_error_path_of_netverify_transaction(self):
        """
        DESCRIPTION: Trigger error path of Netverify transaction
        EXPECTED: Not Success page is shown
        """
        pass

    def test_009_verify_content_of_not_success_page(self):
        """
        DESCRIPTION: Verify content of Not Success page
        EXPECTED: Content of Not Success page corresponds to the html text set up in CMS->Static Blocks->Netverify Error EN
        """
        pass

    def test_010_verify_end_point_after_tapping_visit_coralcouk_button(self):
        """
        DESCRIPTION: Verify end point after tapping 'VISIT CORAL.CO.UK' button
        EXPECTED: User is redirected to the page defined in 'Insert/edit link' (homepage)
        """
        pass

    def test_011_open_cms_static_blocks_netverify_error(self):
        """
        DESCRIPTION: Open CMS->Static Blocks-> Netverify Error
        EXPECTED: Netverify Error configuration is opened
        """
        pass

    def test_012_make_any_changesconfigurations_and_save_them(self):
        """
        DESCRIPTION: Make any changes/configurations and save them
        EXPECTED: All changes are saved successfully
        """
        pass

    def test_013_repeat_step_18_and_verify_not_success_page(self):
        """
        DESCRIPTION: Repeat step №1,8 and verify Not Success page
        EXPECTED: All changes are displayed correctly
        """
        pass
