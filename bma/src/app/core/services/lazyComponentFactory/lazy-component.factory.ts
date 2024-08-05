/**
 * Use for lazy loading components
 * Path to module ('./src/lazy-libs/lazy.module') also should be added to the angular.json file
 * Documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=101687110
 *
 * "options": {
 *  ...
 *  "lazyModules": [
 *    ...
 *    './src/lazy-libs/lazy.module'
 *    ...
 *  ]
 *  ...
 * }
 */

import {
  ComponentRef, Injectable, Injector, ViewContainerRef, NgModuleRef, createNgModuleRef
} from '@angular/core';
import { LazyComponentLoader } from './lazy-component.loader';

@Injectable({
  providedIn: 'root'
})
export class LazyComponentFactory {

  componentName: any;
  moduleRef: NgModuleRef<any>;
  lazymodule: any;
  constructor(
    private loader: LazyComponentLoader,
    private injector: Injector
  ) { }

  /**
   * Create lazy component by given module path:
   *  load module the component belongs to,
   *  create instance of that module,
   *  create component [by name] and put it to given outlet
   *
   * @param lazyModulePath
   * @param lazyComponentOutlet
   * @param entryComponentName - optional (skip it if module holds single component)
   * Create instance of loaded module
   *
   * @param lazyModulePath
   * @param parentInjector
   * Load given module
   *
   * @param lazyModulePath
   */
  createLazyComponent(lazyModulePath: string, lazyComponentOutlet: ViewContainerRef, entryComponentName?: any, lazyComponentPath?: string)
  : Promise<ComponentRef<any>> {
    if (!lazyComponentOutlet) {
      return Promise.reject('Outlet for component is not defined!');
    }
    if (!lazyModulePath) {
      return Promise.reject('Path for module is not defined!');
    }
    return this.loader.getModule(lazyModulePath.slice(0, lazyModulePath.indexOf('#'))).then((lazyModuleRef) => {
      const args =  { moduleLoader: lazyModuleRef, 
        moduleName: lazyModulePath.split('#')[1], 
        container: lazyComponentOutlet,
        injector: this.injector, 
        entryComponentName: entryComponentName
      };
      try {
        this.lazymodule = args.moduleLoader[args.moduleName];
        this.moduleRef = createNgModuleRef(this.lazymodule, args.injector);
        this.componentName = (args.entryComponentName)  && this.moduleRef.instance.constructor.entry && this.moduleRef.instance.constructor.entry.hasOwnProperty(args.entryComponentName) ? 
        this.moduleRef.instance.constructor.entry[args.entryComponentName] : this.moduleRef.instance.constructor.entry;
        args.container.clear();
        return args.container.createComponent(this.componentName, { ngModuleRef: this.moduleRef });
      }
      catch {
        return Promise.reject("Issue in loading: " + args.moduleName);
      }
    }).catch((error) => {
      return Promise.reject(error);
    });
  } 
}

