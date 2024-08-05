import {Component, OnInit, ViewChild} from '@angular/core';
import {TimelineTemplate} from '@app/client/private/models/timelineTemplate.model';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {HttpResponse} from '@angular/common/http';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {TemplateApiService} from '@app/timeline/service/template-api.service';
import { AppConstants, Brand, TimeLine } from '@app/app.constants';
import {ImageLoaderService} from '@app/client/private/services/imageLoader/image-loader-service';
import {IImageData} from '@app/image-manager/model/image-manager.model';
import {SvgListComponent} from '@app/shared/svgList/svg-list.component';
import {TinymceComponent} from '@app/shared/tinymce/tinymce.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { BrandService } from '@app/client/private/services/brand.service';

@Component({
  selector: 'app-template-edit',
  templateUrl: './template-edit.component.html',
  styleUrls: ['./template-edit.component.scss']
})
export class TemplateEditComponent implements OnInit {
  public form: FormGroup;
  public breadcrumbsData: Breadcrumb[];
  template: TimelineTemplate;
  @ViewChild('actionButtons') actionButtons;
  @ViewChild('text') textEditor: TinymceComponent;
  @ViewChild('currentIcon') svgList: SvgListComponent;
  @ViewChild('currentHeaderIcon') svgListHeader: SvgListComponent;

  images: IImageData[];
  activePostIconImage: IImageData;
  activeHeaderIconImage: IImageData;
  showLeftSideLineTextName: string;
  isBrandLads:boolean = false;

  formFieldsModels = {};

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private templateApiService: TemplateApiService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private imageLoaderService: ImageLoaderService,
    private snackBar: MatSnackBar,
    private brandService: BrandService) {}

  ngOnInit() {
    this.isBrandLads = this.brandService.brand === Brand.LADBROKES;
    this.showLeftSideLineTextName = this.isBrandLads ? TimeLine.SHOW_LEFT_SIDE_RED_LINE_TEXT : TimeLine.SHOW_LEFT_SIDE_BLUE_LINE_TEXT;
    this.loadInitData();
  }

  loadInitData(): void {
    this.globalLoaderService.showLoader();

    this.activatedRoute.params.subscribe((params: Params) => {

      this.templateApiService.getTemplate(params['id'])
        .map((data: HttpResponse<TimelineTemplate>) => {
          return data.body;
        })
        .subscribe((template: TimelineTemplate) => {
          this.template = template;
          if (this.textEditor) {
            this.textEditor.update(this.template.text);
          }

          this.form = new FormGroup({
            name: new FormControl(this.template.name, [Validators.required]),
          });
          this.breadcrumbsData = [{
            label: `Templates`,
            url: `/timeline/template/`
          }, {
            label: this.template.name,
            url: `/timeline/template/${this.template.id}`
          }];

          this.initSvgImages();
          if (this.actionButtons) {
            this.actionButtons.extendCollection(this.template);
          }
          this.globalLoaderService.hideLoader();
        }, error => {
          console.error(error.message);
          this.globalLoaderService.hideLoader();
        });
    });
  }

  private initSvgImages() {
    this.imageLoaderService.getDataForBrandAndSprite('timeline')
      .subscribe(data => {
        this.images = data;
        if (this.template.postIconSvgId) {
          this.setPostIconSvg(this.template.postIconSvgId);
        }

        if (this.template.headerIconSvgId) {
          this.setHeaderIconSvg(this.template.headerIconSvgId);
        }
      });
  }

  save(): void {
    this.globalLoaderService.showLoader();
    this.templateApiService.updateTemplate(this.template)
      .map((data: HttpResponse<TimelineTemplate>) => {
        return data.body;
      })
      .subscribe((data: TimelineTemplate) => {
        this.template = data;
        this.actionButtons.extendCollection(this.template);
        this.dialogService.showNotificationDialog({
          title: 'Template',
          message: 'Template is Saved.'
        });
        this.globalLoaderService.hideLoader();
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  revert(): void {
    this.loadInitData();
  }

  remove(): void {
    this.templateApiService.deleteTemplate(this.template.id)
      .subscribe(() => {
        this.router.navigate(['/timeline/template/']);
      }, error => {
        console.error(error.message);
      });
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

  updateText(data) {
    this.template.text = data;
  }

  setPostIconSvg(postIconSvgId) {
    this.activePostIconImage = this.images.filter(image => image.svgId === postIconSvgId)[0];
    if (this.activePostIconImage && this.svgList) {
      this.svgList.reinitSvgElement(this.activePostIconImage.svg);
    }
    this.template.postIconSvgId = postIconSvgId;
  }

  setHeaderIconSvg(headerIconSvgId) {
    this.activeHeaderIconImage = this.images.filter(image => image.svgId === headerIconSvgId)[0];
    if (this.activeHeaderIconImage && this.svgListHeader) {
      this.svgListHeader.reinitSvgElement(this.activeHeaderIconImage.svg);
    }
    this.template.headerIconSvgId = headerIconSvgId;
  }

  uploadTrcImageHandler(file) {
    this.templateApiService.uploadImage(this.template.id, 'TOP_RIGHT_CORNER', file)
      .map((data: HttpResponse<TimelineTemplate>) => {
        return data.body;
      })
      .subscribe((data: TimelineTemplate) => {
        this.template.topRightCornerImage = data.topRightCornerImage;
        this.actionButtons.updateCollectionProperty(['topRightCornerImage'], data.topRightCornerImage);
        this.snackBar.open(`Image Uploaded And Attached To Template.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      }, () => {
        console.error('Error');
      });
  }

  removeTrcImageHandler() {
    this.templateApiService.deleteImage(this.template.id, 'TOP_RIGHT_CORNER')
      .map((data: HttpResponse<TimelineTemplate>) => {
        return data.body;
      })
      .subscribe((data: TimelineTemplate) => {
        this.template.topRightCornerImage = data.topRightCornerImage;
        this.actionButtons.updateCollectionProperty(['topRightCornerImage'], data.topRightCornerImage);
        this.snackBar.open(`Image Deleted And Detached From Template.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      }, () => {
        console.error('Error');
      });
  }

  removePostIconImage() {
    this.activePostIconImage = undefined;
    this.template.postIconSvgId = undefined;
  }

  removeHeaderIconImage() {
    this.activeHeaderIconImage = undefined;
    this.template.headerIconSvgId = undefined;
  }

  isModelValid(template) {
    return true;
  }
}
