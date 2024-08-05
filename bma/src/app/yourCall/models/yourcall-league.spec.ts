import { YourCallLeague } from './yourcall-league';

describe('#YourCallLeague', () => {
  let model: YourCallLeague;

  beforeEach(() => {
    model = new YourCallLeague(
      12345,
      'title',
      1,
      {
        byb: true,
        id: 12
      }
    );
  });

  it('should create model', () => {
    expect(model).toBeTruthy();
    // getters
    expect(model.obTypeId).toEqual(12345);
    expect(model.title).toEqual('title');
    expect(model.status).toEqual(1);
    expect(model.byb).toEqual(true);
    expect(model.id).toEqual(12);
  });
});
