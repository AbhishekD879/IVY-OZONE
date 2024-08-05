import { Component, ElementRef, OnDestroy, OnInit } from '@angular/core';

import { YourcallDashboardService } from '@yourcall/services/yourcallDashboard/yourcall-dashboard.service';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { YourcallMarketsService } from '@yourcall/services/yourCallMarketsService/yourcall-markets.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { UserService } from '@core/services/user/user.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';

import { YourCallDashboardItem } from '@yourcall/models/yourcallDashboardItem/yourcall-dashboard-item';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { AccountUpgradeLinkService } from '@app/vanillaInit/services/accountUpgradeLink/account-upgrade-link.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { BybSelectedSelectionsService } from '@app/lazy-modules/bybHistory/services/bybSelectedSelections/byb-selected-selections';

@Component({
  selector: 'yourcall-dashboard',
  templateUrl: 'yourcall-dashboard.component.html',
  styleUrls: ['./yourcall-dashboard.component.scss']
})
export class YourcallDashboardComponent implements OnInit, OnDestroy {
  expanded: boolean = true;

  EDIT_SECTION_HEIGHT: number = 0;

  readonly LIST_ITEM_HEIGHT: number = 40;
  readonly TABLET_BOTTOM_MENU_HEIGHT: number = 52;
  readonly DASHBOARD_MIN_HEIGHT: number = 50;
  readonly DASHBOARD_TOGGLE_DELAY: number = 50;
  readonly ANIMATION_DURATION: number = 500;

  sticky: boolean = false;
  disableCorrectIcon: boolean = false;
  showDashboard: boolean = true;
  dashboardItems: YourCallDashboardItem[] = [];
  marketTitles: string[] = [];
  selectionsTitles: string[] = [];
  isValid: boolean;
  briefDescription: string;
  counter = 0;
  isEnabled: boolean;
  listHeight: { [key: string]: string; };

  animate: boolean;
  alert: boolean;
  visible: boolean;

  window: any;
  document: any;
  element: any;

  relocateAfterJob: any; // timeout
  displayJob: any; // timeout
  footerVisibilityJob: any; // timeout

  windowScrollListener: () => void;
  windowResizeListener: () => void;
  elementClickListener: () => void;

  private unsubscribe$ = new Subject<void>();
  private _counter: number = 0;
  private unauthorizedFail: boolean = false;
  private updatedOdds: number = 0;
  private readonly title = 'YOUR_CALL';
  newPlayer: any;
  newStat: number;
  newSelectedId: any;
  channelstat: string;
  channelStatVal: string;
  newStatVal: any;
  oldID: any;
  oldPlyerId: number;
  newPlrId: number;
  oldStatId: any;
  oldStatVal: string | number;
  newStatId: any;
  newStatValId: any;

  constructor(
    private windowRefService: WindowRefService,
    private elementRef: ElementRef,
    private rendererService: RendererService,
    private deviceService: DeviceService,
    private pubsubService: PubSubService,
    private commandService: CommandService,
    private domToolsService: DomToolsService,
    private yourcallDashboardService: YourcallDashboardService,
    private yourcallMarketsService: YourcallMarketsService,
    private localeService: LocaleService,
    private userService: UserService,
    private accountUpgradeLinkService: AccountUpgradeLinkService,
    private bybSelectedSelectionsService: BybSelectedSelectionsService
  ) {
    this.window = this.windowRefService.nativeWindow;
    this.document = this.windowRefService.document;
    this.element = this.elementRef.nativeElement;
  }

