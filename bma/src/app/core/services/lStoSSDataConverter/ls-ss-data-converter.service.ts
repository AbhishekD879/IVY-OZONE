import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';

import { ILiveServeUpd, IPayload } from '@core/models/live-serve-update.model';
import { ICollection } from '@app/inPlay/models/collection.model';
import { IMarketData } from '@app/inPlay/models/outcome-market.model';
import { IOutputOutcome } from '@app/inPlay/models/output-outcome.model';

@Injectable()
export class LStoSSDataStructureConverterService {
  // Key maps for markets and outcomes
  private static KEYS_FOR_OUTCOME = {
    marketId: 'ev_mkt_id',
    outcomeMeaningMinorCode: 'fb_result',
    outcomeStatusCode: 'status'
  };

  private static KEYS_FOR_MARKET = {
    eventId: 'ev_id',
    templateMarketId: 'ev_oc_grp_id',
    marketMeaningMajorCode: 'mkt_type',
    marketMeaningMinorCode: 'mkt_sort',
    handicapValues: 'hcap_values',
    isLpAvailable: 'lp_avail',
    isMarketBetInRun: 'bet_in_run',
    marketStatusCode: 'status',
    liveServChildrenChannels: 'channel',
    rawHandicapValue: 'raw_hcap',
    displayed: 'displayed'
  };

  constructor(private fracToDecService: FracToDecService) {}

  /**
   * Return SS structure object
   * @params {Object} lsData - update with LS structure
   * @returns {Object}
   */
  convertData(lsData: ILiveServeUpd): IOutputOutcome | IMarketData {
    // ToDo: Temporary fix unless clarified: push-messages 'subject' property is not nested in 'payload', causing bet placement errors.
    if (!lsData.payload.subject && lsData.subject) { lsData.payload.subject = lsData.subject; }

    const type = lsData.subject_type;
    const dataPayload = lsData.payload;
    return this.convert(type, dataPayload, lsData.subject_number);
  }

  /**
   * Convert outcome with LS structure to SS structure
   * @params {Object} dataPayload - object with LS structure
   * @params {Object} ssData - common properties object for markets & outcome with SS structure
   * @returns {Object}
   */
  private convertToOutcome(dataPayload: IPayload, ssData: IOutputOutcome): IOutputOutcome {
    _.forEach(_.keys(LStoSSDataStructureConverterService.KEYS_FOR_OUTCOME), (key: string) => {
      ssData[key] = dataPayload[LStoSSDataStructureConverterService.KEYS_FOR_OUTCOME[key]];
    });
    if (+dataPayload.lp_num > 0 && +dataPayload.lp_den > 0) {
      ssData.prices = [{
        priceNum: +dataPayload.lp_num,
        priceDen: +dataPayload.lp_den,
        priceType: 'LP', // ToDo: investigate this
        priceDec: Number(this.fracToDecService.getDecimal(+dataPayload.lp_num, +dataPayload.lp_den))
      }];
    } else {
      ssData.prices = [];
    }

    if (dataPayload.runner_num) {
      ssData.runnerNumber = dataPayload.runner_num;
    }

    ssData.outcomeMeaningScores = `${dataPayload.cs_home},${dataPayload.cs_away},`;
    return ssData;
  }

  /**
   * Convert market with LS structure to SS structure
   * @params {Object} dataPayload - object with LS structure
   * @params {Object} ssData - common properties object for markets & outcome with SS structure
   * @returns {Object}
   */
  private convertToMarket(dataPayload: IPayload, ssData: IMarketData): IMarketData {
    _.forEach(_.keys(LStoSSDataStructureConverterService.KEYS_FOR_MARKET), (key: string) => {
      ssData[key] = dataPayload[LStoSSDataStructureConverterService.KEYS_FOR_MARKET[key]];
    });
    if (dataPayload.mkt_disp_code && dataPayload.mkt_disp_code !== '') {
      ssData.dispSortName = dataPayload.mkt_disp_code;
    }
    ssData.templateMarketName = dataPayload.group_names.en;
    ssData.collectionIds = this.mapToCollectionIds(dataPayload);
    return ssData;
  }

  /**
   * Concat mm_coll_id and collections id's from payload to string
   * @params {Object} lsData - object with LS structure
   * @returns {string}
   */
  private mapToCollectionIds(lsData: IPayload): string {
    return `${lsData.mm_coll_id}${this.fromCollectionToString(lsData.collections)},`;
  }

  /**
   * Concat all collection id's from array to string
   * @params {Array} collection
   * @returns {string}
   */
  private fromCollectionToString(collection: ICollection[]): string[] | string {
    if (collection.length === 0) {
      return '';
    }
    return collection.map((e: ICollection) => e.collection_id)
      .reduce((prev, current) => `${prev},${current}`, '');
  }

  /**
   * Return outcome or market with SS structure
   * @params {string} type
   * @params {Object} dataPayload - object with LS structure
   * @returns {Object}
   */
  private convert(type: string, dataPayload: IPayload, id: number): IOutputOutcome | IMarketData {
    const commonProperties = <IOutputOutcome & IMarketData>{
      id: id.toString(),
      displayOrder: dataPayload.disporder,
      liveServChannels: dataPayload.subject,
      name: dataPayload.names.en
    };
    if (type === 'sSELCN') {
      return this.convertToOutcome(dataPayload, commonProperties);
    }

    return this.convertToMarket(dataPayload, commonProperties);
  }
}
