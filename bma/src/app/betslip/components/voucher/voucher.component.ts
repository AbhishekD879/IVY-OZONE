import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { FreebetTriggerService } from '../../services/freebetTrigger/freebet-trigger.service';
import { IVoucher } from './voucher.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { SPORT_VOUCHER_FORM } from './voucher.constant';
import { ITypedMessage } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { VanillaAuthService } from '@vanillaInitModule/services/vanillaAuth/vanilla-auth.service';

@Component({
  selector: 'voucher',
  templateUrl: './voucher.component.html'
})
export class VoucherComponent extends AbstractOutletComponent implements OnInit {
  sportVoucherForm: Partial<IVoucher> = SPORT_VOUCHER_FORM;
  sportVoucher: boolean;
  voucherPlaceholder: string;

  constructor(
    private freebetTriggerService: FreebetTriggerService,
    private localeService: LocaleService,
    private router: Router,
    private auth: VanillaAuthService
  ) {
    super();
  }

  ngOnInit(): void {
    if (this.auth.isLoggedIn()) {
      this.sportVoucherForm = JSON.parse(JSON.stringify(SPORT_VOUCHER_FORM));
      this.sportVoucher = true;
      this.voucherPlaceholder = this.localeService.getString('bs.voucherFormplaceHolder');
      this.hideSpinner();
    } else {
      this.router.navigate(['/']);
    }
  }

  submitVoucherForm(event: Event): void {
    event.preventDefault();
    // Disable form after submit.
    this.sportVoucherForm.isSent = !this.sportVoucherForm.isSent;
    this.sportVoucherForm.sportMessage = {
      type: '',
      msg: ''
    };

    this.freebetTriggerService.getVoucherCode(this.sportVoucherForm.value)
      .subscribe(
        (data: ITypedMessage) => {
          this.sportVoucherForm.isSent = false;
          this.sportVoucherForm.sportMessage = data;
        },
        (data: ITypedMessage) => {
          this.sportVoucherForm.value = '';
          this.sportVoucherForm.isSent = false;
          this.sportVoucherForm.sportMessage = data;
        });
  }

  openPromotions(event: Event): void {
    event.preventDefault();
    this.router.navigate(['/promotions']);
  }

  checkIsDisabled(voucher: Partial<IVoucher>): boolean {
    const regexpPattern: RegExp = new RegExp(voucher.pattern, 'g');
    const isValid: boolean = regexpPattern.test(voucher.value);

    return !voucher.value || !isValid || !!voucher.isSent;
  }
}
