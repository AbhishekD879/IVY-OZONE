import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C64378786_Verify_whether_Freebet_and_Ticket_prizes_can_be_added_in_prize_table_and_Trigger_id_should_be_stored_in_database_as_per_the_CMS_configuration(Common):
    """
    TR_ID: C64378786
    NAME: Verify whether Freebet and Ticket prizes can be added in prize table and Trigger id should be stored in database as per the CMS configuration
    DESCRIPTION: Freebet and Ticket prizes can be added in prize table and Trigger id should be stored in database as per the CMS configuration
    PRECONDITIONS: 1.load CMS and login to application
    PRECONDITIONS: 2.Navigate to 5-A side showdown -&gt;5-A side showdown
    PRECONDITIONS: 3.load the Kibana application
    """
    keep_browser_open = True

    def test_001_click_on_create_a_contest_and_enter_the_contest_name_stake_and_start_time(self):
        """
        DESCRIPTION: click on create a contest and enter the contest name, stake and start time
        EXPECTED: User should give all the details and able to save the contest
        """
        pass

    def test_002_in_the_cms_contest_page_click_on_add_a_prize_button(self):
        """
        DESCRIPTION: In the CMS contest page click on "Add a prize" button
        EXPECTED: prize configuration page should be open and fill the required details(prize type,prize value,# of entries/% of field, Trigger id)
        """
        pass

    def test_003_select_freebet_option_from_the_prize_type_dropdown_and_enter_all_the_required_fields_prize_typeprize_value_of_entries__of_field_trigger_id_and_click_on_save(self):
        """
        DESCRIPTION: Select Freebet option from the prize Type dropdown and enter all the required fields prize type,prize value,# of entries, % of field, Trigger id and click on save
        EXPECTED: user should be able to add Freebet column in prize table as per the given details
        """
        pass

    def test_004_select_ticket_option_from_the_prize_type_dropdown_and_enter_all_the_required_fields_prize_typeprize_value_of_entries__of_field_trigger_id_and_click_on_save(self):
        """
        DESCRIPTION: Select Ticket option from the prize Type dropdown and enter all the required fields prize type,prize value,# of entries, % of field, Trigger id and click on save
        EXPECTED: user should be able to add Ticket column in prize table as per the given details
        """
        pass

    def test_005_in_contest_page_click_on_edit_option_for_freebet_ticket_prizes_and_check_added_prizes_can_be_editable_and_saved(self):
        """
        DESCRIPTION: In contest page click on edit option for Freebet, Ticket prizes and check added prizes can be editable and saved
        EXPECTED: prize configuration page should open, user can be able to edit the options and saved with edited options
        """
        pass

    def test_006_after_the_automatic_prize_distributionafter_the_90_minutes_completion_of_event_trigger_id_for_the_customers_who_awarded_prizes_should_be_stored_in_the_database_as_cms_config(self):
        """
        DESCRIPTION: After the automatic prize distribution(after the 90 minutes completion of event), Trigger id for the customers who awarded prizes should be stored in the database as CMS config
        EXPECTED: user should be able to see the reward id column in kibana and mongo DB database(check with dev support) for the users who got prizes, reward id contains trigger id as configured in CMS
        """
        pass
