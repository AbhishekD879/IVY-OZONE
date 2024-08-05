import {
    Component,
    Input,
    OnInit
} from '@angular/core';
import { Router } from '@angular/router';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { VanillaApiService } from '@frontend/vanilla/core';
import { UserService } from '@app/core/services/user/user.service';
import { ISportConfigTab } from '@app/core/services/cms/models';
import { DeviceService } from '@app/core/services/device/device.service';
import { IOfferReport, IOffer } from "@root/app/core/models/aem-banners-section.model";
import { VirtualHubService } from "@app/vsbr/services/virtual-hub.service";
import { GtmService } from '@core/services/gtm/gtm.service';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';
import { CmsService } from '@core/services/cms/cms.service';
import { ISystemConfig } from '@app/core/services/cms/models';

@Component({
    selector: 'virtual-entry-point-banner',
    templateUrl: './virtual-entry-point-banner.component.html',
    styleUrls: ['./virtual-entry-point-banner.component.scss'],
})

export class VirtualEntryPointBannerComponent implements OnInit {
    @Input() targetTab: ISportConfigTab;
    @Input() eventsBySections?: ITypeSegment[] | any = [];
    @Input() index?: number;
    @Input() isUnTiedSport?: boolean;
    @Input() sportName?: string = 'football';
    @Input() currentLocation?: string = 'event details page';
    public entryPointBanners: IOfferReport;
    public selectedVirtualBanner: any = {
        imgUrl: '',
        altText: ''
    }
    isDisplayed: boolean = false;

    /**
     * Constructor
     */
    constructor(
        protected windowRef: WindowRefService,
        protected router: Router,
        protected vanillaApiService: VanillaApiService,
        public user: UserService,
        protected deviceService: DeviceService,
        protected virtualHubService: VirtualHubService,
        protected gtmService: GtmService,
        protected vEPService: VirtualEntryPointsService,
        protected cmsService: CmsService
    ) {
    }

    /**
     * OnInit
     */
    ngOnInit(): void {
        this.cmsService.getSystemConfig().subscribe((sysConfig: ISystemConfig) => {
            if (sysConfig && sysConfig.VirtualEntryPointConfig && sysConfig.VirtualEntryPointConfig.enabled) {
                if (this.isUnTiedSport) {
                    this.vEPService.targetTab.subscribe((value: ISportConfigTab | null) => {
                        this.targetTab = value;
                    });
                }
                if (this.targetTab?.interstitialBanners?.bannerEnabled) {
                    this.loadSiteCoreImageConfig();
                }
            }
        });
    }


    /**
     * Gets sitecore images for sport entry point banners
     */
    private loadSiteCoreImageConfig(): void {
        const page = 'EntryPointBanners';
        if (!this.virtualHubService.entryPointSiteCoreOffers?.offers?.length) { 
            this.virtualHubService.getSiteCoreImages(page).subscribe((siteCoreOffers) => {
                if (siteCoreOffers) {
                    this.entryPointBanners = siteCoreOffers;
                    this.virtualHubService.entryPointSiteCoreOffers = siteCoreOffers;
                    this.getBannerImageUrl();
                }
            });
        } else {
            this.entryPointBanners = this.virtualHubService.entryPointSiteCoreOffers;
            this.getBannerImageUrl();
        }
       
    }

    /**
     * Finds cms configured image from sitecore image list
     */
    private getBannerImageUrl(): void {
        let imageOffer: IOffer;
        if (this.deviceService.isDesktop) {
            imageOffer = this.entryPointBanners.offers.find(offer => offer.Id === this.targetTab?.interstitialBanners?.desktopBannerId);
        } else {
            imageOffer = this.entryPointBanners.offers.find(offer => offer.Id === this.targetTab?.interstitialBanners?.mobileBannerId);
        }
        this.selectedVirtualBanner = imageOffer;

        // GAtracking
        if((this.isUnTiedSport 
            || ((!this.isUnTiedSport && this.isBannerPositionEnabled(this.index)) && (this.index != -1)))
            && this.targetTab?.interstitialBanners?.bannerEnabled 
            && this.selectedVirtualBanner?.imgUrl){
            this.onBannerLoadGTMEvent();
        }
    }

