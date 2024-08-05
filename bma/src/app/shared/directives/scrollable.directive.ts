import {
  Directive,
  OnDestroy,
  AfterViewInit,
  ElementRef,
  Input,
  OnChanges,
  SimpleChanges
} from '@angular/core';

import { StorageService } from '@core/services/storage/storage.service';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { IElementData } from '../models/element-data.model';
import { RendererService } from '@shared/services/renderer/renderer.service';

// eslint-disable-next-line
@Directive({ selector: '[scrollable]' })
export class ScrollableDirective implements OnDestroy, AfterViewInit, OnChanges {
  @Input() rescrollOnChange: any;

  protected element: HTMLElement;

  private elementData: IElementData;

  private scrollListener: Function;
  private mouseEnterListener: Function;
  private mouseDownListener: Function;
  private mouseMoveListener: Function;
  private mouseLeaveListener: Function;
  private mouseUpListener: Function;
  private dragStartListener: Function;

  constructor(
    protected rendererService: RendererService,
    protected device: DeviceService,
    protected windowRef: WindowRefService,
    protected storage: StorageService,
    public el: ElementRef
  ) {
    // Default Element Data
    this.elementData = {
      isMouseDown: false,
      clientX: 0,
      scrollLeft: 0
    };
  }

  ngAfterViewInit(): void {
    this.element = this.el.nativeElement;
    this.scrollToSelected();
    this.setScrollable();
  }

  /**
   * Listen to changes of rescrollOnChange member, re-scroll list to selected item unless the updated value is null
   * @param changes
   */
  ngOnChanges(changes: SimpleChanges): void {
    if (changes.rescrollOnChange && !changes.rescrollOnChange.firstChange && changes.rescrollOnChange.currentValue !== null) {
      this.windowRef.nativeWindow.setTimeout(() => this.scrollToSelected());
    }
  }

  ngOnDestroy(): void {
    if (this.scrollListener) {
      this.scrollListener();
    }
    if (this.dragStartListener) {
      this.dragStartListener();
    }
    if (this.mouseDownListener) {
      this.mouseDownListener();
    }
  }

  /**
   * Desktop: ini desktop logic
   */
  protected setScrollable(): void {
    if (!this.device.isMobileOrigin) {
      this.dragStartListener = this.rendererService.renderer.listen(this.element, 'dragstart', e => e.preventDefault());
      this.mouseDownListener = this.rendererService.renderer.listen(this.element, 'mousedown', e => this.mouseDownHandler(e));
    } else {
      this.scrollListener = this.rendererService.renderer.listen(this.element, 'scroll', () => this.scrollHandler());
    }
  }

  /**
   * Scroll to selected item
   */
  protected scrollToSelected(): void {
    const selected: HTMLElement = this.element.querySelector('.active');
    if (!selected) { return; }
    // Selected item left position
    const selectedLP = selected.offsetLeft;
    // Get scrollLeft from storage
    const scrollLP = Number(this.storage.get('scrollLeft')) || 0;
    // Element width
    const eW = this.element.offsetWidth;
    // Selected item width
    const sW = selected.offsetWidth || 50; // min element width
    // Check if Selected item is first
    const isFirstSelectedElement = (selectedLP + sW) < eW;
    // Check position Selected item
    // ToDo: condition (selectedLP + sW <= scrollLP && selectedLP + sW > scrollLP) is incorrect, since is always false
    const isSelectedElement = ((selectedLP + sW <= scrollLP && selectedLP + sW > scrollLP) ||
      (selectedLP >= scrollLP && selectedLP + sW <= scrollLP + eW)) && scrollLP;
    if (isFirstSelectedElement) {
      this.element.scrollLeft = 0;
    } else if (isSelectedElement) {
      this.element.scrollLeft = scrollLP;
    } else {
      this.element.scrollLeft = selectedLP;
    }
  }

  /**
   * Set Scroll Left Position to Storage
   */
  private scrollHandler(): void {
    this.storage.set('scrollLeft', this.element.scrollLeft);
  }

  /**
   * Desktop: scroll with mouse
   * @param event
   */
  private mouseMoveHandler(event): void {
    if (this.elementData.isMouseDown) {
      this.element.scrollLeft = this.elementData.scrollLeft + this.elementData.clientX - event.clientX;
    }
  }

  /**
   * Desktop: set scroll start position
   * @param event
   */
  private mouseEnterHandler(event): void {
    this.elementData.clientX = event && event.clientX;
    this.elementData.scrollLeft = this.element.scrollLeft;
  }

  /**
   * Desktop: store position, remove scrolling process listeners
   */
  private mouseLeaveHandler(): void {
    this.elementData.isMouseDown = false;
    this.scrollHandler();
    this.mouseEnterListener();
    this.mouseMoveListener();
    this.mouseLeaveListener();
    this.mouseUpListener();
  }

  /**
   * Desktop: check position, add scrolling process listeners
   * @param event
   */
  private mouseDownHandler(event): void {
    const documentBody: HTMLElement = this.windowRef.nativeWindow.document.body;
    this.mouseEnterHandler(event);
    this.elementData.isMouseDown = true;
    this.mouseEnterListener = this.rendererService.renderer.listen(this.element, 'mouseenter', e => this.mouseEnterHandler(e));
    this.mouseMoveListener = this.rendererService.renderer.listen(this.element, 'mousemove', e => this.mouseMoveHandler(e));
    this.mouseLeaveListener = this.rendererService.renderer.listen(this.element, 'mouseleave', () => this.mouseLeaveHandler());
    this.mouseUpListener = this.rendererService.renderer.listen(documentBody, 'mouseup', () => this.mouseLeaveHandler());
  }
}
