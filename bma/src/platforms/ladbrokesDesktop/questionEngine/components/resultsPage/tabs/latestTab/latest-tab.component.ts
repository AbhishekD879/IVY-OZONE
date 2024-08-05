import { Component } from '@angular/core';

import {
  LatestTabComponent as AppLatestTabComponent
} from '@app/questionEngine/components/resultsPage/tabs/latestTab/latest-tab.component';

@Component({
  selector: 'latest-tab',
  templateUrl: '../../../../../../../app/questionEngine/components/resultsPage/tabs/latestTab/latest-tab.component.html',
  styleUrls: ['./latest-tab.component.scss'],
})
export class LatestTabComponent extends AppLatestTabComponent {
}
