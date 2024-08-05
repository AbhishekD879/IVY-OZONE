import {AfterViewChecked, ChangeDetectorRef, Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {BrandService} from '@app/client/private/services/brand.service';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {ActivatedRoute, Router} from '@angular/router';
import {Campaign} from '@app/client/private/models/campaign.model';
import {Post} from '@app/client/private/models/timeline-post.model';
import {PostStatus} from '@app/client/private/models/timelinePostStatus.model';
import {PostApiService} from '@app/timeline/service/post-api.service';
import {TemplateApiService} from '@app/timeline/service/template-api.service';
import {TimelineTemplate} from '@app/client/private/models/timelineTemplate.model';
import * as _ from 'lodash';
import {CampaignApiService} from '@app/timeline/service/campaign-api.service';
import {TinymceComponent} from '@app/shared/tinymce/tinymce.component';

@Component({
  selector: 'post-create',
  templateUrl: './post-create.component.html'
})
export class PostCreateComponent implements OnInit, AfterViewChecked, OnDestroy {
  @ViewChild('text') postTextEditor: TinymceComponent;

  public breadcrumbsData: Breadcrumb[];
  newPost: Post;
  campaign: Campaign;
  templates: Array<TimelineTemplate>;
  activeTemplate: TimelineTemplate;
  getDataError: string;
  campaignId: string = '';
  campaignName: string = '';


  nameValid: boolean;
  headerValid: boolean;
  yellowHeaderValid: boolean;
  textValid: boolean;
  subHeaderValid: boolean;
  eventIdValid: boolean;
  selectionIdValid: boolean;
  betPromptHeaderValid: boolean;
  postHrefValid: boolean;

  isSpotlight: boolean = false;
  isVerdict: boolean = false;

  constructor(private brandService: BrandService,
              private postApiService: PostApiService,
              private campaignApiService: CampaignApiService,
              private templateApiService: TemplateApiService,
              private dialogService: DialogService,
              private route: ActivatedRoute,
              private cdr: ChangeDetectorRef,
              private router: Router) {
  }

  ngAfterViewChecked(): void {
    this.cdr.detectChanges();
  }

  ngOnInit() {
    if (this.postApiService.currentSpotlightData && this.postApiService.currentSpotlightData.spotlightDetails.dataType === 'spotlight') {
      this.isSpotlight = true;
    }
    if (this.postApiService.currentSpotlightData && this.postApiService.currentSpotlightData.spotlightDetails.dataType === 'verdict') {
      this.isVerdict = true;
    }
    this.campaignId = this.route.snapshot.paramMap.get('campaignId');
    this.campaignApiService.getCampaign(this.campaignId).subscribe((campaign: any) => {
      this.campaign = campaign.body;
      this.campaignName = this.campaign.name;
      this.breadcrumbsData = [{
        label: `Campaigns`,
        url: `/timeline/campaign`
      }, {
        label: `${this.campaign.name}`,
        url: `/timeline/campaign/edit/${this.campaignId}`
      }, {
        label: `Posts`,
        url: `/timeline/post/by-campaign/${this.campaign.id}`
      }, {
        label: 'Create Post',
        url: `/timeline/post/create/${this.campaignId}`
      }];
    });

    this.newPost = {
      id: '',
      template: null,
      pinned: false,
      name: '',
      campaignId: this.campaignId,
      campaignName: this.campaignName,
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',
      publishedAt: '',

      postStatus: PostStatus.DRAFT,

      isChanged: false,
      brand: this.brandService.brand,
      isSpotlight: this.isSpotlight,
      isVerdict: this.isVerdict
    };

    this.loadTemplates();
  }

  ngOnDestroy(): void {
    this.postApiService.currentSpotlightData = undefined;
  }

  updateText(data) {
    this.newPost.template.text = data;
  }

  setTemplate(template: TimelineTemplate) {
    if ((this.isSpotlight || this.isVerdict) && this.postApiService.currentSpotlightData) {
      this.setTemplateForSpotlightOrVerdictPost(template);
    } else {
      this.setTemplateForPlainPost(template);
    }
  }

  setTemplateForPlainPost(template: TimelineTemplate): void {
    this.resetPostSpecificTemplateData();

    this.activeTemplate = _.cloneDeep(template);
    this.newPost.template = template;
    if (this.postTextEditor) {
      this.postTextEditor.update(this.newPost.template.text);
    }
    this.newPost.name = `${template.name} ${new Date().toUTCString()}`;
    this.checkModelValid();
  }

  setTemplateForSpotlightOrVerdictPost(template: TimelineTemplate): void {
    this.resetPostSpecificTemplateData();

    this.activeTemplate = _.cloneDeep(template);
    this.newPost.template = template;
    this.newPost.name = this.postApiService.currentSpotlightData.name;
    this.newPost.template.headerText = this.postApiService.currentSpotlightData.headerText;
    this.newPost.template.text = this.postApiService.currentSpotlightData.text;
    if (this.newPost.template.selectionId && this.isSpotlight) {
      this.newPost.template.selectionId = this.postApiService.currentSpotlightData.selectionId;
    }
    setTimeout(() => {
      if (this.postTextEditor) {
        this.postTextEditor.update(this.newPost.template.text);
        this.postTextEditor.onDataChange();
      }
    }, 1000);

    this.checkModelValid();
  }

  private resetPostSpecificTemplateData() {
    if (this.activeTemplate) {
      this.templates = this.templates.filter(t => t.id !== this.activeTemplate.id);
      this.templates.unshift(this.activeTemplate);
    }
  }

  trackByIdentity = (index: number, item: any) => item.id;

  loadTemplates() {
    this.templateApiService.getTemplatesByBrand()
      .subscribe((data: any) => {
        if (data.body && data.body.length) {
          this.templates = data.body;
          if (this.isSpotlight) {
            this.templates = this.templates.filter(template => template.isSpotlightTemplate);
          }
          if (this.isVerdict) {
            this.templates = this.templates.filter(template => template.isVerdictTemplate);
          }
        }
      }, error => {
        this.getDataError = error.message;
      });
  }

  checkModelValid(): boolean {
    if (this.newPost && this.newPost.template) {
      this.nameValid = this.newPost.name.trim().length > 0;
      this.headerValid = (!this.activeTemplate.headerText) || (this.newPost.template.headerText.trim().length > 0);
      this.yellowHeaderValid = (!this.activeTemplate.yellowHeaderText) || (this.newPost.template.yellowHeaderText.trim().length > 0);
      this.textValid = this.newPost.template.text.trim().length > 0;
      this.subHeaderValid = (!this.activeTemplate.subHeader) || (this.newPost.template.subHeader.trim().length > 0);
      this.eventIdValid = (!this.activeTemplate.eventId) || (this.newPost.template.eventId.trim().length > 0);
      this.selectionIdValid = (!this.activeTemplate.selectionId) || (this.newPost.template.selectionId.trim().length > 0);
      this.betPromptHeaderValid = (!this.activeTemplate.betPromptHeader) ||
        (this.newPost.template.betPromptHeader.trim().length > 0);
      this.postHrefValid = (!this.activeTemplate.postHref) || (this.newPost.template.postHref.trim().length > 0);

      return this.nameValid && this.headerValid && this.yellowHeaderValid && this.textValid && this.subHeaderValid
        && this.eventIdValid && this.selectionIdValid && this.betPromptHeaderValid && this.postHrefValid;
    } else {
      return false;
    }
  }

  public savePostChanges(): void {
    this.postApiService.createPost(this.newPost)
      .subscribe(data => {
        this.newPost.id = data.body.id;
        this.finishPostCreation();
      });
  }

  finishPostCreation(): void {
    const self = this;
    this.dialogService.showNotificationDialog({
      title: 'Save Completed',
      message: 'Post is Created and Stored.',
      closeCallback() {
        self.router.navigate([`timeline/post/by-campaign/${self.campaignId}/edit/${self.newPost.id}`]);
      }
    });
  }
}
