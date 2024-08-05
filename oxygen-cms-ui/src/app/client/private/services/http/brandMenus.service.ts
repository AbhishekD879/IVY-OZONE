import {AbstractService} from './transport/abstract.service';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {Brand} from '../../models/brand.model';

@Injectable()
export class BrandMenuesService extends AbstractService<Brand> {
  menuesByBrandUrl: string = `menu-structure/brand/${this.brand}`;
  menuesUrl: string = `menu-structure`;
  private menuesByIdUrl = function(id) {
    return `menu-structure/${id}`;
  };

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getMenu(): Observable<HttpResponse<any>> {
    return this.sendRequest('get', this.menuesByBrandUrl, null);
  }

  public updateMenu(menuStructure: any, id: string): Observable<HttpResponse<any>> {
    return this.sendRequest('put', this.menuesByIdUrl(id), menuStructure);
  }
}
