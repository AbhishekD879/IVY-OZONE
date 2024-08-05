import { HttpClient } from '@angular/common/http';
import { TinymceService } from '@app/client/private/services/http/tinymce.service';

describe('TinymceService', () => {
    let service: TinymceService;
    let http: HttpClient;
    let domain = 'abc';
    let brand = 'bma';

    beforeEach(() => {
        service = new TinymceService(http, domain, brand);
    })
    it('should initialize service', () => {
        expect(service).toBeDefined();
    })
})