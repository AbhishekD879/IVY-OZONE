import { Injectable } from '@angular/core';

@Injectable()
export class GridHelperService {
  /**
   * Calculate exact division
   * @params{number} length
   * @params{number} typesLength
   */
  modOperation(length: number, typesLength: number): number {
    return typesLength % length;
  }

  /**
   * Calculate modal value
   * @params{number} length
   * @params{number} typesLength
   */
  cellNumber(length: number, typesLength: number): number {
    return Math.abs(length - this.modOperation(length, typesLength));
  }

  /**
   * Add empty cells for row
   * @params{number} length
   * @params{number} typesLength
   */
  addCells(length: number, typesLength: number): number {
    return this.isEqualFor(length, typesLength) ? 0 : this.cellNumber(length, typesLength);
  }

  /**
   * Is equal numbers
   * @params{number} length
   * @params{number} typesLength
   */
  isEqualFor(length: number, typesLength: number): boolean {
    return this.modOperation(length, typesLength) === 0;
  }
}
