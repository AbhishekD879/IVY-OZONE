import {Component, OnInit} from '@angular/core';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {ApiClientService} from '@app/client/private/services/http';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {Router} from '@angular/router';
import {HttpResponse} from '@angular/common/http';
import * as _ from 'lodash';
import {QEQuickLinks} from '@app/client/private/models/qeQuickLinks.model';
import {forkJoin} from 'rxjs/observable/forkJoin';
import {QuizApiService} from '@app/quiz/service/quiz.api.service';

@Component({
  selector: 'app-quick-links-list',
  templateUrl: './quick-links-list.component.html'
})
export class QuickLinksListComponent implements OnInit {

  public qeQuickLinks: Array<QEQuickLinks>;
  public error: string;
  public searchField: string = '';
  public dataTableColumns: Array<DataTableColumn> = [
    {
      'name': 'Title',
      'property': 'title',
      'link': {
        hrefProperty: 'id',
        path: 'quick-link/'
      },
      'type': 'link'
    }
  ];
  public searchableProperties: Array<string> = [
    'title'
  ];

  constructor(
    private apiClientService: ApiClientService,
    private quizApiService: QuizApiService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private router: Router
  ) { }

  ngOnInit() {
    this.globalLoaderService.showLoader();
    this.apiClientService.qeQuickLinksService()
      .findAllByBrand()
      .map((response: HttpResponse<QEQuickLinks[]>) => {
        return response.body;
      })
      .subscribe((data: QEQuickLinks[]) => {
        this.qeQuickLinks = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createQEQuickLinks() {
    this.router.navigate(['question-engine/quick-links/create']);
  }

  removeHandler(qeQuickLinks: QEQuickLinks): void {

    this.quizApiService.getQuizzesByBrand()
      .subscribe((data: any) => {
        const quizzes = data.body;
        const anyQuiz = quizzes.filter(quiz => quiz.qeQuickLinks && quiz.qeQuickLinks.id === qeQuickLinks.id);

        if (anyQuiz && anyQuiz.length > 0) {
          const quizNames = _.map(anyQuiz, 'title');
          this.dialogService.showConfirmDialog({
            title: 'Remove Quick Links Page',
            message: 'This quick links page is used by already configured [' + quizNames.length
              + '] quizzes and this change will affect this configuration. Are you sure?',
            yesCallback: () => {
              removeQELinksPage.call(this);
            }
          });
        } else {
          this.dialogService.showConfirmDialog({
            title: 'QE quick links',
            message: 'Are You Sure You Want to Remove QE Quick Links?',
            yesCallback: () => {
              removeQELinksPage.call(this);
            }
          });
        }

      });

    function removeQELinksPage() {

      this.globalLoaderService.showLoader();
      this.apiClientService.qeQuickLinksService()
        .delete(qeQuickLinks.id)
        .subscribe(() => {
          _.remove(this.qeQuickLinks, {id: qeQuickLinks.id});
          this.globalLoaderService.hideLoader();
        }, error => {
          console.error(error.message);
          this.globalLoaderService.hideLoader();
        });
    }
  }

  removeHandlerMulti(qeQuickLinks: string[]) {
    this.quizApiService.getQuizzesByBrand()
      .subscribe((data: any) => {
        const quizzes = data.body;

        const anyQuizzes = quizzes.filter(quiz => quiz.qeQuickLinks && qeQuickLinks.indexOf(quiz.qeQuickLinks.id) > -1);
        if (anyQuizzes && anyQuizzes.length > 0) {
          const qeQuickLinksPagesTitles = _.uniq(_.map(anyQuizzes, 'qeQuickLinks.title'));
          this.dialogService.showConfirmDialog({
            title: 'Remove QE Quick Links Page',
            message: 'This quick links pages [' + qeQuickLinksPagesTitles + '] are used by already configured ' +
              'quizzes and this change will affect this configuration. Are you sure?',
            yesCallback: () => {
              removeMultiQEQuickLinks.call(this);
            }
          });
        } else {
          this.dialogService.showConfirmDialog({
            title: `Remove QE Quick Links (${qeQuickLinks.length})`,
            message: 'Are You Sure You Want to Remove QE Quick Links?',
            yesCallback: () => {
              removeMultiQEQuickLinks.call(this);
            }
          });
        }

      });


    function removeMultiQEQuickLinks() {
      this.globalLoaderService.showLoader();
      forkJoin(qeQuickLinks.map(id => this.apiClientService.qeQuickLinksService()
        .delete(id)))
        .subscribe(() => {
          qeQuickLinks.forEach((id) => {
            const index = _.findIndex(this.qeQuickLinks, {id: id});
            this.qeQuickLinks.splice(index, 1);
          });
          this.globalLoaderService.hideLoader();
        });
    }
  }

}
