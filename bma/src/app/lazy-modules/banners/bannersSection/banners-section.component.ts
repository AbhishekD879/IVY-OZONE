import { Component, ElementRef, Input, OnDestroy, OnInit, ChangeDetectorRef, AfterViewInit, ChangeDetectionStrategy } from '@angular/core';
import { catchError, finalize, first, map, switchMap } from 'rxjs/operators';
import { Observable, of, throwError } from 'rxjs';
import * as _ from 'underscore';

import { IAEMCarousel, ICMSBannerConfig, IOffer, IOfferReport, IParams } from '@core/models/aem-banners-section.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DeviceService } from '@core/services/device/device.service';
import { StorageService } from '@core/services/storage/storage.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import environment from '@environment/oxygenEnvConfig';
import { GtmService } from '@core/services/gtm/gtm.service';
import { UserService } from '@core/services/user/user.service';
import { IGtmBannerEvent } from '@core/models/gtm.event.model';
import { BannersService } from '@app/core/services/aemBanners/banners.service';
import { BRANDS_FOR_AEM, DEFAULT_OPTIONS, dynamicBannersPageMap } from '@core/services/aemBanners/utils';
import Utils from '@app/core/services/aemBanners/utils';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { Carousel } from '@shared/directives/ng-carousel/carousel.class';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { BannerClickService } from '@core/services/aemBanners/banner-click.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { Location } from '@angular/common';
import { LAZY_LOAD_ROUTE_PATHS } from '@bma/constants/lazyload-route-paths.constant';

