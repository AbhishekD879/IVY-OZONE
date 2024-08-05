import { DialogService } from '@core/services/dialogService/dialog.service';
import { ComponentFactory, ComponentFactoryResolver, ComponentRef, ViewContainerRef } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { OxygenDialogComponent } from './oxygen-dialog.component';
import { Subject } from 'rxjs';
import { IDialogEvent } from '@core/services/dialogService/dialog-params.model';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';

function createDialogRefStub() {
  return Object.assign({}, {
    instance: {
      closeDialog() {},
      open() {
      },
      setParams(_) {
      },
      params: {}
    },
    destroy() {}
  }) as ComponentRef<AbstractDialogComponent>;
}

describe('OxygenDialogComponent', () => {
  let component: OxygenDialogComponent;
  let dialogServiceStub: Partial<DialogService>;
  let componentFactoryResolverStub: Partial<ComponentFactoryResolver>;
  let pubSubServiceStub: Partial<PubSubService>;

  let openedModalStub: Subject<IDialogEvent>;


  beforeEach(() => {
    openedModalStub = new Subject();

    dialogServiceStub = {
      modalListener: openedModalStub.asObservable()
    };
    componentFactoryResolverStub = {
      resolveComponentFactory(_) { return {}; }
    } as ComponentFactoryResolver;
    pubSubServiceStub = {
      publish(channel, channelFunctionArguments, isAsync) { },
      API: { NEW_DIALOG_OPENED: 'opened' }
    };

    function createComponent(): OxygenDialogComponent {
      component = new OxygenDialogComponent(
        dialogServiceStub as DialogService,
        componentFactoryResolverStub as ComponentFactoryResolver,
        pubSubServiceStub as PubSubService
      );
      component.dialogContainerProvider = {
        viewContainerRef: {
          createComponent(_) { }
        } as ViewContainerRef
      };
      return component;
    }

    component = createComponent();
  });

  afterEach(() => {
    // destroy and remove subscriptions
    component.ngOnDestroy();
  });

  describe('constructor', () => {
    it('should have injected services', () => {
      expect(component).toBeTruthy();
      expect(component['dialogService']).toBeTruthy();
      expect(component['componentFactoryResolver']).toBeTruthy();
      expect(component['pubSubService']).toBeTruthy();
    });

    it('should initialize solidOverlay as false', () => {
      expect(component.solidOverlay).toBe(false);
    });

    it('should initialize dialogTypes as empty Map', () => {
      expect(component['dialogTypes'] instanceof Map).toBeTruthy();
      expect(component['dialogTypes'].size).toBe(0);
    });

    it('should initialize dialogRefs as empty Map', () => {
      expect(component['dialogRefs'] instanceof Map).toBeTruthy();
      expect(component['dialogRefs'].size).toBe(0);
    });

    it('should initialize destroyed as Subject', () => {
      expect(component['destroyed$'] instanceof Subject).toBeTruthy();
    });
  });

  describe('ngOnInit', () => {
    it('should subscribe to "DialogService.modalListener"', () => {
      const spy = spyOn(dialogServiceStub.modalListener, 'subscribe');

      component.ngOnInit();

      expect(spy).toHaveBeenCalled();
    });
  });

  describe('ngOnDestroy', () => {
    it('should emit destroyed$ Subject when component destroys', () => {
      const spy = spyOn(component['destroyed$'], 'next');

      component.ngOnDestroy();

      expect(spy).toHaveBeenCalledWith(null);
      expect(spy).toHaveBeenCalled();
    });
  });

  describe('processes events from DialogService', () => {
    let event: IDialogEvent;

    describe('when event.type === "open"', () => {
      beforeEach(() => {
        component['dialogTypes'] = new Map([['registered', {} as ComponentFactory<AbstractDialogComponent>]]);
        component['dialogRefs'] = new Map();
        component.ngOnInit();

        event = {
          type: 'open',
          forceCloseOther: false,
        };
      });

      describe('dialog with event.name is not registered', () => {
        beforeEach(() => {
          event = Object.assign({}, event, {
            name: 'new',
          });
        });

        describe('and does not contain a new component', () => {
          beforeEach(() => {
            event = Object.assign({}, event, {
              component: null,
            });
          });

          it('should not add a dialog to "dialogRefs" if a dialog with an event.name is not registered', () => {
            openedModalStub.next(event);

            expect(component['dialogRefs'].has('new')).toBeFalsy();
          });
        });

        describe('but contain a new component', () => {
          beforeEach(() => {
            event = Object.assign({}, event, {
              component: {}
            });
            spyOn(component['viewContainerRef'], 'createComponent').and.returnValue(createDialogRefStub());
          });

          it('should add a new component to dialogTypes (register a new dialog)', () => {
            openedModalStub.next(event);

            expect(component['dialogTypes'].has('new')).toBeTruthy();
          });
        });
      });

      describe('dialog with event.name is already registered', () => {

        beforeEach(() => {
          event = Object.assign({}, event, {
            name: 'registered',
            params: {
              one: 1,
              two: 2,
            }
          });
          spyOn(component['viewContainerRef'], 'createComponent').and.returnValue(createDialogRefStub());
        });

        it('should set a value of solidOverlay property from event', () => {
          event = Object.assign({}, event, {
            solidOverlay: true,
          });

          openedModalStub.next(event);

          expect(component.solidOverlay).toBe(true);
        });

        it('should create a new dialog (add to dialogRefs)', () => {
          openedModalStub.next(event);

          expect(component['dialogRefs'].has(event.name)).toBeTruthy();
        });

        it('should open the new dialog', () => {
          const ref = component['getDialog'](event.name);
          const spy = spyOn(ref, 'open');

          openedModalStub.next(event);

          expect(spy).toHaveBeenCalled();
        });

        it('should set params to the new dialog', () => {
          const ref = component['getDialog'](event.name);
          const spy = spyOn(ref, 'setParams');

          openedModalStub.next(event);

          expect(spy).toHaveBeenCalledWith(event.params);
        });


        it('should publish to pubSub', () => {
          const spy = spyOn(pubSubServiceStub, 'publish');

          openedModalStub.next(event);

          expect(spy).toHaveBeenCalledWith(pubSubServiceStub.API.NEW_DIALOG_OPENED);
        });
      });
    });

    describe('when event.type === "close"', () => {
      const dialogRef = createDialogRefStub();

      beforeEach(() => {
        component['dialogTypes'] = new Map([['registered', null]]);
        component['dialogRefs'] = new Map([['registered', dialogRef]]);
        component.ngOnInit();

        event = {
          type: 'close',
          forceCloseOther: false,
          name: 'registered'
        };
      });

      it('should call a method "closeDialog" of the dialog instance', () => {
        const spy = spyOn(dialogRef.instance, 'closeDialog');

        openedModalStub.next(event);

        expect(spy).toHaveBeenCalled();
      });

      it('should destroy the dialog', () => {
        const spy = spyOn(dialogRef, 'destroy');

        openedModalStub.next(event);

        expect(spy).toHaveBeenCalled();
      });

      it('should remove the dialog from dialogRefs', () => {
        openedModalStub.next(event);

        expect(component['dialogRefs'].has('registered')).toBeFalsy();
      });

      it('should not change "dialogRefs" if the dialog is not created', () => {
        event = Object.assign({}, event, {
          name: 'notRegistered',
        });
        const amountOfCreatedDialogs = component['dialogRefs'].size;

        openedModalStub.next(event);

        expect(component['dialogRefs'].size).toBe(amountOfCreatedDialogs);
      });

      it('should close dialog even if it is persistent', () => {
        component['dialogRefs'] = new Map([
          ['persistent', createDialogRefStub()]
        ]);
        component['dialogRefs'].get('persistent').instance.params = { isPersistent: true };

        event = {
          type: 'close',
          forceCloseOther: false,
          name: 'persistent'
        };

        openedModalStub.next(event);
        expect(component['dialogRefs'].has('persistent')).toBeFalsy();
      });
    });

    describe('when event.type === "closeAll"', () => {
      beforeEach(() => {
        component['dialogTypes'] = new Map([['registered', null]]);
        component['dialogRefs'] = new Map([['registered', createDialogRefStub()]]);
        component.ngOnInit();

        event = {
          type: 'closeAll',
          forceCloseOther: false,
        };
      });

      it('should close all dialogs', () => {
        openedModalStub.next(event);
        expect(component['dialogRefs'].size).toBe(0);
      });

      it('Should not close persistent dialog', () => {
        component['dialogRefs'] = new Map([
          ['registered', createDialogRefStub()],
          ['persistent', createDialogRefStub()]
        ]);

        component['dialogRefs'].get('persistent').instance.params = { isPersistent: true };

        openedModalStub.next(event);
        expect(component['dialogRefs'].size).toBe(1);
      });
    });

    describe('when event.type === "register"', () => {
      beforeEach(() => {
        component['dialogTypes'] = new Map([['registered', null]]);
        component['dialogRefs'] = new Map();
        component.ngOnInit();

        event = {
          type: 'register',
          name: 'new',
          forceCloseOther: false,
          params: {
            dialog: {}
          }
        };
      });

      it('should register a new dialog (add to dialogTypes)', () => {
        openedModalStub.next(event);

        expect(component['dialogTypes'].has('new')).toBeTruthy();
      });
    });

    describe('when event.forceCloseOther === true', () => {
      beforeEach(() => {
        component['dialogTypes'] = new Map([['registered', null]]);
        component['dialogRefs'] = new Map([['first', createDialogRefStub()], ['second', createDialogRefStub()]]);
        component.ngOnInit();

        event = {
          type: 'open',
          forceCloseOther: true,
          name: 'first'
        };
      });

      it('should close all dialogs except "first"', () => {
        openedModalStub.next(event);

        expect(component['dialogRefs'].size).toBe(1);
        expect(component['dialogRefs'].has('first')).toBeTruthy();
      });
    });
  });

});
