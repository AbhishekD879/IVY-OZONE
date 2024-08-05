import { Injectable } from '@angular/core';

import * as _ from 'underscore';
import { ILottoResult } from '../../models/lotto-result.model';
import { ILotto } from '@app/lotto/models/lotto.model';

@Injectable()
export class BuildLotteriesService {


  constructor() {  }

  build(data): ILotto[] {
    return this.stripResponceFooter(data)
      .map(lotteryObject => {
        return this.arrangeChildren(lotteryObject.lottery);
      })
      .filter(lotteryEntity => {
        return _.has(lotteryEntity, 'draw');
      });
  }

  buildLottoResults(data): ILottoResult[] {
    return this.stripResponceFooter(data)
      .map(lotteryObject => {
        return this.arrangeChildren(lotteryObject.lottery);
      });
  }

  /**
   * Cutts responseFooter
   *
   * @param data
   * @returns {Array}
   */
  private stripResponceFooter(data) {
    const arr = data.SSResponse.children;
    arr.splice(-1, 1);
    return arr;
  }

  /**
   * Arranges lottery children to simpler view
   *
   * @param lotteryEntity
   * @returns {*}
   */
  private arrangeChildren(lotteryEntity) {
    let propKey;
    _.forEach(lotteryEntity.children, childEntity => {
      propKey = Object.keys(childEntity)[0];
      if (!_.has(lotteryEntity, propKey)) {
        lotteryEntity[propKey] = [];
      }
      lotteryEntity[propKey].push(childEntity[propKey]);
    });
    delete lotteryEntity.children;
    return lotteryEntity;
  }

}
