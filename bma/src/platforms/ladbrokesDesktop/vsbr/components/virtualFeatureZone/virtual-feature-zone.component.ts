import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { VirtualHubService } from "@app/vsbr/services/virtual-hub.service";
import { GtmService } from '@core/services/gtm/gtm.service';
import { VirtualFeatureZoneComponent } from '@app/vsbr/components/virtualFeatureZone/virtual-feature-zone.component';

@Component({
    selector: 'virtual-feature-zone',
    templateUrl: './virtual-feature-zone.component.html',
    styleUrls: ['./virtual-feature-zone.component.scss']
})
export class DesktopVirtualFeatureZoneComponent extends VirtualFeatureZoneComponent {

    constructor(
        protected windowRef: WindowRefService,
        protected router: Router,
        protected carouselService: CarouselService,
        protected virtualHubService: VirtualHubService,
        protected gtmService: GtmService
    ) {
        super(windowRef, router, carouselService, virtualHubService, gtmService);
    }

}