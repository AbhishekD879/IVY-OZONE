import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.hl
@pytest.mark.lad_prod
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305091_Verify_GA_tracking_on_getting_SYC_pop_up(BaseDataLayerTest):
    """
    TR_ID: C65305091
    NAME: Verify GA tracking on getting SYC pop-up
    DESCRIPTION: This test case is to verify GA tracking on getting SYC pop-up
    PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
    PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
    PRECONDITIONS: 3) User is in logged in state
    """
    keep_browser_open = True
    expected_response = {"event": "trackEvent",
                         "eventAction": "rendered",
                         "eventCategory": "show your colours",
                         "eventLabel": ""
                         }

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
        PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
        PRECONDITIONS: 3) User is in logged in state
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_001_open_football_sports_landing_page(self):
        """
        DESCRIPTION: Open football sports landing page
        EXPECTED: Football landing page should be displayed
        """
        self.site.open_sport(name='football', fanzone=True)

    def test_002_open_console_and_type_data_layer(self):
        """
        DESCRIPTION: Open console and type Data layer
        EXPECTED: we should able to GA track on populating SYC pop-up
        """
        self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=10)
        actual_response = self.get_data_layer_specific_object(object_key='eventAction',
                                                              object_value='rendered')
        self.compare_json_response(actual_response, self.expected_response)

    def test_003_validate_ga_tracking(self):
        """
        DESCRIPTION: Validate GA tracking
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "rendered",
        EXPECTED: "eventCategory": "show your colors",
        EXPECTED: "eventLabel": ""
        EXPECTED: })
        """
        # covered in above step
