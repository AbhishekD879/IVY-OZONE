import { ChangeDetectorRef, Component, ComponentFactoryResolver } from '@angular/core';
import { Router } from '@angular/router';

import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { FanzoneSharedService } from '@app/lazy-modules/fanzone/services/fanzone-shared.service';

import { FanzonePreferenceCentreAppComponent } from '@app/fanzone/components/fanzonePreferenceCentre/fanzone-preference-centre.component';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';

@Component({
  selector: 'fanzone-preference-centre',
  templateUrl: '../../../../../app/fanzone/components/fanzonePreferenceCentre/fanzone-preference-centre.component.html',
  styleUrls: ['../../../../../app/fanzone/components/fanzonePreferenceCentre/fanzone-preference-centre.component.scss']
})
export class FanzonePreferenceCentreComponent extends FanzonePreferenceCentreAppComponent {

  constructor(
    public nativeBridge: NativeBridgeService,
    protected componentFactoryResolver: ComponentFactoryResolver,
    protected dialogService: DialogService,
    protected fanzoneSharedService: FanzoneSharedService,
    protected router: Router,
    protected fanzoneStorageService: FanzoneStorageService,
    protected pubsubService: PubSubService,
    protected cdRef: ChangeDetectorRef,
    protected windowRefService: WindowRefService,
    protected routingState: RoutingState
  ) {
    super(nativeBridge, componentFactoryResolver, dialogService, fanzoneSharedService, router, fanzoneStorageService, pubsubService, cdRef, windowRefService,routingState);
   }

}
