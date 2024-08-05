import { Component } from '@angular/core';

import { SportTabsPageComponent } from '@sb/components/sportTabsPage/sport-tabs-page.component';

@Component({
  selector: 'sport-tabs-page',
  templateUrl: '../../../../../app/sb/components/sportTabsPage/sport-tabs-page.component.html',
})
export class DesktopSportTabsPageComponent extends SportTabsPageComponent {
  protected navigateToSportLandingPage(): void {
    // Should do nothing
  }
}

