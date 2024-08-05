import { Component } from '@angular/core';

import {
  PreviousTabComponent as AppPreviousTabComponent
} from '@app/questionEngine/components/resultsPage/tabs/previousTab/previous-tab.component';

@Component({
  selector: 'previous-tab',
  templateUrl: '../../../../../../../app/questionEngine/components/resultsPage/tabs/previousTab/previous-tab.component.html',
  styleUrls: ['./previous-tab.component.scss'],
})

export class PreviousTabComponent extends AppPreviousTabComponent {
}
