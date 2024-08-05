import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import environment from '@environment/oxygenEnvConfig';
import { FiltersService } from '../filters/filters.service';
import { NavigationUriService } from '@core/services/navigation/navigation-uri.service';

import { IProcessedRequestModel } from './models/process-request.model';

@Injectable()
export class CmsToolsService {
  CMS_ROOT_URI: string;

  constructor(
    private filtersService: FiltersService,
    private navigationUriService: NavigationUriService
  ) {
    this.CMS_ROOT_URI = environment.CMS_ROOT_URI;
  }

  processResult<T extends IProcessedRequestModel>(
    data: T[],
    deferObj?: any): T[] {
    const paths = ['uriSmall', 'uriMedium', 'desktop_uriSmall', 'desktop_uriMedium',
                   'uriSmallIcon', 'uriMediumIcon', 'image', 'iconUrl'];
    const processedData = _.map(data, val => {
        if (val.targetUri || val.target) {
          val.targetUriCopy = val.targetUri;
          val.sportName = val.targetUri;
          val.relUri = this.navigationUriService.isAbsoluteUri(val.targetUri);

          this.filterLinks(val);
        }

        return this.modifyLink(val, paths);
      });

    if (deferObj) {
      deferObj.resolve(processedData);
    }

    return processedData;
  }

  private modifyLink<T>(item: T, paths: string[]): T {
    _.forEach(paths, pathItem => {
      if (item[pathItem]) {
        item[pathItem] = this.CMS_ROOT_URI + item[pathItem];
      }
    });
    return item;
  }


  private filterLinks<T>(item: T): void {
    const keysToFilter = ['target', 'targetUri', 'desktop_targetUri'];

    _.each(keysToFilter, (key: string) => {
      if (item[key]) {
        item[key] = this.filtersService.filterLink(item[key]);
      }
    });
  }
}
