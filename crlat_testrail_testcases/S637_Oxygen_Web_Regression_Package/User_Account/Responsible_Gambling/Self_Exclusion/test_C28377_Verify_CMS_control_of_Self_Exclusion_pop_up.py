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
class Test_C28377_Verify_CMS_control_of_Self_Exclusion_pop_up(Common):
    """
    TR_ID: C28377
    NAME: Verify CMS control of  'Self Exclusion' pop-up
    DESCRIPTION: This test case verifies CMS control of 'Self Exclusion' pop-up
    PRECONDITIONS: * User is logged in to Oxygen app
    PRECONDITIONS: * Content for CMS configurable part of 'Self Exclusion Request' popup is added in CMS -> Admin -> Static blocks -> 'Self Exclusion Request EN'
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

    def test_005_tap_read_more_about_self_exclusion_button(self):
        """
        DESCRIPTION: Tap 'Read More About Self Exclusion' button
        EXPECTED: 'Self Exclusion' page is opened
        """
        pass

    def test_006_tap_therequestself_exclusion_link(self):
        """
        DESCRIPTION: Tap the 'Request Self Exclusion' link
        EXPECTED: The 'Self Exclusion' pop-up is opened
        EXPECTED: Make sure content (text and image) has been taken from 'Self Exclusion Request EN' static block
        """
        pass

    def test_007_go_to_cms_and_make_some_changes_inself_exclusion_request_en_static_block_and_save_it(self):
        """
        DESCRIPTION: Go to CMS and make some changes in 'Self Exclusion Request EN' static block and save it
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_008_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_009_go_to_self_exclusion_request_pop_up(self):
        """
        DESCRIPTION: Go to 'Self Exclusion Request' pop-up
        EXPECTED: 
        """
        pass

    def test_010_verify_changes_on_selfexlusion_form(self):
        """
        DESCRIPTION: Verify changes on 'Self Exlusion' form
        EXPECTED: Changes made in CMS are displayed successfully
        """
        pass

    def test_011_go_to_cms_and_make_some_changes_incross_brands_self_exclusion_signposting_static_block_and_save_it(self):
        """
        DESCRIPTION: Go to CMS and make some changes in 'Cross brands self exclusion signposting' static block and save it
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_012_repeat_steps_8_10(self):
        """
        DESCRIPTION: Repeat steps #8-10
        EXPECTED: All new changes should be displayed
        """
        pass
