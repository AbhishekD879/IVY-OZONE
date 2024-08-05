import { DynamicComponentsService } from '@core/services/dynamicComponents/dynamic-components.service';

describe('DynamicComponentsService', () => {
  let service: DynamicComponentsService;
  let componentFactoryResolver, appRef, injector, componentReference, componentInstance;


  beforeEach(() => {
    componentInstance = {
      instance: {},
      hostView: {
        rootNodes: [{}]
      },
      destroy: jasmine.createSpy('destroy')
    };
    componentReference = {
      create: jasmine.createSpy('create').and.returnValue(componentInstance),
      instance: componentInstance
    };
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory')
        .and.returnValue(componentReference)
    };
    appRef = {
      attachView: jasmine.createSpy('attachView'),
      detachView: jasmine.createSpy('detachView')
    };
    injector = {};
    service = new DynamicComponentsService(
      componentFactoryResolver,
      appRef,
      injector
    );
  });

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  describe('#addComponent', () => {
    it('should create proper component', () => {
      const target = {
        insertBefore: jasmine.createSpy('insertBefore')
      } as any;
      const ref = document.createElement('p');
      service.addComponent({}, {}, target, ref);
      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith({});
      expect(appRef.attachView).toHaveBeenCalledWith(componentInstance.hostView);
    });

    it('should return proper component instance', () => {
      const target = {
        insertBefore: jasmine.createSpy('insertBefore')
      } as any;
      const ref = document.createElement('p');
      const comp = service.addComponent({}, {}, target, ref);
      comp.destroy();

      expect(appRef.detachView).toHaveBeenCalledWith(componentInstance.hostView);
      expect(componentInstance.destroy).toHaveBeenCalled();
      expect(comp.instance.isPanelShown).toBeDefined();
    });
  });
});
