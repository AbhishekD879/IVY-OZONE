import { AnswersSummaryComponent } from './answers-summary.component';
import { QEData } from '@app/questionEngine/services/qe-mock-data.mock';
import { QuestionEngineService } from '@questionEngine/services/question-engine/question-engine.service';

describe('AnswersSummaryComponent', () => {
  let component: AnswersSummaryComponent;
  let questionEngineService;
  const { qeData } = new QEData();

  beforeEach(() => {
    questionEngineService = {
      trackEventGA: jasmine.createSpy('trackEventGA')
    };
    component = new AnswersSummaryComponent(
      questionEngineService as QuestionEngineService
    );
    component.quiz = qeData.baseQuiz;
  });

  it('should create AnswersSummaryComponent', () => {
    expect(component).toBeTruthy();
  });

  it('should populate scores', () => {
    expect(component).toBeTruthy();
    component.ngOnInit();
    expect(component['homeTeamScore']).toBe(1);
    expect(component['awayTeamScore']).toBe(2);
  });

  it('should not populate scores', () => {
    expect(component).toBeTruthy();
    component.quiz.eventDetails.actualScores = [];
    component.ngOnInit();
    expect(component['homeTeamScore']).not.toBeDefined();
  });

  describe('Test method showHomeTeamScore', () => {
    it('showHomeTeamScore', () => {
      component['homeTeamScore'] = 0;

      expect(component.showHomeTeamScore).toBe(true);
    });

    it('showHomeTeamScore', () => {
      component['homeTeamScore'] = null;

      expect(component.showHomeTeamScore).toBe(false);
    });
  });

  describe('Test method showAwayTeamScore', () => {
    it('showAwayTeamScore', () => {
      component['awayTeamScore'] = 0;

      expect(component.showAwayTeamScore).toBe(true);
    });

    it('showAwayTeamScore', () => {
      component['awayTeamScore'] = null;

      expect(component.showAwayTeamScore).toBe(false);
    });
  });

  it('should call questionSummaryHandler function', () => {
    const questionsList = [{
      answers: [
        {
          'correctAnswer': true,
          'id': 'f48f1116-d00e-4559-ae54-82315b66a2ee',
          'nextQuestionId': '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78',
          'questionAskedId': '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
          'text': 'Tottenham',
          'userChoice': true
        }, {
          'correctAnswer': true,
          'id': 'f48f1116-d00e-4559-ae54-82315b66a2ee',
          'nextQuestionId': '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78',
          'questionAskedId': '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
          'text': 'Tottenham',
          'userChoice': true
        }
      ]
    }];
    component.ngOnInit();
    component['questionSummaryHandler'](questionsList);

    expect(component.correctAnswerCounter).toBeDefined();
    expect(component.correctAnswerResult).toBeDefined();
    expect(component['quizSummary']).toBeTruthy();
  });

  it('should call questionSummaryHandler when userChoice and correctAnswer are false', () => {
    const questionsList = [{
      answers: [
        {
          'correctAnswer': false,
          'id': 'f48f1116-d00e-4559-ae54-82315b66a2ee',
          'nextQuestionId': '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78',
          'questionAskedId': '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
          'text': 'Tottenham',
          'userChoice': false
        }, {
          'correctAnswer': false,
          'id': 'f48f1116-d00e-4559-ae54-82315b66a2ee',
          'nextQuestionId': '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78',
          'questionAskedId': '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
          'text': 'Tottenham',
          'userChoice': false
        }
      ]
    }];
    component.ngOnInit();
    component['questionSummaryHandler'](questionsList);

    expect(component['quizSummary']).toEqual([]);
    expect(component.correctAnswerCounter).toEqual(0);
  });

  it('should call prizeIndicator() and set results according to the answers', () => {
    component.ngOnInit();
    component['prizeIndicator']( component.quiz.correctAnswersPrizes , component.correctAnswerCounter);
    expect(component.correctAnswerResult).toBeDefined();

    component.ngOnInit();
    component['prizeIndicator']( component.quiz.correctAnswersPrizes , 4);

    expect(component['prize']).toBeTruthy();
    expect(component.prizeResult).toBeTruthy();
  });

  it('should call checkCorrectAnswerResult() and set results according to the correctAnswerCounter', () => {
    component.correctAnswerCounter = 2;
    const questionsList = [
      {
        'correctAnswer': true,
        'id': 'f48f1116-d00e-4559-ae54-82315b66a2ee',
        'nextQuestionId': '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78',
        'questionAskedId': '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
        'text': 'Tottenham',
        'userChoice': true
      }, {
      'correctAnswer': true,
      'id': 'f48f1116-d00e-4559-ae54-82315b66a2ee',
      'nextQuestionId': '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78',
      'questionAskedId': '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
      'text': 'Tottenham',
      'userChoice': true
      }];

    component.ngOnInit();
    component['checkCorrectAnswerResult'](questionsList);

    expect(component.correctAnswerResult).toEqual('won');

    component.correctAnswerCounter = 1;
    component.ngOnInit();

    expect(component.correctAnswerResult).toEqual('');
  });

  it('trackByFn', () => {
    const index = 5;
    const output = '5';
    expect(component.trackByFn(index)).toBe(output);
  });

  it('should call hasDefaultQuestionsDetailsInfo and return', () => {
    expect(component.hasDefaultQuestionsDetailsInfo()).toBe(true);
  });

  it('should call hasDefaultQuestionsDetailsInfo and return true if one property is present', () => {
    component.quiz.defaultQuestionsDetails.topRightHeader = null;
    expect(component.hasDefaultQuestionsDetailsInfo()).toBe(true);
  });

  it('should call hasDefaultQuestionsDetailsInfo and return false', () => {
    component.quiz.defaultQuestionsDetails.topLeftHeader = null;
    component.quiz.defaultQuestionsDetails.topRightHeader = null;
    expect(component.hasDefaultQuestionsDetailsInfo()).not.toBe(true);
  });

  describe('Testing `toggleGameSummaryInfo`', () => {
    it('should call toggleGameSummaryInfo and track `View Game Summary --> Expand`', () => {
      component.toggleGameSummaryInfo();

      expect(component.gameSummaryState).toEqual(true);
      expect(questionEngineService.trackEventGA).toHaveBeenCalledWith('View Game Summary', 'Expand');
    });

    it('should call toggleGameSummaryInfo and track `View Game Summary --> Collapse`', () => {
      component.gameSummaryState = true;
      component.toggleGameSummaryInfo();

      expect(component.gameSummaryState).toEqual(false);
      expect(questionEngineService.trackEventGA).toHaveBeenCalledWith('View Game Summary', 'Collapse');
    });
  });

  it('should call hasDefaultQuestionsDetailsInfo', () => {
    component.quiz = null;
    component.ngOnInit();

    expect(component.validSummary).toBe(false);
  });
});
