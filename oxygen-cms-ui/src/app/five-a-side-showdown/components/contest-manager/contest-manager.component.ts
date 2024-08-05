import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { Order } from '@app/client/private/models/order.model';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { forkJoin } from 'rxjs/observable/forkJoin';
import {
  BREADCRUMB_DATA,
  CONTESTFORM,
  CONTEST_ERROR_LABELS,
  CONTEST_TABLE_COLUMNS,
  FILTER_PROPERTIES,
  REMOVE_CONFIRMATION_DIALOG,
  REMOVE_CONFIRMATION_MULTI_DIALOG,
  REMOVE_CONFIRMATION_MULTI_SUCCESS_DIALOG,
  REMOVE_CONFIRMATION_SUCCESS_DIALOG,
  REORDER_MSG,
  SAVE_CONFIRMATION_DIALOG,
} from '@app/five-a-side-showdown/constants/contest-manager.constants';
import { AppConstants } from '@app/app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AddContestComponent } from '@app/five-a-side-showdown/components/add-contest/add-contest.component';
import { HttpResponse } from '@angular/common/http';
import { IContest } from '@app/five-a-side-showdown/models/contest-manager';
import { ErrorService } from '@app/client/private/services/error.service';

@Component({
  selector: 'app-contest-manager',
  templateUrl: './contest-manager.component.html',
  styleUrls: ['./contest-manager.component.scss'],
})
export class ContestManagerComponent implements OnInit {
  public isLoading: boolean = false;

  public filterProperties: string[] = FILTER_PROPERTIES;

  public searchField: string = '';

  public dataTableColumns: Array<DataTableColumn> = CONTEST_TABLE_COLUMNS;

  public contests: IContest[] = [];

  public readonly CONTESTFORM = CONTESTFORM;

  constructor(
    private router: Router,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private apiClientService: ApiClientService,
    private snackBar: MatSnackBar,
    private errorService: ErrorService
  ) {}

  ngOnInit(): void {
    this.loadShowDownContests();
  }

  /**
   * Load the contests for the contest Manager
   */
  private loadShowDownContests(): void {
    this.showHideSpinner();
    this.apiClientService
      .contestManagerService()
      .getContests()
      .map((response: HttpResponse<IContest[]>) => {
        return response.body;
      })
      .subscribe(
        (contestsData: IContest[]) => {
          this.contests = contestsData;
          this.showHideSpinner(false);
        },
        (error) => {
          this.errorService.emitError(CONTEST_ERROR_LABELS.loadingContestLabel);
          this.showHideSpinner(false);
        }
      );
  }

  /**
   * Show or Hide spinner for the api calls
   * @param {boolean} toShow
   */
  public showHideSpinner(toShow: boolean = true): void {
    toShow
      ? this.globalLoaderService.showLoader()
      : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  /**
   * Clone the contest from the contest entries
   * @param {IContest} contest
   */
   cloneContestElement(contest: IContest): void {
    this.createContestModule('clone', contest);
  }

  /**
   * Remove the contest from the contest entries
   * @param {IContest} contest
   */
  removeContestElement(contest: IContest): void {
    this.dialogService.showConfirmDialog({
      title: REMOVE_CONFIRMATION_DIALOG.title,
      message: `${REMOVE_CONFIRMATION_DIALOG.message} ${contest.name}`,
      yesCallback: () => {
        this.sendRemoveRequest(contest);
      },
    });
  }

  /**
   * Remove the multiple contests from the contest entries
   * @param {string[]} contestModulesIds
   */
  removeHandlerMulty(contestModulesIds: string[]): void {
    this.dialogService.showConfirmDialog({
      title: `${REMOVE_CONFIRMATION_MULTI_DIALOG.title} (${contestModulesIds.length})`,
      message: REMOVE_CONFIRMATION_MULTI_DIALOG.message,
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        forkJoin(
          contestModulesIds.map((id) =>
            this.apiClientService.contestManagerService().removeContestForId(id)
          )
        ).subscribe(() => {
          contestModulesIds.forEach((id) => {
            const index = this.contests.findIndex(
              (contest) => contest.id === id
            );
            this.contests.splice(index, 1);
          });
          this.dialogService.showNotificationDialog({
            title: REMOVE_CONFIRMATION_MULTI_SUCCESS_DIALOG.title,
            message: REMOVE_CONFIRMATION_MULTI_SUCCESS_DIALOG.message,
          });
          this.globalLoaderService.hideLoader();
        });
      },
    });
  }

  /**
   * Send remove request for the contest
   * @param {IContest} contest
   */
  sendRemoveRequest(contest: IContest) {
    this.apiClientService
      .contestManagerService()
      .removeContestForId(contest.id)
      .subscribe(() => {
        const index = this.contests.findIndex(
          (removedcontest) => removedcontest.id === contest.id
        );
        this.contests.splice(index, 1);
        this.dialogService.showNotificationDialog({
          title: REMOVE_CONFIRMATION_SUCCESS_DIALOG.title,
          message: REMOVE_CONFIRMATION_SUCCESS_DIALOG.message,
        });
      });
  }

  /**
   * Reordering contests
   * @param {order} newOrder
   */
  reorderHandler(newOrder: Order): void {
    this.globalLoaderService.showLoader();
    this.apiClientService
      .contestManagerService()
      .postNewOrder(newOrder)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.snackBar.open(REORDER_MSG.message, REORDER_MSG.action, {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  /**
   * Click handler for the contest creation
   */
  public createContestModule(type?: string, contestData?: IContest): void {
    this.dialogService.showCustomDialog(AddContestComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: SAVE_CONFIRMATION_DIALOG.title,
      yesOption: SAVE_CONFIRMATION_DIALOG.yesOption,
      noOption: SAVE_CONFIRMATION_DIALOG.noOption,
      data: { dialogType: type, dialogData: contestData },
      yesCallback: (contest: IContest) => {
        this.showHideSpinner();
        this.convertToUTCDate(contest);
        this.apiClientService
          .contestManagerService()
          .createContest(contest)
          .map((response: HttpResponse<IContest>) => {
            return response.body;
          })
          .subscribe(
            (savedcontest: IContest) => {
              this.showHideSpinner(false);
              this.router.navigate([
                `${BREADCRUMB_DATA.edit_url}/${savedcontest.id}`,
              ]);
            },
            (error) => {
              this.showHideSpinner(false);
              this.errorService.emitError(
                CONTEST_ERROR_LABELS.createContestLabel
              );
            }
          );
      },
      noCallback: (data: {cloned: boolean}) => {
        data.cloned ? this.loadShowDownContests() : '';
      }
    });
  }

  /**
   * To convert start time to UTC date format.
   * @param {IContest} contest
   * @returns {void}
   */
  private convertToUTCDate(contest: IContest): void {
    const currentDate: Date = new Date(contest.startDate);
    const utcDate = new Date(Date.UTC(currentDate.getFullYear(), currentDate.getMonth(),
    currentDate.getDate(), currentDate.getHours(), currentDate.getMinutes(), currentDate.getSeconds()));
    contest.utcStartDate = utcDate.toISOString();
  }
}
