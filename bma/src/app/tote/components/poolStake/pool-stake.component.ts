import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

import { IPool } from './../../models/tote-event.model';
import { IFieldsControls } from './../../models/field-controls.model';

interface IValidationObject {
  outcomeId: string;
  value: number | any;
  poolData: IPool;
}

@Component({
  selector: 'pool-stake',
  templateUrl: './pool-stake.component.html'
})
export class PoolStakeComponent implements OnInit {
  @Input() outcomeId: string;
  @Input() stopBetting: boolean;
  @Input() currencySymbol: string;
  @Input() fieldControls: IFieldsControls;
  @Input() currencyCode: string;
  @Input() stakeError: string;
  @Input() poolStakes: IPool;
  @Output() readonly checkFn = new EventEmitter();
  @Output() readonly displayError = new EventEmitter();

  value: number | any;
  isIosDevice: boolean;
  readonly stakePattern: string = '^(\\d{0,12}((\\.|,)\\d{0,2})?)?$';

  constructor() {

  }

  ngOnInit(): void {
    /**
     * @member {Object} from outside allows to add clear fields functionality for ng-model value
     */
    this.fieldControls.clearField.push(this._clearField.bind(this));
  }

  /**
   * Create line validation onbect
   *
   * @param  {number} current value from the input
   * @param  {Object} data    pool data
   * @return {Object}         Object
   */
  createValidationObject(current: number, data: IPool): IValidationObject {
    return {
      outcomeId: this.outcomeId,
      value: current,
      poolData: data
    };
  }

  /**
   * Provides check functionality to outside function
   */
  onChange(): void {
    const data = this.createValidationObject(this.value, this.poolStakes);
    this.displayError.emit(data);
    this.checkFn.emit(data.value);
    this.stakeError = undefined;
  }

  /**
   * Clear error
   */
  clearStakeError(): void {
    this.stakeError = undefined;
  }

  onFormSubmit(event: Event): void {
    event.preventDefault();
  }

  setStake(): void {
    this.value = this.value.replace(",",".");
  }

  /**
   * @private
   */
  private _clearField(): void {
    this.value = null;
  }
}
