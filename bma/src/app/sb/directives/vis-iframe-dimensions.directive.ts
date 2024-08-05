import { Directive, ElementRef, Input, OnDestroy, OnInit } from '@angular/core';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Directive({
  selector: '[visIframeDimensions]'
})
export class VisIframeDimensionsDirective implements OnInit, OnDestroy {
  @Input() dimensionMultiplier: number;
  @Input() visDelta: number;
  @Input() visType: string;

  private readonly SIMPLIFIED_RATION = 0.29;
  private readonly FULL_VERSION_RATION = 0.625;
  private delta: number;
  private container: HTMLElement;
  private iframe: HTMLElement;

  private resizeHandler: Function;
  private orientationChangeHandler: Function;
  private loadHandler: Function;

  constructor(
    private windowRef: WindowRefService,
    private elementRef: ElementRef,
    private rendererService: RendererService
  ) {}

  /*
   * Iframe resize based on ratio height/width ratio of visualization iframe.
   * For simplified(castro) widget: ratio = 0.29 (height/width)
   * For full version(slider) widget: ratio = 0.625 (height/width)
   * For pre-match stats widget: ratio = 0.625 (height/width)
  */
  ngOnInit(): void {
    this.container = this.elementRef.nativeElement;
    this.iframe = this.container.querySelector('iframe');
    this.dimensionMultiplier = this.visType === 'castro' ? this.SIMPLIFIED_RATION : this.FULL_VERSION_RATION;
    this.delta = null;

    // Set parent div height 0 until visualisation is not loaded
    this.rendererService.renderer.setStyle(this.container, 'height', '0');

    this.loadHandler = this.rendererService.renderer.listen(this.iframe, 'load', () => this.resizeFrame());
    /*
     * Delta resizing, to improve page performance(iframe will be resized only 700ms
     * after resize will be completed
     */
    this.resizeHandler = this.rendererService.renderer.listen(this.windowRef.nativeWindow, 'resize', () => this.onResizeBind());
    this.orientationChangeHandler = this.rendererService.renderer
      .listen(this.windowRef.nativeWindow, 'orientationchange', () => this.onResizeBind());
  }

  ngOnDestroy(): void {
    clearTimeout(this.delta);
    this.resizeHandler();
    this.orientationChangeHandler();

    this.loadHandler();
    this.rendererService.renderer.setStyle(this.container, 'height', '0');
  }

  private resizeFrame(): void {
    const visDelta = this.visDelta ? this.visDelta : 0;
    const divWidth = this.elementRef.nativeElement.parentNode.offsetWidth;
    const countHeight = divWidth ? ((divWidth * this.dimensionMultiplier) + visDelta) : '100%';

    this.rendererService.renderer.setStyle(this.iframe, 'width', `${divWidth}px`);
    this.rendererService.renderer.setStyle(this.iframe, 'height', `${countHeight}px`);
    this.rendererService.renderer.setStyle(this.container, 'height', `${countHeight}px`);
  }

  private onResizeBind(): void {
    clearTimeout(this.delta);
    this.delta = this.windowRef.nativeWindow.setTimeout(() => this.resizeFrame(), 700);
  }
}
