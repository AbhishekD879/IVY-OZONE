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
class Test_C28378_Verify_CMS_control_of_Logged_out_Confirmation_Message(Common):
    """
    TR_ID: C28378
    NAME: Verify CMS control of 'Logged out' Confirmation Message
    DESCRIPTION: This test case verifies CMS control of  'Logged out' confirmation message according the story **BMA-4531 **LCCP Auto Self-Exclude: CMS control
    PRECONDITIONS: User should be logged in to view  'Logged out' confirmation message.
    PRECONDITIONS: To load CMS for English language support 'Self Exclusion Logged Out EN' use the link: CMS_ENDPOINT/keystone/static-blocks/
    PRECONDITIONS: To load CMS for Ukrainian language support 'Self Exclusion Logged Out UA' use the link: CMS_ENDPOINT/keystone/static-blocks/
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
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
        EXPECTED: The 'Self Exlusion' pop-up is opened
        """
        pass

    def test_007_select_the_period_for_self_exclusion_from_drop_down(self):
        """
        DESCRIPTION: Select the period for Self Exclusion from drop down
        EXPECTED: Period for Self Exclusion from drop down is selected
        """
        pass

    def test_008_enter_a_valid_password_into_a_password_field(self):
        """
        DESCRIPTION: Enter a valid password into a "Password" field
        EXPECTED: Password is entered
        """
        pass

    def test_009_tap_the_click_here_to_confirm_that_you_wish_to_self_exclude_link(self):
        """
        DESCRIPTION: Tap the 'CLICK HERE to Confirm that you wish to Self Exclude' link
        EXPECTED: The "Account Self-Excluded" confirmation message is shown
        EXPECTED: Make sure content (text and image) has been taken from 'Self Exclusion Logged Out EN' static block
        """
        pass

    def test_010_go_to_cms_and_make_some_changes_in_self_exclusion_logged_out_en_static_block_and_save_it(self):
        """
        DESCRIPTION: Go to CMS and make some changes in 'Self Exclusion Logged Out EN' static block and save it
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_011_verify_changes_on_account_self_excluded_confirmation_message_when_en_language_is_chosen(self):
        """
        DESCRIPTION: Verify changes on "Account Self-Excluded" confirmation message when EN language is chosen
        EXPECTED: Changes made in CMS are displayed successfully
        """
        pass

    def test_012_switch_to_ua_language(self):
        """
        DESCRIPTION: Switch to UA language
        EXPECTED: 
        """
        pass

    def test_013_go_to_account_self_excluded_confirmation_message(self):
        """
        DESCRIPTION: Go to "Account Self-Excluded" confirmation message
        EXPECTED: The "Account Self-Excluded" confirmation message is shown
        EXPECTED: Make sure content (text and image) has been taken from 'Self Exclusion Logged Out UA' static block
        """
        pass

    def test_014_go_to_cms_and_make_some_changes_in_self_exclusion_logged_out_ua_static_block_and_save_it(self):
        """
        DESCRIPTION: Go to CMS and make some changes in 'Self Exclusion Logged Out UA' static block and save it
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_015_go_to_account_self_excluded_confirmation_message_in_oxygen_app(self):
        """
        DESCRIPTION: Go to "Account Self-Excluded" confirmation message in Oxygen app
        EXPECTED: The"Account Self-Excluded" confirmation message is shown
        """
        pass

    def test_016_verify_changes_on_self_exclusion_request__page_when_ua_language_is_chosen(self):
        """
        DESCRIPTION: Verify changes on 'Self Exclusion Request ' page when UA language is chosen
        EXPECTED: Changes made in CMS are displayed successfully
        """
        pass
