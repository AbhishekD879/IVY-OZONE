import {Component, Input, OnInit} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {HttpResponse} from '@angular/common/http';
import {ActivatedRoute, Params} from '@angular/router';
import * as _ from 'lodash';

import {DialogService} from '@app/shared/dialog/dialog.service';
import {CompetitionTab} from '../../../../client/private/models';
import {BigCompetitionAPIService} from '../../service/big-competition.api.service';
import {CompetitionSubTabAddComponent} from '../competition-sub-tab-add/competition-sub-tab-add.component';
import {AppConstants} from '@app/app.constants';
import {SpaceToDashPipe} from '@app/client/private/pipes/space-to-dash.pipe';
import {Order} from '@app/client/private/models/order.model';

@Component({
  selector: 'competition-sub-tabs-list',
  templateUrl: './competition-sub-tabs-list.component.html'
})
export class CompetitionSubTabsListComponent implements OnInit {
  @Input() tabs: CompetitionTab[] = [];

  public searchField: '';
  public dataTableColumns: any[] = [
    {
      name: 'Name',
      property: 'name',
      link: {
        hrefProperty: 'id',
        path: 'subtab/'
      },
      type: 'link'
    },
    {
      name: 'URL',
      property: 'uri'
    },
    {
      name: 'Enabled',
      property: 'enabled',
      type: 'boolean'
    }
  ];

  public filterProperties: string[] = [
    'name'
  ];

  constructor(
    private dialog: MatDialog,
    private dialogService: DialogService,
    public snackBar: MatSnackBar,
    private activatedRoute: ActivatedRoute,
    private bigCompetitionApiService: BigCompetitionAPIService,
    private spaceToDashPipe: SpaceToDashPipe) {
  }

  ngOnInit(): void {
  }

  public createTab(): void {
    const dialogRef = this.dialog
      .open(CompetitionSubTabAddComponent, { width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH });

    dialogRef.afterClosed().subscribe(newTab => {
      if (newTab) {
        newTab.name = _.trim(newTab.name);
        newTab.uri = `/${this.spaceToDashPipe.transform(newTab.name)}`;

        this.activatedRoute.params.subscribe((params: Params) => {
          this.bigCompetitionApiService.createSubTab(params.competitionId, params.tabId, newTab)
            .map((competitionTab: HttpResponse<CompetitionTab>) => {
              return competitionTab.body;
            })
            .subscribe((competitionTab: CompetitionTab) => {
              if (competitionTab) {
                this.tabs.push(competitionTab);
                this.dialogService.showNotificationDialog({
                  title: 'Save Completed',
                  message: 'Competition Sub Tab is Created and Stored'
                });
              }
            });
        });
      }
    });
  }

  public reorderHandler(newOrder: Order): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.bigCompetitionApiService.postNewSubTabsOrder(params.competitionId, params.tabId, newOrder)
        .subscribe(() => {
          this.snackBar.open('Sub Tabs Order Saved!', 'Ok!', {
            duration: AppConstants.HIDE_DURATION
          });
      });
    });
  }

  public removeTab(tab: CompetitionTab): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Sub Tab',
      message: 'Are You Sure You Want to Remove Sub Tab?',
      yesCallback: () => {
        this.sendRemoveRequest(tab);
      }
    });
  }

  /**
   * Send DELETE API request.
   * @param {CompetitionTab} tab
   */
  public sendRemoveRequest(tab: CompetitionTab): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.bigCompetitionApiService.deleteSubTab(params.competitionId, params.tabId, tab.id)
        .subscribe((data: any) => {
          this.tabs.splice(this.tabs.indexOf(tab), 1);
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'Sub Tab is Removed'
          });
        });
    });
  }
}
