import { SegmentStoreService } from './segment-store.service';
import { CSPSegmentConstants } from '@app/app.constants';
// import { of } from 'rxjs';
// import { RoutesRecognized } from '@angular/router';
import { RouterStateService } from './routers/router-state.service';
import { ISegmentModel } from '../models/segment.model';
import { Location } from '@angular/common';

describe('SegmentStoreService', () => {

    let service: SegmentStoreService;
    let location: Location;
    let routerState: RouterStateService
    
    beforeEach(() => {
        service = new SegmentStoreService(location, routerState);
    });

    it('should set the universal value', () => {
        let segmentObject: ISegmentModel = { exclusionList: [], inclusionList: [], universalSegment: true };
        let module: string = 'test-module';
        let expectedObj: any = { segmentModule: module, segmentValue: CSPSegmentConstants.UNIVERSAL_TITLE }
        service.setSegmentValue(segmentObject, module);
        expect(service.updateSegmentMessage).toHaveBeenCalledWith(expectedObj);
    });

    it('should set the segment value', () => {
        let segmentObject: ISegmentModel = { exclusionList: [], inclusionList: ['test'], universalSegment: false };
        let module: string = 'test-module';
        let expectedObj: any = { segmentModule: module, segmentValue: 'test' }
        service.setSegmentValue(segmentObject, module);
        expect(service.updateSegmentMessage).toHaveBeenCalledWith(expectedObj);
    });

    it('should call the initSegmentObject call', () => {
        spyOn<any>(service, 'initSegmentObj');
        service.validateSegmentValue();
        expect(service.initSegmentObj).toHaveBeenCalled();
    });
});