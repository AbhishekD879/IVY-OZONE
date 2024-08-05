import { Component, ChangeDetectorRef, ChangeDetectionStrategy } from '@angular/core';
import * as _ from 'underscore';
import { Router } from '@angular/router';

import { IOutputModule } from '@featured/models/output-module.model';
import { IFeaturedModel } from '@featured/models/featured.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { TemplateService } from '@shared/services/template/template.service';
import { FeaturedModuleService } from '@featured/services/featuredModule/featured-module.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CommentsService } from '@core/services/comments/comments.service';
import { WsUpdateEventService } from '@core/services/wsUpdateEvent/ws-update-event.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';

import { PromotionsService } from '@promotions/services/promotions/promotions.service';
import { GermanSupportFeaturedService } from '@ladbrokesMobile/core/services/germanSupportFeatured/german-support-featured.service';
import { LadbrokesFeaturedModuleComponent } from '@ladbrokesMobile/featured/components/featured-module/featured-module.component';
import { UserService } from '@core/services/user/user.service';
import { EventService } from '@app/sb/services/event/event.service';
import { VirtualSharedService } from '@shared/services/virtual/virtual-shared.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { VanillaApiService } from '@frontend/vanilla/core';
import { Location } from '@angular/common';
import { FreeRideHelperService } from '@lazy-modules/freeRideHelper/freeRideHelper.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { StorageService } from '@app/core/services/storage/storage.service';


@Component({
  selector: 'featured-module',
  styleUrls: ['featured-module.component.scss'],
  templateUrl: './featured-module.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DesktopFeaturedModuleComponent extends LadbrokesFeaturedModuleComponent {
  gtmDataLayer: {} = {};
  sbCount: number;
  isHcAvailable: boolean;

  constructor(
    locale: LocaleService,
    filtersService: FiltersService,
    windowRef: WindowRefService,
    pubsub: PubSubService,
    featuredModuleService: FeaturedModuleService,
    templateService: TemplateService,
    commentsService: CommentsService,
    wsUpdateEventService: WsUpdateEventService,
    sportEventHelper: SportEventHelperService,
    cmsService: CmsService,
    promotionsService: PromotionsService,
    changeDetectorRef: ChangeDetectorRef,
    routingHelperService: RoutingHelperService,
    germanSupportFeaturedService: GermanSupportFeaturedService,
    router: Router,
    gtmService: GtmService,
    awsService: AWSFirehoseService,
    user: UserService,
    eventService: EventService,
    virtualSharedService: VirtualSharedService,
    vanillaApiService: VanillaApiService,
    location: Location,
    freeRideHelperService: FreeRideHelperService,
    protected bonusSuppressionService: BonusSuppressionService,
    protected deviceService: DeviceService,
    protected storage: StorageService
  ) {
    super(locale, filtersService, windowRef, pubsub, featuredModuleService, templateService, commentsService,
      wsUpdateEventService, sportEventHelper, cmsService, promotionsService, changeDetectorRef, germanSupportFeaturedService,
      routingHelperService, router, gtmService, awsService, user, eventService, virtualSharedService, vanillaApiService, location, freeRideHelperService,
      bonusSuppressionService, deviceService, storage);
  }

  /**
   * Function is responsible for initialization of featuredModule
   *
   * @param {IFeaturedModel} featured
   */
  init(featured: IFeaturedModel): void {
    if (featured === null) { return; }
    featured.modules = this.filterModules(featured.modules);
    this.gtmDataLayer = {
      eventAction: 'featured events',
      eventLabel: 'additional markets'
    };
    super.init(featured);
    const modules = _.filter(featured.modules, (module: IOutputModule) => {
      return (!this.isSurfaceBetModule(module) && module['@type'] !== 'HighlightCarouselModule')
       || (this.isSurfaceBetModule(module) && module.data.length>0) 
       || (module['@type'] === 'HighlightCarouselModule' && module.displayOnDesktop);
    });
    this.isModuleAvailable = this.isFeaturedModuleAvailable && modules.length>0;
  }

  /**
   * Check if accordion header should be hidden
   * @param module
   * @returns {boolean}
   */
  isHeaderHidden(module: IOutputModule): boolean {
    return this.isFeaturedOffer(module);
  }

  /**
   * Check if accordion should be expanded
   * @param module
   * @returns {Boolean}
   */
  isExpanded(module: IOutputModule): boolean {
    const isExpanded = module.showExpanded || this.isFeaturedOffer(module);
    if (isExpanded) {
      this.manageSocketSubscription(module, isExpanded);
    }
    return isExpanded;
  }

  /**
   * Send tracking data on show more click
   */
  sendToGTM(): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'home',
      eventAction: 'featured events',
      eventLabel: 'view all'
    });
  }

  /**
   * Operations on module update receiving
   * @param {Object} module
   */
  onModuleUpdate(module: IOutputModule): void {
    if (this.isSurfaceBetModule(module)) {
      (module.data as ISportEvent[]) = this.filterDesktopSurfaceBets(module);
      this.sbCount = module.data.length;
    } else {
      (module.data as ISportEvent[]) = this.removeInPlayEvents(module);
    }
    super.onModuleUpdate(module);
  }

  /**
   * Check if event is featured offer
   * @param module
   * @returns {boolean|string}
   */
  private isFeaturedOffer(module: IOutputModule): boolean {
    return module.isSpecial || module.isEnhanced;
  }

  /**
   * Filtering InPlay events
   * @param module
   * @return {Array}
   */
  private removeInPlayEvents(module: IOutputModule): ISportEvent[] {
    return _.filter(module.data, event => !event.eventIsLive);
  }

  /**
   * Excluded from desktop version modules
   * @param module
   */
  private isExcludedModule(module: IOutputModule) {
    const isMarketModule = (module.dataSelection && module.dataSelection.selectionType === 'Market');
    const isEventIdModule = (module.dataSelection && module.dataSelection.selectionType === 'Event');

    return isMarketModule || isEventIdModule;
  }

  /**
   * Filtering modules with InPlay events and Outright/WinOrEachWay MarketsModules
   * @param modules
   * @return {Object} filtered modules
   */
  private filterModules(modules: IOutputModule[]): IOutputModule[] {
    this.isHcAvailable = false;
    this.sbCount = 0;
    return _.filter(modules, (module: IOutputModule) => {
      if (this.isSurfaceBetModule(module)) {
        (module.data as ISportEvent[]) = this.filterDesktopSurfaceBets(module);
        this.sbCount = module.data.length;
      } else if (module['@type'] === 'HighlightCarouselModule') {
        if (module.displayOnDesktop) {
          this.isHcAvailable = true;
          return true;
        }
      } else {
        (module.data as ISportEvent[]) = this.removeInPlayEvents(module);
      }
      return (this.isEventsModule(module) && module.hasNoLiveEvents && !this.isExcludedModule(module)) || this.isSurfaceBetModule(module);
    });
  }
  /**
   * Check if module type is - EventsModule
   */
  private isEventsModule(module: IOutputModule): boolean {
    return module['@type'] === 'EventsModule';
  }
  /**
   * Check if module type is - SurfaceBetModule
   */
  private isSurfaceBetModule(module: IOutputModule): boolean {
    return module['@type'] === 'SurfaceBetModule';
  }
  /**
   * Filtering desktop surface bets
   * @param module
   * @return {Array}
   */
  private filterDesktopSurfaceBets(module: IOutputModule): ISportEvent[] {
    return module.data.filter(surfaceBet => surfaceBet.displayOnDesktop);
  }
}
