import { Injectable } from '@angular/core';
import { ApiClientService } from '../client/private/services/http';
import { GlobalLoaderService } from '../shared/globalLoader/loader.service';
import { HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';

@Injectable({
  providedIn: 'root'
})
export class ConfigRegistryApiService {

  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService) { }
  /**
* Wrap request to handle success/error.
* @param observableDate
*/
  wrappedObservable(observableDate): Observable<any> {
    return observableDate
      .map(res => {
        this.globalLoaderService.hideLoader();
        return res;
      })
      .catch(response => {
        if (response instanceof HttpErrorResponse && response.status !== 400) {
          this.handleRequestError(response.error);
        }

        this.globalLoaderService.hideLoader();
        return Observable.throw(response);
      });
  }
  /**
* Handle networking error.
* Notify user.
*/
  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
  }
  /**
     * get Registry
     * @returns {Observable<HttpResponse<Brand[]>>}
     */
  getCampaignsByBrandWithOrdering(): Observable<any> {
    const data = this.apiClientService.configRegistryService().getRegistry();
    return this.wrappedObservable(data.map(res => res.body));
  }
  postNewRegistry(newCampaign: any) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.configRegistryService().postNewRegistry(newCampaign);
    return this.wrappedObservable(getData);

  }
  /**
* Submit updated  Registry
* @param newRegistry
* @returns {any}
*/
  updateRegistry(Registry: any, flag: boolean): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.configRegistryService().updateRegistry(Registry.id, Registry, flag);
    return this.wrappedObservable(data);
  }
  /**
  * Load single Registry data to edit
  * @param {string} id
  * @returns {any}
  */
  getSingleRegistryData(id: string) {
    const getData = this.apiClientService.configRegistryService().getSingleRegistry(id);
    return this.wrappedObservable(getData);
  }
  /**
     * Delete Registry
     * @returns {Observable<HttpResponse<Brand[]>>}
     */
  deleteCampaign(id: string): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.configRegistryService().deleteRegistry(id);
    return this.wrappedObservable(data);
  }
}
