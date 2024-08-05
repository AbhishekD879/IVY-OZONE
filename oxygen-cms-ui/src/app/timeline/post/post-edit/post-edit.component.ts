import {ChangeDetectorRef, Component, OnInit, ViewChild, AfterViewChecked} from '@angular/core';

import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {ActivatedRoute, Router} from '@angular/router';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {HttpResponse} from '@angular/common/http';
import {AppConstants} from '@app/app.constants';
import {Post} from '@app/client/private/models/timeline-post.model';
import {PostApiService} from '@app/timeline/service/post-api.service';
import {TimelineTemplate} from '@app/client/private/models/timelineTemplate.model';
import {forkJoin} from 'rxjs/observable/forkJoin';
import {CampaignApiService} from '@app/timeline/service/campaign-api.service';
import {Campaign} from '@app/client/private/models/campaign.model';
import {TinymceComponent} from '@app/shared/tinymce/tinymce.component';
import TimelineUtils from '@app/timeline/timeline-utils';
import {PostStatus} from '@app/client/private/models/timelinePostStatus.model';
import {Observable} from 'rxjs/Observable';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'post-edit',
  styleUrls: ['./post-edit-component.scss'],
  templateUrl: './post-edit.component.html'
})
export class PostEditComponent implements OnInit, AfterViewChecked {
  activeTemplate: TimelineTemplate;

  @ViewChild('actionButtons') actionButtons;
  @ViewChild('text') postTextEditor: TinymceComponent;
  post: Post;
  campaign: Campaign;

  breadcrumbsData: Breadcrumb[];
  id: string;
  getDataError: string;

  nameValid: boolean;
  headerValid: boolean;
  yellowHeaderValid: boolean;
  textValid: boolean;
  subHeaderValid: boolean;
  eventIdValid: boolean;
  selectionIdValid: boolean;
  betPromptHeaderValid: boolean;
  postHrefValid: boolean;
  campaignId: string;

  constructor(private postApiService: PostApiService,
              private campaignApiService: CampaignApiService,
              private route: ActivatedRoute,
              private router: Router,
              private dialogService: DialogService,
              private cdr: ChangeDetectorRef,
              private snackBar: MatSnackBar) {
    this.checkModelValidForSave = this.checkModelValidForSave.bind(this);
    this.checkModelValidForSaveAndPublish = this.checkModelValidForSaveAndPublish.bind(this);
  }

  ngAfterViewChecked(): void {
    this.cdr.detectChanges();
  }

  ngOnInit() {
    this.campaignId = this.route.snapshot.paramMap.get('campaignId');
    this.id = this.route.snapshot.paramMap.get('id');
    this.loadInitialData();
  }

  updateText(data) {
    this.post.template.text = data;
  }

  isPostValidForSave(post: Post): boolean {
    if (post && post.template) {
      this.nameValid = post.name.trim().length > 0;
      this.headerValid = (!this.activeTemplate.headerText) || (post.template.headerText.trim().length > 0);
      this.yellowHeaderValid = (!this.activeTemplate.yellowHeaderText) || (post.template.yellowHeaderText.trim().length > 0);
      this.textValid = post.template.text.trim().length > 0;
      this.subHeaderValid = (!this.activeTemplate.subHeader) || (post.template.subHeader.trim().length > 0);
      this.eventIdValid = (!this.activeTemplate.eventId) || (post.template.eventId.trim().length > 0);
      this.selectionIdValid = (!this.activeTemplate.selectionId) || (post.template.selectionId.trim().length > 0);
      this.betPromptHeaderValid = (!this.activeTemplate.betPromptHeader) ||
        (post.template.betPromptHeader.trim().length > 0);
      this.postHrefValid = (!this.activeTemplate.postHref) || (post.template.postHref.trim().length > 0);

      return this.nameValid && this.headerValid && this.yellowHeaderValid && this.textValid && this.subHeaderValid &&
        this.eventIdValid && this.selectionIdValid && this.betPromptHeaderValid && this.postHrefValid;
    } else {
      return false;
    }
  }

  checkModelValidForSave(post: Post): boolean {
    return this.isPostValidForSave(post) && TimelineUtils.isNotYetPublished(post);
  }

  checkModelValidForSaveAndPublish(post: Post): boolean {
    return this.isPostValidForSave(post);
  }

  private loadInitialData(callback?: any): void {
    forkJoin(this.postApiService.getPost(this.id),
      this.campaignApiService.getCampaign(this.campaignId)).subscribe(
      ([timelinePostResponse, campaignResponse]) => {
        this.post = timelinePostResponse.body;
        if (this.postTextEditor) {
          this.postTextEditor.update(this.post.template.text);
        }

        this.campaign = campaignResponse.body;

        this.activeTemplate = this.post && this.post.template;

        this.breadcrumbsData = [{
          label: `Campaigns`,
          url: `/timeline/campaign`
        }, {
          label: `${this.campaign.name}`,
          url: `/timeline/campaign/edit/${this.post.campaignId}`
        }, {
          label: `Posts`,
          url: `/timeline/post/by-campaign/${this.campaign.id}`
        }, {
          label: 'Edit Post',
          url: `/timeline/post/edit/${this.id}`
        }];

        if (callback) {
          callback();
        }
      });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removePost();
        break;
      case 'save':
        this.savePostChanges();
        break;
      case 'saveAndPublish':
        this.savePostChangesWithPublishedStatus();
        break;
      case 'unpublish':
        this.savePostChangesWithUnpublishedStatus();
        break;
      case 'revert':
        this.revertPostChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  private removePost(): void {
    this.postApiService.deletePost(this.post.id)
      .subscribe((data: any) => {
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Post is Removed.'
        });
        this.router.navigate([`/timeline/campaign/edit/${this.campaignId}`]);
      });
  }

  private savePostChanges(afterMsg?: string) {
    this.doSavePostChanges(afterMsg).subscribe(() => {});
  }


  private doSavePostChanges(afterMsg?: string): Observable<void> {
    return this.postApiService.updatePost(this.post)
      .map((response: HttpResponse<Post>) => {
        return response.body;
      })
      .map((data: Post) => {
        this.post = data;
        this.actionButtons.extendCollection(this.post);
        this.showNotification(afterMsg ? afterMsg : 'Post Changes are Saved.');
      });
  }

  private savePostChangesWithPublishedStatus() {
    const prevStatus = this.post.postStatus;
    this.post.postStatus = PostStatus.PUBLISHED;
    this.doSavePostChanges('Post is Saved and Published').subscribe(() => {}, error => {
      this.post.postStatus = prevStatus;
    });
  }

  private savePostChangesWithUnpublishedStatus() {
    this.loadInitialData(() => {
      const prevStatus = this.post.postStatus;
      this.post.postStatus = PostStatus.UNPUBLISHED;
      this.doSavePostChanges('Post is Saved and Unpublished').subscribe(() => {}, error => {
        this.post.postStatus = prevStatus;
      });
    });
  }

  showNotification(message): void {
    this.snackBar.open(message, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
  }

  private revertPostChanges(): void {
    this.loadInitialData();
  }
}
