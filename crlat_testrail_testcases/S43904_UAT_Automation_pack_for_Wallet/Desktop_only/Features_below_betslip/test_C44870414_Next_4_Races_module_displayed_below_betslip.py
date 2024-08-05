import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870414_Next_4_Races_module_displayed_below_betslip(Common):
    """
    TR_ID: C44870414
    NAME: Next 4 Races module displayed below betslip
    DESCRIPTION: Next 4 Races module displayed below betslip as CMS configuration
    PRECONDITIONS: Next 4 Races module is configured in CMS
    PRECONDITIONS: User loads the Ladbrokes desktop web page and log in
    """
    keep_browser_open = True

    def test_001_verify_that_next_4_races_module_is_displayed_under_betslip_area_as_per_cms_configurationverify_that_the_data_is_updated_by_pushverify_that_user_is_able_to_selectadd_to_betslip_and_place_bet(self):
        """
        DESCRIPTION: Verify that Next 4 Races module is displayed under Betslip area as per CMS configuration
        DESCRIPTION: Verify that the data is updated by push
        DESCRIPTION: Verify that user is able to select/add to betslip and place bet
        EXPECTED: Next 4 Races module feature is displayed as per configuration and works as designed
        """
        pass
