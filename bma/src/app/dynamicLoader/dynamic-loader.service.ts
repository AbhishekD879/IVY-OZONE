import {
  Injectable,
  Injector,
  NgModuleFactory,
  NgModuleRef,
  Compiler
} from '@angular/core';
import { LazyComponentLoader } from '@app/core/services/lazyComponentFactory/lazy-component.loader';

@Injectable()
export class DynamicLoaderService {

  private moduleResolvers = {};

  constructor(
      private compiler: Compiler,
      private injector: Injector,
      private loader: LazyComponentLoader
  ) { }

  /**
   * Load module by given path (same as loadChildren in Router)
   */
  loadModule(modulePath: string, injector?: Injector): Promise<NgModuleRef<any>> {
    const loadedModulePromise = this.moduleResolvers[modulePath];

    if (loadedModulePromise) {
      return loadedModulePromise;
    }

    return this.loader.getModule(modulePath.slice(0, modulePath.indexOf('#')))
      .then((module: any) => {
        return this.loadModuleFactory(module[Object.keys(module)[0]]);
      })
      .then((moduleFactory: any) => {
        return moduleFactory.create(injector || this.injector);
      })
      .then((mod: any) => {
        const p = Promise.resolve(mod);
        this.moduleResolvers[modulePath] = p;
        return Promise.resolve(p);
      })
      .catch(() => {
        delete this.moduleResolvers[modulePath];
      });
  }

  loadModuleFactory(loadedModule: any) {
    if (loadedModule instanceof NgModuleFactory) {
      return loadedModule;
    } else {
      return this.compiler.compileModuleAsync(loadedModule);
    }
  }
}
