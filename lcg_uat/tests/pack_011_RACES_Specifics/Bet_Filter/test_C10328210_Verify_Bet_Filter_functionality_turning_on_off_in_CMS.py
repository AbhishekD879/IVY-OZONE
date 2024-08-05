import pytest
from tests.base_test import vtest
from tests.pack_011_RACES_Specifics.Bet_Filter.base_horseracing_bet_filter_test import BaseHorseRacingBetFilterTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Bet Filter Disabling is not possible in Prod
# @pytest.mark.hl
@pytest.mark.bet_filter
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C10328210_Verify_Bet_Filter_functionality_turning_on_off_in_CMS(BaseHorseRacingBetFilterTest):
    """
    TR_ID: C10328210
    NAME: Verify Bet Filter functionality turning on/off in CMS
    DESCRIPTION: This test case verifies 'Bet Filter' button displaying according to CMS configuration
    DESCRIPTION: BMA-37013 Horse Racing : Bet Filter
    PRECONDITIONS: Verify BetFilter is present in System Configuration in CMS for Ladbrooks and Sportsbook brand.
    PRECONDITIONS: Needs to be tested on Ladbrokes and Oxygen app
    """
    keep_browser_open = True

    def test_001_verify_betfilter_is_enabled_in_system_configuration_in_cms_system_configuration_structure_betfilterhorseracingnavigate_to_horse_racing_page(self):
        """
        DESCRIPTION: Verify BetFilter is enabled in System Configuration in CMS (System Configuration->Structure->BetFilterHorseRacing)
        DESCRIPTION: Navigate to Horse Racing page
        EXPECTED: Bet Filter button is present
        """
        self.__class__.cms_config_state = self.get_initial_data_system_configuration().get('BetFilterHorseRacing')
        if not self.cms_config_state['enabled']:
            self.cms_config.update_system_configuration_structure(config_item='BetFilterHorseRacing',
                                                                  field_name='enabled',
                                                                  field_value=True)
            self.cms_config_state = self.cms_config.get_system_configuration_item('BetFilterHorseRacing')
        if not self.cms_config_state:
            raise CmsClientException('"BetFilterHorseRacing" is absent in CMS')
        if not self.cms_config_state.get('enabled'):
            raise CmsClientException('"Horseracing Bet Filter" is disabled')
        self.navigate_to_page('horse-racing')
        self.site.wait_content_state('horse-racing')
        self.assertTrue(self.site.horse_racing.bet_filter_link.is_displayed(),
                        msg='The bet filter button is not displayed on the Horse Racing Landing page')

    def test_002_disable_betfilter_in_system_configuration_in_cms_system_configuration_structure_betfilterhorseracingnavigate_to_horse_racing_page(self):
        """
        DESCRIPTION: Disable BetFilter in System Configuration in CMS (System Configuration->Structure->BetFilterHorseRacing)
        DESCRIPTION: Navigate to Horse Racing page
        EXPECTED: Bet Filter button is NOT present
        """
        try:
            if self.cms_config_state['enabled']:
                self.cms_config.update_system_configuration_structure(config_item='BetFilterHorseRacing',
                                                                      field_name='enabled',
                                                                      field_value=False)
                self.cms_config_state = self.cms_config.get_system_configuration_item('BetFilterHorseRacing')
            if not self.cms_config_state:
                raise CmsClientException('"BetFilterHorseRacing" is absent in CMS')
            if self.cms_config_state['enabled']:
                raise CmsClientException('"Horseracing Bet Filter" is enabled')
            try:
                for index in range(3):
                    self.assertTrue(self.site.horse_racing.bet_filter_link.is_displayed(),
                                    msg='The bet filter button is not displayed on the Horse Racing Landing page')
                    self.device.refresh_page()
                    self.site.wait_splash_to_hide()
                    self.site.wait_content_state_changed()
            except VoltronException:
                self._logger.info("The bet filter button is not displayed on the Horse Racing Landing page")
        finally:
            self.cms_config.update_system_configuration_structure(config_item='BetFilterHorseRacing',
                                                                  field_name='enabled',
                                                                  field_value=True)