  ngOnInit(): void {
    if (!this.deviceService.isMobileOrigin || this.deviceService.isTablet) {
      this.windowScrollListener = this.rendererService.renderer.listen(this.window, 'scroll', () =>  this.relocate());
      this.windowResizeListener = this.rendererService.renderer.listen(this.window, 'resize', () =>  {
        this.setFooterVisibility(!this.dashboard.length);
        this.relocateAfter();
      });
    }

    this.pubsubService.subscribe(this.title, this.pubsubService.API.QUICK_SWITCHER_ACTIVE,
      (state: boolean) => {
        this.setFooterVisibility(state || (!state && !this.dashboard.length));
        this.showDashboard = !state;
      });

    if (this.deviceService.isIos) {
      const body = this.document.body;

      this.elementClickListener = this.rendererService.renderer.listen(this.element, 'click', event => {
        if (event.target.nodeName.toLowerCase() === 'select') {
          this.domToolsService.scrollTop(body, this.domToolsService.getScrollTop(body));
        }
      });
    }

    this.pubsubService.subscribe(this.title, this.pubsubService.API.SUCCESSFUL_LOGIN, () => {
      if (this.unauthorizedFail) {
        this.unauthorizedFail = false;
        this.placeBet();
      }
    });

    this.pubsubService.subscribe(
      this.title,
      this.pubsubService.API.YC_DASHBOARD_DISPLAYING_CHANGED,
      (visible: boolean, keepFooterHidden: boolean = false, callback?: Function) => {
        this.setVisibility(visible, keepFooterHidden, callback);
      });
    this.pubsubService.subscribe(
      this.title,
      this.pubsubService.API.YC_MARKET_TOGGLED,
      delay => this.relocateAfter(delay)
    );
    this.pubsubService.subscribe(
      this.title,
      this.pubsubService.API.YC_NOTIFICATION_TOGGLED,
      (editMode: boolean) => this.checkAlertMessage(editMode)
    );
    this.yourcallDashboardService.dashboardItems$
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(() => this.handleDashboardItemsUpdate());

      this.yourcallMarketsService.updatedPlayersubject$.subscribe((selection:any) => {
        if(!selection)
          return
        if (selection.updatedPlayerId?.id !== undefined) {
          this.newPlayer = selection.updatedPlayerId.id;
        }
        else if (selection.updatedStatId?.id !== undefined) {
          this.newStat = selection.updatedStatId.id;
        } else if (selection.updatedStatValId !== undefined) {
          this.newStatVal = selection.updatedStatValId;
        }
      });
  }

  trackByDashboard(index: number, dashboard: YourCallDashboardItem): string {
    return `${dashboard.market.id}_${dashboard.selection.id}`;
  }

