import { Injectable } from '@angular/core';
import { AbstractService } from './client/private/services/http/transport/abstract.service';
import { Configuration } from './client/private/models';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

@Injectable({
  providedIn: 'root'
})
export class ConfigRegistryService extends AbstractService<Configuration> {
  configRegistryByBaseUrl: string = `apiCollectionConfig/bma/`; /** get */
  configRegistryUrlPost: string = 'apiCollectionConfig'; /** post */
  configRegistryUrlPUt: string = 'apiCollectionConfig/bma'; /** put */
  configRegistryUrGetRegistry: string = `apiCollectionConfig/bma/${this.brand}`; /** getall*/
  configRegistryUrlDelete: string = `apiCollectionConfig/bma/id`; /** delete*/

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  /**
   * Add Config.
   * @returns {Observable<HttpResponse<any>>}
   */
  public getRegistry(): Observable<HttpResponse<any>> {
    return this.sendRequest<any>('get', this.configRegistryByBaseUrl, null);
  }
  /**
  * get Registry data.
  * @returns {Observable<HttpResponse<any>>}
  */
  public getSingleRegistry(id: string): Observable<HttpResponse<any>> {
    const url = `${this.configRegistryUrGetRegistry}/${id}`;
    return this.sendRequest<any>('get', url, null);
  }
  /**
     * Create Registry data.
     * @returns {Observable<HttpResponse<any>>}
     */
  public postNewRegistry(Registry: any): Observable<HttpResponse<any>> {
    return this.sendRequest<any>('post', this.configRegistryUrlPost, Registry);
  }

  /**
   * Update Registry data.
   * @returns {Observable<HttpResponse<any>>}
   */
  public updateRegistry(id: string, Registry: any, flag: boolean): Observable<HttpResponse<any>> {
    const apiUrl = `${this.configRegistryUrlPUt}/id/${flag}`;
    return this.sendRequest<any>('put', apiUrl, Registry);
  }
  /**
   * Delete Registry data.
   * @returns {Observable<HttpResponse<void>>}
   */
  public deleteRegistry(id: string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('delete', `${this.configRegistryUrlDelete}/${id}`, null);
  }

}
