import {Component, OnInit} from '@angular/core';
import {Quiz} from '@app/client/private/models/quiz.model';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import { MatDialog } from '@angular/material/dialog';
import {AppConstants} from '@app/app.constants';
import {QuizEngineCreateComponent} from '@app/quiz/quiz-engine/quiz-engine-create/quiz-engine-create.component';
import {QuizApiService} from '@app/quiz/service/quiz.api.service';
import {Router} from '@angular/router';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {forkJoin} from 'rxjs/observable/forkJoin';
import * as _ from 'lodash';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';

@Component({
  selector: 'app-quiz-engine-list',
  templateUrl: './quiz-engine-list.component.html',
  styleUrls: ['./quiz-engine-list.component.scss']
})
export class QuizEngineListComponent implements OnInit {
  quizData: Array<Quiz>;
  searchField: string = '';
  getDataError: string;
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Quiz Name',
      property: 'title',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Source ID',
      property: 'sourceId'
    },
    {
      name: 'Displayed?',
      property: 'active',
      type: 'boolean'
    },
    {
      name: 'Display From',
      property: 'displayFrom'
    },
    {
      name: 'Display To',
      property: 'displayTo'
    },
    {
      name: 'Report',
      property: 'questionSummaryReportMarkup',
      type: 'custom',
      customOnClickHandler: (id) =>  this.downloadReport(id)
    }
  ];

  filterProperties: Array<string> = [
    'title',
    'sourceId',
    'active',
    'displayFrom',
    'displayTo'
  ];

  constructor(private dialog: MatDialog,
              private dialogService: DialogService,
              private quizApiService: QuizApiService,
              private globalLoaderService: GlobalLoaderService,
              private router: Router) {
  }

  ngOnInit() {
    this.loadQuizzes();
  }

  loadQuizzes() {
    this.quizApiService.getQuizzesByBrand()
      .subscribe((data: any) => {
        this.quizData = data.body;

        this.quizData.forEach(quiz => {
          if (this.isQuizActiveAndLive(quiz)) {
            quiz.highlighted = true;
          }
          quiz.questionSummaryReportMarkup = '<i class="material-icons report">get_app</i>';
        });
      }, error => {
        this.getDataError = error.message;
      });
  }

  private isQuizActiveAndLive(quiz: Quiz): boolean {
    const displayFromDate = new Date(quiz.displayFrom);
    const displayToDate = new Date(quiz.displayTo);
    const dateNow = new Date();
    return quiz.active && dateNow > displayFromDate && dateNow < displayToDate;
  }

  createQuiz() {
    const dialogRef = this.dialog.open(QuizEngineCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {}
    });

    dialogRef.afterClosed().subscribe(newQuiz => {
      if (newQuiz) {
        this.quizApiService.createQuiz(newQuiz)
          .subscribe(response => {
            if (response) {
              this.quizData.push(newQuiz);
              this.router.navigate([`/question-engine/quiz/${response.body.id}`]);
            }
          });
      }
    });
  }

  removeQuiz(quiz: Quiz) {
    this.dialogService.showConfirmDialog({
      title: 'Remove Quiz',
      message: 'This will permanently remove the quiz. Are you sure?',
      yesCallback: () => {
        this.sendRemoveRequest(quiz);
      }
    });
  }

  sendRemoveRequest(quiz: Quiz) {
    this.quizApiService.deleteQuiz(quiz.id)
      .subscribe((data: any) => {
        this.quizData.splice(this.quizData.indexOf(quiz), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Quiz is Removed.'
        });
      });
  }

  removeHandlerMulty(quizIds: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Quiz (${quizIds.length})`,
      message: 'This will permanently remove the quizzes. Are you sure?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        forkJoin(quizIds.map(id => this.quizApiService.deleteQuiz(id)))
          .subscribe(() => {
            quizIds.forEach((id) => {
              const index = _.findIndex(this.quizData, {id: id});
              this.quizData.splice(index, 1);
            });
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  isRemoveCheckboxEnabled(quiz: Quiz): boolean {
    return quiz.active && new Date(quiz.displayFrom).getTime() < new Date().getTime();
  }

  downloadReport(quiz: Quiz) {
    this.quizApiService.generateQuestionSummaryReport(quiz.id)
      .subscribe(
        response => {
          const blob = new Blob([response.body.csvContent], {type: 'text/csv'});
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = `${quiz.title} ${response.body.createdDate}.csv`;
          link.click();
        },
        error => this.getDataError = error.message,
      );
  }
}

