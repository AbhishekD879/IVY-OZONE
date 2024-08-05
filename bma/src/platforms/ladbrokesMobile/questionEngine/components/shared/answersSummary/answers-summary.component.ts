import { Component } from '@angular/core';

import {
  AnswersSummaryComponent as AppAnswersSummaryComponent
} from '@app/questionEngine/components/shared/answersSummary/answers-summary.component';

@Component({
  selector: 'answers-summary',
  templateUrl: '../../../../../../app/questionEngine/components/shared/answersSummary/answers-summary.component.html',
  styleUrls: ['./answers-summary.component.scss'],
})

export class AnswersSummaryComponent extends AppAnswersSummaryComponent {
}
