import { DomToolsService } from './dom.tools.service';

describe('DomToolsService', () => {
  let windowRef;
  let header;
  let content;
  let footer;
  let service: DomToolsService;

  beforeEach(() => {
    header = {};
    content = {};
    footer = {};
    windowRef = {
      scrollPageTop: jasmine.createSpy(),
      document: {
        body: {},
        documentElement: {},
        querySelector: jasmine.createSpy('querySelector').and.returnValue({}),
        getElementById: jasmine.createSpy('getElementById')
      },
      nativeWindow: {
        addEventListener: jasmine.createSpy('addEventListener'),
        clearTimeout: jasmine.createSpy('clearTimeout'),
        setTimeout: jasmine.createSpy('setTimeout')
      }
    };

    service = new DomToolsService(
      windowRef
    );
  });

  it('HeaderEl', () => {
    service.header = header;
    service['setHeader'] = jasmine.createSpy();
    expect(service.HeaderEl).toBe(service.header);
    expect(service['setHeader']).not.toHaveBeenCalled();
  });

  it('HeaderEl when header was not set', () => {
    service.header = null;
    service['setHeader'] = jasmine.createSpy().and.callFake(() => service.header = header);
    expect(service.HeaderEl).toBe(service.header);
    expect(service['setHeader']).toHaveBeenCalled();
  });

  it('ContentEl', () => {
    service.content = content;
    service['setContent'] = jasmine.createSpy();
    expect(service.ContentEl).toBe(service.content);
    expect(service['setContent']).not.toHaveBeenCalled();
  });

  it('ContentEl when content was not set', () => {
    service.content = null;
    service['setContent'] = jasmine.createSpy().and.callFake(() => service.content = content);
    expect(service.ContentEl).toBe(service.content);
    expect(service['setContent']).toHaveBeenCalled();
  });

  it('FooterEl', () => {
    service.footer = footer;
    service['setFooter'] = jasmine.createSpy();
    expect(service.FooterEl).toBe(service.footer);
    expect(service['setFooter']).not.toHaveBeenCalled();
  });

  it('FooterEl when footer was not set', () => {
    service.footer = null;
    service['setFooter'] = jasmine.createSpy().and.callFake(() => service.footer = footer);
    expect(service.FooterEl).toBe(service.footer);
    expect(service['setFooter']).toHaveBeenCalled();
  });

  it('#getHeight: should get height of the element', () => {
    const elementStub = {
      clientHeight: 10
    };
    const windowStub = {
      innerHeight: 5
    };
    expect(service.getHeight(elementStub as Element)).toBe(10);
    expect(service.getHeight(windowStub as Window)).toBe(5);
    expect(service.getHeight(null)).toBe(0);
  });

  it('#getWidth: should get width of the element', () => {
    const elementStub = {
      clientWidth: 10
    };
    const windowStub = {
      innerWidth: 5
    };
    expect(service.getWidth(elementStub as Element)).toBe(10);
    expect(service.getWidth(windowStub as Window)).toBe(5);
    expect(service.getWidth(null)).toBe(0);
  });

  it('#getScrollTop: should be scrolled vertically', () => {
    const elementStub = {
      scrollTop: 10
    };
    const windowStub = {
      scrollY: 5
    };
    expect(service.getScrollTop(elementStub as Element)).toBe(10);
    expect(service.getScrollTop(windowStub as Window)).toBe(5);
    expect(service.getHeight(null)).toBe(0);
  });

  it('#getElementTopPosition: should get 0', () => {
    expect(service.getElementTopPosition(null)).toEqual(0);
  });

  it('#getElementTopPosition: should get element top position', () => {
    const elemStub = {
      getBoundingClientRect: jasmine.createSpy().and.returnValue({ top: 10 })
    } as any;
    expect(service.getElementTopPosition(elemStub)).toEqual(10);
  });

  it('#getElementBottomPosition: should get 0', () => {
    expect(service.getElementBottomPosition(null)).toEqual(0);
  });

  it('#getElementBottomPosition: should get element bottom position', () => {
    const elemStub = {
      getBoundingClientRect: jasmine.createSpy().and.returnValue({ bottom: 10 })
    } as any;
    expect(service.getElementBottomPosition(elemStub)).toEqual(10);
  });

  it('#getScrollTopPosition: should get scroll top position', () => {
    expect(Math.round(service.getScrollTopPosition())).toBe(0);
  });

  it('#scrollTop: should set scroll top position', () => {
    const elemStub = {
      scrollTop: 10
    } as any;
    service.scrollTop(elemStub, 20);
    expect(elemStub.scrollTop).toBe(20);
    elemStub.scrollTop = undefined;
    service.scrollTop(elemStub, 10);
    expect(elemStub.scrollTop).toBeUndefined();
  });

  it('#getScrollLeft: should not be scrolled horizontally', () => {
    const elementStub = {
      scrollLeft: 10
    };
    const windowStub = {
      scrollX: 5
    };
    expect(service.getScrollLeft(elementStub as Element)).toBe(10);
    expect(service.getScrollLeft(windowStub as Window)).toBe(5);
    expect(service.getHeight(null)).toBe(0);
  });

  it('#getOffset: should get offset of an element', () => {
    const testHTMLElement = document.createElement('div');
    testHTMLElement.setAttribute('style', 'position: relative;');
    const childElement = document.createElement('div');
    childElement.setAttribute('style', 'position: absolute; top: 10px; left: 20px;');
    testHTMLElement.appendChild(childElement);
    document.body.insertBefore(testHTMLElement, document.body.firstChild);

    expect(service.getOffset(null)).toBeNull();
    const parent = service.getOffset(testHTMLElement);
    const child = service.getOffset(childElement);
    expect(Math.round(child.top - parent.top)).toBe(10);
    expect(Math.round(child.left - parent.left)).toBe(20);

    document.body.removeChild(testHTMLElement);
  });

  it('#toggleVisibility: should toggle visibility of an element', () => {
    const elemStub = {
      style: {
        display: 'block'
      }
    } as any;
    spyOn(window, 'getComputedStyle').and.returnValue(elemStub.style);
    service.toggleVisibility(elemStub);
    expect(elemStub.style.display).toBe('none');
    service.toggleVisibility(elemStub);
    expect(elemStub.style.display).toBe('block');
  });

  it('#removeClass: should remove class from element', () => {
    spyOn(service, 'toggleClass');
    service.removeClass({} as any, 'x');
    expect(service.toggleClass).toHaveBeenCalledWith({} as any, 'x', false);
  });

  it('#addClass: should add class to element', () => {
    spyOn(service, 'toggleClass');
    service.addClass({} as any, 'x');
    expect(service.toggleClass).toHaveBeenCalledWith({} as any, 'x', true);
  });

  it('#hasClass: should check if element has a class', () => {
    const elemStub = {
      classList: {
        contains: (className) => true
      },
      className: 'x'
    } as any;
    expect(service.hasClass(elemStub, '')).toBe(true);
  });

  it('#toggleClass: should toggle two classes of element', () => {
    const elemStub = {
      classList: {
        add: jasmine.createSpy(),
        remove: jasmine.createSpy(),
        toggle: jasmine.createSpy()
      },
      className: 'x y z'
    } as any;
    service.toggleClass(elemStub, 'z');
    expect(elemStub.classList.toggle).toHaveBeenCalledWith('z');
    service.toggleClass(elemStub, 'z', true);
    expect(elemStub.classList.add).toHaveBeenCalledWith('z');
    service.toggleClass(elemStub, 'z', false);
    expect(elemStub.classList.remove).toHaveBeenCalledWith('z');
    elemStub.classList = null;
    service.toggleClass(elemStub, 'x', false);
    expect(elemStub.className).toBe('y z');
    service.toggleClass(elemStub, 'y', true);
    expect(elemStub.className).toBe('y z');
  });

  describe('isChild', () => {
    it('should check if one element is a child of another', () => {
      let parentStub = {} as any;
      const childElemStub = {
        parentNode: parentStub
      } as any;
      expect(service.isChild(childElemStub, parentStub)).toBe(true);
      childElemStub.parentNode = null;
      expect(service.isChild(childElemStub, parentStub)).toBe(false);
      parentStub = null;
      childElemStub.parentNode = {};
      expect(service.isChild(childElemStub, null)).toBe(false);
    });

    it('should check case when parentNode and target are null', () => {
      const childElement = {
        parentNode: null
      } as any;
      const parent = null;

      expect(service.isChild(childElement, parent)).toBeFalsy();
    });

    it('should check case when parentNode of childElement is null', () => {
      const childElement = {
        parentNode: null
      } as any;
      const parent = {} as any;

      expect(service.isChild(childElement, parent)).toBeFalsy();
    });

    it('should check case when parent  is null', () => {
      const childElement = {
        parentNode: {}
      } as any;
      const parent = null as any;

      expect(service.isChild(childElement, parent)).toBeFalsy();
    });

    it('should check recursion call case when parent  is null', () => {
      const childElement = {
        parentNode: {
          parentNode: null
        }
      } as any;
      const parent = {} as any;

      expect(service.isChild(childElement, parent)).toBeFalsy();
    });
  });

  it('#closest: should find closest element up over the DOM tree by selector', () => {
    const parentStub = {
      querySelectorAll: (selector) => [childElemStub],
      parentNode: null
    } as any;
    const childElemStub = {
      querySelectorAll: (selector) => [],
      parentNode: parentStub
    } as any;
    expect(service.closest(childElemStub, '')).toEqual(childElemStub);
    expect(service.closest(parentStub, '')).toBeNull();
  });

  it('#innerHeight: should get height of an element', () => {
    spyOn(window, 'getComputedStyle').and.returnValue({ height: 1 } as any);
    expect(service.innerHeight(null)).toBe(0);
    expect(service.innerHeight({} as any)).toBe(1);
  });

  describe('#getParentByLevel', () => {
    it('should get parent by level with selector', () => {
      const level = 0;
      const ElemStub = {
        parentNode: {},
        querySelector: jasmine.createSpy('querySelector').and.returnValue('selector')
      } as any;
      expect(service.getParentByLevel(ElemStub, level, 'selector')).toEqual('selector' as any);
    });

    it('#should get parent by level without selector', () => {
      const level = 0;
      const ElemStub = {
        parentNode: {}
      } as any;
      expect(service.getParentByLevel(ElemStub, level)).toEqual(ElemStub);
    });

    it('should get parent by level if level > 0 and element.parentNode', () => {
      const level = 1;
      const ElemStub = {
        parentNode: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue('selector')
        }
      } as any;
      expect(service.getParentByLevel(ElemStub, level, 'selector')).toEqual('selector' as any);
    });

    it('should get parent by level if level > 0 and not element.parentNode', () => {
      const level = 1;
      const ElemStub = {
        parentNode: null
      } as any;
      expect(service.getParentByLevel(ElemStub, level, 'selector')).toEqual(null);
    });
  });

  it('#getOuterHeight: should coalculate outer height along with margins of an element', () => {
    const elemStub = {
      offsetHeight: 10
    } as any;
    spyOn(window, 'getComputedStyle').and.returnValue({ marginTop: 10, marginBottom: 20 } as any);
    expect(service.getOuterHeight(elemStub)).toBe(40);
  });
  it('#getOuterHeight: should not calculate outer height along with margins of an element', () => {
    const elemStub = null;
    spyOn(window, 'getComputedStyle').and.returnValue(null);
    expect(service.getOuterHeight(elemStub)).not.toBe(40);
  });

  it('#css: add string/number/object value property', () => {
    const elemStub = {
      style: {}
    } as any;
    spyOn(window, 'getComputedStyle').and.returnValue({ 'marginTop': '10px' } as any);
    service.css(elemStub, 'color', 'blue');
    expect(elemStub.style['color']).toBe('blue');
    service.css(elemStub, 'opacity', 1);
    expect(elemStub.style['opacity']).toBe(1);
    service.css(elemStub, { color: 'red', float: 'none' });
    expect(elemStub.style['float']).toBe('none');
    elemStub.style = {};
    service.css(elemStub, 'marginTop');
  });

  it('#setTranslate: should set CSS transform properties', () => {
    const elemStub = {
      style: {}
    } as any;
    spyOn(service, 'css').and.callFake(function (elem, obj) {
      elem.style = obj;
    } as any);
    service.setTranslate(elemStub);
    expect(elemStub.style.transform).toBe('translate(0px, 0px) ');
    service.setTranslate(elemStub, 1, 2, 3, 4);
    expect(elemStub.style.transform).toBe('translate(1px, 2px) scale(3, 4)');
  });

  it('scrollPageTop', () => {
    service.scrollPageTop(100);
    expect(windowRef.document.body.scrollTop).toBe(100);
    expect(windowRef.document.documentElement.scrollTop).toBe(100);
    expect(windowRef.document.querySelector).toHaveBeenCalledWith('html, body');
  });

  it('getPageScrollTop', () => {
    windowRef.document.body.scrollTop = 100;
    expect(service.getPageScrollTop()).toEqual(100);

    windowRef.document.body.scrollTop = 0;
    windowRef.document.documentElement.scrollTop = 100;
    expect(service.getPageScrollTop()).toEqual(100);

    windowRef.document.body.scrollTop = 0;
    windowRef.document.documentElement.scrollTop = 0;
    expect(service.getPageScrollTop()).toEqual(0);
  });

  describe('#scrollStop', () => {
    beforeEach(() => {
      windowRef.nativeWindow.setTimeout.and.callFake(cb => {
        cb();
        return 'fakeTimeout';
      });
      windowRef.nativeWindow.addEventListener.and.callFake((event, handler, config) => {
        if (event === 'scroll') {
          handler();
        }

        return () => { };
      });
    });

    it('callback is undefined', () => {
      const result = service.scrollStop(undefined);
      expect(windowRef.nativeWindow.addEventListener).not.toHaveBeenCalled();
      expect(result).toBeUndefined();
    });

    it('callback is defined', () => {
      const result = service.scrollStop(() => { });
      expect(windowRef.nativeWindow.addEventListener).toHaveBeenCalledWith('scroll', jasmine.any(Function), false);
      expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalled();
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();

      expect(result).toEqual(jasmine.any(Function));
    });

    it('setHeader', () => {
      windowRef.document.querySelector.and.returnValue(header);
      service['setHeader']();
      expect(service.header).toBe(header);
      expect(windowRef.document.querySelector).toHaveBeenCalledWith('header.header');
    });

    it('setContent', () => {
      windowRef.document.querySelector.and.returnValue(content);
      service['setContent']();
      expect(service.content).toBe(content);
      expect(windowRef.document.querySelector).toHaveBeenCalledWith('#content');
    });

    it('setFooter', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.returnValue(footer);
      service['setFooter']();
      expect(service.footer).toBe(footer);
      expect(windowRef.document.querySelector).toHaveBeenCalledWith('.footer-menu');
    });
  });
});
