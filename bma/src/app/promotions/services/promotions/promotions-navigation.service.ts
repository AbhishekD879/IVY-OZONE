import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ILeaderBoard, INavigationGroup } from '@promotions/models/sp-promotion.model';
import environment from '@environment/oxygenEnvConfig';

@Injectable()
export class PromotionsNavigationService {
    CMS_ENDPOINT: string;
    brand: string = environment.brand;

    public isNavGroup: BehaviorSubject<INavigationGroup[]> = new BehaviorSubject([] as INavigationGroup[]);

    constructor(
        protected http: HttpClient
    ) {
        this.CMS_ENDPOINT = environment.CMS_ENDPOINT;
    }

    /**
   * makes get data to the provided url
   * @param {string} url
   * @param {any} params
   * @returns {Observable<HttpResponse<T>>}
   */
    protected getData<T>(url: string, params: any = {}): Observable<HttpResponse<T>> {
        return this.http.get<T>(`${this.CMS_ENDPOINT}/${this.brand}/${url}`, {
            observe: 'response',
            params: params
        });
    }

    /**
   * Sets next value of behaviour subject
   * @param {INavigationGroup[]} params
   */
    public setNavGroupData(params: INavigationGroup[]): void {
        this.isNavGroup.next(params);
    }

    /**
    * Call to get navigation group
    * @returns {Observable<INavigationGroup[]>}
    */
    public getNavigationGroups(): Observable<INavigationGroup[]> {
        return this.getData('navigation-group').pipe(
            map((navData: HttpResponse<INavigationGroup[]>) => navData.body));
    }

    /**
    * Call to get promo Leader board
    * @returns {Observable<ILeaderBoard[]>}
    */
    public getLeaderBoards(): Observable<ILeaderBoard[]> {
        return this.getData('promo-leaderboard').pipe(
            map((ldData: HttpResponse<ILeaderBoard[]>) => ldData.body));
    }    
}
