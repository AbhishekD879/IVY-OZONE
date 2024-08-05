import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {DialogService} from '../../../../shared/dialog/dialog.service';
import {OlympicsAPIService} from '../../service/olympics.api.service';
import {DefaultTabVariants, TemplateType1Variants} from '../../models/enums';
import {Sport} from '../../../../client/private/models/sport.model';
import {HttpResponse} from '@angular/common/http';
import {Breadcrumb} from '../../../../client/private/models/breadcrumb.model';
import {AppConstants} from '../../../../app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import * as _ from 'lodash';

@Component({
  selector: 'single-olympics-page',
  templateUrl: './olympics.page.component.html',
  styleUrls: ['./olympics.page.component.scss']
})

export class SingleOlympicsPageComponent implements OnInit {
  olympicsPage: Sport;
  id: string;
  public breadcrumbsData: Breadcrumb[];

  templateType1Variants: Array<string> = Object.keys(TemplateType1Variants);
  defaultTabVariants: Array<string> = Object.keys(DefaultTabVariants);
  variantsEnum1: any = TemplateType1Variants;
  variantsEnum2: any = DefaultTabVariants;
  @ViewChild('actionButtons') actionButtons;

  constructor(
    public snackBar: MatSnackBar,
    private dialogService: DialogService,
    private route: ActivatedRoute,
    private router: Router,
    private olympicsAPIService: OlympicsAPIService
  ) {}

  /**
   * Load olympicsPage data from server.
   */
  loadInitialData(): void {
    // load current olympicsPage data
    this.olympicsAPIService.getSingleOlympicsItemData(this.id)
      .subscribe((data: HttpResponse<Sport>) => {
        this.olympicsPage = data.body;
        this.breadcrumbsData = [{
          label: `Olympic Sports`,
          url: `/sports-pages/olympics-pages`
        }, {
          label: this.olympicsPage.imageTitle,
          url: `/sports-pages/olympics-pages/${this.olympicsPage.id}`
        }];
      }, error => {
        this.router.navigate(['/sports-pages/olympics-pages']);
      });
  }

  /**
   * Reload olympicsPage data from server.
   */
  public revertOlympicsPageChanges(): void {
    this.loadInitialData();
  }

  /**
   * handle deleting promotion
   * @param {Promotion} promotion
   */
  public removeOlympicsPage(): void {
    this.sendRemoveRequest(this.olympicsPage);
  }

  /**
   * Send DELETE API request
   * @param {Promotion} promotion
   */
  public sendRemoveRequest(olympicsPage: Sport): void {
    this.olympicsAPIService.deleteOlympicsPage(olympicsPage.id)
      .subscribe(() => {
        this.dialogService.showNotificationDialog({
          title: 'Sport is Removed'
        });
        this.router.navigate(['/sports-pages/olympics-pages']);
      });
  }

  /**
   * Make PUT request to server to update widhet data.
   */
  public saveOlympicsPageChanges(): void {
    this.olympicsAPIService
      .putOlympicsItemChanges(this.olympicsPage)
      .map((data: HttpResponse<Sport>) => {
        return data.body;
      })
      .subscribe((data: Sport) => {
        this.olympicsPage = data;
        this.actionButtons.extendCollection(this.olympicsPage);
        this.dialogService.showNotificationDialog({
          title: 'Upload Completed',
          message: 'Sport Page Changes are Saved.'
        });
      });
  }

  /**
   * Upload file on input change event.
   * @param {FormData} formData - image
   * @param {string} fileType - name of property in OlimpicSportObject where filedata will be stored
   */
  public uploadImage(formData: FormData, fileType): void {
    this.olympicsAPIService
        .postNewOlympicsFilename(this.id, formData)
        .map((data: HttpResponse<Sport>) => data.body)
        .subscribe((data: Sport) => {
          this.olympicsPage = _.extend(data, _.pick(this.olympicsPage, 'disabled', 'inApp', 'showInPlay',
            'isOutrightSport', 'isMultiTemplateSport', 'imageTitle', 'categoryId', 'dispSortName', 'targetUri',
            'typeIds', 'alt', 'primaryMarkets', 'tabLive', 'tabMatches', 'tabOutrights', 'tabSpecials', 'defaultTab'));
          this.snackBar.open('Image Was Uploaded.', 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        });
  }

  /**
   * @param type
   * @param {string} type - file type for Removing on backend, will be sent as additional property
   * @param {string} fileType - name of property in OlimpicSportObject where filedata will be Cleared
   */
  public removeImage(type, fileType) {
    this.olympicsAPIService
      .deleteOlympicsFilename(this.id, {
        fileType: type
      })
      .map((data: HttpResponse<Sport>) => data.body)
      .subscribe((data: Sport) => {
        this.olympicsPage = _.extend(data, _.pick(this.olympicsPage, 'disabled', 'inApp', 'showInPlay',
          'isOutrightSport', 'isMultiTemplateSport', 'imageTitle', 'categoryId', 'dispSortName', 'targetUri',
          'typeIds', 'alt', 'primaryMarkets', 'tabLive', 'tabMatches', 'tabOutrights', 'tabSpecials', 'defaultTab'));
        this.snackBar.open('Image Was Removed.', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  public onChangeDefaultTab(value: string): void {
    this.olympicsPage.defaultTab = value;
  }

  public onChangeFirstTemplate(value: string): void {
    this.olympicsPage.outcomesTemplateType1 = value;
  }

  public isValidForm(olympicsPage: Sport): boolean {
    return !!(olympicsPage.imageTitle &&
      olympicsPage.imageTitle.length > 0 &&
      olympicsPage.categoryId &&
      olympicsPage.primaryMarkets.length > 0 &&
      olympicsPage.typeIds.length > 0 &&
      olympicsPage.dispSortName.length > 0);
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeOlympicsPage();
        break;
      case 'save':
        this.saveOlympicsPageChanges();
        break;
      case 'revert':
        this.revertOlympicsPageChanges();
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
}
