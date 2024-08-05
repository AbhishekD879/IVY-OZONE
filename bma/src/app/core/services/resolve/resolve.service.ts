import { Injectable } from '@angular/core';

@Injectable()
export class ResolveService {

  private data: { [key: string]: any } = {};

  /**
   * Store promise resolved data
   * @param {Promise<any>} fn
   * @param {string} key
   * @returns {Promise<void>}
   */
  set(fn: Promise<any>, key: string): Promise<void> {
    return new Promise((resolve, reject) => {
      fn.then(response => {
        this.data[key] = response;
        resolve();
      }, () => {
        reject();
      });
    });
  }

  /**
   * Get previously stored data
   * @param {string} key
   * @returns {any}
   */
  get(key: string): any {
    return key in this.data ? this.data[key] : null;
  }

  /**
   * Delete stored data for key
   * @param {string} key
   */
  reset(key?: string): void {
    delete this.data[key];
  }

}
