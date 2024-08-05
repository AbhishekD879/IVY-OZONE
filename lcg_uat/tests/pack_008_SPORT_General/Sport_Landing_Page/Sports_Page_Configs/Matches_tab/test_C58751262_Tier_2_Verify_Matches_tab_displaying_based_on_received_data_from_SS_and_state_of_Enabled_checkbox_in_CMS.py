import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot update tabs in CMS beta/Prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C58751262_Tier_2_Verify_Matches_tab_displaying_based_on_received_data_from_SS_and_state_of_Enabled_checkbox_in_CMS(Common):
    """
    TR_ID: C58751262
    NAME: [Tier 2] Verify 'Matches' tab displaying based on received data from SS and state of 'Enabled' checkbox in CMS
    DESCRIPTION: This test case verifies 'Matches' tab displaying based on received data from SS and state of 'Enabled' checkbox in CMS
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Tier 2 Sport Landing page where 'Matches' tab is enabled in CMS ('checkEvents: true' is set by default for Tier 2 and can not be edited)
    PRECONDITIONS: 3. No sport modules should be created (i.e. Inplay module, Quick Links, Highlight Carousel, etc)
    PRECONDITIONS: 4. No live events should be configured
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - 'Matches' tab is available in CMS for all Tier types
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use <sport-config> response:
    PRECONDITIONS: https://<particular env e.g. sports-red-tst2.ladbrokes.com>/cms/api/<Brand>/sport-config/<Category ID>
    PRECONDITIONS: **NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead:**
    PRECONDITIONS: ![](index.php?/attachments/get/100267212)
    PRECONDITIONS: ![](index.php?/attachments/get/100267213)
    PRECONDITIONS: - To verify Matches availability on SS use the next link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToMarketForClass/XXXXX?&simpleFilter=event.categoryId:intersects:XX&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.startTime:greaterThanOrEqual:2019-03-20T22:00:00.000Z&existsFilter=event:simpleFilter:market.dispSortName:intersects:MR&simpleFilter=event.suspendAtTime:greaterThan:2019-03-21T13:32:30.000Z&translationLang=en&count=event:market
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XX - Category Id
    PRECONDITIONS: - XXXXX - Class Id
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load the app
        PRECONDITIONS: Go to the IceHockey Landing Page -> 'Click on Matches Tab'
        """
        if tests.settings.backend_env != 'prod':
            event = self.ob_config.add_ice_hockey_event_to_ice_hockey_usa()
            self.__class__.eventID = event.event_id
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                   query_builder=self.ss_query_builder)
            full_section_name = event.ss_response['event']['categoryCode'] + self.get_accordion_name_for_event_from_ss(
                event=event_resp[0])
            self.__class__.section_name = full_section_name.replace('ICE_HOCKEY', '')

    def test_001_verify_matches_tab_displaying_if_enabled_checkbox_is_ticked_and_data_is_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Matches' tab displaying if 'Enabled' checkbox is ticked and data is available on SS
        EXPECTED: * 'Matches' tab is present on Sports Landing page
        EXPECTED: * 'Matches' tab is received in <sport-config> response with 'hidden: false' parameter
        EXPECTED: * List of events received from SS is displayed
        EXPECTED: * Response with available data for 'Matches' tab is received from SS
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        """
        self.navigate_to_page(name='sport/ice-hockey')
        self.site.wait_content_state(state_name='IceHockey')
        config = self.cms_config.get_sport_config(category_id=self.ob_config.ice_hockey_config.category_id)
        self.assertFalse(config.get('tabs')[4].get('hidden'), msg='"hidden" parameter is not "false"')
        self.__class__.expected_tab_name = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                    self.ob_config.ice_hockey_config.category_id)
        current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected Tab: '
                             f'"{self.expected_tab_name}"')

    def test_002_verify_matches_tabs_displaying_if_enabled_checkbox_is_ticked_and_data_is_not_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Matches' tabs displaying if 'Enabled' checkbox is ticked and data is NOT available on SS
        EXPECTED: * 'Matches' tab is NOT present on Sports Landing page
        EXPECTED: * 'Matches' tab is received in <sport-config> response with 'hidden: true' parameter
        EXPECTED: * Response is not received from SS
        EXPECTED: * The first tab is selected by default instead of 'Matches'
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        EXPECTED: **For Desktop:**
        EXPECTED: 'Matches' tab is present on Sports Landing page all the time regardless of cms settings or data availability
        """
        # This step can not be automated

    def test_003_verify_matches_tabs_displaying_if_enabled_checkbox_is_unticked_and_data_is_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Matches' tabs displaying if 'Enabled' checkbox is unticked and data is available on SS
        EXPECTED: * 'Matches' tab is NOT present on Sports Landing page
        EXPECTED: * 'Matches' tab is received in <sport-config> response with 'hidden: true' parameter
        EXPECTED: * Response with available data for 'Matches' tab is NOT received from SS
        EXPECTED: * The first tab is selected by default instead of 'Matches'
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        EXPECTED: **For Desktop:**
        EXPECTED: 'Matches' tab is present on Sports Landing page all the time regardless of cms settings or data availability
        """
        tab_id = self.cms_config.get_sport_tab_id(sport_id=self.ob_config.ice_hockey_config.category_id,
                                                  tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)
        self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="false",
                                                 sport_id=self.ob_config.ice_hockey_config.category_id)
        matches_tab = self.site.sports_page.tabs_menu.items_as_ordered_dict.get(self.expected_tab_name)

        wait_for_result(lambda: matches_tab,
                        name='Waiting for Matches tab to hide',
                        timeout=30)
        self.device.refresh_page()
        sleep(3)
        config = self.cms_config.get_sport_config(category_id=self.ob_config.ice_hockey_config.category_id)
        is_hidden = config.get('tabs')[4].get('hidden')
        if is_hidden and self.device_type == 'mobile':
            self.assertFalse(self.site.sports_page.tabs_menu.items_as_ordered_dict['MATCHES'].is_displayed(),
                             msg='"Matches" tab is still displayed')
        else:
            self.assertTrue(self.site.sports_page.tabs_menu.items_as_ordered_dict['MATCHES'].is_displayed(),
                            msg='"Matches" tab is still displayed')
