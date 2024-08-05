import { HttpClient, HttpResponse } from '@angular/common/http';
import { Configuration } from '../../models/configuration.model';
import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { MystableModel } from '@app/mystable-configurations/mystable.model';
import { IMyStable } from '@app/on-boarding-overlay/onboarding-mystable/onboarding-my-stable.model';

@Injectable({
  providedIn: 'root'
})
export class MyStableService extends AbstractService<Configuration>{
  myStableUrl:string = 'my-stable/configuration'

  constructor(http: HttpClient, domain: string, brand: string) { 
    super(http, domain, brand);
  }

  public postMyStableData(data:MystableModel): Observable<HttpResponse<any>> {
    return this.sendRequest<any>('post', this.myStableUrl, data);
  }

  public getMyStableData(): Observable<HttpResponse<any>> {
    const url = `${this.myStableUrl}/brand/${this.brand}`
    return this.sendRequest<any>('get', url , null);
  }

  public putMyStableData(data:MystableModel,id: string): Observable<HttpResponse<any>> {
    const url = `${this.myStableUrl}/${id}`;
    return this.sendRequest<any>('put', url, data);
  }


  public getDetailsByBrand(apiUrl:string): Observable<HttpResponse<IMyStable>> {
    return this.sendRequest('get', `${apiUrl}/brand/${this.brand}`, null);
  }
  
  public getMyStableById(url:string,id:string): Observable<HttpResponse<IMyStable>> {
    const apiUrl = `${url}/${id}`;
    return this.sendRequest('get', apiUrl, null);
  }


  public postNewMyStableImage(file: FormData, url:string): Observable<HttpResponse<IMyStable>> {
    const apiUrl = `${url}/image`;   
    return this.sendRequest('post', apiUrl, file);
  }

  public updateNewMyStableImage(file: FormData, url:string, id:string): Observable<HttpResponse<IMyStable>> {
    const apiUrl = `${url}/${id}/image`;
    return this.sendRequest('put', apiUrl, file);
  }

  public removeMyStableUploadedImage(id: string, url:string): Observable<HttpResponse<IMyStable>> {
    const apiUrl = `${url}/${id}/images`;
    return this.sendRequest('delete', apiUrl, null);
  }

  public saveOnBoardingMyStable(request:IMyStable, apiUrl:string): Observable<HttpResponse<IMyStable>> {
    return this.sendRequest('post', apiUrl, request);
  }

  public updateOnBoardingMyStable(request:IMyStable, url:string) {
    return this.sendRequest('put', `${url}/${request.id}`, request);
  }
}
