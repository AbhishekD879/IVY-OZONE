import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ApiClientService} from '@app/client/private/services/http';
import {Observable} from 'rxjs/Observable';
import {HttpErrorResponse} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {QEQuickLinks} from '@app/client/private/models/qeQuickLinks.model';

@Injectable()
export class QEQuickLinksApiService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService
  ) {
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

  getQEQuickLinks(): Observable<any> {
    const data = this.apiClientService.qeQuickLinksService().findAll();
    return this.wrappedObservable(data);
  }

  getQEQuickLinksByBrand(): Observable<any> {
    const data = this.apiClientService.qeQuickLinksService().findAllByBrand();
    return this.wrappedObservable(data);
  }

  getQEQuickLinksById(id: string): Observable<any> {
    const data = this.apiClientService.qeQuickLinksService().findOne(id);
    return this.wrappedObservable(data);
  }

  createQEQuickLinks(qeQuickLinks: QEQuickLinks): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.qeQuickLinksService().save(qeQuickLinks);
    return this.wrappedObservable(data);
  }

  updateQEQuickLinks(qeQuickLinks: QEQuickLinks): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.qeQuickLinksService().update(qeQuickLinks);
    return this.wrappedObservable(data);
  }

  deleteQEQuickLinks(id: string): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.qeQuickLinksService().delete(id);
    return this.wrappedObservable(data);
  }
}
