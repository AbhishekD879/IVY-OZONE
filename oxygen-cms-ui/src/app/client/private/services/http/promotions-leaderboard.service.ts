
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Order } from '@app/client/private/models/order.model';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { Observable } from 'rxjs/Observable';
import { Leaderboard, Leaderboards, PromoLeaderboard, PromotionsLeaderboard } from '@app/client/private/models/promotions-leaderboard.model';

@Injectable()
export class PromotionsLeaderboardService extends AbstractService<any[]> {
    constructor(http: HttpClient, domain: string, brand: string) {
        super(http, domain, brand);
        this.uri = `leaderboard`;

    }
    leaderboardColumn = `leaderboard-column`;
    leaderBoardUri = `promo-leaderboard`;

    /**
    * Posts new Leaderboard.
    * @param - {Leaderboard} leaderboard
    * @returns - HttpResponse<PromoLeaderboard>
    */
    public postNewLeaderboard(leaderboard: Leaderboard): Observable<HttpResponse<PromoLeaderboard>> {
        return this.sendRequest<PromoLeaderboard>('post', this.leaderBoardUri, leaderboard);
    }


    /**
     * Posts new order for Nav Items.
     * @param - {Order} order
     * @returns - void
     */
    public postNewNavItemOrder(order: Order): Observable<HttpResponse<void>> {
         return this.sendRequest<void>('post', `${this.leaderboardColumn}/ordering`, order);
    }

    /**
   * Get All Nav Groups by brand.
   * @returns - PromotionsLeaderboard[]
   */
    public findAllByBrand(): Observable<HttpResponse<PromotionsLeaderboard[]>> {
        return this.sendRequest<PromotionsLeaderboard[]>('get', `${this.leaderBoardUri}/brand/${this.brand}`, null);
    }

    /**
     * Update Leaderboard
     * @param - {PromoLeaderboard} Leaderboard
     * @param - {boolean} isFileChanged
     * @returns - PromoLeaderboard
     */
    public updateLeaderboard(leaderboard: PromoLeaderboard, isFileChanged?: boolean): Observable<HttpResponse<PromoLeaderboard>> {
        leaderboard.brand = this.brand;
        const uri = `${this.leaderBoardUri}/${leaderboard.id}`;
        return this.sendRequest<PromoLeaderboard>('put', uri, leaderboard, `isFileChanged=${isFileChanged}`);
    }

    /**
     * remove Leaderboard.
     * @param {string} id
     * @returns - void
     */
    public remove(id: string): Observable<HttpResponse<void>> {
        const uri = `${this.leaderBoardUri}/${id}`;
        return this.sendRequest<void>('delete', uri, null);
    }

    /**
     * get Leaderboard Item by ID
     * @param - {string} id
     * @returns - PromoLeaderboard
     */
    public getLeaderboardById(id: string): Observable<HttpResponse<PromoLeaderboard>> {
        const uri = `${this.leaderBoardUri}/${id}`;
        return this.sendRequest<PromoLeaderboard>('get', uri, null);
    }

    /**
     * Get All active Leaderboards
     * @returns - Leaderboards[]
     */
    public getActiveLeaderboard(): Observable<HttpResponse<Leaderboards[]>> {
        return this.sendRequest<Leaderboards[]>('get', `${this.leaderBoardUri}/active/brand/${this.brand}`, null);
    }

    /**
     * Upload file
     * @returns - any
     */
    public uploadCSVFile(file: FormData): Observable<HttpResponse<any>> {
        const fileUpload = 'file-upload-s3';
        return this.sendRequest<any>('put', `${fileUpload}/${this.brand}`, file);
    }
}