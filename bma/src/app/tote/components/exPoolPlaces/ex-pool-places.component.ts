import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IExTrCheckboxMap } from './ex-tr-checkbox-map.model';
import * as _ from 'underscore';

@Component({
  selector: 'ex-pool-places',
  templateUrl: './ex-pool-places.component.html'
})

/**
 * @description exPoolPlaces component
 */
export class ExPoolPlacesComponent {

  outcomeIds: string[];

  @Input() outcomeId: string;
  @Input() stopBetting: boolean;
  @Input() selectedPlaces: any;
  @Input() map: IExTrCheckboxMap[];
  @Output() readonly checkFn = new EventEmitter();


  constructor() { }

  onChange(): void {
    this.checkFn.emit(this.outcomeId);
  }

  runChecks(map: IExTrCheckboxMap[]): void {
    this.outcomeIds = [];
    this.setEnables(map);
    _.each(map, (places, id: string | number) => {
      _.each(places, (place, index: string | number) => {
        if (places[index] === 'checked') {
          this.outcomeIds[index] = id;
          this.selectedPlaces.status = false;
          // Two places should be selected for exacta
          if ((this.map[id].length === 2 && _.without(this.outcomeIds, undefined).length > 1 ||
               this.map[id].length === 3 && _.without(this.outcomeIds, undefined).length > 2 )) {
            this.selectedPlaces.status = true;
            this.checkFn.emit(this.outcomeIds);
          }
          this.setDisables(map, id, index);
        }
      });
    });
  }

  setEnables(map: IExTrCheckboxMap[]): void {
    _.each(map, places => {
      _.each(places, (place, index) => {
        if (place !== 'checked') {
          places[index] = 'enabled';
        }
      });
    });
  }

  setDisables(map: IExTrCheckboxMap[], row: string| number, col: string | number): void {
    _.each(map, (places, id) => {
      _.each(places, (place, index) => {
        if ((id === row || index === col) && places[index] !== 'checked') {
          places[index] = 'disabled';
        }
      });
    });
  }

  /**
   * Run checkboxes validation
   * @param {String} id
   * @param {Number} index
   */
  checkPlace(id: string | number, index: string | number) {
    const checkbox = this.map[id][index];

    if (checkbox === 'enabled') {
      this.map[id][index] = 'checked';
    }

    if (checkbox === 'checked') {
      this.map[id][index] = 'enabled';
    }

    this.runChecks(this.map);
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  trackByIndex(index: number): number {
    return index;
  }
}
