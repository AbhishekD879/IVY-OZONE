import { from as observableFrom, Observable, Subscription, of as observableOf, lastValueFrom } from 'rxjs';
import { catchError, map, switchMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';
import {
  IBetDetail,
  IBetDetailLeg,
  IBetDetailLegPart,
  IBetsResponse
} from '@app/bpp/services/bppProviders/bpp-providers.model';
import { AddToBetslipByOutcomeIdService } from '@betslip/services/addToBetslip/add-to-betslip-by-outcome-id.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { SiteServerService } from '@app/core/services/siteServer/site-server.service';
import { BetDetailUtils } from '@app/bpp/services/bppProviders/bet-detail.utils';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { CommandService } from '@core/services/communication/command/command.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { DeviceService } from '@core/services/device/device.service';
import { IBetslipSelection } from '@app/quickbet/models/quickbet-common.model';
import { IGtmEventModel } from '@root/app/quickbet/models/quickbet-gtm-event.model';

interface IMessage {
  type?: string;
  msg?: string;
}

@Injectable({ providedIn: BetslipApiModule })
export class BetReuseService {
  ids: string[];
  message: IMessage = {
    type: undefined,
    msg: undefined
  };
  maxPayOutFlag: boolean = false;
  betReceipt: boolean = false;
  horseRacingReceiptCheck: boolean = true;
  placeBetResponse: IBetsResponse;
  placeBetSub: Subscription;
  location:string = "";
  private receipts: IBetDetail[];
  private isBetCanceled: (stake: IBetDetail) => boolean = BetDetailUtils.isCanceled;
  private SIMPLE_SELECTION_TYPE: string = 'simple';

  constructor(
    private siteServerService: SiteServerService,
    private pubSubService: PubSubService,
    private addToBetslipService: AddToBetslipByOutcomeIdService,
    private gtmTrackingService: GtmTrackingService,
    protected gtmService: GtmService,
    private command: CommandService,
    private device: DeviceService,
    private infoDialogService: InfoDialogService
  ) {
    this.pubSubService.subscribe('reUseBet', this.pubSubService.API.REUSE_LOCATION, (name: string) => {
      this.location = name;
    });
  }

  /**
   * Reuse outcome and build the same betslip.
   * @params {number[]} outcomesIdsList
   * @return {Promise<boolean | void>} - promise
   */
  async reuse(outcomesIdsList: string[], receiptBets, location: string): Promise < boolean | void | string[] | unknown > {
    if(location) {
      this.location = location
    }
    const outcomesIds = outcomesIdsList;
    let events: ISportEvent[];
    let selections$: Observable < boolean | void | string[] | unknown > ;

    if (outcomesIds.length > 0) {

      selections$ = observableFrom(this.siteServerService.getEventsByOutcomeIds({
        outcomesIds
      })).pipe(
        map((eventsData: ISportEvent[]) => {
          events = eventsData;
          return this.sortByOutcomeIds(outcomesIds, eventsData)
        }),
        switchMap(() => {
          this.removeSuspendedBetReceipts(outcomesIds, receiptBets);
          this.mergeEventsWithReceipts(events, receiptBets);
          this.markForeCastTricastReceipts(receiptBets);
          this.removeLegsWithNoEventInfo(receiptBets);
          this.receipts = receiptBets;
          return this.addToBetslipService.reuseSelections(outcomesIds, this.receipts, this.location, false);
        }),
        map(() => {
          this.gtmTrackingService.restoreGtmTracking(outcomesIds);
          return outcomesIds;
        }),
        map(() => {
          // this.pubSubService.publish(this.pubSubService.API.HOME_BETSLIP);
          return outcomesIds;
        }),
        catchError(err => {
          console.warn('Error while getEventsByOutcomeIds (BetReuseService.getEventsByOutcomeIds)', err);
          // this.pubSubService.publish(this.pubSubService.API.HOME_BETSLIP);
          return observableOf(null);
        }));
    } else {
      // this.pubSubService.publish(this.pubSubService.API.HOME_BETSLIP);
      selections$ = observableOf(true);
    }
    this.pubSubService.publish(this.pubSubService.API.REUSE_OUTCOME);
    this.message = {
      type: undefined,
      msg: undefined
    };
    return await lastValueFrom(selections$);
  }

  /**
   * Merges leg data with event data
   * @param events data which contains all outcome id details
   * @param receiptBets contains bet receipt data
   */
  private mergeEventsWithReceipts(events: ISportEvent[], receiptBets: IBetDetail[]): void {
    receiptBets.forEach((receipt: IBetDetail): void => {
        events.forEach((event: ISportEvent): void => {
          receipt.leg.forEach((leg: IBetDetailLeg): void => {
            leg.part.forEach((part: IBetDetailLegPart): void => {
              if (Number(part.eventId) === Number(event.id)) {
                part.event = event;
              }
            });
          });
        });
    });
  }

  /**
   * Filters suspended bet legs
   * @param outcomesIds all possible outcome ID's
   * @param receiptBets bet receipt details
   */
  private removeSuspendedBetReceipts(outcomesIds: string[], receiptBets: IBetDetail[]): void {
    receiptBets.forEach(eachBet => {
      eachBet.leg = eachBet.leg.filter((eachLeg) => (outcomesIds.includes(eachLeg.part[0].outcomeId)))
    })
  }

  /**
   * Filters bet legs with no events
   * @param outcomesIds all possible outcome ID's
   * @param receiptBets bet receipt details
   */
  private removeLegsWithNoEventInfo(receiptBets: IBetDetail[]): void {
    receiptBets.forEach(eachBet => {
      eachBet.leg = eachBet.leg.filter((eachLeg) => (eachLeg.part[0].event !== undefined))
    })
  }

  /**
   * Puts outcomes in order by they ids, same as in outcomesIds.
   *
   * @param outcomesIds
   * @returns {Function}
   */
  private sortByOutcomeIds(outcomesIds: string[], data: ISportEvent[]): ISportEvent[] {
    data.forEach(event => {
      event.markets.forEach(market => {
        market.outcomes.sort((a: IOutcome, b: IOutcome): number => {
          const aIndex = outcomesIds.indexOf(a.id),
            bIndex = outcomesIds.indexOf(b.id);

          if (aIndex !== -1 && bIndex !== -1) {
            if (aIndex < bIndex) {
              return -1;
            } else if (aIndex > bIndex) {
              return 1;
            }
          }

          return 0;
        })
      });
    });

    return data;
  }

  private markForeCastTricastReceipts(receiptBets: IBetDetail[]): void {
    receiptBets.forEach((receipt: IBetDetail) => {
      receipt.isFCTC = /^(SF|RF|CF|TC|CT)$/.test(receipt.leg[0].legSort.code);
      if(receipt.isFCTC) {
        receipt.type = receipt.sortType;
        receipt.leg.forEach(leg => leg.legSort = leg.legSort.code)
        // receipt.leg.map(leg => leg.part.map(part => part.display leg.legSort?.code? leg.legSort.code : leg.legSort)
      }
    });
  }

  /**
   * to reuse selections in quickbet
   */
  reuseQuickBet(selection: IQuickbetSelectionModel): void {
    if (this.device.isOnline()) {
      const shouldAddToBetslip = !!selection && selection.disabled === false;

      selection.stake = 0;
      selection.stakeAmount = 0;

      if (shouldAddToBetslip) {
        const selectionState = this.formBetslipSelection(selection);
        this.command.executeAsync(this.command.API.SYNC_TO_BETSLIP, [selectionState]);
        this.trackAddBetToQB(selection, true);
      }
    } else {
      this.infoDialogService.openConnectionLostPopup();
    }
  }

  /**
   * Formats selection data in needed for betslip format.
   * @return {Object}
   */
  private formBetslipSelection(selectionData: IQuickbetSelectionModel): IBetslipSelection {
    const price = selectionData.isLP && !selectionData.hasSP ? Object.assign({
        priceType: 'LP'
      }, selectionData.price) : { priceType: 'SP' };
    const outcomeIds = selectionData.requestData.hasOwnProperty('outcomeIds')
        ? selectionData.requestData.outcomeIds : [];

    let GTMObject = null,
        isOutright,
        isSpecial;
    const tracking = this.gtmTrackingService.getTracking();

    if (tracking) {
      tracking.location = 'quick bet receipt';
      tracking.betType = 'reuse';
      GTMObject = {
        tracking
      };
    }

    const eventId = Number(selectionData.eventId);

    const betSlipSelection = {
      outcomeId: outcomeIds,
      userEachWay: selectionData.isEachWay,
      userStake: selectionData.stake,
      type: this.getSelectionType(selectionData.selectionType),
      price,
      isVirtual: this.isVirtualSport(selectionData.categoryName),
      eventId,
      isOutright,
      isSpecial,
      GTMObject
    };
    const gtmObj = {GTMObject: GTMObject, outcomeId: outcomeIds};
    this.gtmService.setSBTrackingData(gtmObj);
    return betSlipSelection;
  }

  /**
   * Check if it is virtual sport
   * @param categoryName
   */
  private isVirtualSport(categoryName: string): boolean {
    return categoryName === 'Virtual Sports';
  }

  /**
   * Determines selection type parameter needed for add selection request.
   * @param {string} type
   * @return {string}
   */
  private getSelectionType(type: string | number): string {
    return typeof type === 'string' ? type.toLowerCase() : this.SIMPLE_SELECTION_TYPE;
  }


  /**
   * Tracks selection add to betslip.
   * @param {Object} eventData
   * @param {boolean} toBetslip
   */
  private trackAddBetToQB(eventData: IQuickbetSelectionModel, toBetslip?: boolean): void {
    // get stream status during adding selection to BS
    this.command.executeAsync(this.command.API.GET_LIVE_STREAM_STATUS, undefined, false)
      .then((streamData: { streamID: string, streamActive: boolean; } | null) => {
        const gtmObj = {
          eventAction: 'reuse selection',
          eventLabel: 'success',
        };

        Object.assign(gtmObj, {
          ecommerce: {
            add: {
              products: [{
                name: eventData.eventName,
                category: String(eventData.categoryId),
                variant: String(eventData.typeId),
                brand: eventData.marketName,
                metric1: Number(eventData.freebetValue),
                dimension60: String(eventData.eventId),
                dimension61: eventData.outcomeId,
                dimension62: eventData.isStarted ? 1 : 0,
                dimension63: eventData.isYourCallBet ? 1 : 0,
                dimension64: 'quick bet receipt',
                dimension166: 'reuse',
                dimension65: '',
                dimension86: eventData.isBoostActive ? 1 : 0,
                dimension87: streamData && streamData.streamActive ? 1 : 0,
                dimension88: streamData && streamData.streamID || null
              }]
            }
          }
        });
        this.sendEventToGTM(gtmObj);
      });
  }

  /**
   * Send event to GTM
   * @param event {object}
   */
  private sendEventToGTM(event: IGtmEventModel): void {
    this.gtmService.push('trackEvent', Object.assign({}, {
      event: 'trackEvent',
      eventCategory: 'quickbet'
    }, event));
  }

}
