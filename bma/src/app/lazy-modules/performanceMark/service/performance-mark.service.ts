import { Injectable } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { PERFORMANCE_API_MARK, PERFORMANCE_API_MEASURE } from '../enums/performance-mark.enums';
@Injectable()
export class PerformanceMarkService {
    constructor(private pubsubService: PubSubService) {
        this.pubsubService.subscribe('pefromanceMark', this.pubsubService.API.PERFORMANCE_MARK, () => { this.addMarkMeasure(); });
    }
    addMarkMeasure(): void {
        try {
            if (performance.getEntriesByName(PERFORMANCE_API_MARK.TTI, PERFORMANCE_API_MARK.Mark).length > 0) {
                performance.clearMarks(PERFORMANCE_API_MARK.TTI);
            }
            if (performance.getEntriesByName(PERFORMANCE_API_MEASURE.NAV, PERFORMANCE_API_MEASURE.Measure).length > 0) {
                performance.clearMeasures(PERFORMANCE_API_MEASURE.NAV);
            }
            performance.mark(PERFORMANCE_API_MARK.TTI);
            performance.measure(PERFORMANCE_API_MEASURE.NAV, PERFORMANCE_API_MARK.CTI, PERFORMANCE_API_MARK.TTI);
        } catch (e) {
            console.warn('Error in marking TTI values in performance service',e);
        }
    }
}
