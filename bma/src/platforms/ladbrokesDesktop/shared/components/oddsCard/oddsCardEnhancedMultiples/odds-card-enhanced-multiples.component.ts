import { Component, Input } from '@angular/core';
import {
  OddsCardEnhancedMultiplesComponent as LMOddsCardEnhancedMultiplesComponent
} from '@ladbrokesMobile/shared/components/oddsCard/oddsCardEnhancedMultiples/odds-card-enhanced-multiples.component';

@Component({
  selector: 'odds-card-enhanced',
  templateUrl: 'odds-card-enhanced-multiples.component.html'
})

export class DesktopOddsCardEnhancedMultiplesComponent extends LMOddsCardEnhancedMultiplesComponent {
  @Input() limitSelections: boolean | number | any;
}
