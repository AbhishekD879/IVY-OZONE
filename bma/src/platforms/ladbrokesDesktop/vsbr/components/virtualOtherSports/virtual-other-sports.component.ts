import { ChangeDetectorRef, Component } from "@angular/core";
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { VirtualOtherSports } from "@app/vsbr/components/virtualOtherSports/virtual-other-sports.component";
import { CarouselService } from "@app/shared/directives/ng-carousel/carousel.service";
import { Router } from "@angular/router";
import { VirtualHubService } from "@app/vsbr/services/virtual-hub.service";

@Component({
    selector: 'virtual-other-sports',
    templateUrl:'./../../../../coralDesktop/vsbr/components/virtualOtherSports/virtual-other-sports.component.html',
    styleUrls: ['./virtual-other-sports.component.scss']
})

export class DesktopVirtualOtherSports extends VirtualOtherSports {
    constructor(
         deviceService: DeviceService,
         windowRef: WindowRefService,
         carouselService: CarouselService,
         router: Router,
         virtualHubService: VirtualHubService,
         changeDetectorRef: ChangeDetectorRef
    ) {
        super(deviceService,windowRef,carouselService,router, virtualHubService,changeDetectorRef);
    }
}