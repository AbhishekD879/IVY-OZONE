import { of as observableOf,  Observable, Subject } from 'rxjs';
import { Injectable } from '@angular/core';
import { IBetFilterParams } from './bet-filter-params.model';

@Injectable()
export class BetFilterParamsService {
  betFilterParams: IBetFilterParams = {};

  constructor() {}

  get params(): IBetFilterParams {
    return this.betFilterParams;
  }
  set params(value:IBetFilterParams){}

  /**Open dialog with bet filter modes.
   * @returns Observable<IBetFilterParams>
   */
  chooseMode(): Observable<IBetFilterParams> {
     // TODO: will be back to modal dialog implementation. check git file history.
    this.betFilterParams = { mode: 'inshop' };

    return observableOf(this.betFilterParams);
  }

  selectModeAction(value: 'online' | 'inshop', subject: Subject<IBetFilterParams>): void {
    if (value) {
      this.betFilterParams.mode = value;
    }
    subject.next(this.betFilterParams);
    subject.complete();
  }

  cancelAction(value: boolean, subject: Subject<IBetFilterParams>): void {
    this.betFilterParams.cancelled = value;
    subject.next(this.betFilterParams);
    subject.complete();
  }
}
