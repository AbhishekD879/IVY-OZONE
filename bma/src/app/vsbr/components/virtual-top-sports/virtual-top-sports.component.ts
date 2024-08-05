import { Component, Input, OnInit } from "@angular/core";
import { IVirtualSportsHomePage } from '@app/core/services/cms/models/virtual-sports.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { Router } from '@angular/router';
import { VirtualHubService } from "@app/vsbr/services/virtual-hub.service";
import { DeviceService } from '@core/services/device/device.service';

@Component({
    selector: 'virtual-top-sports',
    templateUrl: './virtual-top-sports.component.html',
    styleUrls: ['./virtual-top-sports.component.scss']
})

export class VirtualTopSportsComponent implements OnInit {

    @Input() public topSportsImages: IVirtualSportsHomePage[] = [];
    @Input() public virtualsLiveCount: any;
    @Input() public topSportsBGImage: string;
    public topSportsTitle: string = 'Top Sports';

    /**
     * Constructor
     * @param router : Router
     * @param windowRef : WindowRef
    */
    constructor(
        private router: Router,
        private windowRef: WindowRefService,
        private virtualHubService: VirtualHubService,
        protected deviceService: DeviceService
    ) {
    }

    /**
     * OnInit
     */
    ngOnInit(): void {
    }

    /**
     * on Image redirection Handler
     * @param imageInfo : virtualHomePage Info
     */
    goToVirtualSports(imageInfo: IVirtualSportsHomePage): void {
        if (imageInfo && imageInfo.redirectionURL) {
            this.virtualHubService.onClickNavigationDetails.id = 'top sports';
            this.virtualHubService.onClickNavigationDetails.sportInfo = imageInfo;
            const isExternalLink = imageInfo.redirectionURL.startsWith('http') || imageInfo.redirectionURL.indexOf('#!?') > -1;
            if (isExternalLink) {
                this.windowRef.nativeWindow.open(imageInfo.redirectionURL, '_self');
            } else {
                this.router.navigateByUrl(imageInfo.redirectionURL);
            }
        }
    }


    /**
     * parallex on scroll
     * @param event : mouse event
     */
    onScroll(event: Event): void {
        const scrollPosition = (event.target as HTMLElement).scrollLeft;
        const main: any = document.querySelector('.carousal-container');
        main.style.backgroundPosition = `-${scrollPosition * 1.5}px 0px`;
    }

}