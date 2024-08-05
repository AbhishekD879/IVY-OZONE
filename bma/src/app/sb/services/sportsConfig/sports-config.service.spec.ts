import { of, ReplaySubject, throwError } from 'rxjs';

import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { ISportInstance } from '@app/core/services/cms/models/sport-instance.model';
import { TEAMSPORTSDATA } from '@app/shared/mocks/odds-card-highlight-carousel.mock';

describe('SportsConfigService', () => {
  let service: SportsConfigService;

  let
    olympicsService,
    gamingService,
    cmsService,
    sportsConfigStorageService,
    sportsConfigHelperService

  const eventMethods = {
    today: 'todayEventsByClasses',
    tomorrow: 'todayEventsByClasses',
    future: 'todayEventsByClasses',
    upcoming: 'todayEventsByClasses',
    specials: 'specials',
    antepost: 'todayEventsByClasses',
    coupons: 'coupons',
    outrights: 'outrights',
    live: 'blocker',
    results: 'results',
    allEvents: 'todayEventsByClasses',
    matchesTab: 'todayEventsByClasses'
  };

  function storeInstances(observable = 'observable') {
    let sportInstane;
    if (observable === 'observable') {
      sportInstane = of({
        sportConfig: {
          config: {
            name: 'football',
            title: 'FOOTBALL',
            request: {
              categoryId: '16'
            }
          }
        }
      });
    } else {
      sportInstane = new ReplaySubject<ISportInstance>(1);
    }

    return {
      'football': sportInstane,
      'basketball': sportInstane,
      'tennis': sportInstane,
      'golf': sportInstane,
    };
  }

  beforeEach(() => {
    olympicsService = {
      getCMSConfig: jasmine.createSpy('getCMSConfig').and.returnValue(of([{
        categoryId: '16',
        sportName: 'football'
      }])),
      generateSportConfig: jasmine.createSpy('generateSportConfig').and.returnValue({
        config: {
          name: 'football',
          title: 'FOOTBALL'
        }
      }),
      olympicsService: jasmine.createSpy('olympicsService').and.returnValue({
        sportConfig: {
          config: {
            name: 'football',
            title: 'FOOTBALL'
          }
        }
      })
    };

    gamingService = {
      createNewInstance: jasmine.createSpy('createNewInstance').and.returnValue({
        setConfig: () => {},
        sportConfig: {
          config: {
            name: 'football',
            title: 'FOOTBALL',
            request: {
              categoryId: '16'
            }
          }
        }
      })
    };

    cmsService = {
      getSportCategoriesByName: jasmine.createSpy('getSportCategoriesByName').and.returnValue(of([{
        categoryId: '16',
        sportName: 'football'
      }])),
      getSportCategoryById: jasmine.createSpy('getSportCategoryById').and.returnValue(of({
        categoryId: '16',
        sportName: 'football'
      })),
      getTeamsColors: jasmine.createSpy('getTeamsColors').and.returnValue(of(TEAMSPORTSDATA)),
      getSportConfig: jasmine.createSpy('getSportConfig').and.returnValue(of([{
        config: {
          name: 'football',
          tabs: {
              specials: undefined
            },
          request: {
            categoryId: '16'
          }
        }
      }])),
      getSportConfigs: jasmine.createSpy('getSportConfigs').and.returnValue(of([{
        config: {
          name: 'football',
          tabs: {
              specials: undefined
            },
          request: {
            categoryId: '16'
          }
        }
      }]))
    };

    sportsConfigStorageService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of({
        sportConfig: {
          config: {
            tabs: {
              specials: undefined
            },
            name: 'football',
            title: 'FOOTBALL',
            request: {
              categoryId: '16'
            }
          }
        }
      })),
      storeSport: jasmine.createSpy('storeSport').and.returnValue(new ReplaySubject<ISportInstance>(1)),
      getSports: jasmine.createSpy('getSports').and.callFake((sportName => {
        return { 'football': storeInstances()[sportName]};
      }))
    };

    sportsConfigHelperService = {
      getSportConfigName: jasmine.createSpy('getSportConfigName').and.returnValue('football')
    };


    service = new SportsConfigService(
      olympicsService,
      gamingService,
      cmsService,
      sportsConfigStorageService,
      sportsConfigHelperService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });


  describe('#getSport', () => {
    it('should call getSports', () => {
      service.getSport('football', true).subscribe(data => {
        expect(data).toEqual({
          sportConfig: {
            config: {
              name: 'football',
              title: 'FOOTBALL',
              request: {
                categoryId: '16'
              }
            }
          }
        } as any);
      });
    });

    it('should return null', () => {
      sportsConfigStorageService.getSport.and.returnValue(of(null));
      sportsConfigStorageService.getSports.and.returnValue(of(null));
      service.getSport('horseracing', true).subscribe(data => {
        expect(data).toEqual(null);
      });
    });
  });

  describe('#getSports', () => {
    it('should return null', () => {
      service.getSports([]).subscribe(
        data => {
          expect(data).toEqual(null);
        },
      );
    });

    it('should call storeSport', () => {
      const sportConfigLoader = storeInstances('replaySubject')['football'];
      sportsConfigStorageService.getSport.and.returnValue(null);

      service.getSports(['football'], false);

      expect(sportsConfigStorageService.storeSport).toHaveBeenCalledWith('football', sportConfigLoader);
    });

    it('should catch error and return throwError', () => {
      service['getSportsByCache'] = jasmine.createSpy('getSportsByCache').and.returnValue(of({}));

      service.getSports(['cars']).subscribe(data => {
        expect(data).toEqual({});
      });
    });

    it('should check isSportToRequest = false and !this.cachedSportNamesBuffer.includes(sportConfigName) = false', () => {
      service['cachedSportNamesBuffer'] = ['football'];

      service.getSports(['football']).subscribe();
      expect(service['cachedSportNamesBuffer']).toEqual([]);
    });
  });


  describe('#getSportByCategoryId', () => {
    it('should call getSport method', () => {
      service.getSportByCategoryId(16).subscribe(data => {
        expect(data).toEqual({
          sportConfig: {
            config: {
              name: 'football',
              title: 'FOOTBALL',
              request: {
                categoryId: '16'
              }
            }
          }
        } as any);
      });
    });
  });

  describe('#getSportsByRequest', () => {
    it('should catch error', () => {
      cmsService.getSportCategoriesByName.and.returnValue(throwError('Error'));

      service['getSportsByRequest']([]).subscribe(data => {
        expect(data).toEqual({});
      });
    });

    it('should get sports with storeSport', () => {
      sportsConfigStorageService.getSport.and.returnValue(new ReplaySubject<ISportInstance>(1));

      service['getSportsByRequest'](['football']).subscribe(data => {
        expect(cmsService.getSportConfig).toHaveBeenCalledWith('16');
        expect(sportsConfigStorageService.getSport).toHaveBeenCalledWith('football');
        expect(sportsConfigStorageService.storeSport).toHaveBeenCalled();
      });
    });

    it('should get sports', () => {
      sportsConfigStorageService.getSport.and.returnValue(new ReplaySubject<ISportInstance>(1));
      service['getSportsByRequest'](['football', 'basketball']).subscribe(() => {
        expect(cmsService.getSportConfig).toHaveBeenCalledWith('16');
        expect(sportsConfigStorageService.getSport).toHaveBeenCalledWith('football');
      });
    });

    it('should get sports with sportCategories', () => {
      cmsService.getSportCategoriesByName.and.returnValue(of([{
        categoryId: '16',
        sportName: 'football'
      }, {
        categoryId: '10',
        sportName: 'tennis'
      }]));
      service['getSportsByRequest'](['football']).subscribe(() => {
        expect(cmsService.getSportConfigs).toHaveBeenCalledWith(['16', '10']);
        expect(sportsConfigStorageService.getSport).toHaveBeenCalledWith('football');
      });
    });
    it('should get sports with sportCategories and assign name', () => {
      cmsService.getSportConfig.and.returnValue(of([{
        config: {}
      }]));

      service['getSportsByRequest'](['horseracing'], true).subscribe(() => {
        expect(sportsConfigStorageService.getSport).toHaveBeenCalledWith('horseracing');
      });
    });
  });

  describe('#getTeamColorsForSports', () => {
    it('should get sports data for teams ', () => {
      service['getTeamColorsForSports'](['arsenal','madrid'],'16').subscribe(() => {
        expect(cmsService.getTeamsColors).toHaveBeenCalledWith(['arsenal','madrid'],'16');
      });
    });
  });

  describe('#getSportsByCache', () => {
    it('should return football object', () => {
      const cachedSports = [storeInstances()['football']];
      const result = {
        football: {
          sportConfig: {
            config: {
              name: 'football',
              title: 'FOOTBALL',
              request: {
                categoryId: '16'
              }
            }
          }
        }
      };

      service['getSportsByCache'](cachedSports as any).subscribe(data => {
        expect(data).toEqual(result as any);
      });
    });

    it('should catch error', () => {
      service['getSportsByCache']([null]).subscribe(data => {
        expect(data).toEqual({});
      });
    });
  });

  describe('#getOlympicSports', () => {
    it('should return array of ISportConfig', () => {
      const sportNamesBuffer = ['football'];
      const res = [{
        config: {
          name: 'football',
          title: 'FOOTBALL'
        }
      }];
      service['getOlympicSports'](sportNamesBuffer).subscribe(data => {
        expect(data).toEqual(res as any);
      });
    });

    it('should catch error and return empty array', () => {
      olympicsService.getCMSConfig.and.returnValue(throwError('Error'));
      const sportNamesBuffer = ['football'];

      service['getOlympicSports'](sportNamesBuffer).subscribe(data => {
        expect(data).toEqual([]);
      });
    });

    it('should return empty array', () => {
      const sportNamesBuffer = ['football'];
      olympicsService.olympicsService.and.returnValue(null);

      service['getOlympicSports'](sportNamesBuffer).subscribe(data => {
        expect(data).toEqual([]);
      });
    });
  });

  describe('#getMissingSportNames', () => {
    it('should call getMissingSportNames', () => {
      const configs = [{
        config: {
          name: 'football'
        }
      }, {
        config: {
          name: 'basketball'
        }
      }, {
        config: {
          name: 'handball'
        }
      }];
      const result = service['getMissingSportNames'](configs as any, ['football', 'basketball', 'cricket']);

      expect(result).toEqual(['cricket']);
    });
  });

  describe('#setupSportInstance', () => {
    it('should call setupSportInstance', () => {
      const result = service['setupSportInstance']({
        isFootball: true,
        config: {
          request: {
            categoryId: '16'
          },
          tabs: {
            specials: undefined
          }
        }
      } as any);

      expect(gamingService.createNewInstance).toHaveBeenCalled();
      expect(result).toEqual({
        setConfig: jasmine.any(Function),
        sportConfig: {
          specialsTypeIds: [2297, 2562],
          isFootball: true,
          config: {
            eventRequest: { scorecast: true },
            eventMethods,
            tabs: {
              specials: {
                marketsCount: false,
                marketDrilldownTagNamesContains: 'MKTFLAG_SP'
              },
              live: {},
              coupons: {
                date: 'today',
                isActive: true
              },
              today: {
                isNotStarted: true
              },
              tomorrow: {},
              future: {},
              outrights: {
                isActive: true,
                marketsCount: false
              },
            },
            request: {
              categoryId: '16'
            }
          }
        }
      } as any);
    });
  });

  describe('#extendSportConfig', () => {
    let sportConfig;
    let footballTabs;
    let defaultTabs;

    beforeEach(() => {
      sportConfig = {
        config: {
          name: 'football',
          request: {
            categoryId: '16'
          },
          tabs: {
            specials: undefined
          },
          eventMethods: {
            today: 'today'
          },
          tier: 2,
          scoreboardConfig: {
            config: {
              type: 'type',
              label: 'label'
            }
          }
        }
      };

      footballTabs = {
        live: {},
        coupons: {
          date: 'today',
          isActive: true
        },
        today: {
          isNotStarted: true,
          templateMarketNameOnlyIntersects: true
        },
        tomorrow: {
          templateMarketNameOnlyIntersects: true
        },
        future: {
          templateMarketNameOnlyIntersects: true
        },
        outrights: {
          isActive: true,
          marketsCount: false
        },
        upcoming: {
          isNotStarted: true
        },
        specials: {
          marketsCount: false,
          marketDrilldownTagNamesContains: 'MKTFLAG_SP'
        },
        jackpot: {},
        results: {}
      };

      defaultTabs =  {
        live: {},
        coupons: {
          date: 'today',
          isActive: true
        },
        today: {
          isNotStarted: true
        },
        tomorrow: {},
        future: {},
        outrights: {
          isActive: true,
          marketsCount: false
        },
        specials: {
          marketsCount: false,
          marketDrilldownTagNamesContains: 'MKTFLAG_SP'
        }
      };
    });

    it('eventMethods should have tier2EventMethods', () => {
      service['extendSportConfig'](sportConfig);

      expect(sportConfig.config.eventMethods).toEqual(eventMethods);
      expect(sportConfig.specialsTypeIds).toEqual([2297, 2562]);
      expect(sportConfig.config.tabs).toEqual(defaultTabs);
    });

    it('eventMethods should have footballEventMethods', () => {
      sportConfig.config.tier = 1;

      service['extendSportConfig'](sportConfig);

      expect(sportConfig.config.eventMethods).toEqual({
        ...eventMethods,
        competitions: 'competitionsInitClassIds',
        matches: 'blocker',
        jackpot: 'jackpot',
        specials: 'specials'
      });
      expect(sportConfig.specialsTypeIds).toEqual([2297, 2562]);
      expect(sportConfig.config.tabs).toEqual(footballTabs);
    });

    it('eventMethods for outright sport other than golf', () => {
      sportConfig.config.isOutrightSport = true;

      service['extendSportConfig'](sportConfig);

      expect(sportConfig.config.eventMethods).toEqual({
        coupons: 'coupons',
        outrights: 'outrights',
        live: 'blocker',
        results: 'results',
        today: 'outrights',
        tomorrow: 'outrights',
        future: 'outrights',
        upcoming: 'outrights',
        antepost: 'outrights',
        specials: 'specials',
        allEvents: 'todayEventsByClasses',
        matchesTab: 'todayEventsByClasses'
      });
      expect(sportConfig.config.tabs).toEqual(defaultTabs);
      expect(sportConfig.specialsTypeIds).toEqual([2297, 2562]);
    });
    it('eventMethods would be tier2one for outright sport golf', () => {
      sportConfig.config.isOutrightSport = true;
      sportConfig.config.name = 'golf';

      service['extendSportConfig'](sportConfig);

      expect(sportConfig.config.eventMethods).toEqual({
        today: 'todayEventsByClasses',
        tomorrow: 'todayEventsByClasses',
        future: 'todayEventsByClasses',
        upcoming: 'todayEventsByClasses',
        antepost: 'todayEventsByClasses',
        coupons: 'coupons',
        outrights: 'outrights',
        live: 'blocker',
        results: 'results',
        specials: 'specials',
        allEvents: 'todayEventsByClasses',
        matchesTab: 'todayEventsByClasses'
      });
      expect(sportConfig.specialsTypeIds).toEqual([2297, 2562]);
    });

    it('eventMethods should have tier1EventMethods', () => {
      sportConfig.config.tier = 1;
      sportConfig.config.request.categoryId = '6';

      service['extendSportConfig'](sportConfig);

      expect(sportConfig.config.eventMethods).toEqual({
        ...eventMethods,
        competitions: 'competitionsInitClassIds'
      });
      expect(sportConfig.config.tabs).toEqual(defaultTabs);
      expect(sportConfig.config.scoreboardConfig.config.type).toEqual('betGenius');
    });
  });

  describe('#addLegacyConfig', () => {
    let sportConfig;

    beforeEach(() => {
      sportConfig = {
        config: {
          name: 'football',
          request: {
            categoryId: '16'
          },
          eventRequest: null,
          scoreboardConfig: {
            config: {
              type: 'type',
              label: 'label'
            }
          }
        },
        specialsTypeIds: [1, 2, 3]
      };
    });

    it('should change config by categoryId = 16', () => {
      const eventRequest = {
        scorecast: true
      };

      service['addLegacyConfig'](sportConfig);

      expect(sportConfig.specialsTypeIds).toEqual([2297, 2562]);
      expect(sportConfig.config.eventRequest).toEqual(eventRequest);
    });

    it('should change config by categoryId = 51', () => {
      const scoreboardConfig = {
        config: {
          type: 'double',
          label: 'G'
        }
      };
      sportConfig.config.request.categoryId = '51';

      service['addLegacyConfig'](sportConfig);

      expect(sportConfig.config.scoreboardConfig).toEqual(scoreboardConfig);
    });

    it('should change config by categoryId = 6', () => {
      const scoreboardConfig = {
        config: {
          type: 'betGenius'
        }
      };
      sportConfig.config.request.categoryId = '6';

      service['addLegacyConfig'](sportConfig);

      expect(sportConfig.config.scoreboardConfig).toEqual(scoreboardConfig);
    });

    it('should change config by categoryId = 36, 52', () => {
      const scoreboardConfig = {
        config: {
          type: 'double',
          label: 'S'
        }
      };
      sportConfig.config.request.categoryId = '36';

      service['addLegacyConfig'](sportConfig);

      expect(sportConfig.config.scoreboardConfig).toEqual(scoreboardConfig);

      sportConfig.config.request.categoryId = '52';

      service['addLegacyConfig'](sportConfig);

      expect(sportConfig.config.scoreboardConfig).toEqual(scoreboardConfig);
    });

    it('should change config by categoryId = 20', () => {
      const scoreboardConfig = {
        config: {
          type: 'single'
        }
      };
      sportConfig.config.request.categoryId = '20';

      service['addLegacyConfig'](sportConfig);

      expect(sportConfig.config.scoreboardConfig).toEqual(scoreboardConfig);
    });
  });
});
