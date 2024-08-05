import { Injectable } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { forkJoin } from 'rxjs/observable/forkJoin';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/of';
import * as _ from 'lodash';

import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ApiClientService } from '@app/client/private/services/http';
import { NavigationPoint, ModuleRibbonTab, SportCategory, Competition } from '../../client/private/models';
import { Order } from '@app/client/private/models/order.model';

type NavigationPointsServiceDataType = Observable<HttpResponse<void | NavigationPoint |
  NavigationPoint[] | ModuleRibbonTab[] | SportCategory[] | Competition[]>>;

@Injectable()
export class NavigationPointsApiService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService) {
  }

  /**
   * Wrap request to handle success/error.
   * @param {Observable<HttpResponse>} observableDate
   */
  private wrappedObservable(observableDate: NavigationPointsServiceDataType): NavigationPointsServiceDataType {
    this.globalLoaderService.showLoader();

    return observableDate
      .map(res => {
        this.globalLoaderService.hideLoader();
        return res;
      })
      .catch(response => {
        const emptyResponse = new HttpResponse({
          body: null,
          headers: response.headers,
          status: response.status,
          statusText: response.statusText,
          url: response.url
        });

        this.globalLoaderService.hideLoader();
        return Observable.of(emptyResponse);
      });
  }

  /**
   * Load single navigation point data to edit.
   * @param {string} id
   * @returns {Observable<HttpResponse<NavigationPoint>>}
   */
  public getSingleNavigationPoint(id: string): NavigationPointsServiceDataType {
    const getData = this.apiClientService.navigationPoints().findOne(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to navigation point.
   * @param {NavigationPoint} navigation point
   * @returns {Observable<HttpResponse<NavigationPoint>>}
   */
  public updateNavigationPoint(quickLink: NavigationPoint): NavigationPointsServiceDataType {
    const getData = this.apiClientService.navigationPoints().update(quickLink);
    return this.wrappedObservable(getData);
  }

  /**
   * Order changes to navigation point.
   * @param {NavigationPoint} navigation point
   * @returns {Observable<HttpResponse<NavigationPoint>>}
   */
  public reorderNavigationPoints(newOrder: Order): NavigationPointsServiceDataType {
    const getData = this.apiClientService.navigationPoints().reorderNavigationPoints(newOrder);
    return getData;
  }

  /**
   * Deletes navigation point.
   * @param {string} id
   * @return {Observable<HttpResponse<NavigationPoint>>}
   */
  public deleteNavigationPoint(id: string): NavigationPointsServiceDataType {
    const getData = this.apiClientService.navigationPoints().delete(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Creates new navigation point.
   * @param {NavigationPoint} navigation point
   * @returns {Observable<HttpResponse<NavigationPoint>>}
   */
  public createNavigationPoint(quickLink: NavigationPoint): NavigationPointsServiceDataType {
    const getData = this.apiClientService.navigationPoints().save(quickLink);
    return this.wrappedObservable(getData);
  }

  /**
   * get NavigationPoints By Segment
   * @param segment value
   * @returns 
   */
  public getNavigationPointsBySegment(segment: string): NavigationPointsServiceDataType {
    const getData = this.apiClientService.navigationPoints().getListBySegment(segment);
    return this.wrappedObservable(getData);
  }

  /**
   * Get sport categories list to map promotion
   * @returns {Observable<HttpResponse<ModuleRibbonTab[]>>}
   */
  private getModuleRibbonTabs(): NavigationPointsServiceDataType {
    const getData = this.apiClientService.moduleRibbonTab().getByBrand();
    return this.wrappedObservable(getData);
  }

  /**
   * Get sport categories list to map promotion
   * @returns {Observable<HttpResponse<SportCategory[]>>}
   */
  private getSportCategories(): NavigationPointsServiceDataType {
    const getData = this.apiClientService.sportCategoriesService().getSportCategories();
    return this.wrappedObservable(getData);
  }

  /**
   * Get big competitions list
   * @returns {Observable<HttpResponse<Competition[]>>}
   */
  private getCompetitions(): NavigationPointsServiceDataType {
    const getData = this.apiClientService.competitions().findAllCompetitions();
    return this.wrappedObservable(getData);
  }

  /**
   * Filters sport category to be included in AZ sports, to have categoryId set and
   *   not be in the list of non-sports.
   * @returns {boolean}
   */
  private filterSportCategory(sportCategory: SportCategory): boolean {
    const EXCLUDED_SPORT_CATEGORIES = ['yourcall', 'lotto', 'tote', 'virtual-sports'];
    return sportCategory.showInAZ && !!sportCategory.categoryId &&
      !_.includes(EXCLUDED_SPORT_CATEGORIES, sportCategory.targetUri.toLowerCase());
  }

  /**
   * Combines requests for module ribbon tabs, sport categories and competitions in parallel.
   * @return {Observable<[ModuleRibbonTab[], SportCategory[], Competition[]]>}
   */
  public getLandingPages(): Observable<[ModuleRibbonTab[], SportCategory[], Competition[]]> {
    const homeTabs$: Observable<ModuleRibbonTab[]> = this.getModuleRibbonTabs()
      .map((data: HttpResponse<ModuleRibbonTab[]>) => {
        return _.sortBy(data.body, 'title');
       });
    const sportCategories$: Observable<SportCategory[]> = this.getSportCategories()
      .map((data: HttpResponse<SportCategory[]>): SportCategory[] => {
        return _.chain(data.body)
          .filter(this.filterSportCategory.bind(this))
          .sortBy('imageTitle')
          .value();
      });
    const competitions$: Observable<Competition[]> = this.getCompetitions()
      .map((data: HttpResponse<Competition[]>) => {
        return _.sortBy(data.body, 'name');
      });

    return forkJoin(homeTabs$, sportCategories$, competitions$);
  }
}
