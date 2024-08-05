import { Component, OnInit, ViewChild } from "@angular/core";
import { FormControl, Validators } from "@angular/forms";
import { ActivatedRoute, Params, Router } from "@angular/router";
import { Breadcrumb } from "@app/client/private/models";
import { HomeInplayModule } from "@app/client/private/models/inplaySportModule.model";
import { ISegmentModel } from "@app/client/private/models/segment.model";
import { GlobalLoaderService } from "@app/shared/globalLoader/loader.service";
import { CSPSegmentLSConstants } from "@root/app/app.constants";
import { SegmentStoreService } from "@root/app/client/private/services/segment-store.service";
import { DialogService } from "@root/app/shared/dialog/dialog.service";

import { SportsModulesBreadcrumbsService } from "../../sports-modules-breadcrumbs.service";
import { SportsModulesService } from "../../sports-modules.service";

@Component({
    selector: 'app-inplay-sport-edit',
    templateUrl: './inplay-sport-edit.component.html',
    styleUrls: ['./inplay-sport-edit.component.scss']
  })
export class InplaySportEditComponent implements OnInit {
    eventCount: FormControl;
    routeParams: Params;
    isSegmentValid: boolean = false;
    public breadcrumbsData: Breadcrumb[];
    public inplaySport: HomeInplayModule;
    public segmentsList: ISegmentModel;
    public isRevert: boolean = false;

    @ViewChild('inplayActionButtons') inplayActionButtons;

    constructor(
        private router: Router,
        private activatedRoute: ActivatedRoute,
        private sportsModulesBreadcrumbsService: SportsModulesBreadcrumbsService,
        private sportsModulesService: SportsModulesService,
        private globalLoaderService: GlobalLoaderService,
        private segmentStoreService: SegmentStoreService,
        private dialogService: DialogService) {
        this.validationHandler = this.validationHandler.bind(this);
        this.eventCount = new FormControl('', [Validators.required]);
    }

    ngOnInit(): void {
        this.activatedRoute.params.subscribe((params: Params) => {
        this.routeParams = params;
        this.loadInitialData();
        });
    }

    /*
     * Handles logic for child emitted data. 
    */
    modifiedSegmentsHandler(segmentConfigData: ISegmentModel): void {
      this.inplaySport = { ...this.inplaySport, ...segmentConfigData };
    }

    remove(): void {
        this.globalLoaderService.showLoader();
        this.sportsModulesService.deleteSportById(this.inplaySport.id).subscribe(() => {
            this.globalLoaderService.hideLoader();
            this.router.navigate([this.getUrlToGoBack]);
        }, error => {
            this.globalLoaderService.hideLoader();
        });
    }

    save(): void {
      this.globalLoaderService.showLoader();
      this.sportsModulesService.updateNewInplaySport(this.inplaySport)
        .subscribe((data: HomeInplayModule) => {
          const self = this;
          this.inplaySport = data;
          this.inplayActionButtons.extendCollection(this.inplaySport);
          this.segmentStoreService.setSegmentValue(this.inplaySport, CSPSegmentLSConstants.INPLAY_SPORTS_MODULE);
          this.dialogService.showNotificationDialog({
            title: 'Inplay Sports Module',
            message: 'Inplay Sports is Saved.',
            closeCallback() {
                self.router.navigate([self.getUrlToGoBack]);
            }
          });
          this.globalLoaderService.hideLoader();
        }, error => {
          this.globalLoaderService.hideLoader();
        });
    }

    revert(): void {
      this.loadInitialData();
      this.isRevert = true;
    }

    validationHandler(): boolean {
      return this.isSegmentValid && this.eventCount.valid && 
      this.inplaySport.eventCount > -1 && this.inplaySport.eventCount !== null;
    }

    /**
    * updates issegmentvalid true/false on child form changes
    */
    isSegmentFormValid(val: boolean): void {
      this.isSegmentValid = val;
    }

    public actionsHandler(event): void {
      switch (event) {
        case 'remove':
          this.remove();
          break;
        case 'save':
          this.save();
          break;
        case 'revert':
          this.revert();
          break;
        default:
          console.error('Unhandled Action');
          break;
      }
    }

    private get getUrlToGoBack(): string {
        return `sports-pages/homepage/sports-module/inplay/${this.routeParams['moduleId']}`;
    }

    private loadInitialData(): void {
        this.sportsModulesService.getInplaySportById(this.routeParams['linkId']).subscribe((sport: HomeInplayModule) => {
            this.inplaySport = sport;
            const title = sport.sportName;
            this.sportsModulesBreadcrumbsService.getBreadcrubs(this.routeParams, {
                customBreadcrumbs: [
                        {
                            label: title
                        }
                    ]
                }).subscribe((breadcrumbs: Breadcrumb[]) => {
                this.breadcrumbsData = breadcrumbs;

                this.segmentsList = {
                    exclusionList: this.inplaySport.exclusionList,
                    inclusionList: this.inplaySport.inclusionList,
                    universalSegment: this.inplaySport.universalSegment
                };
            });
        });
    }
}