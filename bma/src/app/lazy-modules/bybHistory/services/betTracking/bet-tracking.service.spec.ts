import { of, Observable } from 'rxjs';
import { fakeAsync } from '@angular/core/testing';

import { BetTrackingService } from './bet-tracking.service';

describe('BetTrackingService', () => {
  let service: BetTrackingService,
    cmsService,
    configFromCms,
    betTrackingRulesService,
    domSanitizer;

  beforeEach(() => {
    configFromCms = {
      BetTracking: {
        enabled: true
      }
    };
    domSanitizer = {
      sanitize: jasmine.createSpy('sanitize'),
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml')
    };
    cmsService = {
      getStaticBlock: jasmine.createSpy('getStaticBlock').and.returnValue(of({htmlMarkup: 'some string'})),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of(configFromCms))
    };
    betTrackingRulesService = {
      matchBettingStatusHandler: jasmine.createSpy('betTrackingRulesService').and.returnValue(
        {
          status: 'Loosing',
          progress: {
            current: 1,
            target: 3,
            desc: '1 of 3 goals'
          }
        }
      )
    };

    service = new BetTrackingService(domSanitizer, cmsService, betTrackingRulesService);
  });

  describe('isTrackingEnabled', () => {
    it('should return true', () => {
      service.isTrackingEnabled().subscribe(res => {
        expect(cmsService.getSystemConfig).toHaveBeenCalled();
        expect(res).toBeTruthy();
      });
    });

    it('should return false', () => {
      configFromCms.BetTracking = { enabled : false };

      service.isTrackingEnabled().subscribe(res => {
        expect(cmsService.getSystemConfig).toHaveBeenCalled();
        expect(res).toBeFalsy();
      });
    });

    it('should return false', () => {
      configFromCms.BetTracking = { };

      service.isTrackingEnabled().subscribe(res => {
        expect(cmsService.getSystemConfig).toHaveBeenCalled();
        expect(res).toBeFalsy();
      });
    });
  });

  describe('getSelectionStatusAndProgress', () => {
    it('should return null', () => {
      const selection: any = {
        part: {},
        config: {
          name: 'name',
          methodName: 'methodName'
        }
      };
      expect(service['getSelectionStatusAndProgress'](selection, {} as any, {} as any)).toEqual({ status: '' });
    });

    it('should return progress', () => {
      const selection: any = {
        part: {},
        config: {
          name: 'name',
          methodName: 'matchBettingStatusHandler'
        }
      };
      expect(service['getSelectionStatusAndProgress'](selection, {} as any, {} as any)).toEqual({
        status: 'Loosing',
          progress: {
          current: 1,
          target: 3,
          desc: '1 of 3 goals'
          }
      });
    });

    it('should not return progress (no result)', () => {
      betTrackingRulesService.matchBettingStatusHandler = jasmine.createSpy('matchBettingStatusHandler').and.returnValue(null);
      const selection: any = {
        part: {
          outcome: [{
            externalStatsLink: { statValue: '3', statCategory: 'Goals', currentValue: '2' }
          }]
        },
        config: {
          name: 'name',
          methodName: 'matchBettingStatusHandler'
        }
      };
      const bet: any = { settled: 'Y' };

      expect(service['getSelectionStatusAndProgress'](selection, bet, {} as any)).toEqual({ status: '' });
    });
  });

  describe('getStaticContent', () => {
    it('should return static block', fakeAsync(() => {
      service.getStaticContent().subscribe( () => {
        expect(cmsService.getStaticBlock).toHaveBeenCalledWith('opta-disclaimer-short-en-us');
        expect(domSanitizer.bypassSecurityTrustHtml).toHaveBeenCalled();
        expect(domSanitizer.sanitize).toHaveBeenCalled();
      });
    }));

    it('should return static block  as empty', fakeAsync(() => {
      cmsService.getStaticBlock.and.returnValue(of({htmlMarkup: ''}));
      service.getStaticContent().subscribe();
      expect(cmsService.getStaticBlock).toHaveBeenCalledWith('opta-disclaimer-short-en-us');
      expect(domSanitizer.bypassSecurityTrustHtml).not.toHaveBeenCalled();
      expect(domSanitizer.sanitize).not.toHaveBeenCalled();
    }));

    it('should return observable if it already exist', fakeAsync(() => {
      service['staticContentObservable'] = new Observable();
      service.getStaticContent().subscribe( () => {
        expect(cmsService.getStaticBlock).not.toHaveBeenCalledWith('opta-disclaimer-short-en-us');
        expect(domSanitizer.bypassSecurityTrustHtml).not.toHaveBeenCalled();
        expect(domSanitizer.sanitize).not.toHaveBeenCalled();
      });
    }));
  });

  describe('updateProgress', ()=> {
    let selections;
    let updatedSelections;

    beforeEach(() => {
      selections = [
        {
          config: {
            template: 'range'
          },
          progress: 'progress',
          status: 'status',
          showBetStatusIndicator: 'showBetStatusIndicator',
          partSettled: false
        },
        {
          config: {
            template: 'range'
          },
          progress: 'progress',
          status: 'status',
          showBetStatusIndicator: true,
          partSettled: true
        },
        {
          config: {
            template: 'binary'
          },
          status: 'status',
          showBetStatusIndicator: 'showBetStatusIndicator',
          partSettled: false
        },
        {
          config: {
            template: 'binary'
          },
          status: 'status',
          showBetStatusIndicator: true,
          partSettled: true
        },
        {
          config: {
            template: 'template'
          },
          progress: 'progress',
          status: 'status',
          showBetStatusIndicator: 'showBetStatusIndicator',
          partSettled: false
        },
        {
          progress: 'progress',
          status: 'status',
          showBetStatusIndicator: 'showBetStatusIndicator'
        },
        {
          config: {
            template: 'range'
          },
          status: 'prePlay2h',
          showBetStatusIndicator: false,
          partSettled: true
        },
        {
          config: {
            template: 'binary'
          },
          status: 'prePlay2h',
          showBetStatusIndicator: false,
          partSettled: true
        }
      ] as any;
      updatedSelections = [
        {
          config: {
            template: 'range'
          },
          progress: 'updated progress',
          status: 'status',
          showBetStatusIndicator: true,
          partSettled: false
        },
        {
          config: {
            template: 'range'
          },
          progress: 'updated progress',
          status: 'status',
          showBetStatusIndicator: true,
          partSettled: true
        },
        {
          config: {
            template: 'binary'
          },
          status: 'status',
          showBetStatusIndicator: true,
          partSettled: false
        },
        {
          config: {
            template: 'binary'
          },
          status: 'status',
          showBetStatusIndicator: true,
          partSettled: true
        },
        {
          config: {
            template: 'template'
          },
          progress: null,
          status: null,
          showBetStatusIndicator: false,
          partSettled: false
        },
        {
          config: {
            template: 'binary'
          },
          status: 'prePlay2h',
          showBetStatusIndicator: false,
          partSettled: true
        },
        {
          config: {
            template: 'range'
          },
          status: 'prePlay2h',
          showBetStatusIndicator: false,
          partSettled: true
        }
      ] as any;
    });

    it('should update progress if part NOT Settled', () => {
      service['getSelectionStatusAndProgress'] = jasmine.createSpy('getSelectionStatusAndProgress').and.returnValue(
        {
          status: 'status',
          progress: 'updated progress'
        }
      );
      service.updateProgress(selections, {} as any, {} as any);

      expect(selections[0].progress).toEqual(updatedSelections[0].progress);
      expect(selections[0].status).toEqual(updatedSelections[0].status);
      expect(selections[0].showBetStatusIndicator).toEqual(updatedSelections[0].showBetStatusIndicator);

      expect(selections[1].progress).toEqual(updatedSelections[1].progress);
      expect(selections[1].status).toEqual(updatedSelections[1].status);
      expect(selections[1].showBetStatusIndicator).toEqual(updatedSelections[1].showBetStatusIndicator);

      expect(selections[2].status).toEqual(updatedSelections[2].status);
      expect(selections[2].showBetStatusIndicator).toEqual(updatedSelections[2].showBetStatusIndicator);

      expect(selections[3].status).toEqual(updatedSelections[3].status);
      expect(selections[3].showBetStatusIndicator).toEqual(updatedSelections[3].showBetStatusIndicator);
    });

    it('should not update progress', () => {
      service['getSelectionStatusAndProgress'] = jasmine.createSpy('getSelectionStatusAndProgress').and.returnValue(null);
      service.updateProgress(selections, {} as any, {} as any);

      expect(selections[0].progress).toEqual(selections[0].progress);
      expect(selections[0].status).toEqual(selections[0].status);
      expect(selections[0].showBetStatusIndicator).toEqual(selections[0].showBetStatusIndicator);

      expect(selections[1].progress).toEqual(selections[1].progress);
      expect(selections[1].status).toEqual(selections[1].status);
      expect(selections[1].showBetStatusIndicator).toEqual(selections[1].showBetStatusIndicator);

      expect(selections[2].status).toEqual(selections[2].status);
      expect(selections[2].showBetStatusIndicator).toEqual(selections[2].showBetStatusIndicator);

      expect(selections[3].status).toEqual(selections[3].status);
      expect(selections[3].showBetStatusIndicator).toEqual(selections[3].showBetStatusIndicator);
    });

    it('should update progress if its pre-play event', () => {
      service['getSelectionStatusAndProgress'] = jasmine.createSpy('getSelectionStatusAndProgress').and.returnValue(
        {
          status: 'prePlay2h',
          progress: 'updated progress'
        }
      );
      service.updateProgress(selections, {} as any, {} as any);

      expect(selections[6].status).toEqual(updatedSelections[5].status);
      expect(selections[6].showBetStatusIndicator).toEqual(updatedSelections[5].showBetStatusIndicator);

      expect(selections[7].status).toEqual(updatedSelections[6].status);
      expect(selections[7].showBetStatusIndicator).toEqual(updatedSelections[6].showBetStatusIndicator);
    });

    it('should not override selectionStatus when part is settled at OB', () => {
      service['updateSelectionStatus'](selections[1], {status: 'winning'});
      expect(selections[1].status).toEqual('status');
      expect(selections[1].showBetStatusIndicator).toEqual(true);
    });
    it('should override selectionStatus with OPTA status when part is not settled at OB', () => {
      service['updateSelectionStatus'](selections[0], {status: 'winning'});
      expect(selections[0].status).toEqual('winning');
      expect(selections[0].showBetStatusIndicator).toEqual(true);
    });
  });

  it('should check is build your bet', () => {
    const part = [
      {
        eventMarketDesc: 'Build Your Bet'
      }
    ] as any;

    expect(service.checkIsBuildYourBet(part)).toBeTruthy();
  });

  describe('extendSelectionsWithTrackingConfig', () => {
    it('should extend selections if eventMarketDesc is present in config', () => {
      const selections = [
        {
          part: {
            eventMarketDesc: 'Build Your Bet MATCH BETTING'
          }
        },
        {
          part: {
            eventMarketDesc: 'eventMarketDesc'
          }
        }
      ] as any;
      service.extendSelectionsWithTrackingConfig(selections);

      expect(selections[0].config).toBeTruthy();
    });
  });
});
