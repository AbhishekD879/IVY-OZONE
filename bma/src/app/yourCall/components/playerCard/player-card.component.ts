import { Component, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';

import { IFiveASidePlayer, ITeamsExist } from '@yourcall/services/fiveASide/five-a-side.model';
import { MARKETS, STATS_TITLES } from '@yourcall/constants/five-a-side.constant';
import { IMatrixFormation } from '@yourcall/models/five-a-side.model';
import { FiveASideService } from '@yourcall/services/fiveASide/five-a-side.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IYourcallStatisticItem } from '@yourcall/models/yourcall-api-response.model';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'player-card',
  templateUrl: './player-card.component.html',
  styleUrls: ['./player-card.component.scss']
})
export class PlayerCardComponent implements OnInit, OnChanges {
  @Input() player: IFiveASidePlayer;
  @Input() eventEntity: ISportEvent;
  @Input() playerFormation: IMatrixFormation;
  readonly TEAMSIMAGEPATH: string = environment.CMS_ROOT_URI + environment.FIVEASIDE.svgImagePath;
  markets = MARKETS;
  statsTitles = STATS_TITLES;
  primaryColour: string;
  secondaryColour: string;
  statValue: number | string;
  unavailable: boolean;
  teamsImage: string;
  fiveASideToggle: boolean;

  private value: number;

  constructor(
    private fiveASideService: FiveASideService,
    private infoDialogService: InfoDialogService,
    private localeService: LocaleService,
    private windowRefService: WindowRefService
  ) {}

  /**
   * Check if teams image exist on both home and away
   * @returns { boolean }
   */
  get teamsImgExistOnHomeAway(): boolean {
    return Object.keys(this.fiveASideService.imagesExistOnHomeAway).length === 2
      && Object.values(this.fiveASideService.imagesExistOnHomeAway).every(
        (team: ITeamsExist) => team.fiveASideToggle && team.filename);
  }

  set teamsImgExistOnHomeAway(value:boolean) {}

  ngOnInit(): void {
    this.playerFormation = this.fiveASideService.activeItem;
    this.primaryColour = this.player.teamColors.primaryColour;
    this.secondaryColour = this.player.teamColors.secondaryColour;
    this.teamsImage = this.player.teamColors.teamsImage && this.player.teamColors.teamsImage.filename ?
    `${this.TEAMSIMAGEPATH}${this.player.teamColors.teamsImage.filename}`: '';
    this.fiveASideToggle = this.player.teamColors.fiveASideToggle;
    this.setPlayerCard();
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.playerFormation) {
      this.setPlayerCard();
    }
  }

  showPlayerPage(): void {
    const { player, playerFormation } = this;
    const drawerBody: HTMLElement = this.windowRefService.document.querySelector('five-a-side-player-list .drawer-body');
    this.fiveASideService.playerListScrollPosition = drawerBody.scrollTop;
    this.fiveASideService.loadPlayerStats(this.eventEntity.id, player.id).subscribe((stats: IYourcallStatisticItem[]) => {
      if (stats.find((stat: IYourcallStatisticItem) => stat.id === playerFormation.statId)) {
        this.fiveASideService.showView({ view: 'player-page', player, item: playerFormation });
        return;
      }

      this.infoDialogService.openInfoDialog(
        this.localeService.getString('yourCall.cantSelectPlayer.caption'),
        this.localeService.getString('yourCall.cantSelectPlayer.text'),
        '', undefined, () => {
          this.unavailable = true;
        }, [{ caption: this.localeService.getString('yourCall.cantSelectPlayer.okBtn') }]
      );
    }, () => {
      this.infoDialogService.openInfoDialog(
        this.localeService.getString('yourCall.error'),
        this.localeService.getString('yourCall.serverError')
      );
    });
  }

  private setUnavailable(): void {
    const stats = this.fiveASideService.getPlayerStats(this.eventEntity.id, this.player.id);
    this.unavailable = stats && !stats.find((stat: IYourcallStatisticItem) => stat.id === this.playerFormation.statId);
  }

  /**
   * To Set player card properties
   */
  private setPlayerCard(): void {
    this.value = this.player[this.markets[this.playerFormation.stat]];
    this.statValue = (this.value === undefined || this.value === null) ? 'N/A' : this.value;
    this.setUnavailable();
  }
}
