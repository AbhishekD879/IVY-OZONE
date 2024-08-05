import { Component, OnDestroy, HostBinding } from '@angular/core';
import { BetslipCounterComponent } from '@shared/components/betslipCounter/betslip-counter.component';

@Component({
  selector: 'betslip-counter',
  template: '<span [textContent]="betCounter || 0" data-crlat="betSlipCounter"></span>',
  styleUrls: ['betslip-counter.component.scss']
})
export class LadbrokesBetslipCounterComponent extends BetslipCounterComponent implements OnDestroy {
  duration: number = 500; // Animation Duration
  animation: any; // Timer
  animateBetCounter: number = 0;

  @HostBinding('class.counter-flash') animate: boolean = false;

  /**
   * Sets counter by adding betslip and digital sport selections.
   * @private
   */
  setCounter(calledOnInit: boolean = false): void {
    super.setCounter();
    if (this.animateBetCounter !== this.betCounter && !calledOnInit) {
      clearTimeout(this.animation);
      this.animate = true;
      this.animateBetCounter = this.betCounter;
      this.animation = setTimeout(() => {
        this.animate = false;
      }, this.duration);
    }
  }

  ngOnDestroy(): void {
    super.ngOnDestroy();
    clearTimeout(this.animation);
  }
}
