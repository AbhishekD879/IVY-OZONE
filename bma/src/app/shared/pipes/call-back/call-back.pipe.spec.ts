import { CallBackPipe } from '@shared/pipes/call-back/call-back.pipe';

describe('CallBackPipe', () => {
  let pipe;
  const callbackMockFunc = {
    mockfunc: jasmine.createSpy('handler').and.returnValue('transforming function'),
    };

  beforeEach(() => {
    pipe = new CallBackPipe();
  });

  it('should transform the function', () => {
    expect(pipe.transform('name', callbackMockFunc.mockfunc, this)).toEqual('transforming function');
  });

  it('should not transform the function', () => {
    expect(pipe.transform('name', callbackMockFunc.mockfunc, null)).toEqual('transforming function');
  });
});
