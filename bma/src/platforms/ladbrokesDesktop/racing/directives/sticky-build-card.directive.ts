import {
  Directive, ElementRef, OnInit, OnDestroy
} from '@angular/core';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { IConstant } from '@core/services/models/constant.model';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { DomToolsService } from '@core/services/domTools/dom.tools.service';

@Directive({
  selector: '[sticky-build-card]'
})

export class StickyBuildCardDirective implements OnInit, OnDestroy {
  protected headerBar: HTMLElement;
  private readonly stickyElement: HTMLElement;
  private buildCardTop: HTMLElement;
  private window: IConstant;
  private featuredRacingTab: HTMLElement;
  private VR: HTMLElement;
  private stickyElementOffset: number;
  private stickyElementHeight: number;

  constructor(private windowRef: WindowRefService,
              private elementRef: ElementRef,
              private domTools: DomToolsService,
              private rendererService: RendererService) {
    this.stickyElement = this.elementRef.nativeElement;
    this.headerBar = this.domTools.HeaderEl;
  }

  ngOnInit(): void {
    this.setStickySize = this.setStickySize.bind(this);
    this.window = this.windowRef.nativeWindow;
    this.buildCardTop =  this.window.document.querySelector('.build-card-top');
    this.featuredRacingTab =  this.window.document.querySelector('.featured-racing-tab');
    this.VR = this.window.document.querySelector('.VR');
    this.stickyElementOffset = this.stickyElement.getBoundingClientRect().top + this.windowRef.nativeWindow.pageYOffset;
    this.stickyElementHeight = this.stickyElement.clientHeight;
    this.setListeners();
    this.setStickySize();
  }

  ngOnDestroy(): void {
    this.removeListeners();
  }

  setStickySize(): void {
    const height = this.headerBar && this.headerBar.offsetHeight || 0;
    const width: number = this.buildCardTop.clientWidth;
    this.rendererService.renderer.setStyle(this.stickyElement, 'width', `${width}px`);
    this.rendererService.renderer.setStyle(this.stickyElement, 'top', `${height}px`);
  }

  scrollHandler(): void {
    const vrOffset = this.VR ? this.VR.offsetHeight : 0;

    if (this.stickyElementOffset < this.window.pageYOffset) {
      const leftOffset = this.buildCardTop.getBoundingClientRect().left;
      const headerBottomPosition = this.domTools.getElementBottomPosition(this.domTools.HeaderEl);
      this.rendererService.renderer.setStyle(this.stickyElement, 'left', `${leftOffset}px`);
      this.rendererService.renderer.setStyle(this.stickyElement, 'top', `${headerBottomPosition}px`);
      this.rendererService.renderer.addClass(this.stickyElement, 'sticky-on');
    }
    if (this.stickyElementOffset > this.window.pageYOffset) {
      this.rendererService.renderer.removeClass(this.stickyElement, 'sticky-on');
    }
    if (this.window.pageYOffset > (this.stickyElementOffset -
        this.stickyElementHeight +
        this.featuredRacingTab.offsetHeight - vrOffset)) {
      this.rendererService.renderer.addClass(this.stickyElement, 'sticky-on-hidden');
    } else {
      this.rendererService.renderer.removeClass(this.stickyElement, 'sticky-on-hidden');
    }
  }

  private setListeners(): void {
    this.window.addEventListener('resize', this.setStickySize);
    this.window.document.addEventListener('scroll', this.scrollHandler.bind(this));
  }

  private removeListeners(): void {
    this.window.removeEventListener('resize', this.setStickySize);
    this.window.document.removeEventListener('scroll', this.scrollHandler.bind(this));
  }
}
