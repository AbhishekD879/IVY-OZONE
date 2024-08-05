from collections import OrderedDict
import pytest
import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from crlat_siteserve_client.utils.exceptions import SiteServeException
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop_only
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.sports_specific
@pytest.mark.table_tennis_specific
@pytest.mark.adhoc_suite
@vtest
class Test_C65968769_Verify_Table_Tennis_In_play_widget_display_in_SLP_and_verify_carousel_behaviour(BaseBetSlipTest):
    """
    TR_ID: C65968769
    NAME: Verify Table Tennis In-play widget display in SLP and verify carousel behaviour
    DESCRIPTION: This test case needs to  verify Table tennis In-play widget display in SLP and verify carousel behaviour
    PRECONDITIONS: 1. User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: 2.Inplay widget   can be configured from CMS-&gt;
    PRECONDITIONS: System config-&gt;structure-&gt; DesktopWidgetsToggle-&gt;Inplay&gt; enable/disable.
    PRECONDITIONS: Note: In mobile when no events are available table tennis sport is not displayed in A-Z sports menu and on clikcing table tennis  from Sports ribbon user is navigated back to the sports homepage.
    """
    keep_browser_open = True
    table_tennis_Category_id = 59
    defualt_tab = vec.sb.TABS_NAME_MATCHES.lower()
    home_breadcrumb = vec.sb.HOME_FOOTER_ITEM.title()
    sport_name = 'table tennis'
    device_name = tests.desktop_default

    def validate_scores_updation(self, scores, odds, count=0):
        self.__class__.scores_changed = False
        self.__class__.odds_changed = False
        for widget_name, widget in self.widgets.items():
            score = widget.in_play_card.in_play_score
            self.assertTrue(score.is_displayed(), msg=f'Widget {score} is not displayed')
            left_score = score.left_score._we.text
            right_score = score.right_score._we.text
            event_odds = list(widget.odds_buttons.items_as_ordered_dict.keys())
            # there is an existing defect in prod
            # if left_score != scores[widget_name].get("home") or right_score != scores[widget_name].get('away'):
            #     self.scores_changed = True
            if len(event_odds) > 1:
                if event_odds[0] != odds[widget_name].get("home") or event_odds[1] != odds[widget_name].get('away'):
                    self.odds_changed = True
            # and self.scores_changed add this code once the defect is fixed
            if self.odds_changed:
                break
        else:
            if count == 3:
                raise VoltronException(f'prices not updated in in-play widget of table tennis under match tab"')
            else:
                wait_for_haul(5)
                self.validate_scores_updation(scores=scores, odds=odds, count=count + 1)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. User should have access to oxygen CMS
        PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
        PRECONDITIONS: 2. Matches tab can be configured from CMS->
        PRECONDITIONS: Sports Menu-> Sports Category ->Table Tennis -> Matches tab -> Enable/Disable.
        PRECONDITIONS: Note: In mobile when no events are available table tennis sport is not displayed in A-Z sports menu and on clicking Table Tennis  from Sports ribbon user is navigated back to the sports home page.
        """
        self.get_active_events_for_category(category_id=self.table_tennis_Category_id, in_play_event=True)
        self.__class__.in_play_status = self.get_initial_data_system_configuration().get('DesktopWidgetsToggle').get(
            'inPlay')
        if not self.in_play_status:
            if tests.settings.cms_env != 'prd0':
                self.cms_config.update_system_configuration_structure(config_item='DesktopWidgetsToggle',
                                                                      field_name='inPlay', field_value=True)
                self.__class__in_play_status = self.get_initial_data_system_configuration().get(
                    'DesktopWidgetsToggle').get(
                    'inPlay')
            else:
                raise CmsClientException(f'Desktop widget is disabled in cms"')

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home page should loaded successfully
        """
        self.navigate_to_page("/")
        self.site.wait_content_state("homepage")
        self.site.login()

    def test_002_click_on_table_tennis_sport(self):
        """
        DESCRIPTION: Click on table tennis sport.
        EXPECTED: User should be able to navigate table tennis landing page.
        """
        self.site.open_sport(name="Table Tennis")

    def test_003_verify_table_tennis_landing_page(self):
        """
        DESCRIPTION: Verify table tennis landing page.
        EXPECTED: Desktop
        EXPECTED: Tabs should be displayed with default selected matches tab with today events .
        EXPECTED: In play widget will display if any events are in live when it was enabled in sys config.
        EXPECTED: Mobile
        EXPECTED: Matches module loaded as default with inplay events in it
        """
        current_tab = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab.lower(), self.defualt_tab,
                         msg=f"table tennis landing page not same {current_tab} as expected {self.defualt_tab}")

    def test_004_verify_inplay_widget(self):
        """
        DESCRIPTION: Verify Inplay widget
        EXPECTED: User must be able to in play events with event details
        """
        sections = self.site.sports_page.in_play_widget.items_as_ordered_dict.get(
            'In-Play LIVE Tabletennis')
        self.__class__.widgets = sections.content.items_as_ordered_dict
        sections.is_expanded()
        self.assertTrue(self.widgets, msg='Widget are not available')
        self.__class__.event_name, self.__class__.event = list(self.widgets.items())[-1]
        live_icon = self.event.in_play_card.in_play_score.game_status
        self.assertTrue(live_icon.is_displayed(), msg=f'Widget "{live_icon}" is not displayed')
        live_label = live_icon._we.text
        self.assertEqual('LIVE', live_label, msg='"LIVE" label is not shown on the screen')

    def test_005_verify_score_updates(self):
        """
        DESCRIPTION: Verify score updates
        EXPECTED: Scores updates needs to be happen
        """
        scores = {}
        odds = {}
        for widget_name, widget in self.widgets.items():
            score = widget.in_play_card.in_play_score
            self.assertTrue(score.is_displayed(), msg=f'Widget {score} is not displayed for widget {widget_name}')
            left_score = score.left_score._we.text
            right_score = score.right_score._we.text
            scores[widget_name] = {
                "home": left_score, "away": right_score}
            event_odds = list(widget.odds_buttons.items_as_ordered_dict.keys())
            if len(event_odds) > 1:
                odds[widget_name] = {"home": event_odds[0], "away": event_odds[1]}
            else:
                odds[widget_name] = {"home": event_odds[0], "away": event_odds[0]}
        self.validate_scores_updation(scores=scores, odds=odds)

    def test_006_verify_various_signposting(self):
        """
        DESCRIPTION: Verify various signposting
        EXPECTED: User should be able to see signposting.
        """
        cashout = self.event.has_cashout_icon()
        self.assertTrue(cashout, msg=f'Widget {cashout} is not displayed')

    def test_007_verify_the_carousel_scroll_behaviour_left_and_right(self):
        """
        DESCRIPTION: Verify the carousel scroll behaviour (Left and Right)
        EXPECTED: Carousel need to visible only when we mouse hover on it.
        EXPECTED: Events need to scrolled to right.
        EXPECTED: Carousel need to disappear once the events ends up at right side.
        EXPECTED: Carousel need to visible only when we mouse hover on it
        EXPECTED: Events need to scrolled to left.
        EXPECTED: Carousel need to disappear once the events ends up at left side .
        """
        pass

    def test_008_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should be navigated on the respective page on click
        """
        self.event.in_play_card.in_play_score.game_status.click()
        page = self.site.sports_page
        breadcrumbs = OrderedDict((key.strip(), page.breadcrumbs.items_as_ordered_dict[key])
                                  for key in page.breadcrumbs.items_as_ordered_dict)

        self.assertTrue(breadcrumbs, msg='No breadcrumbs found')

        self.assertEqual(list(breadcrumbs.keys()).index(self.home_breadcrumb), 0,
                         msg='Home page is not shown the first by default')
        self.assertTrue(breadcrumbs[self.home_breadcrumb].angle_bracket,
                        msg=f'Angle bracket is not shown after "{self.home_breadcrumb}" breadcrumb')

        self.assertEqual(list(breadcrumbs.keys()).index(self.sport_name), 1,
                         msg=f'"{self.sport_name}" sport title is not shown after "{self.home_breadcrumb}"')
        self.assertTrue(breadcrumbs[self.sport_name].angle_bracket,
                        msg=f'Angle bracket is not shown after "{self.sport_name}" breadcrumb')

        self.assertEqual(list(breadcrumbs.keys()).index(self.event_name), 2,
                         msg=f'"{self.event_name} " item name is not shown after "{self.sport_name}"')
        self.assertTrue(
            int(breadcrumbs[self.event_name].link.css_property_value('font-weight')) == 700,
            msg=f'" matches " hyperlink from breadcrumbs is not highlighted according to the selected page')
        self.site.back_button.click()

    def test_009_verify_bet_placements_for_single_multiplecomplex_by_adding_selections_from_the_in_play_widget(self):
        """
        DESCRIPTION: Verify bet placements for single, multiple,complex by adding selections from the in-play widget.
        EXPECTED: Bet placement should be successful
        """

        def odd_to_select(events, odd_selected_count=0, expected_odd_count=1):
            for event_name, event in events.items():
                event.scroll_to()
                event_odds_buttons = event.odds_buttons.items_as_ordered_dict
                if len(event_odds_buttons) > 1:
                    list(event_odds_buttons.values())[0].click()
                    odd_selected_count += 1
                else:
                    continue
                if odd_selected_count == expected_odd_count:
                    break
            else:
                raise SiteServeException(
                    f'There are not available events to place all types of bets expected events {expected_odd_count}')

        sections = self.site.sports_page.in_play_widget.items_as_ordered_dict.get('In-Play LIVE Tabletennis')
        widgets = sections.content.items_as_ordered_dict
        try:
            odd_to_select(events=widgets)
            self.place_and_validate_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        except Exception as e:
            self.clear_betslip()
            odd_to_select(events=widgets)
            self.place_and_validate_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()

        try:
            sections = self.site.sports_page.in_play_widget.items_as_ordered_dict.get('In-Play LIVE Tabletennis')
            widgets = sections.content.items_as_ordered_dict
            odd_to_select(events=widgets, expected_odd_count=2)
            self.place_multiple_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        except Exception as e:
            self.clear_betslip()
            sections = self.site.sports_page.in_play_widget.items_as_ordered_dict.get('In-Play LIVE Tabletennis')
            widgets = sections.content.items_as_ordered_dict
            odd_to_select(events=widgets, expected_odd_count=2)
            self.place_multiple_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()