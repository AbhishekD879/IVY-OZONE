
import { map } from 'rxjs/operators';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import { ITimeHydraModel } from './timeModel';

@Injectable()
export class TimeSyncService {

  private timeDelta: number;
  private customerIp: string;

  constructor(
    private http: HttpClient
  ) {
    (this.getUserSessionTime(true, false) as Observable<ITimeHydraModel>)
        .subscribe((cmsData: ITimeHydraModel) => {
          this.timeDelta = cmsData.timestamp - Date.now();
          this.customerIp = cmsData['x-forward-for'];
        });
  }

  getUserSessionTime(hasTime?: boolean, isPromise?: boolean):
    Observable<ITimeHydraModel> | Promise<ITimeHydraModel> {
    const observable = this.http.get<ITimeHydraModel>(`${environment.TIME_ENDPOINT}/v1/session${hasTime && '?time=true'}`, {
      observe: 'response'
    }).pipe(map((data: HttpResponse<ITimeHydraModel>) => data.body));

    return isPromise ? observable.toPromise() : observable;
  }

  getTimeDelta(): number {
    return this.timeDelta ? this.timeDelta : 0;
  }

  get ip(): string {
    return this.customerIp || '91.232.241.59';
  }
  set ip(value:string){}
}
