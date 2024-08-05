import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.5_a_side
@vtest
class Test_C60546383_Verify_the_display_of_Prize_Pool_information_based_on_Prize_pool_logic(Common):
    """
    TR_ID: C60546383
    NAME: Verify the display of Prize Pool information based on Prize pool logic
    DESCRIPTION: This Test case verifies the display of Prize pool information is based on Prize pool logic
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: **How to Configure Menu Item**
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: **To Qualify for Showdown**
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes(self):
        """
        DESCRIPTION: Login to Ladbrokes
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_5_a_side_showdown__contest__leaderboard(self):
        """
        DESCRIPTION: Navigate to 5-A Side showdown > Contest > Leaderboard
        EXPECTED: User should be navigated to Leaderboard page
        """
        pass

    def test_003_verify_the_display_of_prize_information_in_prize_grid_when_below_configurations_are_set_in_cmscms_configurations_cms__5_a_side_showdown__contest_details_page__prize_pool__add_a_prize__of_entries_is_configured_in_cms(self):
        """
        DESCRIPTION: Verify the display of Prize information in Prize grid when below configurations are set in CMS
        DESCRIPTION: **CMS Configurations**
        DESCRIPTION: * CMS > 5-A Side showdown > Contest Details page > Prize Pool > Add a Prize
        DESCRIPTION: * **# of Entries** is configured in CMS
        EXPECTED: * Prize should be displayed next to the allocated range of entries
        EXPECTED: * This should be a fixed value that can only be changed in CMS
        EXPECTED: **Example**
        EXPECTED: **CMS Configuration**
        EXPECTED: * Prize Type = Ticket
        EXPECTED: * Prize Value = £1
        EXPECTED: * # of Entries = 1-10
        EXPECTED: **Prize Logic**
        EXPECTED: * Current Entries: 500
        EXPECTED: * Prize Awarded: 1-10 = £1 Ticket
        """
        pass

    def test_004_verify_the_display_of_prize_information_in_prize_grid_when_below_configurations_are_set_in_cmscms_configurations_cms__5_a_side_showdown__contest_details_page__prize_pool__add_a_prize__of_field_is_configured_in_cms(self):
        """
        DESCRIPTION: Verify the display of Prize information in Prize grid when below configurations are set in CMS
        DESCRIPTION: **CMS Configurations**
        DESCRIPTION: * CMS > 5-A Side showdown > Contest Details page > Prize Pool > Add a Prize
        DESCRIPTION: * **% of Field** is configured in CMS
        EXPECTED: * Calculation is based on how many teams are currently entered in the contest
        EXPECTED: * This should be a dynamic value that constantly updates as the size of the entries grows
        EXPECTED: **Example**
        EXPECTED: **CMS Configuration**
        EXPECTED: * Prize Type = Ticket
        EXPECTED: * Prize Value = £1
        EXPECTED: * % of Field = 10%
        EXPECTED: **Prize Logic**
        EXPECTED: * Current Entries: 500
        EXPECTED: * Prize Awarded: 1-50 = £1 Ticket
        """
        pass

    def test_005_verify_the_display_of_prize_information_in_prize_grid_when_below_configurations_are_set_in_cmscms_configurations_cms__5_a_side_showdown__contest_details_page__prize_pool__add_a_prize__of_field_is_configured_in_cms__of_entries_is_configured_in_cms(self):
        """
        DESCRIPTION: Verify the display of Prize information in Prize grid when below configurations are set in CMS
        DESCRIPTION: **CMS Configurations**
        DESCRIPTION: * CMS > 5-A Side showdown > Contest Details page > Prize Pool > Add a Prize
        DESCRIPTION: * **% of Field** is configured in CMS
        DESCRIPTION: * **# of Entries** is configured in CMS
        EXPECTED: **When both # of Entries and % of Field are configured**
        EXPECTED: **# of Entries > % of Field**
        EXPECTED: * Prizes are awarded as per # of Entries
        EXPECTED: **% of Field > # of Entries**
        EXPECTED: * Prizes are awarded as per % of Field
        EXPECTED: **% of Field = # of Entries** (Number of customers rewarded with prizes is same)
        EXPECTED: * Prizes are awarded as per # of Entries
        EXPECTED: **Example**
        EXPECTED: **CMS Config**
        EXPECTED: * Prize Type = Ticket
        EXPECTED: * Prize Value = £1
        EXPECTED: * # of Entries = 1-100
        EXPECTED: * % of Field = 10%
        EXPECTED: **Current Entries: 500**
        EXPECTED: Prize Awarded: 1-100 = £1 Ticket
        EXPECTED: **Current Entries: 1500**
        EXPECTED: Prize Awarded: 1-150 = £1 Ticket
        EXPECTED: So at the start of the contest a £1 Ticket goes to the top 1-100 BUT as the field grows, as soon as 10% of the field > 100 then calculation switches to % of Field.
        EXPECTED: **Note:** As % of Field is dynamically updated depending on the number of Teams entered Prizes awarded are also updated accordingly
        """
        pass

    def test_006_verify_the_display_of_prize_information_in_prize_grid_when_exceptions_are_configured_in_cmscms_configurations_cms__5_a_side_showdown__contest_details_page__prize_pool__add_a_prize__of_entries_is_configured_in_cms(self):
        """
        DESCRIPTION: Verify the display of Prize information in Prize grid when Exceptions are Configured in CMS
        DESCRIPTION: **CMS Configurations**
        DESCRIPTION: * CMS > 5-A Side showdown > Contest Details page > Prize Pool > Add a Prize
        DESCRIPTION: * **# of Entries** is configured in CMS
        EXPECTED: **Example 1** : In Pay table it is defined as
        EXPECTED: * Free bet 1-100,*3
        EXPECTED: * Voucher 1-200
        EXPECTED: **Then will display**
        EXPECTED: * 1-2 free bet +voucher
        EXPECTED: * 3 voucher
        EXPECTED: * 4-100 free bet +voucher
        EXPECTED: * 101-200 Voucher
        EXPECTED: **Example 2** :In Pay table it is defined as
        EXPECTED: * Free bet : 1-100,*55
        EXPECTED: * Voucher 1-200
        EXPECTED: **Then will display**
        EXPECTED: * 1-54 Free bet + Voucher
        EXPECTED: * 55 Voucher
        EXPECTED: * 56-100 Free bet + Voucher
        EXPECTED: * 101 - 200 Voucher
        EXPECTED: **The prizes can be excluded for a particular range of customers like *1-10**
        EXPECTED: * Free bet : 1-100,*10-20
        EXPECTED: * Voucher 1-200
        EXPECTED: **Then display**
        EXPECTED: * 1-10 Free Bet + Voucher
        EXPECTED: * 10-20 Voucher
        EXPECTED: * 21-100 Free bet + Voucher
        EXPECTED: * 101-200 Voucher
        """
        pass

    def test_007_verify_the_display_of_prize_information_in_prize_grid_when__of_field_configured_in_cms_has_decimal_valuescms_configurations_cms__5_a_side_showdown__contest_details_page__prize_pool__add_a_prize__of_field_is_configured_in_cms_has_decimal_values(self):
        """
        DESCRIPTION: Verify the display of Prize information in Prize grid when % of field Configured in CMS has decimal values
        DESCRIPTION: **CMS Configurations**
        DESCRIPTION: * CMS > 5-A Side showdown > Contest Details page > Prize Pool > Add a Prize
        DESCRIPTION: * **% of field** is configured in CMS has decimal values
        EXPECTED: **Follow below logic when % of field is having decimal values**
        EXPECTED: * below 0.4 - we will not display any value
        EXPECTED: * 0.5 to 1 : will display 1
        EXPECTED: * 1 - 1.4 : will display 1
        EXPECTED: * 1.5 - 2 : will display 2
        EXPECTED: * 2 - 2.4 : will display 2
        EXPECTED: * 2.5 - 3: will display 3
        EXPECTED: **Note:** We will not display the Prize value at the FE when the % field is less than 0.4
        """
        pass