  /**
   * onDestroy controller function
   */
  ngOnDestroy(): void {
    this.setFooterVisibility(true);

    this.windowScrollListener && this.windowScrollListener();
    this.windowResizeListener && this.windowResizeListener();
    this.elementClickListener && this.elementClickListener();

    this.pubsubService.unsubscribe(this.title);
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  /**
   * Recalculate dashboard position and dimensions
   */
  relocate(): void {
    if (this.deviceService.isMobileOrigin && !this.deviceService.isTablet) {
      return;
    }

    const container = this.element;
    const dashboard = container.querySelector('section');

    if (!dashboard) {
      return;
    }

    const windowHeight = this.window.innerHeight || 0;
    const windowYOffset = this.window.pageYOffset || 0;
    const dashboardHeight = this.domToolsService.getHeight(dashboard) || this.DASHBOARD_MIN_HEIGHT;
    const dashboardOffset = this.domToolsService.getOffset(container).top || 0;
    const dashboardBottom = this.deviceService.isDesktop || this.deviceService.isMobile ? 0 : this.TABLET_BOTTOM_MENU_HEIGHT;
    const dashBoardWidth = this.domToolsService.getWidth(container.offsetParent);

    this.sticky = dashboardOffset + dashboardHeight + dashboardBottom > windowHeight + windowYOffset;

    if (this.sticky) {
      this.domToolsService.css(dashboard, {
        position: 'fixed',
        left: container.getBoundingClientRect().left,
        bottom: dashboardBottom,
        width: dashBoardWidth
      });
    } else {
      this.domToolsService.css(dashboard, { position: 'relative', left: 'auto', bottom: 'auto', width: '100%' });
    }
  }

  get disableDoneButton(): boolean {
    return this.yourcallDashboardService.isButtonAvailable;
  }
  set disableDoneButton(value:boolean){}

  /**
   * Expend/Collapse dashboard
   */
  toggle(): void {
    this.expanded = !this.expanded;
    this.relocateAfter(this.ANIMATION_DURATION);
    this.listHeight = this.getListHeight();
    this.bybSelectedSelectionsService.callGTM('open-close', {
      openClose: this.expanded  ? 'open' : 'close',
    });
  }

  /**
   * Get markets
   * @returns {Array}
   */
  get markets(): any[] {
    return this.yourcallMarketsService.markets;
  }
  set markets(value:any[]){}

  /**
   * get dashboard items
   */
  get dashboard(): YourCallDashboardItem[] {
    return this.yourcallDashboardService.items;
  }
  set dashboard(value:YourCallDashboardItem[]){}

  /**
   * Get error message to display
   * @returns {*}
   */
  get errorMessage(): string {
    let message = '';

    if (this.yourcallDashboardService.error) {
      message = this.yourcallDashboardService.errorMessage;
    } else if (this.alert) {
      message = this.localeService.getString('yourCall.dashboardAlert');
    }

    if (message) {
      this.relocate();
    }
    return message;
  }
  set errorMessage(value:string){}

  /**
   * Check if dashboard has errors
   * @returns {boolean|*}
   */
  hasErrors(): boolean {
    return this.alert || this.yourcallDashboardService.error || !this.isDashboardValid();
  }

  hideFooter(keepFooterHidden: boolean, callback?: Function): void {
    this.setFooterVisibility(!keepFooterHidden);

    this.animate = false;
    this.showDashboard = false;
    this.pubsubService.publish(this.pubsubService.API.BYB_SHOWN, false);
    this.isEnabled = this.isDashboardEnabled();

    if (this.isFunction(callback)) {
      callback();
    }
  }

  /**
   * Show/Hide dashboard with animation
   * @param visible
   * @param keepFooterHidden
   * @param callback
   */
  setVisibility(visible: boolean, keepFooterHidden: boolean = false, callback?: Function): void {
    // remove max exposure error when changing dashboard
    this.removeErrorDisplay();

    this.animate = true;
    this.alert = !visible ? this.alert : !this.yourcallDashboardService.validSelectionCount();
    this.expanded = !visible ? false : this.expanded;
    this.isEnabled = this.isDashboardEnabled();
    this.listHeight = this.getListHeight();

    if (visible) {
      this.setFooterVisibility(false);
      this.showDashboard = true;
      this.pubsubService.publish(this.pubsubService.API.BYB_SHOWN, true);
      this.pubsubService.publish('NETWORK_INDICATOR_BOTTOM_INDEX', true);
    }

    clearTimeout(this.displayJob);

    if (!this.deviceService.isMobile) {
      this.updateVisibility(visible, keepFooterHidden);
    } else {
      this.displayJob = setTimeout(() => {
        this.updateVisibility(visible, keepFooterHidden, callback);
      }, this.DASHBOARD_TOGGLE_DELAY);
    }

    if (!visible) {
      this.yourcallDashboardService.isBetslipLoading = false;
      this.pubsubService.publish('NETWORK_INDICATOR_BOTTOM_INDEX', false);
    }
  }

  updateVisibility(visible: boolean, keepFooterHidden: boolean, callback?: Function) {
    this.relocate();
    this.visible = visible;
    if (visible) {
      clearTimeout(this.footerVisibilityJob);
      if (this.isFunction(callback)) {
        callback();
      }
      return;
    }
    if (!this.deviceService.isMobile) {
      this.hideFooter(keepFooterHidden, callback);
    } else {
      this.footerVisibilityJob = setTimeout(() => {
        this.hideFooter(keepFooterHidden, callback);
      }, this.ANIMATION_DURATION);
    }
  }

  /**
   * is display odds possible
   * @returns {boolean}
   */
  get canDisplayOdds(): boolean {
    return this.yourcallDashboardService.canPlaceBet() && this.isDashboardValid() && !this.yourcallDashboardService.error;
  }

  set canDisplayOdds(value: boolean){}

  /**
   * get odds
   */
  get odds(): number | string {
    return this.yourcallDashboardService.odds;
  }
  set odds(value:number | string){}

  /**
   * Check if calculationg odds or betsip loading is in process
   * @returns {boolean|*}
   */
  get oddsLoading(): boolean {
    return this.yourcallDashboardService.loading || this.yourcallDashboardService.isBetslipLoading;
  }
  set oddsLoading(value:boolean){}

  /**
   * Remove marked selection
   * @param selection
   */
  removeSelection(selection: YourCallDashboardItem): void {
    // can`t convert MarketGroup type to MarketOutcome type
    if(!selection.selection)
      return;
    let selected;
    if(selection.selection.marketType === 'playerBets'){
      selected=selection.selection.idd;
      if(selected===undefined){
        selected=selection.selection.playerId + '-' + selection.selection.statisticId + '-' + selection.selection.value;
      }
      const obj={
        selectedID:selected,
        playerId:selection.selection.playerId
      }
      this.yourcallMarketsService.lastRemovedMarket = selected;
      this.yourcallMarketsService.playerBetRemovalsubject$.next(obj);
    }else{
      selected = selection.selection.id;
      this.yourcallMarketsService.lastRemovedMarket = selected;
      if(selection.selection.idd?.split(' - ')[1] === '6'){
        this.yourcallMarketsService.showBetRemovalsubject$.next(selected);
      }
      else {
      this.yourcallMarketsService.betRemovalsubject$.next(selected);
      }
    }
    this.yourcallMarketsService.removeSelection(selection.market as any, selection.selection);
    this.callGTM(selection);

    if (this._counter === 0) {
      this.expanded = false;
    }

    if(selection.market.key === 'ANYTIME GOALSCORER' || selection.market.key === 'FIRST GOALSCORER' ||
    selection.market.key === 'LAST GOALSCORER'){
      this.yourcallMarketsService.goalscorerSubject$.next({id: selection.selection.id,name: selection.selection.title,market: 'Goalscorer'})
    }
    // Google analytics
    // this.yourcallDashboardService.trackBoardRemovingSelection(selection.market.title);
    this.yourcallMarketsService.selectedSelectionsSet.delete(selected);
  }

    /**
   * to call gtm on adding a selection
   * @returns {void}
   */
     callGTM(selection: YourCallDashboardItem): void {
      this.bybSelectedSelectionsService.callGTM('remove-selection', {selectionName: selection.getTitle()});
    }

  /**
   * Set edit section
   * @param item
   */
  editSelection(item: YourCallDashboardItem): void {

    this.oldID=item.selection.playerId + '-' + item.selection.statisticId + '-' + item.selection.value;
    this.oldPlyerId=item.selection.playerId;
    this.oldStatId=item.selection.statisticId;
    this.oldStatVal=item.selection.value;
    // this.yourcallMarketsService.trackMarketEditingSelection();
    this.bybSelectedSelectionsService.callGTM('edit-bet', { eventLabel: "start", odds: this.odds });
    item.selection.edit = true;
    this.EDIT_SECTION_HEIGHT = this.yourcallDashboardService.isEditSection ? 145 : 0;
    this.relocateAfter(this.ANIMATION_DURATION);
    this.listHeight = this.getListHeight();
  }

  /**
   * Save edit section and close it
   * @param item
   */
  saveEditSelection(item: YourCallDashboardItem): void {
    if(this.oldID) {
      this.bybSelectedSelectionsService.duplicateIdd.delete(this.oldID);
    }
    item.selection.edit = false;
    this.EDIT_SECTION_HEIGHT = this.yourcallDashboardService.isEditSection ? 145 : 0;
    this.relocateAfter(this.ANIMATION_DURATION);
    this.listHeight = this.getListHeight();


    this.newPlrId = (this.newPlayer === undefined || this.newPlayer === null || this.newPlayer === 0 ) ? this.oldPlyerId : this.newPlayer;
    this.newStatId = (this.newStat === undefined || this.newStat === null || this.newStat === 0) ? this.oldStatId : this.newStat;

    this.newStatValId = (this.newStatVal === 0 || this.newStatVal === undefined) ? this.oldStatVal : this.newStatVal;

    this.newSelectedId = this.newPlrId + '-' + this.newStatId + '-' + this.newStatValId;
    
    let obj = {}
    obj = {
      newID: this.newSelectedId,
      oldId: this.oldID,
      oldPlayerId: this.oldPlyerId,
      newPlayerId:this.newPlrId
    }
    this.bybSelectedSelectionsService.callGTM('edit-bet', { eventLabel: "finish", odds: this.odds });
    this.yourcallMarketsService.oldNewplayerStatIdsubject$.next(obj);
    this.newPlayer=0;
    this.newStat=0;
    this.newStatVal=0;
  }

  /**
   * Get css class for specific market
   * @param market
   * @returns {string}
   */
  getCssClass(dashboard: YourCallDashboardItem): string {
    return dashboard.selection.error ?
      `${dashboard.market.key.toLowerCase().replace(/\s/g, '-')} error` :
        dashboard.market.key.toLowerCase().replace(/\s/g, '-');
  }

  /**
   * Place bet
   * @param event
   */
  placeBet(event?: CustomEvent): void {
    if (event) {
      event.stopPropagation();
    }

    if (this.userService.isInShopUser()) {
      this.windowRefService.nativeWindow.location.href = this.accountUpgradeLinkService.inShopToMultiChannelLink;
      return;
    }

    if (this.disableDoneButton) {
      return;
    } else if (!this.userService.status) {
      // Google analytics
      this.yourcallDashboardService.trackAddToQuickBetSlip('click odds', false);
      this.unauthorizedFail = true;
      this.pubsubService.publish(this.pubsubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'header' });
      return;
    }

    // Google analytics
    // this.yourcallDashboardService.trackAddToQuickBetSlip('click odds', true);
    this.yourcallDashboardService.isBetslipLoading = true;
    this.pubsubService.publish(this.pubsubService.API.ADD_TO_YC_BETSLIP,
      { selections: this.dashboard, game: this.yourcallDashboardService.game });

      this.bybSelectedSelectionsService.callGTM('add-bet', {
        selectionsCnt: this.dashboardItems.length,
        odds: this.odds
      });
  }

