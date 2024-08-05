import {AbstractService} from './transport/abstract.service';
import {Configuration} from '../../models/configuration.model';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {Post} from '@app/client/private/models/timeline-post.model';

@Injectable()
export class TimelinePostService extends AbstractService<Configuration> {
  timelineBaseUrl: string = 'timeline/post';
  timelineByBrandUrl: string = `timeline/post/brand/${this.brand}`;

  sortParamName: string = `sort`;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getPosts(): Observable<HttpResponse<Post[]>> {
    return this.sendRequest<Post[]>('get', this.timelineBaseUrl, null);
  }

  public getPostsByBrand(): Observable<HttpResponse<Post[]>> {
    return this.sendRequest<Post[]>('get', this.timelineByBrandUrl, null);
  }

  public getPostsCountByBrandAndCampaignId(campaignId: string): Observable<HttpResponse<Post[]>> {
    return this.sendRequest<Post[]>('get', `${this.timelineByBrandUrl}/${campaignId}/count`, null);
  }

  public getPostsByBrandAndCampaign(campaignId: string): Observable<HttpResponse<Post[]>> {
    return this.sendRequest<Post[]>('get', `${this.timelineByBrandUrl}/${campaignId}`, null);
  }

  public getPostsByBrandWithOrdering(sortParamValue: string): Observable<HttpResponse<Post[]>> {
    return this.sendRequest<Post[]>('get', `${this.timelineByBrandUrl}?${this.sortParamName}=${sortParamValue}`, null);
  }

  public getPostsByBrandAndCampaignWithOrdering(campaignId: string, pageIndex: number,
                                                pageSize: number, sortParamValue: string): Observable<HttpResponse<Post[]>> {
    return this.sendRequest<Post[]>('get',
      `${this.timelineByBrandUrl}/${campaignId}/${pageIndex}/${pageSize}?${this.sortParamName}=${sortParamValue}`, null);
  }

  public getSinglePost(id: string): Observable<HttpResponse<Post>> {
    const url = `${this.timelineBaseUrl}/${id}`;
    return this.sendRequest<Post>('get', url, null);
  }

  public savePost(post: Post): Observable<HttpResponse<Post>> {
    return this.sendRequest<Post>('post', this.timelineBaseUrl, post);
  }

  public updatePost(id: string, post: Post): Observable<HttpResponse<Post>> {
    const apiUrl = `${this.timelineBaseUrl}/${id}`;
    return this.sendRequest<Post>('put', apiUrl, post);
  }

  public deletePost(id: string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('delete', `${this.timelineBaseUrl}/${id}`, null);
  }

  public republishByCampaignId(campaignId: string) {
    return this.sendRequest<void>('put', `${this.timelineBaseUrl}/republish/${campaignId}`, null);
  }
}
