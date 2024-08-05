import { FeaturedQuickLinksComponent } from '@featured/components/featured-quick-links/featured-quick-links.component';

describe('FeaturedQuickLinksComponent', () => {
  let component: FeaturedQuickLinksComponent;

  let windowRef;
  let gtmService;
  let router;
  let quickLinskData;
  let linkDestinationMock;
  let linkDestinationWithoutOrigin;
  let event;
  let pubSubService;
  let changeDetectorRef;
  let bonusSuppressionService;
  let flagSourceService;
  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        location: {
          origin: 'https://bm-tst1.coral.co.uk',
          href: ''
        }
      }
    };

    router = {
      navigate: jasmine.createSpy(),
      navigateByUrl: jasmine.createSpy()
    };

    gtmService = {
      push: jasmine.createSpy('push')
    };

    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true)
    };

    linkDestinationMock = 'https://bm-tst1.coral.co.uk/linkDestination';
    linkDestinationWithoutOrigin = '/linkDestination';

    quickLinskData = {
      data: [{
        destination: linkDestinationMock,
        displayOrder: -11,
        id: '5bf3c940c9e77c0001238a52',
        svg: '<symbol id="0169fbe3-ff05-3910-94bf-13a07fa2ba16"</symbol>',
        title: 'BBC'
      }]
    };

    flagSourceService = {
      flagUpdate: {subscribe: (cb) => cb({ShowQuickLinks: true})}
    };

    event = {
      preventDefault: jasmine.createSpy()
    };

    pubSubService = {
      subscribe: jasmine.createSpy().and.callFake((a, b, cb) => cb && cb()),
      API: {
        SESSION_LOGIN: 'SESSION_LOGIN',
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN'
      },
      unsubscribe: jasmine.createSpy('unsubscribe'),
    }

    changeDetectorRef = {
      detectChanges: jasmine.createSpy(),
      detach: jasmine.createSpy()
    };

    component = new FeaturedQuickLinksComponent(windowRef, router, gtmService, pubSubService,changeDetectorRef, bonusSuppressionService, flagSourceService);
  });

  it('trackByLink() Compose unique string for each slide in collection', () => {
    const element = {
      id: 112,
      title: 'titleOFelement'
    } as any;

    expect(component.trackByLink(33, element)).toEqual('33_112');
  });

  it('clickOnLink() Check navigation by clicking on Quick link. Domain belongs to Coral', () => {
    component.clickOnLink(event, quickLinskData.data[0], 1);
    expect(gtmService.push).toHaveBeenCalled();
    expect(router.navigateByUrl).toHaveBeenCalledWith(linkDestinationWithoutOrigin);
  });

  it('clickOnLink() Check navigation by clicking on Quick link. Domain does NOT belongs to Coral', () => {
    const changedLinkObj = quickLinskData.data[0];

    changedLinkObj.destination = 'https://wwww.nocoraldomain.co.uk/fakeUrl';
    component.clickOnLink(event, changedLinkObj, 1);
    expect(component['windowRef'].nativeWindow.location.href).toEqual(changedLinkObj.destination);
  });

  it('should use OnPush strategy', () => {
    expect(FeaturedQuickLinksComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  describe('#ngOnInit', () => {
    it('should initialize on #ngOnInit', () =>{
      component.quickLinks = {
        data: quickLinskData.data,
        showExpanded: false,
        title: 'quick-links',
        sportId: 1231231,
        _id: '12313 '
      };
      component.ngOnInit();
      expect(component.quickLinks.data.length).toEqual(1);
    });
    it('should filter out quick links on init #filterQuickLinksBasedOnRGYellow', () =>{
      component.quickLinks = {
        data: quickLinskData.data,
        showExpanded: false,
        title: 'quick-links',
        sportId: 1231231,
        _id: '12313 '
      };
      component.filterQuickLinksBasedOnRGYellow();
      expect(component.quickLinks.data.length).toEqual(1);
    });
    it('should not filter out quick links on init if quickLinks data is null #filterQuickLinksBasedOnRGYellow', () =>{
      component.quickLinks = {
        data: null,
        showExpanded: false,
        title: 'quick-links',
        sportId: 1231231,
        _id: '12313 '
      };
      component.filterQuickLinksBasedOnRGYellow();
      expect(bonusSuppressionService.checkIfYellowFlagDisabled).not.toHaveBeenCalled();
    });
    it('should not filter out quick links on init if quickLinks data is null #filterQuickLinksBasedOnRGYellow', () =>{
      component.quickLinks = null;
      component.filterQuickLinksBasedOnRGYellow();
      expect(bonusSuppressionService.checkIfYellowFlagDisabled).not.toHaveBeenCalled();
    });
  })

  describe('#ngOnChanges', () =>{

    it('filter out the quick links on quickLinks value changes' , () =>{
      
      component.quickLinks = {
        data: quickLinskData.data,
        showExpanded: false,
        title: 'quick-links',
        sportId: 1231231,
        _id: '12313 '
      };
      component['filterQuickLinksBasedOnRGYellow'] = jasmine.createSpy();
      component.ngOnChanges({ quickLinks: true as any});
      expect(component['filterQuickLinksBasedOnRGYellow']).toHaveBeenCalled();
    })
  })

  describe('#ngOnDestroy', ()=>{
    it('should call pubSubService.unsubscribe', () =>{
      const controllerIdentifier = 'FeaturedQuickLinks';
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith(controllerIdentifier);
    })
  })
  it('updateTitle if title is odd and length greator than 55  ' , () =>{
      
    component.quickLinks = {
      data: [{
        destination: linkDestinationMock,
        displayOrder: -11,
        id: '5bf3c940c9e77c0001238a52',
        svg: '<symbol id="0169fbe3-ff05-3910-94bf-13a07fa2ba16"</symbol>',
        title: 'BBC'
      }],
      showExpanded: false,
      title: 'quick-links',
      sportId: 1231231,
      _id: '12313 '
    } as any;
    const quickLink = {
      destination: linkDestinationMock,
      displayOrder: -11,
      id: '5bf3c940c9e77c0001238a52',
      svg: '<symbol id="0169fbe3-ff05-3910-94bf-13a07fa2ba16"</symbol>',
      title: 'South Africa v England Cricket World Cup123456789012343Test1'
    }
    component.updateTitle(quickLink);
    expect(component.updateTitle(quickLink)).toEqual('South Africa v England Cricket World Cup123456789012343...')
  })

  it('updateTitle if title is odd and length not greator than 55  ' , () =>{
      
    component.quickLinks = {
      data: [{
        destination: linkDestinationMock,
        displayOrder: -11,
        id: '5bf3c940c9e77c0001238a52',
        svg: '<symbol id="0169fbe3-ff05-3910-94bf-13a07fa2ba16"</symbol>',
        title: 'BBC'
      }],
      showExpanded: false,
      title: 'quick-links',
      sportId: 1231231,
      _id: '12313 '
    } as any;
    const quickLink = {
      destination: linkDestinationMock,
      displayOrder: -11,
      id: '5bf3c940c9e77c0001238a52',
      svg: '<symbol id="0169fbe3-ff05-3910-94bf-13a07fa2ba16"</symbol>',
      title: 'South Africa v England Cricket'
    }
    component.updateTitle(quickLink);
    expect(component.updateTitle(quickLink)).toEqual('South Africa v England Cricket')
  })

  it('updateTitle if title index is not odd and length greator than 24 ' , () =>{
      
    component.quickLinks = {
      data: [{
        destination: linkDestinationMock,
        displayOrder: -11,
        id: '5bf3c940c9e77c0001238a52',
        svg: '<symbol id="0169fbe3-ff05-3910-94bf-13a07fa2ba16"</symbol>',
        title: 'BBC'
      },
      {
        destination: linkDestinationMock,
        displayOrder: -11,
        id: '5bf3c940c9e77c0001238a57777',
        svg: '<symbol id="0169fbe3-ff05-3910-94bf-13a07fa2ba16"</symbol>',
        title: 'BBC'
      }],
      showExpanded: false,
      title: 'quick-links',
      sportId: 1231231,
      _id: '12313 '
    } as any;
    const quickLink = {
      destination: linkDestinationMock,
      displayOrder: -11,
      id: '5bf3c940c9e77c0001238a52',
      svg: '<symbol id="0169fbe3-ff05-3910-94bf-13a07fa2ba16"</symbol>',
      title: 'South Africa v England Cricket'
    }
    component.updateTitle(quickLink);
    expect(component.updateTitle(quickLink)).toEqual('South Africa v England C...')
  })
  it('updateTitle if title index is not odd and length not greator than 24 ' , () =>{
      
    component.quickLinks = {
      data: [{
        destination: linkDestinationMock,
        displayOrder: -11,
        id: '5bf3c940c9e77c0001238a52',
        svg: '<symbol id="0169fbe3-ff05-3910-94bf-13a07fa2ba16"</symbol>',
        title: 'BBC'
      }],
      showExpanded: false,
      title: 'quick-links',
      sportId: 1231231,
      _id: '12313 '
    } as any;
    const quickLink = {
      destination: linkDestinationMock,
      displayOrder: -11,
      id: '5bf3c940c9e77c0001238a52',
      svg: '<symbol id="0169fbe3-ff05-3910-94bf-13a07fa2ba16"</symbol>',
      title: 'South Africa v England'
    }
    component.updateTitle(quickLink);
    expect(component.updateTitle(quickLink)).toEqual('South Africa v England')
  })

  it('updateTitle if title index is not last item and length not greator than 24 ' , () =>{
      
    component.quickLinks = {
      data: [{
        destination: linkDestinationMock,
        displayOrder: -11,
        id: '5bf3c940c9e77c0001238a52',
        svg: '<symbol id="0169fbe3-ff05-3910-94bf-13a07fa2ba16"</symbol>',
        title: 'BBC'
      },{
        destination: linkDestinationMock,
        displayOrder: -11,
        id: '5bf3c940c9e77c0001238a52',
        svg: '<symbol id="0169fbe3-ff05-3910-94bf-13a07fa2ba16"</symbol>',
        title: 'BBC'
      },
    ],
      showExpanded: false,
      title: 'quick-links',
      sportId: 1231231,
      _id: '12313 '
    } as any;
    const quickLink = {
      destination: linkDestinationMock,
      displayOrder: -11,
      id: '5bf3c940c9e77c0001238a52333',
      svg: '<symbol id="0169fbe3-ff05-3910-94bf-13a07fa2ba16"</symbol>',
      title: 'South Africa v England'
    }
    component.updateTitle(quickLink);
    expect(component.updateTitle(quickLink)).toEqual('South Africa v England')
  })

  it('updateTitle if title index is not last item and length not greator than 24 ' , () =>{
      
    component.quickLinks = {
      data: undefined,
      showExpanded: false,
      title: 'quick-links',
      sportId: 1231231,
      _id: '12313 '
    } as any;
    const quickLink = {
      destination: linkDestinationMock,
      displayOrder: -11,
      id: '5bf3c940c9e77c0001238a52333',
      svg: '<symbol id="0169fbe3-ff05-3910-94bf-13a07fa2ba16"</symbol>',
      title: 'South Africa v England'
    }
    component.updateTitle(quickLink);
    expect(component.updateTitle(quickLink)).toEqual('South Africa v England')
  })
});
