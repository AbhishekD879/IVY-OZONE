import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ProductSwitchResolver } from './product-switch.resolver';
import { ProductService } from '@frontend/vanilla/core';
import { ProductActivatorService } from '@frontend/vanilla/shared/product-activation';

describe('ProductSwitchResolver', () => {

    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                {
                    provide: ProductService,
                    useValue: { current: { name: 'true' } },
                },
                {
                    provide: ProductActivatorService,
                    useValue: { activate: () => 'true' },
                }
            ],
        });
    })
    it('should call', fakeAsync(() => {
        const guard = TestBed.runInInjectionContext(() => ProductSwitchResolver({ root: { data: { 'product': 'res' } } } as any, {} as any) as any) as any;
        tick();
    }))

    // fit('should call', fakeAsync(() => {
        
    //     // const actualResult = TestBed.runInInjectionContext(() => ProductSwitchResolver({ root: { data: {} } } as any, {} as any) as any) as any;
    //     expect( () =>TestBed.runInInjectionContext(() => ProductSwitchResolver({ root: { data: {} } } as any, {} as any) as any) as any).toThrow(new Error());
    //     // actualResult.catch('errorHandler');
    //     tick();
    // }))
});
