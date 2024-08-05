import { timer as observableTimer } from 'rxjs';

import { Component, OnInit, OnDestroy } from '@angular/core';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { DeviceService } from '@core/services/device/device.service';
import { BetslipTabsService } from '@core/services/betslipTabs/betslip-tabs.service';
import { IBetslipTab } from '@core/services/betslipTabs/betslip-tab.model';
import { UserService } from '@core/services/user/user.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'w-betslip',
  templateUrl: 'w-betslip.component.html',
  styleUrls: ['./w-betslip.component.scss']
})
export class WBetslipComponent implements OnInit, OnDestroy {
  title: string = 'wBeslip';
  betslipTabs: IBetslipTab[];
  sessionStateDefined: boolean = false;
  mobile: boolean;
  tabsMap: { [key: string]: string };
  MAIN_VIEWS = {
    MY_BETS: 'myBets',
    BETSLIP: 'betslip'
  };

  activeTab: IBetslipTab = { id: 1, name: '', title: '', url: '' };
  activeView: string = '';
  quickDepositIFrameOpened = false;
  errorMsg: string = '';
  bsHeight: string = '100%';
  stakesCount:number = 4;
  isHeightUpdated = false;
  betCount: number;
  isBetCountMatch: boolean = false;
  isDefaultHeight: boolean = false;
  isCoral: boolean;

  private editMyAccaUnsavedInWidget: boolean;

  constructor(
    protected pubSubService: PubSubService,
    private localeService: LocaleService,
    private deviceService: DeviceService,
    private betslipTabsService: BetslipTabsService,
    private windowRef: WindowRefService,
    public userService: UserService
  ) {
    this.isCoral = environment && environment.brand === 'bma';
    this.mobile = this.deviceService.isMobileOrigin && this.deviceService.isMobile;
    this.tabsMap = {
      cashout: this.localeService.getString('app.betslipTabs.cashout'),
      openbets: this.localeService.getString('app.betslipTabs.openbets'),
      bethistory: this.localeService.getString('app.betslipTabs.betHistory')
    };

    this.openBetslip = this.openBetslip.bind(this);
  }

  /**
   * Display bets based on calculated custom height
   */
  displayBets(): void {
    if (this.isHeightUpdated) {
      const myBetNodes = this.windowRef.document.querySelector('#bs-tabs-container');
      const betTypesNode = this.windowRef.document.querySelector('.my-bets-single-stakes-scroll');
      if (myBetNodes && betTypesNode) {        
        this.handleHeightUpdate(myBetNodes, betTypesNode);        
      }
    }
  }

  handleHeightUpdate(myBetNodes: Element, betTypesNode: Element, isFirstUpdate: boolean = true): void {
    if (this.betCount <= this.stakesCount) {
      this.bsHeight = '100%';
    } else {
      const singleStakes = this.windowRef.document.querySelectorAll('.my-bets-item-scroll');
      if (this.betCount !== singleStakes.length && !this.isBetCountMatch) {
        this.isBetCountMatch = true;
        this.handleHeightUpdate(myBetNodes, betTypesNode);
      }
      let stakeMaxHeight = 0;
      const bufferHeight = 22;
      [...singleStakes].slice(0, this.stakesCount).forEach((element: Element) => {
        stakeMaxHeight += element.clientHeight;
      });
      const spinnerScroll = this.windowRef.document.querySelector('.myBets .spinner-loader');
      const ignoreScroll = this.windowRef.document.querySelector('.my-bets-ignore-scroll');
      const betTypesNodeHeight = betTypesNode?.clientHeight || 0;
      const ignoreScrollHeight = ignoreScroll?.clientHeight || 0;
      const spinnerScrollHeight = spinnerScroll?.clientHeight + 20 || 0;
      const bsMaxHeight = myBetNodes.scrollHeight - betTypesNodeHeight - ignoreScrollHeight + stakeMaxHeight + bufferHeight - spinnerScrollHeight;

      this.bsHeight = `${bsMaxHeight}px`;
      [...singleStakes].slice(0, this.betCount>20 ? this.betCount - 20 : this.betCount).forEach((element: Element) => {
        stakeMaxHeight += element.clientHeight;
      });
      myBetNodes.scrollTop = this.betCount>20 ? stakeMaxHeight : 0;
      if (isFirstUpdate) {
        // Bet receipt wrapping after scroll is added    
        this.handleHeightUpdate(myBetNodes, betTypesNode, false);
      }
    }
    this.isHeightUpdated = false;
  }

