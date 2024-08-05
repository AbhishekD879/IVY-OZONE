import { Injectable } from '@angular/core';
import { Observable, from, forkJoin } from 'rxjs';
import { map } from 'rxjs/operators';

import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { PubSubService } from '@coreModule/services/communication/pubsub/pubsub.service';
import { IModuleToLoad } from '@coreModule/services/deferredLoader/deferred-loader.service.model';
import { MODULES_LOADING_DELAY, MODULES_BY_PRIORITY } from '@coreModule/services/deferredLoader/deferred-loader.service.constant';

@Injectable()
export class DeferredLoaderService {
  modulesToLoad: IModuleToLoad[];

  private isLoaded: boolean;
  private modulesLoading: Observable<void>[];

  constructor(
    private dynamicLoaderService: DynamicLoaderService,
    private pubSubService: PubSubService
  ) {
    this.modulesToLoad = MODULES_BY_PRIORITY && MODULES_BY_PRIORITY.slice() || [];
  }

  init(): void {
    this.pubSubService.subscribe('DeferredLoaderService', this.pubSubService.API.APP_IS_LOADED, () => {
      setTimeout(() => this.lazyLoadModules(), MODULES_LOADING_DELAY);
    });

    this.pubSubService.subscribe('DeferredLoaderService', this.pubSubService.API.RELOAD_COMPONENTS, () => {
      if (!this.isLoaded) {
        this.lazyLoadModules();
      }
    });
  }

  private lazyLoadModules(): void {
    this.modulesLoading = this.modulesToLoad.map((module: IModuleToLoad) =>
      from(this.dynamicLoaderService.loadModule(module.path.substring(0, module.path.indexOf(':')))).pipe(
        map(() => {
          this.isLoaded = true;
          this.pubSubService.publish(module.pubSubChannel);
        })
      )
    );

    forkJoin(...this.modulesLoading).subscribe(
      () => this.pubSubService.publish(this.pubSubService.API.DEFERRED_MODULES_LOADED)
    );
  }
}
