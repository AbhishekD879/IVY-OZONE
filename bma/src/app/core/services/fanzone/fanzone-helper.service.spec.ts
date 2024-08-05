import { FanzoneHelperService } from './fanzone-helper.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import {  of as observableOf, of, throwError } from 'rxjs';
import { FANZONEDETAILS, FANZONE_POS_GET } from '@core/services/fanzone/constant/fanzone.constant';
import { PreferenceCentre } from '@app/fanzone/components/fanzonePreferenceCentre/mockData/fanzone-preference-centre.component.mock';
import { fakeAsync, tick } from '@angular/core/testing';
import environment from '@environment/oxygenEnvConfig';
import { FZ_GET_MAPPER } from '@app/lazy-modules/fanzone/fanzone.constant';
import { fanzoneEmailKey } from '@app/fanzone/constants/fanzoneconstants';

describe('FanzoneHelperService', () => {
    describe('FanzoneHelperService with user login/notlogin for fanzone disabled', () => {
        let service: FanzoneHelperService;
        let user;
        let vanillaApiService;
        let timeService;
        let pubsub;
        let cmsService;
        let storageService;
        let fanzoneStorageService;
        const menuItemMock = {
            categoryId: 160
        };
        const menuItemMock2 = {
            categoryId: 16,
            disabled: true
        };
        
        beforeEach(() => {
            user = {
                username: 'abc',
                status: false
            };
            vanillaApiService = {
                get: jasmine.createSpy('vanillaApiService.get').and.returnValue(observableOf(FANZONE_POS_GET)),
                post: jasmine.createSpy('vanillaApiService.post').and.returnValue(observableOf([]))
            };
            pubsub = {
                publish: jasmine.createSpy('publish'),
                publishSync: jasmine.createSpy('publishSync'),
                subscribe: jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn()),
                API: pubSubApi
            };
            storageService = {
                set: jasmine.createSpy('storageService.set'),
                get: jasmine.createSpy('storageService.get').and.returnValue({ teamName: 'Everton', teamId: '123' }),
                remove: jasmine.createSpy('storageService.remove')
            };
            cmsService = {
                isFanzoneConfigDisabled: jasmine.createSpy('isFanzoneConfigDisabled').and.returnValue(of(false)),
                getMenuItems: jasmine.createSpy('cmsService.getMenuItems').and.returnValue(observableOf([menuItemMock])),
                getSystemConfig: jasmine.createSpy('cmsService.getSystemConfig').and.returnValue(observableOf({
                    Fanzone: {
                        enabled: false 
                    }
                })),
                getFanzone: jasmine.createSpy('cmsService.getFanzone').and.returnValue(observableOf([])),
            };
            timeService = {
                getSuspendAtTime: jasmine.createSpy().and.returnValue(new Date())
            };
            fanzoneStorageService = {
                set: jasmine.createSpy('fanzoneStorageService.set'),
                get: jasmine.createSpy('fanzoneStorageService.get')
              };
            service = new FanzoneHelperService(user, vanillaApiService, pubsub, cmsService, storageService, fanzoneStorageService);
        });
        it('should not publish fanzone data if user logged in and fanzone not enabled', () => {
            service.PublishFanzoneData();
            expect(pubsub.publish).not.toHaveBeenCalled();
        });
        it('should not publish fanzone data if user not logged in and fanzone not enabled', () => {
            user.username = null;
            service.PublishFanzoneData();
            expect(pubsub.publish).not.toHaveBeenCalled();
        });
    });
    describe('FanzoneHelperService with user not logged in and fanzone enabled', () => {
        let service: FanzoneHelperService;
        let storageService;
        let user;
        let vanillaApiService;
        let timeService;
        let pubsub;
        let cmsService;
        let fanzoneStorageService;
        const menuItemMock = {
            categoryId: 16
        };
        beforeEach(() => {
            user = {
                username: 'abc',
                status: false
            };
            vanillaApiService = {
                get: jasmine.createSpy('vanillaApiService.get').and.returnValue(observableOf(FANZONE_POS_GET)),
                post: jasmine.createSpy('vanillaApiService.post').and.returnValue(observableOf(FANZONE_POS_GET))
            };
            pubsub = {
                publish: jasmine.createSpy('publish'),
                publishSync: jasmine.createSpy('publishSync'),
                subscribe: jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn()),
                API: pubSubApi
            };
            storageService = {
                set: jasmine.createSpy('storageService.set'),
                get: jasmine.createSpy('storageService.get').and.returnValue({ teamName: 'Everton', teamId: '123' }),
                remove: jasmine.createSpy('storageService.remove')
            };
            cmsService = {
                isFanzoneConfigDisabled: jasmine.createSpy('isFanzoneConfigDisabled').and.returnValue(of(true)),
                getMenuItems: jasmine.createSpy('cmsService.getMenuItems').and.returnValue(observableOf([menuItemMock])),
                getSystemConfig: jasmine.createSpy('cmsService.getSystemConfig').and.returnValue(observableOf({
                    Fanzone: {
                        enabled: true
                    }
                })),
                getFanzone: jasmine.createSpy('cmsService.getFanzone').and.returnValue(observableOf([]))
            };
            timeService = {
                getSuspendAtTime: jasmine.createSpy().and.returnValue(new Date())
            };
            fanzoneStorageService = {
                set: jasmine.createSpy('fanzoneStorageService.set'),
                get: jasmine.createSpy('fanzoneStorageService.get')
              };
            service = new FanzoneHelperService(user, vanillaApiService, pubsub, cmsService, storageService, fanzoneStorageService);
        });
        it('should not publish fanzone data if user not logged in and fanzone enabled', () => {
            user.username = null;
            service.PublishFanzoneData();
            expect(pubsub.publish).not.toHaveBeenCalled();
        });
        it('should not publish fanzone data if user not logged in and fanzone enabled', () => {
            user.username = null;
            service.PublishFanzoneData();
            expect(pubsub.publish).not.toHaveBeenCalled();
        });

        it('getInitFanzoneData for first time login', () => {
            service.isEnableFanzone = true;
            service.getInitFanzoneData = jasmine.createSpy('');
            storageService.get = jasmine.createSpy('USER').and.returnValue(JSON.parse(JSON.stringify({firstLogin:true})));
            service.getFzInitialDataFirstTimeUser();
            expect(service.getInitFanzoneData).toHaveBeenCalled();
        });
        

        it('getInitFanzoneData not called when not logged-in', () => {
            service.isEnableFanzone = true;
            service.getInitFanzoneData = jasmine.createSpy('');
            expect(service.getInitFanzoneData).not.toHaveBeenCalled();
        });

        it('getInitFanzoneData not called when isEnableFanzone not enabled', () => {
            service.isEnableFanzone = false;
            service.getInitFanzoneData = jasmine.createSpy('');
            expect(service.getInitFanzoneData).not.toHaveBeenCalled();
        });

        it('getEmailOptin', () => {
            service.getEmailOptin();
            expect(vanillaApiService.get).toHaveBeenCalled();
        })

        it('getEmailOptin', () => {
            service.getEmailOptin = jasmine.createSpy('getEmailOptin').and.returnValue(of({}));
            service.getEmailOptinData();
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        })

        it('getEmailOptin on error', () => {
            service.getEmailOptin = jasmine.createSpy('getEmailOptin').and.returnValue(throwError({errorCode: "1"}));
            service.getEmailOptinData();
            expect(fanzoneStorageService.set).toHaveBeenCalledWith(fanzoneEmailKey, {...FZ_GET_MAPPER, ...{}});
        })

        it('should not publish fanzone data if no fanzone menu', () => fakeAsync(()=>{
            const menuItemMockData = {
                categoryId: 16
            };
            cmsService.getMenuItems = jasmine.createSpy('cmsService.getMenuItems').and.returnValue(observableOf([menuItemMockData]));
            service.PublishFanzoneData();
            tick();

            expect(service.isEnableFanzone).toBeFalse();
            expect(pubsub.publish).not.toHaveBeenCalled();
        }));
        it('should not publish fanzone data if  fanzone menu disabled', () => {
            const menuItemMockDisabled = {
                categoryId: 160,
                disabled : true,
                fzDisabled: false
            };
            cmsService.getMenuItems = jasmine.createSpy('cmsService.getMenuItems').and.returnValue(observableOf([menuItemMockDisabled]));
            service.PublishFanzoneData();

            expect(service.isEnableFanzone).toBeFalse();
            expect(pubsub.publish).not.toHaveBeenCalled();
        });
    });
    describe('FanzoneHelperService with user logged in and fanzone enabled', () => {
        let service: FanzoneHelperService;
        let storageService;
        let user;
        let vanillaApiService;
        let timeService;
        let pubsub;
        let cmsService;
        let fanzoneStorageService;
        const menuItemMock = {
            categoryId: 160
        };
        const menuItemMock2 = {
            categoryId: 16,
            disabled: true
        };
        beforeEach(() => {
            user = {
                username: 'abc',
                status: true
            };
            vanillaApiService = {
                get: jasmine.createSpy('vanillaApiService.get').and.returnValue(observableOf(FANZONE_POS_GET)),
                post: jasmine.createSpy('vanillaApiService.post').and.returnValue(observableOf([]))
            };
            pubsub = {
                publish: jasmine.createSpy('publish'),
                publishSync: jasmine.createSpy('publishSync'),
                subscribe: jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn()),
                API: pubSubApi
            };
            storageService = {
                set: jasmine.createSpy('storageService.set'),
                get: jasmine.createSpy('storageService.get').and.returnValue({ teamName: 'Everton', teamId: '123' }),
                remove: jasmine.createSpy('storageService.remove')
            };
            fanzoneStorageService = {
                set: jasmine.createSpy('fanzoneStorageService.set'),
                get: jasmine.createSpy('fanzoneStorageService.get')
              };
            cmsService = {
                isFanzoneConfigDisabled: jasmine.createSpy('isFanzoneConfigDisabled').and.returnValue(of(false)),
                getMenuItems: jasmine.createSpy('cmsService.getMenuItems').and.returnValue(observableOf([menuItemMock])),
                getSystemConfig: jasmine.createSpy('cmsService.getSystemConfig').and.returnValue(observableOf({
                    Fanzone: {
                        enabled: true
                    }
                })),
                getFanzone: jasmine.createSpy('cmsService.getFanzone').and.returnValue(observableOf(FANZONEDETAILS)),
                getFanzonePreferences: jasmine.createSpy('fanzonePreferences').and.returnValue(observableOf(PreferenceCentre))
            };
            timeService = {
                getSuspendAtTime: jasmine.createSpy().and.returnValue(new Date())
            };
            environment.brand = 'ladbrokes';
            service = new FanzoneHelperService(user, vanillaApiService, pubsub, cmsService, storageService, fanzoneStorageService);
        });

        it('constructor', () => {
            expect(service).toBeDefined();
        });

        it('publish fanzone data will publish empty array if user logged in and fanzone not enabled', () => {
            pubsub.subscribe.and.callFake((namespace, message: string[], callback) => {
                if (message.includes('RELOAD_COMPONENTS') || message.includes('SESSION_LOGIN')) {
                    callback();
                    expect(service.selectedFanzone).toEqual(FANZONEDETAILS[0])
                    expect(pubsub.publish).toHaveBeenCalledWith('FANZONE_DATA', FANZONEDETAILS);
                    expect(service.getEmailOptinData).toHaveBeenCalled();
                }
            });
        });
        
        it('publish fanzone data will publish empty array if user logged out', () => {
            pubsub.subscribe.and.callFake((namespace, message: string[], callback) => {
                if (message.includes('SESSION_LOGOUT')) {
                    callback();
                    expect(storageService.remove).toHaveBeenCalledWith(fanzoneEmailKey);
                }
            });
        });
        
        it('should call when no error on get fanzone', () => {
            service.getUserFanzoneTeam = jasmine.createSpy('').and.returnValue(of({}));
            fanzoneStorageService.get.and.returnValue({teamName: 'FZ001'});
            service.appendToStorage = jasmine.createSpy();
            service.getInitFanzoneData();
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        })

        it('should call when no error on get fanzone', () => {
            service.getUserFanzoneTeam = jasmine.createSpy('').and.returnValue(of({errorCode: 'NO_RECORD_FOUND'}));
            fanzoneStorageService.get.and.returnValue({teamName: 'FZ001'});
            service.appendToStorage = jasmine.createSpy();
            service.getInitFanzoneData();
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        })

        it('should call when no error on get fanzone', () => {
            service.getUserFanzoneTeam = jasmine.createSpy('').and.returnValue(of({}));
            fanzoneStorageService.get.and.returnValue({teamName: 'FZ001', showSYCPopupOn: '2022-05-07T13:20:00.834Z'});
            service.getInitFanzoneData();
            expect(fanzoneStorageService.set).toHaveBeenCalledWith('fanzone', { isFanzoneExists: false, isResignedUser: false, showSYCPopupOn: '2022-05-07T13:20:00.834Z'});
        })

        it('publish fanzone data will publish empty array if user logged in and fanzone not enabled', () => {
            fanzoneStorageService.get.and.returnValue(FANZONEDETAILS[0]);
            service.PublishFanzoneData();

            expect(service.selectedFanzone).toEqual(FANZONEDETAILS[0]);
            expect(pubsub.publish).toHaveBeenCalledWith('FANZONE_DATA', FANZONEDETAILS[0]);
        });

        it('should not publish when vanilla service when user is not subscribed before', () => {
            const response = { "preferences": [{ "category": "football", "commLastUpdatedAt": "2022-04-28T10:36:57Z", "subscriptionDate": "2022-04-28T10:36:57Z", "preferenceMap": [{"key": "TEAM_ID", "value": "e5p0ehyguld7egzhiedpdnc3w"}, {"key": "TEAM_NAME", "value": "Brighton and Hove Albion"}, {"key": "COMM_PREFERENCES", "value": "[\"\"]"}]}]};
            service.getUserFanzoneTeam = jasmine.createSpy('getUserFanzoneTeam').and.returnValue(of(response));
            service.appendToStorage = jasmine.createSpy('appendToStorage');
            service.checkIfTeamIsRelegated = jasmine.createSpy('').and.returnValue(of(false));
            service.relegatedTeamRemindMeLater = jasmine.createSpy('').and.returnValue(false);
            service.PublishFanzoneData = jasmine.createSpy('publish');
            service.getInitFanzoneData();
            expect(fanzoneStorageService.set).toHaveBeenCalled();
            expect(service.PublishFanzoneData).toHaveBeenCalled();
        })

        it('should not publish when vanilla service when user is not subscribed before', () => {
            const response = { "preferences": [{ "category": "football", "commLastUpdatedAt": "2022-04-28T10:36:57Z", "subscriptionDate": "2022-04-28T10:36:57Z", "preferenceMap": [{"key": "TEAM_ID", "value": "FZ001_UNSUBSCRIBE"}]}]};
            service.getUserFanzoneTeam = jasmine.createSpy('getUserFanzoneTeam').and.returnValue(of(response));
            service['emitTeamUpdate'] = jasmine.createSpy('emitTeamUpdate');
            service.isRemindLaterStorageExists = jasmine.createSpy('isRemindLaterStorageExists');
            service.checkIfTeamIsRelegated = jasmine.createSpy('').and.returnValue(of(false));
            service.PublishFanzoneData = jasmine.createSpy('publish');
            service.getInitFanzoneData();
            expect(service['emitTeamUpdate']).toHaveBeenCalled();
            expect(service.isRemindLaterStorageExists).toHaveBeenCalled();
        })


        it('should publish when when user subscribed before and his team is not relegated', () => {
            const response = { "preferences": [{ "category": "football", "commLastUpdatedAt": "2022-04-28T10:36:57Z", "subscriptionDate": "2022-04-28T10:36:57Z", "preferenceMap": [{"key": "TEAM_ID", "value": "e5p0ehyguld7egzhiedpdnc3w"}, {"key": "TEAM_NAME", "value": "Brighton and Hove Albion"}, {"key": "COMM_PREFERENCES", "value": "[\"\"]"}]}]};
            service.getUserFanzoneTeam = jasmine.createSpy('getUserFanzoneTeam').and.returnValue(of(response));
            service.appendToStorage = jasmine.createSpy('appendToStorage');
            service.checkIfTeamIsRelegated = jasmine.createSpy('').and.returnValue(of(false));
            service.relegatedTeamRemindMeLater = jasmine.createSpy('').and.returnValue(true);
            service.PublishFanzoneData = jasmine.createSpy('publish');
            service.getInitFanzoneData();
            expect(fanzoneStorageService.set).toHaveBeenCalled();
            expect(service.PublishFanzoneData).toHaveBeenCalled();
        })

        
        it('should not publish when when user subscribed before and his team is relegated', () => {
            const response = { "preferences": [{ "category": "football", "commLastUpdatedAt": "2022-04-28T10:36:57Z", "subscriptionDate": "2022-04-28T10:36:57Z", "preferenceMap": [{"key": "TEAM_ID", "value": "e5p0ehyguld7egzhiedpdnc3w"}, {"key": "TEAM_NAME", "value": "Brighton and Hove Albion"}, {"key": "COMM_PREFERENCES", "value": "[\"\"]"}]}]};
            service.getUserFanzoneTeam = jasmine.createSpy('getUserFanzoneTeam').and.returnValue(of(response));
            service.appendToStorage = jasmine.createSpy('appendToStorage');
            service.checkIfTeamIsRelegated = jasmine.createSpy('').and.returnValue(of(true));
            service.relegatedTeamRemindMeLater = jasmine.createSpy('').and.returnValue(true);
            service.PublishFanzoneData = jasmine.createSpy('publish');
            service.getInitFanzoneData();
        })

        it('relegatedTeamRemindMeLater storage exists', () => {
            const isRelegatedTeamRemindMeLater = service.relegatedTeamRemindMeLater({isFanzoneTeamRelegated: true, showRelegatedPopupOn: ''});
            expect(isRelegatedTeamRemindMeLater).toBe(true);
        })

        it('relegatedTeamRemindMeLater storage doesnt exist', () => {
            const isRelegatedTeamRemindMeLater = service.relegatedTeamRemindMeLater({});
            expect(isRelegatedTeamRemindMeLater).toBe(false);
        })

        it('checkIfTeamIsRelegated', () => {
            service.checkIfTeamIsRelegated().subscribe(response => {
                expect(cmsService.getFanzone).toHaveBeenCalled();
            })
        })

        it('should not publish when vanilla service when user is resigned', () => {
            const response = {"preferences": [{"category": "football", "commLastUpdatedAt": "2022-04-28T10:44:02Z", "subscriptionDate": "2022-04-28T10:44:02Z", "preferenceMap": []}]};
            service.getUserFanzoneTeam = jasmine.createSpy('getUserFanzoneTeam').and.returnValue(of(response));
            service.getInitFanzoneData();
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        })

        it('should not publish when vanilla service when user is resigned', () => {
            const response =  {"preferences": [{"category": "football", "commLastUpdatedAt": "2022-04-28T10:44:02Z", "subscriptionDate": "2022-04-28T10:44:02Z", "preferenceMap": [{"key": "COMM_PREFERENCES", "value": "[\"\"]"}]}]};
            service.getUserFanzoneTeam = jasmine.createSpy('getUserFanzoneTeam').and.returnValue(of(response));
            service.getInitFanzoneData();
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        })
       
        it('should call when error on get fanzone', () => {
            service.getUserFanzoneTeam = jasmine.createSpy('').and.returnValue(throwError('error'));
            spyOn(console, 'error');
            service.getInitFanzoneData();
            expect(console.error).toHaveBeenCalledWith('error');
        })

        it('should call when error on checking if team is relegated', () => {
            const response =  {"preferences": [{"category": "football", "commLastUpdatedAt": "2022-04-28T10:44:02Z", "subscriptionDate": "2022-04-28T10:44:02Z", "preferenceMap": [{"key": "COMM_PREFERENCES", "value": "[\"\"]"}]}]};
            service.getUserFanzoneTeam = jasmine.createSpy('getUserFanzoneTeam').and.returnValue(of(response));
            service.checkIfTeamIsRelegated = jasmine.createSpy('checkIfTeamIsRelegated').and.returnValue(throwError('error'));
            spyOn(console, 'error');
            service.getInitFanzoneData();
            expect(console.error).toHaveBeenCalledWith('error');
        })

        it('should emit fanzoneTeamUpdate subject', () => {
            service['fanzoneTeamUpdate'] = {observers: [1],next: jasmine.createSpy()} as any;

            service.appendToStorage({key:'test'});

            expect(service['fanzoneTeamUpdate'].next).toHaveBeenCalled();
        })

        it('should emit getSelectedFzUpdate subject', () => {
            service['selectedFanzoneUpdate'] = {observers: [1],next: jasmine.createSpy()} as any;
            service.checkIfTeamIsRelegated = jasmine.createSpy('').and.returnValue(of(false));
            service.getFanzoneTeam({key:'test', teamId:'diejryrhien12ddi'});

            expect(service['selectedFanzoneUpdate'].next).toHaveBeenCalled();
        })

        describe('Fanzone team relegation', () => {
            beforeEach(() => {
                cmsService = {
                    getFanzone: jasmine.createSpy('').and.returnValue(observableOf([{teamId:'12345', teamName:'Arsenal'}]))
                };
            });
            it('checkIfTeamIsRelegated when team is relegated', () => {
                service['selectedFanzoneUpdate'] = {observers: [1],next: jasmine.createSpy()} as any;
                fanzoneStorageService.get.and.returnValue({teamId: '12345', showSYCPopupOn: '2022-05-07T13:20:00.834Z'});
                service.checkIfTeamIsRelegated().subscribe((res) => {
                    expect(res).toBe(true);
                });
            });
            it('checkIfTeamIsRelegated when team is not relegated', () => {
                service['selectedFanzoneUpdate'] = {observers: [1],next: jasmine.createSpy()} as any;
                fanzoneStorageService.get.and.returnValue({TEAM_ID: '12345', showSYCPopupOn: '2022-05-07T13:20:00.834Z'});
                service.checkIfTeamIsRelegated().subscribe((res) => {
                    expect(res).toBe(false);
                });
            });
            it('checkIfTeamIsRelegated when team id is passed', () => {
                service['selectedFanzoneUpdate'] = {observers: [1],next: jasmine.createSpy()} as any;
                const teamData = {teamId:'12345', teamName:'Arsenal', isFanzoneExists: true};
                service.checkIfTeamIsRelegated(teamData).subscribe((res) => {
                    expect(res).toBe(true);
                });
            })
            it('checkIfTeamIsRelegated when team id is custom team', () => {
                service['selectedFanzoneUpdate'] = {observers: [1],next: jasmine.createSpy()} as any;
                const teamData = {TEAMID:'fz001', teamName:'Arsenal', isFanzoneExists: false};
                service.checkIfTeamIsRelegated(teamData).subscribe((res) => {
                    expect(res).toBe(false);
                });
            })
            it('checkIfTeamIsRelegated when team id is not present', () => {
                service['selectedFanzoneUpdate'] = {observers: [1],next: jasmine.createSpy()} as any;
                fanzoneStorageService.get.and.returnValue({});
                const teamData = {};
                service.checkIfTeamIsRelegated(teamData).subscribe((res) => {
                    expect(res).toBe(false);
                });
            })
            it('checkIfTeamIsRelegated when team id is null', () => {
                service['selectedFanzoneUpdate'] = {observers: [1],next: jasmine.createSpy()} as any;
                fanzoneStorageService.get.and.returnValue(null);
                const teamData = null;
                service.checkIfTeamIsRelegated(teamData).subscribe((res) => {
                    expect(res).toBe(false);
                });
            })
        });
        
        describe('Fanzone team relegation', () => {
            beforeEach(() => {
                cmsService = {
                    getFanzone: jasmine.createSpy('').and.returnValue(observableOf([{teamId:'1234', teamName:'Arsenal'}]))
                };
            });
            it('checkIfTeamIsRelegated when team is relegated', () => {
                service['selectedFanzoneUpdate'] = {observers: [1],next: jasmine.createSpy()} as any;
                fanzoneStorageService.get.and.returnValue({TEAMID: '12345', showSYCPopupOn: '2022-05-07T13:20:00.834Z'});
                service.checkIfTeamIsRelegated().subscribe((res) => {
                    expect(res).toBe(false);
                });
            });
        });

        it('should return fanzoneTeamUpdate', () => {
            service['fanzoneTeamUpdate'] = {observers: [1],next: jasmine.createSpy()} as any;

           const emittedData =  service.getFanzoneTeamUpdate();

            expect(emittedData).not.toEqual(null); 
        })

        it('getInitFanzoneData', () => {
            const response = {"preferences": [{"category": "football", "commLastUpdatedAt": "2022-04-28T10:44:02Z", "subscriptionDate": "2022-04-28T10:44:02Z", "preferenceMap": []}]};
            fanzoneStorageService.get.and.returnValue({showSYCPopupOn: '2022-05-07T13:20:00.834Z'});
            service.getUserFanzoneTeam = jasmine.createSpy('getUserFanzoneTeam').and.returnValue(of(response));
            service.getInitFanzoneData();
        })

        it('getInitFanzoneData when showSYCPopupOn is empty', () => {
            const response = {"preferences": [{"category": "football", "commLastUpdatedAt": "2022-04-28T10:44:02Z", "subscriptionDate": "2022-04-28T10:44:02Z", "preferenceMap": []}]};
            fanzoneStorageService.get.and.returnValue({showSYCPopupOn: ''});
            service.getUserFanzoneTeam = jasmine.createSpy('getUserFanzoneTeam').and.returnValue(of(response));
            service.getInitFanzoneData();
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        })

        it('should return selectedFanzoneUpdate', () => {
            service['selectedFanzoneUpdate'] = {observers: [1],next: jasmine.createSpy()} as any;

           const emittedData =  service.getSelectedFzUpdate();

            expect(emittedData).not.toEqual(null); 
        })

        it('isCustomTeam true', () => {
            const res = service.isCustomTeam('FZ001');
            expect(res).toBe(true);
        })

        it('isCustomTeam false', () => {
            const res = service.isCustomTeam('svbdifohfj');
            expect(res).toBe(false);
        })

        it('#isRemindLaterStorageExists', () => {
            fanzoneStorageService.get.and.returnValue({showSYCPopupOn: '022-04-28T10:44:02Z'});
            service.isRemindLaterStorageExists({ isFanzoneExists: false, isResignedUser: false });
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        })

        it('#isRemindLaterStorageExists for new user', () => {
            fanzoneStorageService.get.and.returnValue({showSYCPopupOn: '022-04-28T10:44:02Z', tempTeam: {teamname:'Everton'}});
            service.isRemindLaterStorageExists({ isFanzoneExists: false, isResignedUser: false }, true);
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        })

        it('#isRemindLaterStorageExists for resigned user', () => {
            fanzoneStorageService.get.and.returnValue({isResignedUser:true, subscriptionDate:'2023-07-26T10:26:54Z', isFanzoneExists:false, isCustomResignedUser: true});
            service.isRemindLaterStorageExists({ isFanzoneExists: false, isResignedUser: true });
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        })
    });
});
