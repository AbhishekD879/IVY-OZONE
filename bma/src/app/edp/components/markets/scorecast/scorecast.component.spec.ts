import { ScorecastComponent } from '@edp/components/markets/scorecast/scorecast.component';

const firstMarketMock = {
  id: '1',
  name: 'First Goal Scorecast',
  isLpAvailable: true,
  cashoutAvail: 'Y',
  outcomes: [
    {
      displayOrder: NaN,
      id: '487',
      name: undefined,
      prices: [],
      scorecastPrices: '959656009,295,1,296.00,959655817,300,1,301.00,959655816,160,1,161.00,959655820,1050,1,1051.00,',
      scorerOutcomeId: '959656009'
    }
  ],
  templateMarketName: 'First Goal Scorecast'
};

const outcome = {
  correctPriceType: 'correctPriceType',
    correctedOutcomeMeaningMinorCode: 213,
  displayOrder: 11,
  fakeOutcome: true,
  icon: true,
  id: 'id',
  isUS: true,
  liveServChannels: 'liveServChannels',
  liveServChildrenChannels: 'liveServChildrenChannels',
  name: 'liveServChildrenChannels',
  outcomeMeaningMajorCode: 'outcomeMeaningMajorCode',
  outcomeMeaningMinorCode: 1123,
  outcomeStatusCode: 'outcomeMeaningMinorCode',
  alphabetName: 'liveServChildrenChannels'
};

const teamsMock = [
  {
    name: 'teamA name',
    outcomeMeaningMinorCode: 1
  },
  {
    name: 'teamH name',
    outcomeMeaningMinorCode: 3
  }
];

const scoreCastMarkets = [{
  teamsGoalscorers: {},
  market: [{
    cashoutAvail: 'cashoutAvail',
    correctPriceTypeCode: 'correctPriceTypeCode',
    dispSortName: 'dispSortName',
    eachWayFactorNum: 'eachWayFactorNum',
    eachWayFactorDen: 'eachWayFactorDen',
    eachWayPlaces: 'eachWayPlaces',
    header: 'header',
    id: 'id',
    name: 'nameTest'
  }],
  name: 'name',
  localeName: 'localeName',
  goalscorerMarket: [{
    cashoutAvail: 'cashoutAvail',
    correctPriceTypeCode: 'correctPriceTypeCode',
    dispSortName: 'dispSortName',
    eachWayFactorNum: 'eachWayFactorNum',
    eachWayFactorDen: 'eachWayFactorDen',
    eachWayPlaces: 'eachWayPlaces',
    header: 'header',
    id: 'id',
    name: 'nameTest'
  }],
  outcome: {
    correctPriceType: 'correctPriceType',
    correctedOutcomeMeaningMinorCode: 213,
    displayOrder: 11,
    fakeOutcome: true,
    icon: true,
    id: 'id',
    isUS: true,
    liveServChannels: 'liveServChannels',
    liveServChildrenChannels: 'liveServChildrenChannels',
    name: 'liveServChildrenChannels',
    outcomeMeaningMajorCode: 'outcomeMeaningMajorCode',
    outcomeMeaningMinorCode: 1123,
    outcomeStatusCode: 'outcomeMeaningMinorCode'
  },
  scorecasts: []
}] as any;


