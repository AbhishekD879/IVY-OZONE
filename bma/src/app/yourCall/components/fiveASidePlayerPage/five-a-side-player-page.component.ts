import { Component, EventEmitter, Input, OnDestroy, OnInit, Output, ChangeDetectorRef } from '@angular/core';
import { Subject, Subscription } from 'rxjs';
import { debounceTime } from 'rxjs/operators';

import { IFiveASidePlayer } from '@yourcall/services/fiveASide/five-a-side.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMatrixFormation } from '@yourcall/models/five-a-side.model';
import { IYourcallStatisticItem } from '@yourcall/models/yourcall-api-response.model';

import { YourcallMarketsService } from '../../services/yourCallMarketsService/yourcall-markets.service';
import { FiveASideBetService } from '@yourcall/services/fiveASideBet/five-a-side-bet.service';
import { FiveASideRole } from '@yourcall/models/fiveASideRole/five-a-side-role.class';
import { MARKETS, NO_BUTTONS_MARKETS } from '../../constants/five-a-side.constant';
import { IConstant } from '@app/core/services/models/constant.model';
import { FiveASideService } from '@yourcall/services/fiveASide/five-a-side.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { dialogIdentifierDictionary } from '@core/constants/dialog-identifier-dictionary.constant';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { UserService } from '@core/services/user/user.service';

@Component({
  selector: 'five-a-side-player-page',
  templateUrl: './five-a-side-player-page.component.html',
  styleUrls: ['./five-a-side-player-page.component.scss']
})
export class FiveASidePlayerPageComponent implements OnInit, OnDestroy {
  @Input() eventEntity: ISportEvent;

  @Output() readonly hideView: EventEmitter<any> = new EventEmitter();

  item: IMatrixFormation;
  player: IFiveASidePlayer;
  animationDelay: number = 5000;
  value: number = 0;
  subtitle: string;
  subtitleEnding: string;
  gradient: string;
  buttonsModel: {
    minValue: number;
    maxValue: number;
    average: number;
  };
  role: FiveASideRole;
  isNoButtonsMarket: boolean;
  betButtonTitle: string;
  playerStatMap: {
    statLabel: string,
    statValue: number | string
  }[];
  oddsFormat: string;
  optaStatisticsAvailable: boolean;

  readonly marketsMap: IConstant = MARKETS;
  private readonly noButtonsMarkets: IConstant = NO_BUTTONS_MARKETS;
  private readonly DEBOUNCE_TIME: number = 250;
  private clicks: Subject<number>;
  private subscription: Subscription;

  constructor(private yourCallMarketsService: YourcallMarketsService,
              public fiveASideBet: FiveASideBetService,
              public fiveASideService: FiveASideService,
              private infoDialogService: InfoDialogService,
              private localeService: LocaleService,
              private gtmService: GtmService,
              private changeDetectorRef: ChangeDetectorRef,
              private user: UserService) {}

  ngOnInit() {
    this.optaStatisticsAvailable = this.fiveASideService.optaStatisticsAvailable;
    this.fiveASideBet.backupPlayers();
    this.item = this.fiveASideService.activeItem;
    this.player = this.fiveASideService.activePlayer;
    this.createPlayerStatMap();
    this.updateButtonsMarketsState(this.item.stat);
    this.addRole(true);
    if (this.player.teamColors) {
      // eslint-disable-next-line max-len
      this.gradient = `linear-gradient(180deg, ${this.player.teamColors.primaryColour} 25%, ${this.hex2rgba(this.player.teamColors.primaryColour)} 60%), url(/assets/shield.svg)`;
    }

    this.betButtonTitle = this.fiveASideService.isEditMode ? 'updatePlayer' : 'addPlayer';
  }

  changeValue(type: string): void {
    if (this.buttonsModel) {
      const step = this.item.stat === 'Passes' ? 5 : 1;
      if (type === 'Plus' && this.value < this.buttonsModel.maxValue) {
        this.value += step;
      } else if (this.value > this.buttonsModel.minValue) {
        this.value -= step;
      }
      this.clicks.next(this.value);
    }
  }

  addDebounceListener(): void {
    if (!this.clicks) {
      this.clicks = new Subject();
    }

    this.subscription && this.subscription.unsubscribe();

    this.subscription = this.clicks
      .pipe(debounceTime(this.DEBOUNCE_TIME))
      .subscribe((value: number) => this.role.changeStatValue(value));
  }

  addPlayer(): void {
    const formationIndex: number = this.fiveASideService.activeMatrixFormation.findIndex((formation: IMatrixFormation) => {
      return formation.roleId === this.item.roleId;
    });
    if (formationIndex !== -1) {
      this.fiveASideService.activeMatrixFormation[formationIndex] = this.item;
    }
    this.fiveASideService.applyStatEdit(this.item);
    this.fiveASideBet.resetEditState();
    this.fiveASideService.hideView();
    this.fiveASideService.playerListScrollPosition = 0;
  }

