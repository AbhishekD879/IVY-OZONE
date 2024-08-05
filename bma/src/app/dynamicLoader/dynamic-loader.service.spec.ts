import { of } from 'rxjs';
import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { } from 'jasmine';
import { Compiler } from '@angular/core';

describe('DynamicLoaderService', () => {
  let manifests,
    loader,
    injector,
    service,
    moduleFactory;
  const compiler = new Compiler();
  beforeEach(() => {
    moduleFactory = { create: jasmine.createSpy('moduleFactory') };
    injector = {
      get: jasmine.createSpy('get').and.returnValue({})
    };
    manifests = {
      find: jasmine.createSpy('find').and.returnValue({ loadChildren: 'loadChildren' })
    };
    loader = {
      getModule: jasmine.createSpy('getModule').and.returnValue(Promise.resolve(moduleFactory))
    };

    service = new DynamicLoaderService(
      compiler,
      injector,
      loader
    );
    service['moduleResolvers'] = {};
  });

  xdescribe('@getComponentFactory', () => {
    let moduleRef;

    beforeEach(() => {
      moduleRef = {
        injector: {
          get: jasmine.createSpy('get')
        },
        componentFactoryResolver: {
          resolveComponentFactory: jasmine.createSpy('resolveComponentFactory')
        }
      };
      service['loadModule'] = jasmine.createSpy('loadModule').and.returnValue(Promise.resolve(moduleRef));
    });

    it('should get object with component factory', () => {
      manifests.find = jasmine.createSpy('find').and.returnValue({ lazyChildren: '' });

      service.getComponentFactory('');

      expect(service['loadModule']).toHaveBeenCalledWith('', undefined);
    });

    it('should get object with component factory and injector to be able dynamically create', () => {
      manifests.find = jasmine.createSpy('find').and.returnValue({ lazyChildren: 'lazyChildren' });
      service.getComponentFactory('componentToken', injector);
      

      expect(service['loadModule']).toHaveBeenCalledWith('lazyChildren', injector);
    });
  });

  describe('@loadModule', () => {
    let modulePath;

    beforeEach(() => {
      modulePath = '@betslipModule/betslip.module#BetslipModule';
    });

    it('should load module by given path', () => {
      const module = {
        BetSlipModule: {}
      } as any;
      const mod = {
        componentFactoryResolver: {}
      } as any;
      const mockModuleFactory = {
        create: jasmine.createSpy('create').and.returnValue(Promise.resolve(mod))
      } as any;
      service.loadModuleFactory = jasmine.createSpy('loadModuleFactory').and.returnValue(Promise.resolve(mockModuleFactory));
      loader.getModule.and.returnValue(Promise.resolve(module));
      service.loadModule(modulePath);
      expect(loader.getModule).toHaveBeenCalledWith('@betslipModule/betslip.module');
    });

    it('should not load module by given path', () => {
      loader.getModule.and.returnValue(Promise.reject('Error'));
      service.moduleResolvers = {'@betslipModule/betslip.module#BetslipModule': ''} as any;
      service.loadModule(modulePath);
      expect(loader.getModule).toHaveBeenCalledWith('@betslipModule/betslip.module');
    });

    it('should get module from moduleResolvers', () => {
      const module = {
        BetSlipModule: {}
      } as any;
      const mod = {
        componentFactoryResolver: {}
      } as any;
      const mockModuleFactory = {
        create: jasmine.createSpy('create').and.returnValue(Promise.resolve(mod))
      } as any;
      service.loadModuleFactory = jasmine.createSpy('loadModuleFactory').and.returnValue(Promise.resolve(mockModuleFactory));
      loader.getModule.and.returnValue(Promise.resolve(module));
      service.moduleResolvers = { '@betslipModule/betslip.module#BetslipModule': '@betslipModule/betslip.module#BetslipModule' };
      service.loadModule(modulePath, injector);
      expect(loader.getModule).not.toHaveBeenCalled();
    });
  });

  xdescribe('@createDynamicComponent', () => {
    let dynamicComp,
      lazyComponent;

    beforeEach(() => {
      dynamicComp = '';
      lazyComponent = {};

      service.getDynamicComponent = jasmine.createSpy('getDynamicComponent');
      service.destroyDynamicComponent = jasmine.createSpy('destroyDynamicComponent');
      service.populateComponentRef = jasmine.createSpy('populateComponentRef');
    });

    it('should lazy load module and get component factory', () => {
      service.createDynamicComponent(dynamicComp, lazyComponent);

      expect(service.getDynamicComponent).toHaveBeenCalledWith(dynamicComp, lazyComponent);
      expect(service.destroyDynamicComponent).not.toHaveBeenCalled();
      expect(service.populateComponentRef).not.toHaveBeenCalled();
    });

    it('should create component', () => {
      lazyComponent = {
        factory: {},
        viewContainer: {
          parentInjector: {},
          createComponent: jasmine.createSpy('createComponent')
        }
      };
      service.createDynamicComponent(dynamicComp, lazyComponent);

      expect(service.getDynamicComponent).not.toHaveBeenCalled();
      expect(service.destroyDynamicComponent).toHaveBeenCalledWith(lazyComponent);
      expect(service.populateComponentRef).toHaveBeenCalledWith(lazyComponent);
    });
  });

  xdescribe('@getDynamicComponent', () => {
    it('should lazy load module, get component factory and create', () => {
      const dynamicComp = '';
      const lazyComponent = {
        viewContainer: {
          parentInjector: {},
          createComponent: jasmine.createSpy('createComponent')
        }
      };
      const componentData = {
        factory: {}
      };
      service.getComponentFactory = jasmine.createSpy('getComponentFactory').and.returnValue(of(componentData));
      service.createDynamicComponent = jasmine.createSpy('createDynamicComponent');

      service.getDynamicComponent(dynamicComp, lazyComponent);

      expect(service.getComponentFactory).toHaveBeenCalledWith(dynamicComp, lazyComponent.viewContainer.parentInjector);
      expect(service.createDynamicComponent).toHaveBeenCalledWith(dynamicComp, lazyComponent);
    });
  });

  describe('@populateComponentRef', () => {
    let component;

    beforeEach(() => {
      component = {
        factory: {
          inputs: [
            {
              templateName: '0',
              propName: '0'
            }
          ]
        },
        viewContainer: {
          element: {
            nativeElement: [{}]
          }
        },
        componentRef: {
          instance: [{}]
        }
      };
      service.populateComponentRef = jasmine.createSpy('populateComponentRef');
    });

    it('should populate component instance with binding values', () => {
      service.populateComponentRef(component);

      expect(component.componentRef.instance[0]).toEqual(component.viewContainer.element.nativeElement[0]);
    });

    it('should not populate component instance with binding values', () => {
      component.factory.inputs[0].templateName = '3';

      service.populateComponentRef(component);

      expect(component.componentRef.instance[0]).toEqual({});
    });
  });

  xdescribe('@destroyDynamicComponent', () => {
    it('should destroy component reference', () => {
      const lazyComponent = {
        viewContainer: {
          clear: jasmine.createSpy('clear')
        },
        componentRef: {
          destroy: jasmine.createSpy('destroy')
        }
      };
      service.destroyDynamicComponent(lazyComponent);

      expect(lazyComponent.componentRef.destroy).toHaveBeenCalled();
      expect(lazyComponent.viewContainer.clear).toHaveBeenCalled();
    });
  });

  xdescribe('@createInstances', () => {
    let componentToken,
      containers,
      keys;

    beforeEach(() => {
      const componentData = {
        factory: {}
      };
      keys = '0';
      componentToken = '';
      containers = [{
        clear: jasmine.createSpy('clear'),
        createComponent: jasmine.createSpy('createComponent').and.returnValue({ instance: [jasmine.createSpy().and.returnValue(of([1]))] }),
        element: {
          nativeElement: [{}]
        }
      }] as any;
      service.getComponentFactory = jasmine.createSpy('getComponentFactory').and.returnValue(of(componentData));
      service.populateComponentRef = jasmine.createSpy('populateComponentRef');
    });

    it('should create multiple instances of dynamic component', () => {
      containers.first = { parentInjector: {} };
      keys = '';

      service.createInstances(componentToken, containers, keys);

      expect(service.getComponentFactory).toHaveBeenCalled();
      expect(service.populateComponentRef).toHaveBeenCalled();
    });

    it('should create multiple instances of dynamic component by key', () => {
      containers.first = { parentInjector: {} };

      service.createInstances(componentToken, containers, keys);

      expect(service.getComponentFactory).toHaveBeenCalled();
      expect(service.populateComponentRef).toHaveBeenCalled();
    });

    it('should not create multiple instances of dynamic component', () => {
      containers = [];

      const result = service.createInstances(componentToken, containers);

      expect(result).toEqual([]);
      expect(service.getComponentFactory).not.toHaveBeenCalled();
      expect(service.populateComponentRef).not.toHaveBeenCalled();
    });
  });

  xdescribe('@destroyInstances', () => {
    let components;

    beforeEach(() => {
      components = [{
        componentRef: {
          destroy: jasmine.createSpy('destroy')
        }
      }];
    });

    it('should destroy multiple dynamic components', () => {
      service.destroyInstances(components);
      expect(components[0].componentRef.destroy).toHaveBeenCalled();
    });

    it('should not destroy multiple dynamic components', () => {
      service.destroyInstances();

      expect(components[0].componentRef.destroy).not.toHaveBeenCalled();
    });
  });
});
