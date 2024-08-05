import { Component } from '@angular/core';

import { ResultsPageComponent as AppResultsPageComponent } from '@app/questionEngine/components/resultsPage/results-page.component';

@Component({
  selector: 'results-page',
  templateUrl: './results-page.component.html',
  styleUrls: ['./results-page.component.scss'],
})

export class ResultsPageComponent extends AppResultsPageComponent {
  handleBackArrow(): void {
    this.backToSplash();
  }
}
