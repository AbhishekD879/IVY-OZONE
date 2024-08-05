import { Component, OnDestroy, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FiveasideLeaderBoardService } from '@fiveASideShowDownModule/services/fiveaside-leader-board.service';
import { UserService } from '@core/services/user/user.service';
import { ILeaderboard } from '@app/fiveASideShowDown/models/leader-board';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { EVENTSTATUS, LEADERBOARD_WIDGET, PUBSUB_API } from '@app/fiveASideShowDown/constants/constants';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { rgyellow } from '@app/bma/constants/rg-yellow.constant';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { IShowDown, IShowDownResponse } from '../../models/show-down';

@Component({
  selector: 'fiveaside-leader-board',
  template: ``
})
export class FiveASideLeaderBoardComponent implements OnInit, OnDestroy {
  leaderBoard: ILeaderboard;
  private readonly subscriber: string = 'FiveASideLeaderBoardComponent';
  private componentId: string;
  private moduleName = rgyellow.FIVE_A_SIDE;

  constructor(private activatedRoute: ActivatedRoute,
    private leaderBoardService: FiveasideLeaderBoardService,
    private userService: UserService,
    private pubSub: PubSubService,
    private changeDetectorRef: ChangeDetectorRef,
    private navigationService: NavigationService,
    private coreToolsService: CoreToolsService,
    private bonusSuppression: BonusSuppressionService
  ) { }

  ngOnInit(): void {
    this.componentId = this.coreToolsService.uuid();
    this.subscribeToEventChange();
    this.getInitialLeaderboardData();
    this.loginTrigger();
  }

  ngOnDestroy(): void {
    this.pubSub.unsubscribe(this.subscriber);
  }

  /**
   * To Fetch Initial Leaderboard data
   * @returns {void}
   */
  private getInitialLeaderboardData(changeState? : string): void {
    const userName: string = this.userService.username;
    const bppToken: string = this.userService.bppToken;
    const contestId: string = this.activatedRoute.snapshot.params.id;
    this.leaderBoardService.getContestInformationById(contestId, userName, bppToken)
      .subscribe((response: IShowDownResponse) => {
        this.leaderBoard = response.contest;
        this.leaderBoardService.setLeaderBoardData(this.leaderBoard);
        this.optInUserIntoTheContest(response.contest);
        if(changeState){
          this.leaderBoard.type = changeState;
        }
        this.changeDetectorRef.markForCheck();
      }, (error) => {
        console.warn(error);
        this.navigationService.openRouterUrl(LEADERBOARD_WIDGET.LOBYY_URL, true);
      });
  }

  /**
    * Opt-in user to the contest
    * @returns void
    */
  private optInUserIntoTheContest(contest: IShowDown): void {
    if (contest) {
      this.leaderBoardService.optInUserIntoTheContest(contest);
    }
  }

  /**
   * To Subscribe to the changes done in Pre and Live leaderboard
   * @returns {void}
   */
  private subscribeToEventChange(): void {
    this.pubSub.subscribe(this.subscriber, PUBSUB_API.LEADERBOARD_EVENT_RESULTED, this.handleResultedEvent.bind(this));
    this.pubSub.subscribe(this.subscriber, PUBSUB_API.LEADERBOARD_EVENT_STARTED, this.handleLiveEvent.bind(this));
  }

  /**
   * To handle resulted event in Live Leaderboard
   * @returns {void}
   */
  private handleResultedEvent(): void {
    this.getInitialLeaderboardData(EVENTSTATUS.POST);
    this.changeDetectorRef.markForCheck();
  }

  /**
   * To Handle Live event in Pre Leader board
   * @returns {void}
   */
  private handleLiveEvent(): void {
    this.leaderBoard.type = EVENTSTATUS.LIVE;
    this.changeDetectorRef.markForCheck();
  }

  /**
   * Callback when login is successful
   * @returns {void}
   */
  private loginTrigger(): void {
    this.pubSub.subscribe(this.componentId, [this.pubSub.API.SUCCESSFUL_LOGIN, this.pubSub.API.SESSION_LOGIN], () => {
        if (!this.bonusSuppression.checkIfYellowFlagDisabled(this.moduleName)) {
          this.bonusSuppression.navigateAwayForRGYellowCustomer();
        }
    })
  }
}
