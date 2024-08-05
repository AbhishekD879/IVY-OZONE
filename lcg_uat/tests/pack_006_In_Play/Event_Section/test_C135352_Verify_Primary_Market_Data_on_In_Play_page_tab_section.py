import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.exceptions.precondition_not_met_exception import PreconditionNotMetException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.in_play
@vtest
class Test_C135352_Verify_Primary_Market_Data_on_In_Play_page_tab_section(Common):
    """
    TR_ID: C135352
    NAME: Verify Primary Market Data on 'In-Play' page/tab/section
    DESCRIPTION: This test case verifies Primary Market Data on 'In-Play Sports' page/tab/section
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach Upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To configure In-Play module on Sports Landing page: https://ladbrokescoral.testrail.com/index.php?/cases/view/8146654
    PRECONDITIONS: * To configure In-Play module on Home page: https://ladbrokescoral.testrail.com/index.php?/cases/view/3019589
    PRECONDITIONS: * 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: * For 'Outrights' events NO market is shown on the page
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX"
    PRECONDITIONS: where:
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    PRECONDITIONS: ![](index.php?/attachments/get/40740)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/Get inplay events
        """
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_autotest_premier_league_football_event(is_live=True, img_stream=True)
        self.navigate_to_page('in-play')
        self.site.wait_content_state(state_name='InPlay')
        if self.device_type == 'mobile':
            self.__class__.leagues = self.site.inplay.tab_content.live_now.items_as_ordered_dict
        else:
            self.__class__.leagues = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict

    def test_001_verify_live_vent_with_available_selections(self):
        """
        DESCRIPTION: Verify live vent with available selections
        EXPECTED: Only selections that belong to the Market with the following attributes are shown on the In-Play page:
        EXPECTED: *   Market's attribute 'siteCannels' contains 'M'
        EXPECTED: *   Attribute 'isMarketBetInRun="true"' is present
        EXPECTED: *   All selections in such market have 'outcomeMeaningMajorCode="MR"/"HH"'
        EXPECTED: *   All selections in such market have attribute 'siteCannels' contains 'M'
        """
        if self.leagues:
            length = len(list(self.leagues.keys()))
            number_of_leagues = 2 if length > 3 else length
            for league in list(self.leagues.values())[:number_of_leagues]:
                if not league.is_expanded():
                    league.expand()
                events = league.items_as_ordered_dict
                length = len(list(events.keys()))
                number_of_events = 2 if length > 3 else length
                for event in list(events.values())[:number_of_events]:
                    event_id = event.template.event_id
                    event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)[0]['event']['children']
                    for markets in event_details:
                        market = markets['market']
                        if 'children' in market:
                            market_details = market['children']
                            self.assertIn('M', market['siteChannels'], msg='Market attribute "siteChannels" does not contain "M".')
                            for outcomes in market_details:
                                outcome = outcomes['outcome']
                                self.assertIn('M', outcome['siteChannels'], msg='Outcome attribute "siteChannels" does not contain "M".')
                                self.assertTrue('MR' or 'HH' in outcome['outcomeMeaningMajorCode'], msg='Outcome attribute "outcomeMeaningMajorCode" does not contain "MR/HH"')
        else:
            raise PreconditionNotMetException('No live events found to test')

    def test_002_navigate_to_upcoming_events_and_repeat_step_1(self):
        """
        DESCRIPTION: Navigate to upcoming events and repeat step 1
        EXPECTED: Only selections that belong to the Market with the following attributes are shown on the In-Play page:
        EXPECTED: *   Market's attribute 'siteCannels' contains 'M'
        EXPECTED: *   Attribute 'isMarketBetInRun="true"' is present
        EXPECTED: *   All selections in such market have 'outcomeMeaningMajorCode="MR"/"HH"'
        EXPECTED: *   All selections in such market have attribute 'siteCannels' contains 'M'
        """
        if self.device_name == 'Desktop Chrome':
            self.site.inplay.tab_content.grouping_buttons.click_button('UPCOMING')
            self.leagues = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        else:
            self.leagues = self.site.inplay.tab_content.upcoming.items_as_ordered_dict
        self.test_001_verify_live_vent_with_available_selections()

    def test_003_repeat_step_1_on_sports_landing_page__matches_tab__in_play_module_for_mobiletablet_homepage__featured_tab__in_play__module_for_mobiletablet_sports_landing_page__in_play_widget_for_desktop_homepage__in_play__live_stream_section__in_play_switcher_for_desktop(self):
        """
        DESCRIPTION: Repeat step 1 on:
        DESCRIPTION: * Sports Landing page > 'Matches' tab > 'In-play' module **For Mobile/Tablet**
        DESCRIPTION: * Homepage > 'Featured' tab > 'In-play'  module **For Mobile/Tablet**
        DESCRIPTION: * Sports Landing page > 'In-play' widget **For Desktop**
        DESCRIPTION: * Homepage > 'In-Play & Live Stream ' section > 'In-Play' switcher **For Desktop**
        """
        # cannot get event id from inplay widget as there is no attribute in inspect element

        if self.device_type == 'mobile':
            self.navigate_to_page('sport/football')
            self.site.wait_content_state('FOOTBALL')
            self.site.football.tabs_menu.click_item('IN-PLAY')
            self.leagues = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            self.test_001_verify_live_vent_with_available_selections()
        self.navigate_to_page('homepage')
        self.site.wait_content_state('homepage')
        if self.device_type != 'mobile':
            self.site.home.desktop_modules.inplay_live_stream_module.tabs_menu.click_button(vec.sb.LIVE_STREAM.upper())
            try:
                self.leagues = self.site.home.get_module_content('IN-PLAY AND LIVE STREAM').accordions_list.items_as_ordered_dict
            except VoltronException:
                self._logger.warning('No events found in "LIVE STREAM" section')
        if self.device_type == 'mobile':
            self.leagues = self.site.home.tab_content.in_play_module.items_as_ordered_dict
        self.test_001_verify_live_vent_with_available_selections()

    def test_004_repeat_steps_1_2_on_home_page__in_play_tab_for_mobiletablet_sports_landing_page__in_play_tab_in_play_page__watch_live_tab(self):
        """
        DESCRIPTION: Repeat steps 1-2 on:
        DESCRIPTION: * Home page > 'In-Play' tab **For Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        DESCRIPTION: * 'In-play' page > 'Watch live' tab
        """
        if self.device_type == 'mobile':
            self.site.home.tabs_menu.click_button('IN-PLAY')
            sports = self.site.home.tab_content.live_now.items_as_ordered_dict
            sport = list(sports.values())[0]
            if not sport.is_expanded():
                sport.expand()
            self.leagues = sport.items_as_ordered_dict
            self.test_001_verify_live_vent_with_available_selections()
        else:
            self.navigate_to_page('sport/football')
            self.site.wait_content_state('FOOTBALL')
            self.site.football.tabs_menu.click_item('IN-PLAY')
            self.leagues = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            self.test_001_verify_live_vent_with_available_selections()
        self.navigate_to_page('in-play')
        self.site.wait_content_state(state_name='InPlay')
        self.site.inplay.inplay_sport_menu.click_item(vec.sb.WATCH_LIVE_LABEL)
        if self.device_type == 'mobile':
            sports = self.site.inplay.tab_content.live_now.items_as_ordered_dict
        else:
            sports = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        sport = list(sports.values())[0]
        if not sport.is_expanded():
            sport.expand()
        self.leagues = sport.items_as_ordered_dict
        self.test_001_verify_live_vent_with_available_selections()
