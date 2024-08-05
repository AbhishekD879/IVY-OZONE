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
class Test_C28369_Verify_CMS_control_of_Responsible_Gambling_page(Common):
    """
    TR_ID: C28369
    NAME: Verify CMS control of 'Responsible Gambling' page
    DESCRIPTION: This test case verifies CMS control of 'Responsible Gambling' page
    PRECONDITIONS: 1. **Responsible Gambling EN** static block should be configured in CMS and set to active (CMS_ENDPOINT/static-blocks/, where CMS_ENDPOINT can be found using devlog):
    PRECONDITIONS: - **Title** field should have 'Responsible gambling EN' value
    PRECONDITIONS: - **Uri** field should have 'responsible-gambling-en-us' value
    PRECONDITIONS: - **Html Markup** field
    PRECONDITIONS: 2. User is logged into Oxygen app
    PRECONDITIONS: 3. User is viewing 'Responsible Gambling' page (to reach it, tap Right Menu > My account > Responsible Gambling) on frontend
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be delay up to 5-10 mins before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_verify_responsible_gambling_page(self):
        """
        DESCRIPTION: Verify 'Responsible Gambling' page
        EXPECTED: Content from 'Html Markup' CMS field is displayed
        """
        pass

    def test_002_go_to_cms_and_make_some_changes_in_html_markup_field_in_responsible_gambling_en_static_block_and_save_it(self):
        """
        DESCRIPTION: Go to CMS and make some changes in 'Html Markup' field in 'Responsible Gambling EN' static block and save it
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_003_verify_changes_on_responsible_gambling_page_on_frontend(self):
        """
        DESCRIPTION: Verify changes on 'Responsible Gambling' page on frontend
        EXPECTED: Changes made in CMS are displayed successfully
        """
        pass

    def test_004_go_to_cms_and_set_responsible_gambling_en_static_block_to_inactive_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS and set 'Responsible Gambling EN' static block to inactive and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_005_verify_changes_on_responsible_gambling_page_on_frontend(self):
        """
        DESCRIPTION: Verify changes on 'Responsible Gambling' page on frontend
        EXPECTED: * 'Responsible Gambling' page is displayed with 'Responsible Gambling' header and 'Back' button
        EXPECTED: * Content from 'Html Markup' CMS field is NOT displayed
        """
        pass