  /**
   * Remove error message on dashboard, endble Odds button
   * @private
   */
  private removeErrorDisplay(): void {
    this.yourcallDashboardService.showOdds = true;
    this.updatedOdds = 0;
    this.yourcallDashboardService.odds = this.updatedOdds;
  }

  private setFooterVisibility(visible: boolean): void {
    this.commandService.executeAsync(this.commandService.API.TOGGLE_FOOTER_MENU, [visible || this.deviceService.isTablet], []);
  }

  private relocateAfter(delay = 0): void {
    clearTimeout(this.relocateAfterJob);
    this.relocateAfterJob = setTimeout(this.relocate.bind(this), delay);
  }

  /**
   * Perfroms validity check of selected bets and clears alert notification state if needed.
   * @param {boolean=} clear
   * @private
   */
  private checkAlertMessage(clear: boolean): void {
    if (clear && this.dashboard.length > 1) {
      this.alert = false;
    } else {
      this.alert = this.expanded ? !this.yourcallDashboardService.validSelectionCount() : this.alert;
    }
  }

  /**
   * handles items update in dashboard
   */
  private handleDashboardItemsUpdate(): void {
    this.dashboardItems = this.yourcallDashboardService.items;
    this.setTitles();
    this.isValid = this.isDashboardValid();
    this.briefDescription = this.getBriefDescriptionText();
    this.counter = this.getCounter();
    this.isEnabled = this.isDashboardEnabled();
    this.listHeight = this.getListHeight();
  }

