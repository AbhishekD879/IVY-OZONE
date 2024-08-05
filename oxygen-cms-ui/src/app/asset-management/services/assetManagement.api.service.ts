import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ApiClientService} from '@app/client/private/services/http';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {AssetManagement} from '@app/client/private/models/assetManagement.model';

@Injectable()
export class AssetManagementApiService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService) {
  }

  /**
   * Wrap request to handle success/error.
   * @param observableDate
   */
  wrappedObservable(observableDate) {
    return observableDate
      .map(res => {
        this.globalLoaderService.hideLoader();
        return res;
      })
      .catch(response => {
        if (response instanceof HttpErrorResponse) {
          const message = response.error ? response.error.message : response.message;
          this.handleRequestError(message);
        }

        return Observable.throw(response);
      });
  }

  /**
   * Handle networking error.
   * Notify user.
   */
  handleRequestError(message) {
    this.globalLoaderService.hideLoader();
  }

  /**
   * Get formations data.
   * @returns {Observable<HttpResponse<AssetManagement[]>>}
   */
  getAssetManagementsList() {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.assetManagements().findAllAssetManagements();

    return this.wrappedObservable(getData);
  }

  /**
   * Load single formation data to edit.
   * @param {string} id
   * @returns {any}
   */
  getSingleAssetManagement(id: string) {
    const getData =  this.apiClientService.assetManagements().getSingleAssetManagement(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to asset Management.
   * @param {AssetManagement} assetManagement
   */
  putAssetManagementChanges(assetManagement: AssetManagement) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.assetManagements().editAssetManagement(assetManagement);
    return this.wrappedObservable(getData);
  }

  /**
   * Deletes Asset Management.
   * @param {string} id
   */
  deleteAssetManagement(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.assetManagements().deleteAssetManagement(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Creates new Asset Management.
   * @param {AssetManagement} assetManagement
   */
  createAssetManagement(assetManagement: AssetManagement) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.assetManagements().createAssetManagement(assetManagement);
    return this.wrappedObservable(getData);
  }
}
