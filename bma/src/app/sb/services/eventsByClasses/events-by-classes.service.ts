import { Injectable } from '@angular/core';

import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { SiteServerUtilityService } from '@core/services/siteServerUtility/site-server-utility.service';
import { ISSRequestParamsModel } from '@core/models/ss-request-params.model';
import { IClassModel } from '@core/models/class.model';

@Injectable()
export class EventsByClassesService {

  constructor(
    private ssRequestHelper: SiteServerRequestHelperService,
    private ssUtility: SiteServerUtilityService
  ) { }

  /**
   * getClasses()
   * @param {number} catId
   * @param {string} channels
   * @returns {Promise<IClassModel[]>}
   */
  getClasses(catId: string, channels: string = 'M'): Promise<string[]> {
    return this
      .ssRequestHelper
      .getClassesByCategory({
        categoryId: catId,
        siteChannels: channels,
        hasOpenEvent: '&simpleFilter=class.hasOpenEvent'
      })
      .then(data => this.ssUtility.stripResponse(data))
      .then(data => this.getClassIds((data)));
  }

  /**
   * getClasses()
   * @param {params} ISSRequestParamsModel
   * @returns {Promise<IClassModel[]>}
   */
  getClassesByParams(params: ISSRequestParamsModel): Promise<string[]> {
    return this
      .ssRequestHelper
      .getClassesByCategory(params)
      .then(data => this.ssUtility.stripResponse(data))
      .then(data => this.getClassIds((data)));
  }

  /**
   * getClassIds()
   * @param {IClassModel[]} classes
   * @returns {IClassModel[]}
   */
  private getClassIds(classes: IClassModel[]): string[] {
    return classes.map((c: IClassModel) => c.class['id']);
  }
}
