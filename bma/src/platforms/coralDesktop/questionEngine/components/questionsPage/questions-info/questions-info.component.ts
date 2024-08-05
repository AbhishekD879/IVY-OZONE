import { Component } from '@angular/core';

import { QuestionsInfoComponent } from '@app/questionEngine/components/questionsPage/questions-info/questions-info.component';

  @Component({
    selector: 'questions-info',
    templateUrl: '../../../../../../app/questionEngine/components/questionsPage/questions-info/questions-info.component.html',
    styleUrls: ['./questions-info.component.scss'],
  })

  export class DesktopQuestionsInfoComponent extends QuestionsInfoComponent {
    isDesktop = true;
}
