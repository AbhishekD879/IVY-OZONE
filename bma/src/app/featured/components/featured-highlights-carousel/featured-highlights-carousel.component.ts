import * as _ from 'underscore';
import { Component, OnInit, Input, OnDestroy, ElementRef, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { IHighlightsCarousel } from '@featured/models/highlights-carousel.model';
import { Router } from '@angular/router';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DeviceService } from '@core/services/device/device.service';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { Carousel } from '@shared/directives/ng-carousel/carousel.class';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { STRATEGY_TYPES } from '@app/core/constants/strategy-types.constant';

@Component({
  selector: 'featured-highlight-carousel',
  templateUrl: './featured-highlights-carousel.component.html',
  styleUrls: ['featured-highlights-carousel.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FeaturedHighlightsCarouselComponent implements OnInit, OnDestroy {
  @Input() highlightsCarousel: IHighlightsCarousel;
  @Input() sportName: string;
  @Input() outcomeColumnsTitles: string[];
  @Input() fzHighlighCarouselTitle = '';
  @Input() eagerLoadCount: number;

  pageId: string = _.uniqueId('featuredHighlightsCarousel_');
  isCarouselInit: boolean;
  showCarouselButtons: boolean = false;
  initialised:boolean = false;
  isDesktop: boolean;
  // change detection type
  changeStrategy = STRATEGY_TYPES.ON_PUSH;

  private resizeListener: Function;

  constructor(
    private elementRef: ElementRef,
    private windowRef: WindowRefService,
    private router: Router,
    private domTools: DomToolsService,
    private carouselService: CarouselService,
    private renderer: RendererService,
    private routingHelperService: RoutingHelperService,
    private device: DeviceService,
    private pubSubService: PubSubService,
    private chageDetectorRef: ChangeDetectorRef
  ) {
  }

  ngOnInit(): void {
    if (!this.device.isTouch()) {
      this.windowRef.nativeWindow.setTimeout(() => {
        this.initShowCarouselButtons();
      }, 0);
      this.resizeListener = this.renderer.renderer.listen(this.windowRef.nativeWindow, 'resize', () => {
        this.initShowCarouselButtons();
      });
    }

    this.pubSubService.subscribe(this.pageId, this.pubSubService.API.WS_EVENT_UPDATED, (event: ISportEvent) => {
      if (event && this.highlightsCarousel.eventIds.includes(event.id)) {
        this.chageDetectorRef.detectChanges();
      }
    });

    this.pubSubService.subscribe(this.pageId, this.pubSubService.API.WS_EVENT_UPDATE, (event: ISportEvent) => {
      this.chageDetectorRef.detectChanges();
    });

    this.isDesktop = this.device.isDesktop;
  }

  ngOnDestroy(): void {
    this.highlightsCarousel && this.carouselService.remove(this.highlightsCarousel._id);
    if (!this.device.isTouch()) {
      this.resizeListener && this.resizeListener();
    }

    this.pubSubService.unsubscribe(this.pageId);
  }

  trackByCard(id: number, element: any): string {
    return element.id;
  }

  childComponentLoaded(): void {
    this.initialised = true;
  }
  /**
   * SEE ALL link
   * to competition page by typeID
   */
  competitionsNavigate(): void {
    const competitionPageUrl = this.routingHelperService.formCompetitionUrl({
      sport: this.highlightsCarousel.data[0].categoryName.toLowerCase(),
      typeName: this.highlightsCarousel.data[0].typeName,
      className: this.highlightsCarousel.data[0].className
    });


    this.router.navigate([competitionPageUrl]);
  }

  nextSlide(): void {
    this.carousel.next();
  }

  prevSlide(): void {
    this.carousel.previous();
  }

  get showNext(): boolean {
    return this.carousel.currentSlide < this.carousel.slidesCount - 1;
  }
 set showNext(value:boolean){}
  get showPrev(): boolean {
    return this.carousel.currentSlide > 0;
  }
 set showPrev(value:boolean){}
  public get isOneCard(): boolean {
    return this.highlightsCarousel.data && this.highlightsCarousel.data.length === 1;
  }
public set isOneCard(value:boolean){}
  public get isValidCarousel(): boolean {
    return !!(this.highlightsCarousel && this.highlightsCarousel.data && this.highlightsCarousel.data.length);
  }
 public set isValidCarousel(value:boolean){}
  private get carousel(): Carousel {
    return this.highlightsCarousel ? this.carouselService.get(this.highlightsCarousel._id) : null;
  }
private set carousel(value:Carousel){}
  private initShowCarouselButtons(): void {
    const carouselSlides = this.highlightsCarousel.data.length;
    const carouselOuterWidth = this.domTools.getWidth(this.elementRef.nativeElement.querySelector('.highlight-carousel'));
    const slideWidth = this.domTools.getWidth(this.elementRef.nativeElement.querySelector('.slide'));
    this.showCarouselButtons = carouselOuterWidth < (carouselSlides * slideWidth);
  }
/**
   * return true if it's fanzone page
   */
  isFanzonePage(): boolean {
    const isFanzonePage = this.router.url.includes('fanzone');
    return isFanzonePage;
  }
}
