
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { IModuleExtension } from '@core/services/moduleExtensionsStorage/module-extension.model';
import { ISportCategory } from '@core/services/cms/models/sport-category.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { ModuleExtensionsStorageService } from '@core/services/moduleExtensionsStorage/module-extensions-storage.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { UserService } from '@core/services/user/user.service';
import { HttpClient } from '@angular/common/http';
import environment from '@environment/oxygenEnvConfig';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';

@Injectable()
export class LeftMenuService {

  constructor(
    private cmsService: CmsService,
    public user: UserService,
    private modulesExtensionsStorage: ModuleExtensionsStorageService,
    private filterService: FiltersService,
    private fanzoneStorageService: FanzoneStorageService,
    protected http: HttpClient
  ) {
  }

  getMenuItems(fanzone?: any): Observable<ISportCategory[]> { 
    return this.cmsService.getMenuItems().pipe(map((data) => {
      const fanzoneIndex = data.findIndex(link => link.targetUri.includes('fanzone'));
      if (fanzoneIndex !== -1 && this.user.status) {
          const fanzoneStorage = this.fanzoneStorageService.get('fanzone');
          if (fanzoneStorage && fanzoneStorage.teamId && fanzone && fanzone.active && fanzone.fanzoneConfiguration.atozMenu) {
            data[fanzoneIndex].showInAZ = true;
            data[fanzoneIndex].disabled = false;
          } else {
            data[fanzoneIndex].showInAZ = false;
            data[fanzoneIndex].disabled = true;
          }
      }

      const extensionsList = this.modulesExtensionsStorage.getList();
      const mainSports = _.where(data, { showInAZ: true });

      let extensionMenuItems;
      extensionsList.forEach((extension: IModuleExtension) => {
        if (extension.extendsModule === 'sb' && extension.menuConfig) {
          extensionMenuItems = extension.menuConfig;
        }
      });

      // Get A-Z Sport items with olympics
      return this.filterService.orderBy(_.where(
        _.uniq(mainSports.concat(extensionMenuItems), 'imageTitle'), { disabled: false }
      ),
        ['imageTitle']
      );
    }));
  }

  getFavouriteItems(token: string): Observable<number[]> {
    return this.http.get<number[]>(`${environment.OPT_IN_ENDPOINT}/api/sportsCategoryFav`, {
      headers: { token }
    });
  }

  storeFavouriteItems(token: string, data: Object): Observable<number[]> {
    return this.http.post<number[]>(`${environment.OPT_IN_ENDPOINT}/api/sportsCategoryFav`, data, {
      headers: { token }
    });
  }
}
