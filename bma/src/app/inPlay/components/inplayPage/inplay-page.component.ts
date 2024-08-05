import { Component, OnDestroy, OnInit, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, Event, NavigationEnd, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { switchMap } from 'rxjs/operators';

import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { IRibbonCache } from '@app/inPlay/models/ribbon.model';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';
import { InPlayStorageService } from '@inplayModule/services/inplayStorage/in-play-storage.service';
import { InplayMainService } from '@inplayModule/services/inplayMain/inplay-main.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'inplay-page',
  templateUrl: 'inplay-page.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class InplayPageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  activeMenuItemUri: string;
  menuItems: IRibbonCache;
  sportsAvailable = false;

  protected readonly tagName: string = 'inplayPage';
  private routeListener: Subscription;
  private connectSubscription: Subscription;

  constructor(
    protected inPlayConnectionService: InplayConnectionService,
    protected inPlayMainService: InplayMainService,
    protected inplayStorageService: InPlayStorageService,
    protected router: Router,
    protected route: ActivatedRoute,
    protected routingState: RoutingState,
    protected pubsubService: PubSubService,
    protected changeDetector: ChangeDetectorRef
  ) {
    super()/* istanbul ignore next */;
  }

  ngOnInit(): void {
    this.connectSubscription = this.inPlayConnectionService.connectComponent().pipe(
      switchMap(() => {
        /**
         * Init Cache - General approach
         */
        this.inPlayMainService.initSportsCache();

        /**
         * inPlay Sports Ribbon functionality
         */
        return this.inPlayMainService.getRibbonData();
      })
    ).subscribe((data: IRibbonCache) => {
      if (!data.data.length || (data.data.length === 1 && data.data[0].targetUriCopy === 'watchlive')) {
        this.hideSpinner();
        this.ngOnDestroy();
      } else {
        this.sportsAvailable = true;
        this.menuItems = data;
        /**
         * Make initial Active Tab - inPlay Sports Ribbon functionality
         */
        this.updateActiveTab();
        this.hideSpinner();
      }
      this.changeDetector.detectChanges();
    }, () => {
      this.showError();
      this.changeDetector.detectChanges();
    });

    this.subscribeToRouteChange();
    this.addEventListeners();
  }

  ngOnDestroy(): void {
    this.unsbscribeFromMS();
    this.pubsubService.unsubscribe(this.tagName);
    this.connectSubscription.unsubscribe();
  }

  /**
   * Updates Active Tab related to chosen sport - inPlay Sports Ribbon functionality
   */
  updateActiveTab(): void {
    this.activeMenuItemUri = this.routingState.getPathName();
    this.changeDetector.detectChanges();
  }

  protected addEventListeners(): void {
    /**
     * Set current sport Uri to Storage
     */
    this.pubsubService.subscribe(this.tagName, this.pubsubService.API.SESSION_LOGIN, () => {
      this.inPlayMainService.setSportUri(this.route.snapshot.params['sport']);
    });
  }

  private subscribeToRouteChange(): void {
    /**
     * Updates Active Tab on route change - inPlay Sports Ribbon functionality
     */
    this.routeListener = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {

        const isWatchLive = this.routingState.getPathName() === 'watchlive' ? 'watchlive' : false;
        const curSportParam = this.routingState.getRouteParam('sport', this.route.snapshot) || isWatchLive
          || this.inPlayMainService.getSportUri();
        this.inPlayMainService.setSportUri(curSportParam);

        setTimeout(() => {
          this.updateActiveTab();
        });
      }
    });
  }

  private unsbscribeFromMS(): void {
    this.routeListener && this.routeListener.unsubscribe();
    this.inplayStorageService.destroySportsCache();
    this.inPlayMainService.unsubscribeForUpdates();
    this.inPlayConnectionService.disconnectComponent();
  }
}
