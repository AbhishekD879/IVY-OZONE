import { Injectable } from '@angular/core';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ApiClientService} from '@app/client/private/services/http';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import { ILottos } from './lotto.model';
@Injectable({
  providedIn: 'root'
})
export class LottoService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
  ) { }
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
  createLotto(ILotto: any): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.lottosService().saveLotto(ILotto);
    return this.wrappedObservable(data);
  }
  getLottery(id: string): Observable<ILottos>{
    const data = this.apiClientService.lottosService().getLottery(id);
    return this.wrappedObservable(data);
  }
}