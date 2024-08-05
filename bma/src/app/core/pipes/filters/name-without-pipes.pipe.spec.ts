import { NameWithoutPipesPipe } from './name-without-pipes.pipe';

describe('NameWithoutPipes', () => {
  let pipe;
  let filtersService;

  beforeEach(() => {
    filtersService = {
      removeLineSymbol: jasmine.createSpy('removeLineSymbol')
    };
    pipe = new NameWithoutPipesPipe(filtersService);
  });

  it('should call bypassSecurityTrustHtml', () => {
    pipe.transform('test');
    expect(filtersService.removeLineSymbol).toHaveBeenCalledWith('test');
  });

});


