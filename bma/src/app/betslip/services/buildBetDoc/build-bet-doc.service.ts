import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';

import { BsDocService } from '../bsDoc/bs-doc.service';
import { BetFactoryService } from '../betFactory/bet-factory.service';
import { DeviceService } from '@core/services/device/device.service';
import { ILeg } from '../models/bet.model';
import { BetErrorService } from '../betError/bet-error.service';
import { LegFactoryService } from '@betslip/services/legFactory/leg-factory.service';

@Injectable({ providedIn: BetslipApiModule })
export class BuildBetDocService extends BsDocService {
  static ngInjectableDef = undefined;

  constructor(
    private deviceService: DeviceService,
    betFactoryService: BetFactoryService,
    legFactoryService: LegFactoryService,
    betErrorService: BetErrorService
  ) {
    super(betFactoryService, legFactoryService, betErrorService);
  }

  content(legs: ILeg[] | any): ILeg | any {
    let request: Partial<ILeg> = {};
    if(legs.length && legs[0].isLotto) {
      request = { lines: [], price: {}};
      legs.forEach(leg => {
        request.lines.push({
          lotteryId: leg.id, priceId: leg.details.priceId, picks: leg.details.selections
        });
        request.price[leg.details.priceId] = leg.details.odds.map(odd => {
            return { numberPick: odd.numberPicks,num:odd.priceNum,den:odd.priceDen };
          });
       });
      return request;
    }

    _.extend(request, this.deviceService.channel);
    request.leg = BuildBetDocService.renderLegs(legs);
    request.legGroup = BuildBetDocService.renderLegGroups(legs);
    request.returnOffers = BuildBetDocService.checkForUniqueOutcomeIds(legs).length > 2 ? 'Y' : 'N';

    return <ILeg>request;
  }

  private static renderLegs(legs: ILeg[]): ILeg[] {
    return _.map(legs, leg => {
      return leg.doc();
    });
  }

  private static checkForUniqueOutcomeIds(legs: ILeg[]): number[] {
    return _.uniq(_.pluck(legs, 'firstOutcomeId'));
  }

  private static renderLegGroups(legs: ILeg[]): ILeg[] {
    const legRefArray = [];
    const mtplWinEl = { legRef: [] };
    const mtplEWEl = { legRef: [] };

    _.each(legs, (item: ILeg) => {
      // to avoid duplication select only win legs
      if (item.winPlace === 'WIN' || item.combi) {
        legRefArray.push({
          legRef: [{ documentId: item.docId }]
        });
      }
      // create leg references for multiples
      if (legs.length > 1 && item.winPlace !== 'EXPLICIT_PLACES' && item.combi !== 'SCORECAST') {
        // form leg reference of win legs
        if (item.winPlace === 'WIN') {
          mtplWinEl.legRef.push({ documentId: item.docId });
        } else if (item.winPlace === 'EACH_WAY') { // form leg reference of EW legs
          mtplEWEl.legRef.push({ documentId: item.docId });
        }
      }
    });

    if (legs.length > 1 && mtplWinEl.legRef.length > 1) {
      legRefArray.push(mtplWinEl);
    }
    // push EW leg ref array only if all the selection in the list have EW part
    if (legs.length > 1 && mtplEWEl.legRef.length > 1 && mtplEWEl.legRef.length === mtplWinEl.legRef.length) {
      legRefArray.push(mtplEWEl);
    }

    return legRefArray;
  }
}
