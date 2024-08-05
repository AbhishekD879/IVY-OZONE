import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../client/private/services/http/';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {Widget} from '../../client/private/models/widget.model';
import {Order} from '../../client/private/models/order.model';

@Injectable()
export class WidgetsAPIService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService
  ) {
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
          this.handleRequestError(response.error);
        }

        return Observable.throw(response);
      });
  }

  /**
   * Get widgets data.
   * @returns {Observable<HttpResponse<Brand[]>>}
   */
  getWidgetsData(): Observable<HttpResponse<Widget[]>> {
    this.globalLoaderService.showLoader();

    const getData =  this.apiClientService.widgetsService().getWidgets();

    return this.wrappedObservable(getData);
  }

  /**
   * Load single promotino data to edit
   * @param {string} id
   * @returns {any}
   */
  getSingleWidgetData(id: string): Observable<HttpResponse<Widget>> {
    const getData =  this.apiClientService.widgetsService().getSingleWidget(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Reorder widgets
   * @param {Order} newOrder , sent id of widgets
   * @returns {any}
   */
  postNewWidgetsOrder(newOrder: Order): Observable<HttpResponse<Widget[]>>  {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.widgetsService().postNewWidgetsOrder(newOrder);
    return this.wrappedObservable(getData);
  }

  /**
   * Update widget data.
   * @param {Widget} widget
   * @return {any}
   */
  putWidgetChanges(widget: Widget): Observable<HttpResponse<Widget>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.widgetsService().putWidgetChanges(widget.id, widget);
    return this.wrappedObservable(getData);
  }

  /**
   * Handle networking error.
   * Notify user.
   */
  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
  }
}
