import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ApiClientService} from '@app/client/private/services/http';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {VirtualSportParent} from '@app/client/private/models/virtualSportParent.model';
import {Order} from '@app/client/private/models/order.model';

@Injectable()
export class VirtualSportsService {
  virtualsData:VirtualSportParent[];
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService) {
  }

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
        if (response instanceof HttpErrorResponse) {
          this.handleRequestError(response.error);
        }

        return Observable.throw(response);
      });
  }

  handleRequestError(error): void {
    this.globalLoaderService.hideLoader();
  }

  hideLoader(): void {
    this.globalLoaderService.hideLoader();
  }

  getVirtualSports(): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.virtualSportsService().getVirtualSports();
    return this.wrappedObservable(data);
  }

  getVirtualSportsByBrand(): Observable<VirtualSportParent> {
    const data = this.apiClientService.virtualSportsService().getVirtualSportsByBrand();
    return this.wrappedObservable(data);
  }

  getVirtualSportParent(id: string): Observable<VirtualSportParent> {
    const data = this.apiClientService.virtualSportsService().getSingleVirtualSport(id);
    return this.wrappedObservable(data);
  }

  createVirtualSportParent(virtualSportParent: any): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.virtualSportsService().saveVirtualSport(virtualSportParent);
    return this.wrappedObservable(data);
  }

  updateVirtualSportParent(virtualSportParent: any): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.virtualSportsService().updateVirtualSport(virtualSportParent.id, virtualSportParent);
    return this.wrappedObservable(data);
  }

  deleteVirtualSportParent(id: string): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.virtualSportsService().deleteVirtualSport(id);
    return this.wrappedObservable(data);
  }

  postSportsOrder(newOrder: Order) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.virtualSportsService().postSportsOrder(newOrder);
    return this.wrappedObservable(getData);
  }

  uploadImage(id: string, file: FormData) {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.virtualSportsService().uploadImage(id, file);
    return this.wrappedObservable(data);
  }

  deleteImage(id: string) {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.virtualSportsService().deleteImage(id);
    return this.wrappedObservable(data);
  }

  setSavedvirtualSports(virtualsData) {
    this.virtualsData = virtualsData
  }

  getSavedvirtualSports() {
    return this.virtualsData;
  }
    
}
