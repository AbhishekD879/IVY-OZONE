import voltron.environments.constants as vec
from collections import OrderedDict

import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod # yourcall no in the scope of roxane release
# @pytest.mark.crl_hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.yc_specials_widget
@pytest.mark.races
@vtest
class Test_C1158565_Your_Call_Specials_Widget(BaseRacing):
    """
    TR_ID: C1158565
    VOL_ID: C9698154
    NAME: Your Call Specials Widget
    DESCRIPTION: This test case verifies the display of the Your Call Specials Widget on Horse Racing Landing Page (Featured tab)
    """
    keep_browser_open = True
    prices = {0: '1/4', 1: '1/2', 2: '2/3', 3: '1/3', 4: '3/2'}
    num_of_displaying_selections = 3
    view_all_link_text = 'VIEW ALL #YOURCALL SPECIALS'
    yc_tab_name = 'YOURCALL'

    def get_yc_special_widget(self):
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertIn(self.yc_specials_type_name, sections.keys())
        return sections[self.yc_specials_type_name]

    def test_001_create_event_in_backoffice(self):
        """
        DESCRIPTION: Create Horse Racing Your Call Specials event
        EXPECTED: Event is created
        """
        self.ob_config.add_racing_your_call_specials_event(number_of_runners=5, lp_prices=self.prices)

    def test_002_navigate_to_hr_featured_tab_your_call_specials_widget(self):
        """
        DESCRIPTION: Navigate to Horse Racing/Featured tab.
        DESCRIPTION: Scroll if necessary until YourCall Specials widget is visible.
        EXPECTED: When the page is loaded, Your Call Specials Widget is displayed
        EXPECTED: YourCall Specials widget accordion is expanded by default
        EXPECTED: YourCall Specials accordion is named "YOURCALL SPECIALS"
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg='Current tab %s is not the same as expected %s'
                             % (current_tab, vec.racing.RACING_DEFAULT_TAB_NAME))
        self.__class__.yc_specials_section = self.get_yc_special_widget()
        self.assertTrue(self.yc_specials_section.is_expanded(),
                        msg='Section: "%s" not expanded by default' % self.yc_specials_type_name)

    def test_003_verify_widget_accordion_content(self):
        """
        DESCRIPTION: Verify the widget accordion content
        EXPECTED: Up to top 3 selections from Featured market of type Your Call Specials are displayed within the widget
        EXPECTED: Selections are ordered by displayOrder parameter for outcomes in EventToOutcomeForType response.
        The lower the value, the higher the position. In case a few outcomes have the same parameter value,
        the order should be as it is in the response.
        EXPECTED: The name of each selection begins with "#Yourcall" hashtag
        EXPECTED: Correct price from EventToOutcomeForType response is displayed for each selection
        """
        outcome_names_prices = OrderedDict([(outcome_name, outcome.bet_button.outcome_price_text) for outcome_name, outcome in self.yc_specials_section.items_as_ordered_dict.items()])
        self._logger.debug('*** Got outcome names and prices "%s" ' % outcome_names_prices)
        type_id = self.ob_config.horseracing_config.daily_racing_specials.your_call_specials.type_id
        resp = self.ss_req.ss_event_to_outcome_for_type(type_id=type_id)
        outcomes_display_order = self.get_outcomes_display_order_for_type(response=resp)
        ss_featured_tab_outcomes = outcomes_display_order.markets_with_outcomes.get('Featured')
        self.assertEqual(list(outcome_names_prices.items()), list(ss_featured_tab_outcomes.items())[:self.num_of_displaying_selections])
        selections = self.yc_specials_section.items_as_ordered_dict
        self.assertTrue(selections, msg='No one market: "%s" selection found' % self.yc_specials_type_name)
        [self.assertIn('#YourCall ', selection.css_property_text()) for selection in selections.values()]

    def test_004_collapse_expand_the_widget(self):
        """
        DESCRIPTION: Collapse/expand the widget
        EXPECTED: Widget is collapsed - "+" sign is shown
        """
        self.yc_specials_section.collapse()
        self.assertFalse(self.yc_specials_section.is_expanded(expected_result=False),
                         msg='Section: "%s" was not collapsed' % self.yc_specials_type_name)
        self.yc_specials_section.expand()
        self.assertTrue(self.yc_specials_section.is_expanded(),
                        msg='Section: "%s" was not expanded' % self.yc_specials_type_name)

    def test_005_verify_view_all_yourcall_specials_link_at_the_bottom(self):
        """
        DESCRIPTION: Verify View all YourCall Specials link at the bottom
        EXPECTED: Underlined "VIEW ALL #YOURCALL SPECIALS" text at the bottom of the widget
        """
        self.assertEqual(self.yc_specials_section.view_all_link.name, self.view_all_link_text,
                         msg='Actual link text: "%s", expected: "%s"'
                             % (self.yc_specials_section.view_all_link.name, self.view_all_link_text))

    def test_006_click_on_view_all_yourcall_specials_link(self):
        """
        DESCRIPTION: Click on View all YourCall Specials link at the bottom of the widget
        EXPECTED: YOURCALL tab in Horse racing is opened
        """
        self.yc_specials_section.view_all_link.click()
        result = wait_for_result(lambda: self.site.horse_racing.tabs_menu.current == self.yc_tab_name,
                                 timeout=1,
                                 name='"%s" tab in Horse racing is opened' % self.yc_tab_name)
        self.assertTrue(result, msg='Current tab "%s" is not the same as expected "%s"'
                                    % (self.site.horse_racing.tabs_menu.current, self.yc_tab_name))

    def test_007_verify_yourcall_widget_if_there_no_yc_specials(self):
        """
        DESCRIPTION: Verify YourCall Specials widget content if there are no YourCall Specials selections from Featured market available
        EXPECTED: YourCall Specials widget is NOT displated
        """
        # Can't cover this validation because we can't delete all YourCall specials (not created by auto test) from TI
        # so we can't be sure there are not YourCall specials at all
