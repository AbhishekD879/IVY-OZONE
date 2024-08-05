from datetime import datetime
import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.lotto
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.low
@pytest.mark.desktop
@pytest.mark.medium
@vtest
class Test_C29585_Lottery_Info_line(BaseSportTest):
    """
    TR_ID: C29585
    NAME: Lottery Info line
    """
    datetime_pattern = r'^\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}$'
    info_line_pattern_body = r'^(.+) LOTTERY - BET UNTIL [0-3]\d\/[0-1]\d\/20[1-2]\d [0-2]\d:[0-5]\d'

    keep_browser_open = True

    def test_000_tap_lotto(self):
        """
        DESCRIPTION: Tap 'Lotto' icon (from Sports Menu Ribbon or A-Z page)
        """
        self.navigate_to_page(name='lotto')
        self.site.wait_content_state('lotto')

    def test_001_tap_lotto_icon_on_carousel(self):
        """
        DESCRIPTION: Tap on any 'Lotto' icon within Lottery Selector Carousel
        EXPECTED: Each Lottery has Info line in between the lottery selector and Numbers Selector Module
        EXPECTED: Info line shows the name of the Lottery and time left for the next draw
        EXPECTED: Lottery info line should be in the following format:
        EXPECTED: The date, time and format is displayed in GMT/UK:
        EXPECTED: - Date format: DD/MM/YYYY
        EXPECTED: - Time format: HH:MM 24 hour clock (00:00 - 23:59)
        EXPECTED: - Count down is in a next line (omit days if there is 0 day, omit hours if there is 0 hour left)
        EXPECTED: - Omit '0', if left time is one-digit figure
        EXPECTED: - 'Information' icon is displayed in the right side of info line
        """
        carousel_names = self.site.lotto.lotto_carousel.items_as_ordered_dict
        self.assertTrue(carousel_names, msg='No Lottery Selector Carousel items found')
        for lottery_name, lottery in carousel_names.items():
            self.site.lotto.lotto_carousel.click_item(lottery_name)
            content = self.site.lotto.tab_content
            self.assertTrue(content.info_panel.is_displayed(),
                            msg='Info Line is not present on Lotto page')

            lottery_name_selected = content.info_panel.lottery_name
            lottery_name = lottery_name.upper() if self.brand == 'ladbrokes' else lottery_name

            self.assertEqual(lottery_name, lottery_name_selected,
                             msg='Lottery name on Lottery Carousel "%s" is not same as in Lottery title under it "%s"'
                             % (lottery_name, lottery_name_selected))

            # Date format: DD/MM/YYYY, Time format: HH:MM 24 hour clock (00:00 - 23:59)
            self.assertRegexpMatches(content.info_panel.bet_until_time, self.datetime_pattern,
                                     msg='Lottery datetime "%s" doesn\'t match expected datetime format "%s"' %
                                         (content.info_panel.bet_until_time,
                                          self.datetime_pattern))

            self.assertRegexpMatches(content.info_panel.info_line, self.info_line_pattern_body,
                                     msg='Info Line doesn\'t match expected format '
                                     '"\'Description\' + "- bet until" + "shutAtTime"", and is "%s"'
                                         % content.info_panel.info_line)
            # Count down is in a next line (omit days if there is 0 day, omit hours if there is 0 hour left)

            # VOL-3093
            date_time_array = [s for s in content.info_panel.info_line_as_list if "MINUTE" in s]
            seconds = 0
            for iterating_var in date_time_array:

                number = int(''.join(list(filter(str.isdigit, str(iterating_var)))))
                alpha = iterating_var.replace(str(number), '').strip()

                if number > 1:
                    self.assertTrue('S' in alpha, msg='Incorrect "%s" string' % iterating_var)
                if number == 1:
                    self.assertTrue('S' not in alpha, msg='Incorrect "%s" string' % iterating_var)

                if "DAY" in alpha:
                    seconds += number * 24 * 60 * 60
                if "HOUR" in alpha:
                    seconds += number * 60 * 60
                if "MINUTE" in alpha:
                    seconds += number * 60

            calc_countdown_val = datetime.strptime(content.info_panel.bet_until_time,
                                                   '%d/%m/%Y %H:%M') - datetime.now()
            days = calc_countdown_val.days
            hours = calc_countdown_val.seconds // 3600
            minutes = calc_countdown_val.seconds % 3600 / 60
            seconds2 = days * 24 * 60 * 60 + hours * 60 * 60 + minutes * 60

            self.assertTrue(seconds2 - seconds <= 60,
                            msg='Incorrect text in info line "%s"' % content.info_panel.info_line)

            self.assertTrue(content.info_panel.info_btn.is_displayed(),
                            msg='Information icon is not displayed for Lottery')
