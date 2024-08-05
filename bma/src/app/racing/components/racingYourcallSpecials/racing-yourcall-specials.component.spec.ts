import { RacingYourcallSpecialsComponent } from '@racing/components/racingYourcallSpecials/racing-yourcall-specials.component';

describe('#RacingYourcallSpecialsComponent', () => {
  let component: RacingYourcallSpecialsComponent;
  let filtersService;
  let deviceService;
  let racingGaService;
  let elementRef;
  let rendererService;
  let windowRefService;
  let localeService;

  beforeEach(() => {
    filtersService = {
      orderBy: jasmine.createSpy('orderBy')
    };
    deviceService = {};
    racingGaService = {
      trackYourcallSpecials: jasmine.createSpy('trackYourcallSpecials')
    };
    elementRef = {
      nativeElement: {}
    };
    rendererService = {
      renderer: {
        setStyle: jasmine.createSpy('renderer.setStyle')
      }
    };
    windowRefService = {
      nativeWindow: {
        scrollY: 0
      }
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('yourcallSpecials')
    };

    component = new RacingYourcallSpecialsComponent(filtersService, deviceService, racingGaService, elementRef,
      rendererService, windowRefService, localeService);
  });

  it('constructor', () => {
    expect(component.isExpanded).toBeTruthy();
    expect(component.title).toEqual('yourcallSpecials');
    expect(component.ycWidgetFilter).toEqual('Featured');
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component['prepareSwitchers'] = jasmine.createSpy('prepareSwitchers');
    });

    it('should prepare switchers', () => {
      component.data = [];

      component.ngOnInit();

      expect(component.data).toEqual([]);
      expect(component['container']).toEqual({} as any);
      expect(filtersService.orderBy).not.toHaveBeenCalled();
      expect(component['prepareSwitchers']).toHaveBeenCalled();
    });

    it('should extract selections', () => {
      const selections = [
        { id: '1', displayOrder: 4 },
        { id: '2', displayOrder: 3 },
        { id: '3', displayOrder: 2 },
        { id: '4', displayOrder: 1 }
      ];

      filtersService.orderBy.and.returnValue(selections);
      component.data = [{ selections: selections }] as any;
      component.type = 'widget';

      component.ngOnInit();

      expect(filtersService.orderBy).toHaveBeenCalledWith(selections, ['displayOrder']);
      expect(component['prepareSwitchers']).not.toHaveBeenCalled();
      expect(component.data[0].selections.length).toEqual(3);
      expect(component.data[0].selections).toEqual(selections.reverse().slice(0, 3) as any);
    });
  });

  describe('checkPositionAndToggleSticky', () => {
    const switchersOrContent = { clientHeight: 0, clientTop: 0, clientWidth: 0 };

    beforeEach(() => {
      component['setOffsetTop'] = jasmine.createSpy('setOffsetTop');
      component['setDefaultStyles'] = jasmine.createSpy('setDefaultStyles');
      component['toggleSwitchersVisibility'] = jasmine.createSpy('toggleSwitchersVisibility');
      component['container'] = {
        querySelector: jasmine.createSpy('container.querySelector').and.callFake((selector: string) => {
          return selector && switchersOrContent;
        })
      } as any;
    });

    it('should not check position if device is not mobile', () => {
      component.checkPositionAndToggleSticky();

      expect(component['setOffsetTop']).not.toHaveBeenCalled();
      expect(component['setDefaultStyles']).not.toHaveBeenCalled();
      expect(component['toggleSwitchersVisibility']).not.toHaveBeenCalled();
      expect(rendererService.renderer.setStyle).not.toHaveBeenCalledTimes(6);
      expect(component['container'].querySelector).not.toHaveBeenCalledTimes(4);
    });

    describe('should check position and', () => {
      beforeEach(() => {
        deviceService.isMobileOrigin = true;
        component.offsetTop = 5;
      });

      it('should set default styles', () => {
        component.checkPositionAndToggleSticky();

        expect(component['setDefaultStyles']).toHaveBeenCalled();
        expect(component['toggleSwitchersVisibility']).toHaveBeenCalledWith(0, 0, switchersOrContent as any);
      });

      it('should set custom styles', () => {
        windowRefService.nativeWindow.scrollY = 10;

        component.checkPositionAndToggleSticky();

        expect(component['toggleSwitchersVisibility']).toHaveBeenCalledWith(10, 0, switchersOrContent as any);
        expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(6);
        expect(rendererService.renderer.setStyle).toHaveBeenCalledWith(switchersOrContent, 'position', 'fixed');
        expect(rendererService.renderer.setStyle).toHaveBeenCalledWith(switchersOrContent, 'width', '0px');
        expect(rendererService.renderer.setStyle).toHaveBeenCalledWith(switchersOrContent, 'top', '0px');
        expect(rendererService.renderer.setStyle).toHaveBeenCalledWith(switchersOrContent, 'z-index', '1');
        expect(rendererService.renderer.setStyle).toHaveBeenCalledWith(switchersOrContent, 'box-shadow', '0 2px 4px 0 rgba(0, 0, 0, 0.3)');
        expect(rendererService.renderer.setStyle).toHaveBeenCalledWith(switchersOrContent, 'margin-top', '0px');
      });

      afterEach(() => {
        expect(component.switchersWidth).toEqual(0);
        expect(component['container'].querySelector).toHaveBeenCalledTimes(4);
        expect(component['container'].querySelector).toHaveBeenCalledWith('.switchers-parent');
        expect(component['container'].querySelector).toHaveBeenCalledWith('#header');
        expect(component['container'].querySelector).toHaveBeenCalledWith('.top-bar-inner');
        expect(component['container'].querySelector).toHaveBeenCalledWith('.yc-specials-content');
        expect(component['setOffsetTop']).toHaveBeenCalledWith(switchersOrContent as any);
        expect(component['toggleSwitchersVisibility']).toHaveBeenCalledTimes(1);
      });
    });
  });

  describe('resize', () => {
    beforeEach(() => {
      component.checkPositionAndToggleSticky = jasmine.createSpy('checkPositionAndToggleSticky');
      component.offsetTop = 100;
    });

    it('should note resize if device is not mobile', () => {
      component.resize();

      expect(component.offsetTop).toEqual(100);
      expect(component.checkPositionAndToggleSticky).not.toHaveBeenCalled();
    });

    it('should resize if device is mobile', () => {
      deviceService.isMobileOrigin = true;

      component.resize();

      expect(component.offsetTop).toEqual(0);
      expect(component.checkPositionAndToggleSticky).toHaveBeenCalled();
    });
  });

  it('trackById', () => {
    expect(component.trackById(1, { id: 'eventId' } as any)).toEqual('1eventId');
  });

  describe('@changeFilter', () => {
    it('should switch to proper filter', () => {
      component.changeFilter('Featured');
      expect(component.ycWidgetFilter).toEqual('Featured');
    });
  });

  it('trackYourcallSpecials', () => {
    component.trackYourcallSpecials();

    expect(racingGaService.trackYourcallSpecials).toHaveBeenCalled();
  });

  it('prepareSwitchers', () => {
    component.changeFilter.bind = jasmine.createSpy('changeFilter.bind').and.returnValue(component.changeFilter);
    component.data = [{ name: 'marketName' }] as any;

    filtersService.orderBy.and.callFake((data: any[], fields: string[]) => data);

    component['prepareSwitchers']();

    expect(component.switchers).toEqual([{
      name: 'marketName',
      viewByFilters: 'marketName',
      onClick: jasmine.any(Function)
    }]);
    expect(component.changeFilter.bind).toHaveBeenCalled();
    expect(component.ycWidgetFilter).toEqual('marketName');
    expect(filtersService.orderBy).toHaveBeenCalledWith([{ name: 'marketName' }], ['displayOrder']);
  });

  describe('setOffsetTop', () => {
    let switchers;

    beforeEach(() => {
      switchers = {
        getAttribute: jasmine.createSpy('getAttribute'),
        clientTop: 0
      };
    });

    it('should set offset top', () => {
      switchers.getAttribute.and.returnValue('absolute');

      component['setOffsetTop'](switchers);

      expect(component.offsetTop).toEqual(0);
    });

    it('should set offset if switchers position is static', () => {
      switchers.getAttribute.and.returnValue('static');

      component['setOffsetTop'](switchers);

      expect(component.offsetTop).toEqual(0);
    });

    it('should set offset if switchers position is relative', () => {
      switchers.getAttribute.and.returnValue('relative');

      component['setOffsetTop'](switchers);

      expect(component.offsetTop).toEqual(0);
    });

    it('should not set offset if it is already defined', () => {
      component.offsetTop = 100;

      component['setOffsetTop'](switchers);

      expect(component.offsetTop).toEqual(100);
    });

    afterEach(() => {
      expect(switchers.getAttribute).toHaveBeenCalledWith('position');
    });
  });

  describe('toggleSwitchersVisibility', () => {
    it('should hide switchers', () => {
      component['toggleSwitchersVisibility'](10, 10, {} as any);

      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'display', 'none');
    });

    it('should show switchers', () => {
      component['toggleSwitchersVisibility'](5, 10, {} as any);

      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'display', 'flex');
    });
  });

  it('setDefaultStyles should set default styles', () => {
    component['setDefaultStyles']({} as any, {} as any);

    expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(5);
    expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'width', '100%');
    expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'position', 'relative');
    expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'top', '0px');
    expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'box-shadow', 'none');
    expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({}, 'margin-top', '0px');
  });
});
