import { Component, OnInit } from '@angular/core';
import { ILink } from '@app/client/private/models/specialPages.model';
import { EuroLoyaltyConstants } from '@app/special-pages/euro-loyalty/euro-loyalty-dashboard/euroLoyalty.constant';

@Component({
  selector: 'special-pages',
  templateUrl: './special-pages.component.html'
})
export class SpecialPagesComponent implements OnInit {

  private readonly EUROLOYAL = EuroLoyaltyConstants;

  public links: ILink[];

  constructor() {
    this.links = [{
      label: this.EUROLOYAL.labels.MatchDayRewards,
      path: './matchDayRewards'
    }];
  }

  ngOnInit() {
  }

}
