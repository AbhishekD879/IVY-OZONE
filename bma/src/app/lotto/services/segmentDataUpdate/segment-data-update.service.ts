import { ILottoChangeEvent } from '../../models/lotteries-config.model';
import { Subject } from 'rxjs';
import { Injectable } from '@angular/core';

@Injectable()
export class SegmentDataUpdateService {

  readonly dataSubject: Subject<ILottoChangeEvent>;
  public headerTime: object;

  constructor() {
    this.dataSubject = new Subject();
  }

  get changes(): Subject<ILottoChangeEvent> {
    return this.dataSubject;
  }
  set changes(value:Subject<ILottoChangeEvent>){}
}
