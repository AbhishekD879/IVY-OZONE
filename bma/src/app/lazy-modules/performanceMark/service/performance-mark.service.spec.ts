import { PerformanceMarkService } from './performance-mark.service';
import { PERFORMANCE_API_MARK, PERFORMANCE_API_MEASURE } from '../enums/performance-mark.enums';
describe('PerformanceMarkService', () => {
    let service: PerformanceMarkService;
    let pubsubService;
    beforeEach(() => {
        pubsubService = {
            subscribe: jasmine.createSpy('subscribe'),
            API: {
                PERFORMANCE_MARK: 'PERFORMANCE_MARK'
            }
        };
        service = new PerformanceMarkService(pubsubService);
        performance.clearMarks();
    });
    describe('Performance Mark', () => {
        it('Calling PerformanceMark Without BMA:TTI', () => {
            performance.mark(PERFORMANCE_API_MARK.CTI);
            service.addMarkMeasure();
            expect(performance.getEntriesByName(PERFORMANCE_API_MEASURE.NAV, PERFORMANCE_API_MEASURE.Measure)[0].duration > 0);
        });
        it('Calling PerformanceMark With BMA:TTI', () => {
            performance.mark(PERFORMANCE_API_MARK.TTI);
            performance.mark(PERFORMANCE_API_MARK.CTI);
            service.addMarkMeasure();
            expect(performance.getEntriesByName(PERFORMANCE_API_MEASURE.NAV, PERFORMANCE_API_MEASURE.Measure)[0].duration > 0);
        });
        it('Calling PerformanceMark With BMA:NAV', () => {
            performance.mark(PERFORMANCE_API_MARK.TTI);
            performance.mark(PERFORMANCE_API_MARK.CTI);
            performance.measure(PERFORMANCE_API_MEASURE.NAV, PERFORMANCE_API_MARK.CTI, PERFORMANCE_API_MARK.TTI);
            performance.mark(PERFORMANCE_API_MARK.TTI);
            service.addMarkMeasure();
            expect(performance.getEntriesByName(PERFORMANCE_API_MEASURE.NAV, PERFORMANCE_API_MEASURE.Measure).length === 1);
        });
        it('should catch error', () => {
            spyOn(console, 'warn');
            performance = undefined;
            service.addMarkMeasure();
            expect(console.warn).toHaveBeenCalled();
          });
    });
});
