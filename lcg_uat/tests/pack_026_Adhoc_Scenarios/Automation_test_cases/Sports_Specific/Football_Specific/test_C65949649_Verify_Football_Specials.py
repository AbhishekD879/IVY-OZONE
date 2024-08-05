import pytest
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.adhoc_suite
@pytest.mark.sports_specific
@pytest.mark.football_specific
@vtest
class Test_C65949649_Verify_Football_Specials(Common):
    """
    TR_ID: C65949649
    NAME: Verify Football Specials
    DESCRIPTION: This test case verifies Football Specials
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. Make sure that the 'Specials' tab is available
    PRECONDITIONS: 4. Specials should be configured in OB
    """
    keep_browser_open = True
    sport_name = vec.sb.FOOTBALL

    def extract_event_id_from_url(self):
        """
        Function to extract the last numbers(event id) from the URL
        """
        current_url = self.device.get_current_url()
        parts = current_url.split('/')
        for part in reversed(parts):
            if part.isnumeric():
                return part

    def test_000_preconditions(self):
        """
        Description : checking outrights tab is enable or disable in cms
        Description : if it is disabled making it enable in cms
        Description : getting all outright events
        """
        # checking whether specials tab is enable or disable
        sport_id = self.ob_config.football_config.category_id
        response = self.cms_config.get_sports_tab_data(sport_id=sport_id, tab_name='specials')
        # making specials tab is enabled in cms if it is disable in cms
        if not response['enabled']:
            tab_id = self.cms_config.get_sport_tab_id(sport_id=sport_id,
                                                      tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials)
            self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="true",
                                                     sport_id=sport_id)

    def test_001_verify_layout_of_specials_tab(self):
        """
        DESCRIPTION: Verify layout of 'Specials' tab
        EXPECTED: Desktop and Mobile:
        EXPECTED: Special accordians should be displayed. All accordians are collapsible, expandable.
        """
        self.site.open_sport(name='FOOTBALL')
        current_tab_name = self.site.football.tabs_menu.current.upper()
        expected_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper()
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Default tab is not "{expected_tab_name}", it is "{current_tab_name}"')
        # navigating to football specials tab
        specials_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.specials.upper()
        specials_tab = self.site.football.tabs_menu.click_button(specials_tab_name)
        # Waiting for specials tab to load
        wait_for_haul(2)
        current_tab_name = self.site.football.tabs_menu.current.upper()
        self.assertEqual(current_tab_name, specials_tab_name,
                         msg=f'{current_tab_name} is not expected as {specials_tab_name}')
        self.assertTrue(specials_tab, msg=f'"{specials_tab_name}" is not opened')
        # getting accordions in specials tab and checking whether each accordion is expanded and collapsed
        sections = list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(sections, msg=f'no accordions are found')
        length = 3 if len(sections) > 3 else len(sections)
        for i in range(0, length):
            sections[i].expand()
            self.assertTrue(sections[i].is_expanded(), msg='section is not expanded')
            sections[i].collapse()
            self.assertFalse(sections[i].is_expanded(), msg='section is not Collapsed')

    def test_002_verify_special__page(self):
        """
        DESCRIPTION: Verify Special  page
        EXPECTED: Selection name which is related to special market is shown
        EXPECTED: Corresponding price/odds button is shown next to selection (if available). Was price should be displayed (if available)
        """
        special_accordions = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
        sp_accordion_name, sp_accordion_value = next(iter(special_accordions.items()))
        self.assertTrue(sp_accordion_name.upper().__contains__("SPECIALS"), msg=f'Special markets are not available')
        sp_accordion_value.expand()
        sp_accordions_items = sp_accordion_value.items_as_ordered_dict
        for sp_accordions_item in sp_accordions_items.values():
            # verifying odds for special market
            odds = sp_accordions_item.template.bet_button.name
            self.assertTrue(odds, msg=f'odds are not displaying')

    def test_003_click_and_navigate_to_specials_event_details_page(self):
        """
        DESCRIPTION: Click and navigate to specials event details page
        EXPECTED: Desktop :
        EXPECTED: All markets and other market tabs should be displayed
        EXPECTED: Mobile:
        EXPECTED: Pills should be displayed
        EXPECTED: By default All markets tab should be selected
        EXPECTED: Note: If special events are in outright view, the selections in specials EDP are in list view
        """
        # expanding first accordion
        first_accordion = list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        first_accordion.expand()
        self.assertTrue(first_accordion.is_expanded(), msg='section is not expanded')
        # clicking on event under accordion
        events = list(first_accordion.items_as_ordered_dict.values())
        self.assertTrue(events, msg=f'Events are not found')
        # clicking on first event in accordian
        events[0].click()
        # waiting for event details page to be load
        wait_for_haul(5)
        self.site.wait_content_state(state_name='EventDetails')
        # checking whether Event accordions are collapsible and expandable in EDP
        selections = list(self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict.values())
        length = 1 if len(selections) > 1 else len(selections)
        for i in range(0, length):
            selections[i].expand()
            self.assertTrue(selections[i].is_expanded(), msg='selection is not expanded')
            selections[i].collapse()
            self.assertFalse(selections[i].is_expanded(), msg='selection is not collapsed')
        # clicking on first event and checking whether it has grouping button or not
        self.__class__.selection_name, self.__class__.selection = next(iter(self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict.items()))
        self.selection.expand()
        self.assertTrue(self.selection.is_expanded(), msg='selection is not expanded')
        # verifying pills are visible for event or not
        if self.selection_name.upper() == ('ODDS BOOSTERS' if self.brand == "bma" else 'PRICE BOOST'):
            self.assertFalse(self.site.sport_event_details.has_pills(), msg=f'grouping buttons are present in event details page')
        else:
            self.assertTrue(self.site.sport_event_details.has_pills(), msg=f'grouping buttons are not in event details page')
            # verifying 'ALL MARKETS' selected by default
            grouping_button_name, grouping_button = next(iter(self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict.items()))
            if grouping_button_name.upper() == 'ALL MARKETS':
                self.assertTrue(grouping_button.is_selected(), msg=f'{grouping_button} grouping button is not selected by default')
            else:
                self.assertFalse(grouping_button.is_selected(), msg=f'{grouping_button} grouping button is selected by default')

    def test_004_verify_event_accordions(self):
        """
        DESCRIPTION: Verify Event accordians
        EXPECTED: Event accordians should be collapsible and expandable in EDP
        """
        # covered in above step

    def test_005_verify_signpostings_and_favourite_icons(self):
        """
        DESCRIPTION: Verify Signpostings and Favourite icons
        EXPECTED: Sign postings should be displayed (if available)
        EXPECTED: Mobile:
        EXPECTED: Favourite (star) icon should be displayed
        """
        event_id = self.extract_event_id_from_url()
        markets = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)[0].get('event').get('children')
        is_cash_out_available = next((True for market in markets if market.get('market').get('name') == self.selection_name and market.get('market').get('cashoutAvail') == 'Y'), False)
        # verifying cash_out sign_post is displaying or not
        self.assertEqual(is_cash_out_available, self.selection.section_header.has_cash_out_mark(), msg=f'Actual status of cashout Signpost is {self.selection.section_header.has_cash_out_mark()} but expected is {is_cash_out_available}')
        # verifying favourites icon is displaying or not in sport event details page
        # favourites icon is visible for Coral Mobile only
        if self.device_type == 'mobile' and self.brand == 'bma':
            self.assertTrue(self.site.sport_event_details.header_line.has_favourites_icon,
                            msg='Favourite icon is not displayed on Football Event Details page')