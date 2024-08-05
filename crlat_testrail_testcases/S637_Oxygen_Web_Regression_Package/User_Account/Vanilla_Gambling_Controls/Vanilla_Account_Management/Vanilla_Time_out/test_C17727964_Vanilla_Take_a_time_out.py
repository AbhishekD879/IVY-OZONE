import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C17727964_Vanilla_Take_a_time_out(Common):
    """
    TR_ID: C17727964
    NAME: [Vanilla] Take a time-out
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Management
    """
    keep_browser_open = True

    def test_001_select_the_id_like_to_take_an_irreversible_time_out_or_exclude_myself_from_gaming_option(self):
        """
        DESCRIPTION: Select the 'I’d like to take an irreversible time-out or exclude myself from gaming' option
        EXPECTED: The time-out page is displayed with time-out duration options and reasons.
        """
        pass

    def test_002_select_time_out_duration(self):
        """
        DESCRIPTION: Select time-out duration
        EXPECTED: Duration gets selected.
        """
        pass

    def test_003_select_time_out_reason(self):
        """
        DESCRIPTION: Select time-out reason
        EXPECTED: Reason gets selected.
        """
        pass

    def test_004_click_the_continue_button(self):
        """
        DESCRIPTION: Click the **Continue** button
        EXPECTED: The confirmation screen of time-out is displayed.
        """
        pass

    def test_005_click_the_take_a_short_time_out_button(self):
        """
        DESCRIPTION: Click the **Take a short time-out** button
        EXPECTED: User account is timed-out for the selected duration.
        EXPECTED: A confirmation message is displayed on the time-out page.
        EXPECTED: Under the confirmation, the consequences of a time-out are displayed with a link to customer service.
        EXPECTED: ![](index.php?/attachments/get/36533)
        """
        pass
