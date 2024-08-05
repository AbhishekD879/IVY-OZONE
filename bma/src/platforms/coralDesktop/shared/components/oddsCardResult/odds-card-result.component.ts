import { Component } from '@angular/core';

import {
  OddsCardResultComponent as AppOddsCardResultComponent
} from '@shared/components/oddsCardResult/odds-card-result.component';

@Component({
  selector: 'odds-card-result-component',
  templateUrl: 'odds-card-result.component.html',
  styleUrls: ['./odds-card-result.component.scss']
})

export class OddsCardResultComponent extends AppOddsCardResultComponent {}
