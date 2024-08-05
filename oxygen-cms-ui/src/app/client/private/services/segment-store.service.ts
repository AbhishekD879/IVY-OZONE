import { Injectable } from '@angular/core';
import { ISegmentModel, ISegmentMsg } from '@app/client/private/models/segment.model';
import { CSPSegmentConstants } from '@app/app.constants';
import { BehaviorSubject, Observable } from 'rxjs';
import { Location } from '@angular/common';
import { RouterStateService } from './routers/router-state.service';
import { IRouterStateModel } from './routers/route.model';

@Injectable({ providedIn: 'root' })
export class SegmentStoreService {
    private segmentInitObj = { segmentModule: '', segmentValue: '' };
    private segmentMsg: BehaviorSubject<ISegmentMsg> = new BehaviorSubject<ISegmentMsg>(this.segmentInitObj);

    constructor(private location: Location, private routerState: RouterStateService) {
    }

    public getSegmentMessage(): Observable<ISegmentMsg> {
        return this.segmentMsg.asObservable();
    }

    public updateSegmentMessage(message: ISegmentMsg): void {
        this.segmentMsg.next(message);
    }

    // update behavior subject data to initial data
    public initSegmentObj() {
        this.segmentMsg.next(this.segmentInitObj);
    }

    public setSegmentValue(segmentObject: ISegmentModel, module_name: string): void {
        let segmentValue;
        if (!segmentObject.universalSegment && segmentObject.inclusionList && segmentObject.inclusionList.length > 0) {
            segmentValue = segmentObject.inclusionList[0];
        }
        else {
            segmentValue = CSPSegmentConstants.UNIVERSAL_TITLE;
        }
        this.updateSegmentMessage(
            { segmentModule: module_name, segmentValue: segmentValue });
    }

    public validateSegmentValue() {
        const routerObj: IRouterStateModel = this.routerState.getRouterState();
        if (routerObj.previousUrl && (routerObj.previousUrl.indexOf(routerObj.currentUrl) === -1)) {
            this.initSegmentObj();
        }
    }

    public validateHomeModule() {
        // return true if path has homepage.
        return this.location.path().includes('homepage');
    }
}