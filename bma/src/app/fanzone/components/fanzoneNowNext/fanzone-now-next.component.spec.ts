import * as _ from 'underscore';
import { FanzoneAppNowNextComponent } from '@app/fanzone/components/fanzoneNowNext/fanzone-now-next.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { featuredModuleMock, featuredDataMock, featuredQuickLinksMock, surfaceBetModule, footballEventMock, eventMock } from '@app/featured/components/featured-module/featured-module.component.mock';
import { fanzoneCleanModuleMock, fanzoneSegmentMock } from '@app/fanzone/mockData/fanzone-now-next.component.mock';
import { fakeAsync } from '@angular/core/testing';
import { FANZONECONFIG } from '@app/fanzone/guards/mockdata/fanzone-auth-guardservice.mock';

describe('FanzoneAppNowNextComponent', () => {
    let component: FanzoneAppNowNextComponent;

    let pubsub;
    let fanzoneStorageService;
    let changeDetectorRef;
    let fanzoneFeaturedService;
    let fanzoneHelperService;
    let wsUpdateEventService;
    beforeEach(() => {
        pubsub = {
            cbMap: {},
            publish: jasmine.createSpy('publish'),
            subscribe: jasmine.createSpy('subscribe').and.callFake((name, method, cb) => pubsub.cbMap[method] = cb),
            unsubscribe: jasmine.createSpy('unsubscribe'),
            API: pubSubApi
        };
        fanzoneFeaturedService = {
            addEventListener: jasmine.createSpy(),
            reconnect: jasmine.createSpy(),
            startConnection: jasmine.createSpy(),
            onError: jasmine.createSpy(),
            clearSubscribedFeaturedTabModules: jasmine.createSpy(),
            disconnect: jasmine.createSpy(),
            cacheEvents: jasmine.createSpy(),
            addModuleToSubscribedFeaturedTabModules: jasmine.createSpy(),
            tabModuleStates: new Map(),
            emit: jasmine.createSpy(),
            addClock: jasmine.createSpy().and.callFake((args) => args),
            getSubscribedFeaturedTabModules: jasmine.createSpy().and.returnValue(['1', '2', '3']),
            removeAllListeners: jasmine.createSpy(),
            removeEventListener: jasmine.createSpy(),
            trackDataReceived: jasmine.createSpy('trackDataReceived'),
        };

        changeDetectorRef = {
            detach: jasmine.createSpy('detach'),
            detectChanges: jasmine.createSpy('detectChanges'),
            markForCheck: jasmine.createSpy('markForCheck')
        };

        fanzoneStorageService = {
            set: jasmine.createSpy('fanzoneStorageService.set'),
            get: jasmine.createSpy('fanzoneStorageService.get').and.returnValue(fanzoneSegmentMock)
        };
        wsUpdateEventService = {
            subscribe: jasmine.createSpy()
          };

        fanzoneHelperService = {};

        component = new FanzoneAppNowNextComponent(
            fanzoneFeaturedService,
            pubsub,
            changeDetectorRef,
            fanzoneStorageService,
            fanzoneHelperService,
            wsUpdateEventService
        );

        component.fanzoneModuleData = {
            directiveName: null,
            modules: [],
            showTabOn: null,
            title: null,
            visible: null
        };
    });

    it('needed constructor methods', () => {
        component['fanzoneOnSocketUpdate'] = jasmine.createSpy();
        component['onSocketUpdate'](featuredModuleMock);

        expect(component['fanzoneOnSocketUpdate']).toHaveBeenCalledWith(featuredModuleMock as any);
    });

    describe('ngOnInit', () => {
        it('should get fanzone details data ', fakeAsync(() => {
            component['pubsub'].subscribe = jasmine.createSpy('pubSubService.subscribe')
                .and.callFake((filename: string, eventName: string, callback: Function) => {
                    if (eventName === 'FANZONE_DATA') {
                        callback(FANZONECONFIG);

                        expect(component.fanzoneDetails).toBeDefined();
                    }
                });
            component.ngOnInit();
        }));

        it('should init connection during  initialisation', () => {
            const sportIdMock = 160;
            fanzoneStorageService.get = jasmine.createSpy('fanzoneStorageService.get').and.returnValue(fanzoneSegmentMock);

            component['fanzoneFeaturedService'].onError = jasmine.createSpy('onError').and.callFake((callback) => {
                callback();
                expect(component.ssDown).toBeTruthy();
                expect(component.fanzoneModuleData).toBeDefined();
                expect(component.showLoader).toBeFalsy();
            });
            component['pubsub'].subscribe = jasmine.createSpy('subscribe').and.callFake((namespace, message, callback) => {
                if (message === 'FEATURED_CONNECT_STATUS') {
                    component['fanzoneFeaturedService'].addEventListener = jasmine.createSpy('addEventListener')
                        .and.callFake((messageText, callbackFn) => {
                            if (messageText === 'FEATURED_STRUCTURE_CHANGED') {
                                callbackFn(Object.assign({}, featuredDataMock));
                                expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.FEATURED_STRUCTURE_CHANGED, []);
                                expect(component['fanzoneFeaturedService'].emit).toHaveBeenCalledWith('login', fanzoneSegmentMock.teamId);
                            }
                        });

                    callback(false);
                    expect(component['fanzoneFeaturedService'].addEventListener)
                        .not.toHaveBeenCalled();

                    callback(true);
                    expect(component.showLoader).toBeFalsy();
                    expect(component.isConnectSucceed).toBeTruthy();
                    expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
                    expect(component['fanzoneFeaturedService'].addEventListener)
                        .toHaveBeenCalledWith('FEATURED_STRUCTURE_CHANGED', jasmine.any(Function));

                }
            });

            component['pubsub'].subscribe = jasmine.createSpy('subscribe').and.callFake((namespace, message, callback) => {
                callback();
                expect(component.showLoader).toBeFalsy();
                expect(component.ssDown).toBeTruthy();
            });


            component['fanzoneFeaturedService'].onError = jasmine.createSpy('onError').and.callFake((callback) => {
                callback();
                expect(component.ssDown).toBeTruthy();
                expect(component.fanzoneModuleData).toBeDefined();
                expect(component.showLoader).toBeFalsy();
            });
            component['pubsub'].subscribe = jasmine.createSpy('subscribe').and.callFake((namespace, message, callback) => {
                if (message[0] && message[0] === 'RELOAD_FEATURED') {
                    callback();
                    expect(fanzoneFeaturedService.reconnect).toHaveBeenCalled();
                    expect(component.showLoader).toBeTruthy();
                    expect(component.isConnectSucceed).toBeTruthy();
                    expect(component.ssDown).toBeFalsy();
                }

                if (message === 'FEATURED_CONNECT_STATUS') {
                    component['fanzoneFeaturedService'].addEventListener = jasmine.createSpy('addEventListener')
                        .and.callFake((messageText, callbackFn) => {
                            if (messageText === 'FEATURED_STRUCTURE_CHANGED') {
                                callbackFn(Object.assign({}, featuredDataMock));
                                expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.FEATURED_STRUCTURE_CHANGED, []);
                            }
                        });

                    callback(false);
                    expect(component['fanzoneFeaturedService'].addEventListener)
                        .not.toHaveBeenCalled();

                    callback(true);
                    expect(component.showLoader).toBeFalsy();
                    expect(component.isConnectSucceed).toBeTruthy();
                    expect(component['fanzoneFeaturedService'].addEventListener)
                        .toHaveBeenCalledWith('FEATURED_STRUCTURE_CHANGED', jasmine.any(Function));
                }

                if (message === 'NAMESPACE_ERROR') {
                    callback();
                    expect(component.showLoader).toBeFalsy();
                    expect(component.ssDown).toBeTruthy();
                }
            });

            component.ngOnInit();
            expect(fanzoneFeaturedService.startConnection).toHaveBeenCalledWith(sportIdMock, 'sport');
        });
        // test

        it('should not init connection if segment is null', () => {
            const sportIdMock = 160;
            fanzoneStorageService.get = jasmine.createSpy('fanzoneStorageService.get').and.returnValue(fanzoneSegmentMock);

            component['pubsub'].subscribe = jasmine.createSpy('subscribe').and.callFake((namespace, message, callback) => {
                if (message === 'FEATURED_CONNECT_STATUS') {
                    component['fanzoneFeaturedService'].addEventListener = jasmine.createSpy('addEventListener')
                        .and.callFake((messageText, callbackFn) => {
                            if (messageText === 'FEATURED_STRUCTURE_CHANGED') {
                                callbackFn(Object.assign({}, featuredDataMock));
                                expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.FEATURED_STRUCTURE_CHANGED, []);
                                expect(component['fanzoneFeaturedService'].emit).toHaveBeenCalledWith('login', `${fanzoneSegmentMock.teamId}`);
                            }
                        });

                    callback(false);
                    expect(component['fanzoneFeaturedService'].addEventListener)
                        .not.toHaveBeenCalled();

                    callback(true);
                    expect(component.showLoader).toBeFalsy();
                    expect(component.isConnectSucceed).toBeTruthy();
                    expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
                    expect(component['fanzoneFeaturedService'].addEventListener).toHaveBeenCalledWith('FEATURED_STRUCTURE_CHANGED', jasmine.any(Function));

                }
            });

            component.ngOnInit();
            expect(fanzoneFeaturedService.startConnection).toHaveBeenCalledWith(sportIdMock, 'sport');
        });
        // test
        it(`should subscribe on WS_EVENT_UPDATED`, () => {
            component.ngOnInit();

            expect(pubsub.subscribe).toHaveBeenCalledWith('fanzoneModule', 'WS_EVENT_UPDATED', jasmine.any(Function));

            changeDetectorRef.detectChanges.calls.reset();
            pubsub.cbMap['WS_EVENT_UPDATED']();

            expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
        });

        
        it('should detectChanges', () => {
            component.ngOnInit();

            expect(component['changeDetectorRef'].markForCheck).toHaveBeenCalled();
        });
        it('trackByModuleData', () => {
            const event = { id: '1', name: 'test event', startTime: 'Friday, 13th' } as any;
            const result = component.trackByModuleData(3, event);
      
            expect(result).toBe('3_1_test event_Friday, 13th');
          });
      
          it('trackByModules', () => {
            expect(component.trackByModules(0, <any>featuredModuleMock)).toEqual(
              `0_5b759926c9e77c000163eede_HO Football_-2`
            );
          });
      
          it('trackByModules for QL', () => {
            expect(component.trackByModules(0, <any>featuredQuickLinksMock)).toEqual(
              `0_featuredQuickLinksModuleId`
            );
          });
      
      
          it('trackByModules for module created by market id', () => {
            expect(
              component.trackByModules(0, {
                _id: '5b759924x77c500163eede',
                '@type': 'EventsModule',
                dataSelection: {selectionType: 'Market'}
              } as any)
            ).toEqual(
              `0_5b759924x77c500163eede`
            );
          });
        it('check init function call', () => {
            spyOn(component as any, 'addModulesEventListeners');
            spyOn(component as any, 'addEventListenersForEventsInModules');
            component.init(<any>featuredDataMock);

            const module: any = featuredModuleMock;

            expect(component['addModulesEventListeners']).toHaveBeenCalled();
            expect(component['addEventListenersForEventsInModules']).toHaveBeenCalled();
            expect(component.fanzoneModuleData).toEqual({
                directiveName: '',
                modules: [featuredModuleMock, featuredQuickLinksMock, surfaceBetModule],
                showTabOn: '',
                title: 'titel',
                visible: true
            } as any);
            expect(component.isModuleAvailable).toBe(true);
            expect(component.noEventFound).toBe(false);
        })
        it(`should subscribe on WS_EVENT_UPDATE`, () => {
                        component.ngOnInit();       
                        expect(pubsub.subscribe).toHaveBeenCalledWith('fanzoneModule', 'WS_EVENT_UPDATE', jasmine.any(Function));
            
                        changeDetectorRef.detectChanges.calls.reset();
                        pubsub.cbMap['WS_EVENT_UPDATE']();
            
                        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
                    });

        it('check init function call without data', () => {
            component.isConnectSucceed = true;
            component.init(null);

            expect(component.showLoader).toBeFalsy();
            expect(component.noEventFound).toBeTruthy();
            expect(component.isModuleAvailable).toBe(false);
        });

        it('check init function call when there are no modules', () => {
            component.init({ modules: [] } as any);

            expect(component.fanzoneModuleData.modules.length).toEqual(0);
        });

        it('should test if no event found', () => {
            component.isConnectSucceed = true;
            component.fanzoneModuleData = <any>{};
            component.showLoader = false;
            expect(component.checkNoEventFound()).toBeTruthy();
            component.ssDown = true;
            expect(component.checkNoEventFound()).toBeFalsy();
            component.ssDown = false;
            component.fanzoneModuleData.modules = [<any>{}];
            expect(component.checkNoEventFound()).toBeFalsy();
            component.fanzoneModuleData.modules = [<any>{ data: [] }];
            expect(component.checkNoEventFound()).toBeFalsy();
            component.fanzoneModuleData.modules = [<any>{ isLoaded: true, data: [] }];
            expect(component.checkNoEventFound()).toBeTruthy();
        });
        it('should call add listener for each module addEventListenersForEventsInModules', () => {
            spyOn(<any>component, 'addEventListenersWithinModule');

            const featuredModuledataMockClone: any = _.clone(featuredDataMock);

            component['addEventListenersForEventsInModules'](<any>featuredModuledataMockClone);

            expect(component['addEventListenersWithinModule']).toHaveBeenCalledTimes(3);
        });

        it('should getModuleIds', () => {
            const result = component['getModuleIds'](<any>featuredDataMock.modules);

            expect(result.indexOf('5b759926c9e77c000163eede') >= 0).toBeDefined();
            expect(result.indexOf('featuredQuickLinksModuleId') >= 0).toBeDefined();
        });
        it('other modules flow', () => {
            component['addEventListenersWithinModule'] = jasmine.createSpy();
            component['fanzoneOnSocketUpdate'](featuredModuleMock as any);

            expect(component['addEventListenersWithinModule']).toHaveBeenCalledWith(featuredModuleMock as any);
        });
        it('should just return', () => {
            const result = component.onModuleUpdate({} as any);
    
            expect(result).toBeUndefined();
          });
          it('should add clock to the module', () => {
            const moduleMock = {
              _id: '123',
              data: [
                {
                  categoryCode: 'GOLF',
                  eventSortCode: 'TNMT',
                  markets: [
                    {
                      templateMarketName: 'Win or Each Way'
                    }
                  ]
                }
              ]
            };
    
            const moduleNotToUpdate = {
              _id: '3',
              data: [
                {
                  categoryCode: 'GOLF',
                  eventSortCode: 'TNMT',
                  markets: [
                    {
                      templateMarketName: 'Win or Each Way'
                    }
                  ]
                }
              ]
            };
    
            
            component.fanzoneModuleData = {
              modules: [{...moduleMock}, {...moduleNotToUpdate}]
            } as any;
            component.onModuleUpdate(moduleMock as any);
    
          });
        it('other modules flow', () => {
            component['addEventListenersWithinModule'] = jasmine.createSpy();
            component['fanzoneOnSocketUpdate'](null as any);

            expect(component['addEventListenersWithinModule']).toHaveBeenCalledWith(fanzoneCleanModuleMock as any);
        });
        describe('#addEventsLiveUpdatesListener', () => {
            it('should add addEventListener to events array', () => {
                component['addEventsLiveUpdatesListener']([footballEventMock, eventMock] as any);
                expect(fanzoneFeaturedService.addEventListener).toHaveBeenCalledTimes(2);
            });

            it('should add addEventListener to events array', () => {
                component['addEventsLiveUpdatesListener']([footballEventMock, eventMock, {}] as any);
                expect(fanzoneFeaturedService.addEventListener).toHaveBeenCalledTimes(2);
            });

            it('should call connect on update', () => {
                fanzoneFeaturedService.addEventListener.and.callFake((string: string, cb: Function) => {
                    cb(string);
                });
                component['addEventsLiveUpdatesListener']([footballEventMock, eventMock] as any);
                expect(pubsub.publish).toHaveBeenCalledTimes(2);
            });
        });

        it('check addClockToEvents function call', () => {
            const featuredModuleMockClone: any = _.clone(featuredModuleMock);
      
            component['addClockToEvents'](<any>{
              modules: [featuredModuleMockClone]
            });
      
            expect(fanzoneFeaturedService.addClock).toHaveBeenCalledWith(featuredModuleMockClone.data);
        });
    });


    describe('ngOnDestroy', () => {
        let initialState;
        beforeEach(() => {
            initialState = {
                directiveName: null,
                modules: [],
                showTabOn: null,
                title: null,
                visible: null
            };
        });

        it('default case', () => {
            component.ngOnDestroy();
            expect(pubsub.unsubscribe).toHaveBeenCalledWith('fanzoneModule');
        });

    });

    it('@reloadComponent should reload component', () => {
        component.reloadComponent();
        expect(fanzoneFeaturedService.reconnect).toHaveBeenCalled();
        expect(component.ssDown).toBe(false);
        expect(component.isConnectSucceed).toBe(true);
        expect(component.showLoader).toBe(true);
        expect(component['changeDetectorRef'].markForCheck).toHaveBeenCalled();
    });

    it('should use OnPush strategy', () => {
        expect(FanzoneAppNowNextComponent['__annotations__'][0].changeDetection).toBe(0);
    });

    describe('handleErrorOnFirstLoad', () => {
        it('Namespace Error', () => {
            component.handleErrorOnFirstLoad();
            expect(component.ssDown).toBeTrue();
            expect(component.showLoader).toBeFalse();
        });

        it('not homepage', () => {

            component.handleErrorOnFirstLoad(false);
            expect(component.ssDown).toBeFalsy();
            expect(component.showLoader).toBeFalsy();
            expect(component['changeDetectorRef'].markForCheck).toHaveBeenCalled();
        });
    });
    it('should not init connection during  initialisation if no fanzone', () => {

    });
});
