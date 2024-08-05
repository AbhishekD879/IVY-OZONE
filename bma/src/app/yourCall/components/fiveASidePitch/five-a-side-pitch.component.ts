import { Component, Input, OnInit, Output, EventEmitter, OnDestroy } from '@angular/core';
import { iif, Subscription, throwError } from 'rxjs';
import { Router, ActivatedRoute } from '@angular/router';
import { map, switchMap } from 'rxjs/operators';

import { ISportEvent } from '@app/core/models/sport-event.model';
import { FiveASideService } from '@yourcall/services/fiveASide/five-a-side.service';
import { IFormation } from '@app/core/services/cms/models';
import { dialogIdentifierDictionary } from '@core/constants/dialog-identifier-dictionary.constant';
import { RoutingHelperService } from '@app/core/services/routingHelper/routing-helper.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { IMatrixFormation } from '../../models/five-a-side.model';
import { FiveASideBetService } from '@yourcall/services/fiveASideBet/five-a-side-bet.service';
import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { FiveASideRole } from '@yourcall/models/fiveASideRole/five-a-side-role.class';
import { GtmService } from '@core/services/gtm/gtm.service';
import { DeviceService } from '@core/services/device/device.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { StorageService } from '@core/services/storage/storage.service';
import { IFreebetToken } from '@bpp/services/bppProviders/bpp-providers.model';
import { IJourneyItems } from '@core/services/cms/models/five-a-side-journey.model';
import { JOURNEY_FREE_BET_SB_TITLE } from '@yourcall/constants/five-a-side.constant';
import { IFiveASidePlayers, ITeamsExist } from '@yourcall/services/fiveASide/five-a-side.model';
import { IPitchDetails, IPlayer } from '@yourcall/models/pitch-details';
import { FiveASideContestSelectionService } from '@app/fiveASideShowDown/services/fiveASide-ContestSelection.service';

@Component({
  selector: 'five-a-side-pitch',
  templateUrl: './five-a-side-pitch.component.html',
  styleUrls: ['./five-a-side-pitch.component.scss']
})

export class FiveASidePitchComponent implements OnInit, OnDestroy {
  @Input() eventEntity: ISportEvent;
  @Output() readonly hidePitchView: EventEmitter<boolean> = new EventEmitter();

  formations: IFormation[];
  isTabletOrDesktop: boolean = false;
  selectedFormation: IFormation;
  currentMatrixFormation: IMatrixFormation;
  showPitch: boolean = true;
  matrixFormation: IMatrixFormation[] = [];
  roleEmpty: Function;
  isRoleDisabled: Function;
  getRole: Function;
  addPlayerlabel: string = 'Add Player';
  oddsFormat: string;
  isBetReceipt: boolean = false;
  yourcallBetslipShown: boolean = false;
  slides: IJourneyItems[] = [];
  showJourney: boolean = false;
  availableFiveASideFreeBets: boolean = false;
  isJourneySeen: boolean = false;
  hasThreeInRow: boolean;
  hasThreeInRowIndex: number;

  private formationDataSubscription: Subscription;
  private playersSubscription: Subscription;
  private pitch: IPitchDetails;
  private readonly MAX_PLAYERS_ROW = '3';

  constructor(
    private fiveASideService: FiveASideService,
    private router: Router,
    private routingHelperService: RoutingHelperService,
    private infoDialogService: InfoDialogService,
    private localeService: LocaleService,
    private user: UserService,
    private pubSubService: PubSubService,
    private fiveASideBetService: FiveASideBetService,
    private gtmService: GtmService,
    private deviceService: DeviceService,
    private freeBetsService: FreeBetsService,
    private storageService: StorageService,
    private activatedRoute: ActivatedRoute,
    private fiveASideContestSelectionService: FiveASideContestSelectionService) {}

  /**
   * Check if teams image exist on both home and away
   * @returns { boolean }
   */
  get teamsImgExistOnHomeAway(): boolean {
    return Object.keys(this.fiveASideService.imagesExistOnHomeAway).length === 2
      && Object.values(this.fiveASideService.imagesExistOnHomeAway).every(
        (team: ITeamsExist) => team.fiveASideToggle && team.filename);
  }

