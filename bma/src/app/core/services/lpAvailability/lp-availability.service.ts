import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { ISportEvent } from '../../models/sport-event.model';
import { IToteEventTab } from '@app/tote/models/tote-event-tab.model';

@Injectable()
export class LpAvailabilityService {

  private readonly CATEGORY_ID: string = '161';

  check(event: ISportEvent | IToteEventTab): boolean {
    if (event.categoryId === this.CATEGORY_ID) {
      return event.markets && event.markets[0].isLpAvailable;
    }
    const winOrEachWayMarket = _.findWhere(event.markets, { name: 'Win or Each Way' });
    return winOrEachWayMarket && winOrEachWayMarket.isLpAvailable;
  }

}
