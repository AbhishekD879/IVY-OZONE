import { FiveASideRole } from './five-a-side-role.class';

describe('#FiveASideRole', () => {
  let instance;
  let bet;
  let selection;
  let matrixItem;
  let selectionWithColours;

  beforeEach(() => {
    selection = {
      name: 'D. Beckham',
      id: 7,
      teamColors: {
        primaryColour: '#777',
        secondaryColour: '#675d5d'
      }
    };

    selectionWithColours = {
      teamColors: {
        primaryColour: '#fff',
        secondaryColour: '#000',
        teamsImage: '',
      }
    };

    matrixItem = {
      statId: 10,
      stat: 'To Concede'
    };

    bet = {
      updateBet: jasmine.createSpy('updateBet')
    };

    instance = new FiveASideRole(
      selection as any,
      matrixItem as any,
      bet as any,
      1
    );
  });

  it('should init instance', () => {
    expect(instance).toBeTruthy();
    expect(instance.playerId).toEqual(7);
    expect(instance.playerName).toEqual('D. Beckham');
    expect(instance.statId).toEqual(10);
    expect(instance.statValue).toEqual(1);
    expect(instance.hasConflict).toBeFalsy();
    expect(instance.playerIconBackground).toEqual('linear-gradient(to right, #777 50%, #675d5d 50%)');
  });

  it('should set background for player with team colours', () => {
    const instanceWithColours = new FiveASideRole(
      selectionWithColours as any,
      matrixItem as any,
      bet as any,
      1
    );
    expect(instanceWithColours.playerIconBackground).toEqual('linear-gradient(to right, #fff 50%, #000 50%)');
  });

  it('should set empty string for the teamsImage', () => {
    const instanceWithColours = new FiveASideRole(
      selectionWithColours as any,
      matrixItem as any,
      bet as any,
      1
    );
    expect(instanceWithColours.teamsImage).toBe('');
  });

  it('should  set image string for the teamsImage', () => {
    const TEAMSIMAGEPATH = {
      imagepath: 'https://cms.ladbrokes.com/image1.svg',
      filename: 'image1.svg'
    };
    selectionWithColours.teamColors.teamsImage = TEAMSIMAGEPATH;
    const instanceWithColours = new FiveASideRole(
      selectionWithColours as any,
      matrixItem as any,
      bet as any,
      1
    );
    expect(instanceWithColours.teamsImage).toBe('https://cms.coral.co.uk/cms//images/uploads/svg/image1.svg');
  });

  it('setConflict should set hasConflict prop to true', () => {
    instance.hasConflict = false;
    instance.setConflict();
    expect(instance.hasConflict).toBeTruthy();
  });

  it('resetConflict should set hasConflict prop to true', () => {
    instance.hasConflict = true;
    instance.resetConflict();
    expect(instance.hasConflict).toBeFalsy();
  });

  describe('changeStatValue', () => {
    it('should change stat value if it more the 0 ' +
      'and not call betUpdate if second parameter false', () => {
      instance.changeStatValue(5, false);
      expect(instance.statValue).toEqual(5);
      expect(bet.updateBet).not.toHaveBeenCalled();
    });
    it('should change stat value if it more the 0 and call betUpdate', () => {
      instance.changeStatValue(7);
      expect(instance.statValue).toEqual(7);
      expect(bet.updateBet).toHaveBeenCalled();
    });
  });

  describe('#getMarketName', () => {
    it('should return correct market for To Be Carded', () => {
      instance.role.stat = 'To Be Carded';
      instance.statValue = 1;
      const result = instance.getMarketName();

      expect(result).toEqual('To Be Carded');
    });
    it('should return correct market for To Keep A Clean Sheet', () => {
      instance.role.stat = 'To Keep A Clean Sheet';
      instance.statValue = 1;
      const result = instance.getMarketName();

      expect(result).toEqual('To Keep A Clean Sheet');
    });
    it('should return correct market for To Concede if value > 0', () => {
      instance.role.stat = 'To Concede';
      instance.statValue = 1;
      const result = instance.getMarketName();

      expect(result).toEqual('To Concede 1+ Goals');
    });
    it('should return correct market for To Concede if value = 0', () => {
      instance.role.stat = 'To Concede';
      instance.statValue = 0;
      const result = instance.getMarketName();

      expect(result).toEqual('To Keep A Clean Sheet');
    });
    it('should return correct market for Assists', () => {
      instance.role.stat = 'Assists';
      instance.statValue = 2;
      const result = instance.getMarketName();

      expect(result).toEqual('2+ Assists');
    });
  });
  describe('#getShortHandMarketTitle', () => {
    it('should return correct market for Shots Outside', () => {
      instance.role.stat = 'Shots Outside The Box';
      instance.statValue = 1;
      const result = instance.getShortHandMarketTitle();

      expect(result).toEqual('1+ Shots Outside');
    });
    it('should return correct market for goals inside', () => {
      instance.role.stat = 'Goals Inside The Box';
      instance.statValue = 1;
      const result = instance.getShortHandMarketTitle();

      expect(result).toEqual('1+ Goals Inside');
    });
    it('should return correct market for goals outside the box', () => {
      instance.role.stat = 'Goals Outside The Box';
      instance.statValue = 1;
      const result = instance.getShortHandMarketTitle();

      expect(result).toEqual('1+ Goals Outside');
    });
    it('should return correct market for To Concede if value = 0', () => {
      instance.marketTitle = 'To Keep A Clean Sheet';
      instance.role.stat = 'To Concede';
      instance.statValue = 2;
      const result = instance.getShortHandMarketTitle();

      expect(result).toEqual('To Keep A Clean Sheet');
    });
    it('should return correct market, if role.stat is null', () => {
      instance.marketTitle = 'To Keep A Clean Sheet';
      instance.role.stat = null;
      instance.statValue = 2;
      const result = instance.getShortHandMarketTitle();

      expect(result).toEqual('To Keep A Clean Sheet');
    });
  });

});
