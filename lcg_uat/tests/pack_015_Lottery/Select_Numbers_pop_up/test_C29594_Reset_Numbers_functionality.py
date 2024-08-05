import pytest
from selenium.common.exceptions import StaleElementReferenceException

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.hl  # sometimes failed on lads-beta. works fine on beta2 with the real data
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.low
@pytest.mark.lotto
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.desktop
@pytest.mark.safari
@vtest
class Test_C29594_Reset_Numbers_functionality(BaseSportTest):
    """
    TR_ID: C29594
    NAME: Verify Lotto 'Reset Numbers' functionality
    """
    keep_browser_open = True
    bet_amount = '0.01'

    def test_000_open_lotto(self):
        """
        DESCRIPTION: Go to Lotto
        """
        self.navigate_to_page(name='lotto')
        self.site.wait_content_state('lotto')

    def test_002_choose_number(self):
        """
        DESCRIPTION: Select lucky numbers using "Lucky Dip" functionality
        """
        lucky_buttons = self.site.lotto.tab_content.lucky_buttons.items_as_ordered_dict
        self.assertTrue(lucky_buttons, msg='Lucky Numbers are not present')
        list(lucky_buttons.values())[0].click()
        result = wait_for_result(lambda: '-' not in list(self.site.lotto.tab_content.number_selectors.items_as_ordered_dict.keys())[0],
                                 timeout=5,
                                 name='Lucky numbers to be selected')
        self.assertTrue(result, msg='Lucky numbers is not selected')

        number_selectors = self.site.lotto.tab_content.number_selectors.items_as_ordered_dict
        selected_numbers = []
        for number_selector_name, number_selector in number_selectors.items():
            if '-' not in number_selector_name:
                selected_numbers.append(number_selector_name)
        self.assertTrue(selected_numbers, msg='No items are selected')

    def test_003_press_reset_numbers_on_page(self):
        """
        DESCRIPTION: Press 'Reset Numbers' on lotto page
        """
        lotto = self.site.lotto.tab_content
        number_selectors = lotto.number_selectors.items_as_ordered_dict
        self.assertTrue(number_selectors, msg='Lotto number selectors are not present')
        reset_numbers = lotto.reset_numbers
        self.assertTrue(reset_numbers.is_enabled(), msg='Reset Numbers Button is not active')
        reset_numbers.click()
        result = wait_for_result(lambda: '-' in list(self.site.lotto.tab_content.number_selectors.items_as_ordered_dict.keys())[0],
                                 timeout=5,
                                 bypass_exceptions=(StaleElementReferenceException, VoltronException),
                                 name='Lucky numbers to be unselected')
        self.assertTrue(result, msg='Lucky numbers is selected')

        number_selectors = lotto.number_selectors.items_as_ordered_dict

        self.assertTrue(number_selectors, msg='Lotto number selectors are not present')
        for number_selector_name, number_selector in number_selectors.items():
            number_selector_name = number_selector_name.split(' ')[1]
            self.assertEqual('-', number_selector_name,
                             msg=f'Number is not cleared. Have "{number_selector_name}" instead')

    def test_004_choose_number(self):
        """
        DESCRIPTION: Select lucky numbers using "Lucky Dip" functionality
        """
        self.test_002_choose_number()

    def test_005_reset_numbers_on_popup(self):
        """
        DESCRIPTION: Press 'Reset Numbers' on 'Choose Your Lucky Numbers Below' dialog
        """
        number_selectors = self.site.lotto.tab_content.number_selectors.items_as_ordered_dict
        self.assertTrue(number_selectors, msg='Lotto number selectors are not present')
        list(number_selectors.values())[-1].click()
        choose_lucky_num_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW, timeout=10)
        self.assertTrue(choose_lucky_num_dialog, msg='"Choose Your Lucky Numbers" dialog is not shown')
        choose_lucky_num_dialog.reset_button.click()
        choose_lucky_num_dialog.close_dialog()
        number_selectors = self.site.lotto.tab_content.number_selectors.items_as_ordered_dict
        self.assertTrue(number_selectors, msg='Lotto number selectors are not present')
        for number_selector_name, number_selector in number_selectors.items():
            number_selector_name = number_selector_name.split(' ')[1]
            self.assertEqual('-', number_selector_name,
                             msg=f'Number is not cleared. Have "{number_selector_name}" instead')
