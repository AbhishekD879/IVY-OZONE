import { Component } from '@angular/core';
import { QuestionsPageComponent } from '@app/questionEngine/components/questionsPage/questions-page.component';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { InfoDialogComponent } from '@coralDesktop/questionEngine/components/shared/infoDialog/info-dialog.component';

@Component({
  selector: 'questions-page',
  templateUrl: './questions-page.component.html',
  styleUrls: ['./questions-page.component.scss'],
})
export class DesktopQuestionsPageComponent extends QuestionsPageComponent {

  protected openInfoDialog(params) {
    this.dialogService.openDialog(DialogService.API.qe.infoDialog,
      this.componentFactoryResolver.resolveComponentFactory(InfoDialogComponent), true, params);
  }
}
