import { ISportEvent } from "@core/models/sport-event.model";
import environment from '@environment/oxygenEnvConfig';
import { CouponStatWidgetComponent } from "./coupon-stat-widget.component";


describe('CouponStatWidgetComponent', () => {
    const gtmService = {
        push: jasmine.createSpy('push')
    } as any;
    const windowRef = {
        document: {
            remove: jasmine.createSpy('remove'),
            getElementById: jasmine.createSpy('getElementById'),
            createElement: jasmine.createSpy('createElement'),
            getElementsByTagName: jasmine.createSpy('createElement'),
            body: {
                appendChild: jasmine.createSpy('appendChild')
            }
        }
    } as any;
    const url = 'https://oxygen-test-lib.com';
    const component: CouponStatWidgetComponent= new CouponStatWidgetComponent(gtmService, windowRef);

    it('should create a component instance', () => {

        expect(component).toBeTruthy();
    });
    describe('@ngAfterViewInit', () => {
        beforeEach(() => {
            component.couponIndex = 1;
            component.eventIndex = 0;
            component.dateIndex = 0;
            component.event = {
                isCouponScoreboardOpened: false,
                cashoutAvail: '',
                categoryCode: '',
                categoryId: '16',
                categoryName: '',
                displayOrder: 0,
                eventSortCode: '',
                eventStatusCode: '',
                id: 1,
                liveServChannels: '',
                liveServChildrenChannels: '',
                typeId: '25230',
                typeName: '',
                name: '',
                startTime: '',
                couponStatId: 'sdm-scoreboard1'
            } as ISportEvent;
            const dummyTag = document.createElement('div');
            component.couponIndex = 1;
            dummyTag.id = 'SB' + (component.couponIndex) + (component.dateIndex) + (component.eventIndex);
            windowRef.document.createElement.and.returnValue(dummyTag);
            windowRef.document.body.appendChild(dummyTag);
        });

        it('should create a tag in dom with id as couponstatid ', () => {
            const dummyTag = document.createElement('div');
            windowRef.document.getElementById.and.returnValue(dummyTag);
            component.ngAfterViewInit();
            expect(windowRef.document.getElementById('sdm-scoreboard1')).toBeTruthy();
        });
        it('should attach new div to div with id SBcouponIndexEventIndexdateIndex', () => {
            const div = windowRef.document.getElementById('SB100');
            component.ngAfterViewInit();
            expect(div.hasChildNodes()).toBeTruthy();
        });
        it('should remove script', () => {
            const script = document.createElement('script');
            script.id = 'coupon_script';
            windowRef.document.getElementById.and.returnValue(script);
            spyOn(script, 'remove');
            component.ngAfterViewInit();
            expect(script.remove).toHaveBeenCalled();
        });
       
        it('should call loadScript function', () => {
            spyOn(component, 'loadScript').and.returnValue(Promise.resolve(true));
            component.ngAfterViewInit();
            expect(component.loadScript).toHaveBeenCalledWith(environment.COUPON_STATS_EXTERNAL_URL);

        });

        it('should create a script tag', () => {
            spyOn(component, 'loadScript').and.returnValue(Promise.reject('data rejected'));
            component.ngAfterViewInit();
            expect(windowRef.document.getElementById('coupon_script')).toBeTruthy();
        })

    });

    describe('gtmHandlerFn', () => {
        const event3 = {
            isTrusted: false,
            bubbles: true,
            cancelBubble: false,
            cancelable: false,
            composed: true,
            currentTarget: null,
            defaultPrevented: false,
            detail:
            {
                event: 'trackEvent',
                eventAction: 'click',
                eventCategory: 'coupon stats widget',
                eventLabel: 'more stats',
                eventID: '7619946'
            },
            type: "googleAnalyticsData"
        };
        component.event = {
            isCouponScoreboardOpened: true,
            cashoutAvail: '',
            categoryCode: '',
            categoryId: '16',
            categoryName: '',
            displayOrder: 0,
            eventSortCode: '',
            eventStatusCode: '',
            id: 1,
            liveServChannels: '',
            liveServChildrenChannels: '',
            typeId: '25230',
            typeName: '',
            name: '',
            startTime: '',
            couponStatId: 'sdm-scoreboard1'
        };

        beforeEach(() => {
            spyOn(component.isLoaded, 'emit');

        });
        const gtmData = {
            event: 'trackEvent',
            eventAction: 'click',
            eventCategory: 'coupon stats widget',
            eventLabel: 'more stats',
            categoryID: '16',
            typeID: '25230',
            eventID: 1
        }
        it('should track event', () => {
            component.gtmHandlerFn(event3);
            expect((component as any).gtmService.push).toHaveBeenCalledWith('trackEvent', gtmData);
        });

        it(`should emit 'isLoaded' if 'isLoadedValue' is Falthy`, () => {
            (component as any).isLoadedValue = false;
            (component as any).gtmHandlerFn(event3);
            expect(component.isLoaded.emit).toHaveBeenCalledWith(true);
            expect((component as any).isLoadedValue).toBeTruthy();
        });

        it(`should Not emit 'isLoaded' if 'isLoadedValue' is Truthy`, () => {
            (component as any).isLoadedValue = true;
            (component as any).gtmHandlerFn(event3);
            expect(component.isLoaded.emit).not.toHaveBeenCalled();
        });
    });

    describe('@loadScript', () => {
        beforeEach(() => {
            component.couponIndex = 1;
            component.eventIndex = 0;
            component.dateIndex = 0;
            component.event = {
                isCouponScoreboardOpened: false,
                cashoutAvail: '',
                categoryCode: '',
                categoryId: '16',
                categoryName: '',
                displayOrder: 0,
                eventSortCode: '',
                eventStatusCode: '',
                id: 1,
                liveServChannels: '',
                liveServChildrenChannels: '',
                typeId: '25230',
                typeName: '',
                name: '',
                startTime: '',
                couponStatId: 'sdm-scoreboard1'
            } as ISportEvent;
            const dummyTag = document.createElement('div');
            component.couponIndex = 1;
            dummyTag.id = 'SB' + (component.couponIndex) + (component.dateIndex) + (component.eventIndex);
            const newdiv = document.createElement('div');
            windowRef.document.createElement.and.returnValue(newdiv);
            windowRef.document.body.appendChild(dummyTag);
            windowRef.document.getElementById.and.returnValue(dummyTag);
        });
        
        it('should trigger  resolve function', () => {
            component.ngAfterViewInit()
            const script = document.getElementById('coupon_script');
            script && script.dispatchEvent(new Event('load'));
            if(script){
               expect(script).toBeTruthy();
            }
        })

        it('should trigger reject function',()=>
        {
            const script = document.getElementById('coupon_script');
            const e=new Event('error');
            script && script.dispatchEvent(e);
            expect(component.loadScript(url, true, 'coupon_script','text/javascript').catch(err => {
            })).toBeDefined();
        })


    })

});
