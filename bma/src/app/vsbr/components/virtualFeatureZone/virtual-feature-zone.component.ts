import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { Carousel } from '@shared/directives/ng-carousel/carousel.class';
import { VirtualHubService } from "@app/vsbr/services/virtual-hub.service";
import { IOffer } from '@core/models/aem-banners-section.model';
import { GtmService } from '@core/services/gtm/gtm.service';
import { IVirtualHomePageSystemConfig } from "@app/core/services/cms/models/system-config";

@Component({
    selector: 'virtual-feature-zone',
    templateUrl: './virtual-feature-zone.component.html',
    styleUrls: ['./virtual-feature-zone.component.scss']
})
export class VirtualFeatureZoneComponent {

    @Input() public featuredZoneOffers: IOffer[];
    @Input() public virtualHubSystemConfig: IVirtualHomePageSystemConfig;
    public carouselName: string = 'featuredZoneCarousel';
    public featureZoneTitle: string = 'Feature Zone';
    public featuredZoneBGImage: string;
    public featuredZoneFilteredOffers: IOffer[];
    public bgImageOffer: IOffer;

    /**
     * Constructor
     * @param windowRef : WindowRefService
     * @param router : Router
     * @param carouselService : CarouselService
     * @param virtualHubService : VirtualHubService
     * @param gtmService : GtmService
     */
    constructor(
        protected windowRef: WindowRefService,
        protected router: Router,
        protected carouselService: CarouselService,
        protected virtualHubService: VirtualHubService,
        protected gtmService: GtmService
    ) {
    }

    /**
     * OnInit
     */
    ngOnInit(): void {
        this.featuredZoneBGImage = this.getBGImageUrl();
        const featuredZoneAllOffers = this.featuredZoneOffers.filter(offer => offer.Id !== this.virtualHubSystemConfig.featureZoneBackgroundID);
        this.featuredZoneFilteredOffers = featuredZoneAllOffers.slice(0, 4);
    }

    /**
     * next click handler
     */
    nextSlide(): void {
        this.carousel.next();
    }

    /**
     * prev click handler
     */
    prevSlide(): void {
        this.carousel.previous();
    }

    /**
     * showNext getter
     */
    get showNext(): boolean {
        return this.carousel ? this.carousel.currentSlide < this.carousel.slidesCount - 1 : false;
    }

    /**
     * showNext setter
     */
    set showNext(value: boolean) { }

     /**
     * ngCarouselDisableRightSwipe getter
     */
    get ngCarouselDisableRightSwipe(): boolean {
        return this.carousel && ((this.carousel.currentSlide + 3) > this.carousel.slidesCount - 1);
    }

    /**
     * ngCarouselDisableRightSwipe setter
     */
    set ngCarouselDisableRightSwipe(value: boolean) { }

    /**
     * showPrev getter
     */
    get showPrev(): boolean {
        return this.carousel ? this.carousel.currentSlide > 0 : false;
    }

    /**
     * showPrev setter
     */
    set showPrev(value: boolean) { }

    /**
     * isOneCard getter
     */
    public get isOneCard(): boolean {
        return this.featuredZoneFilteredOffers && this.featuredZoneFilteredOffers.length === 1;
    }

    /**
     * isOneCard setter
     */
    public set isOneCard(value: boolean) { }

    /**
     * isValidCarousel getter
     */
    public get isValidCarousel(): boolean {
        return !!(this.featuredZoneFilteredOffers && this.featuredZoneFilteredOffers.length);
    }

    /**
     * isValidCarousel setter
     */
    public set isValidCarousel(value: boolean) { }

    /**
     * carousal getter
     */
    private get carousel(): Carousel {
        return this.carouselService.get(this.carouselName);
    }

    /**
     * carousel setter
     */
    private set carousel(value: Carousel) { }

    /**
     * Image click Handler
     * @param offer : Offer
     * @returns : void
     */
    public onImageClick(offer: IOffer): void {
        this.onFeatureClickGTMEvent(offer);
        const link: string = offer.link;
        const target: string = offer.target;
        if (!link) {
            return;
        }
        const isExternalLink: boolean = link.startsWith('http') || link.indexOf('#!?') > -1;
        if (isExternalLink) {
            this.windowRef.nativeWindow.open(link, target);
        } else {
            this.router.navigateByUrl(link);
        }
    }

    /**
     * gets background image url from sitecore offers
     * @returns : string
     */
    getBGImageUrl(): string {
        this.bgImageOffer = this.featuredZoneOffers.find(offer => offer.Id === this.virtualHubSystemConfig.featureZoneBackgroundID);
        const bgImageUrl: string = this.bgImageOffer ? this.bgImageOffer.imgUrl : null;
        return bgImageUrl;
    }

    /**
     * GTM tracking
     * @param imageInfo : sitecore image info
     */
    private onFeatureClickGTMEvent(imageInfo: IOffer): void {
        const gtmData = {
            event: 'Event.Tracking',
            'component.CategoryEvent': 'virtuals sports',
            'component.LabelEvent': 'feature zone',
            'component.ActionEvent': 'click',
            'component.PositionEvent': 'not applicable',
            'component.LocationEvent': 'feature zone',
            'component.EventDetails': imageInfo.itemName,
            'component.URLclicked': imageInfo.link,
        };
        this.gtmService.push(gtmData.event, gtmData);
    }

    /**
     * Ondestroy
    */
    ngOnDestroy(): void {
        this.carouselService.remove(this.carouselName);
    }

}