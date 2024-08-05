import { Component, OnDestroy, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { IOffer } from '@core/services/cms/models/offer/offer.model';
import { IOffersList } from '@core/services/cms/models/offer/offers-list';
import { DeviceService } from '@core/services/device/device.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { UserService } from '@core/services/user/user.service';
import { CasinoLinkService } from '@core/services/casinoLink/casino-link.service';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { ExistNewUserService } from '@core/services/existNewUser/exist-new-user.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { NavigationService } from '@core/services/navigation/navigation.service';

@Component({
  selector: 'offer-section',
  templateUrl: './offer-section.component.html'
})
export class OffersSectionComponent implements OnInit, OnDestroy {

  offersData: IOffersList[];
  isCarouselInited: boolean[] = [];

  readonly DURATION: number = 10000;
  private readonly MAX_OFFERS: number = 3;
  private readonly title = 'offersSection';

  private cmsData: IOffersList[];

  constructor(
    private cmsService: CmsService,
    private existNewUserService: ExistNewUserService,
    private carouselService: CarouselService,
    private casinoLinkService: CasinoLinkService,
    private user: UserService,
    private windowRef: WindowRefService,
    private gtmService: GtmService,
    private deviceService: DeviceService,
    private coreTools: CoreToolsService,
    private pubSubService: PubSubService,
    private navigationService: NavigationService
  ) { }

  ngOnInit(): void {
    this.getOffersData(this.deviceService.strictViewType);
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.title);
  }

  /**
   * Go to index Slide
   * @param {number} index
   * @param {number} num
   */
  gotToSlide(index: number, num: number): void {
    const offersCarousel = this.carouselService.get(`offers-carousel-${num}`);
    offersCarousel.toIndex(index);
  }

  /**
   * Set Active Slide
   * @param {number} index
   * @param {number} num
   */
  setActiveSlide(index: number, num: number): boolean {
    const offersCarousel = this.carouselService.get(`offers-carousel-${num}`);
    return offersCarousel ? offersCarousel.currentSlide === index : false;
  }

  redirect(url): void {
    this.navigationService.openUrl(url);
  }

  /**
   * send GTM when user click on banner
   * @param offer {object} - offer object
   * @param pos {number} - offer index
   */
  sendGTM(offer: IOffer, pos: number): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'banner',
      eventAction: 'click',
      eventLabel: offer.name.toLowerCase().replace(/_/g, ' '),
      location: 'offers module',
      vipLevel: this.user.vipLevel || '',
      position: (pos + 1).toString()
    });
  }

  trackByOffers(i: number, element: IOffer): string {
    return `${i}_${element.sportName}_${element.displayTo}`;
  }

  trackByOffersData(i: number, element: IOffersList): string {
    return `${i}_${element.name}_${element.offers.length}`;
  }

  trackBySlide(i: number, element: IOffer): string {
    return `${i}_${element.sportName}_${element.displayTo}`;
  }

  onCarouselInit(isInit: boolean, index: number): void {
    this.windowRef.nativeWindow.setTimeout(() => this.isCarouselInited[index] = isInit);
  }

  /**
   * Get Offers Data
   * param {String} deviceType
   * @private
   */
  protected getOffersData(deviceType: string): void {
    this.cmsService.getOffers(deviceType)
      .subscribe((data: IOffersList[]) => {
        this.cmsData = data;
        this.getOffers();

      this.pubSubService.subscribe(
          this.title, [this.pubSubService.API.SESSION_LOGOUT, this.pubSubService.API.SESSION_LOGIN], () => this.getOffers()
        );
        this.pubSubService.subscribe(this.title, this.pubSubService.API.RELOAD_COMPONENTS, () => {
          this.checkOffersChanges();
          this.pubSubService.publish(this.pubSubService.API.DISPLAY_WIDGET, [{ name: 'offers' }]);
        });
      });
  }

  /**
   * detect if offers was changed
   * @private
   */
  private checkOffersChanges(): void {
    this.cmsService.getOffers(this.deviceService.strictViewType)
      .subscribe((data: IOffersList[]) => {
        if (data) {
          this.cmsData = data;
        }
        this.getOffers();
      });
  }

  /**
   * get offers from CMS
   * @private
   */
  private getOffers(): void {
    if (!this.offersData) {
      this.offersData = [];
    }
    if (this.cmsData && this.cmsData.length) {
      const cmsData = this.coreTools.deepClone(this.cmsData);
      this.offersData = this.handlingOffers(cmsData);
      const offers = _.chain(this.offersData)
        .pluck('offers')
        .flatten()
        .value();
      if (!(offers && offers.length)) {
        this.hideOffersWidget();
      }
    } else {
      this.hideOffersWidget();
    }
  }

  /**
   * handling and filtering offers
   * @param cmsData {Array} - array of offers objects
   * @return {Array}
   * @private
   */
  private handlingOffers(cmsData: IOffersList[]): IOffersList[] {
    const offersData = _.each(cmsData, (item: IOffersList) => {
      item.offers = this.existNewUserService.filterExistNewUserItems(item.offers).splice(0, this.MAX_OFFERS);
      item.offers = this.casinoLinkService.decorateCasinoLink(item.offers);
      if (item.offers.length) {
        _.each(item.offers, (offer: IOffer) => {
          if (offer.useDirectImageUrl) {
            offer.image = offer.directImageUrl;
          }
          return offer;
        });
      }
    });

    return _.filter((offersData as any[]), item => item.offers && item.offers.length);
  }

  /**
   * hide offers widget
   * @private
   */
  private hideOffersWidget(): void {
    this.pubSubService.publish(this.pubSubService.API.SHOW_WIDGET, {
      name: 'offers',
      data: false
    });
  }
}
