import * as _ from 'underscore';
import { Injectable } from '@angular/core';
import { ISSRequestParamsModel } from '@core/models/ss-request-params.model';
import { SiteServerUtilityService } from '@core/services/siteServerUtility/site-server-utility.service';

@Injectable()
export class LoadByPortionsService {

  private readonly maxClassesInRequest = 100;

  constructor(
    private ssUtility: SiteServerUtilityService
  ) { }

  /**
   * get()
   * @param {Function} service
   * @param {string | Object} reqParams
   * @param {string} key
   * @param {number[]} ids
   * @returns {Promise<any[]>}
   */
  get(service: Function, reqParams: string|Object, key: string, ids: number[]) {
    const load = _.partial(this.loadPortion, service, reqParams, key),
      promises = this.chunkArray(ids || [], this.maxClassesInRequest).map(load);

    return Promise.all(promises)
      .then(data => this.concatResponses(data));
  }

  /**
   * chunkArray()
   * @param {number[]} ids
   * @param {number} size
   * @returns {any}
   */
  private chunkArray(ids: number[], size: number) {
    // eslint-disable-next-line prefer-spread
    return [].concat.apply([], ids.map((e, i:number) => {
      return i % size === 0 ? [ids.slice(i, i + size)] : [] as any ;
    }));
  }

  /**
   * concatResponses()
   * @param {any[]} responses
   * @returns {any[]}
   */
  private concatResponses(responses: any[]) {
    return _.flatten(_.map(responses, this.ssUtility.stripResponse));
  }

  /**
   * loadPortion()
   * @param {Function} service
   * @param {ISSRequestParamsModel} reqParams
   * @param {string} key
   * @param {string[]} ids
   * @returns {any}
   */
  private loadPortion(service: Function, reqParams: ISSRequestParamsModel, key: string, ids: string[]) {
    const params = _.extend({}, reqParams, _.object([key], [ids.join(',')]));
    return service(params);
  }
}
