import { CompetitionModuleDirective } from '@app/bigCompetitions/directives/competition-module.directive';

describe('CompetitionModuleDirective', () => {
  let viewContainerRef;

  beforeEach(() => {
    viewContainerRef = {};
  });

  it('CompetitionModuleDirective, should be', () => {
    expect(new CompetitionModuleDirective(viewContainerRef).viewContainerRef).toBeTruthy();
  });
});
