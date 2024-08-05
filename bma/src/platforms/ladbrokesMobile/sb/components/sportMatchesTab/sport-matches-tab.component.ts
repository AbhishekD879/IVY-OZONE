import {
  Component
} from '@angular/core';

import { SportMatchesTabComponent as CMSportMatchesTabComponent } from '@sb/components/sportMatchesTab/sport-matches-tab.component';

@Component({
  selector: 'sport-matches-tab',
  templateUrl: 'sport-matches-tab.component.html'
})
export class SportMatchesTabComponent extends CMSportMatchesTabComponent  {}
