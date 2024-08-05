import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

import { UserService } from '@core/services/user/user.service';

import { IPool } from './../../models/tote-event.model';
import { IFieldsControls } from './../../models/field-controls.model';

interface IValidationObject {
  outcomeId: string;
  value: string;
  poolData: IPool;
}

@Component({
  selector: 'wn-pool-stakes',
  templateUrl: './wn-pool-stakes.component.html'
})
export class WnPoolStakesComponent implements OnInit {
  @Input() outcomeId: string;
  @Input() stopBetting: boolean;
  @Input() currencySymbol: string;
  @Input() fieldControls: IFieldsControls;
  @Input() currencyCode: string;
  @Input() stakeError: string;
  @Input() poolStakes: IPool;
  @Input() currencyCalculator: any;

  @Output() readonly checkFn = new EventEmitter();
  @Output() readonly displayError = new EventEmitter();

  value: string | any;
  convertedValue: string;
  readonly stakePattern: string = '^(\\d{0,12}((\\.|,)\\d{0,2})?)?$';

  constructor(
    private user: UserService
  ) {

  }

  ngOnInit(): void {
    /**
     * @member {Object} from outside allows to add clear fields functionality for ng-model value
     */
    if (!this.fieldControls) {
      return;
    }
    this.fieldControls.clearField.push(this._clearField.bind(this));
  }

  /**
   * Create line validation onbect
   *
   * @param  {number} current value from the input
   * @param  {Object} data    pool data
   * @return {Object}         Object
   */
  createValidationObject(current: string, data: IPool): IValidationObject {
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
    this.convertValue();
    this.displayError.emit(data);
    this.checkFn.emit({ value: data.value, outcomeId: data.outcomeId});
  }

  /**
   * Clear error
   */
  clearStakeError(): void {
    const data = this.createValidationObject(this.value, this.poolStakes);
    this.displayError.emit(data);
    this.stakeError = undefined;
  }

  convertValue(): string {
    this.convertedValue = this.value && this.currencyCalculator
      ? this.currencyCalculator.currencyExchange(this.currencyCode, this.user.currency, this.value) : null;
    return `${this.user.currencySymbol}${this.convertedValue}`;
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
    this.value = '';
    this.convertedValue = '';
  }
}
