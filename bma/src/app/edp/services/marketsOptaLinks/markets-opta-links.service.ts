import { Injectable } from '@angular/core';
import { CmsService } from '@core/services/cms/cms.service';
import { IMarketLinks } from '@core/services/cms/models/edp-market.model';
import { catchError, map, switchMap } from 'rxjs/operators';
import { ISystemConfig } from '@core/services/cms/models';
import { Observable, throwError } from 'rxjs';


@Injectable()
export class MarketsOptaLinksService {

  constructor(
    private cmsService: CmsService
  ) {
  }

  /**
   * Get Market links from cms
   * @returns {Observable<IMarketLinks[]>}
   */
  getMarketLinks(): Observable<IMarketLinks[]> {
    return this.cmsService.getSystemConfig().pipe(
      map((config: ISystemConfig): boolean => config && config.StatisticsLinks && config.StatisticsLinks.markets),
      switchMap((enabled: boolean) => enabled ? this.cmsService.getMarketLinks() : throwError('market links are disabled on cms')),
      catchError((err) => throwError(err)));
  }
}
