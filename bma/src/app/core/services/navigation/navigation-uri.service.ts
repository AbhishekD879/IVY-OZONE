import { Injectable } from '@angular/core';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

/**
 * General purpose URI Validation service.
 */

@Injectable({
  providedIn: 'root'
})
export class NavigationUriService {
  private readonly _origin: string;

  constructor(private windowRefService: WindowRefService) {
    this._origin = this.windowRefService.nativeWindow.location.origin;
  }

  /**
   * Simple origin getter.
   */
  get origin(): string {
    return this._origin;
  }

  /**
   * Checks if given URI is internal (could be given to angular router)
   *
   * @param uri
   */
  isInternalUri(uri: string = ''): boolean {
    return !this.isAbsoluteUri(uri) || this.isSameOriginUri(uri);
  }

  /**
   * Checks if given URI is absolute (starts with http or https)
   *
   * @param uri
   */
  isAbsoluteUri(uri: string = ''): boolean {
    return /^https?:\/\//.test(uri.trim());
  }

  /**
   * Checks if given URI has same origin as current page
   *
   * @param uri
   */
  isSameOriginUri(uri: string = ''): boolean {
    return uri.includes(this._origin);
  }
}
