import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { Configuration } from "@app/client/private/models/configuration.model";
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { TopSportsInfo } from '@app/virtual-sports/top-sports/models/top-sports.model';

@Injectable()
export class VirtualHubTopSportsService extends AbstractService<Configuration> {
    topSportsUrl: string = 'topsports';

    constructor(http: HttpClient, domain: string, brand: string) {
        super(http, domain, brand);
    }

    getAllTopSports(): Observable<HttpResponse<TopSportsInfo[]>> {
        const uri = `${this.topSportsUrl}/brand/${this.brand}`;
        return this.sendRequest<TopSportsInfo[]>('get', uri, null);
    }

    getTopSports(id: string): Observable<HttpResponse<TopSportsInfo>> {
        const uri = `${this.topSportsUrl}/${id}`;
        return this.sendRequest<TopSportsInfo>('get', uri, null);
    }

    createTopSports(TopSportsInfo: TopSportsInfo): Observable<HttpResponse<TopSportsInfo>> {
        return this.sendRequest<TopSportsInfo>('post', this.topSportsUrl, TopSportsInfo);
    }

    updateTopSports(updateData: TopSportsInfo): Observable<HttpResponse<TopSportsInfo>> {
        const uri = `${this.topSportsUrl}/${updateData.id}`;
        return this.sendRequest<TopSportsInfo>('put', uri, updateData);
    }

    deleteTopSports(id: string): Observable<HttpResponse<void>> {
        const uri = `${this.topSportsUrl}/${id}`;
        return this.sendRequest<void>('delete', uri, null);
    }

}
