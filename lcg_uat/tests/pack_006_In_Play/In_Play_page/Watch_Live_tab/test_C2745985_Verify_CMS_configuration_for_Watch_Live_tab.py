import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from tenacity import retry, wait_fixed, retry_if_exception_type, stop_after_attempt


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot enable or disable in CMS for prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C2745985_Verify_CMS_configuration_for_Watch_Live_tab(Common):
    """
    TR_ID: C2745985
    NAME: Verify CMS configuration for 'Watch Live' tab
    DESCRIPTION: This test case verifies CMS configuration for 'Watch Live' tab
    PRECONDITIONS: 1. 'InPlayWatchLive' should be disabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: 2. Load Oxygen app and navigate to 'In-Play' page
    """
    keep_browser_open = True

    @classmethod
    def custom_tearDown(cls, **kwargs):
        inplay_watch_live_section = cls.get_initial_data_system_configuration().get('InPlayWatchLive', {})
        if not inplay_watch_live_section:
            inplay_watch_live_section = cls.get_cms_config().get_system_configuration_item('InPlayWatchLive')
        if not inplay_watch_live_section.get('enabled'):
            cls.get_cms_config().update_system_configuration_structure(config_item='InPlayWatchLive',
                                                                       field_name='enabled',
                                                                       field_value=True)

    @retry(stop=stop_after_attempt(15), retry=retry_if_exception_type((VoltronException)),
           wait=wait_fixed(wait=2),
           reraise=True)
    def verify_watchlive_to_be_reflected(self, watchlive_status=True):
        try:
            self.__class__.inplay = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
            watchlive = list(self.inplay.keys())[0]
            if watchlive_status:
                self.assertEqual(watchlive, vec.sb.WATCH_LIVE_LABEL)
            else:
                self.assertNotEqual(watchlive, vec.sb.WATCH_LIVE_LABEL)
        except Exception:
            self.delete_cookies()
            self.navigate_to_page('in-play')
            raise VoltronException("The element not found")

    def test_001_verify_displaying_of_watch_live_tabicon_at_in_play_sports_ribbon(self):
        """
        DESCRIPTION: Verify displaying of 'Watch Live' tab/icon at 'In-Play' sports ribbon
        EXPECTED: * 'Watch Live' tab/icon is NOT displayed at'In-Play' sports ribbon
        EXPECTED: * User is landed on the FIRST sport in the ribbon by default e.g. Football
        """
        self.cms_config.update_system_configuration_structure(config_item='InPlayWatchLive',
                                                              field_name='enabled',
                                                              field_value=False)
        self.navigate_to_page('in-play')
        self.site.wait_content_state_changed(timeout=10)
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=10)
        self.verify_watchlive_to_be_reflected(watchlive_status=False)
        self.__class__.expected_order_of_sports = list(self.inplay.keys())[1:]
        first_sport = list(self.inplay.values())[1]
        default_sport = first_sport.name.lower()
        self.assertIn(default_sport, self.device.get_current_url())

    def test_002_go_to_cms__system_configuration__enable_inplaywatchlive_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS > System Configuration > enable 'InPlayWatchLive' and save changes
        EXPECTED:
        """
        self.cms_config.update_system_configuration_structure(config_item='InPlayWatchLive',
                                                              field_name='enabled',
                                                              field_value=True)
        self.navigate_to_page('in-play')
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=10)

    def test_003___go_to_oxygen_app__refresh_in_play_page__verify_displaying_of_watch_live_tabicon(self):
        """
        DESCRIPTION: - Go to Oxygen app
        DESCRIPTION: - Refresh 'In-Play page'
        DESCRIPTION: - Verify displaying of 'Watch Live' tab/icon
        EXPECTED: * 'Watch Live' tab/icon is displayed at 'In-Play' sports ribbon as the first icon
        EXPECTED: * Order of other sport icons remains unchanged
        EXPECTED: * User is landed on the FIRST sport in the ribbon by default e.g. Football
        """
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=10)
        self.verify_watchlive_to_be_reflected(watchlive_status=True)
        actual_order_of_sports = list(self.inplay.keys())[1:]
        self.assertEqual(actual_order_of_sports, self.expected_order_of_sports)
        first_sport = list(self.inplay.values())[1]
        default_sport = first_sport.name.lower()
        self.assertIn(default_sport, self.device.get_current_url())

    def test_004_go_to_cms__system_configuration__disable_inplaywatchlive_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS > System Configuration > disable 'InPlayWatchLive' and save changes
        EXPECTED:
        """
        # covered in above step

    def test_005___go_to_oxygen_app__refresh_in_play_page__verify_displaying_of_watch_live_tabicon(self):
        """
        DESCRIPTION: - Go to Oxygen app
        DESCRIPTION: - Refresh 'In-Play page'
        DESCRIPTION: - Verify displaying of 'Watch Live' tab/icon
        EXPECTED: * 'Watch Live' tab/icon is NOT displayed at'In-Play' sports ribbon
        EXPECTED: * User is landed on the FIRST sport in the ribbon by default e.g. Football
        """
        # covered in above step
