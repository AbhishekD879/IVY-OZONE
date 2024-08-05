import {TinymceComponent} from '@app/shared/tinymce/tinymce.component';
import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {SeoAPIService} from '../../service/seo.api.service';
import {SeoPage} from '@app/client/private/models/seopage.model';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {HttpResponse} from '@angular/common/http';
import {ActionButtonsComponent} from '@app/shared/action-buttons/action-buttons.component';

const priority: number[] = [
  0,
  0.1,
  0.2,
  0.3,
  0.4,
  0.5,
  0.6,
  0.7,
  0.8,
  0.9,
  1,
];

const frequency: string[] = [
  'always',
  'hourly',
  'daily',
  'weekly',
  'monthly',
  'yearly',
  'never'
];


@Component({
  selector: 'single-seo-page',
  templateUrl: './seo.page.component.html',
  styleUrls: ['./seo.page.component.scss']
})
export class SingleSeoPageComponent implements OnInit {
  updateFrequencyOptions: string[] = frequency;
  pagePriorityOptions: number[] = priority;
  seoPage: SeoPage;
  private readonly seoDefaultTitle: string = "SPORTS BETTING ONLINE";
  id: string;
  public breadcrumbsData: Breadcrumb[];
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  @ViewChild('htmlMarkup') editor: TinymceComponent;

  constructor(
    private dialogService: DialogService,
    private route: ActivatedRoute,
    private router: Router,
    private seoAPIService: SeoAPIService
  ) {}

  handleStaticBlockChange(data) {
    this.seoPage.staticBlock = data;
  }

  /**
   * Load seoPage data from server.
   */
  loadInitialData() {
    // load current seoPage data
    this.seoAPIService.getSingSeoItemData(this.id)
      .map((data: HttpResponse<SeoPage>) => data.body)
      .subscribe((data: SeoPage) => {
        this.seoPage = data;
        if (this.seoPage && !this.seoPage.staticBlockTitle) {
          this.seoPage.staticBlockTitle = this.seoDefaultTitle;
        }
        this.breadcrumbsData = [{
          label: `SEO`,
          url: `/seo-pages/manual`
        }, {
          label: this.seoPage.url,
          url: `/seo-pages/manual/${this.seoPage.id}`
        }];
        if (this.editor) {
          this.editor.update(this.seoPage.staticBlock);
        }
      }, error => {
        this.router.navigate(['/seo-pages/manual']);
      });
  }

  /**
   * Reload seoPage data from server.
   */
  revertSeoPageChanges() {
    this.loadInitialData();
  }

  /**
   * Send DELETE API request
   * @param {Promotion} promotion
   */
  removeSeoPage() {
    this.seoAPIService.deleteSeoPage(this.seoPage.id)
      .subscribe((data: HttpResponse<void>) => {
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Seo Page is Removed.'
        });
        this.router.navigate(['/seo-pages/manual']);
      });
  }


  /**
   * Make PUT request to server to update widhet data.
   */
  saveWidgetChanges() {
    this.seoAPIService.putSeoItemChanges(this.seoPage)
        .map((response: HttpResponse<SeoPage>) => {
          return response.body;
        })
        .subscribe((data: SeoPage) => {
          this.seoPage = data;
          this.actionButtons.extendCollection(this.seoPage);
          this.dialogService.showNotificationDialog({
            title: 'Upload Completed',
            message: 'Seo Page Changes are Saved.'
          });
        });
  }

  public isValidForm(seoPage: SeoPage): boolean {
    return !!(seoPage.title && seoPage.title.length > 0);
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeSeoPage();
        break;
      case 'save':
        this.saveWidgetChanges();
        break;
      case 'revert':
        this.revertSeoPageChanges();
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
