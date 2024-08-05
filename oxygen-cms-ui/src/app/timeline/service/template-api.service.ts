import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ApiClientService} from '@app/client/private/services/http';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {TimelineTemplate} from '@app/client/private/models/timelineTemplate.model';

@Injectable()
export class TemplateApiService {

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

  getTemplatesByBrand(): Observable<any> {
    const data = this.apiClientService.timelineTemplate().getTemplatesByBrand();
    return this.wrappedObservable(data);
  }

  getTemplate(id: string): Observable<any> {
    const data = this.apiClientService.timelineTemplate().getSingleTemplate(id);
    return this.wrappedObservable(data);
  }

  createTemplate(template: TimelineTemplate): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.timelineTemplate().saveTemplate(template);
    return this.wrappedObservable(data);
  }

  updateTemplate(template: TimelineTemplate): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.timelineTemplate().updateTemplate(template.id, template);
    return this.wrappedObservable(data);
  }

  deleteTemplate(id: string): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.timelineTemplate().deleteTemplate(id);
    return this.wrappedObservable(data);
  }

  uploadImage(id: string, imageType: string, file: FormData) {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.timelineTemplate().uploadImage(id, imageType, file);
    return this.wrappedObservable(data);
  }

  deleteImage(id: string, imageType: string) {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.timelineTemplate().deleteImage(id, imageType);
    return this.wrappedObservable(data);
  }


}
