import { Component, OnInit } from '@angular/core';
import {EndPage} from '@app/client/private/models/end-page.model';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {Router} from '@angular/router';
import {forkJoin} from 'rxjs/observable/forkJoin';
import * as _ from 'lodash';
import {EndPageApiService} from '@app/quiz/service/end-page.api.service';
import {QuizApiService} from '@app/quiz/service/quiz.api.service';

@Component({
  selector: 'end-page-list',
  templateUrl: './end-page-list.component.html'
})
export class EndPageListComponent implements OnInit {

  endPageData: Array<EndPage>;
  searchField: string = '';
  getDataError: string;
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'End Page Name',
      property: 'title',
      link: {
        hrefProperty: 'id',
        path: 'edit'
      },
      type: 'link'
    }
  ];

  filterProperties: Array<string> = [
    'title'
  ];

  constructor(private dialogService: DialogService,
              private quizApiService: QuizApiService,
              private endPageApiService: EndPageApiService,
              private globalLoaderService: GlobalLoaderService,
              private router: Router) { }

  ngOnInit() {
    this.loadEndPages();
  }

  loadEndPages() {
    this.globalLoaderService.showLoader();
    this.endPageApiService.getEndPagesByBrand()
      .subscribe((data: any) => {
        this.endPageData = data.body;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.getDataError = error.message;
        this.globalLoaderService.hideLoader();
      });
  }

  removeEndPage(endPage: EndPage) {

    this.quizApiService.getQuizzesByBrand()
      .subscribe((data: any) => {
        const quizzes = data.body;
        const anyQuiz = quizzes.filter(quiz => quiz.endPage && quiz.endPage.id === endPage.id);

        if (anyQuiz && anyQuiz.length > 0) {
          const quizNames = _.map(anyQuiz, 'title');
          this.dialogService.showConfirmDialog({
            title: 'Remove End Page',
            message: 'This end page is used by already configured [' + quizNames.length
              + '] quizzes and this change will affect this configuration. Are you sure?',
            yesCallback: () => {
              this.sendRemoveRequest(endPage);
            }
          });
        } else {
          this.dialogService.showConfirmDialog({
            title: 'Remove End Page',
            message: 'Are You Sure You Want to Remove End Page?',
            yesCallback: () => {
              this.sendRemoveRequest(endPage);
            }
          });
        }

      });
  }

  sendRemoveRequest(endPage: EndPage) {
    this.endPageApiService.deleteEndPage(endPage.id)
      .subscribe((data: any) => {
        this.endPageData.splice(this.endPageData.indexOf(endPage), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'End page is Removed.'
        });
      });
  }

  removeHandlerMulti(endPageIds: string[]) {

    this.quizApiService.getQuizzesByBrand()
      .subscribe((data: any) => {
        const quizzes = data.body;

        const anyQuizzes = quizzes.filter(quiz => quiz.endPage && endPageIds.indexOf(quiz.endPage.id) > -1);
        if (anyQuizzes && anyQuizzes.length > 0) {
          const spPagesTitles = _.uniq(_.map(anyQuizzes, 'endPage.title'));
          this.dialogService.showConfirmDialog({
            title: 'Remove End Page',
            message: 'This end pages [' + spPagesTitles + '] are used by already configured ' +
              'quizzes and this change will affect this configuration. Are you sure?',
            yesCallback: () => {
              removeMultiEndPages.call(this);
            }
          });
        } else {
          this.dialogService.showConfirmDialog({
            title: `Remove End Page (${endPageIds.length})`,
            message: 'Are You Sure You Want to Remove End Pages?',
            yesCallback: () => {
              removeMultiEndPages.call(this);
            }
          });
        }

      });

    function removeMultiEndPages() {
      this.globalLoaderService.showLoader();
      forkJoin(endPageIds.map(id => this.endPageApiService.deleteEndPage(id)))
        .subscribe(() => {
          endPageIds.forEach((id) => {
            const index = _.findIndex(this.endPageData, {id: id});
            this.endPageData.splice(index, 1);
          });
          this.globalLoaderService.hideLoader();
        });
    }

  }

  openCreatePage() {
    this.router.navigateByUrl('question-engine/end-page/create');
  }
}