  set teamsImgExistOnHomeAway(value: boolean) {}

  get disabledRolesMarked() {
    return this.fiveASideBetService.disabledRolesMarked;
  }
  set disabledRolesMarked(value:any){}
  get playersObject(): { [key: string]: FiveASideRole } {
    return this.fiveASideBetService.playersObject;
  }
  set playersObject(value:{ [key: string]: FiveASideRole }){}

  get errorMessage(): string {
    return this.fiveASideBetService.errorMessage;
  }
  set errorMessage(value:string){}
  get formattedPrice(): string {
    return this.fiveASideBetService.formattedPrice;
  }
  set formattedPrice(value:string){}

  get isValid(): boolean {
     return this.fiveASideBetService.isValid;
  }
  set isValid(value:boolean){}

  get activeView(): boolean {
    return !this.fiveASideService.activeView;
  }
  set activeView(value:boolean){}

  ngOnInit(): void {
    this.pitch = this.getPitchDetails();
    this.initPitch();
    this.isTabletOrDesktop = this.deviceService.isDesktop || this.deviceService.isTablet;
    this.oddsFormat = this.user.oddsFormat;
    this.pubSubService.publish('NETWORK_INDICATOR_BOTTOM_INDEX', true);
  }

  trackById(index, item: IFormation): string {
    return `${item.id}_${index}`;
  }

  /**
   * Set new formation
   * @param formation - chosen formation
   * @param clearBet - identifies whether need to clear bet
   */
  changeFormation(formation: IFormation, clearBet: boolean = true): void {
    clearBet && this.fiveASideBetService.clear();
    if (!this.selectedFormation || (this.selectedFormation && (this.selectedFormation.id !== formation.id))) {
      this.trackFormationChanges(formation);
    } else {
      return;
    }
    this.fiveASideService.activeFormation = this.selectedFormation.title;
    const actualFormation = formation.actualFormation.split('-');
    this.validateFormation(actualFormation);

    let rowIndex = -1;
    let index = 1;
    this.matrixFormation = [];
    let arrayIndex: number = 0;

    actualFormation.forEach((el: string) => {
      rowIndex = rowIndex + 1;
      switch (el) {
        case '0':
          break;
        case '1':
          this.addPosition(rowIndex, index, 1, arrayIndex++);
          index = index + 1;
          break;
        case '2':
          this.addPosition(rowIndex, index, 6, arrayIndex++);
          this.addPosition(rowIndex, index + 1, 7, arrayIndex++);
          index = index + 2;
          break;
        case '3':
          this.addPosition(rowIndex, index, 0, arrayIndex++);
          this.addPosition(rowIndex, index + 1, 1, arrayIndex++);
          this.addPosition(rowIndex, index + 2, 2, arrayIndex++);
          index = index + 3;
          break;
        default:
          break;
      }
    });
    this.fiveASideService.activeMatrixFormation = this.matrixFormation;
    this.fiveASideBetService.initialize(this.eventEntity);
    this.playersSubscription = this.fiveASideService
      .getPlayerList(this.eventEntity.id, this.eventEntity.sportId)
      .subscribe((players: IFiveASidePlayers) => {
        if (!clearBet) {
          this.fiveASideService.setPlayerDetails(this.pitch, players, this.eventEntity);
        }
      });
  }

  trackFormationChanges(formation: IFormation): void  {
    this.selectedFormation = formation;
    this.gtmService.push('trackEvent', {
      eventCategory: '5-A-Side',
      eventAction: 'Formation',
      eventLabel: this.selectedFormation.title
    });
  }

  trackByFn(index: number, formation: IFormation): string {
    return `${index}_${formation.id}`;
  }

