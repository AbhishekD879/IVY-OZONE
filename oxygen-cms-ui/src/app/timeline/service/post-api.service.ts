import {Injectable} from '@angular/core';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ApiClientService} from '@app/client/private/services/http';
import 'rxjs/add/operator/catch';
import {HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import {Post} from '@app/client/private/models/timeline-post.model';

@Injectable()
export class PostApiService {
  private spotlightData: any;

  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService) {
  }

  get currentSpotlightData() {
    return this.spotlightData;
  }

  set currentSpotlightData(spotlightData: any) {
    this.spotlightData = spotlightData;
  }


  /**
   * Wrap request to handle success/error.
   * @param observableDate
   */
  wrappedObservable(observableDate): Observable<any> {
    return observableDate
      .map(res => {
        this.globalLoaderService.hideLoader();
        return res;
      })
      .catch(response => {
        if (response instanceof HttpErrorResponse) {
          this.handleRequestError(response.error);
        }

        return Observable.throw(response);
      });
  }

  handleRequestError(error): void {
    this.globalLoaderService.hideLoader();
  }

  hideLoader(): void {
    this.globalLoaderService.hideLoader();
  }

  getPosts(): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.postService().getPosts();
    return this.wrappedObservable(data);
  }

  getPostsByBrand(): Observable<any> {
    const data = this.apiClientService.postService().getPostsByBrand();
    return this.wrappedObservable(data);
  }

  getPostsCountByBrandAndCampaignId(campaignId: string): Observable<number> {
    const data = this.apiClientService.postService().getPostsCountByBrandAndCampaignId(campaignId);
    return this.wrappedObservable(data);
  }

  getPostsPageByBrandAndCampaignWithOrdering(campaignId: string,
                                             pageIndex: number, pageSize: number, sortParamValue: string): Observable<any> {
    const data = this.apiClientService.postService().getPostsByBrandAndCampaignWithOrdering(campaignId,
                                                                                            pageIndex, pageSize, sortParamValue);
    return this.wrappedObservable(data);
  }

  getPost(id: string): Observable<any> {
    const data = this.apiClientService.postService().getSinglePost(id);
    return this.wrappedObservable(data);
  }

  createPost(post: Post): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.postService().savePost(post);
    return this.wrappedObservable(data);
  }

  updatePost(post: Post): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.postService().updatePost(post.id, post);
    return this.wrappedObservable(data);
  }

  deletePost(id: string): Observable<any> {
    this.globalLoaderService.showLoader();
    const data = this.apiClientService.postService().deletePost(id);
    return this.wrappedObservable(data);
  }
}
