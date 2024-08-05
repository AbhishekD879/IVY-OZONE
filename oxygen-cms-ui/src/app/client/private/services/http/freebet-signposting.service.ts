import { AbstractService } from './transport/abstract.service';
import { Configuration } from '../../models/configuration.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { SignpostingInfo } from '@root/app/signposting/models/signposting.model';


@Injectable()
export class FreebetSignpostingService extends AbstractService<Configuration> {
    signpostingUrl: string = 'signposting';

    constructor(http: HttpClient, domain: string, brand: string) {
        super(http, domain, brand);
    }

    getAllSignpostings(): Observable<HttpResponse<SignpostingInfo[]>> {
        const uri = `${this.signpostingUrl}/brand/${this.brand}`;
        return this.sendRequest<SignpostingInfo[]>('get', uri, null);
    }

    getSignposting(id: string): Observable<HttpResponse<SignpostingInfo>> {
        const uri = `${this.signpostingUrl}/${id}`;
        return this.sendRequest<SignpostingInfo>('get', uri, null);
    }

    createSignposting(signpostingInfo: SignpostingInfo): Observable<HttpResponse<SignpostingInfo>> {
        return this.sendRequest<SignpostingInfo>('post', this.signpostingUrl, signpostingInfo);
    }

    updateSignposting(updateData: SignpostingInfo): Observable<HttpResponse<SignpostingInfo>> {
        const uri = `${this.signpostingUrl}/${updateData.id}`;
        return this.sendRequest<SignpostingInfo>('put', uri, updateData);
    }

    deleteSignposting(id: string): Observable<HttpResponse<void>> {
        const uri = `${this.signpostingUrl}/${id}`;
        return this.sendRequest<void>('delete', uri, null);
    }

}
