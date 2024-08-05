import { Injectable } from '@angular/core';
import { StorageService } from '@app/core/services/storage/storage.service';

@Injectable({
  providedIn: 'root'
})
export class FanzoneStorageService {

  constructor(private storageService: StorageService) { }

  /**
   * 
   * @param key - storage variable to be updated
   * @param value - value to be set
   * @returns - stores value in storage
   */
  set(key: string, value: any): boolean {
    if (!key || key === 'null') {
      return null;
    }
    return this.storageService.set(key, btoa(JSON.stringify(value)));
  }

  /**
   * 
   * @param key - storage variable to be accessed
   * @returns - stored value in storage
   */
  get(key: string) {
    if (!key || key === 'null' || (this.storageService.get(key) && !Object.keys(this.storageService.get(key)).length)) {
      return null;
    }
    return typeof this.storageService.get(key) === 'string' ? JSON.parse(atob(this.storageService.get(key))) : this.storageService.get(key);
  }
}
