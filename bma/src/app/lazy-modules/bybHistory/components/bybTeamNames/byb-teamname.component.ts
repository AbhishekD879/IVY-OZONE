import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { YourCallMarketGroup } from '@app/yourCall/models/markets/yourcall-market-group';
import { YourCallMarketGroupItem } from '@app/yourCall/models/markets/yourcall-market-group-item';
import { ISwitcher } from '@app/lazy-modules/bybHistory/components/bybLayout/byb-markets-mock';
import environment from '@environment/oxygenEnvConfig';
@Component({
  selector: 'byb-teamname-component',
  templateUrl: 'byb-teamname.component.html',
  styleUrls: ['./byb-teamname.component.scss'],
})

export class BybTeamNameComponent implements OnInit {
  @Output() readonly collapseLists = new EventEmitter();
  @Input() teamA: string;
  @Input() teamB: string;
  @Input() marketGroupArr: YourCallMarketGroup[] | YourCallMarketGroupItem[];
  @Input() marketGroupName: string;
  selectedGroupMarket: YourCallMarketGroup | YourCallMarketGroupItem;
  selectedGroup: number = 0;
  switchers: ISwitcher[] = [];
  isCoral:boolean;
  constructor() {
  }

  /**
   * to populate initial data
   * @returns {void}
   */
  ngOnInit(): void {
    this.isCoral = environment && environment.brand === 'bma';
    this.selectedGroup = 0;
    this.selectedGroupMarket = this.marketGroupArr[0];
    this.populateMarketGroupNames();
  }

  /**
   * to populate switchers
   * @returns {void}
   */
  populateMarketGroupNames(): void {
    this.marketGroupArr?.length && this.marketGroupArr.forEach((marketGroup, index) => {
      this.switchers.push({ name: this.parseTitle(index) || marketGroup.key });
    });
  }

  /**
   * to replace default name with assigned names
   * @param {number} index
   * @returns {string}
   */
  parseTitle(index: number): string {
    let name = '';
    if (this.marketGroupArr && this.marketGroupArr[0].game  && this.marketGroupArr[0].game.homeTeam && this.marketGroupArr[0].game.visitingTeam) {
        if(this.marketGroupArr[index].key.search('Home') != -1) {
          name = this.marketGroupArr[0].game.homeTeam.title;
        } else if (this.marketGroupArr[index].key.search('Away') != -1) {
          name = this.marketGroupArr[0].game.visitingTeam.title;
        } else if(this.marketGroupArr[index].key.search('Total Goals') != -1 || this.marketGroupArr[index].key.search('Total Corners') != -1 ||
        this.marketGroupArr[index].key.search('Match Booking Points') != -1){
         name = 'Both Teams';
       }
        return name?.replace(/(\w)(\w*)/g,
        (g0,g1,g2) => {return g1.toUpperCase() + g2.toLowerCase();});
    }
  }

  /**
   * Track by function
   * @param {number} index
   * @returns {string}
   */
     trackByFn(index: number): number {
      return index;
    }

  /**
   * Track by function
   * @param {number} index
   * @returns {string}
   */
    trackBySwitchers(index: number): number {
      return index;
    }

  /**
   * Select team to display
   * @param {number} index
   * @returns {boolean}
   */
  selectGroup(index: number): boolean {
    if(index === this.selectedGroup) {
      return false;
    }
    this.selectedGroup = index;
    this.selectedGroupMarket = this.marketGroupArr[index];
    return true;
  }

    /**
   * Check if group is selected
   * @param index
   * @returns {boolean}
   */
     isActiveGroup(index: number): boolean {
      return this.selectedGroup === index;
    }

    get displaySwitchers(): boolean {
      if(this.switchers.length == 0) {
        this.populateMarketGroupNames();
        this.selectedGroupMarket = this.marketGroupArr[0];
      }
      return this.marketGroupArr.length > 0;
    }
    set displaySwitchers(value:boolean){}
}
