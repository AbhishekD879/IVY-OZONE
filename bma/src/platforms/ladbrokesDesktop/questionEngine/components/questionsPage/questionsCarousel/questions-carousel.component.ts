import { Component } from '@angular/core';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { InfoDialogComponent } from '@ladbrokesDesktop/questionEngine/components/shared/infoDialog/info-dialog.component';

import {
  QuestionsCarouselComponent as AppQuestionsCarouselComponent
} from '@app/questionEngine/components/questionsPage/questionsCarousel/questions-carousel.component';
import { IInfoDialogParams } from '@questionEngine/models/infoDialogParams.model';
import { TIMEOUT_SWIPE_TUTORIAL, LBR_DESKTOP_HEADER_HEIGHT } from '@questionEngine/constants/question-engine.constant';

@Component({
  selector: 'questions-carousel',
  templateUrl: './questions-carousel.component.html',
  styleUrls: ['./questions-carousel.component.scss'],
})

export class QuestionsCarouselComponent extends AppQuestionsCarouselComponent {

  public goToNextSlide(): void {
    this.qeData.questionsList && this.qeData.questionsList.length > this.currentCarouselStep + 1
    && this.userAction[this.currentCarouselStep] && this.navigateToSlide(this.currentCarouselStep + 1);

    this.questionNumberGA = `/${this.questionEngineService.sourceIdFromParams}/question${this.currentCarouselStep + 1}`;
    this.questionEngineService.trackPageViewGA(this.questionNumberGA);
  }

  protected redirectToEdit(): void {
    super.redirectToEdit();
    this.questionEngineService.trackPageViewGA(`/${this.questionEngineService.sourceIdFromParams}/question1`);
  }

  protected openInfoDialog(params: IInfoDialogParams): void {
    this.dialogService.openDialog(DialogService.API.qe.infoSubmitDialog,
      this.componentFactoryResolver.resolveComponentFactory(InfoDialogComponent), true, params);
  }

  protected swipeBehaviour(): void {
    this.questionsCarousel.onSlideChange(() => {
      this.windowRefService.nativeWindow.scrollTo({ top: LBR_DESKTOP_HEADER_HEIGHT, left: 0, behavior: 'smooth'});
      if (this.showSwipeTutorial && this.showSwipeTutorial() && this.showSwipeTutorialDialog) {
        this.toggleSwipeTutorialDialog = true;
        this.showSwipeTutorialDialog = false;
        this.windowRefService.nativeWindow.setTimeout(() => {
          this.toggleSwipeTutorialDialog = false;
        }, TIMEOUT_SWIPE_TUTORIAL);
      }
      this.ngCarouselDisableRightSwipe = !(this.currentCarouselStep >= 0 && (this.userAction[this.currentCarouselStep]));
    });
  }
}
