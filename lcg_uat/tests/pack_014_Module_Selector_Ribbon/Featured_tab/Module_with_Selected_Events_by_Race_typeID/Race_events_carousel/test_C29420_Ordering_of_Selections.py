import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can not create events on prod/beta
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.homepage_featured
@vtest
class Test_C29420_Ordering_of_Selections(BaseRacing, BaseFeaturedTest):
    """
    TR_ID: C29420
    NAME: Ordering of Selections
    DESCRIPTION: This test case verifies how selections will be sorted in the <Race> events carousel
    DESCRIPTION: **Jira tickets:** BMA-6571 CMS: Featured Tab Module - Horse Racing
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day
    PRECONDITIONS: 3) In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - **'priceTypeCodes'** on the market level to see which rule for sorting should be applied
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True
    lp_prices = {0: '1/2',
                 1: '1/4'}
    lp_sp_prices = {0: '3/4',
                    1: ' '}

    ss_outcome_details = [{0: 'id', 1: 'selection_name', 2: 'run_number'},
                          {0: 'id', 1: 'selection_name', 2: 'run_number'}]

    def test_000_preconditions(self):

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1)
        eventID_sp, self.__class__.selection_ids_sp = \
            event_params.event_id, event_params.selection_ids
        outcome_names = event_params.ss_response['event']['children'][0]['market']['children']
        for self.__class__.outcome in range(len(outcome_names)):
            self.ss_outcome_details[self.outcome][0] = outcome_names[self.outcome]['outcome']['id']
            self.ss_outcome_details[self.outcome][1] = outcome_names[self.outcome]['outcome']['name']
            self.ss_outcome_details[self.outcome][2] = outcome_names[self.outcome]['outcome']['runnerNumber']
        self._logger.info(f'*** Created SP event id: {eventID_sp}, '
                          f'selection ids: {list(self.selection_ids_sp.values())}')

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1,
                                                          lp_prices=self.lp_sp_prices, sp=True)
        eventID_lp_sp, self.__class__.selection_ids_lp_sp = \
            event_params.event_id, event_params.selection_ids

        self._logger.info(f'*** Created LP-SP event id: {eventID_lp_sp}, '
                          f'selection ids: {list(self.selection_ids_lp_sp.values())}')

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1,
                                                          lp_prices=self.lp_prices, sp=False)
        eventID_lp, self.__class__.selection_ids_lp = \
            event_params.event_id, event_params.selection_ids

        self._logger.info(f'*** Created LP event id: {eventID_lp},'
                          f'selection ids: {list(self.selection_ids_lp.values())}')
        self.__class__.selection_ids = self.selection_ids_lp

        type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='RaceTypeId', id=type_id, events_time_from_hours_delta=-10,
            module_time_from_hours_delta=-10, max_rows=self.max_number_of_events)['title'].upper()

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='HomePage')

    def test_002_for_mobiletabletgo_to_module_selector_ribbon___module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Go to Module Selector Ribbon -> Module created by <Race> type ID
        EXPECTED: *   'Feature' tab is selected by default
        EXPECTED: *   Module created by <Race> type ID is shown
        """
        if self.device_type == 'mobile':
            home_featured_tab_name = self.get_ribbon_tab_name(
                self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
            self.wait_for_featured_module(name=self.module_name, timeout=200)
            module = self.get_section(section_name=self.module_name)
            self.assertTrue(module, msg='module is not displayed')
            selected_tab = self.site.home.module_selection_ribbon.tab_menu.current
            self.assertEqual(selected_tab, home_featured_tab_name,
                             msg=f'Selected tab is "{selected_tab}" instead of "{home_featured_tab_name}" tab')

            self.__class__.module = self.get_section(self.module_name)
            self.assertTrue(self.module, msg='No accordions displayed in "Featured" tab on Home page')

    def test_003_for_desktopscroll_the_page_down_to_featured_section____module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Scroll the page down to 'Featured' section ->-> Module created by <Race> type ID
        EXPECTED: * 'Featured' section is displayed below the following sections: Enhanced/ Sports offer carousel, In-Play & Live Stream, Next Races Carousel (if applicable)
        EXPECTED: * Module created by <Race> type ID is shown
        """
        if self.device_type == 'desktop':
            featured_module = self.site.home.desktop_modules.featured_module
            self.assertTrue(featured_module, msg='"Featured" module is not displayed')

            featured_content = featured_module.tab_content
            featured_modules = featured_content.accordions_list.items_as_ordered_dict.keys()
            self.assertTrue(featured_content.accordions_list, msg='"Featured" module does not contain any accordions')
            self.assertIn(self.module_name, featured_content.accordions_list.items_as_ordered_dict.keys(),
                          msg=f'Module "{self.module_name}" is not displayed. '
                              f'Please check list of all displayed modules:\n"{featured_modules}"')
            self.__class__.featured_module_name = featured_content.accordions_list.items_as_ordered_dict[
                self.module_name]
            self.assertTrue(self.featured_module_name, msg='No accordions displayed in "Featured" section on Home page')

    def test_004_on_race_events_carousel_find_an_event_with_attribute_pricetypecodessp(self):
        """
        DESCRIPTION: On <Race> events carousel find an event with attribute **'priceTypeCodes'**='SP'
        EXPECTED: Event is shown
        """
        if self.device_type == 'mobile':
            self.__class__.featured_module = self.site.home.get_module_content(
                self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
            module = self.get_section(section_name=self.module_name)
        else:
            module = self.featured_module_name
        for selection_name, selection_id in self.selection_ids_sp.items():
            bet_button = module.get_bet_button_by_selection_id(selection_id)
            bet_button.scroll_to()
            self.assertEqual(bet_button.name, 'SP',
                             msg='Selection price "%s" is not the same as in TI "%s"'
                                 % (bet_button.name, 'SP'))

    def test_005_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: 1.  Selections are ordered by** 'runnerNumber'** attribute (if such is available for outcomes)
        EXPECTED: 2.  Selections are sorted alphabetically by **'name'** attribute (if **'runnerNumber' **is absent)
        """
        # covered in step 11

    def test_006_verify_event_with_attribute_pricetypecodeslp(self):
        """
        DESCRIPTION: Verify event with attribute **'priceTypeCodes'**='LP'
        EXPECTED: The actual price/odd is displayed in decimal or fractional format (depends upon the users chosen odds display preference)
        """
        if self.device_type == 'mobile':
            module = self.get_section(section_name=self.module_name)
        else:
            module = self.featured_module_name
        for selection_name, selection_id in self.selection_ids_lp.items():
            bet_button = module.get_bet_button_by_selection_id(selection_id)
            bet_button.scroll_to()
            price = bet_button.outcome_price_text
            self.assertRegexpMatches(price, self.fractional_pattern,
                                     msg=f'Odds value for current selections combination "{price}" '
                                         f'is not in correct format "{self.fractional_pattern}"')

    def test_007_verify_order_of_selection(self):
        """
        DESCRIPTION: Verify order of selection
        EXPECTED: 1.
        EXPECTED: Selections are ordered by odds in ascending order (lowest to highest)
        EXPECTED: 2.
        EXPECTED: If odds of selections are the same -> display alphabetically by horse name (in ascending order)
        EXPECTED: 3.
        EXPECTED: If prices are absent for selections - display alphabetically by horse name (in ascending order)
        """
        # covered in step 11

    def test_008_verify_event_with_attributes___pricetypecodessp_lp___prices_are_availale_for_outcomes(self):
        """
        DESCRIPTION: Verify event with attributes:
        DESCRIPTION: *   **'priceTypeCodes'**='SP, LP'
        DESCRIPTION: *   prices ARE availale for outcomes
        EXPECTED: Event is shown
        EXPECTED: One 'LP' button is shown next to each selection
        """
        if self.device_type == 'mobile':
            self.__class__.featured_module = self.site.home.get_module_content(
                self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
            module = self.get_section(section_name=self.module_name)
        else:
            module = self.featured_module_name
        for selection_name, selection_id in self.selection_ids_lp_sp.items():
            bet_button = module.get_bet_button_by_selection_id(selection_id)
            bet_button.scroll_to()
            self.assertEqual(bet_button.name, bet_button.outcome_price_text,
                             msg='Selection price "%s" is not the same as in TI "%s"'
                                 % (bet_button.name, bet_button.outcome_price_text))

    def test_009_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: Selections are ordered as per LP rule in step #6
        """
        # covered in step 6

    def test_010_verify_event_with_attributes___pricetypecodessp_lp___prices_are_not_available_for_outcomes(self):
        """
        DESCRIPTION: Verify event with attributes:
        DESCRIPTION: *   **'priceTypeCodes'**='SP, LP'
        DESCRIPTION: *   prices are NOT available for outcomes
        EXPECTED: Event is shown
        EXPECTED: Only one 'SP' button is shown
        """
        if self.device_type == 'mobile':
            self.__class__.featured_module = self.site.home.get_module_content(
                self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
            module = self.get_section(section_name=self.module_name)
        else:
            module = self.featured_module_name
        for selection_name, selection_id in self.selection_ids_sp.items():
            bet_button = module.get_bet_button_by_selection_id(selection_id)
            bet_button.scroll_to()
            self.assertEqual(bet_button.name, 'SP',
                             msg='Selection price "%s" is not the same as in TI "%s"'
                                 % (bet_button.name, 'SP'))

    def test_011_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: Selections are ordered alphabetically (in A-Z order) by **'name' **attribute
        """
        list_of_numbers = []
        selection_names = []
        for r_no in self.ss_outcome_details:
            run_numbers = r_no[2]
            if r_no[2]:
                list_of_numbers.append(run_numbers)
                self.assertListEqual(list_of_numbers, sorted(list_of_numbers),
                                     msg=f'Outcomes "{list_of_numbers}" are not sorted by '
                                         f'runner numbers "{sorted(list_of_numbers)}"')
            else:
                for sel_name in self.ss_outcome_details:
                    selection_name = sel_name[1]
                    selection_names.append(selection_name)
                    self.assertListEqual(selection_names, sorted(selection_names),
                                         msg=f'Selections are not sorted in alphabetical A-Z order: "{selection_names}" are not sorted by '
                                             f'selection name "{sorted(selection_names)}"')
