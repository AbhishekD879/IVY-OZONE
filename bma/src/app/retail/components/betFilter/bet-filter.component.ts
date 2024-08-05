
import { forkJoin as observableForkJoin,  Subscription } from 'rxjs';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, Event, ChildActivationStart } from '@angular/router';
import * as _ from 'underscore';

import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import environment from '@environment/oxygenEnvConfig';
import { BetFilterParamsService } from '@app/retail/services/betFilterParams/bet-filter-params.service';
import { IBetFilterParams } from '@app/retail/services/betFilterParams/bet-filter-params.model';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { DeviceService } from '@core/services/device/device.service';
import { BET_FILTER } from '@app/retail/constants/retail.constant';
import { CommandService } from '@core/services/communication/command/command.service';
import { BackButtonService } from '@core/services/backButton/back-button.service';
import { UserService } from '@core/services/user/user.service';
import { RecapchaService } from '@app/retail/services/reCapcha/recapcha.service';

@Component({
  selector: 'bet-filter',
  templateUrl: 'bet-filter.component.html'
})

export class BetFilterComponent implements OnInit, OnDestroy {
  private routeChangeStartHandler: Subscription;
  constructor(
    protected windowRef: WindowRefService,
    protected asyncLoad: AsyncScriptLoaderService,
    protected betFilterParams: BetFilterParamsService,
    protected router: Router,
    protected routingState: RoutingState,
    protected deviceService: DeviceService,
    protected commandService: CommandService,
    protected backButtonService: BackButtonService,
    protected userService: UserService,
    private recService : RecapchaService
  ) {
    this.handleAddToBetslip = this.handleAddToBetslip.bind(this);
    this.redirectToPreviousPage = this.redirectToPreviousPage.bind(this);
  }

  ngOnInit(): void {
    this.recService.addScript();
    const historyUrl= this.router.getCurrentNavigation()?.previousNavigation?.finalUrl?.toString();
    if(historyUrl && (historyUrl.includes('/betslip/unavailable') || historyUrl.includes('/shop-locator'))&& this.router.url.includes('/bet-filter') && this.router.url.includes('?')){
      this.router.navigate(['/sport/football/coupons']);
    }
    //added below if condition for grid compliance thing
    if(!this.betFilterParams.params.couponName){
      if(this.router.url.includes('/bet-filter') && !this.router.url.includes('?')){
        this.router.navigate(['/sport/football/coupons']);
      }
    }

    if (!this.tryBootstrapBetFilter(this.betFilterParams.params)) {
      this.betFilterParams.chooseMode().subscribe((modeParams: IBetFilterParams) => {
        if (modeParams.cancelled || !this.tryBootstrapBetFilter(modeParams)) {
          this.router.navigate(['/']);
        }
      });
    }

    this.routeChangeStartHandler = this.router.events.subscribe((event: Event) => {
      if (event instanceof ChildActivationStart) {
        const curSegment = this.routingState.getCurrentSegment(),
          prevSegment = this.routingState.getPreviousSegment();

        if ((curSegment !== prevSegment && prevSegment === 'betFilter')) {
          this.windowRef.document.dispatchEvent(new CustomEvent(BET_FILTER.DESTROY_BET_FILTER));
        }
      }
    });

    this.windowRef.document.addEventListener(BET_FILTER.BF_ADD_TO_BETSLIP, this.handleAddToBetslip);
    this.windowRef.document.addEventListener(BET_FILTER.REDIRECT_TO_PREV_PAGE_BET_FILTER, this.redirectToPreviousPage);
  }

  ngOnDestroy(): void {
    this.routeChangeStartHandler.unsubscribe();
    this.windowRef.document.removeEventListener(BET_FILTER.BF_ADD_TO_BETSLIP, this.handleAddToBetslip);
    this.windowRef.document.removeEventListener(BET_FILTER.REDIRECT_TO_PREV_PAGE_BET_FILTER, this.redirectToPreviousPage);
  }

  /** Try to initialize Bet Filter with specific params
   * @param  {IBetFilterParams} params
   * @returns boolean
   */
  protected tryBootstrapBetFilter(params: IBetFilterParams): boolean {
    if (_.isEmpty(params) || !params.mode) {
      return false;
    }

    const bootstrapEvent = new CustomEvent(BET_FILTER.BOOTSTRAP_BET_FILTER,
      { detail: Object.assign({}, params, { stickyElements: !this.deviceService.isDesktop, currencyType: this.userService.currency } )});

    observableForkJoin([
      this.asyncLoad.loadJsFile(`${environment.BET_FILTER_ENDPOINT}main.js`),
      this.asyncLoad.loadCssFile(`${environment.BET_FILTER_ENDPOINT}main.css`)
    ]).subscribe(() => {
      this.windowRef.document.dispatchEvent(bootstrapEvent);
    });

    return true;
  }

  /** Redirection to previous page
   * @returns {void}
   */
  private redirectToPreviousPage(): void {
    this.backButtonService.redirectToPreviousPage();
  }

  /** Handling betslip adding
   * @returns {void}
   */
  private handleAddToBetslip(event: CustomEvent): void {
    this.commandService.executeAsync(this.commandService.API.ADD_TO_BETSLIP_BY_OUTCOME_IDS, [event.detail.ids, true, true, false]);
  }
}
