import { Component, OnInit, Input, SimpleChanges, ChangeDetectorRef, OnDestroy } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { leaderBoardUserRankData } from '@app/lazy-modules/promoLeaderBoard/constants/leaderboard.model';
import { LeaderboardService } from '@app/lazy-modules/promoLeaderBoard/service/leaderboard.service';
import { ILeaderBoard } from '@app/promotions/models/sp-promotion.model';
import { LEADERBOARD_CONSTANTS } from '@app/lazy-modules/promoLeaderBoard/constants/leaderboard-constants';
import { TimeService } from '@core/services/time/time.service';
import { map } from 'rxjs';
import { STRATEGY_TYPES } from '@app/core/constants/strategy-types.constant';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
@Component({
  selector: 'leaderboard-details',
  templateUrl: './leaderboard-details.component.html',
  styleUrls: ['./leaderboard-details.component.scss']
})
export class LeaderboardDetailsComponent implements OnInit, OnDestroy {

  constructor(protected lbService: LeaderboardService, 
    private timeService: TimeService,
    private changeDetectorRef: ChangeDetectorRef,
    private pubSubService: PubSubService) { }
  @Input() leaderboardConfigId: string;
  @Input() promotionId: string;
  @Input() userStatus: boolean;
  @Input() lbConfigData: ILeaderBoard;
  LEADERBOARD_CONSTANTS = LEADERBOARD_CONSTANTS;
  BRAND: string = LEADERBOARD_CONSTANTS.BRAND_NAME_CORAL;
  leaderboardData: leaderBoardUserRankData;
  initialLoad: number = LEADERBOARD_CONSTANTS.INITIAL_DATA_LOAD;
  datePattern = LEADERBOARD_CONSTANTS.DATE_PATTERN;
  changeStrategy = STRATEGY_TYPES.ON_PUSH;
  showLoader: boolean = false;
  
  ngOnInit(): void {
    this.leaderboardData = null;
    this.loadLeaderBoard();
    this.pubSubService.subscribe(LEADERBOARD_CONSTANTS.LEADERBOARDSUBSCRIPTION, this.pubSubService.API.BPP_TOKEN_SET, () => {
      this.leaderboardData = null;
      this.loadLeaderBoard();
    });
  }

  ngOnChanges(change: SimpleChanges) {
    this.leaderboardData = null;
    this.loadLeaderBoard();
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(LEADERBOARD_CONSTANTS.LEADERBOARDSUBSCRIPTION);
  }

  /**
  * Method to get Css class based on each col
  * @returns {void}
  */
  getCssClass(className): string {
    return `${className}`;
  }

  /**
  * Method to fetch Leaderboard Data
  * @returns {void}
  */
  getleaderBoardData(topX: number, userStatus): void {
    this.showLoader = true;
    this.lbService.fetchleaderboard(this.leaderboardConfigId, userStatus, topX, this.promotionId)
      .pipe(map((data: HttpResponse<leaderBoardUserRankData>) => data.body))
      .subscribe(data => {
        this.setLeaderboardData(data);
        if (+this.lbConfigData.topX > topX) {
          this.getleaderBoardData(+this.lbConfigData.topX, false);
        }
        this.showLoader = false;
        this.changeDetectorRef.detectChanges();
      },
      error => {
        this.leaderboardData =  null;
        this.showLoader = false;
      });
  }

  /**
  * To Check if user Rank Available
  * @returns {void}
  */
  checkUserRank(): boolean {
    return this.leaderboardData && Object.keys(this.leaderboardData.userRank).length > 0 && this.lbConfigData.individualRank;
  }

  /**
  * To load leaderboard with initial load and full data
  * @returns {void}
  */
  loadLeaderBoard(): void {
    this.getleaderBoardData(+this.lbConfigData.topX > this.initialLoad ? this.initialLoad : +this.lbConfigData.topX, (this.userStatus && this.lbConfigData.individualRank));
  }

  /**
 * To get last modified date of leaderboard
 * @returns {string}
 */
  getLastModified(): string {
    const updatedDate = new Date(this.leaderboardData && this.leaderboardData.lastFileModified).toString();
    const lastUpdatedDate = this.timeService.formatByPattern(updatedDate, this.datePattern);
    return `Updated ${lastUpdatedDate}`;
  }

  /**
  * To get style for color
  */
  getColorStyle() {
    return { 'color': this.BRAND === LEADERBOARD_CONSTANTS.BRAND_NAME_CORAL ? LEADERBOARD_CONSTANTS.LB_COL_COLOR_CORAL : '' };
  }

  /**
   * Mask the User Name
   */
  getuserNameMask(userId: string): string {
    const username = userId ? userId : '';
    return userId && userId.trim().length > 5 ? `${userId.slice(0, 5)}***` : username;
  }

  /**
  * Check if masking available
  */
  checkIfMaskingAvailable(isMaskingAvailable, val) {
    return isMaskingAvailable ? this.getuserNameMask(val) : val;
  }

  /**
  * set leaderboard Data based on userrank
  */
  setLeaderboardData(data) {
    if (this.leaderboardData && Object.keys(this.leaderboardData.userRank).length > 0) {
      this.setTopXRank(data);
    }
    else {
      this.setTopXRank(data);
      this.leaderboardData.userRank = data.userRank;
      this.leaderboardData.lastFileModified = data.lastFileModified;
    }
    this.changeDetectorRef.detectChanges();
  }

  /**
  * set topxRank based on first and second time call
  */
  setTopXRank(data) {
    if (this.leaderboardData && this.leaderboardData.topXRank.length > 0) {
      data.topXRank.splice(0, this.leaderboardData.topXRank.length);
      this.leaderboardData.topXRank.splice(this.leaderboardData.topXRank.length, 0, ...data.topXRank);
    }
    else {
      this.leaderboardData = data;
      this.leaderboardData.topXRank = data.topXRank;
    }
    this.changeDetectorRef.detectChanges();
  }

}
