import { Injectable } from '@angular/core';
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';

import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { ApiClientService } from '../../client/private/services/http';
import { LeagueLink } from '@root/app/client/private/models';
import { MarketLink } from '@root/app/client/private/models/marketLink.model';

@Injectable()
export class StatisticLinksService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService
  ) {
  }

  /**
   * Wrap request to handle success/error.
   * @param observableDate
   */
  wrappedObservable(observableDate): Observable<HttpResponse<any>> {
    return observableDate
      .map(res => {
        this.globalLoaderService.hideLoader();
        return res;
      })
      .catch(response => {
        if (response instanceof HttpErrorResponse) {
          const message = response.error ? response.error.message : response.message;
          this.handleRequestError(message);
        }

        return Observable.throw(response);
      });
  }

  /**
   * Handle networking error.
   * Notify user.
   */
  handleRequestError(message): void {
    this.globalLoaderService.hideLoader();
  }

  // League links API
  /**
   * Get league links data.
   * @returns {Observable<HttpResponse<LeagueLink[]>>}
   */
  getLeagueLinksList(): Observable<HttpResponse<LeagueLink[]>> {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.statiscticsLeagueLinks().findAllLeagueLinks();

    return this.wrappedObservable(getData);
  }

  /**
   * Creates new league link.
   * @param {LeagueLink} link
   */
  createLeagueLink(link: LeagueLink): Observable<HttpResponse<LeagueLink>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.statiscticsLeagueLinks().createLeagueLink(link);
    return this.wrappedObservable(getData);
  }

  /**
   * Deletes league link.
   * @param {string} id
   */
  deleteLeagueLink(id: string): Observable<any> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.statiscticsLeagueLinks().deleteLeagueLink(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to league link.
   * @param {LeagueLink} league link
   */
  putLeagueLinkChanges(link: LeagueLink): Observable<HttpResponse<LeagueLink>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.statiscticsLeagueLinks().editLeagueLink(link);
    return this.wrappedObservable(getData);
  }

  /**
   * Load single league link data to edit.
   * @param {string} id
   * @returns {any}
   */
  getSingleLeagueLink(id: string): Observable<HttpResponse<LeagueLink>> {
    const getData =  this.apiClientService.statiscticsLeagueLinks().getSingleLeagueLink(id);
    return this.wrappedObservable(getData);
  }

  // Maket links API
  /**
   * Get market links data.
   * @returns {Observable<HttpResponse<MarketLink[]>>}
   */
  getMarketLinksList(): Observable<HttpResponse<MarketLink[]>> {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.statiscticsMarketLinks().findAllMarketLinks();

    return this.wrappedObservable(getData);
  }

  /**
   * Creates new league link.
   * @param {LeagueLink} link
   */
  createMarketLink(link: MarketLink): Observable<HttpResponse<MarketLink>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.statiscticsMarketLinks().createMarketLink(link);
    return this.wrappedObservable(getData);
  }

  /**
   * Deletes market link.
   * @param {string} id
   */
  deleteMarketLink(id: string): Observable<any> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.statiscticsMarketLinks().deleteMarketLink(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to market link.
   * @param {MarketLink} market link
   */
  putMarketLinkChanges(link: MarketLink): Observable<HttpResponse<MarketLink>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.statiscticsMarketLinks().editMarketLink(link);
    return this.wrappedObservable(getData);
  }

  /**
   * Load single market link data to edit.
   * @param {string} id
   * @returns {Observable<HttpResponse<MarketLink>>}
   */
  getSingleMarketLink(id: string): Observable<HttpResponse<MarketLink>> {
    const getData =  this.apiClientService.statiscticsMarketLinks().getSingleMarketLink(id);
    return this.wrappedObservable(getData);
  }
}
