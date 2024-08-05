import environment from './environment';

describe('environment.spec', () => {
  it('should set exact app version that in package.json', () => {
    expect(environment.production).toEqual(true);
  });
});
