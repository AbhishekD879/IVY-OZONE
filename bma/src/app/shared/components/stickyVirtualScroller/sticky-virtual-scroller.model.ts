import { EventEmitter } from '@angular/core';

export interface IScrollInfo {
  uuid: string;
  stickyElement: Element;
  stickyElementPlaceholder: Element;
  scrollableElement: Element;
  isFirstStickyElement: boolean;
  firstScrollableElement: Element;
  lastScrollableElement: Element;
  lastScrollableHeight: number;
  isVirtualScroll: boolean;
  scrollDebounceTime: number;
  dimensions: IScrollDimensions;
  isSticked?: boolean;
  // event emitters
  calculateScrollDimensions: Function;
  preFetchNext: EventEmitter<boolean>;
  toogleStickyVisiblity: EventEmitter<boolean>;
}

export interface IScrollDimensions {
  documentHeight: number;
  headerHeight: number;
  topBarHeight: number;
  footerMenuHeight: number;

  stickyElementHeight: number;
  scrollableHeight: number;
  scrollableHeaderHeight: number;
  stickyMaxPosition: number;
  scrollableMaxPosition: number;

  viewPortHeight: number;
}

export interface IScrollChanges {
  newItems: any[];
  prevItems: any[];
}

export interface IScrollVisibility {
  visible: boolean;
  reloadData: boolean;
}
