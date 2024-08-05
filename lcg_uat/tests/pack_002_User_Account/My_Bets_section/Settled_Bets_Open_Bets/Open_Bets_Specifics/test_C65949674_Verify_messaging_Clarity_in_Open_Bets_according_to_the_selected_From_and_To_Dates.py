from datetime import datetime, timedelta
import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.open_bets
@pytest.mark.bet_history_open_bets
@vtest
class Test_C65949674_Verify_messaging_Clarity_in_Open_Bets_according_to_the_selected_From_and_To_Dates(Common):
    """
    TR_ID: C65949674
    NAME: Verify messaging Clarity in Open Bets according to the selected From and To Dates
    DESCRIPTION: This testase verifies  messaging Clarity in Open Bets according to the selected From and To Dates
    PRECONDITIONS: User should be on Open bets of My bets area
    """
    keep_browser_open = True
    default_days = 30
    open_bet_message = "No open bets placed within the last " + str(default_days) + " days."

    def validation_of_open_bet_message(self, number_of_days=0):
        past_date = datetime.now() - timedelta(days=number_of_days)
        date_format = "%m-%d-%Yyyy"
        date = self.get_date_time_formatted_string(date_time_obj=past_date, time_format=date_format, url_encode=False)[
               :-3]
        self.site.open_bets.tab_content.date_picker.date_from.date_picker_value = date
        if number_of_days == 0:
            open_bet_message = "No open bets placed today."
        elif number_of_days < 0:
            open_bet_message = "Please select a valid time range"
        elif number_of_days > 365:
            open_bet_message = "No open bets placed within the time period specified."
        else:
            default_days = number_of_days + 1
            open_bet_message = "No open bets placed within the last " + str(default_days) + " days."
        wait_for_haul(10)
        no_bets_placed_text = self.site.open_bets.tab_content.no_open_bets_text
        self.assertEqual(no_bets_placed_text.upper(), open_bet_message.upper(),
                         msg=f'expected text is "{open_bet_message.upper()}" but actual is "{no_bets_placed_text.upper()}"')

    def test_001_launch_the_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the Application and login with valid credentials
        EXPECTED: User should launch the Application and login Successfully
        """
        self.site.login(username=tests.settings.no_bet_history_user, async_close_dialogs=False)

    def test_002_navigate_to_my_bets_section(self):
        """
        DESCRIPTION: Navigate to My bets Section
        EXPECTED: user can able to navigate to the My Bets
        """
        #covered in below step

    def test_003_click_on_open_bets_tab(self):
        """
        DESCRIPTION: Click on Open Bets Tab
        EXPECTED: Open Bets Tab is loaded successfully
        """
        self.navigate_to_page(name='open-bets')
        self.site.wait_content_state(state_name='OpenBets')

    def test_004_verify_there_are_no_open_bets_placed_within_the_last_30_days(self):
        """
        DESCRIPTION: Verify there are No open bets placed within the last 30 days
        EXPECTED: Current login user shouldn't placed any bet within 30 days
        """
        #covered in below step

    def test_005_verify_the_message_that_is_displaying_in_the_open_bets(self):
        """
        DESCRIPTION: Verify the message that is displaying in the open bets
        EXPECTED: user can be able to see the message "No open bets placed within the last 30 days"
        """
        no_bets_placed_text = self.site.open_bets.tab_content.no_open_bets_text
        self.assertEqual(no_bets_placed_text.upper(), self.open_bet_message.upper(), msg=f'expected text is "{self.open_bet_message.upper()}" but actual is "{no_bets_placed_text.upper()}"')

    def test_006_verify_the_clarity_display_message_should_be_dynamic(self):
        """
        DESCRIPTION: Verify the clarity display message should be dynamic
        EXPECTED: the number of days in the clarity message should be changing as the user keeps changing the date in filter
        """
        self.validation_of_open_bet_message(number_of_days=59)

    def test_007_keep_changing_the_date_in_the_filter(self):
        """
        DESCRIPTION: Keep changing the date in the filter
        EXPECTED: Clarity message should be changing as the user keeps changing the date in the filter(If the To Date is current date/day).User can able to see the message as - No Open bets placed within the last X days.
        """
        self.validation_of_open_bet_message(number_of_days=140)


    def test_008_select_the_filter_for_1_day_if_the_to_date_is_current_dateday(self):
        """
        DESCRIPTION: Select the filter for 1 day (If the To Date is current date/day)
        EXPECTED: User can able to see the message- No open bets placed today
        """
        self.validation_of_open_bet_message(number_of_days=0)

    def test_009_select_the_date_range_which_isnt_upto_the_current_day_ie_to_date_is_not_current_dateday(self):
        """
        DESCRIPTION: Select the date range which isn't upto the current day, i.e, To Date is not current date/day
        EXPECTED: User should be able to see the clarity message as - No Open bets placed within the timeperiod specified
        """
        self.validation_of_open_bet_message(number_of_days=470)

    def test_010_verify_when_user_selects_the_filter_amplt_365_days(self):
        """
        DESCRIPTION: Verify when user selects the filter &amp;lt;= 365 days
        EXPECTED: user would be displaying with No open bets placed within the last x days (If the TO Date is current date/da
        """
        self.validation_of_open_bet_message(number_of_days=364)

    def test_011_verify_when_user_selects_the_filter_ampgt_365_days(self):
        """
        DESCRIPTION: Verify when user selects the filter &amp;gt;= 365 days
        EXPECTED: user would be displaying with No open bets placed within the time period specified
        """
        self.validation_of_open_bet_message(number_of_days=390)

    def test_012_verify_when_user_selects_the_filter_where_from_date_is_yesterday_and_to_date_is_current_daydate(self):
        """
        DESCRIPTION: Verify when user selects the filter where From Date is Yesterday and To Date is current Day/Date
        EXPECTED: User can see the message No open bets placed within the last 2 day. (If the TO Date is current date/day)
        """
        self.validation_of_open_bet_message(number_of_days=1)

    def test_013_verify_when_user_selects_the_the_future_date_in_from_date(self):
        """
        DESCRIPTION: Verify when user selects the the future Date in From Date
        EXPECTED: User can see the message Please select a valid time range
        """
        self.validation_of_open_bet_message(number_of_days=-2)