  ngOnInit(): void {
    this.betslipTabsService.getTabsList().subscribe((tabs: IBetslipTab[]) => {
      this.betslipTabs = tabs;

      // select second tab (cashout / open bets)
      this.activeTab.id = tabs[1].id;
      if (!this.userService.status) {
        this.showError(tabs[1].name);
      }
    });

    this.pubSubService.subscribe(this.title, [this.pubSubService.API.SESSION_LOGOUT,
      this.pubSubService.API.HOME_BETSLIP], this.openBetslip);

    this.pubSubService.subscribe(this.title, this.pubSubService.API.LOAD_CASHOUT_BETS,
      () => this.selectMyBetsTab(
        this.betslipTabsService.createTab('cashout', 1)
      ));

    this.pubSubService.subscribe(this.title, 'LOAD_UNSETTLED_BETS',
       () => this.selectMyBetsTab(
        this.betslipTabsService.createTab('openbets', 2)
      ));

    this.pubSubService.subscribe(this.title, 'LOAD_BET_HISTORY',
      () => this.selectMyBetsTab(
        this.betslipTabsService.createTab('betHistory', 3)
      ));

    this.pubSubService.subscribe(this.title, 'EMA_UNSAVED_IN_WIDGET', (unsaved: boolean) => {
      this.editMyAccaUnsavedInWidget = unsaved;
    });

    // No need to render betslip container instantly. Get advantage of betslip lazy loading
    observableTimer(100).subscribe(this.openBetslip);

    this.pubSubService.subscribe(this.title, this.pubSubService.API.TOGGLE_QUICK_DEPOSIT_IFRAME, (isOpened: boolean) => {
      this.quickDepositIFrameOpened = isOpened;
    });

    this.pubSubService.subscribe(this.title, 'UPDATE_SETTLED_BETS_HEIGHT', (betCount: number) => {
      if(this.deviceService.isDesktop) {
        this.bsHeight = '100%';
        this.betCount = betCount;
        this.isHeightUpdated = true;
        this.displayBets();
      }
    });
    if(this.deviceService.isDesktop) {
      this.isHeightUpdated = true;
      this.displayBets();
    }
    this.pubSubService.subscribe(this.title, 'UPDATE_ITEM_HEIGHT', (isDefaultHeight: boolean) => {
      if (isDefaultHeight) {
        this.isDefaultHeight = isDefaultHeight;
      } else {
        this.isDefaultHeight = false;
        this.bsHeight = '100%';
        this.isHeightUpdated = true;
        this.displayBets();
      }
    })
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.title);
  }

  handleTabClick(data) {
    if (!this.editMyAccaUnsavedInWidget) {
      this.selectBetSlipTab(data.id, data.tab);
    } else {
      this.pubSubService.publish(this.pubSubService.API.EMA_OPEN_CANCEL_DIALOG);
    }
  }

  setActiveView(view: string): void {
    if (this.editMyAccaUnsavedInWidget) {
      this.pubSubService.publish(this.pubSubService.API.EMA_OPEN_CANCEL_DIALOG);
    } else {
      this.activeView = view;
    }
    this.publishTabName(view);
  }

  /**
   * setting tab name in a publisher for re use
   * @param {string} view
   */
  private publishTabName(view: string): void {
    if (view === 'betslip') {
      this.pubSubService.publish(this.pubSubService.API.REUSE_LOCATION, view);
    } else {
      const title = this.betslipTabs.find(tab => tab.id === this.activeTab.id).title
      this.pubSubService.publish(this.pubSubService.API.REUSE_LOCATION, 'my bets- ' + title.toLocaleLowerCase());
    }
  }

  /**
   * Select betslip widget tab for tablet
   * @param {string} label
   * @param {IBetslipTab} tab
   */
  private selectBetSlipTab(label: string, tab: IBetslipTab): void {
    this.updateActiveTab(tab);
    this.publishTabName(this.activeView);
    this.pubSubService.publish(this.pubSubService.API.BETSLIP_LABEL, label);
  }

  /**
   * Select my bets widget tab for tablet
   * @param {IBetslipTab} tab
   */
  private selectMyBetsTab(tab: IBetslipTab): void {
    this.updateActiveTab(tab);
    this.setActiveView(this.MAIN_VIEWS.MY_BETS);
  }

  /**
   * update active tab id and name and show error if user is not logged in
   * @param {IBetslipTab} tab
   */
  private updateActiveTab(tab: IBetslipTab ): void {
    this.activeTab = { ...this.activeTab, id: tab.id, name: tab.name };

    if (!this.userService.status) {
      this.showError(tab.name);
    }
  }

  private openBetslip(): void {
    this.setActiveView(this.MAIN_VIEWS.BETSLIP);
  }

  /**
   * Show error message when user is logged out
   */
  private showError(activeTabName: string): void {
    const activeTabId: string = activeTabName.replace(/\s/g, '').toLowerCase();
    const page: string = this.localeService.getString(`app.betslipTabs.${activeTabId}`).toLowerCase();

    this.errorMsg = this.localeService.getString(
      'app.loginToSeePageMessage',
      activeTabId === 'cashout' ? { page: `${ page } bets` } : { page }
    );
  }

}
