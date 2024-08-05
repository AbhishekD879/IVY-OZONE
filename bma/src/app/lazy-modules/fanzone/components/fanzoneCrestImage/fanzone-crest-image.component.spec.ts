
import { FanzoneCrestImageComponent } from '@app/lazy-modules/fanzone/components/fanzoneCrestImage/fanzone-crest-image.component';

import { TEAM_ASSET_DATA } from '@app/fanzone/mockdata/fanzone-select-your-team.component.mock';

describe('FanzoneCrestImageComponent', () => {
  let component: FanzoneCrestImageComponent;

  beforeEach(() => {
    component = new FanzoneCrestImageComponent();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should check if team image to not exists', () => {
    component.team = {} as any;
    component.ngOnInit();
    const isTeamImageExist = component.checkForTeamsImageData();
    expect(isTeamImageExist).toEqual(false);
  })

  it('should check if team image exists', () => {
    component.team = TEAM_ASSET_DATA;
    component.ngOnInit();
    const isTeamImageExist = component.checkForTeamsImageData();
    expect(isTeamImageExist).toEqual(true);
  })
});
