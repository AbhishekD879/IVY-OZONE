import {Configuration} from '../../models/configuration.model';
import {AbstractService} from './transport/abstract.service';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {Order} from '@app/client/private/models/order.model';
import {RemoveImageRequest, VirtualSportChild} from '@app/client/private/models/virtualSportChild.model';

@Injectable()
export class VirtualSportsChildsService extends AbstractService<Configuration> {
  virtualsBaseUrl: string = 'virtual-sport-track';
  virtualsByBrandUrl: string = `virtual-sport-track/brand/${this.brand}`;
  virtualsBySportIdUrl: string = `virtual-sport-track/sport-id`;
  virtualsOrderUrl: string = `virtual-sport-track/ordering`;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getVirtualSportsByParentSportId(parentSportId: string) {
    return this.sendRequest<VirtualSportChild[]>('get', `${this.virtualsBySportIdUrl}/${parentSportId}`, null);
  }

  public getVirtualSportsByBrand(): Observable<HttpResponse<any[]>> {
    return this.sendRequest<any[]>('get', this.virtualsByBrandUrl, null);
  }

  public getSingleVirtualSport(id: string): Observable<HttpResponse<any>> {
    const url = `${this.virtualsBaseUrl}/${id}`;
    return this.sendRequest<any>('get', url, null);
  }


  public saveVirtualSportChild(virtualSport: VirtualSportChild): Observable<HttpResponse<any>> {
    return this.sendRequest<any>('post', this.virtualsBaseUrl, virtualSport);
  }

  public updateVirtualSportChild(id: string, virtualSportChild: VirtualSportChild): Observable<HttpResponse<any>> {
    const apiUrl = `${this.virtualsBaseUrl}/${id}`;
    return this.sendRequest<any>('put', apiUrl, virtualSportChild);
  }


  public deleteVirtualSportChild(id: string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('delete', `${this.virtualsBaseUrl}/${id}`, null);
  }

  public postSportsOrder(sportsOrder: Order): Observable<HttpResponse<VirtualSportChild[]>> {
    return this.sendRequest<VirtualSportChild[]>('post', this.virtualsOrderUrl, sportsOrder);
  }

  public uploadImage(id: string, file: any, event?: string) {
    const uri = `${this.virtualsBaseUrl}/${id}/image-upload`;
    return this.sendRequest<any>('post', uri, file, event && {event: event});
  }

  public deleteImageByChildSportIdAndImageName(childSportId: string, removeImageRequest: RemoveImageRequest) {
    const uri = `${this.virtualsBaseUrl}/${childSportId}/image-remove`;
    return this.sendRequest<any>('post', uri, removeImageRequest);
  }
}
