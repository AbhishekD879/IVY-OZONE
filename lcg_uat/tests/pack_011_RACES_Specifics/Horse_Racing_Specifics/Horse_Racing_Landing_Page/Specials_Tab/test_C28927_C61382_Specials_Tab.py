import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.specials
@pytest.mark.each_way
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C28927_C61382_Specials_Tab(BaseRacing):
    """
    TR_ID: C28927
    TR_ID: C61382
    NAME: Specials Tab
    DESCRIPTION: This test case verifies 'Specials' tab on horse Racing landing page
    PRECONDITIONS: To retrieve an information from the Site Server (tst2) use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/227?translationLang=LL
    PRECONDITIONS: Where *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: *   Horse Racing **categoryId**=21
    PRECONDITIONS: *   **'typeName'** on event level to identify needed event types to be displayed on the application
    PRECONDITIONS: *   **'display order' **on type level to identify order of competitions displaying
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing specials events with Each Way terms and SP/LP prices
        EXPECTED: Events are created in OB
        PRECONDITIONS: To retrieve an information from the Site Server (tst2) use the following link:
        PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/227?translationLang=LL
        PRECONDITIONS: Where *X.XX - current supported version of OpenBet release*
        PRECONDITIONS: LL - language (e.g. en, ukr)
        PRECONDITIONS: See attributes:
        PRECONDITIONS: *   Horse Racing **categoryId**=21
        PRECONDITIONS: *   **'typeName'** on event level to identify needed event types to be displayed on the application
        PRECONDITIONS: *   **'display order' **on type level to identify order of competitions displaying
        """
        self.ob_config.add_racing_specials_event(number_of_runners=2,
                                                 ew_terms=self.ew_terms, time_to_start=20)
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2)
        self.__class__.eventUK_ID = event_params.event_id
        event_off_time = event_params.event_off_time
        self.__class__.uk_event_name = f'{event_off_time} {self.horseracing_autotest_uk_name_pattern.upper()}'
        self.ob_config.add_mobile_exclusive_racing_event()
        self.ob_config.add_price_bomb_racing_event()

    def test_001_tap_horse_racing_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Horse Racing' icon on the Sports Menu Ribbon
        EXPECTED: 'Horse Racing' landing page is opened
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_002_click_tap_specials_tab(self):
        """
        DESCRIPTION: Click / tap 'Specials' tab
        EXPECTED: 'Specials' tab is opened
        """
        self.site.horse_racing.tabs_menu.click_button('SPECIALS')

    def test_003_verify_competition_section_displaying(self):
        """
        DESCRIPTION: Verify competition section displaying
        EXPECTED: *   Coral: All competitions are expanded by default;
        EXPECTED: *   All competitions are collapsible, expandable.
        """
        self.__class__.sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No sections found on Specials page')
        for section_name, section in self.sections.items():
            section.scroll_to()
            if self.brand != 'ladbrokes':
                self.assertTrue(section.is_expanded(), msg=f'Section "{section_name}" is not expanded by default')
            else:
                section.expand()

    def test_004_verify_competition_section_name(self):
        """
        DESCRIPTION: Verify competition section name
        EXPECTED: Competition section name corresponds to **'typeName'** attribute in response from SiteServer
        """
        price_bomb = vec.racing.PRICE_BOMB_NAME.title() if self.device_type == 'desktop' and self.brand != 'ladbrokes' else vec.racing.PRICE_BOMB_NAME
        mobile_exclusive = vec.racing.MOBILE_EXCLUSIVE_NAME.title() if self.device_type == 'desktop' and self.brand != 'ladbrokes' else vec.racing.MOBILE_EXCLUSIVE_NAME
        racing_specials = vec.racing.RACING_SPECIALS_NAME.title() if self.device_type == 'desktop' and self.brand != 'ladbrokes' else vec.racing.RACING_SPECIALS_NAME
        self.assertIn(price_bomb, self.sections,
                      msg=f'Price Bomb section was not found in list of sections "{", ".join(self.sections)}"')

        self.assertIn(mobile_exclusive, self.sections,
                      msg=f'Mobile Exclusive section was not found in list of sections "{", ".join(self.sections)}"')

        self.assertIn(racing_specials, self.sections,
                      msg=f'Racing Specials section was not found in list of sections "{", ".join(self.sections)}"')

    def test_005_verify_competition_section_ordering(self):
        """
        DESCRIPTION: Verify competition section ordering
        EXPECTED: - Competition sections are ordered by **display order **in ascending order** **on type level
        EXPECTED: - Alphabetical order in second instance if display order is the same on type level
        """
        query = self.ss_query_builder
        resp = self.ss_req.ss_event_to_outcome_for_class(class_id=(self.ob_config.horseracing_config.horse_racing_live.class_id,
                                                                   self.ob_config.horseracing_config.daily_racing_specials.class_id,
                                                                   self.ob_config.horseracing_config.horse_racing_specials.class_id),
                                                         query_builder=query)
        types_disp_order = set(
            [(event['event']['typeName'], int(event['event']['typeDisplayOrder'])) for event in resp])
        sections_by_disp_order = [x for x, _ in sorted(types_disp_order, key=lambda x: (x[1], x[0]))]
        intersection = [x for x in self.sections if x.title() in sections_by_disp_order]
        self.assertListEqual(list(self.sections.keys()), intersection,
                             msg='Sections order "%s" is not the same as expected "%s"'
                                 % (list(self.sections.keys()), intersection))

    def test_006_check_special_event_displaying_for_events_which_are_not_related_to_any_of_the_following_groups_uk_ie_int_vr(self):
        """
        DESCRIPTION: Check special event displaying for events which are NOT related to any of the following groups:
        DESCRIPTION: - UK
        DESCRIPTION: - IE
        DESCRIPTION: - INT
        DESCRIPTION: - VR
        EXPECTED: Event is not displayed
        EXPECTED: All events with special flag which are related to Horse Racing category are shown
        """
        query = self.ss_query_builder
        query.add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.INTERSECTS, 'SP')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_RESULTED, OPERATORS.IS_FALSE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                      self.start_date_minus))
        resp = self.ss_req.ss_event_to_outcome_for_class(class_id=(self.ob_config.horseracing_config.horse_racing_live.class_id,
                                                                   self.ob_config.horseracing_config.daily_racing_specials.class_id,
                                                                   self.ob_config.horseracing_config.horse_racing_specials.class_id),
                                                         query_builder=query)

        events_list_ss = []
        for event_resp in resp:
            events_list_ss.append(event_resp['event']['id'].strip())
        self.assertNotIn(self.eventUK_ID, events_list_ss, msg=f'{self.eventUK_ID} found in {events_list_ss}')

        for section_name, section in self.sections.items():
            section.scroll_to()
            events = section.items_as_ordered_dict
            self.assertNotIn(self.uk_event_name, events.keys(),
                             msg=f'"{self.uk_event_name}" found in section "{section_name}" in "{events.keys()}"')
