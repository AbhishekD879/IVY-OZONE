import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import environment from '@environment/oxygenEnvConfig';

@Injectable({
  providedIn: 'root'
})
export class StorageService {

  isSupported: boolean = false;
  protected prefix: string;
  protected storageType: 'localStorage' | 'sessionStorage';
  private webStorage: Storage;

  constructor (protected windowRefService: WindowRefService) {
    this.init();
  }

  /**
   * get local storage method to retrieves a value stored in the storage/cookie collection
   * @param key
   */
  get(key: string): any {
    if (this.isSupported) {
      const item = this.webStorage.getItem(this.deriveKey(key));
      if (!item || item === 'null') {
        return null;
      }
      try {
        return JSON.parse(item);
      } catch (e) {
        return null;
      }
    }

    return this.getCookie(`${environment.STORAGE_SERVICE_PREFIX}.${key}`);
  }

  /**
   * set local storage method to sets the value to the local storage if storage works, if not save it to the cookies.
   * @param key
   * @param value
   */
  set(key: string, value: any): boolean {
    if (this.isSupported) {
      if (value === undefined) {
        value = null;
      } else {
        value = JSON.stringify(value);
      }
      this.webStorage.setItem(this.deriveKey(key), value);
      return true;
    }

    this.setCookie(`${environment.STORAGE_SERVICE_PREFIX}.${key}`, value);
    return false;
  }

  /**
   * remove local storage method to remove the value from the local storage if storage works,
   * if not remove it from the cookies.
   * @param key
   */
  remove(key: string): boolean {
    if (this.isSupported) {
      this.webStorage.removeItem(this.deriveKey(key));
      return true;
    }

    this.removeCookie(`${environment.STORAGE_SERVICE_PREFIX}.${key}`);
    return false;
  }

  /*
   * Retrieves a value stored in the cookie collection
   * @param {string} key The name of the cookie
   * @return {string} The cookie value. If not found, an empty string is returned
   */
  getCookie(key: string): string {
    const cookies = this.windowRefService.document.cookie.split(';'),
        len = cookies.length;
    let data, i;

    for (i = 0; i < len; i++) {
      data = cookies[i].split('=', 2);

      if (data[0].replace(/^\s+|\s+$/g, '') === key) {
        const value = decodeURIComponent(data[1]);
        return this.isJsonObject(value) ? JSON.parse(value) : value;
      }
    }

    return '';
  }

  /*
   * Stores a cookie value in the cookie collection
   * @param {string} key The name of the cookie
   * @param {*} value The value to store
   * @param {string} domainName
   * @param {number} [exdays] Number of days the cookie will be valid before it expires
   */
  setCookie(key: string, value: string | Array<any> | {}, domainName = environment.DOMAIN, exdays = 365, isSecure = false) {
    if (_.isUndefined(value)) {
      return false;
    } else if (_.isArray(value) || _.isObject(value)) {
      value = JSON.stringify(value);
    }

    let cookie = `${key}=${encodeURIComponent(value as string)}`;
    const exmilisecond = exdays * 24 * 60 * 60 * 1000,
        exdate = new Date();

    exdate.setTime(exdate.getTime() + exmilisecond);
    cookie += `; expires=${exdate.toUTCString()}; path=/`;

    if (domainName) {
        cookie += `; domain=${domainName}`;
    }

    if (isSecure && this.windowRefService.nativeWindow.location.href.search('https') !== -1) {
      cookie += '; secure';
    }
    this.windowRefService.document.cookie = cookie;
  }

  /*
   * Removes a cookie
   *
   * @param {string} key The name of the cookie
   */
  removeCookie(key: string): void {
    this.setCookie(key, '', undefined, -1);
  }

  /**
   * Checks if set storageType is supported by the browser and sets the webStorage object
   */
  protected checkSupport(): boolean {
    try {
      const supported = this.storageType in this.windowRefService.nativeWindow
        && this.windowRefService.nativeWindow[this.storageType] !== null;

      if (supported) {
        this.webStorage = this.windowRefService.nativeWindow[this.storageType];

        // When Safari (OS X or iOS) is in private browsing mode, it
        // appears as though localStorage is available, but trying to
        // call .setItem throws an exception.
        //
        // "QUOTA_EXCEEDED_ERR: DOM Exception 22: An attempt was made
        // to add something to storage that exceeded the quota."
        const key = `${this.prefix}__${Math.round(Math.random() * 1e7)}`;
        this.webStorage.setItem(key, '');
        this.webStorage.removeItem(key);
      }

      return supported;
    } catch (e) {
      return false;
    }
  }

  /**
   * Adds prefix to the key
   * @param key
   */
  protected deriveKey(key: string) {
    return `${this.prefix}${key}`;
  }

  /**
   * Sets key prefix
   * @param prefix
   */
  protected setPrefix(prefix: string): void {
    this.prefix = prefix;
    const PERIOD: string = '.';
    if (this.prefix && !this.prefix.endsWith(PERIOD)) {
      this.prefix = `${this.prefix}${PERIOD}`;
    }
  }

  /**
   * Check if value is object to avoid throw exception when JSON.parse(value)
   * @param value
   */
  protected isJsonObject(value: string): boolean {
    try {
      value = JSON.parse(value);
    } catch (e) {
      return false;
    }

    return typeof value === 'object' && value !== null;
  }

  /**
   * Sets storage type, prefix and isSupported properties
   */
  protected init(): void {
    this.storageType = 'localStorage';
    this.setPrefix(environment.STORAGE_SERVICE_PREFIX);
    this.isSupported = this.checkSupport();
  }
}
