import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import { ENTRY_CONFIRMATION } from '@app/fiveASideShowDown/constants/constants';

@Injectable()
  export class FiveASideEntryConfirmationService {
    constructor(private http: HttpClient) {}

  /**
   * Check if the logged in user is a test user
   * @param email { string }
   * @returns { string }
   */
  public isTestOrRealUser(email: string): string {
    return new RegExp(ENTRY_CONFIRMATION.testAccountTokens.join('|')).test(
      email
    ) ? ENTRY_CONFIRMATION.testAccount : ENTRY_CONFIRMATION.realAccount;
  }

    /**
     * getting the data from ShowDown EntryConfirmation api
     * @param showdownObj
     * @returns  showdownObj
     */
    getShowdownConfirmationDisplay(showdownObj: {}): Observable<{showdown: boolean}> {
      const ENTRYCONFIRMATION_URL = `${environment.SHOWDOWN_MS}/${environment.brand}/${'entryconfirmation'}`;
      return this.http.post<{showdown: boolean}>(ENTRYCONFIRMATION_URL, showdownObj);
    }
}
