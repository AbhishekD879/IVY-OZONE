import { Component, ChangeDetectorRef, OnDestroy, ChangeDetectionStrategy } from '@angular/core';
import { FeaturedModuleComponent } from '@featured/components/featured-module/featured-module.component';

import { IFeaturedModel } from '@featured/models/featured.model';
import { IOutputModule } from '@featured/models/output-module.model';

import { Router } from '@angular/router';
import { LocaleService } from '@core/services/locale/locale.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { FeaturedModuleService } from '@featured/services/featuredModule/featured-module.service';
import { TemplateService } from '@shared/services/template/template.service';
import { CommentsService } from '@core/services/comments/comments.service';
import { WsUpdateEventService } from '@core/services/wsUpdateEvent/ws-update-event.service';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { PromotionsService } from '@promotions/services/promotions/promotions.service';
import { GermanSupportFeaturedService } from '@ladbrokesMobile/core/services/germanSupportFeatured/german-support-featured.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { UserService } from '@core/services/user/user.service';
import { EventService } from '@app/sb/services/event/event.service';
import { VirtualSharedService } from '@shared/services/virtual/virtual-shared.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { FreeRideHelperService } from '@lazy-modules/freeRideHelper/freeRideHelper.service';
import { VanillaApiService } from '@frontend/vanilla/core';
import { Location } from '@angular/common';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { StorageService } from '@app/core/services/storage/storage.service';

@Component({
  selector: 'featured-module',
  styleUrls: ['./featured-module.component.scss'],
  templateUrl: './featured-module.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class LadbrokesFeaturedModuleComponent extends FeaturedModuleComponent implements OnDestroy {

  private ctrlName: string = 'LadbrokesFeaturedModuleComponent';
  isFanzoneEnabled = true;


  constructor(
    protected locale: LocaleService,
    protected filtersService: FiltersService,
    protected windowRef: WindowRefService,
    protected pubsub: PubSubService,
    protected featuredModuleService: FeaturedModuleService,
    protected templateService: TemplateService,
    protected commentsService: CommentsService,
    protected wsUpdateEventService: WsUpdateEventService,
    protected sportEventHelper: SportEventHelperService,
    protected cmsService: CmsService,
    protected promotionsService: PromotionsService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected germanSupportFeaturedService: GermanSupportFeaturedService,
    protected routingHelperService: RoutingHelperService,
    public router: Router,
    public gtmService: GtmService,
    protected awsService: AWSFirehoseService,
    public user: UserService,
    public eventService: EventService,
    protected virtualSharedService: VirtualSharedService,
    protected vanillaApiService: VanillaApiService,
    protected location: Location,
    public freeRideHelperService: FreeRideHelperService,
    protected bonusSuppressionService: BonusSuppressionService,
    protected deviceService: DeviceService,
    protected storage: StorageService
  ) {
    super(
      locale,
      filtersService,
      windowRef,
      pubsub,
      featuredModuleService,
      templateService,
      commentsService,
      wsUpdateEventService,
      sportEventHelper,
      cmsService,
      promotionsService,
      changeDetectorRef,
      routingHelperService,
      router,
      gtmService,
      awsService,
      user,
      eventService,
      virtualSharedService,
      bonusSuppressionService,
      deviceService,
      storage
    );

    this.onSocketUpdate = (module: IOutputModule) => {
      if (this.germanSupportFeaturedService.isGermanUser()) {
        module = this.germanSupportFeaturedService.moduleFilterHandler(module);
      }
      super.featureTabOnSocketUpdate(module);
    };

    this.pubsub.subscribe(this.ctrlName, this.pubsub.API.SESSION_LOGIN, () => {
      /*
      Assuming that data has been already received from init call else they will be filtered anyway in init call!
       */
      const featured: IFeaturedModel = this.germanSupportFeaturedService.getActualData();
      this.changeDetectorRef.markForCheck();
      if (featured) {
        super.init(featured);
      }
    });
  }

  /**
   * to check if on home page
   * @return {Boolean}
   */
  checkIfHomeUrl(): boolean {
    const currentPath: string = this.location.path();
    return currentPath === '' || currentPath.indexOf('/home/') > -1 || currentPath.indexOf('utm_source=PWA') > -1 ||
      currentPath.startsWith('?');
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe(this.ctrlName);
    super.ngOnDestroy();
  }

  init(featured: IFeaturedModel): void {
    super.init(this.germanSupportFeaturedService.getInitialData(featured));
  }
}