describe('AppScorecastComponent', () => {
  const fracToDecFactory: any = {
    getFormattedValue: jasmine.createSpy('getFormattedValue').and.returnValue('4/1')
  };
  const scorecastService: any = {
    getMarketByMarketNamePattern: jasmine.createSpy('getMarketByMarketNamePattern').and.returnValue(firstMarketMock),
    isAnyCashoutAvailable: jasmine.createSpy('isAnyCashoutAvailable').and.returnValue(false),
    getTeams: jasmine.createSpy('getTeams').and.returnValue(teamsMock),
    getMarketOutcomesByTeam: jasmine.createSpy('getMarketOutcomesByTeam').and.returnValue({
      [teamsMock[0].name]: [firstMarketMock.outcomes[0]]
    }),
    getDefaultScorecastMarketName: jasmine.createSpy('getDefaultScorecastMarketName').and.returnValue(firstMarketMock.name),
    getMaxScoreValues: jasmine.createSpy('getMaxScoreValues').and.returnValue({
      teamH: [0, 1, 2, 3, 4, 5],
      teamA: [0, 1, 2, 3, 4, 5]
    }),
    getCombinedOutcome: jasmine.createSpy('getCombinedOutcome').and.returnValue(firstMarketMock.outcomes[0]),
    getCombinedOutcomePrices: jasmine.createSpy('getCombinedOutcomePrices').and.returnValue({
      priceDen: 4,
      priceNum: 1
    }),
    setGtmData: jasmine.createSpy('setGtmData').and.returnValue(''),
    setBetslipGtmData: jasmine.createSpy('setBetslipGtmData').and.returnValue(''),
    getFormattedValue: jasmine.createSpy('getFormattedValue').and
  };
  const betSlipSelectionsData: any = {};
  const priceOddsButtonService: any = {};
  const pubsubService: any = {};
  const localeService: any = {
    getString : ()=>{
      return ''
    }
  };
  const filterService: any = {
    orderBy: jasmine.createSpy().and.returnValue({
      outcomeStatusCode: 'test'
    })
  };

  const scorecastDataService = {
    setScorecastData: (data)=> { return data},
    getScorecastData: ()=> { return 'data'},
  } as any;

  let component;

  beforeEach(() => {
    component = new ScorecastComponent(
      fracToDecFactory,
      scorecastService,
      betSlipSelectionsData,
      priceOddsButtonService,
      pubsubService,
      localeService,
      filterService,
      scorecastDataService
    );
  });

  it('should test trackById function', () => {
    const result = component.trackById(1, {
      id: '000'
    });

    expect(result).toEqual('1-000');
  });

  describe('applyData', ()  => {

    it('should initialise component with applyData function', () => {
      spyOn(component, 'resetTeamsScores').and.callThrough();
      spyOn(component, 'selectCorrectScore').and.callThrough();
      firstMarketMock.id = '1';
      component.applyData();

      expect(component.resetTeamsScores).toHaveBeenCalled();
      expect(component.selectCorrectScore).toHaveBeenCalled();
    });

    it('should reset selector state with function resetSelectedScore', () => {
      firstMarketMock.id = '1';
      component.applyData();
      component.scoreH = {
         nativeElement: {
           options: {
             selectedIndex: 1
           }
         }
       };

      component.scoreA = {
        nativeElement: {
          options: {
            selectedIndex: 1
          }
        }
      };

      component.resetSelectedScore();

      expect(component.scoreH.nativeElement.options.selectedIndex).toEqual(0);
      expect(component.scoreA.nativeElement.options.selectedIndex).toEqual(0);
      expect(component.teams.teamA.score).toEqual(0);
      expect(component.teams.teamH.score).toEqual(0);
    });
  });

  it('should reset selector when switching market', () => {
    component.ngOnInit();
    component.scoreH = {
      nativeElement: {
        options: {
          selectedIndex: 1
        }
      }
    };

    component.scoreA = {
      nativeElement: {
        options: {
          selectedIndex: 1
        }
      }
    };
    component.selectScorecastMarket(firstMarketMock.name);
  });

  it('should call resetSelectedScore', () => {
    component.ngOnInit();

    component.scoreA = {
      nativeElement: {
        options: {
          selectedIndex: 1
        }
      }
    };
    spyOn(component, 'resetSelectedScore');
    component.scorecastMarkets = {
      teamsGoalscorers: {
        'teamA name': [],
      'teamH name': []
      },
      market: [{
        cashoutAvail: 'cashoutAvail',
        correctPriceTypeCode: 'correctPriceTypeCode',
        dispSortName: 'dispSortName',
        eachWayFactorNum: 'eachWayFactorNum',
        eachWayFactorDen: 'eachWayFactorDen',
        eachWayPlaces: 'eachWayPlaces',
        header: 'header',
        id: 'id',
        name: 'nameTest'
      }],
      resetSelectedScore: {
        localeName: 'test'
      }
    };
    component.selectScorecastMarket('resetSelectedScore');
    expect(component.resetSelectedScore).toHaveBeenCalled();
  });

  it('should work without data ', () => {
    scorecastService.isAnyCashoutAvailable = jasmine.createSpy('isAnyCashoutAvailable');
    scorecastService.getMarketByMarketNamePattern.and.returnValue(undefined);
    spyOn(component as any, 'getMaxValues').and.callThrough();

    component.ngOnInit();

    expect(scorecastService.isAnyCashoutAvailable).not.toHaveBeenCalled();
    expect(component['getMaxValues']).not.toHaveBeenCalled();
  });

  it('should check selectedScorecastMarket data', () => {
    component.selectedScorecastMarket = undefined;

    expect(component.isGoalScorerMarketSuspended).toEqual(undefined);

    component.selectedScorecastMarket = {
      goalscorerMarket: null
    };

    expect(component.isGoalScorerMarketSuspended).toEqual(null);

    component.selectedScorecastMarket = {
      goalscorerMarket: {
        marketStatusCode: 'A'
      }
    };

    expect(component.isGoalScorerMarketSuspended).toEqual(false);

    component.selectedScorecastMarket = {
      goalscorerMarket: {
        marketStatusCode: 'S'
      }
    };

    expect(component.isGoalScorerMarketSuspended).toEqual(true);
  });

  it('should check correctScore data', () => {
    component.correctScore = undefined;

    expect(component.isCorrectScoreMarketSuspended).toEqual(undefined);

    component.correctScore = {
      marketStatusCode: 'A'
    };

    expect(component.isCorrectScoreMarketSuspended).toEqual(false);

    component.correctScore = {
      marketStatusCode: 'S'
    };

    expect(component.isCorrectScoreMarketSuspended).toEqual(true);
  });

  it('should check selectedCorrectScoreOutcome data', () => {
    component.selectedCorrectScoreOutcome = undefined;

    expect(component.isCorrectScoreOutcomeSuspended).toEqual(undefined);

    component.selectedCorrectScoreOutcome = {
      outcome: null
    };

    expect(component.isCorrectScoreOutcomeSuspended).toEqual(null);

    component.selectedCorrectScoreOutcome = {
      outcome: {
        outcomeStatusCode: 'A'
      }
    };

    expect(component.isCorrectScoreOutcomeSuspended).toEqual(false);

    component.selectedCorrectScoreOutcome = {
      outcome: {
        outcomeStatusCode: 'S'
      }
    };

    expect(component.isCorrectScoreOutcomeSuspended).toEqual(true);
  });

  it('should check scorecastMarket data', () => {
    let mock = {};
    component.selectedScorecastMarket = null;

    expect(component.isScorecastMarketSuspended()).toEqual(null);


    expect(component.isScorecastMarketSuspended(mock)).toEqual(undefined);

    mock = {
      market: null
    };

    expect(component.isScorecastMarketSuspended(mock)).toEqual(null);

    mock = {
      market: {
        marketStatusCode: 'A'
      }
    };

    expect(component.isScorecastMarketSuspended(mock)).toEqual(false);


    mock = {
      market: {
        marketStatusCode: 'S'
      }
    };

    expect(component.isScorecastMarketSuspended(mock)).toEqual(true);
  });

  it('should selectGoalscorerTeam', () => {
    const teamA = { name: 'test' };
    const teamB = { name: 'best' };
    const teamAPlayers = [{ name: 'p6' }, { name: 'p3' }];
    const teamBPlayers = [{ name: 'p3' }, { name: 'p4' }];

    component.ngOnInit();
    component.teamsArray = [teamA, teamB];
    component.selectedScorecastMarket.teamsGoalscorers = {
      'test': teamAPlayers,
      'best': teamBPlayers
    };
    component.selectGoalscorerTeam(teamB);
    // expect(component.selectedGoalscorerTeam).toEqual(teamB);
    // expect(component.goalscorerOutcomes).toEqual(teamBPlayers);
    // expect(component.selectedGoalscorerOutcome.outcome).toEqual(teamBPlayers[0]);
  });

  it('should buildCumulativeOdd', () => {
    const teamB = { name: 'best' };
    const teamAPlayers = [{ name: 'p6' }, { name: 'p3' }];
    const teamBPlayers = [{ name: 'p3' }, { name: 'p4' }];

    component.ngOnInit();
    component.teamsArray = [{ name: 'test' }, teamB];
    component.selectedScorecastMarket.teamsGoalscorers = {
      'test': teamAPlayers,
      'best': teamBPlayers
    };
    spyOn(component, 'buildCumulativeOdd');
    component.selectGoalscorerTeam({ name: 'test' });
    expect(component.buildCumulativeOdd).toHaveBeenCalled();
  });

  describe('trackByIndex', ()  => {
    it('should call trackByIndex and return index 12', () => {
     const result = component.trackByIndex(12);
     expect(result).toEqual(12);
    });
    it('should call trackByIndex and return index 1', () => {
     const result = component.trackByIndex(1);
     expect(result).toEqual(1);
    });
  });

  describe('selectCorrectScore', ()  => {
    it('component teams should be scoreMatkets', () => {
     component.teams = {
        milan: {
          score: []
        },
        chelsea: {
          score: []
        }
      };
     component.correctScore = {
        outcomes: outcome
      };
     spyOn(component, 'buildCumulativeOdd');
     component.selectCorrectScore(scoreCastMarkets[0], 'chelsea');
     expect(component['teams'].chelsea.score).toEqual(scoreCastMarkets[0]);
     expect(component['buildCumulativeOdd']).toHaveBeenCalled();
    });
  });

  describe('getSwitcherText', ()  => {
    it('should call getSwitcherText and return index 12', () => {
      localeService.getString = jasmine.createSpy('getString').and.callFake((p1) => {
        return p1;
      });
     const result = component.getSwitcherText(scoreCastMarkets[0]);
     expect(result).toEqual(`sb.${scoreCastMarkets[0].localeName}`);
    });
  });

  describe('isScorecastDisabled', ()  => {
    it('should call isScorecastDisabled and return true', () => {
      component.selectedScorecastTab = 'First Score';
      component['eventEntity'] = {
        eventStatusCode: {}
      };
      const result = component.isScorecastDisabled(scoreCastMarkets[0]);
      expect(result).toEqual(false);
    });
    it('should call isScorecastDisabled and return true', () => {
      component.selectedScorecastTab = 'First Score';
      component['eventEntity'] = {
        eventStatusCode: 'S'
      };
      const result = component.isScorecastDisabled(scoreCastMarkets[0]);
      expect(result).toEqual(true);
    });
  });
  describe('addToMultiples', ()  => {
    it('should call isScorecastDisabled and return true', () => {
      const event = {} as MessageEvent;
      component.teamsArray = [
        {name: 'teamA'},
        {name: 'teamB'},
      ];
      component.teams = {
        teamH: 2,
        teamA: 1
      };
      component['eventEntity'] = {
        id: '1',
        eventIsLive: 1,
        categoryName: 'categoryName',
        typeId: 'typeId',
        categoryId: 'categoryId',
        eventStatusCode: {}
      };
      component['selectedGoalscorerOutcome'] = {
        outcome: outcome
      };
      component['selectedScorecastMarket'] = {
        market: scoreCastMarkets
      };
      component['selectedCorrectScoreOutcome'] = {
        outcome: outcome
      };
      component['selectedGoalscorerTeam'] = {
        name: 'name'
      };
      component['cumulativeOdd'] = {};
      component.selectedScorecastTab = '';

      priceOddsButtonService['animate'] = jasmine.createSpy('animate').and.returnValue(Promise.resolve(event));
      pubsubService['publish'] = jasmine.createSpy('publish');
      pubsubService.API = {
        ADD_TO_BETSLIP_BY_SELECTION: 'ADD_TO_BETSLIP_BY_SELECTION'
      };

      component.addToMultiples(event);

      expect(priceOddsButtonService['animate']).toHaveBeenCalled();
    });
    it('should call isScorecastDisabled and return true eventLive false', () => {
      const event = {} as MessageEvent;
      component.teamsArray = [
        {name: 'teamA'},
        {name: 'teamB'},
      ];
      component.teams = {
        teamH: 2,
        teamA: 1
      };
      component['eventEntity'] = {
        id: '1',
        eventIsLive: 0,
        categoryName: 'categoryName',
        typeId: 'typeId',
        categoryId: 'categoryId',
        eventStatusCode: {}
      };
      component['selectedGoalscorerOutcome'] = {
        outcome: outcome
      };
      component['selectedScorecastMarket'] = {
        market: scoreCastMarkets
      };
      component['selectedCorrectScoreOutcome'] = {
        outcome: outcome
      };
      component['selectedGoalscorerTeam'] = {
        name: 'name'
      };
      component['cumulativeOdd'] = {};
      component.selectedScorecastTab = '';

      priceOddsButtonService['animate'] = jasmine.createSpy('animate').and.returnValue(Promise.resolve(event));
      pubsubService['publish'] = jasmine.createSpy('publish');
      pubsubService.API = {
        ADD_TO_BETSLIP_BY_SELECTION: 'ADD_TO_BETSLIP_BY_SELECTION'
      };

      component.addToMultiples(event);

      expect(priceOddsButtonService['animate']).toHaveBeenCalled();
    });
  });

  describe('isInBetslip', ()  => {
    it('should call betSlipSelectionsData and return true', () => {
      const result = component.isInBetslip();
      expect(result).toBe(false);
    });
    it('should call isScorecastDisabled and return true', () => {

      component['selectedGoalscorerOutcome'] = {
        outcome: outcome
      };
      component['selectedCorrectScoreOutcome'] = {
        outcome: outcome
      };
      betSlipSelectionsData['contains'] = jasmine.createSpy('contains').and.returnValue(true);

      const result = component.isInBetslip();
      expect(result).toBe(true);
      expect(betSlipSelectionsData['contains']).toHaveBeenCalledWith([outcome.id, outcome.id], [outcome.id, outcome.id]);
    });

  });

  describe('isScoreDisabled', ()  => {
    it('should return isScoreDisabled',  () => {
      component['eventEntity'] = {
        eventStatusCod: 'S'
      };

      component.selectedScorecastMarket = {
        goalscorerMarket: {
          marketStatusCode: 'S'
        }
      };
      component['isScorecastMarketSuspended'] = jasmine.createSpy().and.returnValue(true);
      const result = component['isScoreDisabled'];
      expect(result).toBe(true);
    });
    it('should return isScorecastMarketSuspended',  () => {
      component['eventEntity'] = {
        eventStatusCod: 'P'
      };

      component.selectedScorecastMarket = {
        goalscorerMarket: {
          marketStatusCode: 'P'
        }
      };
      component['selectedScorecastMarket'] = {
        goalscorerMarket: {
          marketStatusCode: 'S'
        }
      };
      component['isScorecastMarketSuspended'] = jasmine.createSpy().and.returnValue(false);
      const result = component['isScoreDisabled'];
      expect(result).toBe(true);
    });

    it('should return isCorrectScoreMarketSuspended false', () => {
      component['eventEntity'] = {
        eventStatusCod: 'P'
      };

      component.selectedScorecastMarket = {
        goalscorerMarket: {
          marketStatusCode: 'P'
        }
      };
      component['selectedScorecastMarket'] = {
          marketStatusCode: 'P'
      };
      component['correctScore'] = {
        goalscorerMarket: {
          marketStatusCode: 'P'
        }
      };
      component['isScorecastMarketSuspended'] = jasmine.createSpy().and.returnValue(false);
      const result = component['isScoreDisabled'];
      expect(result).toBe(false);
    });

    it('should return isCorrectScoreMarketSuspended true', () => {
      component['eventEntity'] = {
        eventStatusCod: 'P'
      };

      component.selectedScorecastMarket = {
        goalscorerMarket: {
          marketStatusCode: 'P'
        }
      };
      component['selectedScorecastMarket'] = {
          marketStatusCode: 'P'
      };
      component['correctScore'] = {
        goalscorerMarket: {
          marketStatusCode: 'P'
        }
      };
      component['isScorecastMarketSuspended'] = jasmine.createSpy().and.returnValue(false);
      const result = component['isScoreDisabled'];
      expect(result).toBe(false);
    });

  });

  describe('isAddToBetslipDisabled', ()  => {
    it('should return isScoreDisabled', () => {
      component['eventEntity'] = {
        eventStatusCod: 'S'
      };

      component.selectedScorecastMarket = {
        goalscorerMarket: {
          marketStatusCode: 'S'
        }
      };
      component['isScorecastMarketSuspended'] = jasmine.createSpy().and.returnValue(true);
      component['cumulativeOdd'] = true;
      const result = component['isAddToBetslipDisabled'];
      expect(result).toBe(true);
    });

    it('should return isGoalScorerMarketSuspended', () => {

      component.selectedScorecastMarket = {
        goalscorerMarket: {
          marketStatusCode: 'S'
        }
      };
      component['eventEntity'] = {
        eventStatusCod: 'P'
      };
      component['selectedScorecastMarket'] = {
        marketStatusCode: 'P'
      };
      component['correctScore'] = {
        goalscorerMarket: {
          marketStatusCode: 'P'
        },
        marketStatusCode: 'S'
      };

      component['isScorecastMarketSuspended'] = jasmine.createSpy().and.returnValue(false);
      component['cumulativeOdd'] = true;
      const result = component['isAddToBetslipDisabled'];
      expect(result).toBe(true);
    });

    it('should return isCorrectScoreOutcomeSuspended true', () => {

      component.selectedScorecastMarket = {
        goalscorerMarket: {
          marketStatusCode: 'S'
        }
      };
      component['eventEntity'] = {
        eventStatusCod: 'P'
      };
      component['selectedScorecastMarket'] = {
        marketStatusCode: 'P'
      };
      component['correctScore'] = {
        goalscorerMarket: {
          marketStatusCode: 'P'
        },
        marketStatusCode: 'S'
      };

      component['selectedCorrectScoreOutcome'] = {
        outcome: {
          outcomeStatusCode: 'S'
        },
      };

      component['isScorecastMarketSuspended'] = jasmine.createSpy().and.returnValue(false);
      component['cumulativeOdd'] = true;
      const result = component['isAddToBetslipDisabled'];
      expect(result).toBe(true);
    });

    it('should return isCorrectScoreOutcomeSuspended false', () => {
      component.selectedScorecastMarket = {
        goalscorerMarket: {
          marketStatusCode: 'P'
        }
      };
      component['eventEntity'] = {
        eventStatusCod: 'P'
      };
      component['selectedScorecastMarket'] = {
        marketStatusCode: 'P'
      };
      component['correctScore'] = {
        goalscorerMarket: {
          marketStatusCode: 'P'
        },
        marketStatusCode: 'P'
      };

      component['selectedCorrectScoreOutcome'] = {
        outcome: {
          outcomeStatusCode: 'P'
        },
      };

      component['isScorecastMarketSuspended'] = jasmine.createSpy().and.returnValue(false);
      component['cumulativeOdd'] = true;
      const result = component['isAddToBetslipDisabled'];
      expect(result).toBe(false);
    });
  });

  describe('isGoalscorerDisabled', ()  => {
    it('should call', () => {
      component['eventEntity'] = {
        eventStatusCod: 'S'
      };

      component.selectedScorecastMarket = {
        goalscorerMarket: {
          marketStatusCode: 'S'
        }
      };
      component['isScorecastMarketSuspended'] = jasmine.createSpy().and.returnValue(true);
      const result = component['isGoalscorerDisabled'];
      expect(result).toBe(true);
    });

    it('should call isEventSuspended false', () => {
      component['eventEntity'] = {
        eventStatusCod: 'P'
      };

      component.selectedScorecastMarket = {
        goalscorerMarket: {
          marketStatusCode: 'P'
        }
      };
      component['isScorecastMarketSuspended'] = jasmine.createSpy().and.returnValue(true);
      const result = component['isGoalscorerDisabled'];
      expect(result).toBe(true);
    });

    it('should call isEventSuspended true', () => {
      component['eventEntity'] = {
        eventStatusCod: 'S'
      };

      component.selectedScorecastMarket = {
        goalscorerMarket: {
          marketStatusCode: 'S'
        }
      };
      component['isScorecastMarketSuspended'] = jasmine.createSpy().and.returnValue(false);
      const result = component['isGoalscorerDisabled'];
      expect(result).toBe(true);
    });
    it('should return false', () => {
      component['eventEntity'] = {
        eventStatusCod: 'P'
      };

      component.selectedScorecastMarket = {
        goalscorerMarket: {
          marketStatusCode: 'P'
        }
      };
      component['isScorecastMarketSuspended'] = jasmine.createSpy().and.returnValue(false);
      const result = component['isGoalscorerDisabled'];
      expect(result).toBe(false);
    });

  });

  describe('goalscorerChanged', ()  => {


    it('should call buildCumulativeOdd', () => {
      component['selectedGoalscorerOutcome'] = {};
      component['selectedGoalscorerTeamScorers'] = [{
        correctPriceType: 'correctPriceType',
        correctedOutcomeMeaningMinorCode: 213,
        displayOrder: 11,
        fakeOutcome: true,
        icon: true,
        id: 'id',
        isUS: true,
        liveServChannels: 'liveServChannels',
        liveServChildrenChannels: 'liveServChildrenChannels',
        name: 'liveServChildrenChannels',
        outcomeMeaningMajorCode: 'outcomeMeaningMajorCode',
        outcomeMeaningMinorCode: 1123,
        outcomeStatusCode: 'outcomeMeaningMinorCode',
        alphabetName: 'liveServChildrenChannels'
      }];


      localeService.getString = jasmine.createSpy('getString').and.callFake((p1) => {
        return p1;
      });
      spyOn(component, 'buildCumulativeOdd');

     component.goalscorerChanged('liveServChildrenChannels');
     expect(component['selectedGoalscorerOutcome'].outcome).toEqual(outcome);
     expect(component['buildCumulativeOdd']).toHaveBeenCalled();
    });

    it('component selectedGoalscorerOutcome outcome should be undefined', () => {
      component['selectedGoalscorerOutcome'] = {};
      component['selectedGoalscorerTeamScorers'] = [{
        correctPriceType: 'correctPriceType',
        correctedOutcomeMeaningMinorCode: 213,
        displayOrder: 11,
        fakeOutcome: true,
        icon: true,
        id: 'id',
        isUS: true,
        liveServChannels: 'liveServChannels',
        liveServChildrenChannels: 'liveServChildrenChannels',
        name: 'liveServChildrenChannels',
        outcomeMeaningMajorCode: 'outcomeMeaningMajorCode',
        outcomeMeaningMinorCode: 1123,
        outcomeStatusCode: 'S'
      }];


      localeService.getString = jasmine.createSpy('getString').and.callFake((p1) => {
        return p1;
      });
      spyOn(component, 'buildCumulativeOdd');

     component.goalscorerChanged('S');
     expect(component['selectedGoalscorerOutcome'].outcome).toEqual(undefined);
     expect(component['buildCumulativeOdd']).toHaveBeenCalled();
    });

    it('component selectedGoalscorerOutcome outcome should be outcomes', () => {
      component['selectedGoalscorerOutcome'] = {};
      component['selectedGoalscorerTeamScorers'] = [{
        correctPriceType: 'correctPriceType',
        correctedOutcomeMeaningMinorCode: 213,
        displayOrder: 11,
        fakeOutcome: true,
        icon: true,
        id: 'id',
        isUS: true,
        liveServChannels: 'liveServChannels',
        liveServChildrenChannels: 'liveServChildrenChannels',
        name: 'liveServChildrenChannels',
        outcomeMeaningMajorCode: 'outcomeMeaningMajorCode',
        outcomeMeaningMinorCode: 1123,
        outcomeStatusCode: 'outcomeMeaningMinorCode',
        alphabetName: 'liveServChildrenChannels'
      }];


      localeService.getString = jasmine.createSpy('getString').and.callFake((p1) => {
        return p1;
      });
      spyOn(component, 'buildCumulativeOdd');

     component.goalscorerChanged('S');
     expect(component['selectedGoalscorerOutcome'].outcome).toEqual(outcome);
     expect(component['buildCumulativeOdd']).toHaveBeenCalled();
    });
  });

  it('should call selectScorecastMarket', () => {

    firstMarketMock.id = '';
    scorecastService.getMarketByMarketNamePattern = jasmine.createSpy('getMarketByMarketNamePattern').and.returnValue(firstMarketMock);
    component.selectScorecastMarket = jasmine.createSpy('resetTeamsScores');
    component.scorecastMarkets = scoreCastMarkets;
    component.scorecastMarketName = 'Test';
    
    component.applyData();

    component.scoreH = {
      nativeElement: {
        options: {
          selectedIndex: 1
        }
      }
    };

    component.scoreA = {
      nativeElement: {
        options: {
          selectedIndex: 1
        }
      }
    };
    component.resetSelectedScore();


    expect(component.selectScorecastMarket).toHaveBeenCalled();
  });

});
