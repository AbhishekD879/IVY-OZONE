from collections import OrderedDict

import voltron.environments.constants as vec
from voltron.pages.shared.components.luckydip import BetShareDialog
from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.dialogs.dialog_contents.account_closure import AccountClosedDialog
from voltron.pages.shared.dialogs.dialog_contents.account_closure_confirmation import AccountClosureConfirmation
from voltron.pages.shared.dialogs.dialog_contents.betslip_full import BetslipFull
from voltron.pages.shared.dialogs.dialog_contents.bpp_unavailable import BPPUnavailable
from voltron.pages.shared.dialogs.dialog_contents.cancel_offer import CancelOffer
from voltron.pages.shared.dialogs.dialog_contents.betslip_is_busy import BetslipIsBusy
from voltron.pages.shared.dialogs.dialog_contents.cancel_withdrawal import CancelWithdrawal
from voltron.pages.shared.dialogs.dialog_contents.cashout_unavailable import CashOutUnavailable
from voltron.pages.shared.dialogs.dialog_contents.choose_your_lucky_numbers import LottoChooseLuckyNumbers
from voltron.pages.shared.dialogs.dialog_contents.congratulations import Congratulations
from voltron.pages.shared.dialogs.dialog_contents.deposit_confirm import DepositConfirm
from voltron.pages.shared.dialogs.dialog_contents.deposit_limits import DepositLimits
from voltron.pages.shared.dialogs.dialog_contents.edit_acca_cancel import EditAccaCancelDialog
from voltron.pages.shared.dialogs.dialog_contents.edit_acca_history import EditAccaHistory
from voltron.pages.shared.dialogs.dialog_contents.error import Error
from voltron.pages.shared.dialogs.dialog_contents.every_race import RacingWatchFreeInfo
from voltron.pages.shared.dialogs.dialog_contents.free_bet_dialog import ContinueWithFreebetDialog, FreeBetNotEligible
from voltron.pages.shared.dialogs.dialog_contents.free_bet_dialog import FreebetStakeDialog
from voltron.pages.shared.dialogs.dialog_contents.freebet_token_description import FreebetTokenDescription
from voltron.pages.shared.dialogs.dialog_contents.good_news import GoodNews
from voltron.pages.shared.dialogs.dialog_contents.infomation_dialog import InfomationDialog
from voltron.pages.shared.dialogs.dialog_contents.log_out import LoggedOut
from voltron.pages.shared.dialogs.dialog_contents.login import LogIn
from voltron.pages.shared.dialogs.dialog_contents.login_message import LoginMessageDialog
from voltron.pages.shared.dialogs.dialog_contents.no_internet_connection import NoInternetConnection
from voltron.pages.shared.dialogs.dialog_contents.odds_boost_on_betslip import OddsBoostOnBetslip
from voltron.pages.shared.dialogs.dialog_contents.odds_boost_on_login import OddsBoostOnLogin
from voltron.pages.shared.dialogs.dialog_contents.player_bet import PlayerBet
from voltron.pages.shared.dialogs.dialog_contents.quick_deposit import QuickDeposit
from voltron.pages.shared.dialogs.dialog_contents.quiz_dialog import QuizDialogOnLogin
from voltron.pages.shared.dialogs.dialog_contents.redirecting import Redirecting
from voltron.pages.shared.dialogs.dialog_contents.remove_all_betslip import RemoveAllBetslip
from voltron.pages.shared.dialogs.dialog_contents.selection_information import SelectionInformation
from voltron.pages.shared.dialogs.dialog_contents.self_exclusion import AccountSelfExcluded
from voltron.pages.shared.dialogs.dialog_contents.self_exclusion import SelfExclusion
from voltron.pages.shared.dialogs.dialog_contents.signposting_promotion import SignPostingPromotion
from voltron.pages.shared.dialogs.dialog_contents.success import Success
from voltron.pages.shared.dialogs.dialog_contents.terms_and_conditions import TermsAndConditions
from voltron.pages.shared.dialogs.dialog_contents.time_out_confirmation import ConfirmationOfTimeOut
from voltron.pages.shared.dialogs.dialog_contents.upgrate_your_account import UpgradeYourAccount
from voltron.pages.shared.dialogs.dialog_contents.verification_failed import VerificationFailed
from voltron.pages.shared.dialogs.dialog_contents.verify_your_account import VerifyYourAccount
from voltron.pages.shared.dialogs.dialog_contents.warning_dialog import WarningDialog
from voltron.pages.shared.dialogs.dialog_contents.what_are_net_deposits import WhatAreNetDeposits
from voltron.pages.shared.dialogs.dialog_contents.what_is_cashout import WhatIsCashout
from voltron.pages.shared.dialogs.dialog_contents.you_are_betting import YouAreBetting
from voltron.pages.shared.dialogs.dialog_contents.watch_live import WatchLive
from voltron.utils import mixins
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import find_element
from voltron.utils.helpers import find_elements
from voltron.utils.waiters import wait_for_result


