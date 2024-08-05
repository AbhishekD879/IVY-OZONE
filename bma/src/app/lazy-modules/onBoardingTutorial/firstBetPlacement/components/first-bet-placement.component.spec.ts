import { NavigationEnd } from "@angular/router";
import { of } from "rxjs";
import { OnBoardingFirstBetComponent } from "./first-bet-placement.component";


describe('OnBoardingFirstBetComponent', () => {
  let component: OnBoardingFirstBetComponent;
  let pubSubService, session, cdr, windowRef,firstBetGAService,userService,  router, location;

  beforeEach(() => {
    windowRef = {    
      document: {
        getElementById: jasmine.createSpy().and.returnValue({ classList: {
          add: jasmine.createSpy('add'),
          remove: jasmine.createSpy('remove')
        }}),
        querySelector: jasmine.createSpy('querySelector').and.returnValue({
          click:()=>{} }),
        createElement: jasmine.createSpy('createElement'),
      }
    }
    pubSubService = {
        publish: jasmine.createSpy(),
        API: {
            FIRST_BET_PLACEMENT_TUTORIAL: 'FIRST_BET_PLACEMENT_TUTORIAL'
        }
      };
      session = {
        set: jasmine.createSpy('set'),
          get: jasmine.createSpy('get').and.callFake(
            n => {
              if(n === 'initialTabLoaded') { return {url:''}} 
              else if(n === 'betPlaced') { return true}
              else if(n=== 'firstBetTutorialAvailable'){ return true}
              else if(n === 'firstBetTutorial') {return {user:'test'}}
            else if(n === 'firstBetPlacementDetails'){ return {betDetails:{cashOut:{title:'',description:'',buttonDesc:''}}}  }
          }), 
        remove : jasmine.createSpy('remove')
      };
      cdr = {
        detectChanges: jasmine.createSpy('detectChanges')
      };
      firstBetGAService = {
        setGtmData: jasmine.createSpy('setGtmData'),
      };
      userService={};

      router = {
        events: of(new NavigationEnd(1, '/', '/')),
      };
      location = {
        path: jasmine.createSpy().and.returnValue('')
      };
    component = new OnBoardingFirstBetComponent(
        session,pubSubService, cdr, windowRef,firstBetGAService, userService,  router, location
    );

  });

  it('should create component instance', () => {
    component.onBoardingData={step:'betPlaced',type:'cashOut'}
    component.activeStep={step:1,totalSteps:5};
    component.tutorialSteps={myBets:{'step':1,totalSteps:5}} as any;
    session.get.and.returnValue({betPlaced:{},url:''});
    component.activeStep.step =5
    component.ngOnInit();
    expect(component).toBeTruthy();
    expect(cdr.detectChanges).toHaveBeenCalled();
  });
  
  it('should create component instance cashOut', () => {
    component.onBoardingData={step:'betDetails',type:'cashOut'}
    component.activeStep={step:1,totalSteps:5};
    component.tutorialSteps={betDetails:{'step':1,totalSteps:5},myBets:{'step':1,totalSteps:5}} as any;
    component.activeStep.step =5
    location.path.and.returnValue('/open-bet');
    session.get.and.callFake(
          n => {
            if(n === 'initialTabLoaded') { return {url:'/open-bet'}} 
            else if(n === 'betPlaced') { return true}
            else if(n=== 'firstBetTutorialAvailable'){ return true}
            else if(n === 'firstBetTutorial') {return {user:'test'}}
            else if(n === 'firstBetPlacementDetails'){ return {betDetails:{cashOut:{title:'',description:''}},brand: 'ladbrokes'}  }
        })
    component.ngOnInit();
    expect(component).toBeTruthy();
    expect(cdr.detectChanges).toHaveBeenCalled();
  });
  it('should create component instance elese condition', () => {
    component.onBoardingData={step:'myBets',type:'cashOut'}
    session.get.and.returnValue({myBets:{cashOut:{title:"test cashout",description:"test descritpion"},buttonDesc:'NEXT'}});
    component.ngOnInit();
    expect(component).toBeTruthy();
    expect(cdr.detectChanges).toHaveBeenCalled();
  });

  it('should create component instance elese condition without button text', () => {
    component.onBoardingData={step:'myBets',type:'cashOut'}
    session.get.and.returnValue({myBets:{cashOut:{title:"test cashout",description:"test descritpion"}}});
    component.ngOnInit();
    expect(component).toBeTruthy();
    expect(cdr.detectChanges).toHaveBeenCalled();
  });

  it('clicked undo', () => { 
    component.activeStep={step:1,totalSteps:5};
    component.openUndo();
    expect(component.isCloseTutorial).toBeTruthy();
  });

  it('clicked dismiss', () => {
    session.get.and.returnValue({user:'test'});
    component.firstBetTutorialData={button:{leftButtonDesc:'test button'}} as any;
    component.activeStep={step:1,totalSteps:5};
    component.dismiss();
    expect(component.isCloseTutorial).toBeFalse();
  });

  it('clicked done', () => {
    component.activeStep={step:1,totalSteps:5};
    component.buttonText='DONE'
    component.firstBetTutorialData  = {myBets:{buttonDesc:'NEXT'}} as any;
    component.handleNextClick();
    expect(component.isCloseTutorial).toBeFalse();
  });

  it('clicked next', () => {
    component.buttonText='NEXT';
    component.activeStep={step:1,totalSteps:5};
    component.firstBetTutorialData  = {myBets:{buttonDesc:'NEXT'}} as any;
    component.handleNextClick();
    expect(session.remove).toHaveBeenCalled();
  });

  it('clicked next else with qb-header close btn class', () => {
    const element = document.createElement('div')
    session.get.and.returnValue({user:'test'});
    element.className='qb-header-close-btn';
    component.buttonText='NEXT';
    
    component.activeStep={step:1,totalSteps:5};
    component.firstBetTutorialData  = {myBets:{buttonDesc:'TEST'}} as any;
    component.handleNextClick();
    expect(component.activeStep).toBeDefined();
  });

  it('on clicked next sidebar-close show step4 default', () => {
    component.activeStep={step:4,totalSteps:5};
    session.get.and.returnValue({user:'test'});
    component.firstBetTutorialData  = {myBets:{buttonDesc:'TEST'}} as any;
    windowRef.document.querySelector = jasmine.createSpy()
    .withArgs('.sidebar-close').and.returnValue({
      click:()=>{} })
    .withArgs('.qb-header-close-btn').and.returnValue(null)
    session.get.and.returnValue( false );
    component.buttonText='NEXT';
    component.handleNextClick();
    expect(component.activeStep.step).toBe(4);
  });

  it('on clicking next sidebar-close show step4 cashout', () => {
    component.activeStep={step:4,totalSteps:5};
    session.get.and.returnValue({user:'test'});
    component.firstBetTutorialData  = {myBets:{buttonDesc:'TEST'}} as any;
    windowRef.document.querySelector = jasmine.createSpy()
    .withArgs('.sidebar-close').and.returnValue({
      click:()=>{} })
    .withArgs('.qb-header-close-btn').and.returnValue(null)
    session.get.and.returnValue( true );
    component.buttonText='NEXT';
    component.handleNextClick();
    expect(component.activeStep.step).toBe(4);
  });

  it('ngOnChanges onBoardingData data to be defined', () => {
    component.activeStep={step:1,totalSteps:5};
    component.tutorialSteps={myBets:{'step':1,totalSteps:5}} as any;
    session.get.and.returnValue({betPlaced:{},url:''});
    component.activeStep.step = 5;
    component.ngOnChanges({onBoardingData:{currentValue:{step: 'betPlaced'}}} as any);
    expect(component.onBoardingData).toBeDefined();
  });
  
  it('ngOnChanges canBoostSelection should always false', () => {
    component.activeStep={step:1,totalSteps:5};
    component.tutorialSteps={myBets:{'step':1,totalSteps:5}} as any;
    session.get.and.returnValue({betPlaced:{},url:''});
    component.activeStep.step = 5;
    component.ngOnChanges({onBoardingData:{currentValue:{step: 'betPlaced', type: 'boost'}}} as any);
    expect(component.onBoardingData).toBeDefined();
    expect(component.canBoostSelection).toBeFalse();
  });

  it('ngOnChanges isDigitKeyboardShown shown', () => {
    component.isExpanded=false;
    component.activeStep={step:1,totalSteps:5};
    component.ngOnChanges({isDigitKeyboardShown:true} as any);
    expect(cdr.detectChanges).toHaveBeenCalled();
  });

  it(' onExpand shown', () => {
    component.isExpanded=true;
    component.activeStep={step:1,totalSteps:5};
    component.expand(false);  
    expect(component.accordionHeader).toBe('Step 1/5');
  });

  it('close tutorial', () => {
    component.activeStep={step:1,totalSteps:5};
    component.firstBetTutorialData={button:{leftButtonDesc:'test button'}} as any;
    component.closeUndo();
    expect(component.isCloseTutorial).toBeFalse();
  });

  it('call ngOnDestroy', () => {
    component['routeListener'] = { unsubscribe: jasmine.createSpy() } as any;
    component.ngOnDestroy();
    expect(component['routeListener'].unsubscribe).toHaveBeenCalledTimes(1);
  });
});
