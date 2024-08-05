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
class Test_C28374_CMS_control_of_Self_Exclusion_Page(Common):
    """
    TR_ID: C28374
    NAME: CMS control of 'Self Exclusion' Page
    DESCRIPTION: This test case verifies CMS control of 'Self Exclusion' Page according the story **BMA-3952 **LCCP Auto Self-Exclude Requirement
    DESCRIPTION: TO EDIT: a part which is connected to localization. Currently we are using only English in app
    PRECONDITIONS: User should be logged in to view 'Self Exclusion' page.
    PRECONDITIONS: To load CMS for English language support 'Self Exclusion EN' use the link: CMS_ENDPOINT/keystone/static-blocks/
    PRECONDITIONS: To load CMS for Ukrainian language support 'Self Exclusion UA' use the link: CMS_ENDPOINT/keystone/static-blocks/
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_on_right_menu_icon(self):
        """
        DESCRIPTION: Tap on Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_003_tap_my_account_item(self):
        """
        DESCRIPTION: Tap 'My account' item
        EXPECTED: 'My account' page is opened with full list of items
        """
        pass

    def test_004_tap_on_responsible_gambling_menu_item(self):
        """
        DESCRIPTION: Tap on 'Responsible Gambling' menu item
        EXPECTED: 'Responsible Gambling' page is opened
        """
        pass

    def test_005_tap_the_read_more_about_self_exlusion_button(self):
        """
        DESCRIPTION: Tap the 'Read More About Self Exlusion' button
        EXPECTED: The 'Self Exclusion ' page is opened
        EXPECTED: Make sure text has been taken from 'Self Exclusion EN' static block
        """
        pass

    def test_006_go_to_cms_and_make_some_changes_in_self_exclusionen_static_block_and_save_it(self):
        """
        DESCRIPTION: Go to CMS and make some changes in 'Self Exclusion EN' static block and save it
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_007_verify_changes_on_self_exlusion_page_when_en_language_is_chosen(self):
        """
        DESCRIPTION: Verify changes on 'Self Exlusion' page when EN language is chosen
        EXPECTED: Changes made in CMS are displayed successfully
        """
        pass
