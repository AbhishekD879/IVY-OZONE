import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class SlpSpinnerStateService {

  slpSpinnerStateObservable$: Subject<number>;
  private spinnersCounter: number = 1;

  createSpinnerStream(): void {
    this.clearSpinnerState();
    this.slpSpinnerStateObservable$ = new Subject();
  }

  handleSpinnerState(): void {
    this.slpSpinnerStateObservable$
      && !this.slpSpinnerStateObservable$.closed
      && this.slpSpinnerStateObservable$.next(this.spinnersCounter++);
  }

  clearSpinnerState(): void {
    this.spinnersCounter = 1;
    this.slpSpinnerStateObservable$ && this.slpSpinnerStateObservable$.unsubscribe();
  }
}
