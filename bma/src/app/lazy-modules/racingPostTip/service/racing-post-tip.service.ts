// import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
// import environment from '@environment/oxygenEnvConfig';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { ISportEvent, IEventMostTipData, IHorse } from '@core/models/sport-event.model';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { horseracingConfig } from '@core/services/racing/config/horseracing.config';
import { IHorseOutcome } from '@core/models/outcome.model';
// import { UserService } from '@app/core/services/user/user.service';
import { IGtmOrigin } from '@app/core/services/gtmTracking/models/gtm-origin.model';

@Injectable({
  providedIn: 'root'
})
export class RacingPostTipService {

  _racingPostGTM: IGtmOrigin;
  raceData: Array<ISportEvent>;
  // private UPCELL_ENDPOINT: string;
  private categoryId= horseracingConfig.config.request.categoryId;
  private filteredEvents: ISportEvent[];
  private mostTippedHorseEvents: IEventMostTipData[] = [];

  constructor(
    // private http: HttpClient,
    // private userService: UserService,
  private pubSubService: PubSubService) {
    // this.UPCELL_ENDPOINT = environment.UPCELL_ENDPOINT;
  }

  set racingPostGTM(value) {
    this._racingPostGTM = value;
  }

  get racingPostGTM() {
    return this._racingPostGTM;
  }

  updateRaceData(data: ISportEvent[]) {
    this.raceData = data;
  }

  /**
   * user place bet with in next 15min race that need to be removed from mainbet
   * @param recent - recent tip races
   */
  getMostTipThroughMainBet(events: IEventMostTipData[],
    receipts: IBetDetail[],
    showReceipt: boolean,
    mainBetReceipt: boolean): IEventMostTipData[] {
      receipts && receipts.length && receipts.forEach(receipt => {
      if (receipt.leg[0].part[0].event.categoryId.toString() === this.categoryId.toString()) {
        this.setFilteredRaceEvents(events, receipt.leg[0].part[0].event.id, showReceipt, mainBetReceipt);
      }
    });
    return this.mostTippedHorseEvents;
  }

  /**
   * user place bet with in next 15min race that need to be removed from quickbet
   * @param recent - recent tip races
   */
  getMostTipThroughQuickBet(events: ISportEvent[],
    receipt: IQuickbetSelectionModel,
    showReceipt: boolean,
    quickBetReceipt: boolean): IEventMostTipData[] {
    if ( receipt && receipt.categoryId === this.categoryId) {
      this.setFilteredRaceEvents(events, Number(receipt.eventId), showReceipt, quickBetReceipt);
    }
    return this.mostTippedHorseEvents;
  }
  /**
   * racingpost Details by upcell
   * @returns {Observable<IRacingPostHRResponse>}
   */

  private setFilteredRaceEvents(events: IEventMostTipData[], id: number,showReceipt: boolean, isReciptPresent: boolean): void {
    this.filteredEvents = events.filter((race: IEventMostTipData) => Number(id) !== Number(race.id));
    const isHorsesEmpty = this.filteredEvents.filter((raceEvent) => raceEvent['horses'] && raceEvent['horses'].length);
    if (isHorsesEmpty && isHorsesEmpty.length && showReceipt && isReciptPresent) {
      this.filteredEvents.forEach((race:IEventMostTipData) => {
        this.getOutComeAndTip(race);
      });
    } else {
      this.pubSubService.publish(this.pubSubService.API.IS_TIP_PRESENT, {
        isTipPresent: false,
        raceData: this.raceData
      });
    }
  }

  /**
   * find most power horse from horses
   * @param race - recent tip races
   */
  private getOutComeAndTip(raceEvent: IEventMostTipData) {
    let powerHorses = [];
      powerHorses = raceEvent['horses'] && raceEvent['horses'].filter(horse => horse.isMostTipped === true);
      if (powerHorses && powerHorses.length) {
        raceEvent.powerHorses = powerHorses;
        if (raceEvent.powerHorses.length > 1) {
          raceEvent.powerHorses.forEach((horse: IHorse) => {
            if(raceEvent.markets && raceEvent.markets.length) {
              horse.runnerNumber  = this.getRunner(horse, raceEvent.markets[0].children);
            }
          });
          raceEvent.powerHorse = raceEvent.powerHorses.reduce((prev, curr) =>
            prev.runnerNumber < curr.runnerNumber ? prev : curr
          );
        } else {
          raceEvent.powerHorse = powerHorses[0];
        }
        raceEvent.isMostPowerHorse = true;
        this.pubSubService.publish(this.pubSubService.API.IS_TIP_PRESENT, {
          isTipPresent: true
        });
        this.mostTippedHorseEvents.push(raceEvent);
      }
  }

  private getRunner(horse: IHorse, outcomes: IHorseOutcome[]): string {
    const runnerOutcome = outcomes && outcomes.length && outcomes.find((out: IHorseOutcome) => horse.horseName === out.outcome.name);
    return runnerOutcome ? runnerOutcome.outcome.runnerNumber: '';
  }

}
