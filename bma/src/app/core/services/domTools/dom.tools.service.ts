import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { WindowRefService } from '@core/services/windowRef/window-ref.service';

interface IOffsetData {
  top: number;
  left: number;
}

@Injectable({
  providedIn: 'root'
})
export class DomToolsService {
  header: HTMLElement;
  content: HTMLElement;
  footer: HTMLElement;

  constructor(public windowRef: WindowRefService) {}

  get HeaderEl(): HTMLElement {
    if (!this.header) {
      this.setHeader();
    }
    return this.header;
  }
  set HeaderEl(value:HTMLElement){}  
  get ContentEl(): HTMLElement {
    if (!this.content) {
      this.setContent();
    }
    return this.content;
  }
  set ContentEl(value:HTMLElement){}
  get FooterEl(): HTMLElement {
    if (!this.footer) {
      this.setFooter();
    }
    return this.footer;
  }
 set FooterEl(value:HTMLElement){}
  getHeight(elem: Element | Window): number {
    return elem ? (<Element>elem).clientHeight || (<Window>elem).innerHeight || 0 : 0;
  }

  getWidth(elem: Element | Window): number {
    return elem ? (<Element>elem).clientWidth || (<Window>elem).innerWidth || 0 : 0;
  }

  getScrollTop(elem: Element | Window): number {
    return elem ? (<Element>elem).scrollTop || (<Window>elem).scrollY || 0 : 0;
  }

  getElementTopPosition(element: Element): number {
    return element ? Math.round(element.getBoundingClientRect().top) : 0;
  }

  getElementBottomPosition(element: Element): number {
    return element ? Math.round(element.getBoundingClientRect().bottom) : 0;
  }

  getScrollTopPosition(): number {
    if (typeof pageYOffset !== undefined) {
      // most browsers except IE before #9
      return pageYOffset;
    } else {
      const B = document.body; // IE 'quirks'
      let D = document.documentElement; // IE with doctype
      D = D.clientHeight ? D : B;
      return D.scrollTop;
    }
  }

  getScrollLeft(elem: Element | Window): number {
    return elem ? (<Element>elem).scrollLeft || (<Window>elem).scrollX || 0 : 0;
  }

  scrollTop(elem: Element, num: number): void {
    if (elem.scrollTop) {
      elem.scrollTop = num;
    }
  }

  scrollStop(callback): Function {
    if (!callback || typeof callback !== 'function') {
      return;
    }

    let isScrolling;

    const scrollHandler = this.windowRef.nativeWindow.addEventListener(
      'scroll',
      event => {
        this.windowRef.nativeWindow.clearTimeout(isScrolling);

        isScrolling = this.windowRef.nativeWindow.setTimeout(() => {
          callback();
        }, 66);
      },
      false
    );

    return scrollHandler;
  }

  getOffset(element: Element): IOffsetData {
    if (!element) {
      return null;
    }

    const box = element.getBoundingClientRect();
    const body = document.body;
    const docEl = document.documentElement;
    const scrollTop = window.pageYOffset || docEl.scrollTop || body.scrollTop;
    const scrollLeft = window.pageXOffset || docEl.scrollLeft || body.scrollLeft;
    const clientTop = docEl.clientTop || body.clientTop || 0;
    const clientLeft = docEl.clientLeft || body.clientLeft || 0;
    const { marginTop, marginLeft } = window.getComputedStyle(element);
    const top = box.top + scrollTop - clientTop - parseFloat(marginTop);
    const left = box.left + scrollLeft - clientLeft - parseFloat(marginLeft);
    return { top, left };
  }

  css(
    element: HTMLElement | Element,
    propertyName: any,
    value?: string | number
  ): HTMLElement | Element {
    /* eslint-disable */
    if (_.isString(propertyName) && value !== undefined) {
      this.setPropertyValue(element, propertyName, value);
    } else if (_.isObject(propertyName)) {
      for (const key in propertyName) {
        this.setPropertyValue(element, key, propertyName[key]);
      }
    }
    /* eslint-enable */
    return element;
  }

  /**
   * Check if element has css class
   * @param {Element} element
   * @param {string} className
   */
  hasClass(element: Element, className: string) {
    if (element.classList) {
      return element.classList.contains(className);
    } else {
      return new RegExp(`(^| ) ${className} ( |$)`, 'gi').test(element.className);
    }
  }

