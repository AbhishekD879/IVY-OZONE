import { Injectable } from '@angular/core';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISportCategory } from '@core/services/cms/models';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SportsConfigHelperService {
  constructor(private cmsService: CmsService) {
  }

  getSportConfigName(sportName: string): string {
    return sportName.toLowerCase().replace(/\s|\/|\||\-/g, '');
  }

  getSportPathByCategoryId(categoryId: number): Observable<string> {
    return this.cmsService.getSportCategoryById(categoryId)
      .pipe(
        map((sportCategory: ISportCategory) => {
          return sportCategory.sportName && sportCategory.sportName.split('/').pop();
        }));
  }

  getSportPathByName(categoryName: string): Observable<string> {
    return this.cmsService.getSportCategoryByName(categoryName)
      .pipe(
        map((sportCategory: ISportCategory) => {
          return sportCategory.sportName && sportCategory.sportName.split('/').pop();
        }));
  }
}
