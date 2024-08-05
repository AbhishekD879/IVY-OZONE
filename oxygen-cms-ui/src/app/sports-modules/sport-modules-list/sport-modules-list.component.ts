import { Component, Input, OnInit } from '@angular/core';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';
import { Order } from '@app/client/private/models/order.model';
import { AppConstants } from '@app/app.constants';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { CreateSportModuleComponent } from '@app/sports-modules/create-sport-module/create-sport-module.component';
import { ISportModuleType } from '@app/client/private/models/sport-modules/sport-module.model';
import { sportModuleTypes } from '@app/sports-modules/constant/module-types.constant';
import * as _ from 'lodash';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ErrorService } from '@app/client/private/services/error.service';

@Component({
  selector: 'sport-modules-list',
  templateUrl: 'sport-modules-list.component.html'
})
export class SportModulesListComponent implements OnInit {
  @Input() hubIndex: number;
  @Input() pageId: number;

  sportModuleTypes: ISportModuleType[] = sportModuleTypes;
  isAddModuleAvailable: boolean; // could not add more than one module of each type
  sportModules: Array<SportsModule> = [];
  getDataError: string;
  searchField: string = '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Module',
      property: 'title',
      link: {
        hrefProperty: 'href'
      },
      type: 'link',
      width: 2
    },
    {
      name: 'Enabled',
      property: 'disabled',
      type: 'boolean',
      isReversed: true,
      width: 1
    }
  ];

  constructor(
    public snackBar: MatSnackBar,
    private sportsModulesService: SportsModulesService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private errorService: ErrorService
  ) {
  }

  ngOnInit(): void {
    this.sportModules = [];

    // call modules for EventHub
    if (this.hubIndex) {
      this.sportsModulesService.getModulesData('eventhub', this.hubIndex)
        .subscribe((modules: SportsModule[]) => {
          this.sportModules = this.sportsModulesService.addModulesHref(modules);
          this.isAddModuleAvailable = this.sportModules.length < this.sportModuleTypes.length;
        });
    } else {
      // Call madules for other sports pages
      // TODO need to replace current modules list on sports pages with this component to use this approach
      this.sportsModulesService.getModulesData('sport', this.pageId)
        .subscribe((modules) => {
          this.sportModules = modules;
        });
    }
  }

  reorderHandler(newOrder: Order): void {
    this.sportsModulesService.updateModulesOrder(newOrder)
      .subscribe((data: any) => {
        this.snackBar.open('New Modules Order Saved!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  addModule(): void {
    this.dialogService.showCustomDialog(CreateSportModuleComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add Sport Mmodule',
      yesOption: 'Save',
      noOption: 'Cancel',
      data: {
        sportModules: this.sportModules
      },
      yesCallback: (moduleName: string) => {
        this.sportsModulesService.createHubModuleByName(moduleName, this.hubIndex.toString())
          .subscribe((moduleData: SportsModule) => {
            this.sportModules.push(moduleData);
            this.isAddModuleAvailable = this.sportModules.length < this.sportModuleTypes.length;

            this.sportModules = this.sportsModulesService.addModulesHref(this.sportModules);
          });
      }
    });
  }

  deleteHandler(module: SportsModule): void {
    this.dialogService.showConfirmDialog({
      title: 'Sport module Delete',
      message: `Are You Sure You Want to Remove module ${module.title}?`,
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.sportsModulesService.removeModule(module)
          .subscribe(() => {
            _.remove(this.sportModules, { id: module.id });
            this.isAddModuleAvailable = this.sportModules.length < this.sportModuleTypes.length;

            this.globalLoaderService.hideLoader();
          }, error => {
            this.errorService.emitError(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }
}
