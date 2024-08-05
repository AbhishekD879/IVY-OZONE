import pytest
import tests
import voltron.environments.constants as vec
from datetime import datetime
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


# @pytest.mark.tst2  #lotto bets are not available most of the times
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.lotto
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C29586_Select_Draw_Opions(BaseSportTest):
    """
    TR_ID: C29586
    NAME: Select Draw Opions
    DESCRIPTION: This Test Case verifies Select Draw Options for Lotteries.
    DESCRIPTION: **Jira Ticket:**
    DESCRIPTION: BMA-2329 'Lottery - Select draw options'
    DESCRIPTION: BMA-7414 'Lotto - select draw bug'
    PRECONDITIONS: 1. Lotto icon should be preconfigured in Sports Menu Ribbon and/or A-Z Page via CMS
    PRECONDITIONS: 2. Launch Invictus application
    PRECONDITIONS: To get a list of lotteries and draws use following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Lottery/X.XX/LotteryToDraw/
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: **NOTE** :
    PRECONDITIONS: *   for all Lotteries all available 'Draw' options for the next t days (7*24=168) are displayed in ascending (in two columns)
    PRECONDITIONS: *   except of two lotteries , i.e. '49's' & 'Daily Million', for which we display only two earliest 'Draw' options
    """
    keep_browser_open = True

    def format_name(self, lotto_name: str):
        """
        This method unifies lotto's name as it is displayed on UI
        :param lotto_name: lotto's name
        :return: formatted lotto's name
        """
        formatted_name = lotto_name.upper().replace(' LOTTO', '').replace(' LOTTERY', ''). \
            replace(' BALL', '').replace(' 6', '').replace(' 7', '')
        return formatted_name

    def test_000_preconditions(self):
        """
        DESCRIPTION: Open Oxygen application
        """
        utc_time = datetime.strftime(datetime.utcnow(), self.ob_format_pattern)

        lotto_filter = self.ss_query_builder.add_filter(simple_filter(LEVELS.LOTTERY, ATTRIBUTES.HAS_OPEN_DRAW))
        lotto_resp = self.ss_req.ss_lottery_to_draw(query_builder=lotto_filter)

        oz_lotto = 'Australian Ozlotto Lottery'
        tats_lotto = 'Australian Tattslotto Lottery'

        ids_to_exclude = ['7', '20', '26', '27'] if self.brand != 'ladbrokes' else ['1801', '1806']

        excluded = [x for x in lotto_resp if x['lottery']['id'] not in ids_to_exclude]

        lotto_name_list = [x['lottery']['description'] for x in excluded]
        lotto_data_list = [x['lottery']['children'] for x in excluded]

        draw_list = []
        for item in lotto_data_list:
            draw = [x for x in item if x.get('draw') is not None]
            draw_list.append(draw)

        lotto_dict = dict(zip(lotto_name_list, draw_list))

        if tests.settings.backend_env == 'prod' and self.brand != 'ladbrokes':
            if oz_lotto in list(lotto_dict.keys()):
                lotto_dict[tats_lotto].extend(lotto_dict[oz_lotto])

        shut_at_time = []
        draw_options = {}
        for name in lotto_dict.keys():
            shut = [x['draw']['shutAtTime'] for x in lotto_dict[name] if x['draw']['shutAtTime'] >= utc_time]
            for x in lotto_dict[name]:
                if x['draw']['shutAtTime'] >= utc_time:
                    draw_options[x['draw']['description']] = x['draw']['shutAtTime']
            if shut:
                shut_at_time.append(min(shut))

        self.__class__.ss_sorted_draw_options = dict(sorted(draw_options.items(), key=lambda x: (x[1])))

    def test_001_tap_on_lotto_icon_from_sports_menu_ribbon_or_a_z_page(self):
        """
        DESCRIPTION: Tap on 'Lotto' icon (from Sports Menu Ribbon or A-Z page)
        EXPECTED: *   'Lotto' page is opened.
        EXPECTED: *   Lottery with the upcoming Draw is selected by default.
        """
        self.navigate_to_page(name='lotto')
        self.site.wait_content_state('lotto')
        self.__class__.lotto_carousel = self.site.lotto.lotto_carousel.items_as_ordered_dict
        self.assertTrue(self.lotto_carousel, msg='No Lottery Selector Carousel items found')
        content = self.site.lotto
        self.__class__.tab_content = content.tab_content
        expected_title = vec.lotto.LOTTO if self.brand == 'ladbrokes' else vec.lotto.LOTTO.upper()

        sport_title = content.header_line.page_title.sport_title
        self.assertEqual(expected_title, sport_title,
                         msg=f'Page title is not "{expected_title}", but "{sport_title}"')

    def test_002_navigate_to_options_panel(self):
        """
        DESCRIPTION: Navigate to 'Options' panel
        EXPECTED: *   'Options' panel is displayed and expanded by default.
        EXPECTED: *   'Select Draw' label is displayed under panel's header.
        EXPECTED: *   The list of all draws availble for the selected Lottery is displayed according to attributes 'openAtTime' & 'shutAtTime'
        EXPECTED: *   Draw name is taken from 'description' attribute on the draw level from SS response.
        EXPECTED: *   Each unique draw description is displayed with a checkbox alongside it.
        EXPECTED: *   The next availabel draw is selected by default.
        """
        self.assertTrue(self.tab_content.options.is_displayed(),
                        msg='Options section isn\'t shown on Lotto page')
        self.assertTrue(self.tab_content.select_draw.is_displayed(),
                        msg='Select draw label isn\'t shown on option container in Lotto page')
        self.assertTrue(self.tab_content.draw_checkboxes.is_displayed(),
                        msg='Checkboxes are not present on draw options')

        self.__class__.selected_lottery_names = []

        for lotto_name in self.lotto_carousel.keys():
            self.__class__.lotto = self.site.lotto
            self.lotto.lotto_carousel.click_item(lotto_name)
            self.__class__.checkboxes = self.lotto.tab_content.draw_checkboxes.items_as_ordered_dict.items()
            for item in list(self.checkboxes):
                self.assertIn(item[0], self.ss_sorted_draw_options.keys(), msg=f'Draw name is not taken from description attribute on the draw level from SS response')
            self.assertTrue(list(self.checkboxes)[0][1].value, msg='Draw is not selected by default')
            self.lotto.tab_content.options.group_header.click()
            self.assertFalse(self.lotto.tab_content.options.is_expanded(expected_result=False), msg='options panel is expanded')
            self.lotto.tab_content.options.group_header.click()
            self.assertTrue(self.lotto.tab_content.options.is_chevron_up, msg='options panel is not expanded')

    def test_003_collapseexpand_the_panelby_tapping_on_its_header(self):
        """
        DESCRIPTION: Collapse/Expand the panel by tapping on it's header
        EXPECTED: It is possible to collapse/expand the panel.
        """
        # covered in step 2

    def test_004_select_another_lottery(self):
        """
        DESCRIPTION: Select another Lottery
        EXPECTED: Appropriate draw descriptions taken from SS are displayed within Options section.
        """
        # covered in step 2

    def test_005_uncheck_selected_by_default_draws_checkbox_and_tap_on_place_bet_for_button(self):
        """
        DESCRIPTION: Uncheck selected by default draw's checkbox and tap on 'Place Bet for' button
        EXPECTED: * Button to place bet is disabled
        """
        list(self.lotto.tab_content.draw_checkboxes.items_as_ordered_dict.values())[0].draw_check_box.click()
        self.assertFalse(self.site.lotto.tab_content.place_bet.is_enabled(), msg="Place bet button is not disabled")

    def test_006_check_out_several_available_draws(self):
        """
        DESCRIPTION: Check out several available draws
        EXPECTED: User has ability to select multiple draws.
        """
        checkboxes = list(self.lotto.tab_content.draw_checkboxes.items_as_ordered_dict.values())
        for check in checkboxes:
            check.draw_check_box.click()
        checkboxes = list(self.lotto.tab_content.draw_checkboxes.items_as_ordered_dict.values())
        for check in checkboxes:
            self.assertTrue(check.value, msg='Multiple checkboxes are not checked')

    def test_007_select_lottery_without_any_draws_available(self):
        """
        DESCRIPTION: Select Lottery without any draws available
        EXPECTED: Whole Options section should not be displayed on front end at all.
        """
        # cannot automate this step
