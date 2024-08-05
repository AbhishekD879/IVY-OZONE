import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ApiClientService} from '@app/client/private/services/http';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {FiveASideFormation} from '@app/client/private/models/fiveASideFormation.model';

@Injectable()
export class FiveASideApiService {
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
   * @returns {Observable<HttpResponse<FiveASideFormation[]>>}
   */
  getFormationsList() {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.fiveASideFormations().findAllFormations();

    return this.wrappedObservable(getData);
  }

  /**
   * Load single formation data to edit.
   * @param {string} id
   * @returns {any}
   */
  getSingleFormation(id: string) {
    const getData =  this.apiClientService.fiveASideFormations().getSingleFormation(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to league.
   * @param {FiveASideFormation} formation
   */
  putFormationChanges(formation: FiveASideFormation) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.fiveASideFormations().editFormation(formation);
    return this.wrappedObservable(getData);
  }

  /**
   * Deletes formation.
   * @param {string} id
   */
  deleteFormation(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.fiveASideFormations().deleteFormation(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Creates new formation.
   * @param {FiveASideFormation} formation
   */
  createFormation(formation: FiveASideFormation) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.fiveASideFormations().createFormation(formation);
    return this.wrappedObservable(getData);
  }

  /**
   * Posts new order for formations.
   * @param {any} formationsOrder
   * @returns {Observable<HttpResponse<FiveASideFormation[]>>}
   */
  postNewFormationsOrder(formationsOrder: any) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.fiveASideFormations().postNewFormationsOrder(formationsOrder);

    return this.wrappedObservable(getData);
  }
}