  private setTitles(): void {
    const titles = this.dashboardItems.reduce((acc, item) => {
      acc.marketTitles = [...acc.marketTitles, this.getMarketTitle(item)];
      acc.selectionsTitles = [...acc.selectionsTitles, this.getSelectionTitle(item)];
      return acc;
    }, { marketTitles: [], selectionsTitles: [] });
    this.marketTitles = titles.marketTitles;
    this.selectionsTitles = titles.selectionsTitles;
  }

  /**
   * Get dashboard valid status
   * @returns {*|boolean}
   */
  private isDashboardValid(): boolean {
    return this.yourcallDashboardService.valid;
  }

  /**
   * Get brief description text
   * @returns {string}
   */
  private getBriefDescriptionText(): string {
    return this.dashboard.map((item: YourCallDashboardItem) => item.getTitle()).join(', ');
  }

  /**
   * Get selections count
   * @returns {number}
   */
  private getCounter(): number {
    if (this._counter !== this.dashboard.length) {
      this._counter = this.dashboard.length;
      this.setVisibility(!!this._counter);
      this.relocateAfter(this.ANIMATION_DURATION);
    }
    return this._counter;
  }

  /**
   * Check if dashboard display enabled
   * @returns {boolean}
   */
  private isDashboardEnabled(): boolean {
    return this.dashboard.length > 0 || this.animate;
  }

  /**
   * checks if parameter is function
   * @param callback
   */
  private isFunction(callback): boolean {
    return typeof callback === 'function';
  }

  /**
   * Get selection list height
   * @returns {{height: number}}
   */
  private getListHeight(): { [key: string]: string; } {
    return {
      'height': `${this.expanded ? (this._counter * this.LIST_ITEM_HEIGHT) + this.EDIT_SECTION_HEIGHT : 0}px`,
      'max-height': `${(4 * this.LIST_ITEM_HEIGHT) + 20 + this.EDIT_SECTION_HEIGHT}px`
    };
  }

  /**
   * Get market title
   * @param market
   * @returns {string}
   */
  private getMarketTitle(market: YourCallDashboardItem): string {
    return market.getMarketTitle();
  }

  /**
   * Get selection value title
   * @param selection
   * @returns {*}
   */
  private getSelectionTitle(selection: YourCallDashboardItem): string {
    return selection.getSelectionTitle();
  }
}
