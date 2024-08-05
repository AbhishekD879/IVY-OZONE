import {AbstractService} from './transport/abstract.service';
import {Configuration} from '../../models/configuration.model';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {SportCategory} from '../../models/sportcategory.model';

@Injectable()
export class SportCategoriesService extends AbstractService<Configuration> {

  sportCategoryUrl: string = `sport-category/brand/${this.brand}`;
  sportCategorySegmentUrl: string = `sport-category/brand/${this.brand}/segment`;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getSportCategories(): Observable<HttpResponse<SportCategory[]>> {
    return this.sendRequest<SportCategory[]>('get', this.sportCategoryUrl, null);
  }

  public getSportCategory(segmentName: string): Observable<HttpResponse<SportCategory[]>> {
    const uri = `${this.sportCategorySegmentUrl}/${segmentName}`;
    return this.sendRequest<SportCategory[]>('get', uri , null);
  }

}
