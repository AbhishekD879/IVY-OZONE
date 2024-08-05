import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28990_Verify_Selection_Information_on_Next_Races_Module(Common):
    """
    TR_ID: C28990
    NAME: Verify Selection Information on 'Next Races' Module
    DESCRIPTION: This test case is for checking selections on the 'Next Races' module
    DESCRIPTION: Jira ticket: BMA-10828 All devices - Next 4 Races
    DESCRIPTION: BMA-18626'Replace Generic Silks with Race Card Number Design (Racing)'
    PRECONDITIONS: To retrieve data from the Site Server use the following:
    PRECONDITIONS: 1) To get Class IDs use a link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:19&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Greyhound category id =19
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To get a list of all "Events" for the classes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?translationLang=LL
    PRECONDITIONS: Notice,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *YYYY is a comma separated list of Class ID's e.g. 97 or 97, 98*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) To retrieve an information about event outcomes and silks info etc. use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYY?racingForm=outcome&translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *YYYY is an **'event id'** which is taken from the link in step 2.*
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - **'name'** on outcome level to see a greyhound name
    PRECONDITIONS: - **'runnerNumber' **to specify silk icon which will display a runner number.
    PRECONDITIONS: Silks will be hardcoded using settled pictures.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: 'Greyhounds' landing page is opened
        """
        pass

    def test_003_open_site_server___find_an_event_which_has_runnernumber_attribute_availablemake_sure_selected_event_will_appear_on_the_next_4_races_module(self):
        """
        DESCRIPTION: Open Site Server -> find an event which has 'runnerNumber' attribute available
        DESCRIPTION: Make sure selected event will appear on the 'Next 4 Races' module
        EXPECTED: Event is shown
        """
        pass

    def test_004_go_back_to_the_invictus_application(self):
        """
        DESCRIPTION: Go back to the Invictus application
        EXPECTED: 
        """
        pass

    def test_005_on_next_races_verify_specified_event(self):
        """
        DESCRIPTION: On 'Next Races' verify specified event
        EXPECTED: Event is shown n the 'Next Races' module
        """
        pass

    def test_006_verify_dog_name(self):
        """
        DESCRIPTION: Verify Dog Name
        EXPECTED: Dog name corresponds to the **'name' **attribute
        """
        pass

    def test_007_verify_runner_number_information(self):
        """
        DESCRIPTION: Verify runner number information
        EXPECTED: Based on **'runnerNumber'** attribute the necessary silk is shown (e.g. if 'runnerNumber'=1  -> silk with number '1' will be shown)
        """
        pass

    def test_008_verify_priceodds_buttons(self):
        """
        DESCRIPTION: Verify price/odds buttons
        EXPECTED: Price/odds buttons are shown next to each selection
        """
        pass

    def test_009_verify_silks_for_selections_if_runnernumber_attribute_is_not_present_on_the_site_server(self):
        """
        DESCRIPTION: Verify silks for selections if 'runnerNumber' attribute is not present on the Site Server
        EXPECTED: Only generic picture is shown instead of silk icons
        """
        pass
