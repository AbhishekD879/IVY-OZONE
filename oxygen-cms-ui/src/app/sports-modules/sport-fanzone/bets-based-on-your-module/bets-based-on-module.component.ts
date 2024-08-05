import { Component, OnInit, ViewChild } from '@angular/core';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { ActivatedRoute, Params } from '@angular/router';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { AppConstants } from '@app/app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'bets-based-on-module',
  templateUrl: './bets-based-on-module.component.html',
 })


export class BetsbasedonmoduleComponent implements OnInit {
    @ViewChild('actionButtons') actionButtons;
    public form: FormGroup;
    public moduleData: SportsModule;
    public breadcrumbsData: Breadcrumb[];
    public routeParams: Params;
   
  
    constructor(
      private activatedRoute: ActivatedRoute,
      private sportsModulesService: SportsModulesService,
      private sportsModulesBreadcrumbsService: SportsModulesBreadcrumbsService,
      private snackBar: MatSnackBar
    ) {
  
    }
  /**
   * ngOninit call the data when component initalized
   */
    public ngOnInit(): void {
      this.activatedRoute.params.subscribe((params: Params) => {
        this.routeParams = params;
        this.loadInitialData(params);
      });
    }

    /**
     * it loads the initial data to the component
     * @param params i
     */
    public loadInitialData(params: Params): void {
      this.sportsModulesService.getSingleModuleData(params['moduleId'], params['id'])
        .subscribe((moduleData: [SportsModule, SportCategory]) => {
          this.moduleData = moduleData[0];
          if(!moduleData[0].teamAndFansBetsConfig){
            this.moduleData.teamAndFansBetsConfig = {noOfMaxSelections : 0};
          }
          this.form = new FormGroup({
            title: new FormControl(this.moduleData.title ||'',[Validators.required,Validators.maxLength(50)]),
            moduleType :  new FormControl({value: this.moduleData.moduleType ||'', disabled: true}),
            noOfMaxSelections: new FormControl(this.moduleData.teamAndFansBetsConfig.noOfMaxSelections || 0, [Validators.required,Validators.min(1),Validators.pattern(/^(\d*)$/)]),
            enableBackedTimes : new FormControl(this.moduleData.teamAndFansBetsConfig.enableBackedTimes || true)
          });
           this.sportsModulesBreadcrumbsService.getBreadcrubs(params, {
            module: this.moduleData
          }).subscribe((breadcrubs: Breadcrumb[]) => {
            this.breadcrumbsData = breadcrubs;
           });
        });     
    }

    /**
     * it sends the data to api
     */
    public saveChanges() {
      // this.module.enabled = !this.module.disabled;
      this.sportsModulesService.updateModule(this.moduleData)
        .subscribe((module: SportsModule) => {
          this.moduleData = module;
          this.actionButtons.extendCollection(this.moduleData);
          this.snackBar.open(`Sports module saved!`, 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        });
    }
  /**
   * Based on the event it triggers the saveChanges method or loadInitialData
   * @param event 
   */
    public actionsHandler(event: string): void {
      switch (event) {
        case 'save':
          this.saveChanges();
          break;
        case 'revert':
          this.loadInitialData(this.routeParams);
          break;
        default:
          console.error('Unhandled Action');
          break;
      }
    }
  }
