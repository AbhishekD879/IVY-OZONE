import { ViewportScroller } from '@angular/common';
import { AfterViewInit, Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { DeviceService } from '@app/core/services/device/device.service';
import { EURO_MESSAGES, EURO_DISPLAY_MESSAGES, BADGE_COLOR } from '@app/euro/constants/euro-constants';
import { IEuroDisplayMessages } from '@app/euro/models/euro.model';
import { UserService } from '@app/core/services/user/user.service';
import { MatchRewardsBadges } from '@app/euro/constants/match-rewards-badge';
import { BadgeRewards } from '@app/euro/constants/badge-rewards';

@Component({
  selector: 'match-rewards',
  templateUrl: './match-rewards.component.html',
  styleUrls: ['./match-rewards.component.scss']
})
export class MatchRewardsComponent implements OnInit, AfterViewInit, OnChanges {

  @Input() public statusrenderIndex: number;
  @Input() public currentBadge: number;
  @Input() public freeBetPositionSequence: number[];
  @Input() public totalNoOfBadges: number;
  public tokenAmount: string;
  @Input() public placedBetToday: boolean;
  public euroBadges: string[];
  public freeTokenMessage: string[];
  public readonly EURO_DISPLAY_MESSAGE: IEuroDisplayMessages = EURO_DISPLAY_MESSAGES;
  public freebetToken: string;
  public matchRewardBadge: MatchRewardsBadges;
  public freeBetDay: boolean;
  @Output() readonly freebetSuccessMsg = new EventEmitter();
  @Input('tokenAmount')
  set TokenAmount(tokenAmount: string) {
    this.tokenAmount = tokenAmount || EURO_MESSAGES.DEFAULT_TOKEN;
    this.tokenAmount = (parseInt(this.tokenAmount, 10)).toString();
  }

  constructor(
    public scroller: ViewportScroller,
    public deviceService: DeviceService,
    public userService: UserService
  ) { }

  ngOnInit(): void {
    this.init();
  }

  ngAfterViewInit() {
    if (!this.deviceService.isDesktop) {
      this.scrollDown();
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if (!changes['freeBetPositionSequence'].isFirstChange()) {
      this.init();
    }
  }

  /**
   * to initialise the logic
   * @returns {void}
   */
  public init(): void {
    this.currentBadge = this.currentBadge === 0 ? 1 : this.currentBadge;
    this.totalNoOfBadges = this.userService.status ? this.totalNoOfBadges : EURO_MESSAGES.TOTAL_BADGES;
    this.matchRewardBadge = new MatchRewardsBadges();
    this.calculateNextFreeToken();
    this.populateMatchRewardBadges(this.totalNoOfBadges);
  }

  /**
   * to enable dynamic scrolling in mobile view
   * @returns {void}
   */
  public scrollDown(): void {
    if (this.currentBadge > 6) {
      this.scroller.scrollToAnchor(`${EURO_MESSAGES.EURO_BADGE}-${this.currentBadge - 4}`);
      window.scrollBy(0, -106);
    }
  }

  /**
   * to calculate how many badges user needs to collect to get a free token
   * @returns {void}
   */
  public calculateNextFreeToken(): void {
    this.freeTokenMessage = [];
    this.freebetToken = `${this.userService.currencySymbol}${this.tokenAmount} ${EURO_MESSAGES.FREE_BET}`;
    this.freeBetPositionSequence.every(currPos => {
      if (currPos - this.currentBadge >= 0) {
        const nextFreeBet = currPos - this.currentBadge;
        this.freeTokenMessage[0] = EURO_DISPLAY_MESSAGES.FREEBET.REWARD;
        this.freeTokenMessage[1] = EURO_DISPLAY_MESSAGES.FREEBET.QUALIFYING_SINGLE_BET;
        this.freeTokenMessage[2] = '';
        if (this.placedBetToday) {
          this.freeTokenMessage[0] = EURO_DISPLAY_MESSAGES.CONGRATULATIONS_MSG.CONGRATS;
          this.freeTokenMessage[1] = EURO_DISPLAY_MESSAGES.CONGRATULATIONS_MSG.EARNED;
          if (nextFreeBet === 0) {
            this.freeTokenMessage[1] = EURO_DISPLAY_MESSAGES.CONGRATULATIONS_MSG.EARNED;
            this.freeTokenMessage[2] = this.freebetToken;
            this.freeTokenMessage[3] = EURO_DISPLAY_MESSAGES.CONGRATULATIONS_MSG.MORE_STAMPS;
            this.freeBetDay = true;
            setTimeout(() => { this.freebetSuccessMsg.emit(this.freeTokenMessage); }, 500);
          } else {
            this.freeTokenMessage[1] = EURO_DISPLAY_MESSAGES.CONGRATULATIONS_MSG.STAMP;
            this.freeTokenMessage[3] = EURO_DISPLAY_MESSAGES.CONGRATULATIONS_MSG.NEXT_DAY;
          }
        } else {
          this.freeTokenMessage[2] = EURO_DISPLAY_MESSAGES.FREEBET.QUALIFYING_MULTIPLE_BET
          .replace('$freeBet', `${this.userService.currencySymbol}${this.tokenAmount}`);
        }
        return false;
      }
      return true;
    });
  }

  /**
   * to enable dynamic badge loading based on color
   * @param index {number}
   * @returns {void}
   */
  public populateMatchRewardBadges(badges: number): void {
    this.matchRewardBadge.allBadges = new Array<BadgeRewards>(badges);
    for (let badgeIndex = 0; badgeIndex < badges; badgeIndex++) {
      const badgeRewards = new BadgeRewards();
      badgeRewards.yellowHighlight = this.isYellowLineDisplayed(badgeIndex);
      badgeRewards.freeBetToken = this.populateFreeBetToken(badgeIndex);
      badgeRewards.message = this.populateMessage(badgeIndex);
      badgeRewards.badgeType = this.populateBadgeColor(badgeIndex);
      this.matchRewardBadge.allBadges[badgeIndex] = badgeRewards;
    }
  }

  /**
   * logic whether to display yellowline
   * @param badgeNumber {number}
   * @returns {boolean}
   */
  public isYellowLineDisplayed(badgeNumber: number): boolean {
    if (this.currentBadge === badgeNumber + 1 && !this.placedBetToday && this.userService.status) {
      return true;
    }
    return false;
  }

  /**
   * logic to populate free bet value
   * @param badgeNumber {number}
   * @returns {string}
   */
  public populateFreeBetToken(badgeNumber: number): string {
    if (this.freeBetPositionSequence.indexOf(badgeNumber + 1) > -1) {
      return this.freebetToken;
    }
    return '';
  }

  /**
   * logic to populate content after and before placing bet
   * @param index {number}
   * @returns {string[]}
   */
  public populateMessage(badgeNumber: number): string[] {
    if (this.statusrenderIndex === badgeNumber && this.userService.status) {
      return this.freeTokenMessage;
    }
    return [];
  }

  /**
   * logic to populate badge color
   * @param index {number}
   * @returns {string}
   */
  public populateBadgeColor(badgeNumber: number): string {
    if(this.userService.status && ((badgeNumber+1) < this.currentBadge || (this.currentBadge === (badgeNumber+1) && this.placedBetToday))) {
      if (badgeNumber % 3 === 0) {
        return BADGE_COLOR.BALL_0;
      } else if (badgeNumber % 3 === 1) {
        return BADGE_COLOR.BALL_1;
      } else {
        return BADGE_COLOR.BALL_2;
      }
    }
    return BADGE_COLOR.BALL_EMPTY;
  }
}
