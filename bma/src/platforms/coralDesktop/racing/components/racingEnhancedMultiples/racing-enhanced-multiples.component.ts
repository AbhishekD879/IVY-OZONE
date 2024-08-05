import { Component,Input } from '@angular/core';
import { RacingEnhancedMultiplesComponent as AppRacingEnhancedMultiplesComponent
} from '@racing/components/racingEnhancedMultiples/racing-enhanced-multiples.component';

@Component({
  selector: 'racing-enhanced-multiples',
  templateUrl: '../../../desktop/components/enchancedMultiplesCarousel/enhancedMultiplesCarousel.component.html',
  styleUrls: ['../../../desktop/components/enchancedMultiplesCarousel/enhancedMultiplesCarousel.component.scss'],
})

export class RacingEnhancedMultiplesComponent extends AppRacingEnhancedMultiplesComponent {
  //added below property for strict mode issue
  @Input() public isHomePage?: boolean;
}
