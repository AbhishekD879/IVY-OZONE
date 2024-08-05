import { ChangeDetectorRef, Component, Input, SimpleChanges } from "@angular/core";
import { IOffer } from '@core/models/aem-banners-section.model';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import environment from '@environment/oxygenEnvConfig';
import { banners } from "./virtual-mock-data";
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { Carousel } from '@app/shared/directives/ng-carousel/carousel.class';
import { IVirtualSportsHomePage } from "@app/core/services/cms/models/virtual-sports.model";
import { Router } from "@angular/router";
import { VirtualHubService } from "@app/vsbr/services/virtual-hub.service";

@Component({
  selector: 'virtual-other-sports',
  templateUrl: './virtual-other-sports.component.html',
  styleUrls: ['./virtual-other-sports.component.scss']
})

export class VirtualOtherSports {
  @Input() public otherSportImages: IVirtualSportsHomePage[] = [];
  @Input() public virtualsLiveCount: any;
  public timePerSlide: number = 7000;
  public imgWidth: number;
  allOffers: IOffer[];
  offers: IOffer[];
  brand: string = '';
  carouselName = 'othersport-banners';
  currentIndex: number = 0;
  extraSlide: Element;
  topOtherSportLength = 0;

  /**
   * Constructor
  */
  constructor(
    private deviceService: DeviceService,
    private windowRef: WindowRefService,
    private carouselService: CarouselService,
    private router: Router,
    private virtualHubService: VirtualHubService,
    private changeDetectorRef: ChangeDetectorRef
  ) {
    this.brand = environment.brand;
  }

  /**
   * OnInit
  */
  ngOnInit(): void {
    this.topOtherSportLength = Math.ceil(this.otherSportImages.length/2);
    this.windowRef.nativeWindow.setInterval(() => {
      this.getLaterUpdates();
    }, 5000);
    this.imgWidth = this.deviceService.isDesktop ? 720 : 480;
  }

  /**
   * ngOnChanges
  */
  ngOnChanges(changes: SimpleChanges): void {
    if (changes.virtualsLiveCount) {
      this.virtualsLiveCount = changes.virtualsLiveCount.currentValue;
    }
    if (changes.otherSportImages) {
      this.topOtherSportLength = Math.ceil(changes.otherSportImages.currentValue.length/2);
      this.otherSportImages = changes.otherSportImages.currentValue;
    }
  }

  /*
   * Gets offers Odds immediatly after rendering banners
  */
  ngAfterViewInit() {
    this.getLaterUpdates();
  }

  /*
   * Gets offers Odds for configured time interval
  */
  getLaterUpdates(): void {
    this.offers = banners;
    if (this.offers && this.offers.length) {
      this.offers = [...this.offers, ...this.offers, ...this.offers, ...this.offers];
    }
  }

  /**
   * updateEventsData
  */
  updateEventsData(sportName: string): string {
    let liveCount: string;
    if (this.virtualsLiveCount) {
      const foundItem: any = this.virtualsLiveCount.find(item => item.sportName.toLowerCase() === sportName.toLowerCase());
      liveCount = foundItem ? foundItem.liveEventCount : null;
      if (liveCount) {
        liveCount = +liveCount > 1 ? liveCount + ' ' + 'Events' : liveCount + ' ' + 'Event';
      }
    }
    return liveCount;
  }

  /**
   * virtual sports redirection handler
   */
  goToVirtualSports(imageInfo: IVirtualSportsHomePage): void {
    if (imageInfo && imageInfo.redirectionURL) {
      this.virtualHubService.onClickNavigationDetails.id = 'other sports';
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
   * next slide click handler
   */
  nextSlide(): void {
    this.currentIndex++;
    this.carousel.next();
    this.showNext();
    this.changeDetectorRef.detectChanges();
  }

  /**
   * previour slide click handler
   */
  prevSlide(): void {
    if (this.currentIndex == 0)
      return;
    this.currentIndex--;
    this.bannersCarousel.previous();
  }

  /**
   * bannersCarousel getter
   */
  private get bannersCarousel(): Carousel {
    return this.carouselService.get(this.carouselName);
  }

  /**
   * bannersCarousel setter
   */
  private set bannersCarousel(value: Carousel) { }

  /**
   * Other Sports Banner event handler
   * @param $event : MouseEvent
   * @param offer : IVirtualSportsHomePage
   */
  public actionHandler($event: MouseEvent, offer: IVirtualSportsHomePage): void {
    $event.preventDefault();
    this.goToVirtualSports(offer);
  }

  /**
   * carousel getter
  */
  private get carousel(): Carousel {
    return this.carouselService.get(this.carouselName);
  }

  /**
   * carousel setter
   */
  private set carousel(value: Carousel) { }

  /**
   * ngCarouselDisableRightSwipe getter
   */
  get ngCarouselDisableRightSwipe(): boolean {
    return this.carousel && ((this.carousel.currentSlide + 1) * 3 > this.carousel.slidesCount - 1);
  }

  /**
   * ngCarouselDisableRightSwipe setter
   */
  set ngCarouselDisableRightSwipe(value: boolean) { }

  /**
   * showNext getter
   */
  showNext(): boolean {
    return this.carousel && ((this.carousel.currentSlide + 1) * 3 <= this.carousel.slidesCount - 1);
  }


  /**
   * showPrev getter
   */
  get showPrev(): boolean {
    return this.carousel && this.carousel.currentSlide > 0;
  }

  /**
   * showPrev setter
   */
  set showPrev(value: boolean) { }

}