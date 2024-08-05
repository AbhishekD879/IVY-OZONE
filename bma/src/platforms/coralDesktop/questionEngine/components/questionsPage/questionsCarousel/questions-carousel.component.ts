import { Component } from '@angular/core';

import { QuestionsCarouselComponent } from '@app/questionEngine/components/questionsPage/questionsCarousel/questions-carousel.component';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { InfoDialogComponent } from '@coralDesktop/questionEngine/components/shared/infoDialog/info-dialog.component';

@Component({
  selector: 'questions-carousel',
  templateUrl: './questions-carousel.component.html',
  styleUrls: ['./questions-carousel.component.scss'],
})

export class DesktopQuestionsCarouselComponent extends QuestionsCarouselComponent {

  public goToNextSlide(): void {
    this.qeData.questionsList && this.qeData.questionsList.length > this.currentCarouselStep + 1
      && this.userAction[this.currentCarouselStep] && this.navigateToSlide(this.currentCarouselStep + 1);

    this.questionNumberGA = `${this.questionEngineService.sourceIdFromParams}/question${this.currentCarouselStep + 1}`;
    this.questionEngineService.trackPageViewGA(this.questionNumberGA);
  }

  protected redirectToEdit(): void {
    super.redirectToEdit();
    this.questionEngineService.trackPageViewGA(`/${this.questionEngineService.sourceIdFromParams}/question1`);
  }

  protected openInfoDialog(params) {
    this.dialogService.openDialog(DialogService.API.qe.infoSubmitDialog,
      this.componentFactoryResolver.resolveComponentFactory(InfoDialogComponent), true, params);
  }
}
