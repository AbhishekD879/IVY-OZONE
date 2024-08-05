import {Component, OnDestroy, OnInit} from '@angular/core';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ActivatedRoute, Router} from '@angular/router';
import {forkJoin} from 'rxjs/observable/forkJoin';
import * as _ from 'lodash';
import {PostApiService} from '@app/timeline/service/post-api.service';
import {Post} from '@app/client/private/models/timeline-post.model';
import {PostStatus} from '@app/client/private/models/timelinePostStatus.model';
import { PageEvent } from '@angular/material/paginator';
import { MatSnackBar } from '@angular/material/snack-bar';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {CampaignApiService} from '@app/timeline/service/campaign-api.service';
import {Campaign} from '@app/client/private/models/campaign.model';
import {HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {SseService} from '@app/shared/sse/sse.service';
import {Subscription} from 'rxjs/Subscription';
import {environment} from '@environment/environment';
import {TimelinePostSseEvent, TimelinePostSseOperation} from '@app/client/private/models/timeline-post-sse-event.model';
import {AppConstants} from '@app/app.constants';

@Component({
  selector: 'post-list',
  templateUrl: './post-list.component.html'
})
export class PostListComponent implements OnInit, OnDestroy {
  public breadcrumbsData: Breadcrumb[];
  campaign: Campaign;
  postData: Array<Post>;
  searchField: string = '';
  getDataError: string;
  campaignId: string = '';

  postsAmount;
  pageSize = 25;
  pageEvent: PageEvent;
  startingNumberOffset = 0;

  sseStream: Subscription;

  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Template',
      property: 'template.name',
      type: 'nested',
      width: 2
    }, {
      name: 'Name',
      property: 'name',
      link: {
        hrefProperty: 'id',
        path: 'edit'
      },
      type: 'link',
      width: 3
    }, {
      name: 'Header',
      property: 'template.headerText',
      type: 'nested',
      width: 2
    }, {
      name: 'Actions',
      property: 'actions',
      type: 'actions',
      subtypes: ['publish', 'unpublish'],
      width: 1
    },
    {
      name: 'Status',
      property: 'postStatus',
      width: 1
    }, {
      name: 'Published At',
      property: 'publishedAt',
      type: 'date',
      width: 1
    },
    {
      name: 'Updated By',
      property: 'updatedByUserName',
      width: 2
    },
    {
      name: 'Modified At',
      property: 'updatedAt',
      type: 'date',
      width: 1
    }
  ];

  filterProperties: Array<string> = [
    'name'
  ];

  constructor(private dialogService: DialogService,
              private postApiService: PostApiService,
              private campaignApiService: CampaignApiService,
              private globalLoaderService: GlobalLoaderService,
              private route: ActivatedRoute,
              private sseService: SseService,
              private snackBar: MatSnackBar,
              private router: Router) { }

  ngOnInit() {
    this.initSseSubscription();

    this.campaignId = this.route.snapshot.paramMap.get('campaignId');
    this.campaignApiService.getCampaign(this.campaignId).subscribe((campaign: any) => {
      this.campaign = campaign.body;
      this.breadcrumbsData = [{
        label: `Campaigns`,
        url: `/timeline/campaign`
      }, {
        label: `${this.campaign.name}`,
        url: `/timeline/campaign/edit/${this.campaignId}`
      }, {
        label: 'Posts',
        url: `/timeline/post/by-campaign/${this.campaignId}`
      }];
    });

    this.pageEvent = <any>{pageIndex: 0, pageSize: this.pageSize};
    this.loadPostsCount();
    this.loadPostsPortion();
  }

  private initSseSubscription(): void {
    this.sseStream = this.sseService.observeMessages(`${environment.apiUrl}timeline/sse`)
      .subscribe((sseEvent: TimelinePostSseEvent) => {
        // Ignore for changes in another campaign
        switch (sseEvent.operation) {
          case TimelinePostSseOperation.INSERT: {
            this.sseAddPost(sseEvent);
            break;
          }
          case TimelinePostSseOperation.UPDATE: {
            this.sseUpdatePost(sseEvent);
            break;
          }
          case TimelinePostSseOperation.DELETE: {
            this.sseRemovePost(sseEvent);
            break;
          }
        }
      });
  }

  private sseAddPost(operationInfo: TimelinePostSseEvent): void {
    const post: Post = operationInfo.content;
    if (post.campaignId && (post.campaignId === this.campaignId)) {
      this.snackBar.open('New post was just added: ' + post.name, 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
      this.postApiService.getPost(post.id)
        .subscribe(postResponse => {
          this.postData.unshift(postResponse.body);
        });
    }
  }

  private sseUpdatePost(operationInfo: TimelinePostSseEvent): void {
    const updatedPost: Post = operationInfo.content;
    if (updatedPost.campaignId && (updatedPost.campaignId === this.campaignId)) {
      for (let i = 0; i < this.postData.length; ++i) {
        const post = this.postData[i];
        if (post.id === updatedPost.id) {
          this.snackBar.open('Post was just updated: ' + updatedPost.name, 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
          this.postApiService.getPost(post.id)
            .subscribe(postResponse => {
              this.postData.splice(i, 1);
              this.postData.unshift(postResponse.body);
            });
          break;
        }
      }
    }
  }

  private sseRemovePost(removePostOperationInfo: TimelinePostSseEvent): void {
    const prevLength = this.postData.length;
    const postToRemove = this.postData.filter(post => post.id === removePostOperationInfo.contentId)[0];
    this.postData = this.postData.filter(post => post.id !== removePostOperationInfo.contentId);
    if (prevLength !== this.postData.length) {
      this.snackBar.open('Post was just removed: ' + postToRemove.name, 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
    }
  }

  ngOnDestroy(): void {
    if (this.sseStream) {
      this.sseStream.unsubscribe();
    }
  }

  loadPostsCount() {
    this.postApiService.getPostsCountByBrandAndCampaignId(this.campaignId)
      .subscribe((data: any) => {
        this.postsAmount = data.body;
      });
  }

  loadPostsPortion() {
    this.globalLoaderService.showLoader();
    this.postApiService.getPostsPageByBrandAndCampaignWithOrdering(this.campaignId,
                                                               this.pageEvent.pageIndex, this.pageEvent.pageSize, 'updatedAt,desc')
      .subscribe((data: any) => {
        this.postData = data.body;
        this.startingNumberOffset = this.pageEvent.pageIndex * this.pageSize;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.getDataError = error.message;
        this.globalLoaderService.hideLoader();
      });
  }

  removePost(post: Post) {
    this.dialogService.showConfirmDialog({
      title: 'Remove Post',
      message: 'Are You Sure You Want to Remove Post?',
      yesCallback: () => {
        this.sendRemoveRequest(post);
      }
    });
  }

  publishPost(post: Post) {
    const prevStatus = post.postStatus;
    post.postStatus = PostStatus.PUBLISHED;
    this.updatePost(post).subscribe((updatedPost: Post) => {
    }, error => {
      post.postStatus = prevStatus;
    });
  }

  unpublishPost(post: Post) {
    const prevStatus = post.postStatus;
    post.postStatus = PostStatus.UNPUBLISHED;
    this.updatePost(post).subscribe((updatedPost: Post) => {
    }, error => {
      post.postStatus = prevStatus;
    });
  }

  updatePost(post: Post): Observable<Post> {
    return this.postApiService.updatePost(post).map((response: HttpResponse<Post>) => {
      return response.body;
    }).map((updatedPost: Post) => {
      const index = this.postData.findIndex((postFromList: Post) => postFromList.id === updatedPost.id);
      this.postData[index] = updatedPost;
      return updatedPost;
    });
  }

  sendRemoveRequest(post: Post) {
    this.postApiService.deletePost(post.id)
      .subscribe((data: any) => {
        this.postData.splice(this.postData.indexOf(post), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Post is Removed.'
        });
      });
  }

  removeHandlerMulti(postIds: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Posts (${postIds.length})`,
      message: 'Are You Sure You Want to Remove Posts?',
      yesCallback: () => {
        removeMultiPosts.call(this);
      }
    });

    function removeMultiPosts() {
      this.globalLoaderService.showLoader();
      forkJoin(postIds.map(id => this.postApiService.deletePost(id)))
        .subscribe(() => {
          postIds.forEach((id) => {
            const index = _.findIndex(this.postData, {id: id});
            this.postData.splice(index, 1);
            this.postsAmount--;
          });
          this.loadPostsPortion();
          this.globalLoaderService.hideLoader();
        });
    }
  }

  openCreatePost() {
    this.router.navigateByUrl(`timeline/post/by-campaign/${this.campaignId}/create`);
  }

  handlePageChanging($event: PageEvent) {
    this.pageEvent = $event;
    this.loadPostsPortion();
  }
}
