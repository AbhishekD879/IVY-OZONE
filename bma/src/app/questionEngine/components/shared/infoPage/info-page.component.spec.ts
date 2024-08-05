import { InfoPageComponent } from './info-page.component';
import { of } from 'rxjs';

describe('InfoPageComponent', () => {
  let component: InfoPageComponent;


  const qeDataObj = {
    live: {
      quickLinks: [
        {
          title: 'Prizes',
          relativePath: 'prizes',
          description: '<h2>Prizes</h2>'
        },
        {
          title: 'Frequently Asked Questions',
          relativePath: 'faq',
          description: '<h2>FAQ</h2>'
        }
      ]
    }
  };

  const questionEngineService = {
    qeData: {
      baseQuiz: {
        sourceId: '/correct4',
        quickLinks: [
          {
            title: 'Prizes',
            relativePath: 'prizes',
            description: '<h2>Prizes</h2>'
          },
          {
            title: 'Frequently Asked Questions',
            relativePath: 'faq',
            description: '<h2>FAQ</h2>'
          }
        ]
      }
    },
    resolvePath: jasmine.createSpy('resolvePath').and.returnValue('/qe/cash_v3'),
    getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(qeDataObj)),
    mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel')
  };

  const domSanitizer = {
    bypassSecurityTrustHtml: (value) => value,
  };

  const activatedRoute = {
    snapshot: {
      paramMap: {
        get: jasmine.createSpy('get').and.returnValue('prizes')
      }
    }
  };

  const localeService = {
    getString: jasmine.createSpy('getString'),
  };

  const router = {
    navigateByUrl: jasmine.createSpy('navigateByUrl'),
  };

  const routingState = {
    getPreviousUrl: jasmine.createSpy('getPreviousUrl').and.returnValue('/correct4/after'),
  };

  beforeEach(() => {
    component = new InfoPageComponent(
      questionEngineService as any,
      domSanitizer as any,
      activatedRoute as any,
      localeService as any,
      router as any,
      routingState as any
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should init component and check pageIdFromRoute', () => {
    component.ngOnInit();

    expect(component['pageIdFromRoute']).toEqual('prizes');
    expect(component.infoPageContent).toBeDefined();
  });

  it('should init component when pageIdFromRoute is not defined', () => {
    component['activatedRoute'] = {
      ...activatedRoute,
      snapshot: {
        paramMap: {
          get: jasmine.createSpy('get').and.returnValue(null)
        }
      }
    } as any;
    component['questionEngineService'] = {
      ...questionEngineService,
      qeData: {
        baseQuiz : {
          quickLinks: [
            {
              title: 'Prizes',
              relativePath: 'prizes',
              description: ''
            },
            {
              title: 'Frequently Asked Questions',
              relativePath: 'faq',
              description: ''
            }
          ]
        }
      },
      getQuizHistory: jasmine.createSpy('getQuizHistory'),
      mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel')
    } as any;

    component.pageIdFromRoute = null;
    component.ngOnInit();

    expect(component.infoPageContent).toEqual(null);
  });

  it('should init component when qeData is not defined', () => {
    component['activatedRoute'] = {
      ...activatedRoute,
      snapshot: {
        paramMap: {
          get: jasmine.createSpy('get').and.returnValue(null)
        }
      }
    } as any;

    component['questionEngineService'] = {
      ...questionEngineService,
      qeData: null,
      getQuizHistory: jasmine.createSpy('getQuizHistory'),
      mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel')
    } as any;
    component.ngOnInit();

    expect(component.infoPageContent).not.toBeDefined();
  });

  describe('Testing `goBack` method', () => {

    it('should redirect to previous url', () => {
      component.goBack();
      expect(router.navigateByUrl).toHaveBeenCalledWith('/correct4/after');
    });

    it('should redirect to QE splash page', () => {

      component['questionEngineService'].qeData.baseQuiz.sourceId = '/cash_v3';

      component.goBack();

      expect(router.navigateByUrl).toHaveBeenCalledWith('/qe/cash_v3');
    });

    it('should redirect to `correct4` QE splash page', () => {
      component['questionEngineService'] = {
        ...questionEngineService,
        qeData: {
          ...questionEngineService.qeData,
          baseQuiz: {
            ...questionEngineService.qeData.baseQuiz,
            sourceId: null
          }
        }
      } as any;
      component['questionEngineService'].qeData.baseQuiz.sourceId = '/cash_v3';

      component.goBack();
      expect(router.navigateByUrl).toHaveBeenCalledWith('/qe/cash_v3');
    });
  });

});