@Component({
  selector: 'banners-section',
  templateUrl: 'banners-section.component.html',
  styleUrls: ['styles/banners-section.component.scss', 'styles/lc-carousel.scss'],
  providers: [ BannersService ],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BannersSectionComponent implements OnInit, OnDestroy, AfterViewInit {
  _pagevalue: string;
  offers: IOffer[];
  allOffers: IOffer[];
  brand: string = '';
  isBannerSectionEmpty: boolean = false;
  bannersVisibility: string = 'hidden';
  showBanners: boolean = true;
  carouselName: string = 'aem-banners-carousel';
  isBannersEnabled: boolean = false;
  firstImageLoaded: boolean = false;
  isLoaded: boolean = false;
  isSlided: boolean = false;
  eargerLoadCountMobile: number;
  eargerLoadCountDesktop: number;

  public timePerSlide: number = 7000;

  readonly SWIPER_RESET_TIMEOUT = 3;

  public activeSlideIndex: number = 0;

  public carousel: IAEMCarousel;

  public animatedPictureRegex: RegExp  = /(.+)\/(content)\/(.+)/;

  // GA Tracking properties
  private isGTMSuccess: boolean = false;

  private readonly ASPECT_RATIO: number = 2.67; // banner image aspect ratio = w:660 / h:247
  private readonly ASPECT_RATIO_MOBILE: number = 2.5; // banner image aspect ratio = w:375 / h:150
  private readonly PADDING: number = 8;
  private readonly DOTS_HEIGHT: number = 3;
  private readonly LIVE_ODDS_INTERVAL: number = 10000;

  private readonly DESKTOP_MARGIN_BOTTOM: number = 10; // taken from $componets-edge-gap in objects.banner.scss

  private orientationChangeListener: any;

  private cmsBannerConfig: ICMSBannerConfig;

  private element: HTMLElement;

  public imgWidth: string;

  private reloadTimer: number;
  @Input() set page(value: string) {
    this._pagevalue = value;
    this.getTeasersData();
  }
  get page() {
    return this._pagevalue;
  }

  constructor(
    private windowRef: WindowRefService,
    private pubsub: PubSubService,
    private deviceService: DeviceService,
    private storage: StorageService,
    private gtmService: GtmService,
    private userService: UserService,
    private bannerService: BannersService,
    private rendererService: RendererService,
    private carouselService: CarouselService,
    private cmsService: CmsService,
    private elementRef: ElementRef,
    private domTools: DomToolsService,
    private bannerClickService: BannerClickService,
    private changeDetectorRef: ChangeDetectorRef,
    private location: Location,
  ) {
    this.brand = Utils.resolveBrandOrDefault(environment.brand);
    this.element = this.elementRef.nativeElement;
    this.imgWidth = this.deviceService.isDesktop ? "720" : "480&q=70";
    this.handleReload = this.handleReload.bind(this);
  }

  ngOnInit(): void {
    this.windowRef.nativeWindow.setInterval(() => {
      this.getLaterUpdates();
    }, this.LIVE_ODDS_INTERVAL);
  }
    /*
  * Gets offers Odds immediatly after rendering banners
  * */
  ngAfterViewInit() {
    this.getLaterUpdates();
  }
    /*
  * Gets offers Odds for configured time interval
  * */
  getLaterUpdates() {
    if (this.allOffers && this.allOffers.length > 0) {
      this.offers = this.allOffers.map((offer: IOffer) => this.bannerService.getOdds(offer))
        .filter((offer: IOffer) => offer.bannerStatus === true);
    }
  }

  isIrishUser(): boolean {
    return this.userService.countryCode === 'IE' || this.storage.get('countryCode') === 'IE';
  }

  gotToSlide(index: number): void {
    this.bannersCarousel.toIndex(index);
  }
  applyConfigFromCMS(config: ICMSBannerConfig) {
    this.cmsBannerConfig = config;
    this.isBannersEnabled = this.cmsBannerConfig.enabled;
    if (!this.isBannersEnabled) {
      this.isBannersEnabled = false;
      this.domTools.css(this.element.parentNode.parentElement, 'contain-intrinsic-size', '0');
    }

    if (this.cmsBannerConfig.timePerSlide && this.cmsBannerConfig.timePerSlide > 0) {
      // convert seconds to milliseconds
      this.timePerSlide = this.cmsBannerConfig.timePerSlide * 1000;
    }
  }

  ngOnDestroy(): void {
    this.orientationChangeListener && this.orientationChangeListener();
    this.unsubscribeFromEvents();
    this.windowRef.nativeWindow.clearTimeout(this.reloadTimer);
    this.windowRef.nativeWindow.clearInterval(this.LIVE_ODDS_INTERVAL);
  }

  actionHandler($event: MouseEvent, offer: IOffer): void {
    $event.preventDefault();
    this.trackClickGTMEvent($event);
    this.bannerClickService.handleBannerClick($event, offer, false);
  }

  handleActiveSlide(slideIndex: number): void {
    if (!Number.isInteger(slideIndex)) {
      return;
    }
    if (!this.isSlided) {
      this.isSlided = true;
    }
    const i = slideIndex - 1;

    if (this.offers[i]) {
      this.offers[this.activeSlideIndex].active = false;
      this.offers[i].active = true;
      this.activeSlideIndex = i;
      this.changeDetectorRef.detectChanges();
    }
    this.trackBannerView();
  }

  resetSwiper(offers: IOffer[]): void {
    this.findGifsAndLoadInBackground(offers);
    this.allOffers = offers;
    this.offers = offers.filter((offer: IOffer)=> offer.bannerStatus === true);

    offers[0].active = true;
    //Adding fetch Priority to reduce LCP time
    offers[0].fetchpriority = 'high';
    (offers.length > 1) && (offers[1].fetchpriority = 'high');

    this.activeSlideIndex = 0;
    this.bannersVisibility = 'visible';
    this.trackBannerView();
  }

  findGifsAndLoadInBackground(offers: IOffer[]): void {
    offers.forEach((offer: IOffer) => {
      if (this.animatedPictureRegex.test(offer.imgUrl)) {
        // set plain image until gif will be loaded
        const originalGif = offer.imgUrl;
        const pictureBasedOnGif = originalGif.replace(this.animatedPictureRegex, '$1/image/$3');
        offer.imgUrl = pictureBasedOnGif;

        // load animated image in background..
        this.loadImageInBackgroundForOffer(offer, originalGif);
      }
    });
  }

  loadImageInBackgroundForOffer(offer: IOffer, originalGif: string): HTMLImageElement {
    const animatedImage = new Image();
    animatedImage.src = originalGif;
    animatedImage.onload = () => {
      offer.imgUrl = originalGif;
    };
    return animatedImage;
  }

  onFirstImageLoaded(): void {
    this.firstImageLoaded = true;
    this.unSetBannerSectionHeight();
  }

  removeSlideOnError(index: number): void {
    this.offers.splice(index, 1);
  }

  nextSlide(): void {
    this.bannersCarousel.next();
    this.sliderGTMTracker('right');
  }

  prevSlide(): void {
    this.bannersCarousel.previous();
    this.sliderGTMTracker('left');
  }
  /**
   * @param {string} imgUrl
   * @return {*}  {string}
   * @memberof BannersSectionComponent
   */
  addImageWidth(imgUrl: string): string {
    return (imgUrl.indexOf("w=") > -1) ? imgUrl : imgUrl + '?w=' + this.imgWidth;
  }

  public initPubSubAndSubscriptions(): void {
    this.pubsub.publish(this.pubsub.API.IS_BANNER_SECTION_AVAILABLE, [_.isEmpty(this.offers)]);

    this.pubsub.subscribe('dynamicBanners', this.pubsub.API.RELOAD_COMPONENTS, this.handleReload);
    this.isBannerSectionEmpty = _.isEmpty(this.offers);

    this.subscribeForEvents();
    this.changeDetectorRef.markForCheck();
  }

  public requestOffersAndCarouselInit(): Observable<any> {
    return this.bannerService
      .fetchOffersFromAEM(this.carousel.settings).pipe(
      map((response: IOfferReport) => {
        this.showBanners = (response.offers.length > 0);
        if (this.showBanners) {
          this.resetSwiper(response.offers);
          this.unSetBannerSectionHeight();
        } else {
          this.domTools.css(this.element, 'display', 'none');
          this.domTools.css(this.element, 'height', '0');
          this.domTools.css(this.element.parentNode.parentElement, 'contain-intrinsic-size', '0');
          this.domTools.css(this.element.parentNode.parentElement, 'min-height', '0');
        }
        this.changeDetectorRef.detectChanges();
      }),
      catchError(error => {
        this.unSetBannerSectionHeight();
        this.showBanners = false;
        return throwError(error);
      }), finalize(() => this.isLoaded = true));
  }

  public trackBannerView(): void {
    const activeOffer = this.offers[this.activeSlideIndex];

    if (!activeOffer.tracked) {
      this.gtmService.push('trackEvent', {
        eventCategory: 'banner',
        eventAction: 'view',
        eventLabel: activeOffer.itemName,
        personalised: activeOffer.personalised,
        location: this.windowRef.nativeWindow.location.pathname,
        vipLevel: this.userService.vipLevel || null,
        position: activeOffer.position
      });
      activeOffer.tracked = true;
    }
  }

  /**
   * AEM Banners GA tracking logic by collecting info about slide (offer) clicked
   * @param {MouseEvent} event
   */
  public trackClickGTMEvent(event: MouseEvent): void {
    if (!this.offers.length || this.isGTMSuccess) {
      return;
    }
    const banner = this.offers[this.activeSlideIndex];

    const vipLevel: string = this.userService.vipLevel || null;
    const gtmEvent: IGtmBannerEvent = {
      event: 'trackEvent',
      eventCategory: 'banner',
      eventAction: 'click',
      eventLabel: banner.itemName,
      personalised: banner.personalised,
      location: this.windowRef.nativeWindow.location.pathname,
      position: (banner.position ? banner.position : (this.activeSlideIndex + 1)),
      vipLevel: vipLevel
    };

    this.gtmService.push('aemBannerClick', gtmEvent);
    // Set true as we need to send GTM one time
    this.isGTMSuccess = true;
  }

  public trackByPosition(offer) {
    return offer.position;
  }

  /*
* Update dynamic banners with new properties
* @param {object} params
* */
  public updateDynamicBanners(): void {
    const options = {
      userType: this.getUserType()
    };

    const vipLevel = this.storage.get('vipLevel');
    if (vipLevel) {
      options['imsLevel'] = vipLevel;
    }

    this.carousel._options = Utils.assign({}, this.carousel._options, options);
    this.carousel.settings = Utils.assign({}, DEFAULT_OPTIONS, this.carousel._options);

    this.requestOffersAndCarouselInit().pipe(first()).subscribe(() => {}, () => {});
  }
  /**
   * Check if the current url is five-a-side
   * @returns {boolean}
   */
  public checkForFiveASideUrl(): boolean {
    const currentPath: string = this.location.path();
    return currentPath.includes(LAZY_LOAD_ROUTE_PATHS.fiveASideShowdown);
  }

  /*
  * Get user type
  * @return {string}
  * */
  private getUserType(): string {
    const user = this.storage.get('existingUser');
    if (!user) {
      return this.brand === BRANDS_FOR_AEM.ladbrokes ? 'new' : 'anonymous';
    } else {
      return this.userService.isRetailUser() ? this.userService.accountBusinessPhase : 'existing';
    }
  }

  /**
   * Set height for banner section to make fixed place for banner.
   */
  private setBannerSectionHeight() {
    /*
    Temporary setting the display to 'block' to be able to get element width;
     */
    this.domTools.css(this.element, 'display', 'block');

    const bannerSectionWidth = this.domTools.getWidth(this.element);
    const viewPortWidth = this.windowRef.nativeWindow.innerWidth;
    const desktopMode = viewPortWidth > 1099 && this.deviceService.isDesktop;
    const bannerSectionHeight = desktopMode
      ? (bannerSectionWidth / 100 * 60) / this.ASPECT_RATIO
      : bannerSectionWidth / this.ASPECT_RATIO_MOBILE + this.PADDING * 3 + this.DOTS_HEIGHT;

    const bannerSectionTemporaryHeight = !this.deviceService.isDesktop ?
        bannerSectionHeight : bannerSectionHeight + this.DESKTOP_MARGIN_BOTTOM;
    /*
    Temporary setting the height on banners load to prevent banners block leaping on UI.
     */
    this.domTools.css(this.element, 'height', `${(bannerSectionTemporaryHeight)}px`);
  }

  /**
   * Remove temporary styles for banner section
   */
  private unSetBannerSectionHeight() {
    /*
    Removing temporary display and height values to not broke banners and offers styles
     */
    this.domTools.css(this.element, 'display', '');
    this.domTools.css(this.element, 'height', '');
  }
  private getTeasersData(): void {
    this.cmsService.getSystemConfig()
      .pipe(switchMap((config: ISystemConfig) => {
        if (config && config.DynamicBanners) {
          this.applyConfigFromCMS(config.DynamicBanners);
        }
        if (config && config.EagerLoadImagesNumber) {
          this.eargerLoadCountDesktop = config.EagerLoadImagesNumber.SiteCoreBannerDesktop;
          this.eargerLoadCountMobile = config.EagerLoadImagesNumber.SiteCoreBannerMobile;
        }
        if (this.isBannersEnabled) {
          const _options = this.getBannerDynamicParams();
          const settings = Utils.assign({}, DEFAULT_OPTIONS, _options);
          this.carousel = {_options, settings};

          if (!this.firstImageLoaded) {
            this.setBannerSectionHeight();
          }
          this.initOrientationChangeListener();
          return this.requestOffersAndCarouselInit().pipe(finalize(() => {
            this.initPubSubAndSubscriptions();
          }), first());
        } else {
          return of({});
        }
      })).subscribe(() => {}, () => {});
  }
  private initOrientationChangeListener(): void {
    this.orientationChangeListener = this.rendererService.renderer.listen(
      this.windowRef.nativeWindow,
      'orientationchange',
      () => {
        this.showBanners = false;
        this.windowRef.nativeWindow.setTimeout(() => {
          this.showBanners = this.offers.length > 0;
          this.resetSwiper(this.offers.slice());
        }, this.SWIPER_RESET_TIMEOUT);
      }
    );
  }

  /**
   * Generates params needed for dynamic banner
   * @return {object}
   */
  private getBannerDynamicParams(): IParams {
    const baseParams: IParams = {
      locale: this.isIrishUser() && this.brand === BRANDS_FOR_AEM.ladbrokes ? 'en-ie' : 'en-gb',
      brand: this.brand,
      channel: this.getAppType(),
      userType: this.getUserType()
    };
    baseParams.page = dynamicBannersPageMap[this.page] ? dynamicBannersPageMap[this.page] : this.page;

    const vipLevel = this.storage.get('vipLevel');
    // This check is needed for requirement: if no vip level then do not send this key at all
    if (vipLevel) {
      baseParams.imsLevel = vipLevel;
    }

    if (this.deviceService.viewType !== 'desktop') {
      baseParams.device = 'mobile';
    }

    if (this.cmsBannerConfig.maxOffers && this.cmsBannerConfig.maxOffers > 0) {
      baseParams.maxOffers = this.cmsBannerConfig.maxOffers;
    }

    return baseParams;
  }

  /**
   * Subscribes for events (like login, logout) to rerender banner
   * @param {object} params
   */
  private subscribeForEvents(): void {
    this.pubsub.subscribe('dynamicBanners', this.pubsub.API.SESSION_LOGIN, () => {
      if (this.carousel) {
        this.showBanners = false;
        // Timeout added to get ngx-swiper-wrapper ready to update slides
        this.windowRef.nativeWindow.setTimeout(() => {
          this.updateDynamicBanners();
        }, this.SWIPER_RESET_TIMEOUT);
      }
    });
  }

  /**
   * Unsubscribe from events
   */
  private unsubscribeFromEvents(): void {
    this.pubsub.unsubscribe('dynamicBanners');
  }

  /*
  * Get application type
  * @return {string}
  * */
  private getAppType(): string {
    if (this.page === 'retail') {
      return 'connect'; // TODO: rename to retail after changes in cms.
    } else if (this.deviceService.isWrapper) {
      return 'app';
    } else if (this.deviceService.isMobile || this.deviceService.isTablet || this.deviceService.isMobileOrigin) {
      return 'mobile';
    } else if (this.deviceService.isDesktop) {
      return 'mobile';  // temporary added, until we will have 'desktop' channel
    }
    return '';
  }

  private get bannersCarousel(): Carousel {
    return this.carouselService.get(this.carouselName);
  }
  private set bannersCarousel(value:Carousel){}

  private handleReload(): void {
    this.windowRef.nativeWindow.clearTimeout(this.reloadTimer);
    this.reloadTimer = this.windowRef.nativeWindow.setTimeout(() => {
      this.ngOnDestroy();
      this.ngOnInit();
    }, DEFAULT_OPTIONS.atJsLoadingTimeout);
  }

  /**
  * AEM Banners GA tracking logic by collecting info about slide (offer) clicked on right and left button
  * @param {string} slideDirection
  */
  private trackSliderClickGTMEvent(slideDirection: string): void {
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'banner',
      'component.LabelEvent': 'virtuals',
      'component.ActionEvent': 'click',
      'component.PositionEvent': 'top banner',
      'component.LocationEvent': 'not applicable',
      'component.EventDetails': `navigate ${slideDirection}`,
      'component.URLclicked': 'not applicable',
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
   * GAtracking handler for sports on left and right slider
   * @param {string} slideDirection 
   */
  private sliderGTMTracker(slideDirection: string): void {
    if (this.page === 'virtuals') {
      this.trackSliderClickGTMEvent(slideDirection);
    }
  }
}
