import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


# @pytest.mark.tst2 # lotto bets are not available
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.lotto
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C29587_Include_or_exclude_the_bonus_ball(BaseSportTest):
    """
    TR_ID: C29587
    NAME: Include or exclude the bonus ball
    DESCRIPTION: This Test Case verifies including or excluding of the bonus ball for Lotteries.
    DESCRIPTION: **Jira Ticket:**
    DESCRIPTION: BMA-2319 'Lottery - Include or exclude the bonus ball'
    DESCRIPTION: BMA-7415 'Lotto - bonus ball bug'
    PRECONDITIONS: 1. Lotto icon should be preconfigured in Sports Menu Ribbon and/or A-Z Page via CMS
    PRECONDITIONS: 2. Launch Invictus application
    PRECONDITIONS: To get a list of lotteries and draws use following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Lottery/X.XX/LotteryToDraw
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    """
    keep_browser_open = True

    def test_001_tap_on_lotto_icon_from_sports_menu_ribbon_or_a_z_page(self):
        """
        DESCRIPTION: Tap on 'Lotto' icon (from Sports Menu Ribbon or A-Z page)
        EXPECTED: 'Lotto' page is opened
        """
        self.navigate_to_page(name='lotto')
        self.site.wait_content_state(state_name='lotto')

    def test_002_tap_on_each_of_the_following_lotteries___ny_lotto___spanish_lotto___irish_lotto___49s_lotto___hong_kong_lotto___singapore_lotto___daily_million___canadian_lotto(self):
        """
        DESCRIPTION: Tap on each of the following Lotteries:
        DESCRIPTION: *   NY Lotto
        DESCRIPTION: *   Spanish Lotto
        DESCRIPTION: *   Irish Lotto
        DESCRIPTION: *   49's Lotto
        DESCRIPTION: *   Hong Kong Lotto
        DESCRIPTION: *   Singapore Lotto
        DESCRIPTION: *   Daily Million
        DESCRIPTION: *   Canadian Lotto
        EXPECTED: *   The Bonus Ball checkbox is displayed for all listed Lotteries under Numbers Selector ribbon.
        EXPECTED: *   'Include Bonus Ball?' label is placed next to checkbox.
        EXPECTED: *   'Include Bonus Ball?' checkbox is NOT ticked by default.
        """
        expected_list = ['NY', '49\'S', 'DAILY MILLIONS' if self.brand == 'ladbrokes' else 'DAILY MILLION', 'IRISH', 'SPANISH', 'HONG KONG', 'SINGAPORE', 'CANADIAN']
        lotto_carousel = self.site.lotto.lotto_carousel.items_as_ordered_dict
        self.assertTrue(lotto_carousel, msg='No Lottery Selector Carousel items found')

        actual_list = [x for x in lotto_carousel.keys()]
        for item in actual_list:
            if item.upper() in expected_list:
                self.site.lotto.lotto_carousel.click_item(item)
                tab_content = self.site.lotto.tab_content
                self.assertTrue(tab_content, msg='Lotto tab content didn\'t found')
                self.assertTrue(tab_content.has_include_bonus_ball(), msg='Include Bonus Ball? label is not displayed')
                self.assertTrue(tab_content.include_bonus_ball_check, msg='Include Bonus Ball? checkbox is not displayed')
                self.assertFalse(tab_content.include_bonus_ball_check.is_selected(), msg='Include Bonus Ball? checkbox is checked by default')
                self.__class__.actual_lotto_name = item
            else:
                self.site.lotto.lotto_carousel.click_item(item)
                tab_content = self.site.lotto.tab_content
                self.assertTrue(tab_content, msg='Lotto tab content didn\'t found')
                self.assertFalse(tab_content.has_include_bonus_ball(), msg='Include Bonus Ball? label is displayed')

    def test_003_select_numbers_for_selected_lottery_wheels(self):
        """
        DESCRIPTION: Select numbers for selected Lottery wheels
        EXPECTED: *   Selected numbers are displayed appropriately on wheels
        EXPECTED: *   Odds is displayed according to '**priceNum**' & '**priceDen**' attributes by '**numberCorrect**' that correspond to quantity of numbers selected
        """
        lucky_buttons = list(self.site.lotto.tab_content.lucky_buttons.items_as_ordered_dict.values())
        self.assertTrue(lucky_buttons, msg='Lucky Numbers are not present')
        lucky_buttons[0].click()
        actual_priceNum, actual_priceDen = self.site.lotto.tab_content.odd_value.split("/")
        lotto_filter = self.ss_query_builder.add_filter(simple_filter(LEVELS.LOTTERY, ATTRIBUTES.HAS_OPEN_DRAW))
        lotto_resp = self.ss_req.ss_lottery_to_draw(query_builder=lotto_filter)
        ids_to_exclude = ['7', '20', '26', '27'] if self.brand != 'ladbrokes' else ['1801', '1806']
        excluded = [x for x in lotto_resp if x['lottery']['id'] not in ids_to_exclude]
        lotto_name_list = [x['lottery']['description'] for x in excluded]
        lotto_data_list = [x['lottery']['children'] for x in excluded]
        lotto_dict = dict(zip(lotto_name_list, lotto_data_list))
        for lotto_name, lotto in lotto_dict.items():
            if self.actual_lotto_name in lotto_name:
                for item in lotto:
                    if item['lotteryPrice']['numberCorrect'] == '3':
                        self.assertEqual(item['lotteryPrice']['priceNum'], actual_priceNum, msg=f'Actual numerator "{actual_priceNum}" is not equal to expected "{item["lotteryPrice"]["priceNum"]}"')
                        self.assertEqual(item['lotteryPrice']['priceDen'], actual_priceDen, msg=f'Actual denominator "{actual_priceDen}" is not equal to expected "{item["lotteryPrice"]["priceDen"]}"')
                        break
                break

    def test_004_tap_on_the_toggle(self):
        """
        DESCRIPTION: Tap on the toggle
        EXPECTED: *   Selected numbers remain
        EXPECTED: *   The relevant odds for the selected Lottery shoud be displayed according to SS 'name' attribute
        EXPECTED: e.g. New York Lotto:
        EXPECTED: **Toggle OFF: **
        EXPECTED: <lottery id="6" sort="NYL" name="|N.Y. Lotto 6 ball|" description="|N.Y. Lotto|" />
        EXPECTED: <lotteryPrice id="18" lotteryId="6" numberCorrect="3" numberPicks="3" priceNum="1250" priceDen="1" />
        EXPECTED: **Toggle ON:**
        EXPECTED: <lottery id="8" sort="NYL7" name="|N.Y. Lotto 7 ball|" description="|N.Y. Lotto|" />
        EXPECTED: <lotteryPrice id="33" lotteryId="8" numberCorrect="3" numberPicks="3" priceNum="600" priceDen="1" />
        """
        # these steps are not applicable - functionality changed

    def test_005_tap_off_the_toggle(self):
        """
        DESCRIPTION: Tap off the toggle
        EXPECTED: *   **"-" **is displayed in each of the Wheels by default
        EXPECTED: *   Toggle default state is displayed (see step 2)
        """
        # these steps are not applicable - functionality changed

    def test_006_tap_on_each_of_the_following_lotteries___australian_tattslotto___australian_ozlotto___french_lotto___german_lotto(self):
        """
        DESCRIPTION: Tap on each of the following Lotteries:
        DESCRIPTION: *   Australian Tattslotto
        DESCRIPTION: *   Australian Ozlotto
        DESCRIPTION: *   French Lotto
        DESCRIPTION: *   German Lotto
        EXPECTED: The Bonus Ball checkbox is hidden for the listed Lotteries.
        """
        # covered in step 2
