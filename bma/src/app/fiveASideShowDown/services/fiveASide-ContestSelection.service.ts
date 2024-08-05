import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { IAvailableContests } from '@app/fiveASideShowDown/models/available-contests.model';
import environment from '@environment/oxygenEnvConfig';
import { ENTRY_CONFIRMATION } from '@app/fiveASideShowDown/constants/constants';
import { UserService } from '@app/core/services/user/user.service';

@Injectable({providedIn: 'root'})
  export class FiveASideContestSelectionService {
    private readonly SHOWDOWN_URL = environment.SHOWDOWN_MS;
    /**
     * Vatiable used to hold the selected contest ID
     */
    private defaultContestId: string;
  constructor(private http: HttpClient,
    private userService: UserService,
  ) { }

    /**
     * used to set the default contest ID from pre leader board
     * @param { contestId } is a string
     */
    public set defaultSelectedContest(contestId: string) {
      this.defaultContestId = contestId;
    }

    /**
     * the default contest ID which has been set from Pre leader board or returns null
     * @returns { string }
     */
    public get defaultSelectedContest():string {
      return this.defaultContestId  || null;
    }


  /**
   * getting all the contests which are linked to user and event ID
   * @param { userdetailsObj } holds the user ID and event ID info
   * @returns Observable<IAvailableContests[]>
   */
  public getAllActiveFiveASideContests(contestObj : {}): Observable<IAvailableContests[]> {
    const ALLCONTESTS_URL = `${this.SHOWDOWN_URL}/${environment.brand}/betslip-contests`;
    return this.http.post<IAvailableContests[]>(ALLCONTESTS_URL, contestObj);
 }

  /**
   * Validate the contest based on logged in user roles and contest type
   * @param  {IAvailableContests[]} activeContests
   * @returns IAvailableContests
   */
  public validateRoleBasedContests(activeContests: IAvailableContests[]): IAvailableContests[] {
    if (activeContests) {
      const userRole: string = this.isTestOrRealUser(this.userService.email);
      return activeContests.filter((contest: IAvailableContests) => {
        if (userRole === ENTRY_CONFIRMATION.testUser && contest.testAccount && !contest.realAccount
          || userRole === ENTRY_CONFIRMATION.realUser && contest.realAccount && !contest.testAccount
          || contest.realAccount && contest.testAccount) {
          return true;
        }
      });
    }
    return [];
  }

  /**
   * Determines the email belongs to test or real user
   * @param  {string} email
   * @returns string
   */
  public isTestOrRealUser(email: string): string {
    return new RegExp(ENTRY_CONFIRMATION.testAccountTokens.join('|')).test(
      email
    ) ? ENTRY_CONFIRMATION.testUser : ENTRY_CONFIRMATION.realUser;
  }
}
