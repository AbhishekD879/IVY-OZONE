import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class StakeValidatorService {
  /**
   * Validation state
   *
   * @param  {object} data [description]
   * @return {object}      [description]
   */
  getValidationState(options) {
    const { stake, totalStake, pool } = options;
    return {
      minStakePerLine: this.isMinValid(stake, pool.minStakePerLine),
      maxStakePerLine: this.isMaxValid(stake, pool.maxStakePerLine),
      stakeIncrementFactor: this.isIncrementValid(stake, pool.stakeIncrementFactor),
      minTotalStake: this.isMinValid(totalStake, pool.minTotalStake),
      maxTotalStake: this.isMaxValid(totalStake, pool.maxTotalStake)
    };
  }

  /**
   * Checking if the increment follows the rules
   *
   * @param  {number}  value  Current value
   * @param  {number}  factor Increment factor
   * @return {Boolean}        true / false
   */
  private isIncrementValid(value: number, factor: number): boolean {
    const current = isNaN(value) ? 0 : value;
    return Math.floor((Math.abs(current) * 100)) % Math.floor((factor * 100)) !== 0;
  }

  /**
   * Checking if the min value follows the rules
   *
   * @param  {number}  value    Number to check
   * @param  {number}  minStake Boundary value
   * @return {Boolean}          [description]
   */
   private isMinValid(value: number, minStake: number): boolean {
    return minStake > value;
  }

  /**
   *  Checking if the max value follows the rules
   *
   * @param  {number}  value    Number to check
   * @param  {number}  maxStake Boundary value
   * @return {Boolean}          [description]
   */
  private isMaxValid(value: number, maxStake: number): boolean {
    return maxStake < value;
  }
}
