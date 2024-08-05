import { Component, OnInit, ViewChild } from '@angular/core';
import { Location } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { NgForm } from '@angular/forms';
import { of } from 'rxjs/observable/of';
import { Observable } from 'rxjs/Observable';
import { map, switchMap } from 'rxjs/operators';

import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import {
  IMAGE_MANAGER_FORM_ERRORS, IMAGE_MANAGER_ROUTES, IMAGE_MANAGER_FORM_NOTES, IMAGE_MANAGER_MAX_FILE_SIZE, IMAGE_MANAGER_SVG_ID_PATTERN
} from '@app/image-manager/constants/image-manager.constant';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ImageManagerService } from '@app/image-manager/services/image-manager.service';
import { IImageData } from '@app/image-manager/model/image-manager.model';

@Component({
  selector: 'img-details-page',
  templateUrl: './details-page.component.html',
  styleUrls: ['./details-page.component.scss']
})
export class DetailsPageComponent implements OnInit {
  @ViewChild('imageForm') imageForm: NgForm;

  appSprites: string[];
  formNotes: {[key: string]: string};
  errors: {[key: string]: string};
  breadcrumbsData: Breadcrumb[];
  image: IImageData;
  svgFragmentId: string; // preview version of svgId
  file: File;
  idPattern: string;

  private _isLoading: boolean = true;
  set isLoading(value: boolean) {
    this._isLoading = value;

    if (value) {
      this.globalLoaderService.showLoader();
    } else {
      this.globalLoaderService.hideLoader();
    }
  }
  get isLoading(): boolean {
    return this._isLoading;
  }

  constructor(
    private activatedRoute: ActivatedRoute,
    private locationService: Location,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private imageManagerService: ImageManagerService,
    private router: Router
  ) {
    this.formNotes = IMAGE_MANAGER_FORM_NOTES;
    this.errors = IMAGE_MANAGER_FORM_ERRORS;
    this.idPattern = IMAGE_MANAGER_SVG_ID_PATTERN;
  }

  ngOnInit() {
    this.isLoading = true;

    this.imageManagerService.getSpriteList().pipe(
      map((spriteList: string[]) => {
        if (!(spriteList && spriteList.length)) {
          console.error('Error. Unable to get list of app sprites.');
          return;
        }

        this.appSprites = spriteList;
      }),
      switchMap(() => {
        const internalId = this.activatedRoute.snapshot.paramMap.get('id');
        return this.getOrCreateImage(internalId);
      })
    ).subscribe((imageData: IImageData) => {
      this.image = imageData;
      this.svgFragmentId = '#' + imageData.svgId;

      this.buildBreadcrumbs();
      this.isLoading = false;
    });
  }

  /**
   * Get existing image data, or ini new image in order to add one
   *
   * @param id
   */
  getOrCreateImage(id: string): Observable<IImageData> {
    if (id) {
      return this.imageManagerService.getSingleImage(id);
    }

    const
      defaultSpriteName = this.appSprites.includes('additional') ? 'additional' : this.appSprites[this.appSprites.length - 1],
      newImageData = {
        id: '',
        svgId: '',
        active: true,
        sprite: defaultSpriteName,
        svgFilename: {
          originalname: ''
        }
      };

    return of(newImageData as IImageData);
  }

  /**
   * Build data for page breadcrumbs
   */
  buildBreadcrumbs(): void {
    this.breadcrumbsData = [{
      label: `image manager`,
      url: IMAGE_MANAGER_ROUTES.base
    }, {
      label: this.image.svgId || 'new image',
      url: `${this.locationService.path()}`
    }];
  }

  /**
   * Run file type and size validations,
   *  update related file fields
   *
   * @param event
   */
  validateAndUpdateFileFields(event): void {
    const file = event.target.files[0];

    if (!file) { return; } // webkit could trigger another change event when canceling file selecting

    const fileType = file.type;
    const supportedTypes = ['image/svg', 'image/svg+xml'];

    if (!supportedTypes.includes(fileType)) {
      this.dialogService.showNotificationDialog({
        title: `Error. Unsupported file type.`,
        message: `Supported 'svg' files only.`
      });
      this.image.svgFilename.originalname = '';
      this.file = null;
    } else {
      this.file = file;
      this.image.svgFilename.originalname = file.name;

      if (!this.image.svgId) {
        this.image.svgId = this.transformName(file.name);
      }

      this.validateFileSize(file);
    }
  }

  /**
   * Check file size and add error to form
   *
   * @param file
   */
  validateFileSize(file: File): void {
    if (!(file && file.size)) { return; }

    if (file.size > IMAGE_MANAGER_MAX_FILE_SIZE) {
      setTimeout(() => {
        this.imageForm.controls.originalname.setErrors({'size': true});
      });
    }
  }

  /**
   * Handle bottom buttons actions
   *
   * @param eventName
   */
  actionsHandler(eventName: string): void {
    switch (eventName) {
      case 'remove':
        this.imageManagerService.deleteAndOpenList(this.image.id);
        break;
      case 'save':
        this.submitImageForm();
        break;
      case 'revert':
        this.ngOnInit();
        break;
      default:
        console.error('Unhandled Action');
    }
  }

  /**
   * Apply transformations to given file name (should go in sync with template validation):
   *  remove fileType,
   *  remove indents and hash-tag,
   *  make lowercase
   *
   * @param value
   */
  transformName(value: string): string {
    const noFileTypeName = value.includes('.') ? value.slice(0, value.lastIndexOf('.')) : value;
    return noFileTypeName.toLowerCase().replace(/#/g, '').replace(/\s/g, '');
  }

  /**
   * Send image data [and file] while adding new or updating existing image
   */
  submitImageForm(): void {
    const imageFormData = this.imageForm.value;
    const formData = new FormData();

    Object.keys(imageFormData).forEach((key: string) => {
      formData.append(key, imageFormData[key]);
    });

    if (this.file) {
       formData.append('file', this.file);
    }

    this.imageManagerService.sendImageData(this.image.id, formData).subscribe((newImageId: string) => {
      this.successfulSaveCallback(newImageId);
    });
  }

  /**
   * Show successful save message and:
   *  (new image) go to image details page
   *  (update image) reload component to get actual data
   *
   * @param imageId
   */
  successfulSaveCallback(imageId: string): void {
    this.dialogService.showNotificationDialog({
      title: 'Image save completed.',
      message: `Changes will be reflected in "${this.image.sprite}" sprite.`,
      closeCallback: () => {
        if (imageId !== this.image.id) {
          this.router.navigate([`${IMAGE_MANAGER_ROUTES.base}/${IMAGE_MANAGER_ROUTES.details.replace(':id', imageId)}`]);
        } else {
          this.ngOnInit();
        }
      }
    });
  }
}
