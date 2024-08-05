import { Injectable } from '@angular/core';
import { SegmentEventManagerService } from '@lazy-modules/segmentEventManager/service/segment-event-manager.service';

@Injectable({ providedIn: 'root' })
export class SegmentedCMSEndPointService {
    constructor(private segmentEventManagerService: SegmentEventManagerService) { }

    /**
     * get the CMS segmented init endpoint
     * @returns string
     */
    getInitialDataEndPoint(): string {
        const segmentValue = this.segmentEventManagerService.getSegmentDetails();
        if (segmentValue) {
            return `initial-data/segment/${segmentValue}/mobile`;
        } else {
            return `initial-data/mobile`;
        }
    }
}
