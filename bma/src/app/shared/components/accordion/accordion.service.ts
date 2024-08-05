import { Injectable } from '@angular/core';
import { StorageService } from '@core/services/storage/storage.service';
import * as _ from 'underscore';

@Injectable()
export class AccordionService {

  private storagePrefix = 'accordion_';

  constructor(private storage: StorageService) {
    this.storagePrefix = 'accordion_';
  }
  /**
   * get accordion state with certain id
   * @param id {string}
   */
  getState(id: string): void {
    return this.storage.get(`${this.storagePrefix}${id}`);
  }

  /**
   * remove accordion state with certain id
   * @param id {string}
   */
  removeState(id: string): void {
    this.storage.remove(`${this.storagePrefix}${id}`);
  }

  /**
   * save to storage object with all accordion's states for certain location
   * @param stateObj {object}
   * @param location {string}
   */
  saveLocationStates(stateObj: { [key: string]: any }, location: string): void {
    // is used when use accordions changes many times for one location
    this.storage.set(`${this.storagePrefix}${location}`, JSON.stringify(stateObj));
  }

  /**
   * save single state or all states for whole location
   * @param state {boolean}
   * @param memoryId {string} - accordion id
   * @param memoryLocation {string} - place where accordion is used
   */
  saveStateDependsOnParams(state: boolean, memoryId: string, memoryLocation: string): void {
    if (!memoryLocation) {
      this.saveState(memoryId, state);
      return;
    }
    // if memoryLocation we should group all states for certain location to have ability
    // to access all of them with certain object
    const locationStates = this.getLocationStates(memoryLocation);
    locationStates[memoryId] = state;
    this.saveLocationStates(locationStates, memoryLocation);
  }

  /**
   * get object with states for all accordions for certain location
   * @param location {string}
   */
  getLocationStates(location: string): any {
    const locationStates = <string>this.storage.get(`${this.storagePrefix}${location}`);
    return locationStates ? JSON.parse(locationStates) : {};
  }

  /**
   * remove certain accordion's state from all states for certain location
   * @param ids {array}
   * @param location {string}
   */
  removeStatesFromLocation(ids: Array<string>, location: string): void {
    if (!ids || ids.length === 0 || !location) {
      return;
    }
    const locationStates = this.getLocationStates(location);
    _.forEach(ids, id => {
      delete locationStates[id];
    });
    // if location has no accordion's states location object should be removed from storage
    // else update storage without removed states
    if (_.isEmpty(locationStates)) {
      this.storage.remove(`${this.storagePrefix}${location}`);
    } else {
      this.saveLocationStates(locationStates, location);
    }
  }

  /**
   * save accordion state for certain id
   * @param id {string}
   * @param state {boolean}
   */
  private saveState(id: string, state: boolean): void {
      this.storage.set(`${this.storagePrefix}${id}`, state);
  }
}
