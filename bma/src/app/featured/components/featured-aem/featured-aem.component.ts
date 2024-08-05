import { Component, OnInit, Input, OnDestroy, OnChanges, SimpleChanges, ChangeDetectionStrategy } from '@angular/core';

import environment from '@environment/oxygenEnvConfig';

import * as _ from 'underscore';

import { IGtmBannerEvent } from '@core/models/gtm.event.model';
import { IFeaturedAemSlideModel, IFeaturedAemModuleModel, ITermsAndConditions } from '../../models/featured-eam-module.model';

import { StorageService } from '@core/services/storage/storage.service';
import { DeviceService } from '@core/services/device/device.service';
import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { BannerClickService } from '@core/services/aemBanners/banner-click.service';

@Component({
  selector: 'featured-aem',
  templateUrl: './featured-aem.component.html',
  styleUrls: ['./featured-aem.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FeaturedAemComponent implements OnInit, OnDestroy, OnChanges {

  @Input() aem: IFeaturedAemModuleModel;

  slides: IFeaturedAemSlideModel[];
  termsAndConditions: ITermsAndConditions;

  private COMPONENT: string = 'featuredAem';

  private USER_TYPES = {
    ANONYMOUS: 'anonymous',
    EXISTING: 'existing',
    MULTI_CHANNEL: 'multi-channel',
    BOTH: 'both',
    IN_SHOP: 'in-shop',
    NEW: 'new'
  };

  private CHANNELS = {
    APP: 'app',
    DESKTOP: 'desktop',
    MOBILE: 'mobile'
  };

  constructor(
    private pubsub: PubSubService,
    private user: UserService,
    private deviceService: DeviceService,
    private storage: StorageService,
    private carouselService: CarouselService,
    private gtmService: GtmService,
    private windowRef: WindowRefService,
    private bannerClickService: BannerClickService
  ) { }

  ngOnInit(): void {
    this.termsAndConditions  = {
      showTC: false,
      text: undefined,
      href: undefined,
    };
    this.slides = this.filterSlides();
    this.termsAndConditions = this.getTermsAndConditions(1);
    this.pubsub.subscribe(`${this.COMPONENT}_${this.aem._id}`,
      [this.pubsub.API.SESSION_LOGIN, this.pubsub.API.SESSION_LOGOUT], () => {
        this.slides = this.filterSlides();
        this.termsAndConditions = this.getTermsAndConditions(1);
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.aem && changes.aem.previousValue) {
      this.slides = this.filterSlides();
    }
  }

  getTermsAndConditions(slideIndex: number): ITermsAndConditions {
    const slide = this.slides[slideIndex - 1];
    if (slide) {
      return {
        showTC: Boolean(slide.webTandC),
        text: slide.webTandC,
        href: slide.mobTandCLink
      };
    }
  }

  ngOnDestroy(): void {
    this.carouselService.remove(this.aem._id);
    this.pubsub.unsubscribe(`${this.COMPONENT}_${this.aem._id}`);
  }

  trackBySlide(slide: IFeaturedAemSlideModel): string {
    return `${slide.offerName}${slide.displayOrder}`;
  }

  handleClick($event: MouseEvent, slide: IFeaturedAemSlideModel): void {
    $event.preventDefault();
    this.trackClickGTMEvent(slide);
    this.bannerClickService.handleFeaturedAemSlideClick(slide.appUrl, slide.appTarget);
  }

  handleActiveSlide(slideIndex: number): void {
    if (Number.isInteger(slideIndex) && this.slides[slideIndex - 1]) {
      this.termsAndConditions = this.getTermsAndConditions(slideIndex);
      this.trackClickGTMEvent(this.slides[slideIndex - 1], 'view');
    }
  }

  private filterSlides(): IFeaturedAemSlideModel[] {
    if (this.user.username) {
      const userType: string = this.getUserType();
      return this.filterByVipLevel(
        this.filterByUserType(this.filterByChannel(this.aem.data),
          [userType, this.USER_TYPES.ANONYMOUS, this.USER_TYPES.NEW, this.USER_TYPES.BOTH])
      ).slice(0, this.aem.maxOffers);
    } else {
      return this.filterByUserType(this.filterByChannel(this.aem.data),
        [this.USER_TYPES.ANONYMOUS, this.USER_TYPES.NEW, this.USER_TYPES.BOTH]).slice(0, this.aem.maxOffers);
    }
  }

  private filterByUserType(slides: IFeaturedAemSlideModel[], userType: string[]): IFeaturedAemSlideModel[] {
    return slides.filter((slide: IFeaturedAemSlideModel) => {
      return _.intersection(this.removeUseless(slide.userType), userType).length > 0;
    });
  }

  private filterByChannel(slides: IFeaturedAemSlideModel[]): IFeaturedAemSlideModel[] {
    const channels: string[] = [];
    if (this.deviceService.isMobile || this.deviceService.isTablet) {
      channels.push(this.CHANNELS.MOBILE);
    }
    if (this.deviceService.isDesktop) {
      channels.push(this.CHANNELS.DESKTOP);
    }
    if (this.deviceService.isWrapper) {
      channels.push(this.CHANNELS.APP);
    }
    return slides.filter((slide: IFeaturedAemSlideModel) => {
      return _.intersection(this.removeUseless(slide.selectChannels), channels).length > 0;
    });
  }

  private filterByVipLevel(slides: IFeaturedAemSlideModel[]): IFeaturedAemSlideModel[] {
    return slides.filter((slide: IFeaturedAemSlideModel) => {
      return this.removeUseless(slide.imsLevel).includes(this.user.vipLevel);
    });
  }

  private getUserType(): string {
    const user = this.storage.get('existingUser');
    if (environment.brand === 'ladbrokes') {
      return user ? this.USER_TYPES.EXISTING : this.USER_TYPES.NEW;
    } else {
      return user ? this.USER_TYPES.EXISTING : this.USER_TYPES.ANONYMOUS;
    }
  }

  private removeUseless(strs: string[], ): string[] {
    return strs.map((str: string) => {
      return str.split('/')[1];
    });
  }

  private trackClickGTMEvent(slide: IFeaturedAemSlideModel, eventAction: string = 'click'): void {
    if (eventAction === 'click' && slide.clickTracked) {
      return;
    }
    if (eventAction === 'view' && slide.viewTracked) {
      return;
    }
    const vipLevel: string = this.user.vipLevel || null;
    const gtmEvent: IGtmBannerEvent = {
      event: 'trackEvent',
      eventCategory: 'banner',
      eventAction: eventAction,
      eventLabel: `${slide.offerName}, ${slide.offerTitle}`,
      personalised: false,
      location: this.windowRef.nativeWindow.location.pathname,
      position: this.aem.data.indexOf(slide),
      vipLevel: vipLevel
    };
    eventAction === 'click' ? slide.clickTracked = true : slide.viewTracked = true;
    this.gtmService.push('featuredAemBannerClick', gtmEvent);
  }

}
