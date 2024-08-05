import {Component, OnInit} from '@angular/core';
import {SplashPage} from '@app/client/private/models/splash-page.model';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {Router} from '@angular/router';
import {forkJoin} from 'rxjs/observable/forkJoin';
import * as _ from 'lodash';
import {SplashPageApiService} from '@app/quiz/service/splash-page.api.service';
import {QuizApiService} from '@app/quiz/service/quiz.api.service';

@Component({
  selector: 'app-splash-page-list',
  templateUrl: './splash-page-list.component.html'
})
export class SplashPageListComponent implements OnInit {

  splashPageData: Array<SplashPage>;
  searchField: string = '';
  getDataError: string;
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Splash Page Name',
      property: 'title',
      link: {
        hrefProperty: 'id',
        path: 'splash-page/'
      },
      type: 'link'
    }
  ];

  filterProperties: Array<string> = [
    'title'
  ];

  constructor(private dialogService: DialogService,
              private quizApiService: QuizApiService,
              private splashPageApiService: SplashPageApiService,
              private globalLoaderService: GlobalLoaderService,
              private router: Router) { }

  ngOnInit() {
    this.loadSplashPages();
  }

  loadSplashPages() {
    this.globalLoaderService.showLoader();
    this.splashPageApiService.getSplashPagesByBrand()
      .subscribe((data: any) => {
        this.splashPageData = data.body;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.getDataError = error.message;
        this.globalLoaderService.hideLoader();
      });
  }

  removeSplashPage(splashPage: SplashPage) {

    this.quizApiService.getQuizzesByBrand()
      .subscribe((data: any) => {
        const quizzes = data.body;
        const anyQuiz = quizzes.filter(quiz => quiz.splashPage && quiz.splashPage.id === splashPage.id);

        if (anyQuiz && anyQuiz.length > 0) {
          const quizNames = _.map(anyQuiz, 'title');
          this.dialogService.showConfirmDialog({
            title: 'Remove Splash Page',
            message: 'This splash page is used by already configured [' + quizNames.length
              + '] quizzes and this change will affect this configuration. Are you sure?',
            yesCallback: () => {
              this.sendRemoveRequest(splashPage);
            }
          });
        } else {
          removeSpPage.call(this);
        }

      });

    function removeSpPage() {
      this.dialogService.showConfirmDialog({
        title: 'Remove Splash Page',
        message: 'Are You Sure You Want to Remove Splash Page?',
        yesCallback: () => {
          this.sendRemoveRequest(splashPage);
        }
      });
    }
  }

  sendRemoveRequest(splashPage: SplashPage) {
    this.splashPageApiService.deleteSplashPage(splashPage.id)
      .subscribe((data: any) => {
        this.splashPageData.splice(this.splashPageData.indexOf(splashPage), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Splash page is Removed.'
        });
      });
  }

  removeHandlerMulty(splashPageIds: string[]) {

    this.quizApiService.getQuizzesByBrand()
      .subscribe((data: any) => {
        const quizzes = data.body;

        const anyQuizzes = quizzes.filter(quiz => quiz.splashPage && splashPageIds.indexOf(quiz.splashPage.id) > -1);
        if (anyQuizzes && anyQuizzes.length > 0) {
          const spPagesTitles = _.uniq(_.map(anyQuizzes, 'splashPage.title'));
          this.dialogService.showConfirmDialog({
            title: 'Remove Splash Page',
            message: 'This splash pages [' + spPagesTitles + '] are used by already configured ' +
              'quizzes and this change will affect this configuration. Are you sure?',
            yesCallback: () => {
              removeMultipleSpPages.call(this);
            }
          });
        } else {
          this.dialogService.showConfirmDialog({
            title: `Remove Splash Page (${splashPageIds.length})`,
            message: 'Are You Sure You Want to Remove Splash Pages?',
            yesCallback: () => {
              removeMultipleSpPages.call(this);
            }
          });
        }

      });

    function removeMultipleSpPages() {
      this.globalLoaderService.showLoader();
      forkJoin(splashPageIds.map(id => this.splashPageApiService.deleteSplashPage(id)))
        .subscribe(() => {
          splashPageIds.forEach((id) => {
            const index = _.findIndex(this.splashPageData, {id: id});
            this.splashPageData.splice(index, 1);
          });
          this.globalLoaderService.hideLoader();
        });
    }
  }

  openCreatePage() {
    this.router.navigate(['question-engine/splash-pages/create']);
  }
}
