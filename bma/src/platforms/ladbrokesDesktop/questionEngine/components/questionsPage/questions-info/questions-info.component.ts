import { Component } from '@angular/core';

import {
  QuestionsInfoComponent as AppQuestionsInfoComponent
} from '@app/questionEngine/components/questionsPage/questions-info/questions-info.component';

@Component({
  selector: 'questions-info',
  templateUrl: '../../../../../../app/questionEngine/components/questionsPage/questions-info/questions-info.component.html',
  styleUrls: ['./questions-info.component.scss'],
})
export class QuestionsInfoComponent extends AppQuestionsInfoComponent {
}
