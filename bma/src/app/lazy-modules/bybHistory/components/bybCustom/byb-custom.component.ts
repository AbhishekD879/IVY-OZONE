import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { YourcallDashboardService } from '@app/yourCall/services/yourcallDashboard/yourcall-dashboard.service';
import { YourcallMarketsService } from '@app/yourCall/services/yourCallMarketsService/yourcall-markets.service';
import { BybSelectedSelectionsService } from '@app/lazy-modules/bybHistory/services/bybSelectedSelections/byb-selected-selections';
import { Added, AddTo, ICustomMarketType } from '@app/lazy-modules/bybHistory/components/bybLayout/byb-markets-mock';
import { YourCallMarketGroup } from '@app/yourCall/models/markets/yourcall-market-group';
import { IYourcallMarketSelectionsData } from '@app/yourCall/models/yourcall-api-response.model';
import { IYourcallSelection } from '@app/yourCall/models/selection.model';
import { YourCallMarketGroupItem } from '@app/yourCall/models/markets/yourcall-market-group-item';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'byb-custom-component',
  templateUrl: 'byb-custom.component.html',
  styleUrls: ['./byb-custom.component.scss'],
})

export class BybCustomComponent implements OnInit, OnChanges {
  @Input() teamA: string;
  @Input() teamB: string;
  @Input() marketGroupArr: ICustomMarketType[];
  @Input() parentSelectionInput:{ name: string , teamType : number } = {name: '' ,teamType: -1};
  @Input() groupName: string;
  @Input() key: string;
  @Input() isInitial :boolean;
  parentSelection: { name: string , teamType : number }  = {name: '' ,teamType: -1};
  selectedGroup: any = 0;
  selectedGroupMarket: any;
  customMarket: any;
  switchers: { name: string }[] = [];
  enableBetBuilder = false;
  currentSelection;
  currentIndex : number;
  isLoaded: boolean;
  addToSlipText: string;
  isCoral:boolean;
  constructor(private yourCallMarketsService: YourcallMarketsService,
    private yourcallDashboardService: YourcallDashboardService,
    private bybSelectedSelectionsService: BybSelectedSelectionsService) {
  }

  /**
   * to change on input selection change
   * @param {SimpleChanges} changes
   * @returns {void}
   */
  ngOnChanges(changes: SimpleChanges): void {
    if (!changes.key.firstChange) {
      this.switchers = [];
      this.selectedGroup = this.isInitial ? 0 : -1;
      this.currentSelection= null;
      this.populateMarketGroupNames();
      this.addToSlipText = AddTo;
    }
  }

  /**
   * to init logic
   * @returns {void}
   */
   ngOnInit(): void {
    this.isCoral = environment && environment.brand === 'bma';
    this.selectedGroup = this.isInitial ? 0 : -1;
    this.addToSlipText = AddTo;
    this.yourcallDashboardService.removeId$.subscribe(selection => {
      if (selection) {
          this.yourCallMarketsService.selectedSelectionsSet.delete(selection);
      }
    });
    if(this.isInitial) {
      this.populateMarketGroupNames();
      this.selectedGroup = 0;
      this.selectedGroupMarket = this.marketGroupArr[0];
      this.parentSelection.name = this.switchers[0].name;
      this.parentSelection.teamType = 1;
    } else {
      this.bybSelectedSelectionsService.betPlacementSubject$.subscribe(selection => {
        if (selection) {
          this.reset();
        }
      });
    }
  }


  /**
   * to change selection when some selection is clicked
   * @param {number} index
   * @returns {boolean}
   */
  selectGroup(index: number): boolean {
    this.isLoaded = false;
    if(!this.isInitial && (index === this.selectedGroup)) {
      this.reset();
      return false;
    }
    this.selectedGroup = index;
    this.selectedGroupMarket = this.marketGroupArr[index];
    this.parentSelection.name = this.switchers[index].name;
    this.fillparentSelectionMarketType(index);
    if(this.marketGroupArr[index].isGroup) {
      this.key = this.marketGroupArr[index].key;
    }
    if(!this.selectedGroupMarket.isGroup) {
      this.loadMarket(this.selectedGroupMarket[this.selectedGroupMarket.key]);
      this.enableBetBuilder = true;
    }
    this.addToSlipText = this.yourCallMarketsService.selectedSelectionsSet.has(this.currentSelection?.id)? Added: AddTo;
    return true;
  }

  /**
   * to fill teamType based on the team selected instead of using name since name is not persistent
   * @param {number} index
   * @returns {void}
   */
  fillparentSelectionMarketType(index: number): void {
    if(this.groupName && this.groupName.toUpperCase() !== 'MATCH BETTING' && index > 0) {
      this.parentSelection.teamType = index;
    } else if(this.groupName && this.groupName.toUpperCase() === 'MATCH BETTING') {
      switch (index) {
        case 0:
          this.parentSelection.teamType = 1;
          break;
        case 1:
          this.parentSelection.teamType = 0;
          break;
        case 2:
          this.parentSelection.teamType = 2;
          break;
      }
    }
  }

  /**
   * to enable switchers with active selection
   * @param {number} index
   * @returns {boolean}
   */
  isActiveGroup(index: number): boolean {
    return this.selectedGroup === index;
  }

