import { Injectable } from '@angular/core';
import { AbstractService } from './transport/abstract.service';
import { Configuration } from '../../models';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

@Injectable({
  providedIn: 'root'
})
export class ConfigRegistryService extends AbstractService<Configuration> {
  apiCollectionUri ='api-collection-config'
  columnName= 'id';
  configRegistryByBaseUrl: string = `${this.apiCollectionUri}/${this.brand}`; /** get */
  configRegistryUrlPost: string = this.apiCollectionUri; /** post */
  configRegistryUrl: string = `${this.apiCollectionUri}/${this.brand}/${this.columnName}`; /** put */
  configRegistryUrGetRegistry: string = `${this.apiCollectionUri}/${this.brand}`; /** getall*/
  

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
  public postNewRegistry(registry: any): Observable<HttpResponse<any>> {
    registry.brand = this.brand;
    return this.sendRequest<any>('post', this.configRegistryUrlPost, registry);
  }

  /**
   * Update Registry data.
   * @returns {Observable<HttpResponse<any>>}
   */
  public updateRegistry(id: string, registry: any, flag: boolean): Observable<HttpResponse<any>> {
    registry.brand = this.brand;
    const apiUrl = `${this.configRegistryUrl}/${id}`;
    return this.sendRequest<any>('put', apiUrl, registry);
  }
  /**
   * Delete Registry data.
   * @returns {Observable<HttpResponse<void>>}
   */
  public deleteRegistry(id: string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('delete', `${this.configRegistryUrl}/${id}`, null);
  }

}
