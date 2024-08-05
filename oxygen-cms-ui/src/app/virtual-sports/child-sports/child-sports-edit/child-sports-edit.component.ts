import {Component, OnInit, ViewChild} from '@angular/core';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {ActivatedRoute, Router} from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import {RemoveImageRequest, RemoveImageRequestType, VirtualSportChild} from '@app/client/private/models/virtualSportChild.model';
import {VirtualSportsChildService} from '@app/virtual-sports/virtual-sports-child.service';
import {VirtualSportsService} from '@app/virtual-sports/virtual-sports.service';
import {VirtualSportParent} from '@app/client/private/models/virtualSportParent.model';
import {HttpResponse} from '@angular/common/http';
import {AppConstants} from '@app/app.constants';

import * as _ from 'lodash';
import {EventDialogComponent} from '@app/virtual-sports/child-sports/event-dialog.component';

@Component({
  selector: 'app-child-sports-edit',
  templateUrl: './child-sports-edit.component.html',
  styleUrls: ['./child-sports-edit.component.scss']
})
export class ChildSportsEditComponent implements OnInit {
  _: any = _;

  id: string;
  initialTitle: string;
  childSport: VirtualSportChild;
  parentSport: VirtualSportParent;
  getDataError: string;

  @ViewChild('actionButtons') actionButtons;
  breadcrumbsData: Breadcrumb[];

  maxFileSizeKb: number = 5;

  removeImageTypes = {
    allForEvent: RemoveImageRequestType[RemoveImageRequestType.ALL_FOR_EVENT],
    singleForEvent: RemoveImageRequestType[RemoveImageRequestType.SINGLE_FOR_EVENT],
    singleForChild: RemoveImageRequestType[RemoveImageRequestType.SINGLE_FOR_TRACK]
  };

  constructor(
    private childSportsService: VirtualSportsChildService,
    private parentSportsService: VirtualSportsService,
    private dialogService: DialogService,
    private snackBar: MatSnackBar,
    private router: Router,
    private route: ActivatedRoute,
    private dialog: MatDialog) {
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('childSportId');
    this.loadInitialData();
  }

  get cmsUploadImageMsg(): string {
    return `Upload Runner Image (.png, max ${this.maxFileSizeKb}KB) here:`;
  }

  private loadInitialData(): void {
    this.childSportsService.getVirtualSportChild(this.id).subscribe((resp: HttpResponse<VirtualSportChild>) => {
      this.childSport = resp.body;
      this.initialTitle = this.childSport.title;
      this.childSport.eventRunnerImages = this.childSport.eventRunnerImages || {};
      this.actionButtons.extendCollection(this.childSport);
      this.parentSportsService.getVirtualSportParent(this.childSport.sportId).subscribe((parentResp: any) => {
        this.parentSport = parentResp.body;
        this.resetBreadcrumb();
      });
    }, error => {
      this.getDataError = error.message;
    });
  }

  private revertChanges() {
    this.loadInitialData();
  }

  private resetBreadcrumb() {
    this.breadcrumbsData = [{
      label: `Virtual sports`,
      url: `/virtual-hub/virtual-sports`
    }, {
      label: `${this.parentSport.title}`,
      url: `/virtual-hub/virtual-sports/${this.parentSport.id}`
    }, {
      label: this.childSport.title,
      url: `/virtual-hub/virtual-sports/child-sport/${this.childSport.id}`
    }];

  }

  saveChildVirtualSport() {
    this.childSportsService.updateVirtualSportChild(this.childSport)
      .subscribe(data => {
        this.finishUpdate(data.body);
      }, error => {
        this.dialogService.showNotificationDialog({
          title: 'Virtual child sport not saved',
          message: `Couldn\'t save virtual child sport: ${error.message}. Details: ${JSON.stringify(error.error)}`
        });
      });
  }

  finishUpdate(updatedChildSport): void {
    this.childSport = updatedChildSport;
    this.initialTitle = updatedChildSport.title;
    this.actionButtons.extendCollection(this.childSport);

    this.snackBar.open('Save Completed', 'Virtual Child Sport is Updated', {
      duration: AppConstants.HIDE_DURATION,
    });
  }

  checkModelValid(childSport: VirtualSportChild) {
    const nameValid: boolean = childSport && childSport.title && childSport.title.trim().length > 0;
    const classIdValid: boolean = childSport && childSport.classId && childSport.classId.trim().length > 0;
    const eventNumber = childSport && childSport.numberOfEvents;
    const eventNumberValid: boolean = (eventNumber && eventNumber > 0);

    return nameValid && classIdValid && eventNumberValid;
  }

  onRemoveClick(): void {
    this.childSportsService.deleteVirtualSportChild(this.childSport.id)
      .subscribe((data: any) => {
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Child Sport is Removed.'
        });
        this.router.navigate([`/virtual-hub/virtual-sports/${this.parentSport.id}`]);
      });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.onRemoveClick();
        break;
      case 'save':
        this.saveChildVirtualSport();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  uploadImageHandler(file, event?: string) {
    for (const fileInfo of file.values()) {
      if (!(/^\d+\.png$/.test(fileInfo.name))) {
        this.showImageNotValidAlert('Please Use Numerical Characters Only');
        return;
      }
    }

    this.childSportsService.uploadImage(this.childSport.id, file, event)
      .map((data: HttpResponse<VirtualSportChild>) => {
        return data.body;
      })
      .subscribe((data: VirtualSportChild) => {
        this.childSport = _.extend(data);
        this.actionButtons.extendCollection(this.childSport);
        this.snackBar.open(`Image Uploaded.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      }, (error) => {
        this.dialogService.showNotificationDialog({
          title: 'Image wasn\'t uploaded',
          message: `Error occurred while uploading image: ${JSON.stringify(error)}`
        });
      });
  }

  handleImageRemoving(removeImageRequest?: RemoveImageRequest) {
    this.childSportsService.removeImage(this.childSport.id, removeImageRequest)
      .map((data: HttpResponse<VirtualSportChild>) => {
        return data.body;
      })
      .subscribe((data: VirtualSportChild) => {
        this.childSport = _.extend(data);
        this.actionButtons.extendCollection(this.childSport);
        this.snackBar.open(`Image Deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      }, () => {
        console.error('Error');
      });
  }

  showImageNotValidAlert(reasonMsg: string) {
    this.dialogService.showNotificationDialog({
      title: 'Image can\'t be uploaded',
      message: `Image Discarded As It Is Not Valid: ${reasonMsg}`
    });
  }

  addEventForImages() {
    const dialogRef = this.dialog.open(EventDialogComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH
    });

    dialogRef.afterClosed().subscribe(event => {
      if (!_.isEmpty(event)) {
        this.childSport.eventRunnerImages[event] = [];
      }
    });
  }

  removeEventImages($event, event: string) {
    $event.stopPropagation();

    this.dialogService.showConfirmDialog({
      title: 'Confirm Event Images Removal',
      message: `You are going to remove all previously uploaded images for '${event}' Event. Are you sure?`,
      yesCallback: () => {
        this.handleImageRemoving({event: event, type: this.removeImageTypes.allForEvent});
      }
    });
  }
}
