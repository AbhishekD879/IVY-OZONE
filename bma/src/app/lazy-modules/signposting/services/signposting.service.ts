import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import { map } from 'rxjs/operators';
import { SignpostingCMSConfig } from "app/lazy-modules/signposting/models/freebet-signposting.model";


@Injectable({
    providedIn: 'root'
})

export class SignpostingCmsService {
    CMS_ENDPOINT: string;
    brand: string = environment.brand;
    freeBetSignpostingArray: SignpostingCMSConfig[];
    gtmLoadingStatus: any = {
        betslip: false,
        quickbet: false
    }

    constructor(
        protected http: HttpClient
    ) {
        this.CMS_ENDPOINT = environment.CMS_ENDPOINT;
    }

    /**
     * @param  {string} url
     * @param  {any={}} params
     * @returns Observable
     */
    getData<T>(url: string, params: any = {}): Observable<HttpResponse<T>> {
        return this.http.get<T>(`${this.CMS_ENDPOINT}/${this.brand}/${url}`, {
            observe: 'response',
            params: params
        });
    }

    //Freebet Signposting
    /**
     * @returns Observable
     */
    getFreebetSignposting(): Observable<any> {
        return this.getData(`signposting`)
            .pipe(
                map((data: HttpResponse<SignpostingCMSConfig>) => data.body)
            );
    }

}
