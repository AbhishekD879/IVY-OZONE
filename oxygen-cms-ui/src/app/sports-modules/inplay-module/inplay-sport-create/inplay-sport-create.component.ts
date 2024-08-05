import { Component, OnInit, ViewChild } from "@angular/core";
import { ISegmentModel } from "@app/client/private/models/segment.model";
import { HomeInplayModule, InplaySports } from "@app/client/private/models/inplaySportModule.model";
import { SportsModulesService } from "../../sports-modules.service";
import { BrandService } from "@app/client/private/services/brand.service";
import { ConfirmDialogComponent } from "@app/shared/dialog/confirm-dialog/confirm-dialog.component";
import { MatDialogRef } from "@angular/material/dialog";
import { GlobalLoaderService } from "@root/app/shared/globalLoader/loader.service";
import { CmsAlertComponent } from "@root/app/shared/cms-alert/cms-alert.component";
import { FormControl, Validators } from "@angular/forms";

@Component({
    selector: 'app-inplay-sport-create',
    templateUrl: './inplay-sport-create.component.html',
    styleUrls: ['./inplay-sport-create.component.scss']
  })
export class InplaySportCreateComponent implements OnInit {
    eventCount: FormControl;
    segmentsList: ISegmentModel;
    sportsList: InplaySports[] = [];
    isSegmentValid: boolean = false;
    inplaySport: HomeInplayModule = {
        id: '0',
        eventCount: null,
        categoryId: '',
        tier: '',
        sportName: '',
        brand: this.brandService.brand,
        updatedBy: null,
        updatedAt: null,
        createdBy: null,
        createdAt: null,
        updatedByUserName: null,
        createdByUserName: null,
        inclusionList: [],
        exclusionList: [],
        universalSegment: true
    };
    @ViewChild('requestError') private requestError: CmsAlertComponent;
    
    constructor(private sportsModulesService: SportsModulesService,
        private brandService: BrandService,
        private dialogRef: MatDialogRef<ConfirmDialogComponent>,
        private globalLoaderService: GlobalLoaderService
    )   {
        this.eventCount = new FormControl('', [Validators.required]);
    } 

    ngOnInit(): void {
        this.segmentsList = {
            inclusionList: [],
            exclusionList: [],
            universalSegment: true
        };

        this.sportsModulesService.getAllSportNames().subscribe((sports) => {
            this.sportsList = sports;
        });
    }

    closeDialog(): void {
      this.dialogRef.close();
    }

    isSegmentFormValid(val: boolean): void {
      this.isSegmentValid = val;
    }

    isEventCountValid(): boolean {
        return this.inplaySport.eventCount !== null && this.inplaySport.eventCount > -1 && this.eventCount.valid;
    }

    createInplaySport(): void {
        this.globalLoaderService.showLoader();
        this.sportsModulesService.saveNewInplaySport(this.inplaySport).subscribe((savedinplaySport: HomeInplayModule) => {
          this.globalLoaderService.hideLoader();
          this.dialogRef.close(savedinplaySport);
        }, (errorMsg) => {
          this.globalLoaderService.hideLoader();
          this.requestError.showError(errorMsg.error);
        });
    }

    onSportsChange(sportName: string): void {
        if(sportName){
            const selectedSport = this.sportsList.find((sport) => sport.sportName === sportName);
            this.inplaySport.sportName = sportName;
            this.inplaySport.categoryId = selectedSport.categoryId.toString();
            this.inplaySport.tier = selectedSport.sportTier;
        }
    }

    /*
     * Handles logic for child emitted data. 
    */
    modifiedSegmentsHandler(segmentConfigData: ISegmentModel): void {
      this.inplaySport = { ...this.inplaySport, ...segmentConfigData };
    }
}