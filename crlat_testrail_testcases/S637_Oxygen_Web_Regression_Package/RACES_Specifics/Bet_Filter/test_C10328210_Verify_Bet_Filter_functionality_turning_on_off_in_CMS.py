import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C10328210_Verify_Bet_Filter_functionality_turning_on_off_in_CMS(Common):
    """
    TR_ID: C10328210
    NAME: Verify Bet Filter functionality turning on/off in CMS
    DESCRIPTION: This test case verifies 'Bet Filter' button displaying according to CMS configuration
    DESCRIPTION: BMA-37013 Horse Racing : Bet Filter
    PRECONDITIONS: Verify BetFilter is present in System Configuration in CMS for Ladbrooks and Sportsbook brand.
    PRECONDITIONS: Needs to be tested on Ladbrokes and Oxygen app
    """
    keep_browser_open = True

    def test_001_verify_betfilter_is_enabled_in_system_configuration_in_cms_system_configuration_gtstructure_gtbetfilterhorseracingnavigate_to_horse_racing_page(self):
        """
        DESCRIPTION: Verify BetFilter is enabled in System Configuration in CMS (System Configuration-&gt;Structure-&gt;BetFilterHorseRacing)
        DESCRIPTION: Navigate to Horse Racing page
        EXPECTED: Bet Filter button is present
        """
        pass

    def test_002_disable_betfilter_in_system_configuration_in_cms_system_configuration_gtstructure_gtbetfilterhorseracingnavigate_to_horse_racing_page(self):
        """
        DESCRIPTION: Disable BetFilter in System Configuration in CMS (System Configuration-&gt;Structure-&gt;BetFilterHorseRacing)
        DESCRIPTION: Navigate to Horse Racing page
        EXPECTED: Bet Filter button is NOT present
        """
        pass
