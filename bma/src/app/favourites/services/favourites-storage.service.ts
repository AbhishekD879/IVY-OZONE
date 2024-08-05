import { Injectable } from '@angular/core';

import { StorageService } from '@core/services/storage/storage.service';

@Injectable()
export class FavouritesStorageService {

  private readonly storageName = 'favourites';

  constructor(
    private storageService: StorageService
  ) { }

  /**
   * get()
   * @returns {Object}
   */
  get(): Object {
    return this.storageService.get(this.storageName) || {};
  }

  /**
   * store()
   * @param {Object} data
   */
  store(data: Object): void {
    this.storageService.set(this.storageName, data);
  }
}
