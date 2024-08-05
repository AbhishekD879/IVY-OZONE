
import { from as observableFrom,  Observable } from 'rxjs';
import * as _ from 'underscore';
import { Injectable } from '@angular/core';
import { ISSRequestParamsModel } from '@core/models/ss-request-params.model';
import { BuildUtilityService } from '@core/services/buildUtility/build-utility.service';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { SiteServerUtilityService } from '@core/services/siteServerUtility/site-server-utility.service';
import { LoadByPortionsService } from '@ss/services/load-by-portions.service';
import { SimpleFiltersService } from '@ss/services/simple-filters.service';
import { IPoolModel } from '@shared/models/pool.model';

@Injectable()
export class SiteServerPoolService {

  constructor(
    private ssRequestHelper: SiteServerRequestHelperService,
    private simpleFilters: SimpleFiltersService,
    private loadByPortions: LoadByPortionsService,
    private ssUtility: SiteServerUtilityService,
    private buildUtility: BuildUtilityService
  ) { }

  /**
   * getPools()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<IPoolModel[]>}
   */
  getPools(params: ISSRequestParamsModel): Observable<IPoolModel[]> {
    return observableFrom(this.get(data => this.ssRequestHelper.getPool(data), params));
  }

  /**
   * getPoolsForEvent()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<IPoolModel[]>}
   */
  getPoolsForEvent(params: ISSRequestParamsModel): Observable<IPoolModel[]> {
    return observableFrom(this.get(data => this.ssRequestHelper.getPoolForEvent(data), params));
  }

  /**
   * getPoolsForClass()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<IPoolModel[]>}
   */
  getPoolsForClass(params: ISSRequestParamsModel): Observable<IPoolModel[]> {
    return observableFrom(this.get(data => this.ssRequestHelper.getPoolForClass(data), params));
  }

  /**
   * getPoolToPoolValue()
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<IPoolModel[]>}
   */
  getPoolToPoolValue(params: ISSRequestParamsModel): Promise<IPoolModel[]> {
    return this.get(data => this.ssRequestHelper.getPoolToPoolValue(data), params);
  }

  /**
   * get()
   * @param {Function} service
   * @param {ISSRequestParamsModel} params
   * @returns {Promise<IPoolModel[]>}
   */
  private get(service: Function, params: ISSRequestParamsModel): Promise<IPoolModel[]> {
    const simpleFilters = [
      'poolProvider',
        'poolIsActive',
        'poolTypes'
      ],
      filters = _.extend({}, _.pick(params, simpleFilters)),
      eventsPropName = params.eventsIds ? 'eventsIds' : undefined,
      classesPropName = params.classIds ? 'classIds' : undefined,
      idsPropName = params.poolsIds ? 'poolsIds' : eventsPropName || classesPropName,
      reqParams = { simpleFilters: this.simpleFilters.genFilters(filters) },
      loader = idsPropName ?
        this.loadByPortions.get(data => service(data), reqParams, idsPropName, params[idsPropName]) :
        this.ssUtility.queryService(service, reqParams);

    return loader.then(data => this.buildUtility.poolsBuilder(data));
  }
}