  addPlayer(item: IMatrixFormation): void {
    this.fiveASideService.playerListScrollPosition = 0;
    if (this.fiveASideBetService.isRoleDisabled(item.roleId)) {
      return;
    }

    if (!this.fiveASideService.optaStatisticsAvailable) {
      this.fiveASideService.preapereOPTAInfo(this.fiveASideService.players, this.fiveASideService.eventId);
      this.fiveASideService.setPlayerDetails(this.pitch, this.fiveASideService.playerList, this.eventEntity);
    }

    const playersObject = this.playersObject[item.roleId];
    // Edit Player Mode
    if (playersObject) {
      const player = this.playersObject[item.roleId].player;
      this.fiveASideService.showView({ view: 'player-page', player, item }, true);
    } else {
      // Choose Player Mode
      this.currentMatrixFormation = item;
      this.fiveASideService.showView({ view: 'player-list', item });
    }
    this.gtmService.push('trackEvent', {
      eventCategory: '5-A-Side',
      eventAction: playersObject ? 'Edit Player' : 'Choose Player',
      eventLabel: item.position
    });
  }

  /**
   * Handler for Place Bet button click
   */
  ctaButtonClick(): void {
    if (!this.fiveASideBetService.isValid) {
      return;
    }
    if (!this.user.status) {
      this.pubSubService.publish('OPEN_LOGIN_DIALOG', { moduleName: 'header' });
      return;
    }
    if (this.isTabletOrDesktop) {
      this.yourcallBetslipShown = true;
    }
    this.fiveASideBetService.addToBetslip();
    this.gtmService.push('trackEvent', {
      event: 'trackEvent',
      eventCategory: 'quickbet',
      eventAction: 'add to quickbet',
      eventLabel: 'success',
        ecommerce: {
         add: {
          products: [{
           name: this.eventEntity.name,
           category: this.eventEntity.sportId,
           variant: this.eventEntity.typeId.toString(),
           brand: '5-A-Side',
           metric1: 0,
           dimension60: this.eventEntity.id.toString(),
           dimension62: 0,
           dimension63: 1,
           dimension64: 'EDP',
           dimension65: '5-A-Side',
           dimension86: 0,
           dimension87: 0,
           dimension89: this.selectedFormation ? this.selectedFormation.title : 0,
           quantity: 1
         }]
        }
      }
   });
  }

  hidePitch(): void {
    if (!this.isBetReceipt && this.matrixFormation
      && this.matrixFormation.some((item: IMatrixFormation) => !this.fiveASideBetService.roleEmpty(item.roleId))) {
      this.infoDialogService.openInfoDialog(
        this.localeService.getString('yourCall.fiveASide'),
        this.localeService.getString('yourCall.closePitchText'),
        null,
        dialogIdentifierDictionary.informationDialog,
        null,
        [
          {
            caption: this.localeService.getString('yourCall.leave'),
            cssClass: 'btn-style4',
            handler: this.closePitch.bind(this)
          }, {
            caption: this.localeService.getString('yourCall.stay'),
            cssClass: '',
            handler: () => {
              this.infoDialogService.closePopUp();
            }
          }
        ]
      );
    } else {
      this.closePitch();
    }
  }

  handleCloseQuickBet(): void {
    this.yourcallBetslipShown = false;
  }

  closePitch(): void {
    this.showPitch = false;
    this.hidePitchView.emit(this.showPitch);
    this.fiveASideContestSelectionService.defaultSelectedContest = '';
    this.fiveASideBetService.clear();
    const url: string = this.routingHelperService.formEdpUrl(this.eventEntity);
    this.router.navigate([`/${url}/5-a-side`]);
    this.storageService.set(`five-a-side-journey-seen`, true);
  }

  ngOnDestroy(): void {
    this.fiveASideBetService.clear();
    this.formationDataSubscription && this.formationDataSubscription.unsubscribe();
    this.playersSubscription && this.playersSubscription.unsubscribe();
    this.pubSubService.publish('NETWORK_INDICATOR_BOTTOM_INDEX', false);
  }

  /**
   * To fetch pitch details from route
   * @returns {IPitchDetails}
   */
  private getPitchDetails(): IPitchDetails {
    if (this.activatedRoute.snapshot.children[0]) {
      return {
        formation: this.activatedRoute.snapshot.children[0].paramMap.get('formation'),
        players: this.getPitchPlayers()
      };
    }
  }

