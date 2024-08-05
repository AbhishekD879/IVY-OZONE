import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { IEuroLoyalty } from '@app/client/private/models/euroLoyalty.model';
import { EuroLoyaltyConstants } from '@app/special-pages/euro-loyalty/euro-loyalty-dashboard/euroLoyalty.constant';

@Injectable()
export class EuroLoyaltyService extends AbstractService<IEuroLoyalty[]> {

  public readonly EUROLOYAL = EuroLoyaltyConstants;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = this.EUROLOYAL.labels.SpecialPagesURL;
  }

  /**
   * Saves the configuration
   * @param euroLoyalty  { IEuroLoyalty }
   * @returns { HttpResponse<IEuroLoyalty> }
   */
  public saveConfig(euroLoyalty: IEuroLoyalty): Observable<HttpResponse<IEuroLoyalty>> {
    return this.sendRequest<IEuroLoyalty>('post', this.uri, euroLoyalty);
  }

  /**
   * Updates the configuration
   * @param euroLoyalty  { IEuroLoyalty }
   * @returns { HttpResponse<IEuroLoyalty> }
   */
  public updateConfig(euroLoyalty: IEuroLoyalty): Observable<HttpResponse<IEuroLoyalty>> {
    return this.sendRequest<IEuroLoyalty>('put', this.uri, euroLoyalty);
  }

  /**
   * Retrieves the configuration
   * @returns { HttpResponse<IEuroLoyalty> }
   */
  public getConfig(): Observable<HttpResponse<IEuroLoyalty>> {
    return this.sendRequest<IEuroLoyalty>('get', this.uri, null);
  }

  /**
   * Deletes the configuration
   * @returns { HttpResponse<void> }
   */
  public deleteConfig(): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('delete', this.uri, null);
  }
}
