from datetime import date
import pytest
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_haul, wait_for_result

@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.avtar_menu
@pytest.mark.adhoc_suite
@vtest
class Test_C65950085_Validate_Avtar_menu_spending_controls_gambling_controls(Common):
    """
    TR_ID: C65950085
    NAME: Validate Avtar menu spending controls gambling controls
    DESCRIPTION: This test case is to verify the Avtar menu spending controls gambling controls
    PRECONDITIONS: 1.User should have vaild login credentials to log into the application
    """
    keep_browser_open = True
    limits = {
        'Daily Deposit Limit': 20,
        'Weekly Deposit Limit': 50,
        'Monthly Deposit Limit': 100
    }

    deposit_limit_tab = 'Deposit limits'
    max_stake_limit_tab = 'Max Stake Limit'
    deposit_curfew_tab = 'Deposit Curfew'

    weekdays = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

    def create_new_user(self):
        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username, amount='5',
                                                                     card_number='6759649826438453',
                                                                     card_type='maestro',
                                                                     expiry_month='12',
                                                                     expiry_year='2080',
                                                                     cvv='111'
                                                                     )
        return username

    def remove_limit(self):
        deposit_limit_items = self.site.spending_controls.tab_content.items_as_ordered_dict
        for item_name, item in deposit_limit_items.items():
            item.remove.click()
            wait_for_haul(8)

    def set_limits(self):
        deposit_limit_items = self.site.spending_controls.tab_content.items_as_ordered_dict
        for item_name, item in deposit_limit_items.items():
            item.set_limit_button.click()
            item.set_limit_input.value = self.limits[item_name]
        self.site.spending_controls.save.click()

    def go_to_deposit_page(self):
        self.navigate_to_page('/')
        self.site.header.right_menu_button.click()
        self.site.wait_content_state_changed()
        right_menu = self.site.right_menu.items_as_ordered_dict
        deposit = next(
            (item for item_name, item in right_menu.items() if item_name.upper() == 'DEPOSIT'), None)
        deposit.click()
        self.site.wait_content_state_changed()

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home page should loaded succesfully
        """
        self.site.go_to_home_page()
        user_name = self.create_new_user()
        self.site.login(username=user_name)

    def test_002_click_on_spending_controls(self):
        """
        DESCRIPTION: Click on spending controls
        EXPECTED: User should be able to see the data
        """
        self.site.header.right_menu_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        right_menu = self.site.right_menu.items_as_ordered_dict
        gambling_control_menu_item = next((item for item_name, item in right_menu.items() if item_name.upper() == 'GAMBLING CONTROLS'), None)
        gambling_control_menu_item.click()
        gambling_controls = wait_for_result(lambda:self.site.gambling_controls.items_as_ordered_dict,timeout=100,name="waiting for gambling oage controls")
        spending_control_obj = next((item for item_name, item in gambling_controls.items() if item_name.upper() == 'SPENDING CONTROLS'), None)
        spending_control_obj.click()
        spending_controls_menu_items = spending_control_obj.items_as_ordered_dict
        next(iter(spending_controls_menu_items.values())).click()
        self.site.wait_content_state_changed()

    def test_003_verify_by_swtiching_the_tabs(self):
        """
        DESCRIPTION: Verify by swtiching the tabs
        EXPECTED: User should be navigated with in the tab
        """
        # covering in below steps

    def test_004_verify_by_setting__the_depoist__limits_dailyweeklymontly(self):
        """
        DESCRIPTION: Verify by Setting  the depoist  limits Daily/weekly/montly
        EXPECTED: Once the user crossed the depoist limit it should throw error .
        """
        current_tab = self.site.spending_controls.tabs_menu.current
        self.assertEqual(self.deposit_limit_tab.upper(), current_tab.upper(), f'tab is not {self.deposit_limit_tab}')
        self.set_limits()
        self.__class__.spending_controls_url = self.device.get_current_url()
        self.go_to_deposit_page()
        wait_for_haul(10)
        for item_name in self.limits.keys():
            self.site.deposit.amount.input.value = self.limits[item_name] + 5
            self.site.deposit.cvv_2.click()
            self.assertTrue(self.site.deposit.is_warning_msg_came, 'warning msg is not came')
        self.device.navigate_to(url=self.spending_controls_url)
        self.remove_limit()

    def test_005_verify_by_setting_the_max_stake_limit(self):
        """
        DESCRIPTION: Verify by setting the max stake limit
        EXPECTED: User should not be able to place bet more than max stake limit in slot games
        """
        tab = self.site.spending_controls.tabs_menu.click_item(self.max_stake_limit_tab)
        wait_for_haul(3)
        current_tab = self.site.spending_controls.tabs_menu.current.upper()
        self.assertEqual(self.max_stake_limit_tab.upper(), current_tab, f'Tab is not switched to {current_tab}')
        max_stake_item = self.site.spending_controls.tab_content.slots_box
        expected_limit = "5 GBP"
        max_stake_item.set_limit_button.click()
        if self.device_type == 'desktop':
            max_stake_item.max_limit_input.value = 5
            max_stake_item.save.click()
        else:
            self.site.spending_controls_overlay.max_limit_input.value = 5
            self.site.spending_controls_overlay.save.click()

        wait_for_haul(5)
        current_limit = self.site.spending_controls.tab_content.slots_box.current_limit
        self.assertEqual(current_limit, expected_limit, f'{current_limit}. limit is not set to 5')
        self.site.spending_controls.tab_content.slots_box.remove.click()
        wait_for_haul(8)

        # here we are not validating max stake in solt games. why because, we can not automate the videos

    def test_006_verify_by_clicking__depoist_curfew(self):
        """
        DESCRIPTION: Verify by clicking  depoist curfew
        EXPECTED: user should be able the acces the page with 3 tabs
        EXPECTED: a)Suggested curfew
        EXPECTED: b)Active curfew
        EXPECTED: c)saved curfew
        EXPECTED: d)Add new curfew
        """
        self.site.spending_controls.tabs_menu.click_item(self.deposit_curfew_tab)
        wait_for_haul(6)
        current_tab = self.site.spending_controls.tabs_menu.current
        self.assertEqual(current_tab, self.deposit_curfew_tab, f'tab is not switched to {self.deposit_curfew_tab}')
        pills = self.site.spending_controls.tab_content.pills_list.items_as_ordered_dict
        expected_pills = ['Suggested Curfews', 'Active Curfews', 'Saved Curfews']
        actual_pills = list(pills.keys())
        self.assertListEqual(expected_pills, actual_pills,
                             f'Actual Pills : "{actual_pills}" is not same as Expected pills "{expected_pills}"')

    def test_007_verify_by_clicking__find_out_more(self):
        """
        DESCRIPTION: Verify by clicking  Find out more
        EXPECTED: User should able to see the popup with depoist FAQ
        """
        self.site.spending_controls.tab_content.find_out_more.click()
        wait_for_result(lambda: self.site.spending_controls_overlay, timeout=5,
                        name='"Spending Controls Overlay" button to be displayed.',
                        bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException))
        depoist_FAQ = self.site.spending_controls_overlay.is_deposit_curfew_pop_up_displayed
        self.assertTrue(depoist_FAQ, 'Deposit FAQ is not displayed after clicking on "Find out more" Button')
        self.site.spending_controls_overlay.close.click()

    def test_008_verify_by_clicking__edit_under_suggestions_curfew(self):
        """
        DESCRIPTION: Verify by clicking  edit under suggestions curfew
        EXPECTED: User should be able to edit
        """
        self.site.spending_controls.tab_content.edit_curfews.click()
        curfews = self.site.spending_controls.tab_content.curfew_list.items_as_ordered_dict
        self.assertTrue(curfews, 'Suggested Curfews are not displayed')  # 009
        for curfew_name, curfew in curfews.items():
            self.assertTrue(curfew.has_edit_icon,
                            f'edit icon is not displayed for "{curfew_name}" after clicking on "Edit curfews" button')
        self.site.spending_controls.tab_content.cancel.click()

    def test_009_verify_by_clicking_suggested_curfew(self):
        """
        DESCRIPTION: Verify by clicking suggested curfew
        EXPECTED: User should be able to see default suggested curfews
        """
        # covered in below steps

    def test_010_verify_by_clicking_active_curfew(self):
        """
        DESCRIPTION: Verify by clicking Active curfew
        EXPECTED: User should able to see all active curfews
        """
        # covered in below steps

    def test_011_verify_by__activating_at_1_curfew(self):
        """
        DESCRIPTION: Verify by  Activating at 1 curfew
        EXPECTED: Suggested curfew tab should not be seen
        """
        first_curfew_name, first_curfew = self.site.spending_controls.tab_content.curfew_list.first_item
        first_curfew.toggle.click()
        self.site.spending_controls_overlay.curfew_enable_button.click()
        wait_for_haul(3)
        self.__class__.pills = self.site.spending_controls.tab_content.pills_list.items_as_ordered_dict
        expected_pills = ['Suggested Curfews', 'Active Curfews', 'Saved Curfews']
        actual_pills = list(self.pills.keys())
        result = [pill for pill in actual_pills if pill not in expected_pills]
        self.assertFalse(result, msg=f'{result} pill not available in expected {expected_pills}')

    def test_012_verify_by_clicking_saved_curfew(self):
        """
        DESCRIPTION: Verify by clicking saved curfew
        EXPECTED: User should able to see all saved curfews
        """
        # covered in below step

    def test_013_verify_by_clicking_add_new__curfew(self):
        """
        DESCRIPTION: Verify by clicking add new  curfew
        EXPECTED: User should be able to add new curfew and once click on submit it should be shown under saved curfew
        """
        self.pills.get('Saved Curfews').click()
        self.site.spending_controls.tab_content.add_new_curfew.click()
        curfew_tab_content = self.site.spending_controls.tab_content
        curfew_tab_content.new_curfew_name.value = "CURFEW TODAY"
        fe_days = curfew_tab_content.days
        today = self.weekdays[date.today().weekday()]
        other_day = next(day for day in self.weekdays.values() if day != today)
        check_box = fe_days.get(today)
        check_box.click()
        self.site.spending_controls.tab_content.save_curfew.click()
        self.site.spending_controls_overlay.curfew_confirm_button.click()
        wait_for_haul(10)

        self.site.spending_controls.tab_content.pills_list.click_item('Active Curfews')
        curfews = self.site.spending_controls.tab_content.curfew_list.items_as_ordered_dict
        newly_created_curfew = next((curfew for name, curfew in curfews.items() if name.upper() == "CURFEW TODAY"),
                                    None)
        self.assertTrue(newly_created_curfew, 'newly created curfew is not came')
        for name, curfew in curfews.items():
            self.site.spending_controls.tab_content.edit_curfews.click()
            curfew.delete_curfew.click()
            self.site.spending_controls_overlay.delete_curfew_button.click()

        if self.site.spending_controls.tab_content.has_upcoming_curfews:
            curfews = self.site.spending_controls.tab_content.upcoming_curfews_list.items_as_ordered_dict
            for name, curfew in curfews.items():
                self.site.spending_controls.tab_content.edit_curfews.click()
                curfew.delete_curfew.click()
                self.site.spending_controls_overlay.delete_curfew_button.click()

        self.site.spending_controls.tab_content.add_new_curfew.click()
        curfew_tab_content = self.site.spending_controls.tab_content
        curfew_tab_content.new_curfew_name.value = "CURFEW OTHER"
        fe_days = curfew_tab_content.days
        check_box = fe_days.get(other_day)
        check_box.click()
        self.site.spending_controls.tab_content.save_curfew.click()
        self.site.spending_controls_overlay.curfew_confirm_button.click()
        wait_for_haul(10)

        self.site.spending_controls.tab_content.pills_list.click_item('Saved Curfews')
        curfews = self.site.spending_controls.tab_content.curfew_list.items_as_ordered_dict
        newly_created_curfew = next((curfew for name, curfew in curfews.items() if name.upper() == "CURFEW OTHER"),
                                    None)
        self.assertTrue(newly_created_curfew, 'newly created curfew is not came')
        for name, curfew in curfews.items():
            self.site.spending_controls.tab_content.edit_curfews.click()
            curfew.delete_curfew.click()
            self.site.spending_controls_overlay.delete_curfew_button.click()
