import { Component } from '@angular/core';

import { QuestionsPageComponent as AppQuestionsPageComponent } from '@app/questionEngine/components/questionsPage/questions-page.component';
import { IInfoDialogParams } from '@questionEngine/models/infoDialogParams.model';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { InfoDialogComponent } from '@questionEngine/components/shared/infoDialog/info-dialog.component';

@Component({
  selector: 'questions-page',
  templateUrl: '../../../../../app/questionEngine/components/questionsPage/questions-page.component.html',
  styleUrls: ['./questions-page.component.scss'],
})
export class QuestionsPageComponent extends AppQuestionsPageComponent {
  protected openInfoDialog(params: IInfoDialogParams): void {
    this.dialogService.openDialog(DialogService.API.qe.infoDialog,
      this.componentFactoryResolver.resolveComponentFactory(InfoDialogComponent), true, params);
  }
}