  /**
   * To fetch players from route
   * @returns {IPlayer[]}
   */
  private getPitchPlayers(): IPlayer[] {
    const players: string[] = [];
    for (let i = 1;i <= 5; i++) {
      const banachPlayer = this.activatedRoute.snapshot.children[0].paramMap.get(`player${i}`);
      if (banachPlayer) {
        players.push(banachPlayer);
      }
    }
    return this.fiveASideService.buildPitchPlayers(players);
  }

  private initPitch(): void {
    this.formationDataSubscription = this.fiveASideService.getFormations().pipe(
      map((formations: IFormation[]) => {
        this.formations = formations;
        if (formations.length > 0) {
          const pitchFormation: string = this.pitch ? this.pitch.formation : null;
          const formation: IFormation = this.fiveASideService.getFormation(this.formations, pitchFormation);
          this.changeFormation(formation || formations[0], false);
        }
      }),
      switchMap(() =>
        iif(
          () => this.isJourneyAvailable(),
          this.fiveASideService.getJourneyStaticBlocks(),
          throwError(null)
        )
      )
    ).subscribe((data: IJourneyItems) => {
      this.slides = this.formJourney(data) ;
    });
  }

  private addPosition(rowIndex: number, index: number, collIndexes: number, roleId: number): void {
    this.matrixFormation.push({
      rowIndex,
      collIndex: collIndexes,
      position: this.selectedFormation[`position${index}`],
      stat: this.selectedFormation[`stat${index}`].title,
      statId: this.selectedFormation[`stat${index}`].id,
      roleId: `position${roleId + 1}`
    });
  }

  /**
   * To check if formation has 3 players in a row
   * @param formation {string[]}
   */
  private validateFormation(formation: string[]): void {
    this.hasThreeInRow = false;
    this.hasThreeInRow = formation.includes(this.MAX_PLAYERS_ROW);
    if (this.hasThreeInRow) {
      this.hasThreeInRowIndex = formation.indexOf(this.MAX_PLAYERS_ROW);
    }
  }

  /**
   * Checks users appearance on page and FreeBets
   */
  private isJourneyAvailable(): boolean {
    this.availableFiveASideFreeBets = this.isAvailableFiveASideFreeBets();
    this.isJourneySeen = this.storageService.get(`five-a-side-journey-seen`);
    this.showJourney = !this.isJourneySeen || this.availableFiveASideFreeBets;

    return this.showJourney;
  }

  /**
   * Checks 5-a-side bets availability
   */
  private isAvailableFiveASideFreeBets(): boolean {
    return this.freeBetsService.isFreeBetVisible(this.eventEntity) ||
      this.freeBetsService.getFreeBetsData().some((freeBet: IFreebetToken) => freeBet.tokenPossibleBet &&
        freeBet.tokenPossibleBet.betLevel === 'ANY');
  }

  /**
   * Forms journey slides
   * Depends on FreeBets and users appearance on page
   */
  private formJourney(staticBlocks: IJourneyItems): IJourneyItems[] {
    let SBNames: string[] = staticBlocks && Object.keys(staticBlocks);

    if (SBNames && SBNames.length) {
      let journeySlides = [];

      switch (true) {
        case this.availableFiveASideFreeBets && !this.isJourneySeen: // show all slides
          journeySlides = this.fillJourneySlides(SBNames, staticBlocks);
          break;
        case this.availableFiveASideFreeBets: // show FreeBet slides
          if(staticBlocks[JOURNEY_FREE_BET_SB_TITLE]) {
            journeySlides.push(staticBlocks[JOURNEY_FREE_BET_SB_TITLE]);
          }
          break;
        case !this.isJourneySeen: // show 5-a-side slides
          if(staticBlocks[JOURNEY_FREE_BET_SB_TITLE]) {
            SBNames = SBNames.filter((SBName: string) => SBName !== JOURNEY_FREE_BET_SB_TITLE);
          }
          journeySlides = this.fillJourneySlides(SBNames, staticBlocks);
          break;
      }

      return journeySlides;
    }

    return [];
  }

  /**
   * Forms journey slides array
   */
  private fillJourneySlides(SBNames, staticBlocks) {
    return SBNames.map((staticBlockName: string) => staticBlocks[staticBlockName]);
  }
}