class DialogManager(mixins.LoggingMixin):
    _item = 'xpath=//*[@data-crlat="dialog"][.//modal[*]]'
    _dialog_type_item = 'xpath=.//*[contains(@data-crlat, "d.")][*]'
    _dialog_type_pattern = 'xpath=.//div[@data-crlat="dialog"]//modal'
    _dialog_type_pattern_item = 'xpath=.//*[@data-crlat="{selector}"][*]'
    _default_dialog_content_type = Dialog

    def __init__(self, *args, **kwargs):
        super(DialogManager, self).__init__()
        self.brand = kwargs.get('brand', 'bma')

    _known_dialog_content_types = {
        vec.dialogs.DIALOG_MANAGER_LOG_IN: {'type': LogIn,
                                            'selector': 'd.login'},
        vec.dialogs.DIALOG_MANAGER_LOGIN_MESSAGE: {'type': LoginMessageDialog,
                                                   'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_QUICK_DEPOSIT: {'type': QuickDeposit,
                                                   'selector': 'd.depositNotification'},
        vec.dialogs.DIALOG_MANAGER_GOOD_NEWS_EX: {'type': GoodNews,
                                                  'selector': 'd.goodNews'},
        vec.dialogs.DIALOG_MANAGER_GOOD_NEWS: {'type': DepositConfirm,
                                               'selector': 'd.depositConfirm'},
        vec.dialogs.DIALOG_MANAGER_SELF_EXCLUSION: {'type': SelfExclusion,
                                                    'selector': 'd.selfEx'},
        vec.dialogs.DIALOG_MANAGER_SELF_EXCLUSION_REQUEST: {'type': SelfExclusion,
                                                            'selector': 'd.selfEx'},
        vec.dialogs.DIALOG_MANAGER_LOGGED_OUT: {'type': LoggedOut,
                                                'selector': 'd.sessionLogout'},
        vec.dialogs.DIALOG_MANAGER_ACCOUNT_SELF_EXCLUDED: {'type': AccountSelfExcluded,
                                                           'selector': 'd.selfExLogout'},
        vec.dialogs.DIALOG_MANAGER_YOU_ARE_LOGGED_OUT: {'type': LoggedOut,
                                                        'selector': 'd.sessionLogout'},
        vec.dialogs.DIALOG_MANAGER_VERIFY_YOUR_ACCOUNT: {'type': VerifyYourAccount,
                                                         'selector': 'd.verification'},
        vec.dialogs.DIALOG_MANAGER_TERMS_AND_CONDITIONS: {'type': TermsAndConditions,
                                                          'selector': 'd.tac'},
        vec.dialogs.DIALOG_MANAGER_SUCCESS: {'type': Success,
                                             'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW: {'type': LottoChooseLuckyNumbers,
                                                                     'selector': 'd.lottoNumber'},
        vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION: {'type': FreebetTokenDescription,
                                                                 'selector': 'd.freeBet'},
        vec.dialogs.DIALOG_MANAGER_CONGRATULATIONS_EX: {'type': Congratulations,
                                                        'selector': 'd.bonus'},
        vec.dialogs.DIALOG_MANAGER_CONGRATULATIONS_EX.title(): {'type': Congratulations,
                                                                'selector': 'd.bonus'},
        vec.dialogs.DIALOG_MANAGER_BEST_ODDS_GUARANTEED: {'type': SignPostingPromotion,
                                                          'selector': 'd.promo'},
        vec.dialogs.DIALOG_MANAGER_ERROR: {'type': Error,
                                           'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_EVERY_RACE_ANGLE_DAY: {'type': RacingWatchFreeInfo,
                                                          'selector': 'd.watchFreeInfo'},
        vec.dialogs.DIALOG_MANAGER_YOU_HAVE_A_PENDING_DEPOSIT_LIMIT_INCREASE: {'type': DepositLimits,
                                                                               'selector': 'd.confirmDepositLimits'},
        vec.dialogs.DIALOG_MANAGER_BETSLIP_FULL: {'type': BetslipFull,
                                                  'selector': 'd.maxStake'},
        vec.dialogs.DIALOG_MANAGER_CANCEL_WITHDRAWAL: {'type': CancelWithdrawal,
                                                       'selector': 'd.cancelWithDraw'},
        vec.dialogs.DIALOG_MANAGER_REDIRECTING: {'type': Redirecting,
                                                 'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_CASH_OUT_SERVICE_UNAVAILABLE: {'type': CashOutUnavailable,
                                                                  'selector': 'd.bppError'},
        vec.dialogs.DIALOG_MANAGER_WHATS_CASHOUT: {'type': WhatIsCashout,
                                                   'selector': 'd.whatIsCashOut'},
        vec.dialogs.DIALOG_MANAGER_WHAT_ARE_NET_DEPOSITS: {'type': WhatAreNetDeposits,
                                                           'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_SELECTION_INFORMATION: {'type': SelectionInformation,
                                                           'selector': 'd.selInfo'},
        vec.dialogs.DIALOG_MANAGER_DOUBLE_SELECTION_INFORMATION: {'type': SelectionInformation,
                                                                  'selector': 'd.info'},
        vec.app.INTERNET_ERROR.upper(): {'type': NoInternetConnection,
                                         'selector': 'd.connectionLost'},
        vec.dialogs.DIALOG_MANAGER_UPGRADE_YOUR_ACCOUNT: {'type': UpgradeYourAccount,
                                                          'selector': 'd.upgradeAccount'},
        vec.dialogs.DIALOG_MANAGER_YOU_RE_BETTING: {'type': YouAreBetting,
                                                    'selector': 'd.betFilter'},
        vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_ON_BETSLIP: {'type': OddsBoostOnBetslip,
                                                           'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_UNAVAILABLE_ON_BETSLIP: {'type': OddsBoostOnBetslip,
                                                                       'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_MAX_STAKE_EXCEEDED: {'type': OddsBoostOnBetslip,
                                                                   'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_ODDS_BOOST: {'type': OddsBoostOnLogin,
                                                'selector': 'd.oddsBoost'},
        vec.dialogs.DIALOG_MANAGER_DOUBLE_YOUR_WINNINGS: {'type': SignPostingPromotion,
                                                          'selector': 'd.promo'},
        vec.dialogs.DIALOG_MANAGER_FALLERS_INSURANCE: {'type': SignPostingPromotion,
                                                       'selector': 'd.promo'},
        vec.dialogs.DIALOG_MANAGER_YOUR_CALL: {'type': SignPostingPromotion,
                                               'selector': 'd.promo'},
        vec.dialogs.DIALOG_MANAGER_BEATEN_BY_A_LENGTH: {'type': SignPostingPromotion,
                                                        'selector': 'd.promo'},
        vec.dialogs.DIALOG_MANAGER_EXTRA_PLACE_RACE: {'type': SignPostingPromotion,
                                                      'selector': 'd.promo'},
        vec.dialogs.DIALOG_MANAGER_CONFIRMATION_OF_ACCOUNT_CLOSURE: {'type': AccountClosureConfirmation,
                                                                     'selector': 'd.closureConfirmation'},
        vec.dialogs.DIALOG_MANAGER_YOUR_ACCOUNT_IS_NOW_CLOSED: {'type': AccountClosedDialog,
                                                                'selector': 'd.closureSuccess'},
        vec.dialogs.DIALOG_MANAGER_CONFIRMATION_OF_TIME_OUT: {'type': ConfirmationOfTimeOut,
                                                              'selector': 'd.timeOutConfirmation'},
        vec.dialogs.DIALOG_MANAGER_WARNING: {'type': WarningDialog,
                                             'selector': 'd.luckyDip'},
        vec.dialogs.DIALOG_MANAGER_BET_PLACEMENT_SERVICE_UNAVAILABLE: {'type': BPPUnavailable,
                                                                       'selector': 'd.bppError'},
        vec.dialogs.DIALOG_MANAGER_VERIFICATION_FAILED: {'type': VerificationFailed,
                                                         'selector': 'd.KYCOverlay'},
        vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER: {'type': CancelOffer,
                                                  'selector': 'd.info'},
        vec.dialogs.DIALOG_BETSLIP_IS_BUSY: {'type': BetslipIsBusy,
                                             'selector': 'd.overAskNotif'},
        vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE: {'type': FreebetStakeDialog,
                                                         'selector': 'd.freeBetSelect'},
        vec.dialogs.DIALOG_MANAGER_FREE_BETS_CONTINUE_WITH_FREE_BET: {'type': ContinueWithFreebetDialog,
                                                                      'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_SHARE: {"type": BetShareDialog,
                              "selector": 'd.betSharing'},

        vec.dialogs.DIALOG_MANAGER_REMOVE_ALL: {'type': RemoveAllBetslip,
                                                'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_EDIT_ACCA_HISTORY: {'type': EditAccaHistory,
                                                       'selector': 'd.emaH'},
        vec.dialogs.DIALOG_MANAGER_INFORMATION: {'type': InfomationDialog,
                                                 'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_QUIZ: {'type': QuizDialogOnLogin,
                                          'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_ON_BETSLIP_EXCEEDED: {'type': OddsBoostOnBetslip,
                                                                    'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_FREE_BET_NOT_ELIGIBLE: {'type': FreeBetNotEligible,
                                                           'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_BETSLIP_LIMITATION: {'type': Error, 'selector': 'None'},
        vec.odds_boost.BETSLIP_DIALOG.continue_with_freebet.upper(): {'type': ContinueWithFreebetDialog,
                                                                      'selector': 'd.info'},
        vec.odds_boost.BETSLIP_DIALOG.continue_with_freebet: {'type': ContinueWithFreebetDialog, 'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_DO_YOU_WANT_TO_CANCEL_EDITING: {'type': EditAccaCancelDialog, 'selector': 'd.info'},
        vec.dialogs.DIALOG_MANAGER_WATCH_LIVE: {'type': WatchLive,
                                                'selector': 'd.videoStreamError'},
        vec.dialogs.DIALOG_MANAGER_PLAYER_NOT_SELECTED: {'type': PlayerBet,
                                                         'selector': 'd.info'},
    }

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        dialogs_we = find_elements(selector=self._item, timeout=0)
        self._logger.debug(
            f'*** Found {len(dialogs_we)} {self.__class__.__name__} - {self._default_dialog_content_type.__name__} items')

        items_ordered_dict = OrderedDict()
        for dialog_we in dialogs_we:
            dialog = self._default_dialog_content_type(selector=self._dialog_type_item, context=dialog_we, timeout=1)
            attr = dialog.get_attribute('data-crlat')
            if (dialog.has_header(timeout=0.5) and dialog.header_object.is_displayed(
                    timeout=0.5)) or dialog.is_displayed(timeout=0.5):
                dialog_name, dialog_type = next(((dialog_name, dialog_properties.get('type'))
                                                 for (dialog_name, dialog_properties) in
                                                 self._known_dialog_content_types.items()
                                                 if dialog_properties.get('selector') == attr), (None, None))
                if not dialog_name:
                    self._logger.debug(f'*** Unknown dialog with selector: "{attr}"')
                    raise VoltronException('Unknown dialog')
                self.logger.info(
                    f'*** Recognized dialog "{dialog_name}" by attribute "{attr}" with internal type "{dialog_type.__name__}"')
                dialog_type_ = dialog_type(web_element=dialog_we)
                items_ordered_dict.update({dialog_name: dialog_type_})
                #  ms: verify dialog title?

        self._logger.debug(f'*** Found {len(items_ordered_dict)} dialogs "{items_ordered_dict.keys()}"')
        return items_ordered_dict

    def wait_for_dialog(self, dialog_name: str, verify_name: bool = True, timeout: (int, float) = 10):
        """
        Method used for checking dialog presence on UI
        :param dialog_name: actual dialog name as on UI
        :param verify_name: parameter for comparing expected dialog title with actual
        :param timeout: timeout for waiting
        :return: dialog object in case of success, None if required dialog is not found
        """
        dialog = None

        dialog_properties = self._known_dialog_content_types.get(dialog_name)
        if not dialog_properties:
            raise VoltronException(f'Dialog "{dialog_name}" is not present in known dialogs')

        selector, dialog_type = dialog_properties.get('selector'), dialog_properties.get('type'),
        if selector == 'None':
            dialog_we = wait_for_result(
                lambda: find_element(selector=self._dialog_type_pattern, timeout=0),
                name=f'Dialog "{dialog_name}" opened',
                timeout=timeout)
        else:
            dialog_we = wait_for_result(
                lambda: find_element(selector=self._dialog_type_pattern_item.format(selector=selector), timeout=0),
                name=f'Dialog "{dialog_name}" opened',
                timeout=timeout)
        if dialog_we:
            dialog = dialog_type(web_element=dialog_we)
            wait_for_result(lambda: dialog.header_object.is_displayed(timeout=0.5) or dialog.is_displayed(timeout=0.5),
                            timeout=1,
                            name=f'Dialog "{dialog_name}" to display')
            if verify_name:
                actual_dialog_name = dialog.name
                if dialog_name.lower() != actual_dialog_name.lower():
                    raise VoltronException(f'Actual Dialog name "{actual_dialog_name}" != Expected "{dialog_name}"')
        return dialog

    def perform_dialog_default_action(self, ignored_dialogs: (list, tuple, str) = ()):
        ignored_dialogs = ignored_dialogs if isinstance(ignored_dialogs, (list, tuple)) else (ignored_dialogs,)
        dialogs = self.items_as_ordered_dict
        for dialog_name, dialog_component in dialogs.items():
            self._logger.info(f'*** Found dialog "{dialog_name}"')
            if dialog_name in ignored_dialogs:
                self._logger.warning(
                    f'*** Skipped closing "{dialog_name}" dialog as it is in ignored dialogs list "{ignored_dialogs}"')
                continue
            try:
                dialog_component.default_action(dialog_name=dialog_name)
            except Exception as e:
                message = f'Exception for dialog "{dialog_name}": {str(e)}'
                if 'stale element reference' in message:
                    self.logger.warning(message)
                else:
                    raise VoltronException(message=message)
