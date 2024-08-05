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
class Test_C44870145_Verify_user_session_ends_time_out_after_requested_period__Navigate_to_Responsible_Gambling_https_responsiblegamblingcoralcouk_and_set_up_time_period_for_user__Then_verify_user_session_ends_as_per_the_limit(Common):
    """
    TR_ID: C44870145
    NAME: "Verify user session ends (time out) after requested period. - Navigate to 'Responsible Gambling' https://responsiblegambling.coral.co.uk/ and set up time period for user. - Then verify user session ends as per the limit."
    DESCRIPTION: "Verify user session ends (time out) after requested period.
    DESCRIPTION: - Navigate to 'Gambling Controls' > 'Time Management' to set up time period for user.
    DESCRIPTION: - Then verify user session ends as per the limit."
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_my_account_item_avatar(self):
        """
        DESCRIPTION: Tap 'My account' item (Avatar)
        EXPECTED: 'My account' page is opened with full list of items
        """
        pass

    def test_003_tap_gambling_controls(self):
        """
        DESCRIPTION: Tap 'Gambling Controls'
        EXPECTED: Options with
        EXPECTED: Deposit Limits (Selected by default)
        EXPECTED: Time Management
        EXPECTED: Account Closure & Reopening
        EXPECTED: are shown
        """
        pass

    def test_004_tap_time_management(self):
        """
        DESCRIPTION: Tap 'Time Management'
        EXPECTED: Options to set time limits with a drop down box is available to the user
        """
        pass

    def test_005_once_the_user_sets_the_time_limit(self):
        """
        DESCRIPTION: Once the user sets the Time limit
        EXPECTED: The user should be notified at the end of the selected time limit and will have the option to continue or log out.
        """
        pass
