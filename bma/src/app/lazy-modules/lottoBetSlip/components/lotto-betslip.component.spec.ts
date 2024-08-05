import { fakeAsync, tick, } from '@angular/core/testing';
import { LottoBetslipComponent } from './lotto-betslip.component';
import { ElementRef } from '@angular/core';

describe('LottoBetslipComponent', () => {
    let component: LottoBetslipComponent;
    let pubSubService;
    let betslipService;
    let deviceService;
    let storageService;
    let userService;
    let filterService;
    let betInfoDialogService;
    let localeService;
    let betSlipStakeService;

    beforeEach(fakeAsync(() => {

        storageService = {
            get: jasmine.createSpy('get'),
            set: jasmine.createSpy('set'),
            remove: jasmine.createSpy('remove'),
        }
        const currentDate = new Date();
        currentDate.setDate(currentDate.getDate() + 1);
        const currentDate1 = new Date();
        currentDate1.setDate(currentDate1.getDate() + 2);

        filterService = {
         setCurrency :jasmine.createSpy('setCurrency')

        };
        localeService = {

        };

        userService = {
            currencySymbol: jasmine.createSpy('currencySymbol'),
        };

        pubSubService = {
            API: {
                ADDTOBETSLIP_PROCESS_FINISHED: "Beslipselection",
            },
            updateBetslipData: jasmine.createSpy('updateBetslipData'),
            publish: jasmine.createSpy('publish'),
            publishSync: jasmine.createSpy('publishSync'),
            subscribe: (key, name, callback) => callback()
        };

        betInfoDialogService = {
            multiple: jasmine.createSpy('multiple'),
        };

        betslipService = {
            betData: [
                {
                    Bet: {
                        params: {
                            lottoData: 'test'
                        }
                    }
                }
            ],

            lottobetslipData: [{
               data: {accaBets: [{ id: 1 }]} as any
            }],
            setAmount: jasmine.createSpy('setAmount'),
            count: jasmine.createSpy(),
        };
        
        deviceService={
             isMobileOnly :jasmine.createSpy('isMobileOnly') 
        }
        localeService = {
            getString: jasmine.createSpy('getString').and.returnValue('test_string')
        };

        betSlipStakeService = {
            checkIndex: jasmine.createSpy('checkIndex'),
            maxPayoutCheck: jasmine.createSpy('maxPayoutCheck').and.returnValue(500)
        }
        createComp();
    }));

    function createComp() {
        component = new LottoBetslipComponent(
            pubSubService,
            betslipService,
            deviceService,
            storageService,
            userService,
            filterService,
            betInfoDialogService,
            localeService,
            betSlipStakeService
        )
    }

    it('should create', () => {
        expect(component).toBeDefined();
    });
    it('lottoBetsContainer element Ref', () => {
        component.lottoBetsContainer = { nativeElement: true } as ElementRef;
    })
       
    it('should call ngOnInit() method', fakeAsync(() => {
        spyOn(component, 'updateBetslipData');
        component.ngOnInit();
        tick();
        expect(component.updateBetslipData).toHaveBeenCalled()
    }));

    it('should call updateBetslipData() method', () => {
        component.lottobetslipData = [{
            accaBets: [{ stake: "2", lines: { number: 1 }, winningAmount: 1 }],
            details: { stake: 0, draws: { expanded: true } }
        }];
        component.updateBetslipData();
        expect(component.lottobetslipData.length).toEqual(1);

    });
    it('should call onExpandSummary() method with expand true', () => {
        component.lottobetslipData = [{
            accaBets: [{ id: 1 }] as any
        }];
        component.lottobetslipData = [
            {
                details: {
                    draws: {
                        expanded: true
                    }
                }
            }
        ];
        const event = {
            'currentTarget': {
                'innerText': 'Surprise Me'
            }
        };
        component.onExpandSummary(0, event);
        expect(component.lottobetslipData).toBeTruthy();
    });
    it('should call onExpandSummary() method with expand false', () => {
        component.lottobetslipData = [{
            accaBets: [{ id: 1 }] as any
        }];
        component.lottobetslipData = [
            {
                details: {
                    draws: {
                        expanded: false
                    }
                }
            }
        ];
        const event = {
            'currentTarget': {
                'innerText': 'show summary'
            }
        };
        component.onExpandSummary(0, event);
        expect(component.lottobetslipData).toBeTruthy()
    });
    it('should call onExpandMultiples() method', () => {
        component.lottobetslipData = [
            {
                details: {
                    draws: {
                        expanded: true
                    }
                }
            }
        ];
        const event = {
            'currentTarget': {
                'innerText': 'Surprise Me'
            }
        };
        component.onExpandMultiples(0, event);
        expect(component.lottobetslipData).toBeTruthy();
    });
 
    it('should call onExpandMultiples() method with expand false', () => {
        component.lottobetslipData = [
            {
                details: {
                    draws: {
                        expanded: false
                    }
                }
            }
        ];
        const event = {
            'currentTarget': {
                'innerText': 'hide multiples'
            }
        };
        component.onExpandMultiples(0, event);
        expect(component.lottobetslipData).toBeTruthy();
    });

    it('should call removeFromBetslip() method', () => {
        component.changedFromAllStakeField =true;    
        component.betSlipSingles =[];  
        component.lottobetslipData = [];
        component.removeFromBetslip(0);
       
    });

    it('it should call setAmount()', ()=> {
        component. changedFromAllStakeField = true;
        component.betSlipSingles =[];
        component.setAmount();
        expect(component.changedFromAllStakeField).toBeTruthy();

    })

    it('it should call setAmount() case2', ()=> {
        component. changedFromAllStakeField = true;
        component.isDidigitKeyboardInit = true;
        component.betSlipSingles = ['1'];
        component.setAmount();
        expect(component.changedFromAllStakeField).toBeTruthy();

    })


    it('trackById should return joined string', () => {
        const index: number = 1;
        const betslipStake: any = {
            ballNo: '2'
        };
        const result = component.trackById(index, betslipStake);
        expect(result).toEqual('undefined_1');
    });

    it('trackByDrawId should return joined string', () => {
        const index: number = 1;
        const draw: any = {
            ballNo: '2'
        };
        const result = component.trackByDrawId(index, draw);
        expect(result).toEqual('undefined_1');
    });

    it('should call onDidigitKeyboardInit()', () => {
        component. isDidigitKeyboardInit = true;
        component.onDidigitKeyboardInit();
        expect(component.isDidigitKeyboardInit).toBeTruthy();
    });

    it('should call calculateEstReturns()', () => {
    const stake = 0,
            winningAmtBet = 1,
            winningAmt = 2,
            lineNumbers = 1,
            estReturn = 4;
        component.lottobetslipData = [{
            accaBets: [{ stake: "2", lines: { number: 1 }, winningAmount: 1 }],
            details: { stake: 0, draws: { expanded: true } }
        }];
        const spy1 = spyOn(component, 'calculateReturns')
        component.calculateEstReturns(0, 1)
        expect(stake).toEqual(0)
        expect(winningAmtBet).toEqual(1)
        expect(winningAmt).toEqual(2)
        expect(lineNumbers).toEqual(1)
        expect(estReturn).toEqual(4)
        expect(spy1).toHaveBeenCalled();

    });

    it('should call calculateEstReturns() case2', () => {
        const stake = 0,
                winningAmtBet = 1,
                winningAmt = 2,
                lineNumbers = 1,
                estReturn = 4;
            component.lottobetslipData = [
                {
                    accaBets: [{
                    lines: {
                        number: 1
                    },
                    stake: 10,

                    winningAmount: 1
                    }],
                    details: {
                        stake: 0,
                        draws: [{
                            expanded: true
                        }]
                    }
                }
            ];
            const empty_stake = 0.00;
            component.ngOnInit();
            component.calculateEstReturns(0,0)
            expect(stake).toEqual(0)
            expect(winningAmtBet).toEqual(1)
            expect(winningAmt).toEqual(2)
            expect(lineNumbers).toEqual(1)
            expect(estReturn).toEqual(4)
    
        });

    it('should call openSelectionMultiplesDialog()', () => {
        const multipleBetslipStake = {
            'betTypeRef': {
                'id': 1
            },
            'lines': {
                'number': 123
            }
        };

        component.openSelectionMultiplesDialog(multipleBetslipStake);
        expect(multipleBetslipStake.lines.number).toEqual(123);
    });

    it('should call getTypeLocale()', () => {
        const multipleBetslipStake = {
            'betTypeRef': {
                'id': 1
            },
            'lines': {
                'number': 123
            }
        };

        component.getTypeLocale(multipleBetslipStake);
        expect(multipleBetslipStake.lines.number).toEqual(123);

    });
    
    it('should call getTypeinfo()', () => {
        const multipleBetslipStake = {betTypeRef: {id: 1}};
        component.getTypeinfo(multipleBetslipStake);
        expect(multipleBetslipStake.betTypeRef.id).toEqual(1)
    });

    it('should call getTypeinfo() with keyNotFound', () => {
        const multipleBetslipStake = {betTypeRef: {id: 1}};
        localeService.getString.and.returnValue('KEY_NOT_FOUND');
        component.getTypeinfo(multipleBetslipStake);
        expect( component.getTypeinfo(multipleBetslipStake)).toEqual('');
    });


    it('should call setFocusMultipleIndex()', () => {
        const multiplesIndex = {
            'lottobetslipData': {
                'accaBets': {
                    'id': 1,
                    'stake': 123
                } as any
            }
        }

        component.lottobetslipData = [
            {
                accaBets: [
                    {
                        stake: 1
                    }
                ]
            }
        ]

        component.setFocusMultipleIndex(200, 0, 0);
        expect(component.lottobetslipData).toEqual([
            {
                accaBets: [
                    {
                        stake: 200
                    }
                ]
            }
        ])

    });

    it('should call trackByAccaBets()', () => {
        const index: number = 1;
        const accaBet: any = {
            ballNo: '2'
        };
        const result = component.trackByAccaBets(index, accaBet);
        expect(result).toEqual('undefined_1');
    });

    it('should call getSelectionTotalEstimate() with SGL_S bet type', () => {
        const accasEstReturns = 2 ;
        const bet = { accaBets: [
            {
                "lines": {
                    "number": 2
                },
                "betTypeRef": {
                    "id": "SGL_S"
                },
                "winningAmount": "600",
                "betType": "SGL_S",
                "betLineSummary": [
                    {
                        "lines": {
                            "number": 1
                        },
                        "betTypeRef": {
                            "id": "SGL_S"
                        },
                        "numPicks": 3
                    }
                ],
                "id": "SGL|10|13",
                "estReturns": 0,
                "stake": 1
            },
        ], details: { maxPayOut: 1000, draws: [{}]} };
        const spy = spyOn(component, 'returnStakeValue');
        component.lottobetslipData = [bet];
        component.ngOnInit();
        component.getSelectionTotalEstimate(0, bet);
        expect(spy).toHaveBeenCalled();
        expect(accasEstReturns).toBeTruthy();
    });

    it('should call getSelectionTotalEstimate()', () => {
        const accasEstReturns = 2 ;
        const bet = { accaBets: [
            {
                "lines": {
                    "number": 1
                },
                "betTypeRef": {
                    "id": "TBL"
                },
                "winningAmount": "600",
                "BetType": "TBL",
                "betLineSummary": [
                    {
                        "lines": {
                            "number": 1
                        },
                        "betTypeRef": {
                            "id": "TBL"
                        },
                        "numPicks": 3
                    }
                ],
                "id": "SGL|10|13|14|64776|0",
                "estReturns": 0,
                "stake": 0.1
            },],
            "details": {
                "draws":[{}]
            } };
        const spy = spyOn(component, 'returnStakeValue');
        component.lottobetslipData = [bet];
        component.ngOnInit();
        component.getSelectionTotalEstimate(0, bet);
        expect(spy).toHaveBeenCalled();
        expect(accasEstReturns).toBeTruthy();
    });

    it("should assign false to lottoPayout if stake is zero", () => {
        const bet = { accaBets: [
            {
                "lines": {
                    "number": 1
                },
                "betTypeRef": {
                    "id": "TBL"
                },
                "winningAmount": "600",
                "betType": "TBL",
                "betLineSummary": [
                    {
                        "lines": {
                            "number": 1
                        },
                        "betTypeRef": {
                            "id": "TBL"
                        },
                        "numPicks": 3
                    }
                ],
                "id": "SGL|10|13|14|64776|0",
                "estReturns": 0,
                "stake": 0
            },],
            "details": {
                maxPayOut: 100,
                "draws":[{}]
            } };

            component.lottobetslipData = [bet];
        component.ngOnInit();

        const val = component.calculateReturns(0, bet, 0);
        expect(val).toBe(0);
    });

    it("should assign maxPayout value if value is greather than maxPayout", () => {
        const bet = { accaBets: [
            {
                "lines": {
                    "number": 1
                },
                "betTypeRef": {
                    "id": "TBL"
                },
                "winningAmount": "600",
                "betType": "TBL",
                "betLineSummary": [
                    {
                        "lines": {
                            "number": 1
                        },
                        "betTypeRef": {
                            "id": "TBL"
                        },
                        "numPicks": 3
                    }
                ],
                "id": "SGL|10|13|14|64776|0",
                "estReturns": 0,
                "stake": 700
            },],
            "details": {
                maxPayOut: 500,
                "draws":[{}]
            } };

            component.lottobetslipData = [bet];
        component.ngOnInit();

        const val = component.calculateReturns(0, bet, 0);
        expect(val).toBe(500);
    });

    it(" should emit onFilterSelect event", fakeAsync(() => {
        component.lottoBetsContainerEl = { elementRef: { nativeElement: true } } as any;
        spyOn(component.lottoBetsEmitter, 'emit');
        component.ngAfterViewChecked();
        expect(component.lottoBetsEmitter.emit).toHaveBeenCalledWith({elementRef:{ nativeElement: true }});     
     }));

     it('should call ngOnDestroy', () => {
        component.ngOnDestroy();
        expect(betSlipStakeService['checkIndex']).toHaveBeenCalled();
     })
 });
