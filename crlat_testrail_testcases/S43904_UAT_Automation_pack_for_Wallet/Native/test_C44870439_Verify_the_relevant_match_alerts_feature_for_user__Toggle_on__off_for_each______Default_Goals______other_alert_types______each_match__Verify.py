import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C44870439_Verify_the_relevant_match_alerts_feature_for_user__Toggle_on__off_for_each______Default_Goals______other_alert_types______each_match__Verify_the_user_is_receiving_match_alerts_other_alert_types__Verify_user_is_able_to_switch_o(Common):
    """
    TR_ID: C44870439
    NAME: "Verify the relevant match alerts feature for user - Toggle on / off  for each          -Default Goals         - other alert types         - each match - Verify the user is receiving match alerts  ,other alert types - Verify user  is able to switch o
    DESCRIPTION: "Verify the relevant match alerts feature for user
    DESCRIPTION: - Toggle on / off  for each
    DESCRIPTION: -Default Goals
    DESCRIPTION: - other alert types
    DESCRIPTION: - each match
    DESCRIPTION: - Verify the user is receiving match alerts  ,other alert types
    DESCRIPTION: - Verify user  is able to switch off all alerts"
    PRECONDITIONS: 
    """
    keep_browser_open = True
