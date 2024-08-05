import { Component } from '@angular/core';

import { QuestionsPageComponent as AppQuestionsPageComponent } from '@app/questionEngine/components/questionsPage/questions-page.component';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { InfoDialogComponent } from '@ladbrokesDesktop/questionEngine/components/shared/infoDialog/info-dialog.component';
import { IInfoDialogParams } from '@questionEngine/models/infoDialogParams.model';

@Component({
  selector: 'questions-page',
  templateUrl: './questions-page.component.html',
  styleUrls: ['./questions-page.component.scss'],
})
export class QuestionsPageComponent extends AppQuestionsPageComponent {
  handleBackArrow(): void {
    this.openGoToSplashOrContinueDialog();
  }

  protected openInfoDialog(params: IInfoDialogParams): void {
    this.dialogService.openDialog(DialogService.API.qe.infoDialog,
      this.componentFactoryResolver.resolveComponentFactory(InfoDialogComponent), true, params);
  }
}
