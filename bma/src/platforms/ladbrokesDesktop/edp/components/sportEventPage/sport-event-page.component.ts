import { Component, HostListener, OnInit, ChangeDetectorRef } from '@angular/core';
import { Router, Event, NavigationEnd, ActivatedRoute } from '@angular/router';

import { SportEventPageComponent } from '@app/edp/components/sportEventPage/sport-event-page.component';
import { StorageService } from '@core/services/storage/storage.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { SportEventPageProviderService } from '@edp/components/sportEventPage/sport-event-page-provider.service';
import { FootballExtensionService } from '@edp/services/footballExtension/football-extension.service';
import { TennisExtensionService } from '@edp/services/tennisExtension/tennis-extension.service';

import { IMarket } from '@core/models/market.model';
import { Subscription } from 'rxjs';
import { TemplateService } from '@shared/services/template/template.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { CmsService } from '@app/core/services/cms/cms.service';
import { MarketsOptaLinksService } from '@edp/services/marketsOptaLinks/markets-opta-links.service';
import { IMarketLinks } from '@core/services/cms/models/edp-market.model';
import { RoutingState } from '@app/shared/services/routingState/routing-state.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { SeoDataService } from '@core/services/seoData/seo-data.service';
import { IsPropertyAvailableService } from '@sb/services/isPropertyAvailable/is-property-available.service';
import { CashOutLabelService } from '@core/services/cashOutLabel/cash-out-label.service';
import { SportEventPageService } from '@edp/services/sportEventPage/sport-event-page.service';

@Component({
  selector: 'sport-event-page',
  styleUrls: ['sport-event-page.component.scss'],
  templateUrl: './sport-event-page.component.html'
})
export class DesktopSportEventPageComponent extends SportEventPageComponent implements OnInit {
  minWidth: number;
  isOneColumn: boolean;
  columns: number[];
  marketsStorage: string;
  sportDataSubscription: Subscription;
  openedMarketTabsCountByDefault: number = 4;

  constructor(
    router: Router,
    activatedRoute: ActivatedRoute,
    sportEventPageProviderService: SportEventPageProviderService,
    templateService: TemplateService,
    footballExtension: FootballExtensionService,
    tennisExtension: TennisExtensionService,
    routingHelperService: RoutingHelperService,
    pubSubService: PubSubService,
    private storageService: StorageService,
    sportsConfigService: SportsConfigService,
    changeDetectorRef: ChangeDetectorRef,
    windowRefService: WindowRefService,
    cmsService: CmsService,
    routingState: RoutingState,
    marketsOptaLinksService: MarketsOptaLinksService,
    locale: LocaleService,
    seoDataService: SeoDataService,
    isPropertyAvailableService: IsPropertyAvailableService,
    cashOutLabelService: CashOutLabelService,
    sportEventPageService: SportEventPageService) {
    super(router, activatedRoute, sportEventPageProviderService, templateService, footballExtension, tennisExtension, routingHelperService,
      pubSubService, sportsConfigService, changeDetectorRef, windowRefService,
      cmsService, routingState, marketsOptaLinksService, locale, seoDataService, isPropertyAvailableService,
      cashOutLabelService, sportEventPageService);
  }

  /**
   * onWindowResize()
   */
  @HostListener('window:resize', [])
  onWindowResize(): void {
    this.updateColumnStatus();
  }

  /**
   * Initialize controller
   */
  ngOnInit(): void {
    this.minWidth = 1280; // Breakpoint Width
    this.isOneColumn = false; // Is One Column Needed
    this.columns = [1, 2]; // Markets Columns quantity
    this.marketsStorage = 'marketsStorage'; // Markets Accordion State Storage
    this.removeStorage();
    this.updateColumnStatus();
    this.marketsOptaLinksService.getMarketLinks().subscribe(
            (links: IMarketLinks[]) => this.replaySubj.next(links));
    this.sportDataSubscription = this.sportEventPageProviderService.sportData
      .subscribe(this.sportDataHandler, () => this.showError());
    this.routeChangeListener = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd && this.isSameEvent()) {
        const previousMarketName = this.marketName;
        this.marketName = this.activatedRoute.snapshot.paramMap.get('market');
        this.init();
        this.recalculateExpandedMarkets(null, previousMarketName !== this.marketName);
        this.removeStorage();
      }
    });
  }

  /**
   * Hide market based on column index
   * @param {Number} index
   * @param {Number} column
   * @returns {Boolean}
   */
  isHidden(index: number, column: number): boolean {
    const isEven = ((index + 1) % 2) === 1; // Is Even Market
    return this.isOneColumn ? column === 0 : (column === 0 && isEven) || (column === 1 && !isEven);
  }

  /**
   * Get accordion name to set into marketsStorage
   * @param {IMarket} market
   * @param {Number} index
   * @param {Boolean} isChild
   * @returns {String}
   */
  getMemoryId(index: string, market: IMarket, isChild?: boolean): string {
    const isMarket = isChild ? true : !(market.marketsGroup || market.viewType === 'Correct Score');
    return isMarket ? `${market.name}-${index}` : '';
  }

  /**
   * Remove Markets Accordion State Storage
   */
  private removeStorage(): void {
    this.storageService.remove(`accordion_${this.marketsStorage}`);
  }

  /**
   * Update Column status
   */
  private updateColumnStatus(): void {
    const isBreakPoint = window.innerWidth < this.minWidth;
    if (isBreakPoint && !this.isOneColumn) {
      this.isOneColumn = true;
    } else if (!isBreakPoint && this.isOneColumn) {
      this.isOneColumn = false;
    }
  }

  /**
   * Checks if event id in urls is the same as stored event id.
   * @return {boolean}
   */
  private isSameEvent(): boolean {
    const eventId = this.activatedRoute.snapshot.paramMap.get('id');

    return !!this.eventEntity && Number(eventId) === Number(this.eventEntity.id);
  }
}

