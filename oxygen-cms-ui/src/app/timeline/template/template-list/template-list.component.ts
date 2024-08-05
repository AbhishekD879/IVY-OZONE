import { Component, OnInit } from '@angular/core';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {Router} from '@angular/router';
import {TemplateApiService} from '@app/timeline/service/template-api.service';
import {TimelineTemplate} from '@app/client/private/models/timelineTemplate.model';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {AppConstants} from '@app/app.constants';
import {TemplateCreateComponent} from '@app/timeline/template/template-create/template-create.component';
import {forkJoin} from 'rxjs/observable/forkJoin';
import * as _ from 'lodash';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-template-list',
  templateUrl: './template-list.component.html',
  styleUrls: []
})
export class TemplateListComponent implements OnInit {

  templateData: Array<TimelineTemplate>;
  searchField: string = '';
  getDataError: string;
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Template Name',
      property: 'name',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Modified By',
      property: 'updatedByUserName'
    },
    {
      name: 'Date Created',
      property: 'createdAt',
      type: 'date'
    }
  ];

  filterProperties: Array<string> = [
    'name',
    'updatedByUserName',
    'createdAt'
  ];

  constructor(private dialog: MatDialog,
              private dialogService: DialogService,
              private templateApiService: TemplateApiService,
              private globalLoaderService: GlobalLoaderService,
              private router: Router) { }

  ngOnInit() {
    this.loadTemplates();
  }

  loadTemplates() {
    this.templateApiService.getTemplatesByBrand()
      .subscribe((data: any) => {
        this.templateData = data.body;
      }, error => {
        this.getDataError = error.message;
      });
  }

  createTemplate() {
    const dialogRef = this.dialog.open(TemplateCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {}
    });

    dialogRef.afterClosed().subscribe(template => {
      if (template) {
        this.templateApiService.createTemplate(template)
          .subscribe(response => {
            if (response) {
              this.templateData.push(template);
              this.router.navigate([`/timeline/template/${response.body.id}`]);
            }
          });
      }
    });
  }

  removeTemplate(template: TimelineTemplate) {
    this.dialogService.showConfirmDialog({
      title: 'Remove Template',
      message: 'This action will permanently remove the template. Are you sure?',
      yesCallback: () => {
        this.sendRemoveRequest(template);
      }
    });
  }

  sendRemoveRequest(template: TimelineTemplate) {
    this.templateApiService.deleteTemplate(template.id)
      .subscribe((data: any) => {
        this.templateData.splice(this.templateData.indexOf(template), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Template is Removed.'
        });
      });
  }

  removeHandlerMulty(templateIds: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Template (${templateIds.length})`,
      message: 'This will permanently remove the templates. Are you sure?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        forkJoin(templateIds.map(id => this.templateApiService.deleteTemplate(id)))
          .subscribe(() => {
            templateIds.forEach((id) => {
              const index = _.findIndex(this.templateData, {id: id});
              this.templateData.splice(index, 1);
            });
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

}
