import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable, OnDestroy } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { Observable, ReplaySubject } from 'rxjs';
import { first, map } from 'rxjs/operators';
import { SegmentedCMSEndPointService } from './segmented-cms-endpoint.service';
import { IInitialData, INavigationPoint } from '@app/core/services/cms/models';
import { PubSubService } from '../communication/pubsub/pubsub.service';
import { ONE_TWO_FREE_CONSTS } from './cms.constants';

@Injectable({ providedIn: 'root' })
export class SegmentedCMSService implements OnDestroy {
  CMS_ENDPOINT: string;
  brand: string = environment.brand;
  private initialData$: ReplaySubject<IInitialData>;
  private initialData: IInitialData;
  private initialDataAvailable: boolean = false;

  constructor(protected http: HttpClient,
    private segmentedCMSEndPointService: SegmentedCMSEndPointService,
    private pubsubService: PubSubService) {
    this.CMS_ENDPOINT = environment.CMS_ENDPOINT;
    this.pubsubService.subscribe('cms-init-data', this.pubsubService.API.SEGMENT_RECEIVED, () => {
      this.getCmsInitData(true);
    });
  }

  ngOnDestroy(): void {
    if (this.initialData$) {
      this.initialData$.unsubscribe();
    }
  }

  /**
   * @returns Observable of IInitialData data
   */
  getCmsInitData(refresh: boolean = false): Observable<IInitialData> {
    if (this.initialData$ && !refresh) {
      return this.initialData$.asObservable();
    }
    this.initialData$ = new ReplaySubject<IInitialData>(1);
    const endPoint = this.segmentedCMSEndPointService.getInitialDataEndPoint();
    this.getData(endPoint)
      .pipe(
        first(),
        map((response: HttpResponse<IInitialData>) => response.body)
      )
      .subscribe((data: IInitialData) => {
        this.releaseSubject(data);
        if (refresh) {
          this.pubsubService.publish(this.pubsubService.API.SEGMENTED_INITIAL_DATA_RECEIVED, { action: 'CMS_SEGMENTED_INIT=>SUCCESS' });
        }
      }, error => {
        console.warn(error);
        this.pubsubService.publish(this.pubsubService.API.CMS_SEGMENT_API_FAILED, { action: 'CMS_SEGMENTED_INIT=>FAILED' });
      });
    return this.initialData$.asObservable();
  }

  /**
   *
   * @param url endpoint
   * @param params any
   * @returns
   */
  protected getData<T>(url: string, params: any = {}): Observable<HttpResponse<T>> {
    return this.http.get<T>(`${this.CMS_ENDPOINT}/${this.brand}/${url}`, {
      observe: 'response',
      params: params
    });
  }

  /**
   * @param  {IInitialData} data
   * @returns void
   */
  protected releaseSubject(data: IInitialData): void {
    this.initialDataAvailable = true;
    this.initialData = data;
    this.initialData$.next(this.initialData);
    this.initialData$.complete();
  }

  isInitialDataAvailable() {
    return this.initialDataAvailable;
  }

  /* 
To Check if any Extra super Buttons are configured are active
 */
getActiveExtraNavPoints(data,selectedModule,type){
  return (data?.extraNavigationPoints || []).filter((point:INavigationPoint) =>{
      return Date.now() < Date.parse(point.validityPeriodEnd) &&
      Date.now() > Date.parse(point.validityPeriodStart) && 
      this.checkForModule(selectedModule,point,type) && point.featureTag && point.featureTag === ONE_TWO_FREE_CONSTS.OTF_FEATURE_TAG
    })
}

/* 
To Check if Extra SB is configured for the specific category,sport or competition*/
checkForModule(selectedModule,point,type){
   return (selectedModule && (type == 'homeTabs'?point.homeTabs.includes(this.showOtfBtn(selectedModule[0])):
   type=="bigCompetition"?
   point.competitionId.includes(selectedModule[1]) :
   point.categoryId.includes(Number(selectedModule[2]))))
}

/* check for home/featured page */
showOtfBtn(url: string): string {
  const [baseURL] = url.split('?');
  return baseURL === '/' || baseURL === '/home/featured'?'/home/featured':baseURL;
}
}
