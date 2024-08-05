import { LazyComponentFactory } from '@core/services/lazyComponentFactory/lazy-component.factory';
import { NgModule, Injector } from '@angular/core';
import {RightColumnModule} from '@lazy-modules/rightColumn/right-column.module';
import {FreebetsModule} from '@freebetsModule/freebets.module';

describe('LazyComponentFactory -', () => {
  let service: LazyComponentFactory;
  let
    loader,
    injector,
    moduleFactory,
    newComponent,
    lazyComponentOutlet;

  beforeEach(() => {
    moduleFactory = {
      module: {} as any,
      moduleType: {entry: {lazyComponent: 'foo'}},
      moduleName: 'RightColumnModule',
      RightColumnModule: jasmine.createSpy('lazyModuleRef').and.returnValue(RightColumnModule)()
    };
    loader = {
      getModule: jasmine.createSpy('getModule').and.returnValue(Promise.resolve(moduleFactory))
    };

    injector=Injector.create({providers: []});

    newComponent = {foo: ''};

    lazyComponentOutlet = {
      clear: jasmine.createSpy('clear'),
      createComponent: jasmine.createSpy('createComponent').and.returnValue(newComponent)
    };
    service = new LazyComponentFactory(loader, injector);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });  

  describe('createLazyComponent-new way', () => {

    it('createLazyComponent with no viewcontainer', () => {
      service.createLazyComponent('foo', null).then(()=> {
        expect(loader.getModule).not.toHaveBeenCalled();
      }).catch((error) => {
        expect(error).toEqual(jasmine.any(String));
      }); 
    });

    it('createLazyComponent with no Lazy load module URL', () => {
      service.createLazyComponent(null, lazyComponentOutlet).then(()=> {
        expect(loader.getModule).not.toHaveBeenCalled();
      }).catch((error) => {
        expect(error).toEqual(jasmine.any(String));
      });      
    });

    it('createLazyComponent with no Lazy load module URL', () => {
      service.createLazyComponent('@betslipModule/betslip.module', lazyComponentOutlet).then(()=> {
        expect(loader.getModule).toHaveBeenCalled();
      }).catch((error) => {
        expect(error).toEqual(jasmine.any(String));
      });      
    });   

    it('createLazyComponent with viewcontainer and URL - catch', (done: DoneFn) => {
      service.createLazyComponent('foo', null).catch((err) => {
        done();
        expect(err).toEqual(jasmine.any(String));
      });
      expect(loader.getModule).not.toHaveBeenCalled();
    });

    it('createLazyComponent with viewcontainer and URL', (done: DoneFn ) => {     
      service.createLazyComponent('@rightColumnModule/right-column.module#RightColumnModule', lazyComponentOutlet, 'RightColumnWidgetWrapperComponent').then(()=> {      
      expect(loader.getModule).toHaveBeenCalled();
      const modRe =  jasmine.createSpy('lazyModuleRef').and.returnValue(moduleFactory as any) as any;
      loader = {
        getModule: jasmine.createSpy('getModule').and.returnValue(Promise.resolve(modRe)) as any
      };
      const instance = {constructor: {entry:  'RightColumnWidgetWrapperComponent' } as any} as any;
      const moduleRef = {instance} as any;
      const spyCreateNgModuleRef = jasmine.createSpy('createNgModuleRef').and.returnValue({moduleRef} as any) as any;
     
      (loader.getModule('@rightColumnModule/right-column.module#RightColumnModule')).then((res)=> {  
        done();      
        res = {
          module: {} as any,
          moduleType: {entry: {lazyComponent: 'foo'}},
          RightColumnModule: import("@rightColumnModule/right-column.module").then(m => m.RightColumnModule) as any
        } as any;
        service['lazymodule'] =  import("@rightColumnModule/right-column.module").then(m => m.RightColumnModule);
        const moduleRefData = spyCreateNgModuleRef(service['lazymodule'] as NgModule, injector as any);
        service['moduleRef'] = moduleRefData as any;
        service['componentName'] = moduleRefData.moduleRef.instance?.constructor?.entry as any;
        expect(service['componentName']).toEqual('RightColumnWidgetWrapperComponent');        
      }).catch((error) => {
        expect(error).toEqual(jasmine.any(String));
      });
    }).catch((error) => {
      expect(error).toEqual(jasmine.any(String));
    });
    });
  })

  describe('', ()=> {
    let lazyLoadService: LazyComponentFactory;
    let
    loader,
    injector,
    moduleFactory,
    newComponent,
    lazyComponentOutlet;
    beforeEach(() => {
      moduleFactory = {
        module: {} as any,
        moduleType: {entry: {lazyComponent: 'foo'}},
        FreebetsModule: jasmine.createSpy('lazyModuleRef').and.returnValue(FreebetsModule)()
      } as any;
      loader = {
        getModule: jasmine.createSpy('getModule').and.returnValue(Promise.resolve(moduleFactory))
      };  
      injector=Injector.create({providers: []});  
      newComponent = {foo: ''};  
      lazyComponentOutlet = {
        parentInjector: {foo: ''},
        clear: jasmine.createSpy('clear'),
        createComponent: jasmine.createSpy('createComponent').and.returnValue(newComponent)
      };  
      lazyLoadService = new LazyComponentFactory(loader, injector);
    }); 
    it('createLazyComponent with no Lazy load module URL-multiple entries', (done: DoneFn) => {
      lazyLoadService.createLazyComponent('@betslipModule/betslip.module#FreebetsModule', lazyComponentOutlet, 'FreeBetToggleComponent').then(() => {
        expect(loader.getModule).toHaveBeenCalled();
        const modRe = jasmine.createSpy('lazyModuleRef').and.returnValue(moduleFactory as any) as any;
        loader = {
          getModule: jasmine.createSpy('getModule').and.returnValue(Promise.resolve(modRe)) as any
        };
        const instance = { constructor: { entry: { 'FreeBetToggleComponent': 'FreeBetToggleComponent', 'dummyComponent': 'FreeBetToggleComponent' } } as any } as any;
        const moduleRef = { instance } as any;
        const spyCreateNgModuleRef = jasmine.createSpy('createNgModuleRef').and.returnValue({ moduleRef } as any) as any;

        (loader.getModule('@FreebetsModule/freebets.module')).then((res) => {
          done();
          const moduleRefData = spyCreateNgModuleRef(res as NgModule, injector as any);
          lazyLoadService['moduleRef'] = moduleRefData as any;
          lazyLoadService['componentName'] = moduleRefData.moduleRef.instance?.constructor?.entry.FreeBetToggleComponent as any;
          lazyComponentOutlet = {
            parentInjector: { foo: '' },
            clear: jasmine.createSpy('clear'),
            createComponent: jasmine.createSpy('createComponent').and.returnValue('FreeBetToggleComponent' as any)
          };
          expect(lazyLoadService['componentName']).toEqual('FreeBetToggleComponent');
        }).catch((error) => {
          expect(error).toEqual(jasmine.any(String));
        });
      }).catch((error) => {
        expect(error).toEqual(jasmine.any(String));
      });
    });
  })
});
