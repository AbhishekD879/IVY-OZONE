import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C883690_CMS_Verify_displaying_outright_selections(Common):
    """
    TR_ID: C883690
    NAME: CMS: Verify displaying outright selections
    DESCRIPTION: This test case verifies CMS control of Outrights in Featured Tab accoring to Story BMA-22719.
    PRECONDITIONS: Following configurations are in scope for the below test steps:
    PRECONDITIONS: - Android Native web and Chrome;
    PRECONDITIONS: - Android Coral App (wrapper);
    PRECONDITIONS: - iOS Safari;
    PRECONDITIONS: - iOS Coral App for iPad and iPhone.
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/structure
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: NOTE: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_cms_for_the_environment_in_test(self):
        """
        DESCRIPTION: Load CMS for the environment in test
        EXPECTED: CMS is opened.
        """
        pass

    def test_002_tap_on_featured_tab_modules(self):
        """
        DESCRIPTION: Tap on Featured Tab Modules
        EXPECTED: Featured Tab modules is opened.
        """
        pass

    def test_003_create_new_featured_tab_module_with_valid_input_including_the_following_requirements__max_events_displayed___show_all__max_selections_to_display__3__expanded_by_default__true__select_event_by_enhanced_multiple__id_existing_outright_of_a_sport_eg_football_with_more_than_3_selections(self):
        """
        DESCRIPTION: Create new Featured Tab Module with valid input including the following requirements:
        DESCRIPTION: - Max events displayed =  Show all
        DESCRIPTION: - Max selections to Display = 3
        DESCRIPTION: - Expanded by default = True
        DESCRIPTION: - Select Event by "Enhanced Multiple" = ID (existing Outright of a sport e.g Football with more than 3 selections)
        EXPECTED: Featured Tab module is saved.
        """
        pass

    def test_004_verify_the_featured_tab_module_in_front_end_for_the_environment_in_test(self):
        """
        DESCRIPTION: Verify the Featured Tab Module in Front end for the environment in test.
        EXPECTED: New Outright event is displayed in Featured Tab Module according to specification.
        EXPECTED: - The Outright is expanded by Dedault;
        EXPECTED: - Selection names are correctly displayed inline with the odds;
        EXPECTED: - Link is present displaying the total number of selections for the outright; (+ no selections)
        EXPECTED: - Section title should inherit the type id name (Tournament name)
        """
        pass

    def test_005_tap_on_the_link_displayed_under_the_outright_selections_plus_no_selections(self):
        """
        DESCRIPTION: Tap on the Link displayed under the Outright selections (+ no selections)
        EXPECTED: User is being redirected to the Outright event page where all selections are displayed.
        """
        pass

    def test_006_create_new_featured_tab_module_with_valid_input_including_the_following_requirements__max_events_displayed___show_all__max_selections_to_display__show_all__expanded_by_default__false__select_event_by_type__id_existing_outrights_of_a_sport_eg_football_or_tennis(self):
        """
        DESCRIPTION: Create new Featured Tab Module with valid input including the following requirements:
        DESCRIPTION: - Max events displayed =  Show all
        DESCRIPTION: - Max selections to Display = Show all
        DESCRIPTION: - Expanded by default = False
        DESCRIPTION: - Select Event by Type = ID (existing Outrights of a sport e.g Football or Tennis)
        EXPECTED: Featured Tab module is saved.
        """
        pass

    def test_007_verify_the_featured_tab_module_in_front_end_for_the_environment_in_test(self):
        """
        DESCRIPTION: Verify the Featured Tab Module in Front end for the environment in test.
        EXPECTED: New Outright event is displayed in Featured Tab Module according to specification.
        EXPECTED: - The Outright is NOT expanded;
        EXPECTED: - Selection names are correctly displayed inline with the odds;
        EXPECTED: - Link is present even if all selections are already displayed; (See all selection)
        EXPECTED: - Section title should inherit the type id name (Tournament name)
        """
        pass

    def test_008_tap_on_the_link_displayed_under_the_outright_selections_see_all_selections(self):
        """
        DESCRIPTION: Tap on the Link displayed under the Outright selections (See all selections)
        EXPECTED: User is being redirected to the Outright event page where all selections are displayed.
        """
        pass

    def test_009_create_new_featured_tab_modules_with_valid_inputs_in_order_to_display_outright_for_multiple_sports(self):
        """
        DESCRIPTION: Create new Featured Tab Modules with valid inputs in order to display "Outright" for multiple Sports.
        EXPECTED: Featured Tab modules are saved.
        """
        pass

    def test_010_verify_the_featured_tab_module_in_front_end_for_the_environment_in_test(self):
        """
        DESCRIPTION: Verify the Featured Tab Module in Front end for the environment in test.
        EXPECTED: Outright are being correctly displayed in Front End.
        EXPECTED: - Only one instance of Outright is being displayed in the featured Tab;
        EXPECTED: - Each Sport Outright section title inherits the type id name (Tournament name)
        """
        pass

    def test_011_access_the_cms_and_schedule_some_of_the_outright_to_be_visible_a_certain_time(self):
        """
        DESCRIPTION: Access the CMS and schedule some of the Outright to be visible a certain time.
        EXPECTED: Featured Tab modules are saved.
        """
        pass

    def test_012_verify_the_outright_in_the_featured_tab_module_from_front_end_after_the_set_time(self):
        """
        DESCRIPTION: Verify the Outright in the Featured Tab Module from Front end after the set time.
        EXPECTED: Outright is no longer visible.
        """
        pass
