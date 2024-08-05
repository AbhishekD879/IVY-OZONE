import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from '@angular/router';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs/Observable';
import {ApiClientService} from '../client/private/services/http/index';
import {forkJoin} from 'rxjs/observable/forkJoin';

@Injectable()
export class MainDataResolver implements Resolve<any> {

  constructor(
    private apiClientService: ApiClientService
  ) {
  }

  resolve(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<any> {
    return forkJoin([
      this.apiClientService.menues().getMenu(),
      this.apiClientService.brands().findAllBrands()
    ]);
  }
}
