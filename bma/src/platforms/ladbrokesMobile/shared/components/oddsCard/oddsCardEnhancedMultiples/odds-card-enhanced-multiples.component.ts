import { Component, OnInit } from '@angular/core';
import {
  OddsCardEnhancedMultiplesComponent as AppOddsCardEnhancedMultiplesComponent
} from '@shared/components/oddsCard/oddsCardEnhancedMultiples/odds-card-enhanced-multiples.component';

@Component({
  selector: 'odds-card-enhanced',
  templateUrl: '../../../../../../app/shared/components/oddsCard/oddsCardEnhancedMultiples/odds-card-enhanced-multiples.component.html'
})

export class OddsCardEnhancedMultiplesComponent extends AppOddsCardEnhancedMultiplesComponent implements OnInit {
  ngOnInit(): void {
    super.ngOnInit();
    this.eventTime = this.eventTime.replace(',', '');
  }
}
