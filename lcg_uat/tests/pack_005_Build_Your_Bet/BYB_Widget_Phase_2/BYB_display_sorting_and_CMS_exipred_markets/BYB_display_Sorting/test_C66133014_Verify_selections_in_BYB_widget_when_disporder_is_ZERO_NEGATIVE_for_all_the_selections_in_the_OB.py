import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66133014_Verify_selections_in_BYB_widget_when_disporder_is_ZERO_NEGATIVE_for_all_the_selections_in_the_OB(Common):
    """
    TR_ID: C66133014
    NAME: Verify selections in BYB widget when disporder is ZERO/NEGATIVE for all the selections in the OB
    DESCRIPTION: This testcase is to verify selections in BYB widget to be displayed as per the order value which is set in OB
    PRECONDITIONS: 1.Create BYB market for the event in OB with disporder zero/negative
    PRECONDITIONS: 2. BYB Widget sub section should be created under BYB main section
    PRECONDITIONS: 3. Navigation to go CMS -> BYB -> BYB Widget
    PRECONDITIONS: 4.Create a BYB active card for the above created event in OB
    """
    keep_browser_open = True

    def test_000_launch_the_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the application and login with valid credentials
        EXPECTED: Able to launch the application and login successfully
        """
        pass

    def test_000_navigate_to_the_football_landing_page(self):
        """
        DESCRIPTION: Navigate to the Football Landing page
        EXPECTED: User can able to navigate to the Football Landing page successfully
        """
        pass

    def test_000_verify_the_display_of_byb_widget(self):
        """
        DESCRIPTION: Verify the display of BYB Widget
        EXPECTED: User can able to see the BYB Widget
        """
        pass

    def test_000_verify_selections_in_byb_widget_when_disporder_is_zero_for_all_the_selections_in_the_ob(self):
        """
        DESCRIPTION: Verify selections in BYB widget when disporder is ZERO for all the selections in the OB
        EXPECTED: Odds should be displayed as per the selections ID's ascending order
        """
        pass

    def test_000_verify_selections_in_byb_widget_when_disporder_is_negative_followed_by_zero_for_few_of_the_selections_in_the_ob(self):
        """
        DESCRIPTION: Verify selections in BYB widget when disporder is NEGATIVE followed by Zero for few of the selections in the OB
        EXPECTED: Odds with negative disporder should be displayed followed by zero as per disorder in the OB
        """
        pass
