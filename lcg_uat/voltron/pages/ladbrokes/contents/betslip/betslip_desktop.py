from voltron.pages.ladbrokes.contents.betslip.betslip import BetSlipLadbrokes, LottoBetSlipLadbrokes
from voltron.pages.shared.contents.betslip.betslip_desktop import BetSlipDesktop, LottoBetSlipDesktop


class BetSlipDesktopLadbrokes(BetSlipLadbrokes, BetSlipDesktop):

    @property
    def header(self):
        return super().header

    @property
    def close_button(self):
        return super().close_button


class LottoBetSlipDesktopLadbrokes(LottoBetSlipLadbrokes, LottoBetSlipDesktop):
    pass
