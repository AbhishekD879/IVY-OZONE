import { Component, Input } from '@angular/core';
import {
  OddsCardEnhancedMultiplesComponent as AppOddsCardEnhancedMultiplesComponent
} from '@shared/components/oddsCard/oddsCardEnhancedMultiples/odds-card-enhanced-multiples.component';

@Component({
  selector: 'odds-card-enhanced',
  templateUrl: 'odds-card-enhanced-multiples.component.html'
})

export class OddsCardEnhancedMultiplesComponent extends AppOddsCardEnhancedMultiplesComponent {
  @Input() limitSelections: boolean | number;
}
