import { Injectable } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';

import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { ApiClientService } from '../../client/private/services/http/';
import { YourCallLeague, YourCallMarket, YourCallStaticBlock } from '../../client/private/models';

@Injectable()
export class YourCallAPIService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService) {
  }

  /**
   * Wrap request to handle success/error.
   * @param observableDate
   */
  wrappedObservable(observableDate) {
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
  handleRequestError(message) {
    this.globalLoaderService.hideLoader();
  }

  // Leagues API
  /**
   * Get leagues data.
   * @returns {Observable<HttpResponse<YourCallLeague[]>>}
   */
  getLeaguesList() {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.yourCallLeagues().findAllLeagues();

    return this.wrappedObservable(getData);
  }

  /**
   * Load single league data to edit.
   * @param {string} id
   * @returns {any}
   */
  getSingleLeague(id: string) {
    const getData =  this.apiClientService.yourCallLeagues().getSingleLeague(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to league.
   * @param {YourCallLeague} league
   */
  putLeagueChanges(league: YourCallLeague) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.yourCallLeagues().editLeague(league);
    return this.wrappedObservable(getData);
  }

  /**
   * Deletes league.
   * @param {string} id
   */
  deleteLeague(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.yourCallLeagues().deleteLeague(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Creates new league.
   * @param {YourCallLeague} league
   */
  createLeague(league: YourCallLeague) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.yourCallLeagues().createLeague(league);
    return this.wrappedObservable(getData);
  }

  /**
   * Posts new order for leagues.
   * @param {any} leaguesOrder
   * @returns {Observable<HttpResponse<YourCallLeague[]>>}
   */
  postNewLeaguesOrder(leaguesOrder: any) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.yourCallLeagues().postNewLeaguesOrder(leaguesOrder);

    return this.wrappedObservable(getData);
  }

  // Markets API
  /**
   * Get markets data.
   * @returns {Observable<HttpResponse<YourCallMarket[]>>}
   */
  getMarketsList() {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.yourCallMarkets().findAllMarkets();

    return this.wrappedObservable(getData);
  }

  /**
   * Load single market data to edit.
   * @param {string} id
   * @returns {any}
   */
  getSingleMarket(id: string) {
    const getData =  this.apiClientService.yourCallMarkets().getSingleMarket(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to market.
   * @param {YourCallMarket} market
   */
  putMarketChanges(market: YourCallMarket) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.yourCallMarkets().editMarket(market);
    return this.wrappedObservable(getData);
  }

  /**
   * Deletes market.
   * @param {string} id
   */
  deleteMarket(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.yourCallMarkets().deleteMarket(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Creates new market.
   * @param {YourCallMarket} market
   */
  createMarket(market: YourCallMarket) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.yourCallMarkets().createMarket(market);
    return this.wrappedObservable(getData);
  }

  /**
   * Posts new order for leagues.
   * @param {any}  marketsOrder
   * @returns {Observable<HttpResponse<YourCallMarket[]>>}
   */
  postNewMarketsOrder(marketsOrder: any) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.yourCallMarkets().postNewMarketsOrder(marketsOrder);

    return this.wrappedObservable(getData);
  }

  // Static Blocks API
    /**
   * Get staticBlocks data.
   * @returns {Observable<HttpResponse<YourCallStaticBlock[]>>}
   */
  getStaticBlocksList() {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.yourCallStaticBlocks().findAllStaticBlocks();

    return this.wrappedObservable(getData);
  }

  /**
   * Load single staticBlock data to edit.
   * @param {string} id
   * @returns {any}
   */
  getSingleStaticBlock(id: string) {
    const getData =  this.apiClientService.yourCallStaticBlocks().getSingleStaticBlock(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to staticBlock.
   * @param {YourCallStaticBlock} staticBlock
   */
  putStaticBlockChanges(staticBlock: YourCallStaticBlock) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.yourCallStaticBlocks().editStaticBlock(staticBlock);
    return this.wrappedObservable(getData);
  }

  /**
   * Deletes staticBlock.
   * @param {string} id
   */
  deleteStaticBlock(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.yourCallStaticBlocks().deleteStaticBlock(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Creates new staticBlock.
   * @param {YourCallStaticBlock} staticBlock
   */
  createStaticBlock(staticBlock: YourCallStaticBlock) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.yourCallStaticBlocks().createStaticBlock(staticBlock);
    return this.wrappedObservable(getData);
  }
}
