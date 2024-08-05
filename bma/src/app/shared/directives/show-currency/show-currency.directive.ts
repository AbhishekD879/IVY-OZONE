import { Directive, Input, OnChanges, SimpleChanges, HostBinding } from '@angular/core';
import { IShowCurrency } from '@sharedModule/models/show-currency.model';

/**
 * Directive used to show currency & value centred in the input field
 * Expl: [showCurrency]="{ currency: 'AUD', value: 12, limit: 8 }"
 * If more then limit symbols are in input, hide currency to let input has more visible digits
 * exp: for AUD 12345, Kr 123.56, $ 1234567 limit = 8
 * First usage for tote-stake input in betslip
 */
@Directive({
  // eslint-disable-next-line
  selector: '[showCurrency]'
})
export class ShowCurrencyDirective implements OnChanges {
  @Input() showCurrency: IShowCurrency;

  @HostBinding('class.show-currency') isShowCurrency: boolean = false;

  ngOnChanges(changes: SimpleChanges): void {
    this.isShowCurrency = !!changes.showCurrency && !!this.showCurrency.currency &&
      !!this.showCurrency.value && !this.isCurrencyValueOverflow();
  }

  private isCurrencyValueOverflow(): boolean {
    return this.showCurrency.currency.length + this.showCurrency.value.toString().length > this.showCurrency.limit;
  }
}
