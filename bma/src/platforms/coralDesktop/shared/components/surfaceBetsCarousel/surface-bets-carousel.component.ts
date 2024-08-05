import { ChangeDetectorRef, Component, ElementRef, OnDestroy, OnInit, OnChanges, SimpleChanges  } from '@angular/core';
import {
  SurfaceBetsCarouselComponent as AppSurfaceBetsCarouselComponent
} from '@shared/components/surfaceBetsCarousel/surface-bets-carousel.component';
import { Carousel } from '@shared/directives/ng-carousel/carousel.class';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'surface-bets-carousel',
  templateUrl: './surface-bets-carousel.component.html',
  styleUrls: ['./surface-bets-carousel.component.scss']
})
export class SurfaceBetsCarouselComponent extends AppSurfaceBetsCarouselComponent implements OnInit, OnDestroy, OnChanges {
  public showCarouselButtons: boolean;
  private resizeListener: Function;

  constructor(
    private elementRef: ElementRef,
    private domTools: DomToolsService,
    private windowRef: WindowRefService,
    private renderer: RendererService,
    private carouselService: CarouselService,
    protected changeDetRef: ChangeDetectorRef,
    protected pubsub: PubSubService,
  ) {
    super(changeDetRef, pubsub);
  }

  ngOnInit(): void {
    super.ngOnInit();
    this.windowRef.nativeWindow.setTimeout(() => {
      this.initShowCarouselButtons();
    }, 0);
    this.resizeListener = this.renderer.renderer.listen(this.windowRef.nativeWindow, 'resize', () => {
      this.initShowCarouselButtons();
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if(changes.module){
      this.initShowCarouselButtons();
    }
  }

  ngOnDestroy(): void {
    super.ngOnDestroy();
    this.carouselService.remove(this.carouselName);
    this.resizeListener && this.resizeListener();
  }

  public nextSlide(): void {
    this.carousel.next();
  }

  public prevSlide(): void {
    this.carousel.previous();
  }

  public get showNext(): boolean {
    return this.carousel.currentSlide < this.carousel.slidesCount - 1;
  }
  public set showNext(value:boolean){}

  public get showPrev(): boolean {
    return this.carousel.currentSlide > 0;
  }
  public set showPrev(value:boolean){}

  private get carousel(): Carousel {
    return this.module ? this.carouselService.get(this.carouselName) : null;
  }
  private set carousel(value:Carousel){}

  private initShowCarouselButtons(): void {
    const carouselSlides = this.module.data.length;
    const carouselOuterWidth = this.domTools.getWidth(this.elementRef.nativeElement.querySelector('.surface-bets-carousel'));
    const slideWidth = this.domTools.getWidth(this.elementRef.nativeElement.querySelector('.slide'));
    this.showCarouselButtons = carouselOuterWidth < (carouselSlides * slideWidth);
  }
}
