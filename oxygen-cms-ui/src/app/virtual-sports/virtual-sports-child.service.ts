import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ApiClientService} from '@app/client/private/services/http';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {Order} from '@app/client/private/models/order.model';
import {RemoveImageRequest, VirtualSportChild} from '@app/client/private/models/virtualSportChild.model';

@Injectable()
export class VirtualSportsChildService {
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

  postSportsOrder(newOrder: Order) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.virtualSportsChildsService().postSportsOrder(newOrder);
    return this.wrappedObservable(getData);
  }

  createVirtualSportChild(childSport: VirtualSportChild) {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.virtualSportsChildsService().saveVirtualSportChild(childSport);
    return this.wrappedObservable(data);
  }

  updateVirtualSportChild(childSport: VirtualSportChild): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.virtualSportsChildsService().updateVirtualSportChild(childSport.id, childSport);
    return this.wrappedObservable(data);
  }

  postChildSportsOrder(newOrder: Order) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.virtualSportsChildsService().postSportsOrder(newOrder);
    return this.wrappedObservable(getData);
  }

  getVirtualSportChild(id: string): Observable<HttpResponse<VirtualSportChild>> {
    const data = this.apiClientService.virtualSportsChildsService().getSingleVirtualSport(id);
    return this.wrappedObservable(data);
  }

  getVirtualSportsChildrenByParentSportId(parentSportId: string): Observable<HttpResponse<VirtualSportChild[]>> {
    const data = this.apiClientService.virtualSportsChildsService().getVirtualSportsByParentSportId(parentSportId);
    return this.wrappedObservable(data);
  }

  deleteVirtualSportChild(id: string): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.virtualSportsChildsService().deleteVirtualSportChild(id);
    return this.wrappedObservable(data);
  }

  uploadImage(id: string, file: any, event?: string) {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.virtualSportsChildsService().uploadImage(id, file, event);
    return this.wrappedObservable(data);

  }

  removeImage(childSportId: string, removeImageRequest: RemoveImageRequest) {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.virtualSportsChildsService()
      .deleteImageByChildSportIdAndImageName(childSportId, removeImageRequest);
    return this.wrappedObservable(data);
  }
}
