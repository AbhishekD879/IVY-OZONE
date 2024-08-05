import { Injectable } from "@angular/core";
import { RssRewards } from "@app/client/private/models/coins-rewards.model";
import { AbstractService } from "./transport/abstract.service";
import { HttpClient, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";

@Injectable()
export class RssRewardsService extends AbstractService<RssRewards> {
    constructor(http: HttpClient, domain: string, brand: string) {
        super(http, domain, brand);
        this.uri = `rss-rewards`;
    }
    public get(): Observable<HttpResponse<RssRewards>> {
        const uri = `${this.uri}/brand/${this.brand}`;
        return this.sendRequest<RssRewards>('get', uri, null);
    }
    public update(rssRewards: RssRewards): Observable<HttpResponse<RssRewards>> {
        const uri = `${this.uri}/${rssRewards.id}`;
        return this.sendRequest<RssRewards>('put', uri, rssRewards);
    }
    public create(rssRewards: RssRewards): Observable<HttpResponse<RssRewards>> {
        const uri = `${this.uri}`;
        return this.sendRequest<RssRewards>('post', uri, rssRewards);
    }
}