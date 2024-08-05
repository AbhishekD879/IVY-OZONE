import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { ISportEvent } from '@core/models/sport-event.model';

@Injectable()
export class JackpotReceiptPageService {
  private jackpotEvents: ISportEvent[] = [];
  private selectedOutcomesIds: string[] = [];
  private totalStake: number;
  private totalLines: number;
  private betReceiptNumber: string;

  constructor() {}

  get getTotalStake(): number {
    return this.totalStake;
  }
  set getTotalStake(value:number){}
  get getTotalLines(): number {
    return this.totalLines;
  }
  set getTotalLines(value:number){}
  get getBetReceiptNumber(): string {
    return this.betReceiptNumber;
  }
  set getBetReceiptNumber(value:string){}

  get getReceiptData(): ISportEvent[] {
    _.each(this.jackpotEvents, (event: ISportEvent) => {
      for (let i = 0; i < event.markets[0].outcomes.length; i++) {
        const outcome = event.markets[0].outcomes[i];
        if (this.selectedOutcomesIds.indexOf(outcome.id) === -1) {
          event.markets[0].outcomes.splice(i, 1);
          i--;
        }
      }
    });

    return _.sortBy(_.sortBy(this.jackpotEvents, 'classDisplayOrder'), 'startTime');
  }
  set getReceiptData(value:ISportEvent[]){}

  setReceiptData(events: ISportEvent[], outcomesIds: string[], stake: number, lines: number, receiptNumber: string) {
    this.jackpotEvents = events;
    this.selectedOutcomesIds = [].concat(outcomesIds);
    this.totalStake = stake;
    this.totalLines = lines;
    this.betReceiptNumber = receiptNumber;
  }
}
