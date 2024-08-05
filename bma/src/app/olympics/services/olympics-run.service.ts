import { Injectable } from '@angular/core';

import { ModuleExtensionsStorageService } from '@core/services/moduleExtensionsStorage/module-extensions-storage.service';
import { OlympicsService } from '@app/sb/services/olympics/olympics.service';

import { IModuleExtension } from '@core/services/moduleExtensionsStorage/module-extension.model';
import { ISportCMSConfig } from '@app/olympics/models/olympics.model';

@Injectable()
export class OlympicsRunService {

 constructor(
   private moduleExtensionsStorageService: ModuleExtensionsStorageService,
   private olympicsService: OlympicsService,
 ) { }

 run(): void {
   this.olympicsService.getCMSConfig()
     .subscribe((cmsConfigs: ISportCMSConfig[]) => {
       const extension: IModuleExtension = {
         name: this.olympicsService.extensionName,
         extendsModule: 'sb',
         sportsConfig: this.olympicsService.getSportsConfigs(cmsConfigs),
         menuConfig: this.olympicsService.getMenuConfigs(cmsConfigs)
       };
       this.moduleExtensionsStorageService.addToList(extension);
       this.olympicsService.extendCacheParams();
     }, error => {
       console.warn('CMS Sports Configs:', error && error.error || error);
     });
 }
}
