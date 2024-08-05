import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable  } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import { Time } from '@app/fiveASideShowDown/constants/enums';
import { ContestInfo, LeaderboardInfo, IOptinContest, IPostEventResponse, IShowDown, IShowDownResponse } from '@app/fiveASideShowDown/models/show-down';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { ITeamColor } from '@app/fiveASideShowDown/models/team-color';
import { DEFAULT_TEAM_COLOURS, DYNAMIC_CLASSES, EVENTSTATUS } from '@app/fiveASideShowDown/constants/constants';
import { IPrize } from '@app/fiveASideShowDown/models/IPrize';
import { ILeaderboard } from '@app/fiveASideShowDown/models/leader-board';
import { UserService } from '@core/services/user/user.service';
import { AWSFirehoseService } from '@app/lazy-modules/awsFirehose/service/aws-firehose.service';
@Injectable({
  providedIn: FiveASideShowDownApiModule
})
export class FiveasideLeaderBoardService {
  private readonly SHOWDOWN_URL = environment.SHOWDOWN_MS;

  constructor(
    private http: HttpClient,
    private localeService: LocaleService,
    private userService: UserService,
    private awsService: AWSFirehoseService
    ) { }

  /**
   * To fetch contest information by id
   * @param {string} contestId
   * @param {string} userName
   * @returns {Observable<IShowDown>}
   */
  getContestInformationById(contestId: string, userName: string, bppToken: string): Observable<IShowDownResponse> {
    const brand = environment.brand;
    const contestInfoObj: ContestInfo = {
      contestId: contestId,
      userId: userName,
      token: bppToken,
      brand: brand
    };
    const CONTEST_INFO_URL = `${this.SHOWDOWN_URL}/${brand}/leaderboard/contest`;
    return this.http.post<IShowDownResponse>(CONTEST_INFO_URL, contestInfoObj);
  }

  /**
   * To fetch post contest information by contestid and username
   * @param {string} contestId
   * @param {string} userName
   * @returns {Observable<IPostEventDto>}
   */
  getPostContestInformationById(contestId: string, userName: string, bppToken: string): Observable<IPostEventResponse> {
    const postContestInfoObj: ContestInfo = {
      contestId: contestId,
      userId: userName,
      token: bppToken
    };
    const POST_CONTEST_INFO_URL = `${this.SHOWDOWN_URL}/postcontest`;
    return this.http.post<IPostEventResponse>(POST_CONTEST_INFO_URL, postContestInfoObj);
  }

/**
 * get legs information  For EntryId
 * @param  {string} outcomeIds
 */
  getLegsForEntryId(outcomeIds: string): Observable<any> {
    return this.http.get<IShowDown>(`${this.SHOWDOWN_URL}/postcontest/outcome/${outcomeIds}`);
  }

  /**
   * Checks if match time is full time
   * @param  {ISportEvent} event
   * @returns boolean
   */
   isFulltime(event: ISportEvent): boolean {
    const eventClock = event.clock;
    return !!eventClock && eventClock.matchTime === Time.FULL_TIME;
  }

  /**
   * form the Flag Name
   * @param  {string} name
   * @returns string
   */
  formFlagName(name: string): string {
    const teamName: string = name.toLowerCase().split(' ').join('_');
    return this.localeService.getString('fs.flagIcon', {teamName});
  }

  /**
   * @param  {string} contestId
   * @param  {string} userName
   * @returns Observable
   */
   getContestPrizeById(contestId: string): Observable<IPrize> {
    return this.http.get<IPrize>(`${this.SHOWDOWN_URL}/contest/contest-prizes/${contestId}`);
  }

  /**
   * To get Leader board Information
   * @param {userName} userName
   * @returns {Observable<IShowDown[]>}
   */
  getLeaderBoardInformation(userName: string, bppToken: string): Observable<{ contests: IShowDown[] }> {
    const BRAND = environment.brand;
    const leaderboradInfoObj: LeaderboardInfo = {
      userId: userName,
      token: bppToken,
      brand: BRAND
    };
    const LOBYY_CONTESTS_URL = `${this.SHOWDOWN_URL}/${BRAND}/leaderboard-widget`;
    return this.http.post<{ contests: IShowDown[] }>(LOBYY_CONTESTS_URL, leaderboradInfoObj);
  }

