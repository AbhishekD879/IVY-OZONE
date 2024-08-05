import { ModuleWithProviders, NgModule } from '@angular/core';

import { DynamicLoaderService } from './dynamic-loader.service';

@NgModule({})
export class DynamicLoaderModule {
  static forRoot(): ModuleWithProviders<DynamicLoaderModule> {
    return {
      ngModule: DynamicLoaderModule,
      providers: [
        DynamicLoaderService
      ],
    };
  }
}