  backHandler(): void {
    if (this.fiveASideService.isEditMode) {
      this.fiveASideBet.restorePlayers();
      this.fiveASideBet.updateBet();
      this.fiveASideService.hideView();
    } else {
      this.fiveASideBet.resetEditState();
      this.fiveASideBet.clearRole(this.item.roleId);
      this.fiveASideService.showView({ view: 'player-list' });
    }
  }

  changeStat(newStat: IYourcallStatisticItem): void {
    this.fiveASideService.saveDefaultStat();

    this.item = {
      ...this.item, stat: newStat.title, statId: newStat.id
    };

    this.updateButtonsMarketsState(this.item.stat);
    this.trackChangeStat(this.item);
    this.addRole();
  }

  ngOnDestroy(): void {
    this.subscription && this.subscription.unsubscribe();
    this.fiveASideBet.clearPlayersBackup();
  }

  removeSelection(): void {
    this.infoDialogService.openInfoDialog(
      this.localeService.getString('yourCall.removePlr'),
      this.localeService.getString('yourCall.removeDesc'),
      null,
      dialogIdentifierDictionary.fiveASideRemoveSelDialog,
      null,
      [
        {
          caption: this.localeService.getString('yourCall.cancel'),
          handler: () => this.infoDialogService.closePopUp(),
          cssClass: 'btn-style4'
        }, {
          caption: this.localeService.getString('yourCall.remove'),
          handler: () => this.removePlayer()
        }
      ]
    );
  }

  private updateButtonsMarketsState(stat: string): void {
    this.isNoButtonsMarket = this.noButtonsMarkets.includes(stat);
  }

  private removePlayer(): void {
    this.gtmService.push('trackEvent', {
      eventCategory: '5-A-Side',
      eventAction: 'Delete Player',
      eventLabel: this.item.position
    });
    this.fiveASideService.restoreDefaultStat();
    this.fiveASideBet.resetEditState();
    this.fiveASideBet.clearRole(this.item.roleId);
    this.infoDialogService.closePopUp();
    this.fiveASideService.hideView();
  }

  private addRole(isInit?: boolean): void {
    const playerId = this.player.id;
    const statId = this.item.statId;
    const obEventId = this.eventEntity.id.toString();
    const playerObject = this.fiveASideBet.playersObject[this.item.roleId];
    this.subtitleEnding = !this.isNoButtonsMarket ? (this.item.stat === 'To Concede' ? 'Goals' : this.item.stat) : '';
    this.oddsFormat = this.user.oddsFormat;
    this.yourCallMarketsService
      .getStatValues({ obEventId, playerId, statId })
      .then((response) => {
        if (!response || !response.data) {
          return;
        }
        let average = response.data.average;
        if (this.fiveASideService.isEditMode && isInit && playerObject) {
          average = playerObject.statValue;
        }
        this.buttonsModel = {
          minValue: response.data.minValue,
          maxValue: response.data.maxValue,
          average
        };
        this.role = this.fiveASideBet.addRole(this.player, this.item, average);
        this.fiveASideBet.setEditState();
        this.value = average;
        this.changeDetectorRef.detectChanges();
      });
    this.addDebounceListener();
  }

  private trackChangeStat(item: IMatrixFormation): void {
    this.gtmService.push('trackEvent', {
      eventCategory: '5-A-Side',
      eventAction: 'Edit Market',
      eventLabel: item.stat
    });
  }

  private createPlayerStatMap(): void {
    if (this.player.isGK) {
      this.playerStatMap = [{ statLabel: 'appearances', statValue: this.player.appearances },
        { statLabel: 'conceeded', statValue: this.player.conceeded },
        { statLabel: 'cleanSheets', statValue: this.player.cleanSheets },
        { statLabel: 'saves', statValue: this.player.saves },
        { statLabel: 'penaltySaves', statValue: this.player.penaltySaves }];
    } else {
      this.playerStatMap = [{ statLabel: 'appearances', statValue: this.player.appearances },
        { statLabel: 'goals', statValue: this.player.goals },
        { statLabel: 'assists', statValue: this.player.assists },
        { statLabel: 'shots', statValue: this.player.shots },
        { statLabel: 'passes', statValue: this.player.passes }];
    }
  }

  private hex2rgba(hex: string): string {
    const [r, g, b] = hex.match(/\w\w/g).map(x => parseInt(x, 16));
    return `rgba(${r},${g},${b},0.90)`;
  }
}
