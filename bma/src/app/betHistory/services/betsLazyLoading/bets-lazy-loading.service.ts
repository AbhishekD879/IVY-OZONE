import { Injectable } from '@angular/core';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { BetHistoryMainService } from '../betHistoryMain/bet-history-main.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';

import { IPageBets } from '@app/betHistory/models/bet-history.model';
import { BET_HISTORY_CONFIG } from '@betHistoryModule/constants/bet-promotions.constant';

@Injectable({ providedIn: BetHistoryApiModule })
export class BetsLazyLoadingService {
  bindedScrollHandler: Function;
  loadMoreCallBack: Function;
  initialData: any;
  isLoadingMore: boolean = false;
  pageToken: string;
  timeStamp: string;
  betType: string;
  betfilter: string;
  addLazyLoadedBets: Function;
  window: any;
  readonly BETHISTORYCONFIG = BET_HISTORY_CONFIG;

  constructor(
    private betHistoryMainService: BetHistoryMainService,
    private windowRefService: WindowRefService,
    private domTools: DomToolsService
  ) {
    this.window = this.windowRefService.nativeWindow;
  }

  initialize(options: any) {
    this.reset();
    this.isLoadingMore = false;
    this.initialData = options.initialData;
    this.betType = options.betType;
    this.betfilter = options.betfilter;
    this.addLazyLoadedBets = options.addLazyLoadedBets;
    this.loadMoreCallBack = options.loadMoreCallBack;
    this.bindedScrollHandler = this.scrollHandler.bind(this);
    this.setData(this.initialData);
  }

  reset() {
    this.bindedScrollHandler = null;
    this.initialData = null;
    this.betType = null;
    this.betfilter = null;
    this.addLazyLoadedBets = null;
    this.isLoadingMore = false;
    this.pageToken = null;
    this.timeStamp = null;
    this.window.removeEventListener('scroll', this.bindedScrollHandler);
  }

  /**
   * Scroll listener, load more bets if almost bottom position
   */
  private scrollHandler(): void {
    if (this.isLoadingMore) {
      return;
    }
    const containerNode = document.querySelector('.bet-history-page') || document.querySelector('.lazyload-scroll');
    if (!containerNode) {
      return;
    }
    const containerTopPosition = this.domTools.getOffset(containerNode).top;
    const containerBottomPosition = containerTopPosition + this.domTools.getHeight(containerNode);

    if ((this.domTools.getScrollTop(this.window) + this.domTools.getHeight(this.window)) > containerBottomPosition) {
      this.loadMore();
    }
  }

  /**
   * Sets data from response
   * @param {Object} data
   */
  setData(data, isLazyLoaded: boolean = false): void {
    if (isLazyLoaded) {
      this.addLazyLoadedBets(data.bets);
    }

    this.pageToken = data.pageToken;
    this.timeStamp = data.timeStamp;

    if (this.pageToken) {
      this.window.addEventListener('scroll', this.bindedScrollHandler);
    }
    this.isLoadingMore = false;
  }

  private loadMore(): void {
    this.window.removeEventListener('scroll', this.bindedScrollHandler);

    if (!this.pageToken) {
      this.reset();
      return;
    }

    this.isLoadingMore = true;

    if(this.loadMoreCallBack && this.betfilter === this.BETHISTORYCONFIG.sportsTab) {
      this.loadMoreCallBack();
      return;
    }
    
    this.betHistoryMainService.getHistoryPage(this.pageToken, this.betType)
      .subscribe(
        (data: IPageBets) => this.setData(data, true),
        (error) => {
          console.warn('error happened while loading bets: ', error.message);
        this.reset();
      });
  }
}
