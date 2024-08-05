import {Component, OnInit, ViewChild} from '@angular/core';
import {QEQuickLinks} from '@app/client/private/models/qeQuickLinks.model';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {QEQuickLinksApiService} from '@app/quiz/service/quick-links.api.service';
import {ActivatedRoute} from '@angular/router';
import {DialogService} from '@app/shared/dialog/dialog.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import {HttpResponse} from '@angular/common/http';
import {AppConstants} from '@app/app.constants';
import {QuizApiService} from '@app/quiz/service/quiz.api.service';
import * as _ from 'lodash';

@Component({
  selector: 'app-quick-links-edit',
  templateUrl: './quick-links-edit.component.html'
})
export class QuickLinksEditComponent implements OnInit {

  @ViewChild('actionButtons') actionButtons;

  qeQuickLinks: QEQuickLinks;
  public breadcrumbsData: Breadcrumb[];
  id: string;
  getDataError: string;

  constructor(private quickLinksApi: QEQuickLinksApiService,
              private quizApiService: QuizApiService,
              private route: ActivatedRoute,
              private dialogService: DialogService,
              private snackBar: MatSnackBar) {
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.loadInitialData();
  }

  isValidModel(qeQuickLinks): boolean {
    return qeQuickLinks.id.length > 0 && qeQuickLinks.title.trim().length > 0;
  }

  public updateText(htmlMarkup: string, index: number): void {
    this.qeQuickLinks.links[index].description = htmlMarkup;
  }

  private loadInitialData(): void {
    this.quickLinksApi.getQEQuickLinksById(this.id).subscribe((resp: any) => {
      this.qeQuickLinks = resp.body;
      this.breadcrumbsData = [{
        label: `Quick Links`,
        url: `/question-engine/quick-links`
      }, {
        label: this.qeQuickLinks.title,
        url: `/question-engine/quick-links/quick-link/${this.qeQuickLinks.id}`
      }];
    }, error => {
      this.getDataError = error.message;
    });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeQuickLinksPage();
        break;
      case 'save':
        this.saveQuickLinksPageChanges();
        break;
      case 'revert':
        this.revertQuickLinksPageChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  private removeQuickLinksPage(): void {

    this.quizApiService.getQuizzesByBrand()
      .subscribe((data: any) => {
        const quizzes = data.body;
        const anyQuiz = quizzes.filter(quiz => quiz.qeQuickLinks && quiz.qeQuickLinks.id === this.qeQuickLinks.id);

        if (anyQuiz && anyQuiz.length > 0) {
          const quizNames = _.map(anyQuiz, 'title');
          this.dialogService.showConfirmDialog({
            title: 'Remove Quick Links Page',
            message: 'This quick links page is used by already configured [' + quizNames.length
              + '] quizzes and this change will affect this configuration. Are you sure?',
            yesCallback: () => {
              removeQLPage.call(this);
            }
          });
        } else {
          removeQLPage.call(this);
        }

      });

    function removeQLPage() {
      this.quickLinksApi.deleteQEQuickLinks(this.qeQuickLinks.id)
        .subscribe((data: any) => {
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'Quick Links Page is Removed.'
          });
          this.router.navigate(['/question-engine/quick-links/']);
        });
    }

  }

  private saveQuickLinksPageChanges(): void {
    this.quickLinksApi.updateQEQuickLinks(this.qeQuickLinks)
      .map((response: HttpResponse<QEQuickLinks>) => {
        return response.body;
      })
      .subscribe((data: QEQuickLinks) => {
        this.qeQuickLinks = data;

        this.actionButtons.extendCollection(this.qeQuickLinks);
        this.showNotification('Quick Links Page Changes are Saved.');

      });
  }

  showNotification(message): void {
    this.snackBar.open(message, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
  }

  private revertQuickLinksPageChanges(): void {
    this.loadInitialData();
  }

}
