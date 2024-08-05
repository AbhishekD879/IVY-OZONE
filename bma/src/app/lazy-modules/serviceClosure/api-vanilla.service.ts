import { Injectable } from '@angular/core';
import { ApiBase, ApiServiceFactory } from '@frontend/vanilla/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
  useFactory: apiServiceFactory,
  deps: [ApiServiceFactory]
})
export class ApiVanillaService extends ApiBase{
  public persistPlaybreakVal: boolean = false;
  public playBreakSubject = new Subject<boolean>();

  constructor() {
    super();  }
  /**
   *getter to return persistPlaybreakVal
   * @return {boolean}
   */
  get persistPlaybreak(): boolean {
    return this.persistPlaybreakVal;
  }
}

export function apiServiceFactory(apiServiceFactorySer: ApiServiceFactory) {
  return apiServiceFactorySer.create(ApiVanillaService, { product: 'portal', area: 'mobileportal', forwardProductApiRequestHeader: true });
}