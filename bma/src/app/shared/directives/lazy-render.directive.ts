import { Directive, EventEmitter, OnDestroy, OnInit, OnChanges, Input, Output, ElementRef } from '@angular/core';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@shared/services/renderer/renderer.service';

// eslint-disable-next-line
@Directive({selector: '[lazyRender]'})
export class LazyRenderDirective implements OnInit, OnDestroy, OnChanges {
  @Input() lazyIsScroll: boolean = false;
  @Input() lazyIsOpen: boolean = true;
  @Input() lazyItems: number = 3;
  @Input() lazyStep: number = 5;
  @Input() lazyRender: number;

  @Output() readonly lazyLimitChange: EventEmitter<number> = new EventEmitter<number>();

  limit: number = this.lazyItems;

  private loadTimeout: any;
  private loadTime: number = 100;
  private scrollListener: Function;

  constructor(private window: WindowRefService,
              private element: ElementRef,
              private rendererService: RendererService) {}

  ngOnInit(): void {
    this.lazyLimitChange.emit(this.limit);
    this.setLazyRender();
  }

  ngOnChanges(changes: any ): void  {
    const isChanges = changes.lazyIsOpen && changes.lazyIsOpen.currentValue && changes.lazyIsOpen.previousValue !== undefined &&
      (changes.lazyIsOpen.currentValue !== changes.lazyIsOpen.previousValue);

    if (isChanges) {
      this.setLazyRender();
    }
  }

  ngOnDestroy(): void {
    this.clearTimeout();
    if (this.scrollListener) {
      this.scrollListener();
    }
  }

  private setLazyRender(): void {
    if (this.lazyIsScroll && (this.lazyRender > this.lazyItems)) {
      this.scrollListener = this.rendererService.renderer.listen(this.window.nativeWindow, 'scroll', () => this.loadMoreOnScroll());
    } else if (!this.lazyIsScroll && this.lazyIsOpen && (this.lazyRender > this.lazyItems)) {
      this.loadMoreOnTimeout();
    } else {
      this.clearTimeout();
    }
  }

  /** Clear Timeout */
  private clearTimeout(): void {
    if (this.loadTimeout) {
      clearTimeout(this.loadTimeout);
    }
  }

  /** Load more data on Scroll */
  private loadMoreOnScroll(): void {
    const isLoadMore: boolean = this.window.nativeWindow.scrollY + this.window.nativeWindow.innerHeight >=
      this.element.nativeElement.getBoundingClientRect().top + this.element.nativeElement.clientHeight;
    if (isLoadMore && (this.limit <= this.lazyRender)) {
      this.limit += this.lazyStep;
      this.lazyLimitChange.emit(this.limit);
    }
  }

  /** Load more data every few milliseconds */
  private loadMoreOnTimeout(): void {
    if (this.limit <= this.lazyRender) {
      this.limit += this.lazyStep;
      this.lazyLimitChange.emit(this.limit);
      this.loadTimeout = setTimeout(() => this.loadMoreOnTimeout(), this.loadTime);
    }
  }
}
