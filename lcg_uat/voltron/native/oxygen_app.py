from voltron.native.fast_login_pop_up import FastLoginPopUp, FastLoginConfirmedPopUp, AutoLoginPopUp, FailedLoginDialog, \
    CoralNotificationDialog
from voltron.pages.coral.mobile_site import MobileSite
from voltron.pages.shared import get_driver


class OxygenApp(object):
    @property
    def web_content(self):
        webcontext = get_driver().contexts[1]
        get_driver().switch_to.context(webcontext)
        return MobileSite()

    @property
    def fast_login_pop_up(self):
        return FastLoginPopUp()

    @property
    def fast_login_confirmed_pop_up(self):
        return FastLoginConfirmedPopUp()

    @property
    def auto_login_pop_up(self):
        return AutoLoginPopUp()

    @property
    def failed_login_dialog(self):
        return FailedLoginDialog()

    @property
    def coral_notification_dialog(self):
        return CoralNotificationDialog()
