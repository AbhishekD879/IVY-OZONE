import { Injectable } from '@angular/core';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { Configuration } from '@app/client/private/models/configuration.model';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { ISegment } from '@app/client/private/models/segment.model';
import { Observable } from 'rxjs';

@Injectable()
export class SegmentManagerService extends AbstractService<Configuration>{
    constructor(http: HttpClient, domain: string, brand: string) {
        super(http, domain, brand);
    }

    /*
     * @returns list of segments
     */
    public getSegments(): Observable<HttpResponse<ISegment[]>> {
        const uri = `segments/brand/${this.brand}`;
        return this.sendRequest<ISegment[]>('get', uri, null);
    }

    /**
     * deletes the segments
     * @param segmentIds
     */
    public deleteSegments(segmentIds: string): Observable<HttpResponse<ISegment[]>> {
        const uri = `segments/${segmentIds}/brand/${this.brand}`;
        return this.sendRequest<ISegment[]>('delete', uri, null);
    }
}