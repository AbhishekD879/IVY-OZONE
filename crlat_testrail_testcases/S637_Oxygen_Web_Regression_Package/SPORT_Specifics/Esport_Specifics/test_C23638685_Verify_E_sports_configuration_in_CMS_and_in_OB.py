import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C23638685_Verify_E_sports_configuration_in_CMS_and_in_OB(Common):
    """
    TR_ID: C23638685
    NAME: Verify  E-sports configuration in CMS and in OB.
    DESCRIPTION: This test case verifies E-sports correct configuration.
    DESCRIPTION: Created to cover this Prod Incident - https://jira.egalacoral.com/browse/BMA-37381
    PRECONDITIONS: To verify correctness of configuration you need to check it in CMS:
    PRECONDITIONS: SPORT PAGES -> SPORT CATEGORIES -> ESPORTS
    PRECONDITIONS: Category ID - 148
    PRECONDITIONS: SS Category Code - ESPORTS
    PRECONDITIONS: Also you need to check configuration in according Back office:
    PRECONDITIONS: Check Market template - |Match Result (2 way)| with Display Sort - HH
    """
    keep_browser_open = True

    def test_001_verify_that_the_newly_created_e_sports_event_is_visible_of_the_fe(self):
        """
        DESCRIPTION: Verify that the newly created E-sports event is visible of the FE.
        EXPECTED: If the configuration is correct, then the user should see the newly created event on the FE.
        """
        pass

    def test_002_verify_that_response_is_correct_dev_toolsnetwork_tab(self):
        """
        DESCRIPTION: Verify that response is correct dev tools/network tab.
        EXPECTED: Data should have the following parameters in SS response for the Esports event:
        EXPECTED: categoryCode: "ESPORTS"
        EXPECTED: categoryId: "148"
        EXPECTED: categoryName: "ESports"
        """
        pass
