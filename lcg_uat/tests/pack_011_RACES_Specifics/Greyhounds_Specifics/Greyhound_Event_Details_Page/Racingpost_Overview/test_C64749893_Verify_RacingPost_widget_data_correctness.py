import pytest
from tests.base_test import vtest
from json import JSONDecodeError
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from voltron.utils.helpers import do_request


# @pytest.mark.tst2 # Racing Post Info is not available
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.greyhounds
@pytest.mark.other
@pytest.mark.racingpost
@vtest
class Test_C64749893_Verify_RacingPost_widget_data_correctness(BaseGreyhound):
    """
    TR_ID: C64749893
    NAME: Verify RacingPost widget data correctness
    DESCRIPTION: This testcase verifies RacingPost
    DESCRIPTION: widget data correctness
    PRECONDITIONS: User should have CMS access
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: when enabled - Racingpost info should be displayed.
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    ss_url_ladbrokes = 'https://sb-api.ladbrokes.com'
    ss_url_coral = 'https://sb-api.coral.co.uk'

    def get_response_url(self, url, event_id):
        """
        :param url: SS or Commentary url
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    data = do_request(url=request_url, method='GET')
                    pick = data['document'][event_id]['postPick']
                    return pick
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_000_preconditions(self):
        """
        PRECONDITIONS: - User should have CMS access
        PRECONDITIONS: - Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
        PRECONDITIONS: - when enabled - Racingpost info should be displayed.
        """
        racing_data_hub = self.cms_config.get_system_configuration_structure()['RacingDataHub']['isEnabledForGreyhound']
        if not racing_data_hub:
            self.cms_config.update_system_configuration_structure(config_item='RacingDataHub',
                                                                  field_name='isEnabledForGreyhound', field_value=True)

    def test_001_load_oxygen_appgo_to_the_greyhounds_landing_pageselect_event_with_racingpost_available_and_go_to_its_details_pageverify_racingpost_widgetverify_racingpost_widget_data_correctness(self):
        """
        DESCRIPTION: Load Oxygen app
        DESCRIPTION: Go to the Greyhounds landing page
        DESCRIPTION: Select event with RacingPost available and go to its details page
        DESCRIPTION: Verify RacingPost widget
        DESCRIPTION: Verify RacingPost widget data correctness.
        EXPECTED: Homepage is loaded
        EXPECTED: Greyhounds landing page is opened
        EXPECTED: * Event details page is opened
        EXPECTED: * RacingPost widget is located in Main Column under selections list
        EXPECTED: RacingPost consists of racing post image (as per the Zeplin links) based on the previous performance of the dogs (ratings).
        EXPECTED: * the value after racingpost widget should be same as postpick attribute from API response in network tab.
        """
        self.navigate_to_page('Homepage')
        event_id = self.get_event_details(racing_post_pick=True).event_id
        self.navigate_to_edp(event_id=event_id, sport_name='greyhound-racing')
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.greyhound_event_details.tab_content.post_info.has_logo_icon(),
                        msg='Racing Post logo icon is not found')
        url = self.ss_url_coral if self.brand == 'bma' else self.ss_url_ladbrokes
        post_pick_response = self.get_response_url(url=url,event_id=event_id)
        post_pick_ui =[silk.split("gh")[-1] for silk in self.site.greyhound_event_details.tab_content.post_info.items_names]
        post_pick_final = ""
        for post_pick in post_pick_ui:
            post_pick_final += post_pick + '-'
        post_pick = post_pick_final[:-1]
        self.assertEqual(post_pick, post_pick_response, msg=f'Post pick attribute value in UI "{post_pick}" is not same as response value "{post_pick_response}"')