  /**
   * to populate group names on inital load
   * @returns {void}
   */
  populateMarketGroupNames(): void {
    if(!this.marketGroupArr)
      return;
    this.marketGroupArr.length && this.marketGroupArr.forEach((marketGroup) => {
      this.switchers.push({ name: this.parseName(marketGroup.key)});
    });
  }

  /**
   * to change the name of selection according to reqments
   * @param {string} unFormattedName
   * @returns {string}
   */
  parseName(unFormattedName :string): string {
    if(!unFormattedName)
      return unFormattedName;
    unFormattedName = unFormattedName.toUpperCase();
    if(unFormattedName == 'HOME') {
      return this.teamA;
    } else if(unFormattedName == 'AWAY') {
      return this.teamB;
    }
    return unFormattedName;
  }

  /**
   * to initiate switchers arr
   * @returns {boolean}
   */
  get displaySwitchers(): boolean {
    if(!this.marketGroupArr)
      return false;
    if(this.switchers.length == 0) {
      this.populateMarketGroupNames();
      this.selectedGroupMarket =this.marketGroupArr[0].val;
    }
    return this.marketGroupArr.length > 0;
  }
  set displaySwitchers(value:boolean){}

  /**
   * make call to fetch data
   * @param {YourCallMarketGroup} marketName
   * @returns {void}
   */
  loadMarket(marketName: YourCallMarketGroup): void {
    this.yourCallMarketsService.markets.forEach((market, index) => {
        if (market.key === marketName) {
          this.currentIndex = index;

        this.yourCallMarketsService.loadSelectionData(market).then((marketRespData: IYourcallMarketSelectionsData[]) => {
          this.isLoaded = true;
          if(!marketRespData || !marketRespData.length || !marketRespData[0].selections.length) {
            return;
          }
          marketRespData[0].selections.forEach((marketSelection: IYourcallSelection) => {
            if(this.parentSelectionInput.teamType === marketSelection.relatedTeamType) {
              this.currentSelection = marketSelection;
            }
            if (marketSelection.title == this.parseName(this.parentSelectionInput.name) || marketSelection.title.toUpperCase() === 'YES') {
              this.currentSelection = marketSelection;
            }
              this.addToSlipText = this.yourCallMarketsService.selectedSelectionsSet.has(this.currentSelection?.id)? Added: AddTo;
          });
        });
      }
    });
  }

  /**
   * when add to bb is clicked
   * @returns {void}
   */
  selectedValue(): void {
    if(this.selectedGroup === -1)
      return;
    if(this.groupName === 'Match Betting') {
        this.addMarketBettingSelections();
    }
    if(this.currentIndex === undefined || this.currentSelection === undefined) {
      return;
    }
    this.isSelected(this.yourCallMarketsService.markets[this.currentIndex],this.currentSelection);
    this.yourCallMarketsService.selectValue(this.yourCallMarketsService.markets[this.currentIndex], this.currentSelection);
    this.updateSelectionSet();
  }

  /**
   * update selectionSet on every addition and removal
   * @returns {void}
   */
  updateSelectionSet(): void {
    this.yourCallMarketsService.selectedSelectionsSet = new Set();
    this.yourcallDashboardService.items.forEach(combinationSelection => {
      if(combinationSelection.selection && combinationSelection.selection.id)
        this.yourCallMarketsService.selectedSelectionsSet.add(combinationSelection.selection.id);
    });
  }

  /**
   * to check if the selection is already there
   * @returns {void}
   */
  isSelected(market: YourCallMarketGroupItem | YourCallMarketGroup,selection : IYourcallSelection): boolean {
    const isMarketSelected = this.yourCallMarketsService.isSelected(market, selection);
    return isMarketSelected;
  }

  /**
   * to check for marketbetting selections are added properly
   * @returns {void}
   */
  addMarketBettingSelections(): void {
      if(this.key == 'HOME') {
        this.yourCallMarketsService.markets[this.currentIndex].selections.forEach(selection => {
          if(selection.relatedTeamType == 1) {
            this.currentSelection = selection;
          }
        });
      } else if(this.key == 'AWAY') {
        this.yourCallMarketsService.markets[this.currentIndex].selections.forEach(selection => {
          if(selection.relatedTeamType == 2) {
            this.currentSelection = selection;
          }
        });
      } else {
        this.yourCallMarketsService.markets[this.currentIndex].selections.forEach(selection => {
          if(selection.relatedTeamType == 0) {
            this.currentSelection = selection;
          }
        });
      }
  }

  reset() {
    if(this.isInitial)
      return;
    this.selectedGroup = -1;
  }

  checkCurrentStatus() {
    if(this.yourCallMarketsService.removeAllMarkets) {
      this.yourCallMarketsService.selectedSelectionsSet = new Set();
      this.selectedGroup = -1;
      this.yourCallMarketsService.removeAllMarkets = false;
    }
    if (this.yourCallMarketsService.lastRemovedMarket && this.yourCallMarketsService.lastRemovedMarket === this.currentSelection?.id) {
      this.selectedGroup = -1;
      this.yourCallMarketsService.lastRemovedMarket = -1;
    }
    this.addToSlipText = this.yourCallMarketsService.selectedSelectionsSet.has(this.currentSelection?.id)? Added: AddTo;
    return true;
  }
}
