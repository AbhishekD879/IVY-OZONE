import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C106002_Tracking_of_Session_Expiration_Message(Common):
    """
    TR_ID: C106002
    NAME: Tracking of Session Expiration Message
    DESCRIPTION: This test case verifies tracking of session expiration message
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: [BMA-15964 (Session Limit - Expiration Message)] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-15964
    PRECONDITIONS: - User is just logged out with session expiration message
    PRECONDITIONS: * user can be logged out because of session time limits
    PRECONDITIONS: * user can be logged out because session is over on the server (i.e. when users logs out from the second tab, being logged in on the first)
    PRECONDITIONS: - Browser console is opened
    PRECONDITIONS: - Test case should be run on Mobile, Tablet and Desktop
    """
    keep_browser_open = True

    def test_001_right_after_session_expiration_message_appears_type_in_console_datalayer_press_enter_and_expand_needed_object_should_be_from_the_last_ones(self):
        """
        DESCRIPTION: Right after session expiration message appears type in console dataLayer, press 'Enter' and expand needed Object (should be from the last ones)
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: * 'event':  'trackPageview'
        EXPECTED: *  'virtualUrl' : '/session-expiration'
        EXPECTED: * 'sessionLimit' : '<session limit>'
        EXPECTED: where <session limit> is equal to what the user has selected in their account settings
        """
        pass

    def test_002_repeats_step_1_for_different_session_limits_setting_at_least_for_not_defined_and_any_other_limit_set(self):
        """
        DESCRIPTION: Repeats step #1 for different Session Limits setting (at least for 'Not defined' and any other limit set)
        EXPECTED: 
        """
        pass