    /**
     * Event Handler for entry point button click
     * @param offer : sitecore image offer
     * @param targetTabConfig : sport tab configuration
     * @returns void
     */
    public onCtaButtonClick(offer: IOffer, targetTabConfig: ISportConfigTab): void {
        this.onCTABtnClickGTMEvent();
        this.onClickRedirect(offer, targetTabConfig);
    }

    public onBannerClick(offer: IOffer, targetTabConfig: ISportConfigTab) {
        if (!targetTabConfig?.interstitialBanners?.ctaButtonLabel) {
            this.onBannerClickGTMEvent();
            this.onClickRedirect(offer, targetTabConfig);
        }
    }

    private onClickRedirect(offer: IOffer, targetTabConfig: ISportConfigTab) {
        const link: string = targetTabConfig?.interstitialBanners?.redirectionUrl;
        const target: string = offer?.target;
        if (!link) {
            return;
        }

        const isExternalLink: boolean = link.startsWith('http') || target === '_blank' || link.indexOf('#!?') > -1;
        if (isExternalLink) {
            this.windowRef.nativeWindow.open(link, target);
        } else {
            this.router.navigateByUrl(link);
        }
    }

    /**
     * Checks if the banner is enabled for the accordion
     * @param index : index of the accordian item
     * @returns : boolean
     */
    isBannerPositionEnabled(index: number): boolean {
        const isBannerEnabled: boolean = false;
        const lastItem = this.eventsBySections?.filter(eventbySection => !eventbySection.deactivated)?.length;
        if (Number(this.targetTab?.interstitialBanners?.bannerPosition) === Number(index)) {
            return true;
        }

        if (lastItem === index && (Number(this.targetTab?.interstitialBanners?.bannerPosition) >= lastItem)) {
            return true;
        }
        if (index == -1) {
            return true;
        }

        return isBannerEnabled;
    }


    private onCTABtnClickGTMEvent(): void {
        const gtmData = {
            event: 'Event.Tracking',
            'component.CategoryEvent': 'banner',
            'component.LabelEvent': 'virtual sports',
            'component.ActionEvent': 'click',
            'component.PositionEvent': `${this.sportName} virtual banner`,
            'component.LocationEvent': this.currentLocation,
            'component.EventDetails': `${this.targetTab?.interstitialBanners?.ctaButtonLabel} cta`,
            'component.URLclicked': `${this.targetTab?.interstitialBanners?.redirectionUrl}`,
        };
        this.gtmService.push(gtmData.event, gtmData);
    }

    private onBannerClickGTMEvent(): void {
        const gtmData = {
            event: 'Event.Tracking',
            'component.CategoryEvent': 'banner',
            'component.LabelEvent': 'virtual sports',
            'component.ActionEvent': 'click',
            'component.PositionEvent': `${this.sportName} virtual banner`,
            'component.LocationEvent': this.currentLocation,
            'component.EventDetails': 'banner click',
            'component.URLclicked': `${this.targetTab?.interstitialBanners?.redirectionUrl}`
        };
        this.gtmService.push(gtmData.event, gtmData);
    }

    private onBannerLoadGTMEvent(): void {
        const gtmData = {
            event: 'contentView',
            'component.CategoryEvent': 'banner',
            'component.LabelEvent': 'virtual sports',
            'component.ActionEvent': 'load',
            'component.PositionEvent': `${this.sportName} virtual banner`,
            'component.LocationEvent': this.currentLocation,
            'component.EventDetails': `${this.sportName} virtual banner`,
            'component.URLclicked': 'not applicable',
        };
        this.gtmService.push(gtmData.event, gtmData);
    }

    public isDisplay() {
        this.isDisplayed = true;
    }

}
