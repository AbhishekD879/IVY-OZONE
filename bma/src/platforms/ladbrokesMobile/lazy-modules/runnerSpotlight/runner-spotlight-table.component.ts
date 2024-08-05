import { Component } from '@angular/core';

import { RunnerSpotlightTableComponent } from '@lazy-modules/runnerSpotlight/runner-spotlight-table.component';

@Component({
  selector: 'runner-spotlight-table',
  templateUrl: './runner-spotlight-table.component.html',
  styleUrls: ['./runner-spotlight-table.component.scss']
})
export class MobileRunnerSpotlightTableComponent extends RunnerSpotlightTableComponent {
}
