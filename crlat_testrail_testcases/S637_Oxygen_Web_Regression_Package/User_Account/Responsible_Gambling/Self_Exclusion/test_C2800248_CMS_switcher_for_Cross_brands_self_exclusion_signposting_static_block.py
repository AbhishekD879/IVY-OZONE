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
class Test_C2800248_CMS_switcher_for_Cross_brands_self_exclusion_signposting_static_block(Common):
    """
    TR_ID: C2800248
    NAME: CMS switcher for 'Cross brands self exclusion signposting' static block
    DESCRIPTION: This test case verifies CMS switcher for 'Cross brands self exclusion signposting' static block
    PRECONDITIONS: In CMS
    PRECONDITIONS: *  Load CMS and log in
    PRECONDITIONS: * Go to Static Block section and make sure that CMS configurable part of 'Self Exclusion Request' popup is added
    PRECONDITIONS: * Go to System Configuration section
    PRECONDITIONS: In Oxygen app
    PRECONDITIONS: *  Load app and log in
    PRECONDITIONS: *  Navigate to Right Menu -> My Account -> select Responsible Gambling item
    PRECONDITIONS: *  Tap 'Read More About Self Exclusion' link within 'Self-Exclusion' section -> 'Self-exclusion' page is opened
    PRECONDITIONS: *  Tap 'Request Self-Exclusion' link ->'Self Exclusion Request' popup is displayed
    """
    keep_browser_open = True

    def test_001_switch_off_cross_brands_self_exclusion_signposting_switcher_in_cms_and_save_changes(self):
        """
        DESCRIPTION: Switch off 'Cross brands self exclusion signposting' switcher in CMS and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_002_in_oxygen_app_open_self_exclusion_request_popup(self):
        """
        DESCRIPTION: In Oxygen app open 'Self Exclusion Request' popup
        EXPECTED: 'Cross brands self exclusion signposting' static block is NOT displayed
        """
        pass

    def test_003_switch_on_cross_brands_self_exclusion_signposting_switcher_in_cms_and_save_changes(self):
        """
        DESCRIPTION: Switch on 'Cross brands self exclusion signposting' switcher in CMS and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_004_in_oxygen_app_open_self_exclusion_request_popup(self):
        """
        DESCRIPTION: In Oxygen app open 'Self Exclusion Request' popup
        EXPECTED: 'Cross brands self exclusion signposting' static block is displayed within 'Self Exclusion Request' popup
        """
        pass
