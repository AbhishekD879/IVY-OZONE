import { HttpClient, HttpResponse } from '@angular/common/http';
import { Configuration } from '../../models/configuration.model';
import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class OnboardBetpackService extends AbstractService<Configuration> {
  onboardBetpackUrl: string = 'bet-pack/onboarding';

  constructor(http: HttpClient, domain: string, brand: string) { 
    super(http, domain, brand);
  }

  postOnboardData(data:FormData): Observable<HttpResponse<any>> {
    return this.sendRequest<any>('post', this.onboardBetpackUrl, data);
  }

  getOnboardData(): Observable<HttpResponse<any>> {
    return this.sendRequest<any>('get', `bet-pack/onboarding/brand/${this.brand}`, null);
  }

  putOnboardData(data:FormData,id: string): Observable<HttpResponse<any>> {
    const url = `${this.onboardBetpackUrl}/${id}`;
    return this.sendRequest<any>('put', url, data);
  }

  deleteOnboard(id: string): Observable<HttpResponse<any>> {
    const url = `${this.onboardBetpackUrl}/${id}`;
    return this.sendRequest<any>('delete', url, null);
  } 
  
  deleteOnboardImage(onboarding_id:string, image_id:string){
    const url = `${this.onboardBetpackUrl}/${onboarding_id}/images/${image_id}`;
    return this.sendRequest<any>('delete',url,null)
  }

  getOnboardImage(onboarding_id:string, image_id:string){
    const url = `${this.onboardBetpackUrl}/${onboarding_id}/images/${image_id}`;
    return this.sendRequest<any>('get',url,null)
  }

  putOnboardImage(data,onboarding_id:string, image_id:string){
    const url = `${this.onboardBetpackUrl}/${onboarding_id}/images/${image_id}`;
    return this.sendRequest<any>('put',url,data)
  }

}
