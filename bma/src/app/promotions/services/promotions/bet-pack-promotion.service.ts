import { Injectable } from '@angular/core';
import { of, Observable, throwError } from 'rxjs';
import { mergeMap, catchError } from 'rxjs/operators';
import * as _ from 'underscore';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { DeviceService } from '@core/services/device/device.service';
import { LocaleService } from '@coreModule/services/locale/locale.service';
import { IBetPackTriggerResponse } from '@bpp/services/bppProviders/bpp-providers.model';
import { ITypedMessage } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { BETPACK_ERROR_STATUSES } from '@betslipModule/constants/betpack-error-statuses.constant';
import { GtmService } from '@core/services/gtm/gtm.service';

@Injectable()
export class BetPackPromotionService {

  constructor(
    protected bppService: BppService,
    protected device: DeviceService,
    protected localeService: LocaleService,
    private gtmService: GtmService,
  ) { }

  /**
     * buy Betpack Return promise with well formatted response
     * message.
     *
     * @param {string} triggerId - 24 symbols code.
     * @param {string} betValue
     * @returns {object}
     */
  onBuyBetPack(triggerId: string = '', betValue: string = ''): Observable<ITypedMessage> {
    return this.bppService.send('betPackTrigger', {
      value: betValue.replace(/-/g, '').trim(),
      extTriggerId: triggerId,
      source: this.device.channel.channelRef.id
    }).pipe(
      catchError(() => throwError({ type: 'error', msg: this.localeService.getString('bs.SERVICE_ERROR')})),
      mergeMap((response: any): Observable<ITypedMessage> =>
        response.error && _.contains(BETPACK_ERROR_STATUSES, response.error)
          ? throwError({ type: 'error', msg: response.error})
          : of(this.successBetPackResponse(response.response, triggerId))));
  }

  /**
     * GA for tracking betpack
     * @param eventAction
     * @param eventLabel
     * @param promotionId
     * @param errormsg
     */
  sendGTM(eventAction: string, eventLabel: string, promotionId: string, errormsg?: string, errorCode?: string): void {
    const gtmData = {
      event: 'trackEvent',
      eventAction: eventAction,
      eventCategory: 'bet pack',
      eventLabel: eventLabel,
      promoType: `Bet Pack – ${promotionId}`
    };
    if (errorCode) {
      Object.assign(gtmData, { errorCode: errorCode });
    }
    if (errormsg) {
      Object.assign(gtmData, { errorMessage: errormsg });
    }
    this.gtmService.push('trackEvent', gtmData);
  }

  /**
   * Success betpack callback function.
   * Prepering a success message object.
   *
   * @param response
   * @param code
   * @returns ITypedMessage
   */
  private successBetPackResponse(response: IBetPackTriggerResponse, code: string): ITypedMessage {
    return response && response.returnStatus && response.returnStatus.message && response.returnStatus.message === 'success'
      ? { type: 'success', msg: this.localeService.getString('bs.VOUCHER_SUCCESS', [code]) }
      : <ITypedMessage>{};
  }
}
