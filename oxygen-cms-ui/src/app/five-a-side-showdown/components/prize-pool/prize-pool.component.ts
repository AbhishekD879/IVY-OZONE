import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { HTMLInputEvent } from '@app/five-a-side-showdown/models/contest-manager';
import { IPrizePool } from '@app/five-a-side-showdown/models/prize-pool';

@Component({
  selector: 'prize-pool',
  templateUrl: './prize-pool.component.html'
})
export class PrizePoolComponent implements OnInit {
  @Input()poolData: IPrizePool;
  @Output()prizePoolChanged: EventEmitter<IPrizePool> = new EventEmitter<IPrizePool>();
  prizePool: IPrizePool;
  form: FormGroup;

  constructor() { }

  ngOnInit(): void {
    this.prizePool = {} as IPrizePool;
    this.prizePool = {...this.prizePool, ...this.poolData};
    this.form = new FormGroup({
      cash: new FormControl(''),
      firstPlace: new FormControl(''),
      tickets: new FormControl(''),
      freeBets: new FormControl(''),
      vouchers: new FormControl(''),
      totalPrizes: new FormControl(''),
      summary: new FormControl('')
    });
    this.emitPrizePool();
  }

  /**
   * To Emit Prizepool data on form change
   */
  private emitPrizePool(): void {
    this.form.valueChanges.subscribe((updatedPriceForm) => {
      this.prizePoolChanged.emit(JSON.parse(JSON.stringify(updatedPriceForm)));
    });
  }

  /**
   * To avoid special characters 
   * @param  event 
   * @returns 
   */
  blockSpecialChars(event: HTMLInputEvent): void {
    event.target.value = event.target.value.replace(/[^a-zA-Z0-9]/g,'');
  }
}
