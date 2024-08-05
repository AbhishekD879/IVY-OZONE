import { fakeAsync, tick } from '@angular/core/testing';
import { EventEmitter } from '@angular/core';

import { LazyComponent } from './lazy-component.component';

describe('LazyComponent', () => {
  let component: LazyComponent;
  let lazyComponentFactory;
  let applicationRef;
  let windowRef;
  let changeDetectRef;

  beforeEach(() => {
    applicationRef = {
      tick: jasmine.createSpy('tick')
    };
    lazyComponentFactory = jasmine.createSpyObj(['createLazyComponent']);
    windowRef = {
      nativeWindow: {
        clearTimeout: jasmine.createSpy('clearTimeout'),
        setTimeout: jasmine.createSpy('setTimeout')
      }
    };
    changeDetectRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    component = new LazyComponent(lazyComponentFactory, applicationRef, windowRef, changeDetectRef);
  });

  describe('ngAfterViewInit', () => {
    beforeEach(() => {
      spyOn<any>(component, 'createComponentByUri');
    });

    it('ngAfterViewInit', () => {
      component.ngAfterViewInit();

      expect(component['createComponentByUri']).not.toHaveBeenCalled();
    });

    it('ngAfterViewInit', () => {
      component.moduleUri = 'some/path/to/module';
      component.ngAfterViewInit();

      expect(component['createComponentByUri']).toHaveBeenCalled();
    });
  });

  it('ngOnChanges', () => {
    component['shouldUpdateInputs'] = jasmine.createSpy().and.returnValue(true);
    component['updateInputs'] = jasmine.createSpy();
    component['formatChanges'] = jasmine.createSpy();
    component['componentRef'] = { instance: { ngOnChanges: jasmine.createSpy() } } as any;
    component.ngOnChanges({});

    expect(component['shouldUpdateInputs']).toHaveBeenCalled();
    expect(component['updateInputs']).toHaveBeenCalled();
    expect(component['componentRef'].instance.ngOnChanges).toHaveBeenCalled();
  });

  it('ngOnChanges falsy', () => {
    component['shouldUpdateInputs'] = jasmine.createSpy().and.returnValue(true);
    component['updateInputs'] = jasmine.createSpy();
    component['formatChanges'] = jasmine.createSpy();
    component['componentRef'] = null;
    component.ngOnChanges({});

    expect(component['shouldUpdateInputs']).toHaveBeenCalled();
    expect(component['updateInputs']).toHaveBeenCalled();
    expect(component['formatChanges']).not.toHaveBeenCalled();
  });

  it('ngOnChanges falsy 2', () => {
    component['shouldUpdateInputs'] = jasmine.createSpy().and.returnValue(true);
    component['updateInputs'] = jasmine.createSpy();
    component['formatChanges'] = jasmine.createSpy();
    component['componentRef'] = { instance: { ngOnChanges: null } } as any;
    component.ngOnChanges({});

    expect(component['shouldUpdateInputs']).toHaveBeenCalled();
    expect(component['updateInputs']).toHaveBeenCalled();
    expect(component['formatChanges']).not.toHaveBeenCalled();
  });

  it('ngOnDestroy', () => {
    component['destroyComponent'] = jasmine.createSpy();
    component.ngOnDestroy();
    expect(component['destroyComponent']).toHaveBeenCalled();
    expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalled();
  });

  describe('createComponentByUri', () => {
    it('should handle success module loading', fakeAsync(() => {
      const container = {};
      const moduleUri = 'some/module/uri';
      const data = { instance: {}, location: {nativeElement: {
        localName: 'multi-market-template'
      }} } as any;

      component.state.loading = true;
      component.container = container as any;
      component.moduleUri = moduleUri;
      component.entryComponent = null;
      lazyComponentFactory.createLazyComponent.and.returnValue(Promise.resolve(data));
      component['updateInputs'] = jasmine.createSpy();
      component['subscribeToOutputs'] = jasmine.createSpy();
      component.init.emit = jasmine.createSpy();
      component['createComponentByUri']();

      tick();
      expect(lazyComponentFactory.createLazyComponent).toHaveBeenCalledWith(component.moduleUri, container, null);
      expect(component['componentRef']).toEqual(data);
      expect(component['updateInputs']).toHaveBeenCalled();
      expect(component['subscribeToOutputs']).toHaveBeenCalled();
      expect(component.init.emit).toHaveBeenCalled();
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(component.state.loading).toBeFalsy();
    }));

    it('should handle success module loading case 2', fakeAsync(() => {
      const container = {};
      const moduleUri = 'some/module/uri';
      const data = { instance: {}, location: {nativeElement: {
        localName: 'multi-market-template'
      }} } as any;

      component.state.loading = true;
      component.container = container as any;
      component.moduleUri = moduleUri;
      component.entryComponent = null;
      lazyComponentFactory.createLazyComponent.and.returnValue(Promise.resolve(data));
      component['updateInputs'] = jasmine.createSpy();
      component['subscribeToOutputs'] = jasmine.createSpy();
      component.init.emit = jasmine.createSpy();
      component['createComponentByUri']();

      tick();
      expect(lazyComponentFactory.createLazyComponent).toHaveBeenCalledWith(component.moduleUri, container, null);
      expect(component['componentRef']).toEqual(data);
      expect(component['updateInputs']).toHaveBeenCalled();
      expect(component['subscribeToOutputs']).toHaveBeenCalled();
      expect(component.init.emit).toHaveBeenCalled();
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(component.state.loading).toBeFalsy();
    }));

    it('should handle success module loading case 3', fakeAsync(() => {
      const container = {};
      const moduleUri = 'some/module/uri';
      const data = { instance: { changeStrategy: 'onpush' }, location: {nativeElement: {
        localName: 'multi-market-template'
      }}  } as any;

      component.state.loading = true;
      component.container = container as any;
      component.moduleUri = moduleUri;
      component.entryComponent = null;
      lazyComponentFactory.createLazyComponent.and.returnValue(Promise.resolve(data));
      component['updateInputs'] = jasmine.createSpy();
      component['subscribeToOutputs'] = jasmine.createSpy();
      component.init.emit = jasmine.createSpy();
      component['createComponentByUri']();

      tick();
      expect(lazyComponentFactory.createLazyComponent).toHaveBeenCalledWith(component.moduleUri, container, null);
      expect(component['componentRef']).toEqual(data);
      expect(component['updateInputs']).toHaveBeenCalled();
      expect(component['subscribeToOutputs']).toHaveBeenCalled();
      expect(component.init.emit).toHaveBeenCalled();
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(component.state.loading).toBeFalsy();
    }));
    it('should handle success module with tote-free-bets-toggle', fakeAsync(() => {
      const container = {};
      const moduleUri = 'some/module/uri';
      const data = { instance: { changeStrategy: 'default' }, location: {nativeElement: {
        localName: 'tote-free-bets-toggle'
      }}  } as any;

      component.state.loading = true;
      component.container = container as any;
      component.moduleUri = moduleUri;
      component.entryComponent = null;
      lazyComponentFactory.createLazyComponent.and.returnValue(Promise.resolve(data));
      component['updateInputs'] = jasmine.createSpy();
      component['subscribeToOutputs'] = jasmine.createSpy();
      component.init.emit = jasmine.createSpy();
      component['createComponentByUri']();

      tick();
      expect(lazyComponentFactory.createLazyComponent).toHaveBeenCalledWith(component.moduleUri, container, null);
      expect(component['componentRef']).toEqual(data);
      expect(component['updateInputs']).toHaveBeenCalled();
      expect(component['subscribeToOutputs']).toHaveBeenCalled();
      expect(component.init.emit).toHaveBeenCalled();
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(component.state.loading).toBeFalsy();
    }));

    it('should handle success module loading case4', fakeAsync(() => {
      const container = {};
      const moduleUri = 'some/module/uri';
      const data = { instance: { changeStrategy: 'default' }, location: {nativeElement: {
        localName: 'multi-market-template'
      }}  } as any;

      component.state.loading = true;
      component.container = container as any;
      component.moduleUri = moduleUri;
      component.entryComponent = null;
      lazyComponentFactory.createLazyComponent.and.returnValue(Promise.resolve(data));
      component['updateInputs'] = jasmine.createSpy();
      component['subscribeToOutputs'] = jasmine.createSpy();
      component.init.emit = jasmine.createSpy();
      component['createComponentByUri']();

      tick();
      expect(lazyComponentFactory.createLazyComponent).toHaveBeenCalledWith(component.moduleUri, container, null);
      expect(component['componentRef']).toEqual(data);
      expect(component['updateInputs']).toHaveBeenCalled();
      expect(component['subscribeToOutputs']).toHaveBeenCalled();
      expect(component.init.emit).toHaveBeenCalled();
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(component.state.loading).toBeFalsy();
    }));


    it('should handle failed module loading', fakeAsync(() => {
      const container = {};
      const moduleUri = 'some/module/uri';

      component.state.loading = true;
      component.state.error = false;
      component.container = container as any;
      component.moduleUri = moduleUri;
      component.entryComponent = null;
      lazyComponentFactory.createLazyComponent.and.returnValue(Promise.reject('error'));

      component['createComponentByUri']();

      tick();
      expect(component.state.loading).toBeFalsy();
      expect(component.state.error).toBeTruthy();
    }));
  });

  it('destroyComponent', () => {
    const ouputUnsubSpy = jasmine.createSpy();
    component['outputSubs'] = [
      { unsubscribe: ouputUnsubSpy }, { unsubscribe: ouputUnsubSpy }
    ] as any;
    component['componentRef'] = { destroy: jasmine.createSpy() } as any;

    component['destroyComponent']();

    expect(ouputUnsubSpy).toHaveBeenCalledTimes(2);
    expect(component['componentRef'].destroy).toHaveBeenCalled();
  });

  it('updateInputs', () => {
    component['componentRef'] = { instance: { x: 0 } } as any;
    component['inputs'] = { x: 1, y: 2 };

    component['updateInputs']();

    expect(component['componentRef'].instance).toEqual(
      jasmine.objectContaining({ x: 1, y: 2 })
    );
  });

  it('formatChanges', () => {
    component['inputs'] = { previousValue: { x: 1, y: 2, z: 3 }, currentValue: { x: 3, y: 4, z: 3 } };
    const mockDataIn = {
      inputs: {
        previousValue: { x: 1, y: 2, z: 3 }, currentValue: { x: 3, y: 4, z: 3 },
        isFirstChange: jasmine.any(Function), firstChange: false
      }
    };
    const mockDataOut = { x: { previousValue: 1, currentValue: 3 }, y: { previousValue: 2, currentValue: 4 } } as any;
    expect(component['formatChanges'](mockDataIn as any)).toEqual(mockDataOut);
  });

  it('shouldUpdateInputs', () => {
    expect(
      component['shouldUpdateInputs']({})
    ).toBeFalsy();

    expect(
      component['shouldUpdateInputs']({
        inputs: {
          firstChange: true, previousValue: undefined, currentValue: { x: 1 }
        }
      } as any)
    ).toBeTruthy();

    expect(
      component['shouldUpdateInputs']({
        inputs: {
          firstChange: false, previousValue: { x: 1 }, currentValue: { x: 1 }
        }
      } as any)
    ).toBeFalsy();

    expect(
      component['shouldUpdateInputs']({
        inputs: {
          firstChange: false, previousValue: { x: 1 }, currentValue: { x: 2 }
        }
      } as any)
    ).toBeTruthy();
  });

  it('subscribeToOutputs', () => {
    const subscribeSpies = {} as any;
    const instance = {
      edit: new EventEmitter(),
      remove: new EventEmitter(),
      like: new EventEmitter()
    };

    Object.entries(instance).forEach(value => {
      value[1].subscribe = subscribeSpies[value[0]] = jasmine.createSpy().and.returnValue({ unsubscribe: () => { } });
    });

    component.outputs = ['edit', 'remove'];
    component['componentRef'] = { instance } as any;

    component['subscribeToOutputs']();

    expect(subscribeSpies.edit).toHaveBeenCalled();
    expect(subscribeSpies.remove).toHaveBeenCalled();
    expect(subscribeSpies.like).not.toHaveBeenCalled();
  });

  it('@reloadComponent should call loadComponent', () => {
    component['loadComponent'] = jasmine.createSpy('loadComponent');
    component.reloadComponent();
    expect(component['loadComponent']).toHaveBeenCalledTimes(1);
  });
});
