import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@vtest
class Test_C9765550_Verify_layout_of_Next_Races_tab_on_Greyhounds(BaseRacing):
    """
    TR_ID: C9765550
    NAME: Verify layout of 'Next Races' tab on Greyhounds
    DESCRIPTION: This test case verifies layout of event cards on 'Next Races' tab
    PRECONDITIONS: 1. "Next Races" tab should be enabled in CMS (CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle-> nextRacesTabEnabled)
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Race events are available for the current day
    PRECONDITIONS: 4. Navigate to Greyhounds
    PRECONDITIONS: Note:
    PRECONDITIONS: To get info about class use link:
    PRECONDITIONS: https://tst2-backoffice-lcm.ladbrokes.com/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&existsFilter=event:simpleFilter:market.name:equals:%7CWin%20or%20Each%20Way%7C&simpleFilter=market.name:equals:%7CWin%20or%20Each%20Way%7C&priceHistory=true&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&racingForm=outcome&limitRecords=outcome:3&simpleFilter=event.siteChannels:contains:M&simpleFilter=outcome.outcomeStatusCode:equals:A&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&translationLang=en
    PRECONDITIONS: Where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: "Next Races" should be enabled in CMS (CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle-> nextRacesTabEnabled)
        PRECONDITIONS: Load Oxygen app.
        PRECONDITIONS: Tap on 'Next Races' tab on the Greyhounds.
        """
        self.get_active_events_for_category(category_id=self.ob_config.backend.ti.greyhound_racing.category_id)

        greyhound_next_races_toggle = self.get_initial_data_system_configuration().get('GreyhoundNextRacesToggle', {})
        if not greyhound_next_races_toggle:
            greyhound_next_races_toggle = self.cms_config.get_system_configuration_item('GreyhoundNextRacesToggle')
        if not greyhound_next_races_toggle.get('nextRacesTabEnabled'):
            raise CmsClientException('Next Races Tab is not enabled for greyhounds in CMS')

        if self.brand != 'ladbrokes':
            self.navigate_to_page(name='greyhounds')
            self.site.wait_content_state('Greyhounds')
        else:
            self.navigate_to_page(name='greyhound-racing')
            self.site.wait_content_state('Greyhoundracing')

    def test_001_tap_on_next_races_tab(self):
        """
        DESCRIPTION: Tap on 'Next Races' tab
        EXPECTED: * 'Next Races' tab is selected and highlighted
        EXPECTED: * Content is loaded
        """
        if self.brand == 'ladbrokes':
            next_races_tab = self.site.greyhound.tabs_menu.click_button(button_name=vec.racing.RACING_NEXT_RACES_NAME)
            self.assertTrue(next_races_tab, msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')
            self.device.refresh_page()
            self.__class__.sections = self.get_sections('greyhound-racing')
        else:
            next_races = self.get_next_races_section()
            self.__class__.sections = next_races.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No race sections are found in Next Races')

    def test_002_verify_next_races_tab_layout(self):
        """
        DESCRIPTION: Verify 'Next Races' tab layout
        EXPECTED: * Event cards are displayed one by one as the list
        """
        for event_card_name, race in self.sections.items():
            self.assertTrue(event_card_name,
                            msg="Event cards are not displayed")