  /**
   * To set default team colors
   * @param {ITeamColor[]} teamColors
   * @param {string[]} teams
   * @returns {ITeamColor[]}
   */
  setDefaultTeamColors(teamColors: ITeamColor[], teams: string[]): ITeamColor[] {
    const teamsSelected: ITeamColor[] = [];
    teams.forEach((name: string) => {
      let selectedTeam: ITeamColor = teamColors.find((team: ITeamColor) => {
        return (team.teamName === name.toUpperCase()) || (team.secondaryNames && team.secondaryNames.includes(name.toUpperCase()));
      });
      if (!selectedTeam) {
        selectedTeam = {
          primaryColour: this.checkHexColor(null, DEFAULT_TEAM_COLOURS.primary),
          secondaryColour: this.checkHexColor(null, DEFAULT_TEAM_COLOURS.secondary)
        };
      }
      teamsSelected.push(selectedTeam);
    });
    return teamsSelected;
  }

  /**
   * To Check Hex color
   * @param {string} color
   * @param {string} defaultColor
   * @returns {string}
   */
  checkHexColor(color: string, defaultColor: string): string {
    const pattern = new RegExp('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$');
    return pattern.test(color) ? color : defaultColor;
  }

  /**
   * To Check If it has images for home and away
   * @param {ITeamColor[]} teamColors
   * @returns {boolean}
   */
  hasImageForHomeAway(teamColors: ITeamColor[]): boolean {
    if (!teamColors.length) {
      return false;
    }
    const hasTwoTeams: boolean = teamColors.length === 2;
    const validTeams: ITeamColor[] = teamColors.filter((team: ITeamColor) => {
      return team.fiveASideToggle && team.teamsImage && team.teamsImage.filename;
    });
    return hasTwoTeams && (validTeams.length === teamColors.length);
  }

  /**
   * To Set Leaderboard UI model
   * @param {ILeaderboard} leaderBoard
   * @returns {void}
   */
  setLeaderBoardData(leaderBoard: ILeaderboard): void {
    if (leaderBoard && leaderBoard.eventDetails) {
        const eventEntity = leaderBoard.eventDetails;
        leaderBoard.isStarted = eventEntity.started;
        leaderBoard.isRegularTimeFinished = eventEntity.regularTimeFinished;
        this.validateLeaderboardType(leaderBoard);
      } else {
        leaderBoard.hasInvalidEntity = true;
      }
  }

  /**
   * To Get dynamic class for rank
   * @param {string} entryRank
   * @returns {string}
   */
   getDynamicClass(entryRank: string | number): string {
    switch (entryRank.toString().length) {
      case 3: {
        return DYNAMIC_CLASSES.DIGIT_THREE;
      }
      case 4: {
        return DYNAMIC_CLASSES.DIGIT_THREE;
      }
      case 5: {
        return DYNAMIC_CLASSES.DIGIT_FIVE;
      }
      case 6: {
        return DYNAMIC_CLASSES.DIGIT_SIX;
      }
      case 7: {
        return DYNAMIC_CLASSES.DIGIT_SEVEN;
      }
      default: {
        return DYNAMIC_CLASSES.DEFAULT;
      }
    }
  }

  /**
    * Post Opt-in user info invitational contest
    * @param  {string} userName
    * @param  {string} contestId
    * @returns Observable
    */
  postOptInUserContestInfo(contestObj: IOptinContest): Observable<IShowDown> {
    const url: string = `${this.SHOWDOWN_URL}/${environment.brand}/optin-contest`;
    return this.http.post<IShowDown>(url, contestObj);
  }

  /**
   * Opt-in user to the contest
   * @returns void
   */
  optInUserIntoTheContest(contestData: IShowDown): void {
    if (contestData.isInvitationalContest && contestData.isPrivateContest && this.userService.username) {
      // Post call for Opt-in
      const contestObj: IOptinContest = {
        userId: this.userService.username,
        token: this.userService.bppToken,
        contestId: contestData.id,
        brand: environment.brand
      };
      this.postOptInUserContestInfo(contestObj).subscribe(() => {
        this.awsService.addAction('SHOWDOWN=>OPTIN_USER_CONTEST=>SUCCESS', {
          userId: this.userService.username,
          contestId: contestData.id
        });
      },
        (error) => {
          this.awsService.addAction('SHOWDOWN=>OPTIN_USER_CONTEST=>ERROR', {
            userId: this.userService.username,
            contestId: contestData.id,
            error: error
          });
        });
    }
  }

  /**
   * To Validate the state of leaderboard
   * @param {ILeaderboard} leaderboard
   * @returns {void}
   */
  private validateLeaderboardType(leaderboard: ILeaderboard): void {
    if (!leaderboard.isStarted) {
      leaderboard.type = EVENTSTATUS.PRE;
    } else if(leaderboard.isStarted && !leaderboard.isRegularTimeFinished) {
      leaderboard.type = EVENTSTATUS.LIVE;
    } else {
      leaderboard.type = EVENTSTATUS.POST;
    }
  }
}
