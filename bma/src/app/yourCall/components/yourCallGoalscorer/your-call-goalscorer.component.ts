import { Component, OnInit, Input } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { IConditions } from '@root/app/lazy-modules/bybHistory/models/byb-selection.model';
import * as _ from 'underscore';
import { IYourcallSelection } from '../../models/selection.model';
import { IYourcallMarketSelectionsData } from '../../models/yourcall-api-response.model';
import { YourcallMarketsService } from '../../services/yourCallMarketsService/yourcall-markets.service';
import { GOALSCORER_GROUP } from '../yourCallMarketButtons/your-call-market-button-constant';
import { ChangeDetectorRef } from '@angular/core';
import { BybSelectedSelectionsService } from '@app/lazy-modules/bybHistory/services/bybSelectedSelections/byb-selected-selections';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { IFiveASidePlayer } from '../../services/fiveASide/five-a-side.model';

@Component({
  selector: 'your-call-goalscorer',
  templateUrl: './your-call-goalscorer.component.html'
})
export class YourCallGoalscorerComponent implements OnInit  {
  @Input() market;
  @Input() enabled;
  @Input() eventEntity: ISportEvent;
  @Input() marketsSet;
  @Input() player;
  @Input() loaded
  @Input() expand;

  goalscorerGroup = GOALSCORER_GROUP;
  selectedGS = []
  multi: boolean = false;
  marketSelected: any;
  selection: IYourcallSelection;
  showCardPlayersDup: IConditions = {};
  id: number;

  constructor(
    private yourCallMarketsService: YourcallMarketsService,
    public dialogService: DialogService,
    private infoDialogService: InfoDialogService,
    private localeService: LocaleService,
    private changeDetector: ChangeDetectorRef,
    private bybSelectedSelectionsService: BybSelectedSelectionsService,
    protected windowRefService: WindowRefService,

  ) { }

  /**
   * @returns void
   */
  ngOnInit(): void {
    this.changeDetector.detectChanges();
    this.expand = false;
    this.check(this.player, this.goalscorerGroup[0]);
    this.yourCallMarketsService.goalscorerSubject$.subscribe((value: any) => {
      if (this.yourCallMarketsService.selectedSelectionsSet.has(value.id)) {
        this.yourCallMarketsService.selectedSelectionsSet.delete(value.id);
      }
      this.showCardPlayersDup[value.name.indexOf('. ') >= 0 ? value.name.split('. ')[1].toUpperCase() : value.name.toUpperCase()] = this.yourCallMarketsService.selectedSelectionsSet.has(this.id) ? true : false;
    });
    this.bybSelectedSelectionsService.betPlacementSubject$.subscribe(selection => {
      if (selection) {
        this.showCardPlayersDup = {};
      }
    });
  }

  /**
   */
  callLocalStorageToFetchPlayerBets() {
    if (JSON.parse(this.windowRefService.nativeWindow.localStorage.getItem('OX.yourCallStoredData'))[this.eventEntity.id] != undefined) {
      const oldPlayer = JSON.parse(this.windowRefService.nativeWindow.localStorage.getItem('OX.yourCallStoredData'))[this.eventEntity.id].markets.BYB;
      const oldPlayerObj = (Object.keys(oldPlayer).toString()).split(',');
      oldPlayerObj.forEach(ele => {
        oldPlayer[ele].selections.forEach(element => {
          if (element.playerStatID) {
            this.yourCallMarketsService.selectedSelectionsSet.add(element.playerStatID);
          }
        });
      });
    }
  }

  /**
   * @param  {IFiveASidePlayer} player
   * @param  {any} team
   * @returns void
   */
  check(player: IFiveASidePlayer, team: any): void {
    this.changeDetector.detectChanges();
    if (!this.isteamSelectedGS(team)) {
      this.addGSSelection(team);
      this.selectedGSMarket(player, team);
    }
  }

  /**
   * @param  {any} team
   * @returns boolean
   */
  isteamSelectedGS(team: any): boolean {
    return _.indexOf(this.selectedGS, team) > -1;
  }

  /**
   * @param  {any} value
   * @returns void
   */
  addGSSelection(value: any): void {
    if (this.multi) {
      this.selectedGS.push(value);
    } else {
      this.selectedGS[0] = value;
    }
  }

  /**
   * @param  {any} player
   * @param  {any} team
   */
  selectedGSMarket(player: IFiveASidePlayer, team: any) {
    this.marketSelected = this.marketsSet.find(market => market.grouping === team.marketName);
    this.marketSelected.key = this.marketSelected.key.toUpperCase();
    const playerName = (player.name.indexOf('. ') >= 0 ? player.name.split('. ')[1].toUpperCase() : player.name.toUpperCase());
    this.yourCallMarketsService.loadMarketSelections({ obEventId: this.eventEntity.id, marketIds: team.id })
      .then((marketSelectionsData: IYourcallMarketSelectionsData[]) => {
        this.selection = marketSelectionsData[0].selections.find(x => (x.title.indexOf('. ') >= 0 ? x.title.split('. ')[1].toUpperCase() : x.title.toUpperCase()) === playerName);
        if (this.selection) {
          this.loaded = false;
          this.showCardPlayersDup[playerName] = this.yourCallMarketsService.selectedSelectionsSet.has(this.selection.id) ? true : false;
          this.id = this.selection.id;
        } else {
          this.enabled = undefined;
          this.playerAvailabe();
        }
      });
  }

  /**
   * @returns void
   */
  playerAvailabe(): void {
    this.enabled = undefined;
    this.infoDialogService.openInfoDialog(
      this.localeService.getString('yourCall.cantSelectPlayer.caption'),
      this.localeService.getString('yourCall.cantSelectPlayer.text'),
      '', undefined, () => {
      }, [{ caption: this.localeService.getString('yourCall.cantSelectPlayer.okBtn') }]
    );
  }

  /**
   * @param  {IFiveASidePlayer} player
   */
  done(player: IFiveASidePlayer) { // add and remove bet for show card and goalscorer
    this.selection.title = player.name;
    if (this.yourCallMarketsService.selectedSelectionsSet.has(this.selection.id)) {
      this.yourCallMarketsService.removeSelection(this.marketSelected, this.selection);
      this.yourCallMarketsService.selectedSelectionsSet.delete(this.selection.id);
      this.bybSelectedSelectionsService.callGTM('remove-selection', { deselect: true, selectionName: this.marketSelected.grouping + ' ' + this.selection.title });
    }
    else {
      this.yourCallMarketsService.selectValue(this.marketSelected, this.selection);
      this.yourCallMarketsService.selectedSelectionsSet.add(this.selection.id);
    }
    const playerName = player.name.indexOf('. ') >= 0 ? player.name.split('. ')[1].toUpperCase() : player.name.toUpperCase();
    this.showCardPlayersDup[playerName] = this.yourCallMarketsService.selectedSelectionsSet.has(this.selection.id) ? true : false;
  }

  /**
   * @param  {} playerName
   */
  getShowCardDup(playerName: string) {
    return this.showCardPlayersDup[playerName.indexOf('. ') >= 0 ? playerName.split('. ')[1].toUpperCase() : playerName.toUpperCase()];
  }
}
