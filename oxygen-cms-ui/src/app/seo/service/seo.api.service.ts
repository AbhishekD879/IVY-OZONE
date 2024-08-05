import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../client/private/services/http/';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {SeoPage} from '../../client/private/models/seopage.model';
import {HttpResponse} from '@angular/common/http';
import { AutoSeoPage } from '@app/client/private/models/seopage.model';

@Injectable()
export class SeoAPIService {
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
          this.handleRequestError(response.error);
        }

        return Observable.throw(response);
      });
  }

  /**
   * Get widgets data.
   * @returns {Observable<HttpResponse<Brand[]>>}
   */
  getSeoListData(): Observable<HttpResponse<SeoPage[]>> {
   this.globalLoaderService.showLoader();

    const getData =  this.apiClientService.seoPageService().getSeoPageList();

    return this.wrappedObservable(getData);
  }

  /**
   * Load single promotino data to edit
   * @param {string} id
   * @returns {any}
   */
  getSingSeoItemData(id: string): Observable<HttpResponse<SeoPage>> {
    const getData =  this.apiClientService.seoPageService().getSingleSeoPage(id);
    return this.wrappedObservable(getData);
  }

  putSeoItemChanges(seoPage: SeoPage): Observable<HttpResponse<SeoPage>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.seoPageService().putSeoPageChanges(seoPage.id, seoPage);
    return this.wrappedObservable(getData);
  }

  deleteSeoPage(id: string): Observable<HttpResponse<void>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.seoPageService().deleteSeoPage(id);
    return this.wrappedObservable(getData);
  }

  createSeoItem(seoPage: SeoPage): Observable<HttpResponse<SeoPage>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.seoPageService().postNewSeoPage(seoPage);
    return this.wrappedObservable(getData);
  }

  /**
   * Handle networking error.
   * Notify user.
   */
  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
  }

  /**
   * @returns all the autoseopagesData
   */
  getAutoSeoListData(): Observable<HttpResponse<AutoSeoPage[]>> {
    this.globalLoaderService.showLoader();
    const getautoseoData = this.apiClientService.autoseoPageService().getAutoSeoPageList();
    return this.wrappedObservable(getautoseoData);
  }
  /** 
   * @param autoseoPage 
   * @returns upadated autoseopage data
   */
  putAutoSeoItemChanges(autoseoPage: AutoSeoPage): Observable<HttpResponse<AutoSeoPage>> {
    this.globalLoaderService.showLoader();
    const getautoseoData = this.apiClientService.autoseoPageService().putAutoSeoPageChanges(autoseoPage.id, autoseoPage);
    return this.wrappedObservable(getautoseoData);
  }
  /**
   * @param autoseopageid
   * @returns autoseopage data to remove the page
   */
  deleteAutoSeoPage(autoseopageid: string): Observable<HttpResponse<void>> {
    this.globalLoaderService.showLoader();
    const getautoseoData = this.apiClientService.autoseoPageService().deleteAutoSeoPage(autoseopageid);
    return this.wrappedObservable(getautoseoData);
  }
  /**
   * @param autoseoPage 
   * @returns new autoseopage data
   */
  createAutoSeoItem(autoseoPage: AutoSeoPage): Observable<HttpResponse<AutoSeoPage>> {
    this.globalLoaderService.showLoader();
    const getautoseoData = this.apiClientService.autoseoPageService().postNewAutoSeoPage(autoseoPage);
    return this.wrappedObservable(getautoseoData);
  }
}
