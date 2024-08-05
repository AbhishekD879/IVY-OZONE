import { Component, ChangeDetectionStrategy, ChangeDetectorRef, ComponentFactoryResolver } from '@angular/core';
import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { WsUpdateEventService } from '@core/services/wsUpdateEvent/ws-update-event.service';
import { TemplateService } from '@app/shared/services/template/template.service';
import { CommentsService } from '@app/core/services/comments/comments.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { ActivatedRoute, Router } from '@angular/router';
import { FanzoneAppModuleService } from '@app/fanzone/services/fanzone-module.service';
import { FanzoneAppHomeComponent } from '@app/fanzone/components/fanzoneHome/fanzone-home.component';
import { FanzoneHelperService } from '@app/core/services/fanzone/fanzone-helper.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { FanzoneSharedService } from '@app/lazy-modules/fanzone/services/fanzone-shared.service';
import { DeviceService } from '@frontend/vanilla/core';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';
import { UserService } from '@core/services/user/user.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { FanzoneGamesService } from '@app/fanzone/services/fanzone-games.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { StorageService } from '@app/core/services/storage/storage.service';

@Component({
  selector: 'fanzone-home',
  templateUrl: './fanzone-home.component.html',
  styleUrls: ['../../../../../app/fanzone/components/fanzoneHome/fanzone-home.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FanzoneHomeComponent extends FanzoneAppHomeComponent {

  constructor(
    protected cms: CmsService,
    protected navigationService: NavigationService,
    protected dynamicComponentLoader: DynamicLoaderService,
    public routingState: RoutingState,
    protected fanzoneModuleService: FanzoneAppModuleService,
    protected pubsub: PubSubService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected wsUpdateEventService: WsUpdateEventService,
    protected templateService: TemplateService,
    protected commentsService: CommentsService,
    protected routingHelperService: RoutingHelperService,
    protected router: Router,
    protected route: ActivatedRoute,
    protected fanzoneStorageService: FanzoneStorageService,
    protected fanzoneHelperService: FanzoneHelperService,
    protected fanzoneSharedService: FanzoneSharedService,
    protected gtmService: GtmService,
    protected device: DeviceService,
    protected user: UserService,
    protected bonusSuppression: BonusSuppressionService,
    protected dialogService: DialogService,
    protected componentFactoryResolver: ComponentFactoryResolver,
    protected fanzoneGamesService: FanzoneGamesService,
    protected windowRefService: WindowRefService,
    protected storageService: StorageService,
) {
    super(cms, navigationService, dynamicComponentLoader, routingState, fanzoneModuleService,
      pubsub, changeDetectorRef, wsUpdateEventService, templateService, commentsService, router, route, fanzoneStorageService, fanzoneHelperService, fanzoneSharedService, gtmService, device, user, bonusSuppression, dialogService, componentFactoryResolver, fanzoneGamesService,windowRefService, storageService);
  }
}
