import { PlaceBetDocService } from './place-bet-doc.service';

describe('PlaceBetDocService', () => {
  let service: PlaceBetDocService;
  let betFactoryService;
  let legFactoryService;
  let betErrorService;

  beforeEach(() => {
    betFactoryService = {};
    legFactoryService = {};
    betErrorService = {};

    service = new PlaceBetDocService(
      betFactoryService,
      legFactoryService,
      betErrorService
    );
  });

  it('content', () => {
    const data = {
      doc: jasmine.createSpy('doc').and.returnValue({}),
      legs: [{
        doc: jasmine.createSpy('leg.doc')
      }]
    };
    service.content(data);
    expect(data.doc).toHaveBeenCalled();
    expect(data.legs[0].doc).toHaveBeenCalled();
  });
});
