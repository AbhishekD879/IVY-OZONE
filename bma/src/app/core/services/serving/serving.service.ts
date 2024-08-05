import { Location } from '@angular/common';
import { Injectable } from '@angular/core';
import { UserService } from '@core/services/user/user.service';

@Injectable()
export class ServingService {

  /**
   * Remove leading / and #
   * @param {string} path
   * @returns {string}
   */
  static trimPath(path: string): string {
    return path.replace(/^[#\/]+/, '');
  }

  constructor(private location: Location,
              private userService: UserService) {}

  /**
   * Check if current location starts with path
   * @param {string} path
   * @returns {boolean}
   */
  pathStartsWith(path: string): boolean {
    if (typeof path !== 'string') {
      return false;
    }
    const trimmedPath = ServingService.trimPath(path);
    const trimmedLocation = ServingService.trimPath(this.location.path());

    return trimmedPath.length ? (trimmedLocation.indexOf(trimmedPath) === 0) : trimmedPath === trimmedLocation;
  }

  /**
   * Get active class
   * @param {string} path
   * @returns {boolean}
   */
  getClass(path: string): boolean {
    if (path) {
      const regex = /(\/[^\/]+)|(^\/$)/, // eslint-disable-line no-useless-escape
          match = this.location.path().match(regex),
          matchPath = match && match[0] || '/',
          absPath = path.length > 1 && !path.startsWith('/') ? `/${path}` : path;
      return absPath === matchPath;
    }
    return false;
  }

  /**
   * Send cookies if link is external
   * @param {string} uri
   */
  sendExternalCookies(uri: string | boolean): void {
    if (uri) {
      this.userService.setExternalCookies();
    }
  }

}
