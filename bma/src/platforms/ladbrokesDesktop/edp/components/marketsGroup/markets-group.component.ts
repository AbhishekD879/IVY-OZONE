import { Component } from '@angular/core';

import { MarketsGroupComponent as BaseMarketsGroupComponent } from '@edp/components/marketsGroup/markets-group.component';

@Component({
  selector: 'markets-group-component',
  templateUrl: '../../../../../app/edp/components/marketsGroup/markets-group.component.html',
  styleUrls: ['./markets-group.component.scss']
})

export class MarketsGroupComponent extends BaseMarketsGroupComponent {}
