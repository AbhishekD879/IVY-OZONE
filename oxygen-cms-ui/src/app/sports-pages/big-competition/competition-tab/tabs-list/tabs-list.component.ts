import {Component, Input, OnInit} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {HttpResponse} from '@angular/common/http';
import {ActivatedRoute, Params} from '@angular/router';
import * as _ from 'lodash';

import {DialogService} from '@app/shared/dialog/dialog.service';
import {TabAddComponent} from '../tab-add/tab-add.component';
import {CompetitionTab} from '../../../../client/private/models';
import {BigCompetitionAPIService} from '../../service/big-competition.api.service';
import {AppConstants} from '@app/app.constants';
import {SpaceToDashPipe} from '@app/client/private/pipes/space-to-dash.pipe';
import {Order} from '@app/client/private/models/order.model';

@Component({
  selector: 'app-competition-tabs-list',
  templateUrl: './tabs-list.component.html'
})
export class TabsListComponent implements OnInit {
  @Input() tabs: CompetitionTab[] = [];

  public searchField: '';
  public dataTableColumns: any[] = [
    {
      name: 'Name',
      property: 'name',
      link: {
        hrefProperty: 'id',
        path: 'tab/'
      },
      type: 'link'
    },
    {
      name: 'Enabled',
      property: 'enabled',
      type: 'boolean'
    },
    {
      name: 'Tab has sub-tabs',
      property: 'hasSubtabs',
      type: 'boolean'
    }
  ];

  filterProperties: string[] = [
    'name'
  ];

  constructor(
    private dialog: MatDialog,
    public snackBar: MatSnackBar,
    private dialogService: DialogService,
    private activatedRoute: ActivatedRoute,
    private bigCompetitionApiService: BigCompetitionAPIService,
    private spaceToDashPipe: SpaceToDashPipe) {
  }

  ngOnInit(): void {
  }

  public createTab(): void {
    const dialogRef = this.dialog
      .open(TabAddComponent, { width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH });

    dialogRef.afterClosed().subscribe(newTab => {
      if (newTab) {
        newTab.name = _.trim(newTab.name);
        newTab.uri = `/${this.spaceToDashPipe.transform(newTab.name)}`;

        this.activatedRoute.params.subscribe((params: Params) => {
          this.bigCompetitionApiService.createCompetitionTab(params.competitionId, newTab)
            .map((competitionTab: HttpResponse<CompetitionTab>) => {
              return competitionTab.body;
            })
            .subscribe((competitionTab: CompetitionTab) => {
              if (competitionTab) {
                this.tabs.push(competitionTab);
                this.dialogService.showNotificationDialog({
                  title: 'Save Completed',
                  message: 'Competition Tab is Created and Stored'
                });
              }
            });
         });
      }
    });
  }

  public reorderHandler(newOrder: Order): void {

    this.activatedRoute.params.subscribe((params: Params) => {
      this.bigCompetitionApiService.postNewTabsOrder(params.competitionId, newOrder)
        .subscribe(() => {
          this.snackBar.open('Tabs Order Saved!', 'Ok!', {
            duration: AppConstants.HIDE_DURATION
          });
      });
    });
  }

  /**
   *
   * @param {Object} tab
   */
  public removeTab(tab: CompetitionTab): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Competition Tab',
      message: `Are You Sure You Want to Remove Competition Tab "${tab.name}"?`,
      yesCallback: () => {
        this.sendRemoveRequest(tab);
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {CompetitionTab} competitionTab
   */
  private sendRemoveRequest(competitionTab: CompetitionTab): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.bigCompetitionApiService.deleteCompetitionTab(params.competitionId, competitionTab.id)
        .subscribe((data: any) => {
          this.tabs.splice(this.tabs.indexOf(competitionTab), 1);
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'Competition Tab is Removed'
          });
        });
    });
  }
}
