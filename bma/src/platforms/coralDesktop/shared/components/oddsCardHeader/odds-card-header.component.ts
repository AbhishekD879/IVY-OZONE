import { Component, ViewEncapsulation } from '@angular/core';
import { OddsCardHeaderComponent as AppOddsCardHeaderComponent } from '@shared/components/oddsCardHeader/odds-card-header.component';

@Component({
  selector: 'odds-card-header',
  templateUrl: 'odds-card-header.component.html',
  styleUrls: ['odds-card-header.component.scss'],
  encapsulation : ViewEncapsulation.None
})

export class OddsCardHeaderComponent extends AppOddsCardHeaderComponent {}
