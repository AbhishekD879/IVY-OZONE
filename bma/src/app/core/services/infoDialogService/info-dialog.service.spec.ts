import { dialogIdentifierDictionary } from '../../constants/dialog-identifier-dictionary.constant';
import { InfoDialogService } from './info-dialog.service';

describe('InfoDialogService', () => {
  let service: InfoDialogService;
  let dialogService;

  beforeEach(() => {
    dialogService = {
      openDialog: jasmine.createSpy('openDialog'),
      closeDialog: jasmine.createSpy('closeDialog'),
      closeDialogs: jasmine.createSpy('closeDialogs'),
      ids: dialogIdentifierDictionary,
      openedPopups: () => {}
    };

    service = new InfoDialogService(dialogService);
  });

  it('openOkDialog shortcut should fill in other params', () => {
    spyOn(service, 'openInfoDialog');
    service.openOkDialog('text');

    expect(service.openInfoDialog).toHaveBeenCalledWith(
      undefined,
      'text',
      'simpleDialog',
      undefined,
      undefined,
      [{
        caption: 'OK',
        cssClass: 'btn-style2 okButton'
      }]
    );
  });

  it('openInfoDialog', () => {
    service.openInfoDialog('caption', 'text');
    expect(dialogService.openDialog).toHaveBeenCalledTimes(1);
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      'informationDialog',
      jasmine.anything(),
      true,
      {
        caption: 'caption',
        text: 'text',
        dialogClass: undefined,
        buttons: undefined,
        links: undefined,
        hideCrossIcon: undefined,
        onBeforeClose: jasmine.anything(),
        compName: undefined,
        label: undefined
      }
    );
  });

  it('closePopUp', () => {
    service.closePopUp();
    expect(dialogService.closeDialogs).toHaveBeenCalledTimes(1);
  });

  it('openLogoutPopup', () => {
    service.openLogoutPopup();
    expect(dialogService.closeDialogs).toHaveBeenCalledTimes(1);
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      dialogService.ids.sessionLimitLogout,
      jasmine.anything(),
      true
    );
  });

  it('openConnectionLostPopup', () => {
    service.openConnectionLostPopup();
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      dialogService.ids.connectLost,
      jasmine.anything(),
      true
    );
  });

  it('closeConnectionLostPopup', () => {
    service.closeConnectionLostPopup();
    expect(dialogService.closeDialog).not.toHaveBeenCalled();

    dialogService.openedPopups = { connectionLost: true };
    service.closeConnectionLostPopup();
    expect(dialogService.closeDialog).toHaveBeenCalledWith(dialogService.ids.connectLost);
  });
});
