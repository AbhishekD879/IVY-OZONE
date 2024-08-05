import pytest
import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2987535_Verify_layout_of_Next_Races_tab_at_the_Homepage(BaseRacing):
    """
    TR_ID: C2987535
    NAME: Verify layout of 'Next Races' tab at the Homepage
    DESCRIPTION: This test case verifies layout of 'Next Races' tab at the Homepage.
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Race events are available for the current day
    PRECONDITIONS: *Note:*
    PRECONDITIONS: 1) 'Next Races' tab is CMS configurable, please look at the https://ladbrokescoral.testrail.com/index.php?/cases/view/29371 test case where this process is described.
    PRECONDITIONS: 2) The number of events and selections are CMS configurable too. CMS -> system-configuration -> structure -> NextRaces.
    PRECONDITIONS: 3) To get info about class events use link:
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: 4) To get info about Extra place events use link:
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isResulted:isFalse&simpleFilter=event.isStarted:isFalse&simpleFilter=event.isLiveNowEvent:isFalse&simpleFilter=event.rawIsOffCode:notEquals:Y&existsFilter=event:simpleFilter:market.drilldownTagNames:intersects:MKTFLAG_EPR&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&racingForm=event&limitRecords=outcome:1&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        next_races_toggle = self.get_initial_data_system_configuration().get('NextRacesToggle', {})
        if not next_races_toggle:
            next_races_toggle = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if not next_races_toggle.get('nextRacesTabEnabled'):
            if tests.settings.backend_env != 'prod':
                self.cms_config.set_next_races_toggle_component_status(next_races_component_status=True)
            else:
                raise CmsClientException('Next Races Tab is not enabled in CMS')
        if tests.settings.backend_env != 'prod':
            event = self.ob_config.add_UK_racing_event(number_of_runners=1, market_extra_place_race=True,
                                                       ew_terms=self.ew_terms)
            self.__class__.event_ID = event.event_id
            self.ob_config.change_racing_promotion_state(promotion_name='extra_place_race',
                                                         level='event',
                                                         market_id=self.ob_config.market_ids[self.event_ID],
                                                         event_id=self.event_ID)

    def test_001_tap_on_next_races_tab(self):
        """
        DESCRIPTION: Tap on 'Next Races' tab
        EXPECTED: * 'Next Races' tab is selected and highlighted
        EXPECTED: * Content is loaded
        """
        self.site.wait_content_state('Homepage', timeout=20)
        next_races = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.next_races)
        self.site.home.module_selection_ribbon.tab_menu.click_button(next_races)
        sleep(3)
        if self.brand == 'Ladbrokes':
            current_tab = self.site.home.module_selection_ribbon.tab_menu.current
            self.assertEquals(current_tab, vec.racing.RACING_NEXT_RACES_NAME,
                              msg=f'Actual tab opened: "{current_tab}" is not equal to '
                                  f'Expected tab: "{vec.racing.RACING_NEXT_RACES_NAME}"')

    def test_002_verify_next_races_tab_layout(self):
        """
        DESCRIPTION: Verify 'Next Races' tab layout
        EXPECTED: * 'Extra Place' section is displayed at the top of the page (if Extra Place racing events are available)
        EXPECTED: * Event cards are displayed one by one as the list (The number of events depends on CMS configurations)
        """
        if not self.site.home.tab_content.has_extra_place_module():
            self.device.refresh_page()
            self.site.wait_splash_to_hide()

        self.assertTrue(self.site.home.tab_content.has_extra_place_module(timeout=5),
                        msg='Next Races tab has no Extra Place Module')
        sections = self.site.home.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No race sections are found in Next Races')

        for event_card_name, race in sections.items():
            self.assertTrue(event_card_name,
                            msg="Event cards are not displayed")
