import { Component, Input, OnInit } from '@angular/core';

import { TopBarComponent as AppTopBarComponent } from '@shared/components/topBar/top-bar.component';

import * as _ from 'underscore';

@Component({
  selector: 'top-bar',
  templateUrl: 'top-bar.component.html',
  styleUrls: ['top-bar.component.scss']
})
export class TopBarComponent extends AppTopBarComponent implements OnInit {

  isFavourites: boolean;

  @Input() event: any;
  @Input() sportName: string;
  @Input() isSpecial: boolean;

  ngOnInit(): void {
    super.ngOnInit();
    this.isFavourites = this.isFavouritesVisible();
  }

  /**
   * Checks if event's market has "SP" flag in "drilldownTagNames".
   * @return {boolean}
   * @private
   */
  hasMarketSPFlag(): boolean {
    const SP_FLAG = 'MKTFLAG_SP';
    let drilldownTagNames;

    if (this.event && this.event.markets) {
      const market = _.isArray(this.event.markets) && this.event.markets[0];
      drilldownTagNames = market && market.drilldownTagNames;
    }
    return _.isString(drilldownTagNames) && drilldownTagNames.indexOf(SP_FLAG) > -1;
  }

  /**
   * Checks if favourites icon should be visible.
   * @return {Boolean} [description]
   */
  isFavouritesVisible(): boolean {
    const isFootball = this.sportName === 'football';
    return isFootball && !this.isSpecial && !this.hasMarketSPFlag();
  }
}
