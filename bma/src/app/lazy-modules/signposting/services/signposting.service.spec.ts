
import { of } from 'rxjs';
import { SignpostingCmsService } from 'app/lazy-modules/signposting/services/signposting.service';
import environment from '@environment/oxygenEnvConfig';

const httpResponse = {};
const responseBody = {};
describe('Signposting Cms Service', () => {
    let service: SignpostingCmsService,
        httpServiceStub, httpClient;

    beforeEach(() => {
        httpClient = {
            get: jasmine.createSpy('get').and.returnValue(of({ body: [] }))
        };

        service = new SignpostingCmsService(httpClient);

    });

    it('constructor', () => {
        expect(service).toBeTruthy();
        expect(service['CMS_ENDPOINT']).toBe(environment.CMS_ENDPOINT);
        expect(service['brand']).toBe(environment.brand);
    });

    it('should call getData() with params', () => {
        const url = 'signposting', options = { option: 'option' };
        service['getData'](url, options);
        expect(httpClient.get).toHaveBeenCalled();
        expect(httpClient.get).toHaveBeenCalledWith(
            `${environment.CMS_ENDPOINT}/${environment.brand}/${url}`,
            { observe: 'response', params: options }
        );
    });

    it('should call getData() without params', () => {
        const url = 'signposting';
        service['getData'](url);
        expect(httpClient.get).toHaveBeenCalled();
        expect(httpClient.get).toHaveBeenCalledWith(
            `${environment.CMS_ENDPOINT}/${environment.brand}/${url}`,
            { observe: 'response', params: {} }
        );
    });

    it('#getFreebetSignposting', () => {
        service['getData'] = jasmine.createSpy().and.returnValue(of({ body: responseBody }));
        service.getFreebetSignposting().subscribe((data) => {
            expect(service['getData']).toHaveBeenCalledWith(`signposting`);
            expect(data).toBe(responseBody);
        });
    });
});
