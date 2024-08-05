import {Component, Input, OnInit} from '@angular/core';
import {CompetitionModule} from '../../../../client/private/models';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {CompetitionModuleAddComponent} from '../competition-module-add/competition-module-add.component';
import {DialogService} from '../../../../shared/dialog/dialog.service';
import {HttpResponse} from '@angular/common/http';
import {ActivatedRoute, Params} from '@angular/router';
import {BigCompetitionAPIService} from '../../service/big-competition.api.service';
import {Observable} from 'rxjs/Observable';
import {AppConstants} from '@app/app.constants';
import {TableColumn} from '@app/client/private/models/table.column.model';
import {Order} from '@app/client/private/models/order.model';

@Component({
  selector: 'competition-modules-list',
  templateUrl: './competition-modules-list.component.html',
  styleUrls: ['./competition-modules-list.component.scss']
})
export class CompetitionModulesListComponent implements OnInit {
  @Input() modulesList: CompetitionModule[] = [];
  @Input() container: string;
  public searchField: string = '';
  public filterProperties: string[] = [
    'name'
  ];
  public dataTableColumns: Array<TableColumn> = [
    {
      name: 'Name',
      property: 'name',
      link: {
        hrefProperty: 'id',
        path: 'module/'
      },
      type: 'link'
    },
    {
      name: 'Type',
      property: 'type'
    },
    {
      name: 'Enabled',
      property: 'enabled',
      type: 'boolean'
    }
  ];
  constructor(
    public snackBar: MatSnackBar,
    private dialogService: DialogService,
    private dialog: MatDialog,
    private activatedRoute: ActivatedRoute,
    private bigCompetitionApiService: BigCompetitionAPIService
  ) { }

  ngOnInit(): void {
  }

  createModule(): void {
    const dialogRef = this.dialog
      .open(CompetitionModuleAddComponent, { width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH });
    dialogRef.afterClosed().subscribe(newModule => {
      if (newModule) {
        this.activatedRoute.params.subscribe((params: Params) => {
          this.saveNewModule(newModule, params)
            .map((competitionModule: HttpResponse<CompetitionModule>) => {
              return competitionModule.body;
            })
            .subscribe((competitionModule: CompetitionModule) => {
              if (competitionModule) {
                this.modulesList.push(competitionModule);
                this.dialogService.showNotificationDialog({
                  title: 'Save complete.',
                  message: 'Competition Module Created and Stored'
                });
              }
            });
        });
      }
    });
  }

  saveNewModule(module: CompetitionModule, params: Params): Observable<HttpResponse<CompetitionModule>> {
    if (this.container === 'tab') {
      return this.bigCompetitionApiService.createTabModule(params.competitionId, params.tabId, module);
    } else {
      return this.bigCompetitionApiService.createSubTabModule(params.competitionId, params.tabId, params.subTabId, module);
    }
  }

  removeModule(module: CompetitionModule): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Module',
      message: `Are You Sure You Want to Delete Module '${module.name}'?`,
      yesCallback: () => {
        this.activatedRoute.params.subscribe((params: Params) => {
          this.bigCompetitionApiService.deleteModule(params.competitionId, params.tabId, params.subTabId, module.id)
            .subscribe((data: any) => {
              this.modulesList.splice(this.modulesList.indexOf(module), 1);
              this.dialogService.showNotificationDialog({
                title: 'Remove Completed',
                message: 'Competition Module is Removed'
              });
            });
        });
      }
    });
  }

  reorderHandler(newOrder: Order): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.saveNewOrder(params, newOrder)
        .subscribe(() => {
          this.snackBar.open('Modules Order Saved!', 'Ok!', {
            duration: AppConstants.HIDE_DURATION
          });
        });
    });
  }

  saveNewOrder(params: Params, newOrder: Order): Observable<HttpResponse<CompetitionModule>> {
    if (this.container === 'tab') {
      return this.bigCompetitionApiService.postNewTabModulesOrder(params.competitionId, params.tabId, newOrder);
    } else {
      return this.bigCompetitionApiService.postNewSubTabModulesOrder(params.competitionId, params.tabId, params.subTabId, newOrder);
    }
  }
}
