import { IClassModel } from '@core/models/class.model';
import { IYourcallBYBEventResponse } from '@yourcall/models/byb-events-response.model';
import { IYourcallBYBLeagueEventsResponse } from './../../models/byb-events-response.model';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { IYourCallLeague } from '@core/services/cms/models/yourcall/yourcall-league.model';
import { YOURCALL_DATA_PROVIDER } from '@yourcall/constants/yourcall-data-provider';
import { YourcallService } from '@yourCallModule/services/yourcallService/yourcall.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { YourcallProviderService } from '@yourcall/services/yourcallProvider/yourcall-provider.service';

@Injectable({
  providedIn: 'root'
})
export class BybHomeService {

  upcomingLeagues: IYourcallBYBEventResponse[];
  todayLeagues: IYourcallBYBEventResponse[];
  leaguesStatuses: { [key: number]: boolean; };
  classData: {
    [key: string]: {
      categoryId: number;
      categoryName: string;
      className: string;
      typeName: string;
    }
  };

  private cmsLeagues: IYourCallLeague[];
  private msLeagues: IYourcallBYBEventResponse[];
  private orderedLeaguesIds: number[];

  constructor(
    private yourCallProvider: YourcallProviderService,
    private cms: CmsService,
    private yourCallService: YourcallService
  ) {
    this.cmsLeagues = null;
    this.msLeagues = [];
    this.upcomingLeagues = null;
    this.todayLeagues = null;
    this.orderedLeaguesIds = null;
    this.leaguesStatuses = {};
    this.classData = {};
  }

  /**
   * Get leagues from cms & ms and entry point for preparing of them
   * @return {Promise}
   * @private
   */
  getLeagues(): Promise<boolean> {
    return Promise.all([this.getUpcomingLeagues(), this.getCMSLeagues()])
    .then((result) => this.getLeaguesClassData(result[0], result[1]))
    .then(({ upcomingLeagues, cmsLeagues }) => this.prepareLeagues(upcomingLeagues, cmsLeagues));
  }

  /**
   * Prepare leagues class data
   * @param data
   */
  parseClassData(data: IClassModel[]): void {
    _.each(data, (classInfo: IClassModel) => {
      const classData = classInfo.class;
      _.each(classData.children, typeInfo => {
        const typeData = typeInfo.type;
        const leagueId = typeData.id;

        this.classData[leagueId] = {
          categoryId: classData.categoryId,
          categoryName: classData.categoryName,
          className: classData.name,
          typeName: typeData.name
        };
      });
    });
  }

  /**
   * Load classData for byb leagues
   * @param upcomingLeagues
   * @param cmsLeagues
   * @returns {Promise}
   * @private
   */
  private getLeaguesClassData(upcomingLeagues: IYourcallBYBLeagueEventsResponse, cmsLeagues: IYourCallLeague[]) {
    const flatLeagues = _.flatten(_.toArray(upcomingLeagues.data));
    const ids = _.pluck(flatLeagues, 'obTypeId');
    return this.yourCallService.getClassData(ids).then((classData: IClassModel[]) => {
      this.parseClassData(classData);
      return { upcomingLeagues, cmsLeagues };
    });
  }

  /**
   * Prepare leagues data
   * @param upcomingLeagues
   * @param cmsLeagues
   * @returns {boolean}
   * @private
   */
  private prepareLeagues(upcomingLeagues: IYourcallBYBLeagueEventsResponse, cmsLeagues: IYourCallLeague[]) {
    this.msLeagues = [];
    _.each(<any>upcomingLeagues.data, (group: IYourcallBYBEventResponse[], period: string) => {
      _.each(group, (league: IYourcallBYBEventResponse) => {
        const obj = Object.assign(league, { period });
        if (this.classData[league.obTypeId]) {
          _.extend(obj, this.classData[league.obTypeId], { normilized: true });
        }
        this.msLeagues.push(obj);
      });
    });
    this.cmsLeagues = cmsLeagues;
    this.orderedLeaguesIds = _.pluck(this.cmsLeagues, 'typeId').reverse();

    _.each(this.cmsLeagues, (leagueConfig: IYourCallLeague) => {
      this.leaguesStatuses[leagueConfig.typeId] = leagueConfig.enabled;
    });

    this.fillLeagues();
    return true;
  }

  /**
   * Request to get all leagues from ms (today + upcoming)
   * @return {Promise}
   * @private
   */
  private getUpcomingLeagues(): Promise<any> {
    return this.yourCallProvider.useOnce(YOURCALL_DATA_PROVIDER.BYB).getUpcomingLeagues();
  }

  /**
   * Request to get all leagues from CMS
   * @return {Promise}
   * @private
   */
  private getCMSLeagues(): Promise<IYourCallLeague[]>  {
    return this.cms.getCmsYourCallLeaguesConfig().toPromise();
  }

  /**
   * Fills today and upcoming collections for future displaying
   * @private
   */
  private fillLeagues(): void {
    this.todayLeagues = this.sortLeagues('today');
    this.upcomingLeagues = this.sortLeagues('upcoming');
  }

  /**
   * Sorts ms leagues by cms leagues
   * @param source
   * @private
   */
  private sortLeagues(period: string): IYourcallBYBEventResponse[] {
    const leagues = _.where(this.msLeagues, { period });
    return leagues.sort((a: IYourcallBYBEventResponse, b: IYourcallBYBEventResponse) => {
      return this.orderedLeaguesIds.indexOf(b.obTypeId) - this.orderedLeaguesIds.indexOf(a.obTypeId);
    });
  }
}
