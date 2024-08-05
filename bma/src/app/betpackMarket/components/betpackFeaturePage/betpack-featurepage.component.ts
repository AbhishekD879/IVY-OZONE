import { Component, Input} from '@angular/core';
import { Carousel } from '@app/shared/directives/ng-carousel/carousel.class';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { PubSubService } from 'app/core/services/communication/pubsub/pubsub.service';
import { BetpackCmsService } from '@app/lazy-modules/betpackPage/services/betpack-cms.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { IFreebetToken, IOffer } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { BetPackLabels, BetPackModel } from '@app/betpackReview/components/betpack-review.model';
import { UserService } from '@app/core/services/user/user.service';
import { BET_PACK_CONSTANTS } from '@app/betpackMarket/constants/constants';
import { ArcUserService } from '@app/lazy-modules/arcUser/service/arcUser.service';
@Component({
  selector: 'betpack-featurepage',
  templateUrl: './betpack-featurepage.component.html',
  styleUrls: ['./betpack-featurepage.scss']
})
export class BetpackFeaturepageComponent {
  brand: string = 'new';
  carouselName = 'betpack-banners';
  public activeSlideIndex: number = 0;
  isSlided = true;
  BET_PACK_CONSTANTS = BET_PACK_CONSTANTS;
  @Input() filteredBetPack: BetPackModel[];
  @Input() betpackDetails: BetPackModel[];
  @Input() isMaxPurchaseLimitOver: boolean;
  @Input() getLimitsData: number;
  @Input() getFreeBets: IFreebetToken[];
  @Input() betpackLabels: BetPackLabels;
  @Input() isPromptDisplay: boolean;
  @Input() accLimitFreeBets: IOffer[];
  deleteLater: boolean = false;
  scrollCalled: boolean=false;

  constructor(private carouselService: CarouselService,
    private liveServConnectionService: LiveServConnectionService,
    private pubSubService: PubSubService,
    public betpackCmsService: BetpackCmsService,
    private gtmService: GtmService,    
    public userService: UserService,    
    private arcUserService: ArcUserService,
    ) {
  }

  /**
   * @returns {void}
   */
  nextSlide(): void {
    this.bannersCarousel.next();
  }

  /**
   * @returns {void}
   */
  prevSlide(): void {
    this.bannersCarousel.previous();
  }
  /**
   * @returns {void}
   */
  gotToSlide(index: number): void {
    this.bannersCarousel.toIndex(index);
  }

  /**
   * @param  {number} slideIndex
   * @returns {void}
   */
  handleActiveSlide(slideIndex: number): void {
    if (!Number.isInteger(slideIndex)) {
      return;
    }
    if (!this.isSlided) {
      this.isSlided = true;
    }
    const i = slideIndex - 1;

    if (this.filteredBetPack[i]) {
      this.filteredBetPack[this.activeSlideIndex].active = false;
      this.filteredBetPack[i].active = true;
      this.activeSlideIndex = i;
    }
    if(!this.scrollCalled){
      this.sendGtmData('scroll');
    }
  }
  /**
   * @returns {Carousel}
   */
  private get bannersCarousel(): Carousel {
    return this.carouselService.get(this.carouselName);
  }

  /**
   * @param  {Carousel} value
   */
  private set bannersCarousel(value: Carousel) { }

  /**
  * GATracking for bet bundles event
  * @param  {Carousel} value
  * @returns void
  */
  private sendGtmData(eventLabel:string): void {
    const gtmData = {
      event: 'trackEvent',
      eventAction: 'bet bundles',
      eventCategory: 'bet bundles marketplace',
      eventLabel: eventLabel
    };
    this.scrollCalled=true;
    this.gtmService.push(gtmData.event, gtmData);
  }

}