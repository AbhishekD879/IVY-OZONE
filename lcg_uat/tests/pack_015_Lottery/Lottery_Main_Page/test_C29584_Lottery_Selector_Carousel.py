import pytest
import tests
from datetime import datetime
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.lotto
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.menu_ribbon
@pytest.mark.desktop
@pytest.mark.medium
@vtest
class Test_C29584_Lottery_Selector_Carousel(BaseSportTest):
    """
    TR_ID: C29584
    NAME: Lottery Selector Carousel
    DESCRIPTION: This Test Case verifies Lottery Selector Carousel
    PRECONDITIONS: 1. Launch Invictus application
    PRECONDITIONS: To get a list of lotteries and draws use following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Lottery/X.XX/LotteryToDraw/
    PRECONDITIONS: * X.XX - current supported version of OpenBet release
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
        irish_6 = 'Irish Lotto 6 ball'
        irish_7 = 'Irish Lotto 7 ball'

        # this is configured in bma project:
        # src/environments/configs/lotteriesConfig.ts for Coral
        # src/environments/configs/lotteriesLadbrokesConfig.ts for Ladbrokes
        if tests.settings.backend_env != 'prod':
            ids_to_exclude = ['7', '20', '26', '27'] if self.brand != 'ladbrokes' else ['']
        else:
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

        if tests.settings.backend_env != 'prod' and self.brand == 'ladbrokes':
            if irish_6 in list(lotto_dict.keys()):
                lotto_dict[irish_7].extend(lotto_dict[irish_6])
                lotto_dict.pop(irish_6)

        shut_at_time = []
        for name in lotto_dict.keys():
            shut = [x['draw']['shutAtTime'] for x in lotto_dict[name] if x['draw']['shutAtTime'] >= utc_time]
            if shut:
                shut_at_time.append(min(shut))

        shut_at_time_local = [self.convert_time_to_local(
            date_time_str=x, ob_format_pattern=self.ob_format_pattern,
            ui_format_pattern=self.ob_format_pattern,
            future_datetime_format=self.ob_format_pattern,
            ss_data=True) for x in shut_at_time]

        lotto_ui_names = [self.format_name(x) for x in lotto_dict.keys()]

        name_time = dict(zip(lotto_ui_names, shut_at_time_local))
        sorted_name_time = dict(sorted(name_time.items(), key=lambda x: (x[1], x[0])))

        self.__class__.ss_lotto_names = list(sorted_name_time.keys())
        self.__class__.ss_lotto_times = list(sorted_name_time.values())

    def test_001_tap_lotto_icon_from_sports_menu_ribbon_or_a_z_page(self):
        """
        DESCRIPTION: Tap 'Lotto' icon (from Sports Menu Ribbon or A-Z page)
        EXPECTED: 'Lotto' page is opened
        """
        self.navigate_to_page(name='lotto')
        self.site.wait_content_state(state_name='lotto')

    def test_002_verify_lotteries_presence_in_carousel_basing_on_siteserve_response(self):
        """
        DESCRIPTION: Launch URL from Preconditions to verify Lotteries presence in Carousel basing on SiteServe response
        EXPECTED: All lotteries from SiteServe response are available within Lottery Selector Carousel
        """
        self.__class__.lotto_carousel = self.site.lotto.lotto_carousel.items_as_ordered_dict
        self.assertTrue(self.lotto_carousel, msg='No Lottery Selector Carousel items found')

        actual_list = [x.upper() for x in self.lotto_carousel.keys()]
        expected_list = self.ss_lotto_names
        self.assertTrue(all(item in expected_list for item in actual_list),
                        msg=f'\nLists are not equal!'
                            f'\nActual list: {actual_list}'
                            f'\nExpected list: {expected_list}')

    def test_003_verify_lottery_selector_carousel(self):
        """
        DESCRIPTION: Verify Lottery Selector Carousel
        EXPECTED: * Each Lottery in the Carousel has it's own icon and title
        EXPECTED: * Lottery with the upcoming Draw should be selected and highlighted by default
        """
        self.__class__.lotto_titles = []
        lotto_icons = []
        for lotto_name, lotto in self.lotto_carousel.items():
            lotto_icons.append(lotto.icon)
            self.lotto_titles.append(lotto_name)
        self.assertEqual(len(lotto_icons), len(self.lotto_titles),
                         msg=f'Number of icons ("{len(lotto_icons)}") and titles ("{len(self.lotto_titles)}") '
                             f'is not the same on Lottery Carousel')

    def test_004_verify_lotteries_order(self):
        """
        DESCRIPTION: Verify Lotteries order
        EXPECTED: Lotteries order should be based on the Draw time (**shutAtTime** attribute) in ascending order, displaying horizontally from left to right
        """
        self.__class__.lotto = self.site.lotto
        self.__class__.selected_lottery_names = []
        bet_until_times = []
        for lotto_name in self.lotto_carousel.keys():
            self.lotto.lotto_carousel.click_item(lotto_name)
            bet_until_times.append(self.lotto.tab_content.info_panel.bet_until_time)
            actual_name = self.lotto.tab_content.info_panel.lottery_name
            self.__class__.selected_lottery_names.append(actual_name)
            self.assertTrue(lotto_name.upper() == actual_name.upper(),
                            msg=f"Expected name '{lotto_name}' is not selected, actual selected lotto is '{actual_name}'")

        if tests.settings.backend_env != 'prod':
            bet_until_time_parse = [datetime.strptime(x, '%d/%m/%Y %H:%M') for x in bet_until_times]
            bet_until_time_format = [datetime.strftime(x, self.ob_format_pattern) for x in bet_until_time_parse]

            actual_list = bet_until_time_format
            expected_list = self.ss_lotto_times
            self.assertListEqual(actual_list, expected_list,
                                 msg=f'\nLists are not equal!'
                                     f'\nActual list: {actual_list}'
                                     f'\nExpected list: {expected_list}')

    def test_005_swipe_lottery_selector_carousel(self):
        """
        DESCRIPTION: Swipe Lottery Selector Carousel
        EXPECTED: * Swipe is supported within the Carousel to browse the available Lotteries
        EXPECTED: * It is possible to swipe both ways
        """
        # cannot automate
        pass

    def test_006_verify_lottery_icons(self):
        """
        DESCRIPTION: Verify Lottery icons
        EXPECTED: Lottery icons correspond to "**description**" attribute on the lottery level
        """
        actual_list = [x.upper() for x in self.lotto_titles]
        expected_list = self.ss_lotto_names
        self.assertTrue(all(item in expected_list for item in actual_list),
                        msg=f'\nLists are not equal!'
                            f'\nActual list: {actual_list}'
                            f'\nExpected list: {expected_list}')

    def test_007_tap_on_any_lotto_icon(self):
        """
        DESCRIPTION: Tap on any 'Lotto' icon
        EXPECTED: Related information to the selected Lottery is loaded below the Carousel
        """
        # already verified in steps #3-4

    def test_008_verify_lottery_name(self):
        """
        DESCRIPTION: Verify Lottery name
        EXPECTED: Lottery name corresponds to "**description**" attribute on the lottery level
        """
        actual_list = self.selected_lottery_names
        expected_list = self.ss_lotto_names
        self.assertTrue(all(item in expected_list for item in actual_list),
                        msg=f'\nLists are not equal!'
                            f'\nActual list: {actual_list}'
                            f'\nExpected list: {expected_list}')
