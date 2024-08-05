import { Injectable } from '@angular/core';
import { AbstractService } from './transport/abstract.service';
import { Configuration } from '@app/client/public/models';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { AutoSeoPage } from '@app/client/private/models/seopage.model';

@Injectable()
export class AutoseoService extends AbstractService<Configuration> {
  private readonly autoseoPageUrl: string = 'seo-auto-page';
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }
  /**
   * @returns request to get all the autoseopages
   */
  public getAutoSeoPageList(): Observable<HttpResponse<AutoSeoPage[]>> {
    return this.sendRequest<AutoSeoPage[]>('get', `${this.autoseoPageUrl}/brand/${this.brand}`, null);
  }
  /**
   * @param newautoseopage 
   * @returns request to save new autoseopage
   */
  public postNewAutoSeoPage(newautoseopage: AutoSeoPage): Observable<HttpResponse<AutoSeoPage>> {
    return this.sendRequest<AutoSeoPage>('post', this.autoseoPageUrl, newautoseopage);
  }
  /**
   * @param autoseopageid 
   * @param updatedautoseopageData 
   * @returns request to save updatedautoseopage
   */
  public putAutoSeoPageChanges(autoseopageid: string, updatedautoseopageData: AutoSeoPage): Observable<HttpResponse<AutoSeoPage>> {
    const apiUrl = `${this.autoseoPageUrl}/${autoseopageid}`;
    return this.sendRequest<AutoSeoPage>('put', apiUrl, updatedautoseopageData);
  }
  /**
   * @param autoseopageid 
   * @returns request to delete a autoseopage
   */
  public deleteAutoSeoPage(autoseopageid: string): Observable<HttpResponse<void>> {
    const url = `${this.autoseoPageUrl}/${autoseopageid}`;
    return this.sendRequest<void>('delete', url, null);
  }
}