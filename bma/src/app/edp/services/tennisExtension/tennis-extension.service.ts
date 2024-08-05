// TEMPORARY SOLUTION !!!
// WRONG FRAMEWORK USAGE !!!
// REFACTORING IS EXTREMELY NEEDED !!!

import { Injectable, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import * as _ from 'underscore';

// Models
import { IMarket } from '@core/models/market.model';
import { ITabOlympic } from '@core/models/tab.model';
import { IOutcome } from '@core/models/outcome.model';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IMarketCollection } from '@core/models/market-collection.model';
import { ISportConfig } from '@core/services/cms/models';

const GAME_MARKETS = ['Game Markets', 'Game'];

@Injectable()
export class TennisExtensionService implements OnDestroy {
  parentScope: any;
  timeOutId: any;
  private tennisConfig: ISportConfig;

  constructor(
    private pubsub: PubSubService,
    private router: Router
  ) {
    clearTimeout(this.timeOutId);
    this.updateDelay = this.updateDelay.bind(this);
  }

  ngOnDestroy() {
    clearTimeout(this.timeOutId);
  }

  public eventMarkets(parentScope, tennisConfig: ISportConfig): void {
    this.parentScope = parentScope;
    this.tennisConfig = tennisConfig;
    this.updateMarketDisplay();
    this.pubsub.subscribe('tennisExtension', this.pubsub.API.OUTCOME_UPDATED, this.updateDelay);
  }

  /**
   * Set a delay of 3 seconds before hiding the market.
   * @param {object} updatedMarket
   */
  private updateDelay(updatedMarket?: IMarket): void {
    this.timeOutId = setTimeout(() => {
      this.updateMarketDisplay(updatedMarket);
    }, 300, true);
  }

  /**
   * Update Market Display, when outcome or market status has changed.
   * @param {object} updatedMarket (optional)
   */
  private updateMarketDisplay(updatedMarket?: IMarket, ): void {
    let collection: IMarketCollection;
    this.parentScope.marketsByCollection.forEach((market: IMarketCollection) => {
      if (GAME_MARKETS.includes(market.name)) {
        collection = market;
      }
    });
    if (collection) {
      if (updatedMarket) {
        this.displayMarket(updatedMarket);
      } else {
        _.forEach(collection.markets, market => {
          this.displayMarket(market);
        });
      }
      this.displayCollection(collection);
    }
  }

  /**
   * Display Market.
   * Hide Market if all outcomes are "suspended"
   * and remove it from filteredMarketGroup.
   * @param {object} market
   */
  private displayMarket(market: IMarket): void {
    const primaryMarkets = this.tennisConfig.config.request.marketTemplateMarketNameIntersects || '',
      checkSuspended = !this.checkOutcomesInMarket(market) || market.marketStatusCode === 'S';

    if (primaryMarkets.indexOf(market.name) === -1 && checkSuspended) {
      if (this.parentScope.filteredMarketGroup) {
        this.parentScope.filteredMarketGroup = _.without(this.parentScope.filteredMarketGroup, market);
      }
      market.hidden = checkSuspended;
    }
  }

  /**
   * Display Collection.
   * Hide Collection if all markets are hidden.
   * @param {object} collection
   */
  private displayCollection(collection: IMarketCollection): void {
    let gameTab: ITabOlympic = {};
    this.parentScope.eventTabs.forEach((tab: ITabOlympic) => {
      if (GAME_MARKETS.includes(tab.label)) {
        gameTab = tab;
      }
    });

    gameTab.hidden = !this.checkMarketsInCollection(collection);
    if (gameTab.hidden && this.parentScope.activeTab.label === collection.name) {
      this.redirectToMainMarkets();
    }
  }

  /**
   * Check if not all markets are hidden.
   * Returns false if all markets are hidden, and true if some market is not hidden.
   * @param {object} collection
   */
  private checkMarketsInCollection(collection: IMarketCollection): boolean {
    return _.some(collection.markets, (market: IMarket) => {
      return !market.hidden;
    });
  }

  /**
   * Check if not all outcomes "suspended".
   * Returns false if all outcomes are "suspended", and true if some outcome is not "suspended".
   * @param {object} market
   * @returns {bool}
   */
  private checkOutcomesInMarket(market: IMarket): boolean {
    return _.some(market.outcomes, (outcome: IOutcome) => {
      return outcome.outcomeStatusCode !== 'S';
    });
  }

  /**
   * Redirect to Main Markets if possible, otherwise redirect to All Markets.
   */
  private redirectToMainMarkets(): void {
    const mainMarkets = _.findWhere(this.parentScope.eventTabs, { id: 'tab-main-markets' });
    const tab: IMarketCollection = mainMarkets || _.findWhere(this.parentScope.eventTabs, { id: 'tab-all-markets' });

    if (tab) {
      this.router.navigateByUrl(tab.url);
    }
  }
}
