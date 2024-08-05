import { AbstractService } from './transport/abstract.service';
import { Configuration } from '@app/client/private/models/configuration.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { GamificationData, MyBadges, SeasonData, TabNameConfigurationData } from '@root/app/one-two-free/constants/otf.model';

@Injectable()
export class OtfSeasonBadgesService extends AbstractService<Configuration> {
  byBrandUrl: string = `/brand/${this.brand}`;
  allSeasonByBrandUrl: string = `season/all/brand/${this.brand}`;
  badgesByBrandUrl: string = `badge/brand/${this.brand}`;
  tabNameConfigurationByBrandUrl: string = `otf-tab-config/brand/${this.brand}`;
  badgesUrl: string = 'badge';
  seasonUrl: string = 'season';
  gamificationUrl: string = 'gamification';
  tabNameConfigurationUrl: string = 'otf-tab-config';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  /**
   * Get Badges table Data.
   * @returns { Observable<HttpResponse<MyBadges>>}
   */
  public getBadgeData(): Observable<HttpResponse<MyBadges>> {
    return this.sendRequest<MyBadges>('get', this.badgesByBrandUrl, null);
  }

  /**
  * Post Badges Data.
  * @returns Observable<HttpResponse<MyBadges>>
  */
  public postnewBadgeData(badges: MyBadges): Observable<HttpResponse<MyBadges>> {
    badges.brand = this.brand;
    return this.sendRequest<MyBadges>('post', this.badgesUrl, badges);
  }

  /**
   * Post Badges Data.
   * @Params id
   *  badges
   * @returns Observable<HttpResponse<MyBadges>>
   */
  public putBadgeChanges(id: string, badges: MyBadges): Observable<HttpResponse<MyBadges>> {
    const apiUrl = `badge/${id}`;
    return this.sendRequest<MyBadges>('put', apiUrl, badges);
  }

    /**
   * Get TabNameConfiguration Data.
   * @returns { Observable<HttpResponse<TabNameConfigurationData>>}
   */
    public getTabNameConfiguration(): Observable<HttpResponse<TabNameConfigurationData>> {
      return this.sendRequest<TabNameConfigurationData>('get', this.tabNameConfigurationByBrandUrl, null);
    }
  
    /**
    * Post TabNameConfiguration Data.
    * @returns Observable<TabNameConfigurationData<TabNameConfigurationData>>
    */
    public postTabNameConfigurationData(tabNameConfiguration: TabNameConfigurationData): Observable<HttpResponse<TabNameConfigurationData>> {
      tabNameConfiguration.brand = this.brand;
      return this.sendRequest<TabNameConfigurationData>('post', this.tabNameConfigurationUrl, tabNameConfiguration);
    }

      /**
   * Put Badges Data.
   * @Params id
   *  badges
   * @returns Observable<HttpResponse<TabNameConfigurationData>>
   */
  public putTabNameConfigurationData(id: string, tabNameConfiguration: TabNameConfigurationData): Observable<HttpResponse<TabNameConfigurationData>> {
    const apiUrl = `otf-tab-config/${id}`;
    return this.sendRequest<TabNameConfigurationData>('put', apiUrl, tabNameConfiguration);
  }

  
  /**
  * Get All Seasons List Data.
  * @returns { Observable<HttpResponse<SeasonData[]>>}
  */
  public getAllSeasonsList(): Observable<HttpResponse<SeasonData[]>> {
    return this.sendRequest<SeasonData[]>('get', this.allSeasonByBrandUrl, null);
  }

  /**
   * Get All Seasons Data.
   * @returns { Observable<HttpResponse<SeasonData[]>}
   */
  public getAllSeasons(): Observable<HttpResponse<SeasonData[]>> {
    return this.sendRequest<SeasonData[]>('get', `${this.seasonUrl}${this.byBrandUrl}`, null);
  }

  /**
   * Get All gamification Data.
   * @returns { Observable<HttpResponse<GamificationData[]>}
  */
  public getAllGamification(): Observable<HttpResponse<GamificationData[]>> {
    return this.sendRequest<GamificationData[]>('get', `${this.gamificationUrl}${this.byBrandUrl}`, null);
  }

  /**
   * Post Season Data.
   * @returns Observable<HttpResponse<SeasonData>>
  */
  public postnewSeasonData(season: SeasonData): Observable<HttpResponse<SeasonData>> {
    season.brand = this.brand;
    return this.sendRequest<SeasonData>('post', this.seasonUrl, season);
  }

  /**
   * update Season Changes.
   * @returns Observable<HttpResponse<SeasonData>>
  */
  public putSeasonChanges(season: SeasonData, flag): Observable<HttpResponse<SeasonData>> {
    const apiUrl = `season/${season.id}/${flag}`;
    return this.sendRequest<SeasonData>('put', apiUrl, season);
  }

  /**
   * Post Gamification Data.
   * @returns Observable<HttpResponse<GamificationData>>
  */
  public postnewGamification(gamificationData): Observable<HttpResponse<GamificationData>> {
    gamificationData.brand = this.brand;
    return this.sendRequest<GamificationData>('post', this.gamificationUrl, gamificationData);
  }

  /**
   * Update Gamification
   * @Param gamificationData
   * @returns Observable<HttpResponse<GamificationData>>
  */
  public putGamificationChanges(gamificationData: GamificationData): Observable<HttpResponse<GamificationData>> {
    const apiUrl = `${this.gamificationUrl}/${gamificationData.id}`;
    return this.sendRequest<GamificationData>('put', apiUrl, gamificationData);
  }

  /**
   * Get Season by id
   * @Param id
   * @returns { Observable<HttpResponse<SeasonData>}
  */
  public getSingleSeason(id: string): Observable<HttpResponse<SeasonData>> {
    const uri = `${this.seasonUrl}/${id}`;
    return this.sendRequest<SeasonData>('get', uri, null);
  }

  /**
   * Get gamification by id
   * @returns { Observable<HttpResponse<GamificationData>> }
  */
  public getSingleGamification(id: string): Observable<HttpResponse<GamificationData>> {
    const uri = `${this.gamificationUrl}/${id}`;
    return this.sendRequest<GamificationData>('get', uri, null);
  }

  /**
   * delete Season by id
   * @Param id
   * @returns { Observable<HttpResponse<void>}
  */
  public deleteSeason(id: string): Observable<HttpResponse<void>> {
    const url = `${this.seasonUrl}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }

  /**
   * delete gamification by id
   * @Param id
   * @returns { Observable<HttpResponse<void>}
  */
  public deleteGamification(id: string): Observable<HttpResponse<void>> {
    const url = `${this.gamificationUrl}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }
}
