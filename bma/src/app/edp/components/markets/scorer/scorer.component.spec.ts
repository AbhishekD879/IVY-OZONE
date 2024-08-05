//import { ScorerComponent } from "@root/platforms/ladbrokesMobile/edp/components/markets/scorer/scorer.component";

import { ScorerComponent } from "./scorer.component";

describe('ScorerComponent', () => {
    let component: ScorerComponent;

    beforeEach(() => {
        component = new ScorerComponent(
            
          );
    });
    describe('ngOnInit', () => {
    it('should get teamH', () => {
        component.eventEntity={name:'ManUtd v Liverpool'} as any;
        component.marketsGroup = { header:false,outcomes:[{originalOutcomeMeaningMinorCode:'H',teamName:'',name:'No Goalscorer'}]} as any;
        component.ngOnInit();
        expect(component.teamH).toEqual('ManUtd');
       // expect(component.marketsGroup.outcomes.teamName).toEqual('ManUtd');
      });
      it('should get teamA', () => {
        component.eventEntity={name:'ManUtd v Liverpool'} as any
        component.marketsGroup = { header: false,outcomes:[{originalOutcomeMeaningMinorCode:'A',teamName:''}]} as any;
        component.ngOnInit();
        component.env='bma'
       /// expect(component.allPlayers).toEqual(component.marketsGroup.outcomes);
       expect(component.teamA).toEqual('Liverpool');
       expect(component.marketCount).toEqual(5);
      });

      it('should get', () => {
        component.eventEntity={name:'ManUtd v Liverpool'} as any
        component.groupPlayers=[];
        component.env='bma'
        component.marketsGroup = { header: true,noGoalscorer:[{ id: 1 }, { id: 2 }],outcomes:[{originalOutcomeMeaningMinorCode:'A',teamName:''}]} as any;
        component.ngOnInit();
        expect(component.allPlayers).toEqual([]);
        expect(component.marketCount).toEqual(5);
      });

      it('should get market count for ladbrokes', () => {
        component.eventEntity={name:'ManUtd v Liverpool'} as any
        component.groupPlayers=[];
        component.marketsGroup = { header: true,noGoalscorer:[{ id: 1 }, { id: 2 }],outcomes:[{originalOutcomeMeaningMinorCode:'A',teamName:''}]} as any;
        component.env='Ladbrokes'
        component.ngOnInit();
        expect(component.allPlayers).toEqual([]);
        expect(component.marketCount).toEqual(5);
      });
    });


    describe('selectedOutcomes', () => {
        let outcomes;
    
        beforeEach(() => {
          outcomes = [{ id: 1 }, { id: 2 }, { id: 3 }, { id: 4 },{id:5}] as any;
        });
    
        it('should slice outcomes by marketCount', () => {
          component.limitCount = 0;
          const result = component.selectedOutcomes(outcomes);
    
          expect(result.length).toEqual(5);
        });
    });

    describe('selectedNoGoalOutcomes', () => {
        let outcomes;
    
        beforeEach(() => {
          outcomes = [{ id: 1 }, { id: 2 }, { id: 3 }, { id: 4 },{id:5}] as any;
        });
    
        it('should slice outcomes by marketCount', () => {
          component.limitCount = 0;
          const result = component.selectedNoGoalOutcomes(outcomes);
    
          expect(result.length).toEqual(outcomes.length);
        });
    });

    describe('toggleShow', () => {
          
        it('should toggle isAllShow from true to false', () => {
          component.isAllShow = false;
          component.allPlayers=[{id:1},{id:2},{id:3},{id:4},{id:5},{id:6}] as any
          component.toggleShow();
          expect(component.isAllShow).toEqual(true);
        });
    
        it('should toggle isAllShow from false to true', () => {
          component.isAllShow = true;
          component.toggleShow();
          expect(component.isAllShow).toEqual(false);
        });
    
        it('should limitCount as marketCount', () => {
          component.isAllShow = true;
          component.marketCount=5
          component.toggleShow();
          expect(component.limitCount).toEqual(5);
        });
      });
});