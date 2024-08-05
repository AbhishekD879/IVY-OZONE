import { of as observableOf, throwError, Observable } from 'rxjs';

import { mergeMap, catchError } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';

import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { LocaleService } from '@coreModule/services/locale/locale.service';
import { DeviceService } from '@coreModule/services/device/device.service';

import { FREEBET_ERROR_STATUSES } from '@betslipModule/constants/freebet-error-statuses.constant';
import {
  IFreebetTriggerResponse,
  IResponseTransFreebetTrigger,
  ITypedMessage
} from '@app/bpp/services/bppProviders/bpp-providers.model';

@Injectable({ providedIn: BetslipApiModule })
export class FreebetTriggerService {
  constructor(
    protected bppService: BppService,
    private deviceService: DeviceService,
    private localeService: LocaleService,
  ) {}

  /**
   * Checking voucher code. Return promise with well formatted response
   * message.
   *
   * @param {string} code - 24 symbols code.
   * @returns {*}
   */
  getVoucherCode(code: string = ''): Observable<ITypedMessage> {
    return this.bppService.send('freebetTrigger', {
      value: code.replace(/-/g, ''),
      source: this.deviceService.channel.channelRef.id
    }).pipe(
      catchError(() => throwError({ type: 'error', msg: this.localeService.getString('bs.SERVICE_ERROR') })),
      mergeMap((response: IResponseTransFreebetTrigger): Observable<ITypedMessage> =>
        response.error && _.contains(FREEBET_ERROR_STATUSES, response.error)
          ? throwError({ type: 'error', msg: this.localeService.getString(`bs.${response.error}`) })
          : observableOf(this.successVoucherResponse(response.response, code))));
  }

  /**
   * Success sportsbook voucher callback function.
   * Prepering a success message object.
   *
   * @param response
   * @param code
   * @returns ITypedMessage
   */
  private successVoucherResponse(response: IFreebetTriggerResponse, code: string): ITypedMessage {
    return response && response.returnStatus && response.returnStatus.message && response.returnStatus.message === 'success'
      ? { type: 'success', msg: this.localeService.getString('bs.VOUCHER_SUCCESS', [code]) }
      : <ITypedMessage>{};
  }
}
