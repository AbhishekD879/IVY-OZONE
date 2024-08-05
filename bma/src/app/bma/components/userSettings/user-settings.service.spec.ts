import { UserPreferenceProvider } from './user-settings.service';
import { of as observableOf } from 'rxjs';

describe('UserPreferenceProvider', () => {
    let service: UserPreferenceProvider;
    let http;

    beforeEach(() => {
        http = {
            put: jasmine.createSpy().and.returnValue(observableOf({ body: {} })),
            get: jasmine.createSpy().and.returnValue(observableOf({ body: {} }))
        };
        service = new UserPreferenceProvider(http);
    });

    it('constructor', () => {
        expect(service).toBeDefined();
    });

    it('should call getOddsPreference', () => {
        service.getOddsPreference('');
        expect(service).toBeDefined();
    });

    it('should call setOddsPreference', () => {
        const perf = {brand:'bma'}
        service.setOddsPreference(perf, '');
        expect(service).toBeDefined();
    });
});