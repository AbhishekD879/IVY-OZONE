from voltron.pages.shared.components.amount_form import AmountForm
from voltron.pages.shared.components.base import ComponentBase


class BetSlipStakeAmountForm(AmountForm):

    @property
    def label(self):
        label = ComponentBase(selector=self._amount, context=self._we, timeout=2)
        return label.get_attribute('placeholder')