  /**
   * Toggle css class
   * @param {HTMLElement} element
   * @param {string} className
   * @param {boolean?} forceToState
   */
  toggleClass(element: Element, className: string, forceToState?: boolean): void {
    if (!element) {
      return;
    }

    if (element.classList) {
      if (forceToState === undefined) {
        element.classList.toggle(className);
      } else if (forceToState) {
        element.classList.add(className);
      } else {
        element.classList.remove(className);
      }
    } else {
      const uniqueClassNames = element.className
        .split(' ')
        .filter((klass, index, self) => self.indexOf(klass) === index);
      const existingIndex = uniqueClassNames.indexOf(className);

      if (existingIndex >= 0) {
        (forceToState === undefined || !forceToState) && uniqueClassNames.splice(existingIndex, 1);
      } else {
        (forceToState === undefined || forceToState) && uniqueClassNames.push(className);
      }
      element.className = uniqueClassNames.join(' ');
    }
  }

  addClass(element: Element, className: string): void {
    this.toggleClass(element, className, true);
  }

  removeClass(element: Element, className: string): void {
    this.toggleClass(element, className, false);
  }

  /**
   * Toggle css display property
   * @param {HTMLElement} element
   */
  toggleVisibility(element: HTMLElement): void {
    const visibility: string = getComputedStyle(element)['display'];
    element.style.display = visibility === 'none' ? 'block' : 'none';
  }

  /**
   * Get the first element that matches the selector by testing the element itself
   * and traversing up through its ancestors in the DOM tree.
   * @param {HTMLElement} element
   * @param {string} selector
   * @returns {HTMLElement | null}
   */
  closest(element: HTMLElement, selector: string): HTMLElement | null {
    let child: HTMLElement = element,
      parent: HTMLElement = <HTMLElement>element.parentNode;

    while (parent && Array.prototype.indexOf.call(parent.querySelectorAll(selector), child) < 0) {
      child = parent;
      parent = <HTMLElement>parent.parentNode;
    }

    return parent && child;
  }

  /**
   * Checks whether the childElement is child
   * @param childElement
   * @param parent
   * @return {boolean}
   */
  isChild(childElement: Node, parent: Node): boolean {
    if (childElement.parentNode === null || parent === null) {
      return false;
    } else if (childElement.parentNode === parent) {
      return true;
    }

    return this.isChild(childElement.parentNode, parent);
  }

  /**
   * Set CSS transform properties
   * @param elm
   * @param translateX
   * @param translateY
   * @param scaleX
   * @param scaleY
   */
  setTranslate(
    elm: HTMLElement,
    translateX?: number,
    translateY?: number,
    scaleX?: number,
    scaleY?: number
  ) {
    const translate = `translate(${translateX || 0}px, ${translateY || 0}px)`;
    const scale = scaleX || scaleY ? `scale(${scaleX || 0}, ${scaleY || 0})` : '';
    const transform = `${translate} ${scale}`;
    this.css(elm, {
      transform,
      '-ms-transform': transform
    });
  }

  getOuterHeight(el: HTMLElement): number {
    if (!el) {
      return 0;
    }
    let height = el.offsetHeight;
    const style = getComputedStyle(el);

    height += parseInt(style?.marginTop, 10) + parseInt(style?.marginBottom, 10);
    return height;
  }

  innerHeight(element: HTMLElement | Element): number {
    if (!element) {
      return 0;
    }
    return parseFloat(window.getComputedStyle(element).height);
  }

  scrollPageTop(top: number): void {
    this.windowRef.document.body.scrollTop = top; // For Safari
    this.windowRef.document.documentElement.scrollTop = top; // For Chrome, Firefox, IE and Opera
    this.windowRef.document.querySelector('html, body').scrollTop = top;
  }

  getPageScrollTop(): number {
    return (
      this.windowRef.document.body.scrollTop ||
      this.windowRef.document.documentElement.scrollTop ||
      0
    );
  }

  getParentByLevel(element: Element, level: number, selector?: string): Element {
    if (level > 0) {
      level--;
      return element.parentNode
        ? this.getParentByLevel(element.parentNode as Element, level, selector)
        : null;
    }

    return selector ? element.querySelector<HTMLElement>(selector) : element;
  }

  private setHeader(): void {
    this.header = this.windowRef.document.querySelector('header.header');
  }

  private setContent(): void {
    this.content = this.windowRef.document.querySelector('#content');
  }

  private setFooter(): void {
    this.footer = this.windowRef.document.querySelector('.footer-menu');
  }

  private setPropertyValue(element, prop: string, val: string | number): void {
    element.style[prop] = this.isValidValue(prop, val) ? `${val}px` : val;
  }

  /**
   * Checks if value is valid and is not pixel property
   *
   * @param prop
   * @param val
   * @return {boolean}
   */
  private isValidValue(prop: string, val: string | number): boolean {
    const nonPixelProperties = ['opacity'];

    return _.isNumber(val) && !_.contains(nonPixelProperties, prop);
  }
}
