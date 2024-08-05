import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {VirtualSportsService} from '@app/virtual-sports/virtual-sports.service';
import {HttpResponse} from '@angular/common/http';
import {AppConstants} from '@app/app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {VirtualSportParent} from '@app/client/private/models/virtualSportParent.model';
import { BrandService } from '@app/client/private/services/brand.service';

@Component({
  selector: 'app-parent-sports-edit',
  templateUrl: './parent-sports-edit.component.html',
  styleUrls: ['./parent-sports-edit.component.scss']
})
export class ParentSportsEditComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;

  id: string;
  parentSport: VirtualSportParent;
  initialTitle: string;
  getDataError: string;

  breadcrumbsData: Breadcrumb[];
  isIMActive: boolean;
  existIndexSport:string;
  existIndex:number;
  constructor(
    private virtualSportsService: VirtualSportsService,
    private dialogService: DialogService,
    private snackBar: MatSnackBar,
    private router: Router,
    private route: ActivatedRoute,
    private brandService: BrandService
    ) {
    this.isIMActive = this.brandService.isIMActive();
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.onRemoveClick();
        break;
      case 'save':
        this.saveParentVirtualSport();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.loadInitialData();
  }

  uploadImageHandler(file) {
    this.virtualSportsService.updateVirtualSportParent(this.parentSport)
      .subscribe(() => {
        this.virtualSportsService.uploadImage(this.parentSport.id, file)
          .map((data: HttpResponse<any>) => {
            return data.body;
          })
          .subscribe((data: any) => {
            this.parentSport = data;
            this.actionButtons.extendCollection(this.parentSport);
            this.snackBar.open(`Image Uploaded.`, 'Ok!', {
              duration: AppConstants.HIDE_DURATION,
            });
          }, () => {
            console.error('Error');
          });
      });
  }

  removeImageHandler() {
    this.virtualSportsService.updateVirtualSportParent(this.parentSport)
      .subscribe(() => {
        this.virtualSportsService.deleteImage(this.parentSport.id)
          .map((data: HttpResponse<any>) => {
            return data.body;
          })
          .subscribe((data: any) => {
            this.parentSport = data;
            this.actionButtons.extendCollection(this.parentSport);
            this.snackBar.open(`Image Deleted.`, 'Ok!', {
              duration: AppConstants.HIDE_DURATION,
            });
          }, () => {
            console.error('Error');
          });
      });
  }

  saveParentVirtualSport() {
    const {isTopSportIndexValid, ...defaultParentSport} = this.parentSport;
    this.parentSport = defaultParentSport;
    this.virtualSportsService.updateVirtualSportParent(this.parentSport)
      .subscribe(data => this.finishVirtualSportUpdate(data.body));
  }

  revertChanges() {
    this.loadInitialData();
  }

  isModelValid(parentSport: VirtualSportParent) {
    if (parentSport && parentSport.topSports) {
      return (parentSport.title.trim().length > 0) && parentSport.topSportsIndex <= 4 && parentSport.topSportsIndex > 0 && parentSport.isTopSportIndexValid;
    } else {
      return (parentSport) && (parentSport.title.trim().length > 0);
    }
  }

  onRemoveClick(): void {
    this.virtualSportsService.deleteVirtualSportParent(this.parentSport.id)
      .subscribe((data: any) => {
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Sport is Removed.'
        });
        this.router.navigate(['/virtual-hub/virtual-sports']);
      });
  }

  private loadInitialData(): void {
    this.virtualSportsService.getVirtualSportParent(this.id).subscribe((resp: any) => {
      this.parentSport = resp.body;
      this.initialTitle = this.parentSport.title;
      this.parentSport.isTopSportIndexValid = true;
      this.actionButtons.extendCollection(this.parentSport);
      this.breadcrumbsData = [{
        label: `Virtual sports`,
        url: `/virtual-hub/virtual-sports`
      }, {
        label: this.parentSport.title,
        url: `/virtual-hub/virtual-sports/${this.parentSport.id}`
      }];
    }, error => {
      this.getDataError = error.message;
    });
  }

  private finishVirtualSportUpdate(updatedParentSport): void {
    this.parentSport = updatedParentSport;
    this.initialTitle = this.parentSport.title;
    this.actionButtons.extendCollection(this.parentSport);
    this.loadInitialData();

    this.snackBar.open('Save Completed', 'Virtual Sport is Updated', {
      duration: AppConstants.HIDE_DURATION,
    });
  }

  onTopSportsChange(parentSport) {
    this.parentSport.topSports = !this.parentSport.topSports;
    this.onTopSportsIndexChange(parentSport);
  }

  onTopSportsIndexChange(parentSport): void {
    this.existIndexSport = null;
    if (!parentSport.topSportsIndex) {
      parentSport.topSportsIndex = 0;
    } else {
      const virtualsData = this.virtualSportsService.getSavedvirtualSports();
      if (virtualsData) {
        let duplicateSport = virtualsData.find(sport => sport.topSportsIndex == parentSport.topSportsIndex && sport.topSports);
        if (duplicateSport && this.initialTitle != duplicateSport.title) {
          parentSport.isTopSportIndexValid = false;
          this.existIndex = duplicateSport.topSportsIndex;
          this.existIndexSport = duplicateSport.title;
        } else {
          parentSport.isTopSportIndexValid = true;
          this.existIndexSport = null;
        }
      }
    }
  }
}
