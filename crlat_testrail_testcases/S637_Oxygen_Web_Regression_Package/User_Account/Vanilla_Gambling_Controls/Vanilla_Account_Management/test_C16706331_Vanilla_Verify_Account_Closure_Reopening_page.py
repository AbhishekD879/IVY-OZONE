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
class Test_C16706331_Vanilla_Verify_Account_Closure_Reopening_page(Common):
    """
    TR_ID: C16706331
    NAME: [Vanilla] Verify Account Closure & Reopening page
    DESCRIPTION: This test case verifies Account Closure & Reopening page 1
    PRECONDITIONS: Load app
    PRECONDITIONS: **Prepare users:**
    PRECONDITIONS: (Users should be real-money players - at least one deposit in the past)
    PRECONDITIONS: 1) UK user that don't have any closed products
    PRECONDITIONS: 2) UK user that have some closed products
    PRECONDITIONS: 3) UK user that have all products closed
    PRECONDITIONS: 4) non UK user that don't have any closed products
    PRECONDITIONS: 5) non UK user that have some closed products
    PRECONDITIONS: 6) non UK user that have all products closed
    PRECONDITIONS: Or just simply 2 users - **UK user** and **Non UK user** - check when no product is closed, close one product - check when one product is closed, close all products - check when all products are closed.
    PRECONDITIONS: **For all users:**
    PRECONDITIONS: Navigate to My Account -> Gambling Controls
    PRECONDITIONS: Select 'Account Closure & Reopening' option
    """
    keep_browser_open = True

    def test_001_log_in_with_user_nr_1_and_go_through_the_path_from_preconditions(self):
        """
        DESCRIPTION: Log in with user nr 1 and go through the path from preconditions
        EXPECTED: -
        """
        pass

    def test_002_click_the__choose__button(self):
        """
        DESCRIPTION: Click the [ Choose ] button
        EXPECTED: Account closure page appears with content:
        EXPECTED: - **Account Closure & Reopening** header
        EXPECTED: - 'Please choose one of the options below.' line with radio button options underneath:
        EXPECTED: -- 'I want to close my account or sections of it'
        EXPECTED: -- 'I'd like to take an irreversible time-out or exclude myself from gaming'
        EXPECTED: - [ Continue ] button
        EXPECTED: - [ Cancel ] button
        """
        pass

    def test_003_verify__continue__button(self):
        """
        DESCRIPTION: Verify [ Continue ] button
        EXPECTED: [ Continue ] button is disabled by default
        """
        pass

    def test_004_verify__cancel__button(self):
        """
        DESCRIPTION: Verify [ Cancel ] button
        EXPECTED: [ Cancel ] button is enabled by default
        """
        pass

    def test_005_clicktap__cancel__button(self):
        """
        DESCRIPTION: Click/Tap [ Cancel ] button
        EXPECTED: User is navigated to 'Gambling Controls' page
        """
        pass

    def test_006_log_in_with_user_nr_2_and_go_through_the_path_from_preconditions(self):
        """
        DESCRIPTION: Log in with user nr 2 and go through the path from preconditions
        EXPECTED: -
        """
        pass

    def test_007_click_the__choose__button(self):
        """
        DESCRIPTION: Click the [ Choose ] button
        EXPECTED: Account closure page appears with content:
        EXPECTED: - **Account Closure & Reopening** header
        EXPECTED: - 'Please choose one of the options below.' line with radio button options underneath:
        EXPECTED: -- 'I want to close my account or sections of it'
        EXPECTED: -- 'I want to reopen my account or sections of it'
        EXPECTED: -- 'I'd like to take an irreversible time-out or exclude myself from gaming'
        EXPECTED: - [ Continue ] button
        EXPECTED: - [ Cancel ] button
        """
        pass

    def test_008_log_in_with_user_3_and_go_through_the_path_from_preconditions(self):
        """
        DESCRIPTION: Log in with user 3 and go through the path from preconditions
        EXPECTED: -
        """
        pass

    def test_009_click_the__choose__button(self):
        """
        DESCRIPTION: Click the [ Choose ] button
        EXPECTED: Account closure page appears with content:
        EXPECTED: - **Account Closure & Reopening** header
        EXPECTED: - 'Please choose one of the options below.' line with radio button options underneath:
        EXPECTED: -- 'I want to reopen my account or sections of it'
        EXPECTED: -- 'I'd like to take an irreversible time-out or exclude myself from gaming'
        EXPECTED: - [ Continue ] button
        EXPECTED: - [ Cancel ] button
        """
        pass

    def test_010_log_in_with_user_4_and_go_through_the_path_from_preconditions(self):
        """
        DESCRIPTION: Log in with user 4 and go through the path from preconditions
        EXPECTED: -
        """
        pass

    def test_011_click_the__choose__button(self):
        """
        DESCRIPTION: Click the [ Choose ] button
        EXPECTED: Account closure page appears with content:
        EXPECTED: - **Account Closure & Reopening** header
        EXPECTED: - 'Please choose one of the options below.' line with radio button options underneath:
        EXPECTED: -- 'I want to close my account or sections of it'
        EXPECTED: -- 'I'd like to take an irreversible time-out or exclude myself from gaming'
        EXPECTED: - [ Continue ] button
        EXPECTED: - [ Cancel ] button
        """
        pass

    def test_012_log_in_with_user_5_and_go_through_the_path_from_preconditions(self):
        """
        DESCRIPTION: Log in with user 5 and go through the path from preconditions
        EXPECTED: -
        """
        pass

    def test_013_click_the__choose__button(self):
        """
        DESCRIPTION: Click the [ Choose ] button
        EXPECTED: Account closure page appears with content:
        EXPECTED: - **Account Closure & Reopening** header
        EXPECTED: - 'Please choose one of the options below.' line with radio button options underneath:
        EXPECTED: -- 'I want to close my account or sections of it'
        EXPECTED: -- 'I want to reopen my account or sections of it'
        EXPECTED: -- 'I'd like to take an irreversible time-out or exclude myself from gaming'
        EXPECTED: - [ Continue ] button
        EXPECTED: - [ Cancel ] button
        """
        pass

    def test_014_log_in_with_user_6_and_go_through_the_path_from_preconditions(self):
        """
        DESCRIPTION: Log in with user 6 and go through the path from preconditions
        EXPECTED: -
        """
        pass

    def test_015_click_the__choose__button(self):
        """
        DESCRIPTION: Click the [ Choose ] button
        EXPECTED: Account closure page appears with content:
        EXPECTED: - **Account Closure & Reopening** header
        EXPECTED: - 'Please choose one of the options below.' line with radio button options underneath:
        EXPECTED: -- 'I want to reopen my account or sections of it'
        EXPECTED: -- 'I'd like to take an irreversible time-out or exclude myself from gaming'
        EXPECTED: - [ Continue ] button
        EXPECTED: - [ Cancel ] button
        """
        pass
