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
class Test_C62912865_Verify_displaying_of_messaging_in_betslip_when_user_login_on_Nth_day_PG(Common):
    """
    TR_ID: C62912865
    NAME: Verify displaying of messaging in  betslip when user login on Nth day_PG
    DESCRIPTION: This test cases verifies message display in betslip when user login on Nth day
    PRECONDITIONS: User risk level should be set
    PRECONDITIONS: Frequency and Message should be set in CMS
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_user_login_to_application_on_nth_day(self):
        """
        DESCRIPTION: User login to application on Nth day
        EXPECTED: Login should be successful
        """
        pass

    def test_003_go_to_any_sport_and_add_single_selection_to_betslip(self):
        """
        DESCRIPTION: Go to any sport and add single selection to betslip
        EXPECTED: Selection is displayed and  added to betslip
        """
        pass

    def test_004_check_the_messaging_in_betslip_on_nth_day(self):
        """
        DESCRIPTION: Check the Messaging in Betslip on Nth day
        EXPECTED: User view a messaging component prior to bet placement as per CMS config
        """
        pass

    def test_005_user_click_on_minimize_for_message_component(self):
        """
        DESCRIPTION: User click on Minimize for message component
        EXPECTED: Message component is minimized,Application save the interaction successfully and should display next time
        """
        pass

    def test_006_user_click_on_close_icon_for_message_component_in_betslip(self):
        """
        DESCRIPTION: User click on close icon for message component in betslip
        EXPECTED: Message component is closed and application save the user interaction successfully
        """
        pass
