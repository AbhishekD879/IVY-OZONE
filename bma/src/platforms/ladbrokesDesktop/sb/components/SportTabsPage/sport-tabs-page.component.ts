import { Component } from '@angular/core';

import {
  SportTabsPageComponent as AppSportTabsPageComponent
} from '@sb/components/sportTabsPage/sport-tabs-page.component';

@Component({
  selector: 'sport-tabs-page',
  templateUrl: '../../../../../app/sb/components/sportTabsPage/sport-tabs-page.component.html',
})
export class SportTabsPageComponent extends AppSportTabsPageComponent {
  protected navigateToSportLandingPage(): void {
    // Should do nothing
  }
}

