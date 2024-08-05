import { AccordionComponent } from './accordion.component';

describe('AccordionComponent', () => {
  let accordionService;
  let gtmService;
  let component: AccordionComponent;
  let event;
  let changeDetectorRef;
  let pubSubService;

  beforeEach(() => {
    accordionService = {
      saveStateDependsOnParams: jasmine.createSpy(),
      getLocationStates: jasmine.createSpy(),
      getState: jasmine.createSpy()
    };
    gtmService = {
      push: jasmine.createSpy()
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        WS_EVENT_UPDATE: 'WS_EVENT_UPDATE'
      }
    };

    event = {
      preventDefault: jasmine.createSpy('preventDefault'),
      stopPropagation: jasmine.createSpy('stopPropagation')
    };

    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy('detectChanges')
    };

    component = new AccordionComponent(
      accordionService,
      gtmService,
      changeDetectorRef,
      pubSubService,
    );
  });

  it('ngOnInit', () => {
    component.setHeaderClass = jasmine.createSpy();
    component.setState = jasmine.createSpy();
    component.initMemory = jasmine.createSpy();
    component.isExpanded = undefined;
    component.memoryId = '1';
    component.disabled = false;

    component.ngOnInit();

    expect(component.setHeaderClass).toHaveBeenCalled();
    expect(component.isExpanded).toBeTruthy();
    expect(component['initialState']).toBe(component.isExpanded);
    expect(component.setState).toHaveBeenCalledWith(component['initialState']);
    expect(component['initMemory']).toHaveBeenCalledWith(component['initialState']);
  });

  it('should handle WS_EVENT_UPDATE event', () => {
    pubSubService.subscribe.and.callFake((name, channel, cb) => {
      if (channel === 'WS_EVENT_UPDATE') {
        cb();
      }
    });
    component.ngOnInit();
    expect(pubSubService.subscribe).toHaveBeenCalledWith('accSocketUpdate', 'WS_EVENT_UPDATE', jasmine.any(Function));
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });

  it('setHeaderClass', () => {
    component.headerClass = 'header';
    component.disabled = false;
    component.inner = true;

    component.setHeaderClass();

    expect(component.setHeaderClass()).toEqual({
      'toggle-header': true,
      'inner-header': true,
      'header': 'header',
      'hr-header': false
    });
  });
  it('setHeaderClass if isCustomElement is true', () => {
    component.headerClass = 'header';
    component.disabled = false;
    component.isCustomElement = true

    component.setHeaderClass();

    expect(component.setHeaderClass()).toEqual({
      'toggle-header': true,
      'inner-header': false,
      'header': 'header',
      'hr-header': undefined
    });
  });

  it('setHeaderClass if isCustomElement and inner is true', () => {
    component.headerClass = 'header';
    component.disabled = false;
    component.isCustomElement = true;
    component.inner = true;

    component.setHeaderClass();

    expect(component.setHeaderClass()).toEqual({
      'toggle-header': true,
      'inner-header': false,
      'header': 'header',
      'hr-header': true
    });
  });

  it('setState (memory enabled)', () => {
    component['memoryEnabled'] = true;
    component.setState(true);
    expect(component.isExpanded).toBeTruthy();
    expect(accordionService.saveStateDependsOnParams).toHaveBeenCalledWith(
      true, component.memoryId, component.memoryLocation
    );
  });

  it('setState (memory disabled)', () => {
    component['memoryEnabled'] = false;
    component.setState(true);
    expect(component.isExpanded).toBeTruthy();
    expect(accordionService.saveStateDependsOnParams).not.toHaveBeenCalledWith();
  });

  it('toggled (disabled)', () => {
    component.disabled = true;
    component.setState = jasmine.createSpy();

    component.toggled(event);
    expect(component.setState).not.toHaveBeenCalled();
    expect(event.preventDefault).not.toHaveBeenCalled();
    expect(event.stopPropagation).not.toHaveBeenCalled();
  });

  it('toggled (enabled)', () => {
    component.disabled = false;
    component.setState = jasmine.createSpy();
    component.trackLabel = 'lbl';
    component.trackCategory = 'cat';
    component.isExpanded = true;
    component.func.emit = jasmine.createSpy();

    component.toggled(event);

    expect(component.setState).toHaveBeenCalledWith(false);
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      event: 'trackEvent',
      eventCategory: component.trackCategory,
      eventAction: 'show',
      eventLabel: component.trackLabel
    });
    expect(component.func.emit).toHaveBeenCalledWith(true);
    expect(event.preventDefault).toHaveBeenCalled();
    expect(event.stopPropagation).toHaveBeenCalled();
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });

  it('toggled (enabled) for undefined emit function', () => {
    component.disabled = false;
    component.setState = jasmine.createSpy();
    component.trackLabel = 'lbl';
    component.trackCategory = 'cat';
    component.isExpanded = true;
    component.func = undefined;

    component.toggled(event);
    expect(component.func).toBeUndefined();
  });

  it('initMemory (memory location set)', () => {
    component.setState = jasmine.createSpy();
    component.memoryLocation = '1';
    accordionService.getLocationStates.and.returnValue([]);

    component.initMemory(true);

    expect(component['memoryEnabled']).toBeTruthy();
    expect(accordionService.getLocationStates).toHaveBeenCalledWith(
      component.memoryLocation
    );
    expect(component.setState).toHaveBeenCalledTimes(1);
  });

  it('initMemory (memory location unset)', () => {
    component.setState = jasmine.createSpy();
    component.memoryLocation = '';

    component.initMemory(true);

    expect(component['memoryEnabled']).toBeTruthy();
    expect(accordionService.getState).toHaveBeenCalledWith(component.memoryId);
    expect(component.setState).toHaveBeenCalledTimes(1);
  });

  it('initMemory (memory location set)', () => {
    component.setState = jasmine.createSpy();
    component.memoryLocation = '';
    accordionService.getState.and.returnValue('test');

    component.initMemory(true);
    expect(component.setState).toHaveBeenCalledTimes(1);
  });

  it('initMemory (memory location set)', () => {
    component.setState = jasmine.createSpy();
    component.memoryLocation = '';
    accordionService.getState.and.returnValue(null);

    component.initMemory(true);
    expect(component.setState).toHaveBeenCalledTimes(1);
  });

  it('initMemory (memory location set)', () => {
    component.setState = jasmine.createSpy();
    component.memoryLocation = '';
    accordionService.getState.and.returnValue(undefined);

    component.initMemory(true);
    expect(component.setState).toHaveBeenCalledTimes(1);
  });
  
  describe('trackToggle', () => {
    it('shouldn\'t send analytics if trackLabel isn\'t set', () => {
      component.trackCategory = 'trackCategory1';
      component.trackToggle();
      expect(gtmService.push).not.toHaveBeenCalled();
    });
    it('shouldn\'t send analytics if trackLabel isn\'t set', () => {
      component.trackLabel = 'trackLabel1';
      component.trackToggle();
      expect(gtmService.push).not.toHaveBeenCalled();
    });
    it('shouldn\'t track collapse action if trackExpandOnly is true', () => {
      component.trackLabel = 'trackLabel1';
      component.trackCategory = 'trackCategory1';
      component.trackExpandOnly = true;
      component.isExpanded = false;
      component.trackToggle();
      expect(gtmService.push).not.toHaveBeenCalled();
    });
    it('should call push method with provided trackAction', () => {
      component.trackLabel = 'trackLabel1';
      component.trackCategory = 'trackCategory1';
      component.trackExpandOnly = false;
      component.isExpanded = false;
      component.trackAction = 'home/home';
      component.trackToggle();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'trackCategory1',
        eventAction: 'home/home',
        eventLabel: 'trackLabel1'
      });
    });
    it('should call push method with provided show event lavel ' +
      'if event action isn\'t provided', () => {
        component.trackLabel = 'trackLabel1';
        component.trackCategory = 'trackCategory1';
        component.trackExpandOnly = false;
        component.isExpanded = false;
        component.trackToggle();
        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
          event: 'trackEvent',
          eventCategory: 'trackCategory1',
          eventAction: 'hide',
          eventLabel: 'trackLabel1'
        });
      });
    it('should call push method with provided show event lavel ' +
      'if event action isn\'t provided', () => {
        component.trackLabel = 'trackLabel1';
        component.trackCategory = 'trackCategory1';
        component.trackExpandOnly = false;
        component.isExpanded = true;
        component.trackToggle();
        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
          event: 'trackEvent',
          eventCategory: 'trackCategory1',
          eventAction: 'show',
          eventLabel: 'trackLabel1'
        });
      });
  });

  describe('ngOnDestroy', () => {
    it('#ngOnDestroy', () => {
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('accSocketUpdate');
    });
  });
  describe('#inplayHRHeaderLoaded', () => {
    it('should call changeDetectorRef.detectChanges', () => {
      component.inplayHRHeaderLoaded();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });
});
