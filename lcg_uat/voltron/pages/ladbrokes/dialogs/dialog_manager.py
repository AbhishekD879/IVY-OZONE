import voltron.environments.constants as vec
from voltron.pages.ladbrokes.dialogs.dialog_contents.country_restriction import CountryRestriction
from voltron.pages.ladbrokes.dialogs.dialog_contents.email_opt_in import EmailOptIn
from voltron.pages.ladbrokes.dialogs.dialog_contents.fanzone_games import FanzoneGames
from voltron.pages.ladbrokes.dialogs.dialog_contents.syc import SYC
from voltron.pages.ladbrokes.dialogs.dialog_contents.five_a_side import FiveASide
from voltron.pages.ladbrokes.dialogs.dialog_contents.i_dont_support_any_team import IDontSupportAnyTeam
from voltron.pages.ladbrokes.dialogs.dialog_contents.team_Confirmation import TeamConfirmation
from voltron.pages.ladbrokes.dialogs.dialog_contents.thank_you import ThankYou
from voltron.pages.ladbrokes.dialogs.dialog_contents.team_alerts import TeamAlerts
from voltron.pages.ladbrokes.dialogs.dialog_contents.unsubscribe_fanzone import UnsubscribeFanzone
from voltron.pages.ladbrokes.dialogs.dialog_contents.your_betting import YourBetting
from voltron.pages.ladbrokes.dialogs.dialog_contents.remove_player import RemovePlayer
from voltron.pages.ladbrokes.dialogs.dialog_contents.watch_live_dialog import WatchLiveDialog
from voltron.pages.ladbrokes.dialogs.dialog_contents.extra_place_race import ExtraPlaceDialog
from voltron.pages.ladbrokes.dialogs.dialog_contents.acca_insurance_offer import LadbrokesAccaInsuranceOfferDialog
from voltron.pages.shared.dialogs.dialog_manager import DialogManager
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import find_element
from voltron.utils.waiters import wait_for_result
from voltron.pages.ladbrokes.dialogs.dialog_contents.free_ride import FreeRideDialog
from voltron.pages.ladbrokes.dialogs.dialog_contents.change_team import ChangeTeam


class DialogManagerLadbrokes(DialogManager):
    _ladbrokes_dialogs_type = {
        vec.bma.COUNTRY_RESTRICTION.header: {'type': CountryRestriction,
                                             'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_EXTRA_PLACE: {'type': ExtraPlaceDialog,
                                                 'selector': 'd.promo'},
        vec.dialogs.DIALOG_MANAGER_WATCH_LIVE: {'type': WatchLiveDialog,
                                                'selector': 'd.videoStreamError'},
        vec.betslip.ACCA_INSURANCE_TITLE: {'type': LadbrokesAccaInsuranceOfferDialog,
                                           'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_REMOVE_PLAYER: {'type': RemovePlayer,
                                                   'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_FIVE_A_SIDE: {'type': FiveASide,
                                                 'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_YOUR_BETTING: {'type': YourBetting,
                                                  'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_5ASIDE_PLAYER_NOT_SELECTED: {'type': FiveASide,
                                                                'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_FREE_RIDE: {'type': FreeRideDialog,
                                               'selector': 'None'},
        vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS: {'type': SYC,
                                                         'selector': 'None'},
        vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION: {'type': TeamConfirmation,
                                                       'selector': 'None'},
        vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS: {'type': TeamAlerts,
                                                 'selector': 'None'},
        vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS: {'type': IDontSupportAnyTeam,
                                                                     'selector': 'None'},

        vec.dialogs.DIALOG_MANAGER_UNSUBSCRIBE_FROM_FANZONE: {'type': UnsubscribeFanzone,
                                                              'selector': 'None'},

        vec.dialogs.DIALOG_MANAGER_THANK_YOU: {'type': ThankYou,
                                               'selector': 'None'},
        vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM: {'type': ChangeTeam,
                                                 'selector': 'None'},
        vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN: {'type':EmailOptIn,
                                                'selector': 'None'},
        vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES: {'type':FanzoneGames,
                                                   'selector': 'None'},
    }

    @property
    def _all_dialog_content_types(self):
        self._known_dialog_content_types.update(self._ladbrokes_dialogs_type)
        return self._known_dialog_content_types

    def wait_for_dialog(self, dialog_name, verify_name=True, timeout=10):
        """
        Method used for checking dialog presence on UI
        :param dialog_name: actual dialog name as on UI
        :param verify_name: parameter for comparing expected dialog title with actual
        :param timeout: timeout for waiting
        :return: dialog object in case of success, None if required dialog is not found
        """
        dialog = None
        dialog_properties = self._all_dialog_content_types.get(dialog_name)
        if not dialog_properties:
            raise VoltronException(f'Dialog "{dialog_name}" is not present in known dialogs')
        selector, dialog_type = dialog_properties.get('selector'), dialog_properties.get('type'),
        if selector == 'None':
            dialog_we = wait_for_result(
                lambda: find_element(selector=self._dialog_type_pattern, timeout=0),
                name=f'Dialog "{dialog_name}" opened',
                timeout=timeout)
        else:
            selector_ = self._dialog_type_pattern_item.format(selector=selector) if 'd.' in selector else selector
            dialog_we = wait_for_result(lambda: find_element(selector=selector_, timeout=0),
                                        name=f'Dialog "{dialog_name}" opened',
                                        timeout=timeout)
        if dialog_we:
            dialog = dialog_type(web_element=dialog_we)
            wait_for_result(lambda: dialog.header_object.is_displayed(timeout=0.5) or dialog.is_displayed(timeout=0.5),
                            timeout=1,
                            name=f'Dialog "{dialog_name}" to display')
            if verify_name:
                dialog_name = dialog_name.replace('lad', "")
                actual_dialog_name = dialog.name
                if dialog_name != actual_dialog_name:
                    raise VoltronException(f'Actual Dialog name "{actual_dialog_name}" != Expected "{dialog_name}"')
        return dialog
