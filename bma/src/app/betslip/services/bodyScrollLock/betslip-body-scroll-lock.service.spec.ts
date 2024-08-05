import { BodyScrollLockService } from '@betslip/services/bodyScrollLock/betslip-body-scroll-lock.service';

describe('BodyScrollLockService', () => {
  let service: BodyScrollLockService;
  let windowRef;
  let rendererFactory;
  let renderer2;
  let ngZone;

  beforeEach(() => {
    renderer2 = {
      listen: jasmine.createSpy('listen').and.returnValue(() => {})
    };

    windowRef = {
      document: {}
    };
    rendererFactory = {
      createRenderer: jasmine.createSpy('createRenderer').and.returnValue(renderer2)
    };

    ngZone = {
      runOutsideAngular: jasmine.createSpy('runOutsideAngular').and.callFake((fn) => fn())
    };

    service = new BodyScrollLockService(windowRef as any, rendererFactory as any, ngZone as any);
  });

  it('should create service', () => {
    expect(service).toBeTruthy();
    expect(rendererFactory.createRenderer).toHaveBeenCalledWith(null, null);
    expect(service['renderer']).toBeDefined();
  });

  describe('disableBodyScroll', () => {
    const element = {};
    const clientY = 155;
    const event = {
      targetTouches: [{
        clientY: clientY
      }]};

    beforeEach(() => {
      spyOn<any>(service, 'handleScroll');
      spyOn<any>(service, 'preventDefault');
    });

    it('should not lock scroll if no element', () => {
      service['isBodyScrollLocked'] = false;
      service.disableBodyScroll(null);

      expect(service['isBodyScrollLocked']).toEqual(false);
      expect(service['elTouchStartSub']).not.toBeDefined();
      expect(service['elTouchMoveSub']).not.toBeDefined();
      expect(service['windowTouchMoveSub']).not.toBeDefined();
      expect(service['renderer'].listen).not.toHaveBeenCalled();
    });

    it('should lock scroll', () => {
      service['isBodyScrollLocked'] = false;
      service.disableBodyScroll(element as any);

      expect(service['isBodyScrollLocked']).toEqual(true);
      expect(service['elTouchStartSub']).toEqual(jasmine.any(Function));
      expect(service['elTouchMoveSub']).toEqual(jasmine.any(Function));
      expect(service['windowTouchMoveSub']).toEqual(jasmine.any(Function));
      expect(service['renderer'].listen).toHaveBeenCalledTimes(3);
    });

    it('should not add additional listeners if was locked', () => {
      service['isBodyScrollLocked'] = true;
      service['windowTouchMoveSub'] = undefined;
      service['elTouchStartSub'] = jasmine.createSpy();
      service['elTouchMoveSub'] = jasmine.createSpy();
      service.disableBodyScroll(element as any);

      expect(service['renderer'].listen).toHaveBeenCalledTimes(2);
      expect(service['windowTouchMoveSub']).not.toBeDefined();
    });

    it('should call callbacks', () => {
      service['isBodyScrollLocked'] = false;
      service['renderer'].listen = jasmine.createSpy().and.callFake((a, b, fn) => { fn(event); });
      service.disableBodyScroll(element as any);

      expect(service['initialClientY']).toEqual(clientY);
      expect(service['handleScroll']).toHaveBeenCalledWith(event as any, element as any);
      expect(service['preventDefault']).toHaveBeenCalled();
      expect(ngZone.runOutsideAngular).toHaveBeenCalledWith(jasmine.any(Function));
    });

    it('should not unsubscribe if was not locked', () => {
      const stub = jasmine.createSpy();
      service['elTouchStartSub'] = stub;
      service['elTouchMoveSub'] = stub;
      service['isBodyScrollLocked'] = false;
      service.disableBodyScroll(element as any);

      expect(stub).not.toHaveBeenCalled();
    });

    it('should unsubscribe if was locked', () => {
      const stub = jasmine.createSpy();
      service['elTouchStartSub'] = stub;
      service['elTouchMoveSub'] = stub;
      service['isBodyScrollLocked'] = true;
      service.disableBodyScroll(element as any);

      expect(stub).toHaveBeenCalledTimes(2);
    });
  });

  describe('enableBodyScroll', () => {
    beforeEach(() => {
      service['initialClientY'] = 100;
      service['elTouchStartSub'] = jasmine.createSpy();
      service['elTouchMoveSub'] = jasmine.createSpy();
      service['windowTouchMoveSub'] = jasmine.createSpy();
    });

    it('should remove all added listeners', () => {
      service['isBodyScrollLocked'] = true;
      service.enableBodyScroll();

      expect(service['initialClientY']).toEqual(-1);
      expect(service['isBodyScrollLocked']).toEqual(false);
      expect(service['elTouchStartSub']).toHaveBeenCalled();
      expect(service['elTouchMoveSub']).toHaveBeenCalled();
      expect(service['windowTouchMoveSub']).toHaveBeenCalled();
    });

    it('should not remove all added listeners', () => {
      service['isBodyScrollLocked'] = false;

      service.enableBodyScroll();

      expect(service['isBodyScrollLocked']).toEqual(false);
      expect(service['initialClientY']).toEqual(100);
      expect(service['elTouchStartSub']).not.toHaveBeenCalled();
      expect(service['elTouchMoveSub']).not.toHaveBeenCalled();
      expect(service['windowTouchMoveSub']).not.toHaveBeenCalled();
    });
  });

  describe('preventDefault', () => {
    it('should prevent', () => {
      const event = {
        preventDefault: jasmine.createSpy()
      };

      expect(service['preventDefault'](event as any)).toEqual(false);
      expect(event.preventDefault).toHaveBeenCalled();
    });

    it('should not prevent', () => {
      const event = {
        preventDefault: jasmine.createSpy()
      };

      expect(service['preventDefault']({} as any)).toEqual(false);
      expect(event.preventDefault).not.toHaveBeenCalled();
    });
  });

  describe('isElementTotallyScrolled', () => {
    it('should return false', () => {
      const element = {
        scrollHeight: 100,
        scrollTop: 20,
        clientHeight: 0
      };

      expect(service['isElementTotallyScrolled'](element as any)).toEqual(false);
    });

    it('should return true', () => {
      const element = {
        scrollHeight: 100,
        scrollTop: 100,
        clientHeight: 100
      };

      expect(service['isElementTotallyScrolled'](element as any)).toEqual(true);
    });
  });

  describe('handleScroll', () => {
    let event;
    let element;

    beforeEach(() => {
      spyOn<any>(service, 'preventDefault').and.returnValue(false);
      event = {
        stopPropagation: jasmine.createSpy('stopPropagation'),
        targetTouches: [{
          clientY: 0
        }]
      };
      element = {
        scrollTop: 0
      };
    });

    it('should return true when not fully in the top', () => {
      service['initialClientY'] = 50;
      event.targetTouches[0].clientY = 100;
      element.scrollTop = 10;

      const result = service['handleScroll'](event as any, element as any);

      expect(event.stopPropagation).toHaveBeenCalled();
      expect(service['preventDefault']).not.toHaveBeenCalled();
      expect(result).toEqual(true);
    });

    it('should return false and stop propagation for the top position ', () => {
      service['initialClientY'] = 50;
      event.targetTouches[0].clientY = 100;
      element.scrollTop = 0;

      const result = service['handleScroll'](event as any, element as any);

      expect(event.stopPropagation).not.toHaveBeenCalled();
      expect(service['preventDefault']).toHaveBeenCalledWith(event);
      expect(result).toEqual(false);
    });

    it('should return true when not fully in the bottom', () => {
      service['initialClientY'] = 1000;
      event.targetTouches[0].clientY = 100;
      spyOn<any>(service, 'isElementTotallyScrolled').and.returnValue(false);

      const result = service['handleScroll'](event as any, element as any);

      expect(event.stopPropagation).toHaveBeenCalled();
      expect(service['preventDefault']).not.toHaveBeenCalled();
      expect(result).toEqual(true);
    });

    it('should return false and stop propagation for the bottom position ', () => {
      service['initialClientY'] = 1000;
      event.targetTouches[0].clientY = 100;
      spyOn<any>(service, 'isElementTotallyScrolled').and.returnValue(true);

      const result = service['handleScroll'](event as any, element as any);

      expect(event.stopPropagation).not.toHaveBeenCalled();
      expect(service['preventDefault']).toHaveBeenCalledWith(event);
      expect(result).toEqual(false);
    });
  });
});
