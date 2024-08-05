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
class Test_C64378784_Verify_whether_the_new_column_Trigger_id_is_added_for_Freebet_and_Ticket_in_paytable_during_contest_creation_in_CMS(Common):
    """
    TR_ID: C64378784
    NAME: Verify whether the new column Trigger id is added for Freebet and Ticket in paytable during contest creation in CMS
    DESCRIPTION: new Trigger id column is displaying in paytable during contest creation in CMS
    PRECONDITIONS: 1.load CMS and login to appliaction
    PRECONDITIONS: 2.Navigate to 5-A side showdown -&gt;5-A side showdown
    """
    keep_browser_open = True

    def test_001_click_on_create_a_contest_and_enter_the_contest_name_stake_andstart_time(self):
        """
        DESCRIPTION: click on create a contest and enter the contest name, stake and
        DESCRIPTION: start time
        EXPECTED: User should give all the details and able to save the contest
        """
        pass

    def test_002_in_the_cms_contest_page_click_on_add_a_prize_button(self):
        """
        DESCRIPTION: In the CMS contest page click on "Add a prize" button
        EXPECTED: prize configuration pop up page should be open and fill the
        EXPECTED: required details(prize type,prize value,# of entries/% of
        EXPECTED: field,offer id)
        """
        pass

    def test_003_select_freebet_option_from_the_prize_type_dropdown(self):
        """
        DESCRIPTION: Select Freebet option from the prize Type dropdown
        EXPECTED: user able to select the freebet option
        """
        pass

    def test_004_verify_new_trigger_id_column_is_added(self):
        """
        DESCRIPTION: verify new Trigger id column is added
        EXPECTED: user can able to see new Trigger id column after the # of entries field
        """
        pass

    def test_005_select_ticket_option_from_the_prize_typedropdown(self):
        """
        DESCRIPTION: Select Ticket option from the prize Type
        DESCRIPTION: dropdown
        EXPECTED: user able to select the Ticket option
        """
        pass

    def test_006_verify_new_trigger_id_column_is_added(self):
        """
        DESCRIPTION: verify new Trigger id column is added
        EXPECTED: user can able to see new Trigger id column after the # of entries
        EXPECTED: field
        """
        pass
