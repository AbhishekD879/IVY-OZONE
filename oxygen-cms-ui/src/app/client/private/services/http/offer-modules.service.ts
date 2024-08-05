import { AbstractService } from './transport/abstract.service';
import { Configuration } from '../../models/configuration.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse} from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Brand } from '../../models/brand.model';
import { OfferModule } from '../../models/offermodule.model';
import { Order } from '../../models/order.model';

@Injectable()
export class OfferModulesService extends AbstractService<Configuration> {
  offerModulesByBrandUrl: string = `offer-module/brand/${this.brand}`;
  offerModulesUrl: string = 'offer-module';
  offerModulesOrderUrl: string = 'offer-module/ordering';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getOfferModules(): Observable<HttpResponse<Brand[]>> {
    return this.sendRequest<Brand[]>('get', this.offerModulesByBrandUrl, null);
  }

  public getSingleOfferModule(id: string): Observable<HttpResponse<OfferModule>> {
    const url = `${this.offerModulesUrl}/${id}`;
    return this.sendRequest<OfferModule>('get', url, null);
  }

  public postNewOfferModule(offerModule: OfferModule): Observable<HttpResponse<OfferModule>> {
    return this.sendRequest<OfferModule>('post', this.offerModulesUrl, offerModule);
  }

  public putOfferModuleChanges(id: string, prmotionData: OfferModule): Observable<HttpResponse<OfferModule>> {
    const apiUrl = `${this.offerModulesUrl}/${id}`;

    return this.sendRequest<OfferModule>('put', apiUrl, prmotionData);
  }

  public postNewOfferModulesOrder(offerModulesOrder: Order): Observable<HttpResponse<OfferModule[]>> {
    return this.sendRequest<OfferModule[]>('post', this.offerModulesOrderUrl, offerModulesOrder);
  }

  public deleteOfferModule(id: string): Observable<HttpResponse<void>> {
    const url = `${this.offerModulesUrl}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }
}
