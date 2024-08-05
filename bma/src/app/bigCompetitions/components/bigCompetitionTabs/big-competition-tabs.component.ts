import { of as observableOf,  Subscription } from 'rxjs';
import { finalize, concatMap } from 'rxjs/operators';
import { Component, OnInit, OnDestroy, ViewEncapsulation, Input } from '@angular/core';
import { ActivatedRoute, Router, Params } from '@angular/router';
import * as _ from 'underscore';

import { ICompetitionTabs } from '../../models/ICompetitionTabs';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { IBCModule, ICompetitionSubTab } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.model';

import { BigCompetitionsService } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { DeviceService } from '@app/core/services/device/device.service';

@Component({
  selector: 'big-competition-tabs',
  templateUrl: './big-competition-tabs.html',
  styleUrls: ['./big-competition-tabs.scss'],
  encapsulation: ViewEncapsulation.None
})
export class BigCompetitionTabsComponent extends AbstractOutletComponent implements OnInit, OnDestroy {

  @Input() tab: string;

  showLoader: boolean;
  switchers: ISwitcherConfig[];
  modulesData: IBCModule[];
  filter: number;
  subtabData: ICompetitionSubTab[];
  loadFailed: boolean;
  isPromoUnavailable: boolean = false;
  routeSubscriber: Subscription;
  loadDataSubscriber: Subscription;
  currentTab: string;
  constructor(
    public bigCompetitionsService: BigCompetitionsService,
    private route: ActivatedRoute,
    private deviceService: DeviceService,
    private routingState: RoutingState,
    private router: Router
  ) {
    super();
  }

  ngOnInit(): void {
    this.routeSubscriber = this.route.params.pipe(
      concatMap((param: Params) => {
        if (param.tab) {
          this.currentTab = param.tab;
          this.getSubTabs();
        } else if (this.tab) {
          this.currentTab = this.tab;
          this.getSubTabs();
        }

        return observableOf({});
      }))
      .subscribe();
  }

  ngOnDestroy(): void {
    this.loadDataSubscriber && this.loadDataSubscriber.unsubscribe();
    this.routeSubscriber && this.routeSubscriber.unsubscribe();
  }

  /**
   * Generates switchers config based on subtabs data.
   * @param {Array} subtabs
   * @return {Array}
   * @private
   */
  generateSwitchers(subtabs: ICompetitionSubTab[]): Array<ISwitcherConfig> {
    return _.map(subtabs, (tab: any) => {
      return {
        onClick: () => this.router.navigateByUrl(tab.path),
        viewByFilters: tab.uri,
        label: tab.name,
        name: tab.name,
        uri: tab.uri,
        url: tab.path
      };
    });
  }

  trackByIndex(index: number, item: IBCModule): string {
    return item.id;
  }

  /*
   * Set active subtab, and load modules list for subtabs.
   * @private
   */
  setActiveTab(): void {
    const subTab: string = this.routingState.getRouteParam('subTab', this.route.snapshot);
    const index: number = _.findIndex(this.switchers, (tab: ICompetitionTabs) => tab.uri === `/${subTab}`);

    if (!subTab) {
      this.filter = 0;
      this.subtabData && this.subtabData.length > 0 ? this.loadModules(this.subtabData[0].name) : this.loadModules();
    }
    else if (index === -1) {
      this.filter = 0;
      this.router.navigateByUrl((this.switchers[this.filter] && this.switchers[this.filter].url) || '/');
    } else {
      this.filter = index;
      this.loadModules();
    }
  }

  /**
   * Loads modules list for given tab or subtab.
   * @private
   */
  loadModules(subTabName?: string): void {
    this.loadDataSubscriber && this.loadDataSubscriber.unsubscribe();
    this.loadDataSubscriber = this.bigCompetitionsService.getModules(subTabName).pipe(
      finalize(() => {
        this.showLoader = false;
      }))
      .subscribe((data: IBCModule[]) => {
        this.modulesData = data.filter(mData => !this.bigCompetitionsService.gModules.includes(mData.type));
        this.isPromoUnavailable = this.isPromotionsEmpty(data);
        if (this.state.loading) { this.hideSpinner(); }
      }, () => {
        this.modulesData = [];
        this.showError();
      });
  }

  private isPromotionsEmpty(data: IBCModule[] = []): boolean {
    const isPromo = data.some(promo => promo.type === 'PROMOTIONS');
    const promotions = data.filter(promo => promo.promotionsData && promo.promotionsData.promotions.length > 0);
    return isPromo && promotions.length === 0;
  }
  getClass(): string {
    switch (true) {
      case this.currentTab === 'groups' && this.deviceService.isMobile:
        return 'grp-grid grp-grid-col'
      case this.currentTab === 'groups':
        return 'grp-grid'
      default:
        return '';
    }
  }

  private getSubTabs(): Subscription {
    this.showLoader = true;
    return this.bigCompetitionsService.getSubTabs()
      .subscribe((subtabData: ICompetitionSubTab[]) => {
        this.subtabData = subtabData;
        this.switchers = this.generateSwitchers(this.subtabData);

        if (this.subtabData.length) {
          this.setActiveTab();
        } else {
          this.loadModules();
        }
      }, () => {
        this.showLoader = false;
        this.showError();
      });
  }
}
